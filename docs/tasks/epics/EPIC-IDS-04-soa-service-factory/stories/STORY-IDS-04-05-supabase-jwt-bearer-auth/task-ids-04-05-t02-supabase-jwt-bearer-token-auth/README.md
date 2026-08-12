## Task workspace — `task-ids-04-05-t02-supabase-jwt-bearer-token-auth`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** ready  
**Wave:** `pkg-000005`  
**Decision Ref:** [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) §6 Story 5  
**Story:** [`../STORY-IDS-04-05-supabase-jwt-bearer-auth.md`](../STORY-IDS-04-05-supabase-jwt-bearer-auth.md)  
---

## Task: implement — SupabaseJwtBearerTokenAuth in security.py

### Цель
Обновить [`src/core/api/security.py`](../../../../../../../src/core/api/security.py): добавить `SupabaseJwtBearerTokenAuth` по epic L286–288; обновить `get_current_user` для полиморфного `deps.bearer_token_auth`.

### Почему это важно
FastAPI dependency chain: `Authorization: Bearer <jwt> → validate → UserClaims`. Конвертация `JwtValidationError` → `UnauthorizedError(code="AUTHENTICATION_REQUIRED")` сохраняет совместимость с exception handler EPIC-IDS-02.

### Факты из кода
1. [`src/core/api/security.py:33-42`](../../../../../../../src/core/api/security.py) — `StubBearerTokenAuth` используется в [`dependencies.py:64`](../../../../../../../src/core/api/dependencies.py).
2. [`src/core/api/security.py:13-18`](../../../../../../../src/core/api/security.py) — `UnauthorizedError` — единственный источник (audit H-4); validator импортирует отсюда, не из domain.
3. [`src/core/auth/supabase_validator.py`](../../../../../../../src/core/auth/supabase_validator.py) — создаётся в t01.
4. Epic L288: поведение совместимо со `StubBearerTokenAuth` для тестов до полного закрытия валидатора.

### Gap
Нет `SupabaseJwtBearerTokenAuth`; `build_api_dependencies` всё ещё возвращает stub.

### AC/DoD
- [ ] (P0) `SupabaseJwtBearerTokenAuth(validator=...)` корректно конвертирует `JwtValidationError` → `UnauthorizedError(code="AUTHENTICATION_REQUIRED")`.
- [ ] (P0) `validate(headers)` парсит `Authorization: Bearer ...` и делегирует валидатору.
- [ ] (P0) `get_current_user` использует `deps.bearer_token_auth` (полиморфно).
- [ ] (P0) `StubBearerTokenAuth` сохранён для backward-compatible tests.

### Где менять код
- `doge-identity-service/src/core/api/security.py` (обновить)

### Out of scope
- `SupabaseJwtValidatorImpl` body — t01
- `build_api_dependencies` swap stub → real — Story 6 t02
- `asgi_app.py` — без изменений (epic L354)
- Story 5 pytest — t03

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "
from core.api.security import SupabaseJwtBearerTokenAuth, UnauthorizedError
from core.auth.supabase_validator import SupabaseJwtValidatorImpl
auth = SupabaseJwtBearerTokenAuth(validator=SupabaseJwtValidatorImpl(jwt_secret='s', supabase_url='https://x.supabase.co'))
print('SupabaseJwtBearerTokenAuth OK')
"
```
