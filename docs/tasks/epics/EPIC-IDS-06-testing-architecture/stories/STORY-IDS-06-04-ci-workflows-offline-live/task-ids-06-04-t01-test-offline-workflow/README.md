## Task workspace — `task-ids-06-04-t01-test-offline-workflow`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000008`  
**Decision Ref:** [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 4  
**Story:** [`../STORY-IDS-06-04-ci-workflows-offline-live.md`](../STORY-IDS-06-04-ci-workflows-offline-live.md)  
---

## Task: implement — test-offline GitHub Actions workflow

### Цель
Создать `.github/workflows/test-offline.yml` per epic §6 Story 4 Outputs L231–235.

### Почему это важно
Offline suite на каждый push/PR без сети и без Supabase secrets (epic Story 4 Why L228).

### Факты из кода
1. [`doge-identity-service/.github`](../../../../../../../.github) — каталог **отсутствует**.
2. Epic L231–235 — triggers `push`, `pull_request`; Python 3.11; `pip install -e ".[dev]"`; `pytest -q -m "not live_integration"`.
3. [`pyproject.toml`](../../../../../../../pyproject.toml) L30–37 — pytest config.

### Gap
`test-offline.yml` отсутствует.

### AC/DoD
- [x] (P0) Triggers: `push`, `pull_request`.
- [x] (P0) Python 3.11, `pip install -e ".[dev]"`.
- [x] (P0) `python -m pytest -q -m "not live_integration" --tb=short`.
- [x] (P1) Upload pytest results as artifact (epic L235).

### Где менять код
- `doge-identity-service/.github/workflows/test-offline.yml` (новый)

### Out of scope
- `integration-live.yml` — t02
- Story 4 acceptance — t03

### Проверка
```bash
# после push — локально симулировать:
cd doge-identity-service && .venv/bin/python -m pytest -q -m "not live_integration" --tb=short
```
