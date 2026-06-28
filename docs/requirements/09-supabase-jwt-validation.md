# 09. Supabase JWT Validation

> **Статус:** реализовано (актуализировано 2026-06-24). Код: `src/core/auth/supabase_validator.py` и `src/core/api/security.py`.
> **Предусловие:** `SUPABASE_JWT_SECRET` или JWKS endpoint настроен (файл 07).
> **Связь:** Используется во всех protected endpoints (/me, /auth/eid/start, /stories, /oauth/authorize).
> **Аудит:** G-5 закрыт SEC-03 (2026-06-26) — `aud` + форма импорта ключа согласованы с кодом.

---

## Зачем нужна своя JWT validation

Supabase Auth выдаёт access tokens (JWT) при login. Identity-service должен:
1. Проверить подпись токена — убедиться, что токен выдан нашим Supabase проектом.
2. Проверить срок действия — `exp` claim.
3. Извлечь `sub` — `supabase_user_id` (UUID пользователя).

**Важно:** Frontend session existence alone НЕ является доверенным источником. Каждый HTTP request должен нести валидный JWT и быть верифицирован независимо.

---

## Алгоритмы подписи Supabase JWT

### HS256 (Supabase Cloud, стандарт)
- JWT подписан симметричным секретом `SUPABASE_JWT_SECRET`.
- Суpabase Dashboard → Settings → API → JWT Secret.
- Простая валидация: `joserfc.jwt.decode(token, key=SUPABASE_JWT_SECRET, algorithms=["HS256"])`.

### ES256 / RS256 (Supabase Cloud, JWKS)
- JWT подписан асимметричным ключом Supabase (типично **ES256** в Cloud).
- JWKS endpoint: `{SUPABASE_URL}/auth/v1/.well-known/jwks.json`
- Валидация через `JwksCache` (тот же паттерн, что OIDC id_token): `ES256`, `RS256`, `ES384`, `ES512`.
- Алгоритм выбирается по JWT header `alg`; при unknown `kid` — один refresh JWKS.

**As-built (2026-06-28):** `SupabaseJwtValidatorImpl` поддерживает **HS256** (секрет) и **JWKS-путь** для асимметричных алгоритмов. Для локального demo (`supabase_url` ends with `demo.local`) JWKS не инициализируется — только HS256.

---

## Обязательные проверки JWT claims

| Claim | Значение | Проверка (фактически в коде) |
|-------|---------|---------|
| `alg` | `HS256` или JWKS (`ES256`, `RS256`, …) | HS256 через секрет; асимметричные — через JWKS ✅ |
| `iss` | `{SUPABASE_URL}/auth/v1` | essential, должен совпадать с конфигом ✅ |
| `aud` | `authenticated` | essential, должен совпадать с `authenticated` ✅ |
| `exp` | Unix timestamp | essential, `exp > now()` ✅ |
| `sub` | UUID пользователя | essential + явная проверка «не пустой» ✅ |
| `role` | `authenticated` | проверяется явно (`role != "authenticated"` → ошибка) ✅ |

> **SEC-03 (2026-06-26):** `aud=authenticated` валидируется через `JWTClaimsRegistry`. Решение и live-sanity: [`epic-ids-12-sec-03-jwt-aud-decision-2026-06-26.md`](../analysis/epic-ids-12-sec-03-jwt-aud-decision-2026-06-26.md).

**Атака на `alg: none`:** Явно задавать список разрешённых алгоритмов `["HS256"]`. Никогда `algorithms=None` или `algorithms=["*"]`. (В коде: `jwt.decode(token, key, algorithms=["HS256"])` ✅.)

---

## Спецификация модуля `src/core/auth/supabase_validator.py`

> **Форма реализации (фактическая):** не свободная функция, а **класс `SupabaseJwtValidatorImpl`** с методом `validate(token)`, реализующий `Protocol` `SupabaseJwtValidator` из `src/core/domain/contracts.py`. `UserClaims` и `JwtValidationError` живут в `src/core/domain/models.py` (валидатор их импортирует). Конфигурация (`jwt_secret`, `supabase_url`) передаётся в конструктор, а не в каждый вызов.

```python
# src/core/domain/contracts.py
@runtime_checkable
class SupabaseJwtValidator(Protocol):
    def validate(self, token: str) -> UserClaims: ...


# src/core/domain/models.py
@dataclass(frozen=True)
class UserClaims:
    supabase_user_id: str   # = JWT sub claim (UUID)
    email: str | None       # may be absent for phone-only accounts
    role: str               # "authenticated"


class JwtValidationError(Exception):
    """Raised when JWT is invalid, expired, or tampered."""
```

### Реализация (фактический код `SupabaseJwtValidatorImpl`)

