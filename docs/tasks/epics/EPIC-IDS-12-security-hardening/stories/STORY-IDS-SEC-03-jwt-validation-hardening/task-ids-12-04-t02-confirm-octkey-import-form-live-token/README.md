## Task workspace — `task-ids-12-04-t02-confirm-octkey-import-form-live-token`

- Story: [`../STORY-IDS-SEC-03-jwt-validation-hardening.md`](../STORY-IDS-SEC-03-jwt-validation-hardening.md)
- Prerequisite: — (may reuse live session from t01)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000038`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md) Scope §Сверка формы импорта ключа; Story AC #3  
---

## Task: fix — confirm OctKey import form against live Supabase token

### Цель
Подтвердить на **реальном** Supabase JWT, какая форма ключа верна — `OctKey.import_key(jwt_secret)` (raw) vs base64url JWK wrapper — и привести код и spec 09 к одной форме — Story Scope §Сверка формы импорта ключа, AC #3.

### Почему это важно
G-5: spec и код расходятся по импорту ключа; offline green suite не доказывает форму для production secret.

### Факты из кода
1. Raw import в валидаторе — [`supabase_validator.py:17`](../../../../../../../src/core/auth/supabase_validator.py) `OctKey.import_key(jwt_secret)`.
2. Spec NB b64url wrapper — [`09-supabase-jwt-validation.md:93-94,126`](../../../../../../../docs/requirements/09-supabase-jwt-validation.md).
3. Synthetic token encode uses raw key — [`test_supabase_jwt_validator.py:42`](../../../../../../../tests/test_supabase_jwt_validator.py).
4. Live creds — [`tests/integration/supabase/conftest.py`](../../../../../../../tests/integration/supabase/conftest.py).

### Gap / Проблема
Единственно верная форма импорта не подтверждена live; spec и code могут расходиться.

### AC/DoD
- [ ] (P0) Live sanity: `SupabaseJwtValidatorImpl.validate(real_token)` succeeds with **documented** key import form; alternate form fails or documented as invalid.
- [ ] (P0) `supabase_validator.py` и spec 09 описывают **одну** форму (raw или wrapper).
- [ ] (P1) Story AC #3.
- [ ] (P1) Не ломать offline synthetic tests (adjust only if import form changes).

### Где менять код
- `doge-identity-service/src/core/auth/supabase_validator.py`
- `doge-identity-service/docs/requirements/09-supabase-jwt-validation.md`
- `doge-identity-service/tests/integration/supabase/` (optional live test)
- `doge-identity-service/tests/test_supabase_jwt_validator.py` (offline key-form sanity)

### Out of scope
- RS256/JWKS
- `aud` registry (t03)
- Изменение `iss`/`sub`/`exp`/`role` checks

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_supabase_jwt_validator.py -m "not live_integration" -q
.venv/bin/python -m pytest tests/integration/supabase/ -m live_integration -k "jwt or validator" -q
grep -n "OctKey.import_key" docs/requirements/09-supabase-jwt-validation.md src/core/auth/supabase_validator.py
```
