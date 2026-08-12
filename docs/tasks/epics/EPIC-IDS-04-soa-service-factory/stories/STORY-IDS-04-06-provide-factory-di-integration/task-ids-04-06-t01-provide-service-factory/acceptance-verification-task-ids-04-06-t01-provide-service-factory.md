# Acceptance verification — task-ids-04-06-t01-provide-service-factory

- **Gate:** PASS (2026-05-30)
- **Wave:** pkg-000005
- **Evidence:** `src/core/infrastructure/providers.py` — `provide_service_factory()` builds InMemory repos, OAuth token service, `SupabaseJwtValidatorImpl` + `SupabaseJwtBearerTokenAuth`, mock `EIDProviderRegistry`; supabase branch falls back with warning; unsupported backend → `ValueError`
