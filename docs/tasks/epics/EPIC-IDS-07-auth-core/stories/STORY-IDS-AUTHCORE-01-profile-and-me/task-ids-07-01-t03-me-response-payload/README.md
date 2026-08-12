## Task workspace — `task-ids-07-01-t03-me-response-payload`

- Story: [`../STORY-IDS-AUTHCORE-01-profile-and-me.md`](../STORY-IDS-AUTHCORE-01-profile-and-me.md)
- Prerequisite: [`../task-ids-07-01-t02-handle-me-handler/README.md`](../task-ids-07-01-t02-handle-me-handler/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000009`  
**Skill declared:** python-pro  
---

## Task: implement — `/me` response payload (profile + rights)

### Цель
Сформировать `data` для `GET /me`: `supabase_user_id`, `eid_verified`, поля профиля (если есть), **базовые права** — без новой permission-системы.

### Почему это важно
Story Scope п.3 и AC #2; gateway ожидает `eid_verified` ([`04-security §Часть A`](../../../../../../../runtime-docs/04-security.md), [`09-gateway-expectations.md`](../../../../../../../runtime-docs/09-gateway-expectations.md)).

### Факты из кода
1. [`models.py:22-40`](../../../../../../../src/core/domain/models.py) — `ProfileRecord` поля (display_name, avatar_url, eid_*, wallet_*).
2. [`models.py:16-19`](../../../../../../../src/core/domain/models.py) — `UserClaims.role` (JWT role).
3. [`05-data-model.md`](../../../../../../../runtime-docs/05-data-model.md) — описание полей profiles.
4. [`01-api.md:24`](../../../../../../../runtime-docs/01-api.md) — «профиль + права» для `/me`.

### Gap / Проблема
Stub не возвращает структуру `data`; нет mapper profile → JSON.

### AC/DoD
- [x] (P0) `data` содержит минимум `supabase_user_id`, `eid_verified` (story AC #2).
- [x] (P0) При наличии `ProfileRecord` — в `data` попадают поля профиля из модели (как минимум display_name/avatar_url или согласованный подмножество — зафиксировать в BULLRUN).
- [x] (P0) **Базовые права:** минимум `role` из `UserClaims` (или эквивалентный ключ `permissions`/`rights` — один стабильный контракт, без RBAC-матрицы).
- [x] (P0) Envelope остаётся `{"data": {...}}` ([`envelope.py:6-7`](../../../../../../../src/core/api/envelope.py)).
- [x] (P1) Datetime поля сериализуются в ISO-8601 строки (JSON-safe).

### Где менять код
- `doge-identity-service/src/core/api/handlers.py` и/или новый модуль рядом (напр. `core/api/me_response.py`)

### Out of scope
- OAuth introspection endpoint — STORY-IDS-OAUTH-02
- Новая permission/RBAC система

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_me_profile.py -q -k payload 2>/dev/null || echo "run after t05"
```
