## Task workspace — `task-ids-07-01-t05-me-offline-tests`

- Story: [`../STORY-IDS-AUTHCORE-01-profile-and-me.md`](../STORY-IDS-AUTHCORE-01-profile-and-me.md)
- Prerequisite: [`../task-ids-07-01-t04-asgi-route-wire-handle-me/README.md`](../task-ids-07-01-t04-asgi-route-wire-handle-me/README.md), решение t01

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000009`  
**Skill declared:** python-pro  
---

## Task: tests — offline `/me` coverage (in_memory)

### Цель
Покрыть story AC offline: 401 без токена, 200 с JWT, missing profile (per t01), envelope; обновить тесты, ожидающие 501.

### Почему это важно
Story AC #1, #2, #3, #4, #5; регрессия transport smoke после замены stub.

### Факты из кода
1. [`test_http_transport_smoke.py:73-83`](../../../../../../../tests/test_http_transport_smoke.py) — 401 OK; 501 с bearer — **нужно 200**.
2. [`test_asgi_transport.py:57-65`](../../../../../../../tests/test_asgi_transport.py) — аналогично 501 → 200.
3. [`tests/conftest.py`](../../../../../../../tests/conftest.py) — `test_client`, `_block_dotenv_leakage` → `DB_BACKEND=in_memory`.
4. [`test_supabase_jwt_auth.py:141-143`](../../../../../../../tests/test_supabase_jwt_auth.py) — bearer проходит auth на `/me`.

### Gap / Проблема
Нет `tests/test_me_profile.py`; существующие тесты assert 501.

### AC/DoD
- [x] (P0) `GET /me` без токена → 401 `AUTHENTICATION_REQUIRED` (regression).
- [x] (P0) Валидный JWT + seeded profile → 200, `data.supabase_user_id`, `data.eid_verified`, поля профиля.
- [x] (P0) Missing profile → детерминированный ответ per t01 + явный тест.
- [x] (P0) Top-level ключ ответа — `data` (envelope).
- [x] (P0) Все тесты offline (`pytest -m "not live_integration"`), `DB_BACKEND=in_memory` via conftest.
- [x] (P1) Обновлены `test_http_transport_smoke` / `test_asgi_transport` (501 → 200).

### Где менять код
- `doge-identity-service/tests/test_me_profile.py` (new)
- `doge-identity-service/tests/test_http_transport_smoke.py`
- `doge-identity-service/tests/test_asgi_transport.py`

### Out of scope
- Live Supabase `/me` — отдельный live tier
- Smoke `tests/smoke/` against running server

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q tests/test_me_profile.py tests/test_http_transport_smoke.py tests/test_asgi_transport.py
```
