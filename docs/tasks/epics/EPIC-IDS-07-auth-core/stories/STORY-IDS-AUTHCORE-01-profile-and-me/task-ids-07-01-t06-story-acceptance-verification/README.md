## Task workspace — `task-ids-07-01-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-AUTHCORE-01-profile-and-me.md`](../STORY-IDS-AUTHCORE-01-profile-and-me.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-AUTHCORE-01-profile-and-me.md`](../../../../../../backlog-stories/STORY-IDS-AUTHCORE-01-profile-and-me.md) AC

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000009`  
**Skill declared:** python-pro  
---

## Task: tests — Story AUTHCORE-01 acceptance verification

### Цель
Верифицировать все AC story verbatim после t01–t05; оформить `acceptance-verification-*.md`.

### Почему это важно
Закрытие story в bullrun; traceability backlog → pipeline.

### Факты из кода
1. Story AC — [`../STORY-IDS-AUTHCORE-01-profile-and-me.md`](../STORY-IDS-AUTHCORE-01-profile-and-me.md) §Acceptance Criteria.
2. Epic verify — [`../../../../EPIC-IDS-07-auth-core.md`](../../../../EPIC-IDS-07-auth-core.md) §7.
3. Tasks t01–t05 — implementation + tests.

### Gap / Проблема
Нет acceptance-verification артефакта для story.

### AC/DoD
- [x] (P0) `GET /me` без токена → 401 `AUTHENTICATION_REQUIRED`.
- [x] (P0) `GET /me` с валидным Supabase JWT → 200, `data` содержит как минимум `supabase_user_id`, `eid_verified`, и (если есть) поля профиля.
- [x] (P0) Если профиля нет — поведение детерминировано и покрыто тестом.
- [x] (P0) Ответ в envelope-формате `{"data": {...}}`.
- [x] (P0) Покрыто тестами (offline, без сети) на оба backend'а (`in_memory`).
- [x] (P1) `acceptance-verification-task-ids-07-01-t06-story-acceptance-verification.md` с таблицей AC → PASS/FAIL + команды.

### Где менять код
- `acceptance-verification-task-ids-07-01-t06-story-acceptance-verification.md` (this folder)
- `BULLRUN-PHASE-LOG.md` (this folder)

### Out of scope
- Новая функциональность сверх story AC

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
```
