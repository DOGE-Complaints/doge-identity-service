## Task workspace — `task-ids-13-02-t01-me-response-email-and-email-verified`

- Story: [`../STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md`](../STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md)
- Prerequisite: AUTHCORE-01/02 Done (`build_me_data` exists; preserve `created_at`/`account_status`)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000045`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md`](../../../../../../backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md); [`identity-cabinet-me-fields-interview-2026-07-13.md`](../../../../../../../analysis/identity-cabinet-me-fields-interview-2026-07-13.md) (D-CAB-3)  
---

## Task: implement — `email` + `email_verified` в `build_me_data`

### Цель
В базовый dict `build_me_data` добавить `email=current_user.email` и `email_verified=True` (включая no-profile). Не удалять поля AUTHCORE-02.

### Почему это важно
CAB-02 Account Summary / consumers нуждаются в email; D-CAB-3 — политика «токен ⇒ подтверждён». Story AC #1–#2.

### Факты из кода
1. [`me_response.py:17-49`](../../../../../../../src/core/api/me_response.py) — нет `email`/`email_verified`; есть `created_at`/`account_status`.
2. [`models.py:16-19`](../../../../../../../src/core/domain/models.py) — `UserClaims.email: str | None`.

### Gap / Проблема
`/me` не эмитит `email` / `email_verified`.

### AC/DoD
- [x] (P0) Базовый dict: `email=current_user.email`, `email_verified=True` (и при `profile is None`).
- [x] (P0) Сохранены AUTHCORE-02 поля `created_at` / `account_status`.
- [x] (P1) Import smoke: `from core.api.me_response import build_me_data`.

### Где менять код
- `doge-identity-service/src/core/api/me_response.py` only

### Out of scope
- Runbook / API docs (t02); tests (t03); hard email gate

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.api.me_response import build_me_data"
rg -n 'email|email_verified|created_at|account_status' src/core/api/me_response.py
```
