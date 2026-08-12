## Task workspace — `task-ids-08-01-t07-story-acceptance-verification`

- Story: [`../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md) AC #1–#4

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000011`  
**Skill declared:** python-pro  
---

## Task: tests — story acceptance verification

### Цель
Формально закрыть STORY-IDS-CLEANUP-01: прогнать все AC #1–#4, зафиксировать evidence в acceptance-артефакте и BULLRUN-PHASE-LOG.

### Почему это важно
Финальная точка story wave pkg-000011; без acceptance нельзя перевести story в Done.

### Факты из кода
После t01–t06 ожидается:
1. `/ready` 200 на bootstrap без `story_drafts` (AC #1).
2. Grep clean в `src/` и `tests/` (AC #2, migration exempt).
3. Offline pytest green (AC #3).
4. req-15 deprecated (AC #4).

### Gap / Проблема
Нет формального acceptance report для CLEANUP-01.

### AC/DoD
- [x] (P0) Story AC #1: evidence `/ready` 200 + `schema:true` (test или manual log).
- [x] (P0) Story AC #2: `rg` по `src tests` — 0 hits (migration/changelog exempt).
- [x] (P0) Story AC #3: `pytest -m "not live_integration" -q` — N passed, 0 failed.
- [x] (P0) Story AC #4: req-15 содержит deprecated banner.
- [x] (P1) Создан `acceptance-verification-task-ids-08-01-t07-story-acceptance-verification.md` в этой папке.
- [x] (P1) Создан `BULLRUN-PHASE-LOG.md` в этой папке (P3).

### Где менять код
- Task-артефакты в этой папке (P3):
  - `acceptance-verification-task-ids-08-01-t07-story-acceptance-verification.md`
  - `BULLRUN-PHASE-LOG.md`
- Обновить статус story в pipeline story file → Done (P3/P5)

### Out of scope
- Epic gate EPIC-IDS-08 (CLEANUP-02/03 вне pkg-000011)
- Runtime-docs drift (CLEANUP-03)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
rg "story_drafts|StoryDraft|story-drafts|submit-story" src tests --glob '!*migrations*'
# AC #1: pytest tests/test_db_supabase_healthcheck.py или live /ready check
head -10 docs/requirements/15-story-authorization.md | rg -i deprecated
```
