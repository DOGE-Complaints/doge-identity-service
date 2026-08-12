## Task workspace — `task-ids-06-01-t02-story1-acceptance-verification`

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000008`  
**Decision Ref:** [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 1  
**Story:** [`../STORY-IDS-06-01-conftest-autouse-fixtures.md`](../STORY-IDS-06-01-conftest-autouse-fixtures.md)  
---

## Task: tests — Story 1 acceptance verification

### Цель
Верифицировать verbatim AC Story 1 (epic L144–149) после [`task-ids-06-01-t01-conftest-autouse-fixtures`](../task-ids-06-01-t01-conftest-autouse-fixtures/README.md).

### Почему это важно
Security-инвариант: unit/integration offline никогда не трогают production Supabase (epic §1 L13).

### Факты из кода
1. Story 1 AC — [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) L144–149.
2. [`task-ids-06-01-t01-conftest-autouse-fixtures`](../task-ids-06-01-t01-conftest-autouse-fixtures/README.md) — реализует фикстуры.
3. [`tests/integration/supabase/.gitkeep`](../../../../../../../tests/integration/supabase/.gitkeep) — каталог для auto-marker тестов.

### Gap
Нет автоматической проверки AC L144–149.

### AC/DoD
- [x] (P0) `pytest tests/ -q` без `.env` файла — все unit-тесты `DB_BACKEND=in_memory`, `EID_PROVIDER=mock`.
- [x] (P0) `pytest tests/ -q` с `.env` содержащим `DB_BACKEND=supabase` + реальные creds — тесты используют in_memory (env перезаписан).
- [x] (P0) `tests/integration/supabase/*.py` автоматически помечены `live_integration` без явного декоратора.
- [x] (P0) `pytest -m "not live_integration" -q` — пропускает все Supabase тесты.
- [x] (P0) В тесте, переопределяющем env через свой `monkeypatch.setenv()` ПОСЛЕ autouse — переопределение работает (autouse применяется первым).

### Где менять код
- `doge-identity-service/tests/conftest.py` (при необходимости — тесты в `tests/test_conftest_env_isolation.py` только если epic не запрещает; предпочтительно ручные команды из epic §8)

### Out of scope
- Реализация фикстур — t01
- Live Supabase tests — Story 3

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/ -q
# с .env supabase+creds — in_memory
.venv/bin/python -m pytest -m "not live_integration" -q
```
