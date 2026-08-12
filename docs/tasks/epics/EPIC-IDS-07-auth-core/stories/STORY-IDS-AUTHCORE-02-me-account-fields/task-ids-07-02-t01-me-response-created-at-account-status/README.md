## Task workspace — `task-ids-07-02-t01-me-response-created-at-account-status`

- Story: [`../STORY-IDS-AUTHCORE-02-me-account-fields.md`](../STORY-IDS-AUTHCORE-02-me-account-fields.md)
- Prerequisite: AUTHCORE-01 Done (`build_me_data` exists)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000044`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md`](../../../../../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md); [`identity-cabinet-me-fields-interview-2026-07-13.md`](../../../../../../../analysis/identity-cabinet-me-fields-interview-2026-07-13.md) (D-CAB-1/2)  
---

## Task: implement — `created_at` + `account_status` в `build_me_data`

### Цель
В `GET /me` `data` всегда отдавать `account_status="active"` и `created_at` из `ProfileRecord.created_at` (ISO) или `null` без профиля — без миграций и без Auth.

### Почему это важно
CAB-02 Account Summary ждёт эти поля; identity-гап MVP (D-CAB-1/2). Story AC #1–#2 (частично) и AC #3 (grep gate).

### Факты из кода
1. [`me_response.py:17-46`](../../../../../../../src/core/api/me_response.py) — `build_me_data` без `created_at`/`account_status`.
2. [`me_response.py:11-14`](../../../../../../../src/core/api/me_response.py) — `_format_datetime` уже есть.
3. [`models.py:44`](../../../../../../../src/core/domain/models.py) — `ProfileRecord.created_at` уже в модели.

### Gap / Проблема
`/me` не эмитит CAB-02 account fields (`created_at`, `account_status`).

### AC/DoD
- [x] (P0) Базовый dict: `account_status="active"`, `created_at=None`.
- [x] (P0) При `profile is not None`: `created_at = _format_datetime(profile.created_at)`.
- [x] (P0) Не трогать `email` / `email_verified` (ONB-01).
- [x] (P0) `grep account_status supabase/bootstrap/` → пусто (нет миграции).
- [x] (P1) Unit/import smoke: `build_me_data` импортируется без ошибок.

### Где менять код
- `doge-identity-service/src/core/api/me_response.py` only

### Out of scope
- API docs (t02), tests (t03), email (ONB-01), spa CAB-api note

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.api.me_response import build_me_data"
rg -n 'account_status' supabase/bootstrap/ || true
# expect: no matches
```
