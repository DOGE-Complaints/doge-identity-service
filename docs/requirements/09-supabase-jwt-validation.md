# 09. Supabase JWT Validation

> **Статус:** реализовано (актуализировано 2026-07-04, SEC-06 JWKS-only). Код: `src/core/auth/supabase_validator.py` и `src/core/api/security.py`.
> **Предусловие:** `SUPABASE_URL` настроен — JWKS endpoint `{SUPABASE_URL}/auth/v1/.well-known/jwks.json` (файл 07).
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

Supabase Cloud подписывает access tokens **асимметрично** (типично **ES256**). Identity-service проверяет подпись **только через JWKS** — симметричный HS256-путь удалён (SEC-06 D-1).

### JWKS-only (as-built SEC-06)
- JWKS endpoint: `{SUPABASE_URL}/auth/v1/.well-known/jwks.json`
- Разрешённые алгоритмы: `ES256`, `RS256`, `ES384`, `ES512` (по JWT header `alg`).
- Валидация через `JwksCache` (тот же паттерн, что OIDC id_token): DI в [`providers.py`](../../src/core/infrastructure/providers.py) создаёт `httpx.Client` + `JwksCache` при непустом `SUPABASE_URL`.
- При unknown `kid` — один refresh JWKS; пустой `SUPABASE_URL` → fail-closed (JWKS недоступен).
- **HS256 не поддерживается** для Supabase access tokens (удалён `SUPABASE_JWT_SECRET`).

---

## Обязательные проверки JWT claims

| Claim | Значение | Проверка (фактически в коде) |
|-------|---------|---------|
| `alg` | JWKS (`ES256`, `RS256`, …) | Только асимметричные алгоритмы через JWKS ✅ |
| `iss` | `{SUPABASE_URL}/auth/v1` | essential, должен совпадать с конфигом ✅ |
| `aud` | `authenticated` | essential, должен совпадать с `authenticated` ✅ |
| `exp` | Unix timestamp | essential, `exp > now()` ✅ |
| `sub` | UUID пользователя | essential + явная проверка «не пустой» ✅ |
| `role` | `authenticated` | проверяется явно (`role != "authenticated"` → ошибка) ✅ |

> **SEC-03 (2026-06-26):** `aud=authenticated` валидируется через `JWTClaimsRegistry`. Решение и live-sanity: [`epic-ids-12-sec-03-jwt-aud-decision-2026-06-26.md`](../analysis/epic-ids-12-sec-03-jwt-aud-decision-2026-06-26.md).

**Атака на `alg: none` / HS256:** Явно задавать список разрешённых JWKS-алгоритмов; HS256 отклоняется как unsupported. Никогда `algorithms=None` или `algorithms=["*"]`.

---

## Спецификация модуля `src/core/auth/supabase_validator.py`

> **Форма реализации (фактическая):** класс **`SupabaseJwtValidatorImpl`** с методом `validate(token)`, реализующий `Protocol` `SupabaseJwtValidator`. Конфигурация: `supabase_url` + инжектированный `JwksCache` (создаётся в `providers.py`).

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

### Реализация (фактический код, сокращённо)

См. [`supabase_validator.py`](../../src/core/auth/supabase_validator.py): `_header_alg` → если `alg` в `_JWKS_ALGORITHMS`, decode через `JwksCache.get_key_set()` с одним retry при `InvalidKeyIdError`; иначе `JwtValidationError("Unsupported JWT algorithm")`.

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
