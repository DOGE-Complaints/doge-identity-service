## Task workspace — `task-ids-13-02-t03-me-profile-offline-tests-email-fields`

- Story: [`../STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md`](../STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md)
- Prerequisite: [`../task-ids-13-02-t01-me-response-email-and-email-verified/README.md`](../task-ids-13-02-t01-me-response-email-and-email-verified/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000045`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md`](../../../../../../backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md)  
---

## Task: tests — offline `/me` email fields

### Цель
Расширить `test_me_profile.py`: `email` из токена (`null`, если claim отсутствует); `email_verified is True`; сохранить asserts AUTHCORE-02; offline-сюита зелёная.

### Почему это важно
Story AC #1–#2, #5; регрессия одного билдера `/me` с AUTHCORE-02.

### Факты из кода
1. [`tests/test_me_profile.py`](../../../../../../../tests/test_me_profile.py) — offline `/me` без email asserts.
2. [`supabase_jwt_harness.py:66-85`](../../../../../../../tests/supabase_jwt_harness.py) — `email=` уже в mint.

### Gap / Проблема
Нет assertions на `email` / `email_verified`.

### AC/DoD
- [x] (P0) С default JWT email: `data["email"]` соответствует claim; `email_verified is True`.
- [x] (P0) Без email claim: `email is None`; `email_verified is True`.
- [x] (P0) AUTHCORE-02 asserts (`created_at` / `account_status`) не сломаны.
- [x] (P0) `.venv/bin/python -m pytest tests/test_me_profile.py -q` green.
- [x] (P0) `.venv/bin/python -m pytest -q -m "not live_integration"` green.

### Где менять код
- `doge-identity-service/tests/test_me_profile.py`

### Out of scope
- Live integration; spa

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_me_profile.py -q
.venv/bin/python -m pytest -q -m "not live_integration"
```
