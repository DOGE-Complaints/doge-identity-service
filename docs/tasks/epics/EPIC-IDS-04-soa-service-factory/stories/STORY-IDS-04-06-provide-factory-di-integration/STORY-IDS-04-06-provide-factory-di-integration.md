# STORY-IDS-04-06: `provide_service_factory()` — backend selection + интеграция в `build_api_dependencies`

## Meta
- Key: `STORY-IDS-04-06-provide-factory-di-integration`
- Parent Epic: [`../../EPIC-IDS-04-soa-service-factory.md`](../../EPIC-IDS-04-soa-service-factory.md)
- Type: Technical Story (SOA Wiring)
- Status: Done
- Decision Ref: [`../../EPIC-IDS-04-soa-service-factory.md`](../../EPIC-IDS-04-soa-service-factory.md) §6 Story 6

## Story Goal
Единственная точка выбора backend по `DB_BACKEND`; интеграция factory в `build_api_dependencies()` без изменений singleton hook в `asgi_app.py`.

## AC / DoD (из EPIC-IDS-04 §6 Story 6)
- [x] `provide_service_factory()` при `DB_BACKEND=in_memory` возвращает `DefaultServiceFactory` с InMemory-репозиториями.
- [x] `provide_service_factory(config_with_supabase)` — fallback на InMemory + warning (до EPIC-IDS-05), не падает.
- [x] `build_api_dependencies().profile_repository is not None` (после EPIC-IDS-04 уже не `None`).
- [x] `build_api_dependencies().eid_provider_registry.get("mock").provider_name == "mock"`.
- [x] `build_api_dependencies().bearer_token_auth.__class__.__name__ == "SupabaseJwtBearerTokenAuth"`.

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-04-06-t01-provide-service-factory`](./task-ids-04-06-t01-provide-service-factory/README.md) | pkg-000005 |
| 2 | [`task-ids-04-06-t02-build-api-dependencies-integration`](./task-ids-04-06-t02-build-api-dependencies-integration/README.md) | pkg-000005 |
| 3 | [`task-ids-04-06-t03-story6-epic-integration-verification`](./task-ids-04-06-t03-story6-epic-integration-verification/README.md) | pkg-000005 |
