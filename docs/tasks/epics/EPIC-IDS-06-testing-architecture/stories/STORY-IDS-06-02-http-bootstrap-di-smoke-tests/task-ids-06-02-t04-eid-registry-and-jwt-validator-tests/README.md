## Task workspace — `task-ids-06-02-t04-eid-registry-and-jwt-validator-tests`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000008`  
**Decision Ref:** [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 2  
**Story:** [`../STORY-IDS-06-02-http-bootstrap-di-smoke-tests.md`](../STORY-IDS-06-02-http-bootstrap-di-smoke-tests.md)  
---

## Task: tests — eID registry and JWT validator modules

### Цель
Создать `tests/test_eid_provider_registry.py` (L181–185) и `tests/test_supabase_jwt_validator.py` (L186–191) — без сети, synthetic JWT via `joserfc`.

### Почему это важно
Offline coverage identity provider registry и JWT validation (epic Story 2 Outputs).

### Факты из кода
1. [`tests/test_eid_provider_registry.py`](../../../../../../../tests/test_eid_provider_registry.py) — **отсутствует**; overlap [`tests/test_eid_providers.py`](../../../../../../../tests/test_eid_providers.py).
2. [`tests/test_supabase_jwt_validator.py`](../../../../../../../tests/test_supabase_jwt_validator.py) — **отсутствует**; overlap [`tests/test_supabase_jwt_auth.py`](../../../../../../../tests/test_supabase_jwt_auth.py).
3. Epic L186–191 — five JWT test cases (valid, expired, wrong sig, alg none, iss mismatch).

### Gap
Канонические модули из epic §5 L58–59 отсутствуют.

### AC/DoD
- [x] (P0) `test_mock_provider_registered_by_default`.
- [x] (P0) `test_get_active_returns_mock_when_eid_provider_mock`.
- [x] (P0) `test_get_unknown_provider_raises`.
- [x] (P0) `test_mock_provider_start_flow_creates_session` — через `InMemoryVerificationSessionStore`.
- [x] (P0) `test_valid_token_returns_user_claims` — HMAC sign + decode.
- [x] (P0) `test_expired_token_raises_jwt_validation_error`.
- [x] (P0) `test_wrong_signature_raises`.
- [x] (P0) `test_alg_none_attack_rejected`.
- [x] (P0) `test_iss_mismatch_raises`.

### Где менять код
- `doge-identity-service/tests/test_eid_provider_registry.py` (новый)
- `doge-identity-service/tests/test_supabase_jwt_validator.py` (новый)

### Out of scope
- Story 2 acceptance — t05
- `mock_oidc` marker tests — epic §9 L314

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_eid_provider_registry.py tests/test_supabase_jwt_validator.py -v
```
