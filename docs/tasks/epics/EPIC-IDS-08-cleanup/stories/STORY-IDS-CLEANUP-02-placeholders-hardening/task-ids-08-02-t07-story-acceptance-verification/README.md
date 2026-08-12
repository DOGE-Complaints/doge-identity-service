## Task workspace — `task-ids-08-02-t07-story-acceptance-verification`

- Story: [`../STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../STORY-IDS-CLEANUP-02-placeholders-hardening.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-02-placeholders-hardening.md) AC #1–#4

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000013`  
**Skill declared:** python-pro  
---

## Task: tests — story acceptance verification

### Цель
Формально закрыть STORY-IDS-CLEANUP-02: прогнать все AC #1–#4, зафиксировать evidence в acceptance-артефакте и BULLRUN-PHASE-LOG.

### Почему это важно
Финальная точка story wave pkg-000013; без acceptance нельзя перевести story в Done.

### Факты из кода
После t01–t06 ожидается:
1. [`owner-decisions-e17-e22.md`](../task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/owner-decisions-e17-e22.md) — 5 решений (AC #1).
2. E17: validation + foreign-domain test **или** config removed (AC #2 conditional).
3. Removed placeholders: grep = 0 per t01 decisions (AC #3).
4. Offline pytest green (AC #4).

### Gap / Проблема
Нет формального acceptance report для CLEANUP-02.

### AC/DoD
- [ ] (P0) Story AC #1: evidence — owner decisions выполнены (t01 artifact + t02–t06 closed).
- [ ] (P0) Story AC #2: evidence — если ALLOWED_RETURN_URLS остаётся, test reject foreign domain PASS.
- [ ] (P0) Story AC #3: `rg` по идентификаторам удалённых заготовок = 0 (per t01).
- [ ] (P0) Story AC #4: `pytest -m "not live_integration" -q` — N passed, 0 failed.
- [ ] (P1) Создан `acceptance-verification-task-ids-08-02-t07-story-acceptance-verification.md` в этой папке.
- [ ] (P1) Создан `BULLRUN-PHASE-LOG.md` в этой папке (P3).

### Где менять код
- Task-артефакты в этой папке (P3):
  - `acceptance-verification-task-ids-08-02-t07-story-acceptance-verification.md`
  - `BULLRUN-PHASE-LOG.md`
- Обновить статус story в pipeline story file → Done (P3/P5)
- Обновить backlog story AC checkboxes (P3/P5, backlog file не удалять)

### Out of scope
- Epic gate EPIC-IDS-08 (CLEANUP-03 вне pkg-000013)
- Runtime-docs full sync (CLEANUP-03)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
# AC #3 — примеры grep (adjust per t01 removed identifiers):
rg "StubBearerTokenAuth" src tests || true
rg "resolve_idempotency_key" src/ || true
rg "allowed_return_urls" src/ || true
rg "code_verifier_encryption" src/ || true
rg "core\.audit|core\.oauth|core\.profiles" src/ || true
```
