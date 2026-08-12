# STORY-IDS-04-03: `ServiceFactory(Protocol)` + `DefaultServiceFactory(frozen=True)`

## Meta
- Key: `STORY-IDS-04-03-service-factory-default`
- Parent Epic: [`../../EPIC-IDS-04-soa-service-factory.md`](../../EPIC-IDS-04-soa-service-factory.md)
- Type: Technical Story (SOA Factory)
- Status: Done
- Decision Ref: [`../../EPIC-IDS-04-soa-service-factory.md`](../../EPIC-IDS-04-soa-service-factory.md) §6 Story 3

## Story Goal
Factory — единственный объект связей между сервисами: `ServiceFactory` Protocol + frozen `DefaultServiceFactory` с `get_*()` returning same instances.

## AC / DoD (из EPIC-IDS-04 §6 Story 3)
- [x] `DefaultServiceFactory(...).config` — возвращает переданный `AppConfig`.
- [x] `factory.get_profile_repository() is factory.get_profile_repository()` — True (same instance, factory не плодит копии).
- [x] `factory.something = "x"` → `FrozenInstanceError`.
- [x] `ServiceFactory` — `Protocol`, не базовый класс; `DefaultServiceFactory` его удовлетворяет.

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-04-03-t01-service-factory-protocol-and-default`](./task-ids-04-03-t01-service-factory-protocol-and-default/README.md) | pkg-000005 |
| 2 | [`task-ids-04-03-t02-story3-acceptance-verification`](./task-ids-04-03-t02-story3-acceptance-verification/README.md) | pkg-000005 |
