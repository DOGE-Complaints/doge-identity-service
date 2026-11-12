# 18. eID Easy Provider

> **Статус:** НЕ реализовано. Spec для `src/core/providers/eideasy/`.
> **Предусловие:** Файл 17 (provider abstraction) — реализует `EIDProviderPort`.
> **Активация:** `EID_PROVIDER=eideasy` в env.
> **Связь:** Файл 07 (env vars — добавить EIDEASY_*), Файл 08 (migrations — `provider_session_data`), Файл 13 (subject_hash).

---

## Протокол

eID Easy использует **OAuth2 Authorization Code Flow** (НЕ OIDC):
- Нет PKCE, нет nonce, нет ID token, нет JWKS.
- CSRF защита через `state` (random token, server-side хранение).
- После callback: code → access_token → user_data (три отдельных HTTP запроса).

```
SPA: window.location.href = redirect_url (из /auth/eid/start)
        ↓
eID Easy: /oauth/authorize
        ↓  (user authenticates)
eID Easy: redirect → /auth/eideasy/callback?code=...&state=...
        ↓
Backend: validate state → exchange code → fetch user_data → generate subject_hash
        ↓
Backend: conflict detection → mark eid_verified=true → redirect SPA to return_url
```

---

## Env vars (добавить в файл 07)

| Переменная | Required | Default | Описание |
|-----------|----------|---------|---------|
| `EID_PROVIDER` | Yes | `mock` | Активный провайдер: `eideasy` \| `authentigate` \| `mock` |
| `DOGESTONIA_EID_SECRET` | Yes (prod) | — | HMAC-SHA256 ключ для генерации `subject_hash`. Поле AppConfig: `eid_secret` |
| `NODE_ID` | No | `tallinn` | Идентификатор ноды для multi-node (будущее) |
| `EIDEASY_ENV` | No | `test` | `test` или `production` |
| `EIDEASY_BASE_URL` | No | `https://test.eideasy.com` | Base URL. Production: `https://id.eideasy.com` |
| `EIDEASY_CLIENT_ID` | Yes (eideasy) | — | Client ID из eID Easy портала |
| `EIDEASY_CLIENT_SECRET` | Yes (eideasy) | — | Client Secret (только backend, никогда frontend) |
| `EIDEASY_REDIRECT_URI` | Yes (eideasy) | — | Зарегистрированный callback. Production: `https://identity.dogestonia.ee/auth/eideasy/callback` |
| `EIDEASY_ALLOWED_METHODS` | No | `ee-id-login,mid-login,smartid` | Разрешённые методы идентификации |
| `EIDEASY_DEFAULT_COUNTRY` | No | `EE` | Страна по умолчанию |
| `EIDEASY_ALLOWED_COUNTRIES` | No | `EE` | Разрешённые страны (MVP = только EE) |

### `example.env` фрагмент (добавить):

```env
# ── eID Provider ────────────────────────────────────────────────────────────
EID_PROVIDER=mock
DOGESTONIA_EID_SECRET=
NODE_ID=tallinn

# ── eID Easy (заполнить при EID_PROVIDER=eideasy) ─────────────────────────
EIDEASY_ENV=test
EIDEASY_BASE_URL=https://test.eideasy.com
EIDEASY_CLIENT_ID=
EIDEASY_CLIENT_SECRET=
EIDEASY_REDIRECT_URI=http://localhost:8100/auth/eideasy/callback
EIDEASY_ALLOWED_METHODS=ee-id-login,mid-login,smartid
EIDEASY_DEFAULT_COUNTRY=EE
EIDEASY_ALLOWED_COUNTRIES=EE
```

---

## Структура файлов

```
src/core/providers/eideasy/
├── __init__.py
├── config.py      ← EIDEasyConfig dataclass (из AppConfig)
├── client.py      ← HTTP вызовы к eID Easy endpoints
├── state_store.py ← DB-backed state store (anti-CSRF)
└── provider.py    ← EIDEasyProvider implements EIDProviderPort
```

---

## `src/core/providers/eideasy/config.py`

