## Task workspace — `task-ids-11-03-t06-durability-and-stateless-jwt-tests`

- Story: [`../STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../STORY-IDS-OAUTH-03-persistent-token-store-supabase.md)
- Prerequisite: t02–t05

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000033`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) Story AC #4, #5  
---

## Task: tests — durability redeploy emulation and stateless access token

### Цель
Закрыть durability AC: state переживает пересоздание store instance; access-token остаётся валидным без обращения к БД.

### Почему это важно
Ядро OAUTH-03 — «редеплой не рвёт логин в процессе»; stateless JWT — явное подтверждение, что access tokens не нужно персистить.

### Факты из кода
1. Durability gap: in-memory stores cleared on process restart — [`repositories.py:431-461`](../../../../../../../src/core/infrastructure/repositories.py).
2. JWT validate path: [`repositories.py:536-545`](../../../../../../../src/core/infrastructure/repositories.py) — no DB read.
3. Mock store backend from t05 can simulate «new process» by new Python instance with same mocked PostgREST data.
4. `invalid_grant` on expired/consumed: [`repositories.py:507-513`](../../../../../../../src/core/infrastructure/repositories.py).

### Gap / Проблема
Нет тестов, эмулирующих redeploy (recreate store) и stateless JWT после recreate.

### AC/DoD
- [x] (P0) **Durability:** issue authorization code (or save request) → destroy store instance → new store with same backend data → `issue_access_token` / `consume` succeeds.
- [x] (P0) **Durability:** expired or consumed code/request → `invalid_grant` (or `consume` → `None`).
- [x] (P0) **Stateless:** issue access token → recreate `SupabaseOAuthTokenService` → `validate_access_token` succeeds without DB read (assert mock call count or use in-memory JWT path only).
- [x] (P1) Traceability: Story AC #4, #5.

### Где менять код
- `doge-identity-service/tests/test_oauth_supabase_stores.py` (extend) or `tests/test_oauth_durability.py` (new)

### Out of scope
- Multi-instance integration / Railway deploy test
- Migration SQL (t01, t05)
- Story gate (t07)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_oauth_supabase_stores.py -k "durability or stateless" -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
