## Task workspace — `task-ids-07-02-t05-audit-g3-created-at-semantics-docs`

- Story: [`../STORY-IDS-AUTHCORE-02-me-account-fields.md`](../STORY-IDS-AUTHCORE-02-me-account-fields.md)
- Prerequisite: [`task-ids-07-02-t04-story-acceptance-verification`](../task-ids-07-02-t04-story-acceptance-verification/README.md)
- Audit source: [`../../../../../../analysis/identity-authcore-02-code-audit-2026-07-24.md`](../../../../../../analysis/identity-authcore-02-code-audit-2026-07-24.md) (G3)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_07_authcore_02_audit_2026_07_24`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/identity-authcore-02-code-audit-2026-07-24.md`](../../../../../../analysis/identity-authcore-02-code-audit-2026-07-24.md) §Gaps G3; [`identity-cabinet-me-fields-interview-2026-07-13.md`](../../../../../../../analysis/identity-cabinet-me-fields-interview-2026-07-13.md) D-CAB-2  
---

## Task: docs — `created_at` semantics caveat in api-reference (G3)

### Цель
В consumer-facing описании `MeData.created_at` явно указать: значение = `profiles.created_at` (момент создания профиля / первой верификации), **не** дата регистрации в Supabase Auth. UI-label «Account Created» может быть неточным.

### Почему это важно
Audit G3 LOW: оговорка есть только в interview D-CAB-2; [`openapi.yaml:87`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) и [`API_REFERENCE.md:83`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) описывают источник без семантики.

### Факты из кода
1. [`openapi.yaml:84-87`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) — `created_at` description: `profiles.created_at when profile exists; null when no profile (no Auth lookup)` — без «не дата регистрации».
2. [`API_REFERENCE.md:83`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) — Account fields: ISO from `profiles.created_at` or null — без семантической оговорки.
3. D-CAB-2 — [`identity-cabinet-me-fields-interview-2026-07-13.md`](../../../../../../../analysis/identity-cabinet-me-fields-interview-2026-07-13.md).
4. Runtime emit уже корректен — [`me_response.py:33,48`](../../../../../../../src/core/api/me_response.py) (не трогать в этом таске).

### Gap / Проблема
Потребитель (SPA CAB-02) может трактовать `created_at` как Auth signup date.

### AC/DoD
- [x] (P0) `openapi.yaml` `MeData.created_at` description включает оговорку: профиль / первая верификация, **не** дата регистрации Auth.
- [x] (P0) `API_REFERENCE.md` §6 — та же оговорка рядом с Account fields / `created_at`.
- [x] (P1) `rg` (или grep) по обоим файлам: hits на семантику (`перв` / `верифик` / `регистрац` / `first` / `verification` / `registration` — по фактическому тексту).
- [x] (P1) Не менять код `me_response.py`, тесты, миграции.

### Где менять код
- `doge-identity-service/docs/runtime-docs/api-reference/openapi.yaml`
- `doge-identity-service/docs/runtime-docs/api-reference/API_REFERENCE.md`

### Out of scope
- `me_response.py` / email (ONB-01 = G1)
- Spa CAB-api-requirements (G2)
- Backlog T04 numbering sync (G4 ignored)
- Новый `pkg-*.yaml`, смена `identity-active-package.current.yaml`

### Проверка
```bash
cd doge-identity-service
rg -n 'created_at|верифик|регистрац|verification|registration|first' \
  docs/runtime-docs/api-reference/openapi.yaml \
  docs/runtime-docs/api-reference/API_REFERENCE.md
```
