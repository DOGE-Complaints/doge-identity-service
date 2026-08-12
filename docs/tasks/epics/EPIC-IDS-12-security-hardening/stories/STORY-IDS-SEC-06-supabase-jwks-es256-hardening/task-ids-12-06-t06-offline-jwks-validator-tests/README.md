## Task workspace — `task-ids-12-06-t06-offline-jwks-validator-tests`

- Story: [`../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md)
- Prerequisite: [`task-ids-12-06-t05-es256-mock-jwks-test-harness`](../task-ids-12-06-t05-es256-mock-jwks-test-harness/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000042`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md) §Подзадачи T06; Story AC #7  
---

## Task: tests — offline ES256/JWKS validator coverage

### Цель
Покрыть JWKS-путь: happy ES256; unknown-kid→refresh; kid-not-found; alg whitelist; `none`/`HS256` reject; jwks-unavailable; claims `aud`/`iss`/`sub`/`exp`/`role` on ES256.

### Почему это важно
Инцидент Session Expired чинился ES256/JWKS — без регрессионных тests путь не защищён (W4 из build-session).

### Факты из кода
1. Validator — [`supabase_validator.py`](../../../../../../../src/core/auth/supabase_validator.py) `_validate_jwks`, `_JWKS_ALGORITHMS`.
2. Existing RS256 mock pattern — [`test_supabase_jwt_validator.py`](../../../../../../../tests/test_supabase_jwt_validator.py) `test_rs256_token_validated_via_mock_jwks`.
3. OIDC mock transport pattern — [`test_oidc_toolkit.py`](../../../../../../../tests/test_oidc_toolkit.py).
4. SEC-03 claim tests — prior HS256 cases to port to ES256.

### Gap / Проблема
JWKS/ES256 critical path has insufficient dedicated unit coverage vs HS256 legacy suite.

### AC/DoD
- [ ] (P0) Happy ES256 via mock JWKS → `UserClaims`.
- [ ] (P0) unknown-kid → refresh → success; kid not found after refresh → `JwtValidationError`.
- [ ] (P0) `alg` outside whitelist → reject; `alg=none` → reject; `alg=HS256` → reject.
- [ ] (P0) `jwks_cache is None` + asymmetric alg → clear error (fail-closed).
- [ ] (P0) Claims regression on ES256: expired, wrong iss, wrong aud, missing aud, role != authenticated.
- [ ] (P1) Story AC #7 traceability.

### Где менять код
- `doge-identity-service/tests/test_supabase_jwt_validator.py`
- Optional shared harness from t05

### Out of scope
- 14-file harness migration (t05 — prerequisite)
- Live integration (`test_supabase_jwt_live_sanity.py` — coordinate, not gate)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_supabase_jwt_validator.py -q
.venv/bin/python -m pytest tests/test_supabase_jwt_auth.py -q
```
