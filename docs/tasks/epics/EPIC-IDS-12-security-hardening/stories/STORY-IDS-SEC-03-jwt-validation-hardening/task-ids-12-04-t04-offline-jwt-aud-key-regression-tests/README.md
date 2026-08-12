## Task workspace — `task-ids-12-04-t04-offline-jwt-aud-key-regression-tests`

- Story: [`../STORY-IDS-SEC-03-jwt-validation-hardening.md`](../STORY-IDS-SEC-03-jwt-validation-hardening.md)
- Prerequisite: [`task-ids-12-04-t02-confirm-octkey-import-form-live-token`](../task-ids-12-04-t02-confirm-octkey-import-form-live-token/README.md), [`task-ids-12-04-t03-aud-claim-registry-or-spec-waiver`](../task-ids-12-04-t03-aud-claim-registry-or-spec-waiver/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000038`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md) Story AC #2, #5  
---

## Task: tests — offline JWT `aud` and key-import regression suite

### Цель
Расширить offline-тесты: при ветке validate — `aud≠authenticated` отклоняется, `aud=authenticated` проходит; сохранить регрессию `iss`/`sub`/`exp`/`role` и key-import baseline — Story AC #2, #5.

### Почему это важно
AC #2 требует проверяемый тест; audit §6 baseline must stay green offline.

### Факты из кода
1. Existing validator tests — [`test_supabase_jwt_validator.py`](../../../../../../../tests/test_supabase_jwt_validator.py) (valid, expired, wrong sig, alg none, iss mismatch).
2. Bearer auth integration — [`test_supabase_jwt_auth.py`](../../../../../../../tests/test_supabase_jwt_auth.py).
3. `_make_valid_token` sets `aud: authenticated` — [`test_supabase_jwt_validator.py:37`](../../../../../../../tests/test_supabase_jwt_validator.py).

### Gap / Проблема
Нет теста на wrong `aud`; нет explicit key-import form regression offline.

### AC/DoD
- [ ] (P0) If validate branch: `test_wrong_aud_raises` (e.g. `aud=service_role` or missing) → `JwtValidationError`; valid token still passes.
- [ ] (P0) If waiver branch: test documents that wrong `aud` still passes (or skip aud-negative test with comment linking spec waiver).
- [ ] (P0) Regression: expired, wrong signature, alg none, iss mismatch still fail — Story AC #5.
- [ ] (P1) Offline key-import sanity (raw vs wrong wrapper) if applicable after t02.
- [ ] (P1) Story AC #2, #5 traceability.

### Где менять код
- `doge-identity-service/tests/test_supabase_jwt_validator.py`
- `doge-identity-service/tests/test_supabase_jwt_auth.py` (if bearer path needs aud coverage)

### Out of scope
- Live integration tests (t01/t02)
- Spec doc G-5 cleanup (t05)
- RS256/JWKS

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_supabase_jwt_validator.py tests/test_supabase_jwt_auth.py -m "not live_integration" -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