```python
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class EIDEasyConfig:
    base_url: str
    client_id: str
    client_secret: str
    redirect_uri: str
    allowed_methods: frozenset[str]
    default_country: str
    allowed_countries: frozenset[str]

    @classmethod
    def from_app_config(cls) -> EIDEasyConfig:
        from src.core.config.schema import app_config
        cfg = app_config()
        return cls(
            base_url=cfg.eideasy_base_url,
            client_id=cfg.eideasy_client_id,
            client_secret=cfg.eideasy_client_secret,
            redirect_uri=cfg.eideasy_redirect_uri,
            allowed_methods=frozenset(cfg.eideasy_allowed_methods.split(",")),
            default_country=cfg.eideasy_default_country,
            allowed_countries=frozenset(cfg.eideasy_allowed_countries.split(",")),
        )


ALLOWED_LANGS: frozenset[str] = frozenset({"en", "et", "ru"})
```

---

## `src/core/providers/eideasy/client.py`

```python
from __future__ import annotations
import hashlib
import hmac
import secrets
from urllib.parse import urlencode

import httpx

from src.core.providers.eideasy.config import EIDEasyConfig, ALLOWED_LANGS
from src.core.providers.base import EIDVerificationResult


class EIDEasyHTTPError(Exception):
    def __init__(self, step: str, status: int):
        super().__init__(f"eideasy {step} failed: HTTP {status}")
        self.step = step
        self.status = status


class EIDEasyUserDataError(Exception):
    """Данные от eID Easy не прошли валидацию."""
    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


def build_authorize_url(
    config: EIDEasyConfig,
    *,
    state: str,
    method: str | None = None,
    lang: str = "en",
) -> str:
    if lang not in ALLOWED_LANGS:
        lang = "en"

    params: dict[str, str] = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "state": state,
        "country": config.default_country,
        "lang": lang,
        "allow_country_change": "false",
    }

    if method is not None:
        if method not in config.allowed_methods:
            raise ValueError(f"Unsupported eID Easy method: {method!r}")
        params["start"] = method

    return f"{config.base_url}/oauth/authorize?{urlencode(params)}"


async def exchange_code_for_token(config: EIDEasyConfig, code: str) -> str:
    """POST /oauth/access_token → access_token."""
    url = f"{config.base_url}/oauth/access_token"
    data = {
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "redirect_uri": config.redirect_uri,
        "code": code,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.post(
            url,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    if resp.status_code >= 400:
        raise EIDEasyHTTPError("token_exchange", resp.status_code)

    payload = resp.json()
    token = payload.get("access_token")
    if not token:
        raise EIDEasyHTTPError("token_missing", 0)

    # SECURITY: access_token не логируется, не сохраняется
    return token


async def fetch_user_data(config: EIDEasyConfig, access_token: str) -> dict:
    """GET /api/v2/user_data → user_data dict."""
    url = f"{config.base_url}/api/v2/user_data"
    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.get(url, headers={"Authorization": f"Bearer {access_token}"})
    if resp.status_code >= 400:
        raise EIDEasyHTTPError("user_data", resp.status_code)

    # SECURITY: полный ответ не логируется (содержит PII)
    return resp.json()


def validate_user_data(
    config: EIDEasyConfig,
    user_data: dict,
    hash_secret: str,
    node_id: str,
) -> EIDVerificationResult:
    """
    Валидирует данные от eID Easy и возвращает провайдер-агностичный результат.
    raw idcode используется только для HMAC — после этого выбрасывается.
    """
    from datetime import datetime, timezone

    status = user_data.get("status")
    country = user_data.get("country")
    idcode = user_data.get("idcode")
    login_method = user_data.get("current_login_method")

    if status != "OK":
        raise EIDEasyUserDataError(f"status={status!r}")
    if country not in config.allowed_countries:
        raise EIDEasyUserDataError(f"country={country!r} not allowed")
    if not idcode:
        raise EIDEasyUserDataError("idcode missing")
    if login_method not in config.allowed_methods:
        raise EIDEasyUserDataError(f"method={login_method!r} not allowed")

    # HMAC: raw idcode используется здесь и нигде больше
    message = f"eideasy:{country}:{idcode}".encode("utf-8")
    key = hash_secret.encode("utf-8")
    subject_hash = hmac.new(key, message, hashlib.sha256).hexdigest()
    # idcode выходит из scope после этой функции — не возвращается

    return EIDVerificationResult(
        provider="eideasy",
        country=country,
        subject_hash=subject_hash,
        login_method=login_method,
        verified_at=datetime.now(timezone.utc),
    )
```

