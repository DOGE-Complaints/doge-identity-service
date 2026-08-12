## Task workspace — `task-ids-04-05-t03-story5-acceptance-verification`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** ready  
**Wave:** `pkg-000005`  
**Decision Ref:** [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) §6 Story 5  
**Story:** [`../STORY-IDS-04-05-supabase-jwt-bearer-auth.md`](../STORY-IDS-04-05-supabase-jwt-bearer-auth.md)  
---

## Task: tests — Story 5 JWT acceptance verification

### Цель
Добавить pytest-покрытие verbatim AC Story 5 (epic L290–296): valid/expired/alg_none/iss_mismatch tokens, `SupabaseJwtBearerTokenAuth` error mapping, smoke что `/me` с valid token не даёт 401 на auth layer.

### Почему это важно
Auth — security boundary; AC переписаны под class-реализацию (audit C-3), не standalone function.

### Факты из кода
1. Story 5 AC — [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) L290–296.
2. [`src/core/auth/supabase_validator.py`](../../../../../../../src/core/auth/supabase_validator.py) — t01.
3. [`src/core/api/security.py`](../../../../../../../src/core/api/security.py) — t02 добавляет `SupabaseJwtBearerTokenAuth`.
4. [`tests/test_security_primitives.py`](../../../../../../../tests/test_security_primitives.py) — существует для EPIC-IDS-02; Story 5 JWT tests — отдельный файл.

### Gap
Нет JWT-specific tests с AC L290–296.

### AC/DoD
- [ ] (P0) `SupabaseJwtValidatorImpl(jwt_secret=S, supabase_url=U).validate(valid_token)` → `UserClaims` с корректным `supabase_user_id` (req-09 acceptance).
- [ ] (P0) `SupabaseJwtValidatorImpl(jwt_secret=S, supabase_url=U).validate(expired_token)` raises `JwtValidationError` (req-09 acceptance).
- [ ] (P0) `SupabaseJwtValidatorImpl(jwt_secret=S, supabase_url=U).validate(alg_none_token)` raises `JwtValidationError` (req-09 §«Атака на alg: none»).
- [ ] (P0) `SupabaseJwtValidatorImpl(jwt_secret=S, supabase_url=U).validate(token_with_iss_mismatch)` raises `JwtValidationError`.
- [ ] (P0) `SupabaseJwtBearerTokenAuth(validator=...)` корректно конвертирует `JwtValidationError` → `UnauthorizedError(code="AUTHENTICATION_REQUIRED")`.
- [ ] (P1) `GET /me` с валидным токеном — `bearer_token_auth.validate(headers)` возвращает `UserClaims`; `/me` остаётся stub до функционального эпика, но 401 больше не возвращается.

### Где менять код
- `doge-identity-service/tests/test_supabase_jwt_auth.py` (новый)

### Out of scope
- Полный `tests/test_supabase_jwt_validator.py` — EPIC-IDS-06 Story 2
- `tests/test_di_service_factory.py` — EPIC-IDS-06
- Functional `/me` handler — отдельный эпик

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_supabase_jwt_auth.py -v
```
