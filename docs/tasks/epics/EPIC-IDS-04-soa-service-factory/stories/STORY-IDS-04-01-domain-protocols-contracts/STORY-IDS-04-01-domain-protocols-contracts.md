# STORY-IDS-04-01: Domain Protocols в `core/domain/contracts.py`

## Meta
- Key: `STORY-IDS-04-01-domain-protocols-contracts`
- Parent Epic: [`../../EPIC-IDS-04-soa-service-factory.md`](../../EPIC-IDS-04-soa-service-factory.md)
- Type: Technical Story (SOA Domain)
- Status: Done
- Decision Ref: [`../../EPIC-IDS-04-soa-service-factory.md`](../../EPIC-IDS-04-soa-service-factory.md) §6 Story 1

## Story Goal
Единственный источник истины об интерфейсах репозиториев: `@runtime_checkable` Protocols в `core/domain/contracts.py` и frozen dataclasses в `core/domain/models.py`.

## AC / DoD (из EPIC-IDS-04 §6 Story 1)
- [x] `from core.domain.contracts import ProfileRepository, VerificationSessionStore, ...` — без ошибок.
- [x] Все Protocols имеют `@runtime_checkable`.
- [x] `from core.domain.models import ProfileRecord, VerificationSession, EIDAuditEvent` — без ошибок.
- [x] Domain-слой (`core/domain/*`) не импортирует ничего из `core.infrastructure.*`, `httpx`, `fastapi`, `joserfc`.

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-04-01-t01-domain-contracts-protocols`](./task-ids-04-01-t01-domain-contracts-protocols/README.md) | pkg-000005 |
| 2 | [`task-ids-04-01-t02-domain-models-dataclasses`](./task-ids-04-01-t02-domain-models-dataclasses/README.md) | pkg-000005 |
| 3 | [`task-ids-04-01-t03-story1-acceptance-verification`](./task-ids-04-01-t03-story1-acceptance-verification/README.md) | pkg-000005 |