---

## `src/core/providers/eideasy/state_store.py`

```python
from __future__ import annotations
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import psycopg

STATE_TTL_MINUTES = 10


@dataclass
class EIDEasyState:
    state: str
    supabase_user_id: str
    return_url: str
    return_context: str
    method: str | None
    created_at: datetime


class EIDEasyStateStore:
    """
    DB-backed state store для OAuth2 CSRF protection.
    State хранится в eid_verification_sessions.provider_session_data JSONB.
    TTL = 10 минут. State consume-once (удаляется при чтении).
    """

    def __init__(self, conn: psycopg.AsyncConnection):
        self._conn = conn

    async def create(
        self,
        *,
        supabase_user_id: str,
        return_url: str,
        return_context: str,
        method: str | None,
    ) -> EIDEasyState:
        state = secrets.token_urlsafe(32)
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=STATE_TTL_MINUTES)

        await self._conn.execute(
            """
            INSERT INTO eid_verification_sessions
              (id, supabase_user_id, state, return_url, return_context,
               status, provider, provider_session_data, created_at, expires_at)
            VALUES
              (gen_random_uuid(), %s, %s, %s, %s, 'started', 'eideasy',
               %s::jsonb, now(), %s)
            """,
            (
                supabase_user_id, state, return_url, return_context,
                # provider_session_data: только метод (нет PKCE/nonce)
                f'{{"oauth_state": "{state}", "method": {repr(method)}}}',
                expires_at,
            ),
        )

        return EIDEasyState(
            state=state,
            supabase_user_id=supabase_user_id,
            return_url=return_url,
            return_context=return_context,
            method=method,
            created_at=now,
        )

    async def consume(self, state: str) -> EIDEasyState | None:
        """
        Возвращает и удаляет state (one-time use).
        Возвращает None если state не найден, истёк, или уже использован.
        """
        async with self._conn.transaction():
            rows = await self._conn.execute(
                """
                DELETE FROM eid_verification_sessions
                WHERE state = %s
                  AND provider = 'eideasy'
                  AND status = 'started'
                  AND expires_at > now()
                RETURNING
                  supabase_user_id, return_url, return_context,
                  provider_session_data, created_at
                """,
                (state,),
            )
            row = await rows.fetchone()

        if row is None:
            return None

        return EIDEasyState(
            state=state,
            supabase_user_id=row[0],
            return_url=row[1],
            return_context=row[2],
            method=row[3].get("method"),
            created_at=row[4],
        )
```

---

## `src/core/providers/eideasy/provider.py`

