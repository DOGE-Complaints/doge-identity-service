## Task workspace — `task-ids-09-06-t07-audit-f1-backlog-story-status-sync`

- Story: [`../STORY-IDS-EID-06-browser-callback-redirect.md`](../STORY-IDS-EID-06-browser-callback-redirect.md)
- Audit source: [`../../../../../../analysis/epic-ids-09-eid-06-audit-2026-06-08.md`](../../../../../../analysis/epic-ids-09-eid-06-audit-2026-06-08.md) (F1)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_09_eid_06_audit_2026_06_08`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-09-eid-06-audit-2026-06-08.md`](../../../../../../analysis/epic-ids-09-eid-06-audit-2026-06-08.md) §F1  
---

## Task: fix — backlog story status and code refs sync (F1)

### Цель
Привести backlog SSOT [`STORY-IDS-EID-06-browser-callback-redirect.md`](../../../../../../backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md) в соответствие с фактом: story 🟢 Done под **EPIC-IDS-09** (pkg-000019), callback redirect + динамический роут реализованы (не JSON-only callback / pre-EID-06 hardcoded routes).

### Почему это важно
Backlog INDEX и операторы читают backlog как SSOT; устаревший `⚪ Todo`, устаревшие «Точки в коде» и AC `[ ]` вводят в заблуждение при intake EID-07+.

### Факты из кода
1. [`backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md:6`](../../../../../../backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md) — `Status: ⚪ Todo`.
2. [`backlog-stories/...:25-29`](../../../../../../backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md) — «Точки в коде» — устаревший JSON-исход ([`handlers.py:327-330`](../../../../../../../src/core/api/handlers.py)), захардкоженные роуты ([`asgi_app.py:214-248`](../../../../../../../src/core/api/asgi_app.py)).
3. [`backlog-stories/...:32-37`](../../../../../../backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md) — AC checkboxes `[ ]`.
4. Pipeline story: [`../STORY-IDS-EID-06-browser-callback-redirect.md`](../STORY-IDS-EID-06-browser-callback-redirect.md) — 🟢 Done, AC [x], «Точки в коде (реализовано)».
5. `EidCallbackOutcome`: [`eid_callback.py`](../../../../../../../src/core/api/eid_callback.py); handler → outcome: [`handlers.py:191-197`](../../../../../../../src/core/api/handlers.py).
6. Dynamic route + redirect render: [`asgi_app.py:77-97,242-261`](../../../../../../../src/core/api/asgi_app.py).
7. Redirect tests: [`tests/test_eid_callback_redirect.py`](../../../../../../../tests/test_eid_callback_redirect.py) — 7 offline tests; suite 232 passed.

### Gap / Проблема
Doc-stale в backlog; расхождение backlog ↔ pipeline ↔ код (audit F1 MEDIUM).

### AC/DoD
- [x] (P0) Backlog Meta: `Status: 🟢 Done`.
- [x] (P0) Секция «Точки в коде» отражает `EidCallbackOutcome`, dynamic `/auth/{provider}/callback`, 303 redirect + `Accept: application/json` (не pre-EID-06 line refs `handlers.py:327-330`, `asgi_app.py:214-248`).
- [x] (P0) AC checkboxes в backlog [x] — **verbatim** формулировки AC не менять.
- [x] (P1) Ссылка на pipeline story / pkg-000019 как источник исполнения.

### Где менять код
- `doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md` only

### Out of scope
- Изменение AC текста story (verbatim).
- Код, pytest, runtime-docs.
- Pipeline story «Точки в коде» (audit F1 scope = backlog only).

### Проверка
```bash
grep -n "Status\|EidCallbackOutcome\|/auth/{provider}/callback\|214-248\|327-330" \
  doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md
```