```python
from joserfc import jwt
from joserfc.errors import JoseError
from joserfc.jwk import OctKey

from core.domain.models import JwtValidationError, UserClaims


class SupabaseJwtValidatorImpl:
    def __init__(self, *, jwt_secret: str, supabase_url: str) -> None:
        self._jwt_secret = jwt_secret
        self._supabase_url = supabase_url.rstrip("/")
        self._expected_iss = f"{self._supabase_url}/auth/v1"
        self._key = OctKey.import_key(jwt_secret)
        self._claims_registry = jwt.JWTClaimsRegistry(
            iss={"essential": True, "value": self._expected_iss},
            sub={"essential": True},
            exp={"essential": True},
            aud={"essential": True, "value": "authenticated"},
        )

    def validate(self, token: str) -> UserClaims:
        try:
            token_obj = jwt.decode(token, self._key, algorithms=["HS256"])
            self._claims_registry.validate(token_obj.claims)
        except JoseError as exc:
            raise JwtValidationError(f"JWT validation failed: {exc}") from exc
        except Exception as exc:
            raise JwtValidationError(f"JWT validation failed: {exc}") from exc

        claims = token_obj.claims
        if claims.get("role") != "authenticated":
            raise JwtValidationError("Token role is not 'authenticated'")

        sub = claims.get("sub")
        if not sub:
            raise JwtValidationError("JWT sub missing")

        return UserClaims(
            supabase_user_id=str(sub),
            email=claims.get("email"),
            role=str(claims["role"]),
        )
```

Импорт ключа: `OctKey.import_key(jwt_secret)` — **сырая строка** JWT Secret из Supabase Dashboard (Settings → API). Это канонический путь для HS256; не требует JWK-обёртки `{"kty":"oct","k":…}`.

---

## FastAPI Dependency Pattern

> **Фактическая форма:** `get_current_user` в `src/core/api/security.py` делегирует валидацию объекту `deps.bearer_token_auth` (тип `BearerTokenAuth` Protocol). В проде это `CompositeBearerTokenAuth` — сначала пробует Supabase JWT через `SupabaseJwtValidatorImpl.validate(...)`, затем (если не прошло) OAuth access-token, выданный самим сервисом. Ошибки представлены доменным `UnauthorizedError` (код `AUTHENTICATION_REQUIRED`), который маппится в 401 на уровне error-handler'ов, а не через прямой `HTTPException` в депенденси.

```python
# src/core/api/security.py (фактический код, сокращённо)

class SupabaseJwtBearerTokenAuth:
    def __init__(self, *, validator: SupabaseJwtValidator) -> None:
        self._validator = validator

    def validate(self, headers: Mapping[str, str]) -> UserClaims:
        token = _extract_bearer_token(headers)
        if token is None:
            raise UnauthorizedError("Bearer token required")
        try:
            return self._validator.validate(token)
        except JwtValidationError as exc:
            raise UnauthorizedError("AUTHENTICATION_REQUIRED") from exc


def get_current_user(
    request: Request,
    deps: ApiDependencies = Depends(_get_api_dependencies),
) -> UserClaims:
    headers = {name: value for name, value in request.headers.items()}
    return deps.bearer_token_auth.validate(headers)


# Использование в endpoint:
@app.get("/me")
async def me(current_user: UserClaims = Depends(get_current_user)) -> JSONResponse:
    ...
```

---

## OAuth Bearer Token Pattern (для Custom GPT)

Custom GPT передаёт access_token выданный identity-service (не Supabase JWT). **Фактически** отдельной депенденси нет: `CompositeBearerTokenAuth.validate(...)` сначала пробует Supabase JWT, при неудаче — `oauth_token_service.validate_access_token(token)` и собирает `UserClaims(supabase_user_id=claims.sub, email=None, role="authenticated")`.

```python
# src/core/api/security.py — CompositeBearerTokenAuth (сокращённо)
class CompositeBearerTokenAuth:
    def validate(self, headers: Mapping[str, str]) -> UserClaims:
        token = _extract_bearer_token(headers)
        if token is None:
            raise UnauthorizedError("Bearer token required")
        try:
            return self._supabase_auth._validator.validate(token)
        except JwtValidationError:
            pass
        oauth_service = self._oauth_token_service
        if oauth_service is not None:
            try:
                claims = oauth_service.validate_access_token(token)
            except ValueError as exc:
                raise UnauthorizedError("AUTHENTICATION_REQUIRED") from exc
            return UserClaims(supabase_user_id=claims.sub, email=None, role="authenticated")
        raise UnauthorizedError("AUTHENTICATION_REQUIRED")
```

Спецификация OAuth токена — в файле 14.

---

## Acceptance Criteria

- [x] `SupabaseJwtValidatorImpl(...).validate(valid_token)` возвращает `UserClaims` с корректным `supabase_user_id`
- [x] `.validate(expired_token)` поднимает `JwtValidationError`
- [x] `.validate(wrong_signature_token)` поднимает `JwtValidationError`
- [x] `.validate(alg_none_token)` поднимает `JwtValidationError`
- [x] `GET /me` без Authorization header → 401 `authentication_required`
- [x] `GET /me` с невалидным токеном → 401 `authentication_required`
- [x] `GET /me` с валидным токеном → 200 с профилем пользователя
