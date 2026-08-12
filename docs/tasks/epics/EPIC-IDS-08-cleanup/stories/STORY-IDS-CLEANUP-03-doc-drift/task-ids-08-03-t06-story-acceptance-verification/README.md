## Task workspace — `task-ids-08-03-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-CLEANUP-03-doc-drift.md`](../STORY-IDS-CLEANUP-03-doc-drift.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-03-doc-drift.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-03-doc-drift.md) AC #1–#4

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000014`  
**Skill declared:** python-pro  
---

## Task: tests — story acceptance verification

### Цель
Формально закрыть STORY-IDS-CLEANUP-03: прогнать все AC #1–#4, зафиксировать evidence в acceptance-артефакте и BULLRUN-PHASE-LOG.

### Почему это важно
Финальная точка story wave pkg-000014; docs-only story — acceptance по grep/doc evidence, не runtime pytest gate.

### Факты из кода
После t01–t05 ожидается:
1. req-08/req-02 reflect 4 migrations (AC #1).
2. `.env.example` AUTHENTIGATE_REDIRECT_URI matches `/auth/authentigate/callback` (AC #2).
3. req-15 deprecated + req-02/03 gateway direction (AC #3).
4. requirements ↔ runtime-docs aligned (AC #4).

### Gap / Проблема
Нет формального acceptance report для CLEANUP-03.

### AC/DoD
- [x] (P0) Story AC #1: evidence table — 4 migrations in req-08/req-02.
- [x] (P0) Story AC #2: evidence — `.env.example` redirect URI matches `asgi_app.py` route.
- [x] (P0) Story AC #3: evidence — req-15 deprecated; req-02/03 gateway→identity model.
- [x] (P0) Story AC #4: evidence — grep matrix requirements vs runtime-docs; no contradictions.
- [x] (P1) Создан `acceptance-verification-task-ids-08-03-t06-story-acceptance-verification.md` в этой папке (P3).
- [x] (P1) Создан `BULLRUN-PHASE-LOG.md` в этой папке (P3).
- [x] (P1) Pipeline story status → Done; bullrun sync (P3).

### Где менять код
- Task-артефакты в этой папке (P3):
  - `acceptance-verification-task-ids-08-03-t06-story-acceptance-verification.md`
  - `BULLRUN-PHASE-LOG.md`
- [`../STORY-IDS-CLEANUP-03-doc-drift.md`](../STORY-IDS-CLEANUP-03-doc-drift.md) — AC checkboxes + status Done (P3)
- [`bullrun-launch-index.md`](../../../../bullrun-launch-index.md) — story/task rows Done (P3)

### Out of scope
- EPIC-IDS-08 epic gate (after all CLEANUP stories Done)
- EPIC-IDS-07 epic gate
- pytest full suite (optional smoke only if operator requests)

### Проверка
```bash
cd doge-identity-service
grep -n "provider_abstraction\|20260526000001" docs/requirements/08-supabase-migrations.md
grep AUTHENTIGATE_REDIRECT_URI .env.example
head -5 docs/requirements/15-story-authorization.md | grep -i deprecated
grep -rn "story-drafts" docs/requirements/ docs/runtime-docs/ | head -30
```
