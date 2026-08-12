## Task workspace — `task-ids-07-01-t09-audit-f3-remove-handle-me-stub`

- Story: [`../STORY-IDS-AUTHCORE-01-profile-and-me.md`](../STORY-IDS-AUTHCORE-01-profile-and-me.md)
- Audit source: [`../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md) (F3)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000010`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md) §F3  
---

## Task: refactor — remove orphaned `handle_me_stub` (F3)

### Цель
Удалить неиспользуемый `handle_me_stub` и устаревшие ссылки на `EPIC-IDS-AUTH-CORE` в сообщении stub, если функция больше не вызывается из маршрутов.

### Почему это важно
Dead code усложняет навигацию и создаёт ложное впечатление, что `/me` всё ещё на заглушке.

### Факты из кода
1. [`handlers.py:41-52`](../../../../../../../src/core/api/handlers.py) — `handle_me_stub` → 501, `next_epic="EPIC-IDS-AUTH-CORE"`.
2. [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) — маршрут `/me` импортирует и вызывает `handle_me`, не stub.
3. Grep: `handle_me_stub` — только определение в `handlers.py` (после t04 wire).

### Gap / Проблема
Осиротевший stub после успешного AUTHCORE-01; устаревший `next_epic` alias.

### AC/DoD
- [x] (P0) `handle_me_stub` удалён **или** явно deprecated с нулевыми call-sites (предпочтительно удаление).
- [x] (P0) Нет импортов `handle_me_stub` в `asgi_app.py` и тестах.
- [x] (P0) `pytest -m "not live_integration" -q` — без регрессий.
- [x] (P1) Если stub нужен для совместимости — задокументировать в BULLRUN (одна строка why kept).

### Где менять код
- `doge-identity-service/src/core/api/handlers.py`
- опционально: grep по репо на `handle_me_stub`

### Out of scope
- Изменение поведения `handle_me`.
- OAuth / eID stubs (`handle_auth_*_stub`).

### Проверка
```bash
cd doge-identity-service
rg "handle_me_stub" src tests
.venv/bin/python -m pytest -m "not live_integration" -q tests/test_me_profile.py
```
