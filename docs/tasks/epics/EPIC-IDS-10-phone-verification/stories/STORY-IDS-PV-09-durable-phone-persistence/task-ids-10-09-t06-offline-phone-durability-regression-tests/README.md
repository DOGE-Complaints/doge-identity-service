## Task workspace — `task-ids-10-09-t06-offline-phone-durability-regression-tests`

- Story: [`../STORY-IDS-PV-09-durable-phone-persistence.md`](../STORY-IDS-PV-09-durable-phone-persistence.md)
- Prerequisite: [`task-ids-10-09-t04-di-phone-store-backend-selection`](../task-ids-10-09-t04-di-phone-store-backend-selection/README.md); [`task-ids-10-09-t05-bootstrap-full-init-parity`](../task-ids-10-09-t05-bootstrap-full-init-parity/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000039`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md); OAUTH-03 t05/t06 durability test pattern  
---

## Task: tests — offline phone durability and in_memory regression

### Цель
Добавить offline-тесты durability: session/audit переживают пересоздание store/repo; expired/consumed status; in_memory path regression green.

### Почему это важно
Story AC #1/#2/#4 требуют доказательства durability и неизменности in-memory path; без тестов gate не закрывается.

### Факты из кода
1. OAuth durability tests precedent: OAUTH-03 t05/t06 in pkg-000033.
2. In-memory session store: [`repositories.py:284+`](../../../../../../../src/core/infrastructure/repositories.py).
3. In-memory audit repo: [`repositories.py:362+`](../../../../../../../src/core/infrastructure/repositories.py).
4. DI switch from t04: [`providers.py`](../../../../../../../src/core/infrastructure/providers.py).
5. SEC-02 already covers IP/UA hash assertions — **no new IP/UA assertions beyond existing SEC-02 tests**.

### Gap / Проблема
Нет offline-тестов, эмулирующих редеплой (new store instance) для phone Supabase stores.

### AC/DoD
- [x] (P0) Session: create → new `SupabasePhoneVerificationSessionStore` instance → `get_latest_for_confirm` / `confirm` path still works.
- [x] (P0) Audit: `log_event` → new repo instance → `list_events` returns persisted row.
- [x] (P0) Expired/consumed session status correct after rebuild.
- [x] (P0) `DB_BACKEND=in_memory` regression — full offline suite green.
- [x] (P1) Traceability: Story AC #1, #2, #4, #7 (scope boundary: no new IP/UA assertions).

### Где менять код
- `doge-identity-service/tests/` (new or extend test modules; pattern OAUTH-03 t05/t06)

### Out of scope
- Live Supabase integration tests (unless existing harness used with skip)
- IP/UA hashing new assertions (SEC-02 scope)
- Migration SQL changes (t01)
- Story gate doc (t07)

### Проверка
```bash
cd doge-identity-service
python3 -m pytest -m "not live_integration" -q
python3 -m pytest tests/ -k "phone" -m "not live_integration" -q
```
