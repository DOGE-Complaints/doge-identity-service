## Task workspace — `task-ids-12-06-t05-es256-mock-jwks-test-harness`

- Story: [`../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md)
- Prerequisite: [`task-ids-12-06-t03-jwks-cache-di-wiring`](../task-ids-12-06-t03-jwks-cache-di-wiring/README.md), [`task-ids-12-06-t04-remove-supabase-jwt-secret`](../task-ids-12-06-t04-remove-supabase-jwt-secret/README.md)

---
**Приоритет:** P0  
**Сложность:** L  
**Статус:** done  
**Wave:** `pkg-000042`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md) §Подзадачи T05; Story AC #6  
---

## Task: fix — migrate auth test harness HS256 → ES256+mock-JWKS

### Цель
Общий хелпер: ES256 keypair, mock `JwksCache`, функция mint Supabase Bearer; мигрировать **14 файлов** + `conftest.py`; убрать `test-secret-for-demo`.

### Почему это важно
Критический change-propagation: вся offline-сюита минтит HS256 против fallback-секрета — при JWKS-only всё красное без этой миграции.

### Факты из кода
1. Minters (sample) — [`test_supabase_jwt_validator.py`](../../../../../../../tests/test_supabase_jwt_validator.py), [`test_supabase_jwt_auth.py`](../../../../../../../tests/test_supabase_jwt_auth.py).
2. Full list — pipeline story §Scope Change-propagation (14 files).
3. `conftest.py:35` — [`conftest.py`](../../../../../../../tests/conftest.py) `SUPABASE_JWT_SECRET`.
4. DI from t03 — injectable `JwksCache` in tests via `SupabaseJwtValidatorImpl` / app factory.

### Gap / Проблема
Supabase Bearer tokens in tests use `jwt.encode({"alg":"HS256"}, ..., OctKey)` — incompatible with JWKS-only validator.

### AC/DoD
- [ ] (P0) Shared helper module (e.g. `tests/supabase_jwt_harness.py` or `conftest` fixture) — ES256 mint + mock JWKS URI aligned with test `SUPABASE_URL`.
- [ ] (P0) All 14 backlog-listed test files migrated off Supabase HS256 minters.
- [ ] (P0) `conftest.py` — no `SUPABASE_JWT_SECRET` autouse for Supabase auth path.
- [ ] (P0) No `test-secret-for-demo` in tests/.
- [ ] (P1) OAuth access-token HS256 tests unchanged (`oauth/access_token_jwt` path).
- [ ] (P1) Story AC #6: grep Supabase `"alg": "HS256"` in tests/ empty (excluding OAuth access-token tests).

### Где менять код
- `doge-identity-service/tests/conftest.py`
- `doge-identity-service/tests/` — 14 files per backlog §Change-propagation
- Optional new `doge-identity-service/tests/supabase_jwt_harness.py` (or similar)

### Out of scope
- Validator unit edge cases (t06)
- Docs (t07)
- `oauth/access_token_jwt.py`

### Проверка
```bash
cd doge-identity-service
grep -rn 'test-secret-for-demo' tests/ && exit 1 || true
grep -rn 'alg": "HS256"' tests/ | grep -v oauth | grep -v access_token || true
.venv/bin/python -m pytest -m "not live_integration" -q
```
