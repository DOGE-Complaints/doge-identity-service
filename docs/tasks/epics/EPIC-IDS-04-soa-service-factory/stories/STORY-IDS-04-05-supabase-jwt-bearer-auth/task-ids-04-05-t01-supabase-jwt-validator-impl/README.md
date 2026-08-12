## Task workspace — `task-ids-04-05-t01-supabase-jwt-validator-impl`

---
**Приоритет:** P0  
**Сложность:** L  
**Статус:** ready  
**Wave:** `pkg-000005`  
**Decision Ref:** [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) §6 Story 5  
**Story:** [`../STORY-IDS-04-05-supabase-jwt-bearer-auth.md`](../STORY-IDS-04-05-supabase-jwt-bearer-auth.md)  
---

## Task: implement — SupabaseJwtValidatorImpl

### Цель
Создать `src/core/auth/supabase_validator.py` и обновить `src/core/auth/__init__.py` по epic L279–284: `SupabaseJwtValidatorImpl`, re-export `UserClaims` из domain, `JwtValidationError`, joserfc HS256 с проверкой `iss`, `sub`, `exp`, `role=="authenticated"`.

### Почему это важно
Заменяет stub auth-цепочку реальной валидацией Supabase JWT (req-09). `algorithms=["HS256"]` обязателен против `alg: none` attack.

### Факты из кода
1. [`src/core/auth/__init__.py`](../../../../../../../src/core/auth/__init__.py) — только docstring; `supabase_validator.py` **отсутствует**.
2. [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py) — `SupabaseJwtValidator(Protocol)` (Story 1).
3. [`src/core/api/security.py:21-25`](../../../../../../../src/core/api/security.py) — `UserClaims` сейчас в security; epic требует canonical copy в domain + re-export в validator.
4. [`src/core/api/dependencies.py:37`](../../../../../../../src/core/api/dependencies.py) — слот `supabase_jwt_validator`.

### Gap
Нет `SupabaseJwtValidatorImpl` и domain-aligned `JwtValidationError`.

### AC/DoD
- [ ] (P0) `SupabaseJwtValidatorImpl(jwt_secret=S, supabase_url=U).validate(valid_token)` → `UserClaims` с корректным `supabase_user_id`.
- [ ] (P0) `validate(expired_token)` raises `JwtValidationError`.
- [ ] (P0) `validate(alg_none_token)` raises `JwtValidationError`.
- [ ] (P0) `validate(token_with_iss_mismatch)` raises `JwtValidationError`.
- [ ] (P0) `algorithms=["HS256"]` захардкожены (req-09 §«Атака на alg: none»).

### Где менять код
- `doge-identity-service/src/core/auth/supabase_validator.py` (новый)
- `doge-identity-service/src/core/auth/__init__.py` (exports)

### Out of scope
- `SupabaseJwtBearerTokenAuth` — t02
- Story 5 integration pytest — t03
- `tests/test_supabase_jwt_validator.py` полный набор — EPIC-IDS-06 Story 2

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "
from core.auth.supabase_validator import SupabaseJwtValidatorImpl, JwtValidationError
print('SupabaseJwtValidatorImpl import OK')
"
```
