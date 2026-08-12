## Task workspace — `task-ids-07-02-t02-me-api-docs-created-at-account-status`

- Story: [`../STORY-IDS-AUTHCORE-02-me-account-fields.md`](../STORY-IDS-AUTHCORE-02-me-account-fields.md)
- Prerequisite: [`../task-ids-07-02-t01-me-response-created-at-account-status/README.md`](../task-ids-07-02-t01-me-response-created-at-account-status/README.md) (контракт кода)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000044`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md`](../../../../../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md)  
---

## Task: docs — `MeData` + API_REFERENCE: `created_at` / `account_status`

### Цель
Синхронизировать OpenAPI `MeData` и `API_REFERENCE.md §6` с полями CAB-02: `created_at` nullable date-time; `account_status` enum + «MVP: всегда active».

### Почему это важно
Story AC #4; фронт contract-first на CAB-api-requirements.

### Факты из кода
1. [`openapi.yaml`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) — схема `MeData` (без account fields до P3).
2. [`API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) §6 — пример `/me`.

### Gap / Проблема
Доки не описывают `created_at` / `account_status` в `/me`.

### AC/DoD
- [x] (P0) `openapi.yaml` `MeData`: `created_at` (`string|null`, date-time); `account_status` (enum + description «MVP: всегда `active`»).
- [x] (P0) `API_REFERENCE.md §6` — те же поля в примере/таблице `/me`.
- [x] (P1) `rg account_status|created_at` в обоих docs — hits.

### Где менять код
- `doge-identity-service/docs/runtime-docs/api-reference/openapi.yaml`
- `doge-identity-service/docs/runtime-docs/api-reference/API_REFERENCE.md`

### Out of scope
- Реализация `me_response.py` (t01); email docs (ONB-01)

### Проверка
```bash
cd doge-identity-service
rg -n 'account_status|created_at' docs/runtime-docs/api-reference/openapi.yaml docs/runtime-docs/api-reference/API_REFERENCE.md
```
