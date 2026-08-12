## Task workspace — `task-ids-09-01-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-EID-01-eid-verification-flow.md`](../STORY-IDS-EID-01-eid-verification-flow.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-EID-01-eid-verification-flow.md`](../../../../../../backlog-stories/STORY-IDS-EID-01-eid-verification-flow.md) AC

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000015`  
**Skill declared:** python-pro  
---

## Task: tests — Story EID-01 acceptance verification

### Цель
Верифицировать все AC story verbatim после t01–t05; оформить `acceptance-verification-*.md` + `BULLRUN-PHASE-LOG.md`.

### Почему это важно
Закрытие story в bullrun; traceability backlog → pipeline → code.

### Факты из кода
1. Story AC — [`../STORY-IDS-EID-01-eid-verification-flow.md`](../STORY-IDS-EID-01-eid-verification-flow.md) §Acceptance Criteria.
2. Epic verify — [`../../../../EPIC-IDS-09-eid-verification.md`](../../../../EPIC-IDS-09-eid-verification.md) §7.
3. Tasks t01–t05 — implementation + tests.

### Gap / Проблема
Нет acceptance-verification артефакта для story.

### AC/DoD
- [x] (P0) `POST /auth/eid/start` (валидный JWT) → создаёт сессию `started`, отдаёт redirect к провайдеру.
- [x] (P0) callback с валидным `state` → профиль становится `eid_verified=true`, заполнены `verified_person_hash`/`eid_verified_at`.
- [x] (P0) Повторный callback / просроченная сессия → корректная обработка (не перезаписывает терминальный статус).
- [x] (P0) Конфликт `verified_person_hash` → `ProfileConflictError`/409.
- [x] (P0) Каждое событие пишется в `eid_audit_events` без PII.
- [x] (P0) Полный флоу проходит на `mock` офлайн-тестом.
- [x] (P1) `acceptance-verification-task-ids-09-01-t06-story-acceptance-verification.md` с таблицей AC → PASS/FAIL + команды.

### Где менять код
- `acceptance-verification-task-ids-09-01-t06-story-acceptance-verification.md` (this folder)
- `BULLRUN-PHASE-LOG.md` (this folder)

### Out of scope
- Новая функциональность сверх story AC
- eideasy/authentigate — EID-02

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
```
