## Task workspace — `task-ids-06-05-t02-story5-acceptance-verification`

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000008`  
**Decision Ref:** [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 5  
**Story:** [`../STORY-IDS-06-05-live-server-smoke.md`](../STORY-IDS-06-05-live-server-smoke.md)  
---

## Task: tests — Story 5 acceptance verification

### Цель
Верифицировать verbatim AC Story 5 (epic L267–270) после t01.

### Почему это важно
Smoke — операторская проверка deploy, отдельно от CI offline/live markers.

### Факты из кода
1. Story 5 AC — [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) L267–270.
2. Epic §8 L305–309 — `make serve` + `IDENTITY_URL` smoke pattern.

### Gap
Нет формальной проверки AC L267–270.

### AC/DoD
- [x] (P0) `IDENTITY_URL=http://localhost:8100 pytest tests/smoke/ -v` — PASSED при запущенном сервере (`make serve`).
- [x] (P0) Smoke тесты НЕ входят в `pytest tests/ -q` (`collect_ignore = ["smoke"]` в `tests/conftest.py`; `testpaths` остаётся `["tests"]`).
- [x] (P1) `IDENTITY_URL=https://identity.dogestonia.ee pytest tests/smoke/` работает против Railway deploy.

### Где менять код
- N/A (verification)

### Out of scope
- Автоматический production smoke — epic §9 L315

### Проверка
```bash
cd doge-identity-service
make serve &
sleep 3
IDENTITY_URL=http://localhost:8100 .venv/bin/python -m pytest tests/smoke/ -v
kill %1
```
