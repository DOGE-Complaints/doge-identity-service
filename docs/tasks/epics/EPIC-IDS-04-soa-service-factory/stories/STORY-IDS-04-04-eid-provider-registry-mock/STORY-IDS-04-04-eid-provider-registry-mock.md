# STORY-IDS-04-04: eID Provider Port + Registry + Mock Provider

## Meta
- Key: `STORY-IDS-04-04-eid-provider-registry-mock`
- Parent Epic: [`../../EPIC-IDS-04-soa-service-factory.md`](../../EPIC-IDS-04-soa-service-factory.md)
- Type: Technical Story (eID Plugin)
- Status: Done
- Decision Ref: [`../../EPIC-IDS-04-soa-service-factory.md`](../../EPIC-IDS-04-soa-service-factory.md) §6 Story 4

## Story Goal
Plugin-архитектура eID: `EIDProviderPort`, `EIDProviderRegistry`, `MockEIDProvider` для локальной работы без credentials.

## AC / DoD (из EPIC-IDS-04 §6 Story 4)
- [x] `isinstance(MockEIDProvider(...), EIDProviderPort)` — True.
- [x] `EIDProviderRegistry({"mock": MockEIDProvider(...)}).get("mock").provider_name == "mock"`.
- [x] `EIDProviderRegistry({}).get_active(config_with_eid_provider_eideasy)` → `KeyError` (решение: KeyError).
- [x] При `config.eid_provider == "mock"` flow проходит без EIDEASY_*/AUTHENTIGATE_* (req-17 acceptance).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-04-04-t01-eid-provider-port-base`](./task-ids-04-04-t01-eid-provider-port-base/README.md) | pkg-000005 |
| 2 | [`task-ids-04-04-t02-eid-registry-and-mock-provider`](./task-ids-04-04-t02-eid-registry-and-mock-provider/README.md) | pkg-000005 |
| 3 | [`task-ids-04-04-t03-story4-acceptance-verification`](./task-ids-04-04-t03-story4-acceptance-verification/README.md) | pkg-000005 |
