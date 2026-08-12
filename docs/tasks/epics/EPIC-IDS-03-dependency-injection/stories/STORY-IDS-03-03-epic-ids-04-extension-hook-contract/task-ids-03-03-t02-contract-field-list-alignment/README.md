## Task workspace — `task-ids-03-03-t02-contract-field-list-alignment`

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000004`  
**Decision Ref:** [`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) §3, §6 Story 3  
---

## Task: analyze — ApiDependencies field list vs EPIC-IDS-04 contract

### Цель
Верифицировать, что nine optional полей `ApiDependencies` (Story 1) совпадают с таблицей epic §3 и target block Story 3 — без реализации `provide_service_factory`.

### Факты из кода
1. Epic §3 field table — [`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) L39-53 (`supabase_jwt_validator` … `story_draft_repository`).
2. Story 1 Outputs — [`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) L91-99 (nine `object | None` fields).
3. Story 3 AC — [`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) L188: список полей Story 1 = EPIC-IDS-04 factory getters.

### Gap
Нет явной checklist-верификации alignment после t01 Story 1 + t01 Story 3.

### AC/DoD
- [x] (P0) Список целевых полей в Story 1 совпадает с тем, что EPIC-IDS-04 реализует через `provide_service_factory`.
- [x] (P0) Checklist в story anchor или task note: 9 полей × epic §3 × dataclass × commented block getters — все match.

### Acceptance
- [acceptance-verification-task-ids-03-03-t02-contract-field-list-alignment.md](./acceptance-verification-task-ids-03-03-t02-contract-field-list-alignment.md) — PASS
- [BULLRUN-PHASE-LOG.md](./BULLRUN-PHASE-LOG.md)
- Checklist: [`../STORY-IDS-03-03-epic-ids-04-extension-hook-contract.md`](../STORY-IDS-03-03-epic-ids-04-extension-hook-contract.md) §Field alignment

### Где менять код
- Review-only: [`src/core/api/dependencies.py`](../../../../../../../src/core/api/dependencies.py)
- Update story anchor checklist if gap found: [`../STORY-IDS-03-03-epic-ids-04-extension-hook-contract.md`](../STORY-IDS-03-03-epic-ids-04-extension-hook-contract.md)

### Out of scope
- EPIC-IDS-04 implementation
- Protocol type upgrades (`object | None` → domain contracts)

### Команды проверки
```bash
# Nine optional fields in dataclass (after Story 1 t01)
grep -E 'supabase_jwt_validator|profile_repository|verification_session_store|eid_audit_log_repository|eid_provider_registry|oauth_client_store|oauth_token_service|story_draft_repository' \
  doge-identity-service/src/core/api/dependencies.py
```