```python
from __future__ import annotations
import psycopg
from datetime import datetime, timedelta, timezone

from src.core.providers.base import EIDProviderPort, EIDVerificationResult, EIDStartResult
from src.core.providers.eideasy.config import EIDEasyConfig
from src.core.providers.eideasy.client import (
    build_authorize_url,
    exchange_code_for_token,
    fetch_user_data,
    validate_user_data,
    EIDEasyHTTPError,
    EIDEasyUserDataError,
)
from src.core.providers.eideasy.state_store import EIDEasyStateStore


class EIDEasyProviderError(Exception):
    def __init__(self, code: str, message: str = ""):
        super().__init__(message)
        self.code = code  # machine-readable: "invalid_state" | "verification_failed" | etc.


class EIDEasyProvider:
    """
    Реализует EIDProviderPort для eID Easy OAuth2 flow.
    Создаётся per-request через FastAPI Depends.
    """

    def __init__(self, conn: psycopg.AsyncConnection | None = None):
        self._config = EIDEasyConfig.from_app_config()
        self._conn = conn  # injected by Depends; None в unit тестах

    @property
    def provider_name(self) -> str:
        return "eideasy"

    @property
    def callback_path(self) -> str:
        return "/auth/eideasy/callback"

    async def start_flow(
        self,
        *,
        supabase_user_id: str,
        return_url: str,
        return_context: str,
        requested_action: str,
        method: str | None = None,
        lang: str = "en",
    ) -> EIDStartResult:
        store = EIDEasyStateStore(self._conn)
        session = await store.create(
            supabase_user_id=supabase_user_id,
            return_url=return_url,
            return_context=return_context,
            method=method,
        )
        redirect_url = build_authorize_url(
            self._config,
            state=session.state,
            method=method,
            lang=lang,
        )
        return EIDStartResult(
            redirect_url=redirect_url,
            session_id=session.state,  # используем state как session identifier
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
        )

    async def handle_callback(
        self,
        *,
        raw_params: dict[str, str],
    ) -> tuple[EIDVerificationResult, str]:
        error = raw_params.get("error")
        if error:
            # Пользователь отменил или ошибка на стороне eID Easy
            raise EIDEasyProviderError("verification_cancelled", f"eideasy error: {error}")

        code = raw_params.get("code")
        state = raw_params.get("state")

        if not code or not state:
            raise EIDEasyProviderError("invalid_callback", "missing code or state")

        # Consume state (one-time, validates TTL)
        store = EIDEasyStateStore(self._conn)
        session = await store.consume(state)
        if session is None:
            raise EIDEasyProviderError("invalid_state", "state not found or expired")

        # Exchange code for access_token
        try:
            access_token = await exchange_code_for_token(self._config, code)
        except EIDEasyHTTPError as e:
            raise EIDEasyProviderError("token_exchange_failed", str(e))

        # Fetch user_data
        try:
            user_data = await fetch_user_data(self._config, access_token)
        except EIDEasyHTTPError as e:
            raise EIDEasyProviderError("user_data_failed", str(e))
        finally:
            # access_token больше не нужен — явно обнуляем
            access_token = None  # noqa: F841

        # Validate and normalize (raw idcode → subject_hash)
        from src.core.config.schema import app_config
        cfg = app_config()
        try:
            result = validate_user_data(
                self._config,
                user_data,
                hash_secret=cfg.eid_secret,
                node_id=cfg.node_id,
            )
        except EIDEasyUserDataError as e:
            raise EIDEasyProviderError("verification_failed", str(e))
        finally:
            # user_data содержит PII (idcode, name, birth_date) — не хранить
            user_data = None  # noqa: F841

        return result, session.return_url
```

---

## Callback route registration

В `src/core/api/asgi_app.py` добавить router с eideasy callback:

```python
# Импорт в asgi_app.py:
from src.core.api.routes.eid_callback import router as eid_callback_router

# В create_app():
app.include_router(eid_callback_router)
```

`eid_callback_router` содержит:
- `GET /auth/eideasy/callback` — eideasy callback (файл 17)
- `GET /auth/mock/callback` — mock callback (dev)
- `GET /auth/authentigate/callback` — authentigate callback (будущее)

---

## Изменения в DB schema (дополнение к файлу 08)

Новая миграция (после `20260525000002`):

```sql
-- 20260526000001_eid_sessions_provider_abstraction.sql

-- Добавить provider и provider_session_data
ALTER TABLE public.eid_verification_sessions
  ADD COLUMN IF NOT EXISTS provider TEXT NOT NULL DEFAULT 'eideasy',
  ADD COLUMN IF NOT EXISTS provider_session_data JSONB NOT NULL DEFAULT '{}';

-- Сделать PKCE поля nullable (обратная совместимость, нужны только для Authentigate)
ALTER TABLE public.eid_verification_sessions
  ALTER COLUMN nonce DROP NOT NULL,
  ALTER COLUMN code_verifier_encrypted DROP NOT NULL,
  ALTER COLUMN code_verifier_hash DROP NOT NULL;

-- Индекс
CREATE INDEX IF NOT EXISTS idx_eid_sessions_provider
  ON public.eid_verification_sessions (provider);
```

