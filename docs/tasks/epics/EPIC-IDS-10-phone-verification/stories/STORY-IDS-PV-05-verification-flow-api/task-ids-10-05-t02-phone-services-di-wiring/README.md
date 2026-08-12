## Task workspace — `task-ids-10-05-t02-phone-services-di-wiring`

- Story: [`../STORY-IDS-PV-05-verification-flow-api.md`](../STORY-IDS-PV-05-verification-flow-api.md)
- Prerequisite: t01 PhoneAuditLogRepository; PV-01 SmsSenderRegistry

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** todo  
**Wave:** `pkg-000026`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md) Scope bullet 5 (роуты+DI); [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §6  
---

## Task: implement — wire phone services into DI and service factory

### Цель
Expose `SmsSenderRegistry`, `PhoneVerificationSessionStore`, `PhoneAuditLogRepository` via `ApiDependencies` — Story Scope §роуты+DI.

### Почему это важно
Handlers t03/t04 need registry + session store + audit from `deps`; currently only eID services wired ([`providers.py`](../../../../../../../src/core/infrastructure/providers.py), [`dependencies.py`](../../../../../../../src/core/api/dependencies.py)).

### Факты из кода
1. `build_sms_registry` exists: [`registry_builder.py`](../../../../../../../src/core/phone/registry_builder.py) — **not called** from `provide_service_factory`.
2. `InMemoryPhoneVerificationSessionStore`: [`repositories.py:282`](../../../../../../../src/core/infrastructure/repositories.py) — not in DI.
3. `ApiDependencies` optional fields: [`dependencies.py:41-48`](../../../../../../../src/core/api/dependencies.py) — no phone slots.
4. `DefaultServiceFactory`: [`service_factory.py`](../../../../../../../src/core/infrastructure/service_factory.py) — eID registry only.
5. `build_api_dependencies` maps factory → deps: [`dependencies.py:54+`](../../../../../../../src/core/api/dependencies.py).

### Gap / Проблема
Phone HTTP flow cannot access SMS registry or session store through existing DI container.

### AC/DoD
- [ ] (P0) `ApiDependencies`: `sms_sender_registry`, `phone_verification_session_store`, `phone_audit_log_repository` (optional `| None` like eID slots).
- [ ] (P0) `DefaultServiceFactory` + getters for three phone services.
- [ ] (P0) `provide_service_factory`: build `SmsSenderRegistry` via `build_sms_registry(build_sms_provider_runtime(...))` (follow PV-01 pattern); instantiate in-memory phone session + audit repos for both `in_memory` and `supabase` backends (session store in-memory per story scope).
- [ ] (P0) `build_api_dependencies` populates new fields from factory.
- [ ] (P1) Update `EPIC_IDS_04_OPTIONAL_FIELDS` if project convention requires.

### Где менять код
- `doge-identity-service/src/core/api/dependencies.py`
- `doge-identity-service/src/core/infrastructure/service_factory.py`
- `doge-identity-service/src/core/infrastructure/providers.py`

### Out of scope
- HTTP routes — t05
- Handler logic — t03, t04
- Supabase phone session persistence

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "
from core.api.asgi_app import get_api_dependencies
d = get_api_dependencies()
assert d.sms_sender_registry is not None
assert d.phone_verification_session_store is not None
assert d.phone_audit_log_repository is not None
print('ok')
"
```
