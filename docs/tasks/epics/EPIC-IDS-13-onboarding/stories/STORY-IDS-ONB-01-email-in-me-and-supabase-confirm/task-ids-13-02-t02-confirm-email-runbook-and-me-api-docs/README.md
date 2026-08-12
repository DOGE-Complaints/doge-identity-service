## Task workspace — `task-ids-13-02-t02-confirm-email-runbook-and-me-api-docs`

- Story: [`../STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md`](../STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md)
- Prerequisite: [`../task-ids-13-02-t01-me-response-email-and-email-verified/README.md`](../task-ids-13-02-t01-me-response-email-and-email-verified/README.md) (контракт кода)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000045`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md`](../../../../../../backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md)  
---

## Task: docs — Confirm email runbook + MeData `email` / `email_verified`

### Цель
Зафиксировать обязательный «Confirm email» в Supabase runbook; синхронизировать OpenAPI `MeData` и `API_REFERENCE.md §6` (`email` nullable; `email_verified` bool, «политика: токен ⇒ true»).

### Почему это важно
Story AC #3–#4; `email_verified` корректен только при Confirm email.

### Факты из кода
1. [`supabase-project-setup.md`](../../../../../../../docs/runbook/supabase-project-setup.md) — нет Confirm email (grep пусто до P3).
2. [`openapi.yaml`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) `MeData` — без `email`/`email_verified`.
3. [`API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) §6 — пример `/me` без email fields.

### Gap / Проблема
Нет runbook-предусловия и consumer-facing схемы для email fields.

### AC/DoD
- [x] (P0) `supabase-project-setup.md` — обязательный пункт включить «Confirm email» (Auth → Providers → Email); связь с `email_verified`.
- [x] (P0) `openapi.yaml` `MeData`: `email` (`string|null`); `email_verified` (boolean + description политика токен ⇒ true).
- [x] (P0) `API_REFERENCE.md §6` — те же поля в примере/описании `/me`.
- [x] (P1) `rg` Confirm email / `email_verified` в трёх файлах — hits.

### Где менять код
- `doge-identity-service/docs/runbook/supabase-project-setup.md`
- `doge-identity-service/docs/runtime-docs/api-reference/openapi.yaml`
- `doge-identity-service/docs/runtime-docs/api-reference/API_REFERENCE.md`

### Out of scope
- `me_response.py` (t01); tests (t03)

### Проверка
```bash
cd doge-identity-service
rg -n 'Confirm email|email_verified|"email"' \
  docs/runbook/supabase-project-setup.md \
  docs/runtime-docs/api-reference/openapi.yaml \
  docs/runtime-docs/api-reference/API_REFERENCE.md
```
