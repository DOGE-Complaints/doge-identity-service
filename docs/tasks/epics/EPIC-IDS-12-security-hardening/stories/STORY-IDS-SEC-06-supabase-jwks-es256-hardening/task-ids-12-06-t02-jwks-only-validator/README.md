## Task workspace — `task-ids-12-06-t02-jwks-only-validator`

- Story: [`../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md)
- Prerequisite: [`task-ids-12-06-t01-change-propagation-audit`](../task-ids-12-06-t01-change-propagation-audit/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000042`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md) §Подзадачи T02 (D-1/D-2); Story AC #2, #4  
---

## Task: implement — Supabase JWT validator JWKS-only (D-1/D-2)

### Цель
Удалить HS256-путь и sentinel-эвристику; оставить только асимметричную валидацию через `_JWKS_ALGORITHMS`; JWKS-гейт по непустому реальному `supabase_url`, fail-closed при пустом URL.

### Почему это важно
Dual-path HS256 + fallback `test-secret-for-demo` — дыра подделки; Cloud использует ES256/JWKS only (D-1).

### Факты из кода
1. Remove targets — [`supabase_validator.py:35-43,51,72-73,101-102`](../../../../../../../src/core/auth/supabase_validator.py).
2. Keep JWKS core — [`supabase_validator.py:76-105`](../../../../../../../src/core/auth/supabase_validator.py) `_validate_jwks`, `_JWKS_ALGORITHMS`.
3. Keep claims — [`supabase_validator.py`](../../../../../../../src/core/auth/supabase_validator.py) `_claims_from_token` (SEC-03).
4. Sentinel wiring — [`providers.py:109-110`](../../../../../../../src/core/infrastructure/providers.py).

### Gap / Проблема
Валидатор всё ещё принимает HS256 и создаёт OctKey из `jwt_secret`; `demo.local` отключает JWKS.

### AC/DoD
- [ ] (P0) Удалены `_validate_hs256`, `self._key`, `jwt_secret` param, `OctKey` import, ветка `alg=="HS256"`.
- [ ] (P0) Убрана эвристика `endswith("demo.local")`; JWKS активен при непустом `supabase_url`.
- [ ] (P0) Пустой `supabase_url` → fail-closed (нет HS256 fallback).
- [ ] (P1) `_JWKS_ALGORITHMS` и refresh-on-unknown-kid сохранены.
- [ ] (P1) Story AC #2 grep (partial — OctKey may remain in oauth, not in supabase_validator).

### Где менять код
- `doge-identity-service/src/core/auth/supabase_validator.py`
- `doge-identity-service/src/core/infrastructure/providers.py` (убрать sentinel URL only if in scope t02; full secret removal in t04)

### Out of scope
- DI `JwksCache` (t03)
- `schema.py` / `SUPABASE_JWT_SECRET` (t04)
- Test harness migration (t05)
- `oauth/access_token_jwt.py`

### Проверка
```bash
cd doge-identity-service
grep -n '_validate_hs256\|OctKey\|alg=="HS256"' src/core/auth/supabase_validator.py && exit 1 || true
grep -n 'demo\.local' src/core/auth/supabase_validator.py && exit 1 || true
.venv/bin/python -m pytest tests/test_supabase_jwt_validator.py -q -m "not live_integration" || true
```
