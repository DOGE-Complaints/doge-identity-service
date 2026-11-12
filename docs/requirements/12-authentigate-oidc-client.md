# 12. Authentigate OIDC Client

> **Статус:** НЕ реализовано. Spec для `src/core/auth/authentigate_client.py`.
> **Предусловие:** Файл 07 (env vars: AUTHENTIGATE_*) настроен.
> **Связь:** Вызывается из файла 11 (eID flow) на шагах 7-8.

---

## Что делает этот модуль

`authentigate_client.py` инкапсулирует всё взаимодействие с Authentigate OIDC:

1. **Discovery** — загрузка и кэширование OpenID configuration endpoint.
2. **JWKS** — загрузка и кэширование публичных ключей для ID token validation.
3. **Code exchange** — обмен authorization code на tokens через `/token` endpoint.
4. **ID token validation** — верификация подписи, claims, nonce.
5. **Claims extraction** — извлечение `personal_code`, `personal_code_country`.

---

## Authentigate Endpoints

### Production
```
Discovery: https://id.authentigate.eu/.well-known/openid-configuration
JWKS:      https://id.authentigate.eu/.well-known/jwks
Token:     https://id.authentigate.eu/token
Authorize: https://id.authentigate.eu/authorize
```

### Demo (SK ID Solutions sandbox)
```
Discovery: https://oidc.demo.sk.ee/.well-known/openid-configuration
```

### Dev / Local (Mock OIDC)
```
Discovery: http://localhost:8080/.well-known/openid-configuration
```

Все endpoints получаются динамически через discovery, не хардкодятся в коде (кроме issuer URL).

---

## PKCE S256 — требования

Authentigate требует PKCE с `code_challenge_method=S256`.

```python
import secrets
import hashlib
import base64

# Генерация (в /auth/eid/start):
code_verifier = secrets.token_urlsafe(48)  # 64 символа, > min 43
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode("ascii")).digest()
).rstrip(b"=").decode("ascii")

# Хранение:
# code_verifier — шифруем AES-GCM → DB
# code_verifier_hash = hashlib.sha256(code_verifier.encode()).hexdigest()  — для audit

# Использование (в /auth/eid/callback, шаг 7):
# POST /token:  code_verifier=<decrypted_from_db>
# НЕ code_verifier_hash!
```

---

## Спецификация модуля

```python
# src/core/auth/authentigate_client.py

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticateEidClaims:
    personal_code: str          # never stored; used only to generate hash
    personal_code_country: str  # "EE" | "LV" | "LT"
    auth_method: str | None     # "smart_id" | "mobile_id" | "id_card"


class OIDCError(Exception):
    """Raised when OIDC flow fails (network, validation, claims)."""


class AuthenticateClient:
    """OIDC client for Authentigate. Thread-safe, caches JWKS."""

    def __init__(
        self,
        issuer: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scopes: str,
        http_client: httpx.AsyncClient,
    ) -> None: ...

    async def discover(self) -> OIDCConfiguration:
        """Fetch and cache /.well-known/openid-configuration."""
        ...

    async def exchange_code(
        self,
        code: str,
        code_verifier: str,  # MUST be plaintext verifier, not hash
    ) -> TokenResponse:
        """
        POST /token: authorization_code grant with PKCE.
        Returns id_token + access_token.
        Raises OIDCError on HTTP error or token validation failure.
        """
        ...

    async def validate_id_token(
        self,
        id_token: str,
        nonce: str,
    ) -> AuthenticateEidClaims:
        """
        Validate ID token signature, claims, and nonce.
        Extract only required claims.
        Raises OIDCError if validation fails.
        """
        ...

    async def fetch_jwks(self) -> dict:
        """Fetch and cache JWKS. Cache TTL: 1 hour."""
        ...
```

---

## ID Token Validation (шаг 8 callback)

**Обязательные проверки:**

| Check | Что проверяем |
|-------|-------------|
| Signature | Подпись RS256/ES256 через JWKS от Authentigate |
| `iss` | Должен совпадать с `AUTHENTIGATE_ISSUER` |
| `aud` | Должен содержать `AUTHENTIGATE_CLIENT_ID` |
| `exp` | `exp > now()` |
| `iat` | `iat <= now() + 5s` (clock skew tolerance) |
| `nonce` | Должен совпадать с `nonce` из сессии |
| `sub` | Не пустой |

**Claims extraction:**
```python
claims = {
    "personal_code":         token_payload["personal_code"],
    "personal_code_country": token_payload["personal_code_country"],
    "auth_method":           token_payload.get("amr", [None])[0],  # "smartid" etc
}
```

**После extraction немедленно:**
- Передать в `verified_person_hasher.py` для генерации hash.
- Не логировать `personal_code`.
- Не хранить `personal_code` или `id_token`.

---

## Scopes запрашиваемые у Authentigate

```
openid personal_code personal_code_country
```

**НЕ запрашиваем (privacy policy):**
```
given_name  family_name  name  birthdate
```

---

## Mock OIDC для разработки

До получения Authentigate credentials — использовать `mock-oauth2-server`:

```bash
docker run -p 8080:8080 ghcr.io/navikt/mock-oauth2-server:latest
```

Mock конфигурация (токены возвращают нужные claims):
```json
{
  "interactiveLogin": true,
  "tokenCallbacks": [{
    "issuerId": "default",
    "requestMappings": [{
      "requestParam": "scope",
      "match": "personal_code",
      "claims": {
        "personal_code": "38501010000",
        "personal_code_country": "EE"
      }
    }]
  }]
}
```

Переключение на реальный Authentigate:
```env
# dev (mock):
AUTHENTIGATE_ISSUER=http://localhost:8080

# demo (SK ID Solutions sandbox):
AUTHENTIGATE_ISSUER=https://oidc.demo.sk.ee

# production:
AUTHENTIGATE_ISSUER=https://id.authentigate.eu
```

Код `authentigate_client.py` не меняется — только env vars.

---

## HTTP client настройки

```python
# Timeout для OIDC calls — из AppConfig (req-07 OIDC_REQUEST_TIMEOUT_S, default 10)
# httpx timeout=config.oidc_request_timeout_s

# JWKS cache TTL
JWKS_CACHE_TTL_S = 3600  # 1 hour

# Retry policy: нет автоматического retry для token exchange
# (idempotency не гарантирована)
```

---

## Acceptance Criteria

- [ ] `exchange_code(code, code_verifier)` — успешный обмен возвращает `TokenResponse` с id_token
- [ ] `validate_id_token(id_token, nonce)` — валидный токен возвращает `AuthenticateEidClaims`
- [ ] `validate_id_token(expired_token, nonce)` → `OIDCError`
- [ ] `validate_id_token(wrong_nonce_token, nonce)` → `OIDCError`
- [ ] `validate_id_token(wrong_iss_token, nonce)` → `OIDCError`
- [ ] `personal_code` НИГДЕ не логируется (audit log содержит только `success=true/false`)
- [ ] Mock OIDC flow работает end-to-end с `AUTHENTIGATE_ISSUER=http://localhost:8080`
