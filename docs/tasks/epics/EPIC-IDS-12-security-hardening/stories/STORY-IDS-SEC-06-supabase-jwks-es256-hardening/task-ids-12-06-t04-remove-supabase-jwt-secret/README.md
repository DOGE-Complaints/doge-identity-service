## Task workspace — `task-ids-12-06-t04-remove-supabase-jwt-secret`

- Story: [`../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md)
- Prerequisite: [`task-ids-12-06-t01-change-propagation-audit`](../task-ids-12-06-t01-change-propagation-audit/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000042`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md) §Подзадачи T04 (D-5); Story AC #2, #5  
---

## Task: implement — remove SUPABASE_JWT_SECRET from config (D-5)

### Цель
Снять `SUPABASE_JWT_SECRET` / `supabase_jwt_secret` из schema, providers, `.env.example`; обновить pilot-required и `test_config_schema.py`.

### Почему это важно
Мёртвый секрет и публичный fallback `test-secret-for-demo` — security debt после перехода на JWKS-only.

### Факты из кода
1. AppConfig field — [`schema.py:34`](../../../../../../../src/core/config/schema.py).
2. Load + pilot-required — [`schema.py:160,190,215`](../../../../../../../src/core/config/schema.py).
3. Fallback — [`providers.py:109`](../../../../../../../src/core/infrastructure/providers.py).
4. `.env.example` — [`.env.example:29,37,41`](../../../../../../../.env.example).
5. Tests — [`test_config_schema.py`](../../../../../../../tests/test_config_schema.py).

### Gap / Проблема
Config и pilot gate всё ещё требуют/знают `SUPABASE_JWT_SECRET` после D-1.

### AC/DoD
- [ ] (P0) `supabase_jwt_secret` удалён из `AppConfig`, load, pilot-required tuple.
- [ ] (P0) `providers.py` не передаёт `jwt_secret` / fallback `test-secret-for-demo`.
- [ ] (P0) `.env.example` — строки `SUPABASE_JWT_SECRET` сняты или помечены removed.
- [ ] (P0) `test_config_schema.py` — pilot-required без `SUPABASE_JWT_SECRET`.
- [ ] (P1) `grep -rn 'SUPABASE_JWT_SECRET\|supabase_jwt_secret' src/` пусто (Story AC #2 partial).

### Где менять код
- `doge-identity-service/src/core/config/schema.py`
- `doge-identity-service/src/core/infrastructure/providers.py`
- `doge-identity-service/.env.example`
- `doge-identity-service/tests/test_config_schema.py`
- `doge-identity-service/tests/conftest.py` (autouse `SUPABASE_JWT_SECRET` — coordinate with t05)

### Out of scope
- Docs/runbooks (t07)
- OAuth secrets

### Проверка
```bash
cd doge-identity-service
grep -rn 'SUPABASE_JWT_SECRET\|supabase_jwt_secret\|test-secret-for-demo' src/ && exit 1 || true
.venv/bin/python -m pytest tests/test_config_schema.py -q
```
