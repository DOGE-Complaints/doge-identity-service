## Task workspace — `task-ids-11-01-t08-audit-f1-backlog-story-doc-sync`

- Story: [`../STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../STORY-IDS-OAUTH-01-oauth-server-endpoints.md)
- Audit source: [`../../../../../../analysis/epic-ids-11-oauth-01-audit-2026-06-24.md`](../../../../../../analysis/epic-ids-11-oauth-01-audit-2026-06-24.md) (F1)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_11_oauth_01_audit_2026_06_24`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-11-oauth-01-audit-2026-06-24.md`](../../../../../../analysis/epic-ids-11-oauth-01-audit-2026-06-24.md) §F1  
---

## Task: fix — backlog STORY-IDS-OAUTH-01 doc sync (F1)

### Цель
Привести backlog SSOT [`STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) в соответствие с фактом: story 🟢 Done под **EPIC-IDS-11** (pkg-000029).

### Почему это важно
Backlog читается при intake; устаревший `⚪ Todo`, AC `[ ]` и «Точки в коде» с 501 вводят в заблуждение (рекуррентный паттерн PV-06 audit F1).

### Факты из кода
1. [`backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md:6`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) — `Status: ⚪ Todo`.
2. [`...:11`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) — «маршруты `/oauth/*` пока 501».
3. [`...:26-30`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) — устаревшие line refs (`asgi_app.py:219-256`, `repositories.py:238-346`, `client_secret` не проверяется).
4. [`...:33-40`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) — AC checkboxes `[ ]`.
5. Pipeline story: [`../STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../STORY-IDS-OAUTH-01-oauth-server-endpoints.md) — 🟢 Done, AC [x].
6. Код: роуты [`asgi_app.py:369-403`](../../../../../../../src/core/api/asgi_app.py); handlers [`core/oauth/handlers.py`](../../../../../../../src/core/oauth/handlers.py).

### Gap / Проблема
Doc-stale в backlog; расхождение backlog ↔ pipeline ↔ epic (audit F1 MEDIUM).

### AC/DoD
- [x] (P0) Backlog Meta: `Status: 🟢 Done`.
- [x] (P0) AC checkboxes в backlog [x] — **verbatim** формулировки AC не менять.
- [x] (P0) «Точки в коде» → актуальные пути (`core/oauth/`, `InMemoryAuthorizationRequestStore`, `verify_client_secret`, `asgi_app.py:368-403`).
- [x] (P1) «Зачем простыми словами» — убрать «пока 501» (факт: построено).
- [x] (P1) Ссылка на pipeline story / pkg-000029 как источник исполнения.

### Где менять код
- `doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md`

### Out of scope
- Изменение AC текста story (verbatim).
- Код, pytest, runtime-docs, `EPIC-IDS-OAUTH.md` (t09).
- `identity-active-package.current.yaml`, pkg-000029 yaml.

### Проверка
```bash
grep -n "Status\|\[x\]\|\[ \]\|501\|asgi_app" \
  doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md
```
