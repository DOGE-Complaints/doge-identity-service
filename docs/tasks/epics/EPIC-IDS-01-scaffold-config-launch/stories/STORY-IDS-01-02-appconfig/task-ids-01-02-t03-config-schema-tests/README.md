## Task workspace — `task-ids-01-02-t03-config-schema-tests`

- Story: [`../STORY-IDS-01-02-appconfig.md`](../STORY-IDS-01-02-appconfig.md)
- Epic: [`../../../../EPIC-IDS-01-scaffold-config-launch.md`](../../../../EPIC-IDS-01-scaffold-config-launch.md) §Story 2 AC + §8

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000001`  
**Зависимости:** task-ids-01-02-t01-config-schema  
---

## Task: tests — AppConfig validation matrix

### Цель
Pytest-покрытие AC Story 2: demo defaults, supabase missing vars, sqlite forbidden, pilot secrets, eid_provider, frozen instance, pilot empty `DOGESTONIA_EID_SECRET`.

### Факты из кода
1. `tests/test_config_schema.py` — отсутствует.
2. Эпик §Story 2 Acceptance Criteria — 8 сценариев (включая interview 4.4).
3. Эпик §8 — inline `python -c` scripts как reference assertions.

### Gap / Проблема
Без автотестов регрессии валидации config не ловятся в CI (EPIC-IDS-06).

### AC/DoD
- [x] (P0) `tests/test_config_schema.py` — тесты покрывают AC эпика §Story 2.
- [x] (P0) `FrozenInstanceError` при mutation `config.eid_secret`.
- [x] (P0) `pytest tests/test_config_schema.py -q` — all passed.
- [x] (P1) Marker: offline only (no `live_integration`).

### Где менять код
- `doge-identity-service/tests/test_config_schema.py`

### Out of scope
- Dotenv merge tests (STORY-IDS-01-03 T03)
- Integration с реальным `.env` file

### Команды проверки
```bash
cd doge-identity-service && . .venv/bin/activate
python3.11 -m pytest tests/test_config_schema.py -q
```
