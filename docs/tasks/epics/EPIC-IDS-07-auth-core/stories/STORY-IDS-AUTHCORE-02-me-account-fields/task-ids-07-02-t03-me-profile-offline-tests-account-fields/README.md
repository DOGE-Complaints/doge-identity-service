## Task workspace — `task-ids-07-02-t03-me-profile-offline-tests-account-fields`

- Story: [`../STORY-IDS-AUTHCORE-02-me-account-fields.md`](../STORY-IDS-AUTHCORE-02-me-account-fields.md)
- Prerequisite: [`../task-ids-07-02-t01-me-response-created-at-account-status/README.md`](../task-ids-07-02-t01-me-response-created-at-account-status/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000044`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md`](../../../../../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md)  
---

## Task: tests — offline `/me` account fields (`created_at` / `account_status`)

### Цель
Расширить `test_me_profile.py`: с профилем → ISO `created_at`; без профиля → `null`; `account_status=="active"` в обоих случаях; offline-сюита зелёная.

### Почему это важно
Story AC #1–#2, #5; регрессия no-auto-provision.

### Факты из кода
1. [`tests/test_me_profile.py`](../../../../../../../tests/test_me_profile.py) — существующие offline-кейсы `/me`.
2. [`me_response.py`](../../../../../../../src/core/api/me_response.py) — цель t01 после P3.

### Gap / Проблема
Нет assertions на `created_at` / `account_status`.

### AC/DoD
- [x] (P0) С профилем: `data["created_at"]` = ISO из `profile.created_at`; `account_status == "active"`.
- [x] (P0) Без профиля: `created_at is None`; `account_status == "active"`.
- [x] (P0) `.venv/bin/python -m pytest tests/test_me_profile.py -q` green.
- [x] (P0) `.venv/bin/python -m pytest -q -m "not live_integration"` green.

### Где менять код
- `doge-identity-service/tests/test_me_profile.py`

### Out of scope
- Live integration; email assertions (ONB-01)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_me_profile.py -q
.venv/bin/python -m pytest -q -m "not live_integration"
```
