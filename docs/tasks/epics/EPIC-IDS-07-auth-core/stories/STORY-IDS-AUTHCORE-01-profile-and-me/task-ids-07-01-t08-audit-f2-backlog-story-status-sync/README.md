## Task workspace — `task-ids-07-01-t08-audit-f2-backlog-story-status-sync`

- Story: [`../STORY-IDS-AUTHCORE-01-profile-and-me.md`](../STORY-IDS-AUTHCORE-01-profile-and-me.md)
- Audit source: [`../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md) (F2)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000010`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md) §F2  
---

## Task: fix — backlog story status and epic alias sync (F2)

### Цель
Привести backlog SSOT [`STORY-IDS-AUTHCORE-01-profile-and-me.md`](../../../../../../backlog-stories/STORY-IDS-AUTHCORE-01-profile-and-me.md) в соответствие с фактом: story 🟢 Done под **EPIC-IDS-07**, `/me` реализован (не stub 501).

### Почему это важно
Backlog INDEX и операторы читают backlog как SSOT; устаревший `⚪ Todo` и ссылка на `EPIC-IDS-AUTH-CORE` / stub вводят в заблуждение при следующем intake.

### Факты из кода
1. [`backlog-stories/STORY-IDS-AUTHCORE-01-profile-and-me.md:5-6`](../../../../../../backlog-stories/STORY-IDS-AUTHCORE-01-profile-and-me.md) — `Status: ⚪ Todo`, `Epic: EPIC-IDS-AUTH-CORE`.
2. [`backlog-stories/...:24`](../../../../../../backlog-stories/STORY-IDS-AUTHCORE-01-profile-and-me.md) — «Точки в коде» всё ещё `handle_me_stub` → 501.
3. Pipeline story: [`../STORY-IDS-AUTHCORE-01-profile-and-me.md`](../STORY-IDS-AUTHCORE-01-profile-and-me.md) — 🟢 Done, AC [x].
4. Runtime: [`asgi_app.py:166`](../../../../../../../src/core/api/asgi_app.py) — `/me` → `handle_me`.

### Gap / Проблема
Doc-stale в backlog; расхождение backlog ↔ pipeline ↔ код.

### AC/DoD
- [x] (P0) Backlog Meta: `Status: 🟢 Done` (или эквивалент принятого в INDEX формата).
- [x] (P0) Epic reference: `EPIC-IDS-07` (alias `EPIC-IDS-AUTH-CORE` — пояснение, не путать с несуществующим эпик-файлом).
- [x] (P0) Секция «Точки в коде» отражает `handle_me` / 200 (не stub 501).
- [x] (P0) AC checkboxes в backlog [x] — **verbatim** формулировки AC не менять.
- [x] (P1) Ссылка на pipeline story / pkg-000009 как `source` исполнения.

### Где менять код
- `doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-AUTHCORE-01-profile-and-me.md` only

### Out of scope
- Изменение AC текста story.
- Реализация нового функционала `/me`.

### Проверка
```bash
grep -n "Status\|handle_me\|501\|EPIC-IDS" doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-AUTHCORE-01-profile-and-me.md
```
