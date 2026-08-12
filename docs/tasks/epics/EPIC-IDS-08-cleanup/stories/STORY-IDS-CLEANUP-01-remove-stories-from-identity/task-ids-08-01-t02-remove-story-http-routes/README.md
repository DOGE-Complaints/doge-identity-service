## Task workspace — `task-ids-08-01-t02-remove-story-http-routes`

- Story: [`../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md) Scope п.2

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000011`  
**Skill declared:** python-pro  
---

## Task: implement — remove story HTTP routes

### Цель
Удалить story-роуты (4 POST stubs 501) и их записи в `PROTECTED_OPTIONS_PATHS` из ASGI-приложения.

### Почему это важно
Истории — домен gateway ([`09-gateway-expectations`](../../../../../../../runtime-docs/09-gateway-expectations.md)); identity не должен экспонировать story endpoints. Story AC #2.

### Факты из кода
1. [`asgi_app.py:32-35`](../../../../../../../src/core/api/asgi_app.py) — `PROTECTED_OPTIONS_PATHS` включает `/story-drafts`, `/story-drafts/{draft_id}/submit`, `/stories`, `/gpt/actions/submit-story`.
2. [`asgi_app.py:258-310`](../../../../../../../src/core/api/asgi_app.py) — четыре `@app.post` handlers с `next_epic="EPIC-IDS-STORIES"`.
3. Smoke-тесты могут ссылаться на эти пути (обновить в t06).

### Gap / Проблема
Story-роуты остаются в контракте identity, хотя домен вынесен в gateway.

### AC/DoD
- [x] (P0) Удалены 4 POST route handlers (`/story-drafts`, `/story-drafts/{draft_id}/submit`, `/stories`, `/gpt/actions/submit-story`).
- [x] (P0) Удалены соответствующие пути из `PROTECTED_OPTIONS_PATHS`.
- [x] (P0) Story AC #2: grep по `asgi_app.py` не находит story-роуты.

### Где менять код
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py)

### Out of scope
- Domain/repos/DI — t03
- Полный grep cleanup — t06/t07

### Проверка
```bash
cd doge-identity-service
rg "story-drafts|/stories|submit-story" src/core/api/asgi_app.py
# ожидание: 0 matches
.venv/bin/python -m pytest tests/ -m "not live_integration" -q -k "asgi or route or smoke" 2>/dev/null || true
```