---

## Регистрация credentials в eID Easy портале

```
My Webpages → Register new webpage

Homepage URL:
  https://dogestonia.ee

Redirect URI:
  https://identity.dogestonia.ee/auth/eideasy/callback

Для test environment:
  Redirect URI: http://localhost:8100/auth/eideasy/callback
```

**Test environment:** `https://test.eideasy.com` — credentials отдельные от production.

---

## Smart-ID тестовый пользователь (EE)

```
EE test idcode: 30303039914
```

Ожидаемый ответ `user_data`:

```json
{
  "idcode": "30303039914",
  "lastname": "Testnumber",
  "firstname": "Ok",
  "birth_date": "1903-03-03",
  "country": "EE",
  "status": "OK",
  "current_login_method": "smartid"
}
```

Наша система использует только: `status`, `country`, `idcode → HMAC`, `current_login_method`.

---

## Тест-кейсы (имена функций)

```python
# tests/providers/eideasy/test_eideasy_provider.py

test_start_flow_creates_state_in_db
test_start_flow_returns_correct_authorize_url
test_start_flow_includes_country_ee
test_start_flow_with_method_smartid_includes_start_param
test_start_flow_rejects_unsupported_method

test_handle_callback_rejects_missing_code
test_handle_callback_rejects_missing_state
test_handle_callback_rejects_invalid_state
test_handle_callback_rejects_expired_state
test_handle_callback_rejects_on_error_param
test_handle_callback_consumes_state_once          # повторный вызов с тем же state → None

# tests/providers/eideasy/test_eideasy_client.py

test_exchange_code_success
test_exchange_code_http_error_raises
test_fetch_user_data_success
test_fetch_user_data_http_error_raises
test_validate_user_data_ok
test_validate_user_data_rejects_non_ok_status
test_validate_user_data_rejects_non_ee_country
test_validate_user_data_rejects_missing_idcode
test_validate_user_data_rejects_unsupported_method
test_validate_user_data_returns_hmac_not_raw_idcode
test_validate_user_data_does_not_store_name_or_birthdate
```

---

## Security checklist (eideasy-специфично)

- [ ] `client_secret` только в backend env, никогда в frontend
- [ ] `access_token` не логируется, не хранится (выбрасывается после `user_data`)
- [ ] `idcode`, `firstname`, `lastname`, `birth_date` не логируются, не хранятся
- [ ] State consume-once: повторный callback с тем же state → отклоняется
- [ ] State TTL = 10 минут
- [ ] Только country=EE разрешена в MVP
- [ ] `EIDEASY_REDIRECT_URI` в production = HTTPS
- [ ] `DOGESTONIA_EID_SECRET` не коммитится в репо

---

## Acceptance Criteria

- [ ] `EID_PROVIDER=eideasy` + корректные EIDEASY_* → `/auth/eid/start` создаёт state, возвращает eideasy authorize URL
- [ ] eideasy authorize URL содержит `client_id`, `redirect_uri`, `response_type=code`, `state`, `country=EE`
- [ ] `/auth/eideasy/callback?code=...&state=...` → валидирует state → обменивает code → fetches user_data
- [ ] При `country != "EE"` в user_data → `EIDEasyProviderError("verification_failed")`
- [ ] При `idcode` отсутствующем в user_data → `EIDEasyProviderError("verification_failed")`
- [ ] `subject_hash` = `HMAC_SHA256(DOGESTONIA_EID_SECRET, "eideasy:EE:{idcode}")` — hex digest
- [ ] `firstname`, `lastname`, `birth_date` не записываются в DB
- [ ] `access_token` обнуляется после `user_data` запроса
- [ ] `EID_PROVIDER=mock` → работает без EIDEASY_* (mock provider)
- [ ] Smart-ID тест user (EE `30303039914`) проходит в test environment
