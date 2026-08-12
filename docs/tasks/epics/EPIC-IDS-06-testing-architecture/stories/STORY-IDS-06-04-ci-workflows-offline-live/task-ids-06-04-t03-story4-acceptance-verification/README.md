## Task workspace — `task-ids-06-04-t03-story4-acceptance-verification`

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000008`  
**Decision Ref:** [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 4  
**Story:** [`../STORY-IDS-06-04-ci-workflows-offline-live.md`](../STORY-IDS-06-04-ci-workflows-offline-live.md)  
---

## Task: tests — Story 4 acceptance verification

### Цель
Верифицировать verbatim AC Story 4 (epic L244–248) для обоих workflows.

### Почему это важно
Разделение offline (every push) и live (main only) — security/ops инвариант эпика.

### Факты из кода
1. Story 4 AC — [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) L244–248.
2. Epic §8 L302–303 — `gh run list --workflow=test-offline.yml`.

### Gap
Нет проверки trigger matrix и timing AC.

### AC/DoD
- [x] (P0) `test-offline.yml` запускается на каждый push и PR.
- [x] (P0) `integration-live.yml` — только merge в `main` или ручной запуск.
- [x] (P0) В offline workflow нет `SUPABASE_*` secrets → live-тесты SKIPPED.
- [x] (P0) Offline workflow < 5 минут (setup + install + tests).

### Где менять код
- N/A (verification via GitHub Actions UI / `gh`)

### Out of scope
- Implementing workflows — t01–t02

### Проверка
```bash
gh run list --workflow=test-offline.yml --limit 1
gh run list --workflow=integration-live.yml --limit 1
```
