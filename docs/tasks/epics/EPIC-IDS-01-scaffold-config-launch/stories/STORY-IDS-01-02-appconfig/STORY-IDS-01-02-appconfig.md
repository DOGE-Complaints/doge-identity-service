# STORY-IDS-01-02: AppConfig — immutable identity-конфигурация

## Meta
- Key: `STORY-IDS-01-02-appconfig`
- Parent Epic: [`../../../EPIC-IDS-01-scaffold-config-launch.md`](../../../EPIC-IDS-01-scaffold-config-launch.md)
- Type: Technical Story (NFR / Infrastructure)
- Status: Implemented (Waiting Acceptance)
- Depends on: STORY-IDS-01-01
- Decision Ref: [`../../../../../requirements/07-env-configuration-spec.md`](../../../../../requirements/07-env-configuration-spec.md); [`../../../../../requirements/17-eid-provider-abstraction.md`](../../../../../requirements/17-eid-provider-abstraction.md); [`../../../../../requirements/18-eideasy-provider.md`](../../../../../requirements/18-eideasy-provider.md); [`../../../../../analysis/interview-cpo-cto-epics-2026-05-27.md`](../../../../../analysis/interview-cpo-cto-epics-2026-05-27.md) §4.2, 4.4, 4.5
- Operative queue: [`../../../../identity-active-packages/pkg-000001-20260527-epic-ids-01-scaffold.yaml`](../../../../identity-active-packages/pkg-000001-20260527-epic-ids-01-scaffold.yaml)

## Story Goal
Реализовать frozen `AppConfig` + `load_config_from_env` с identity field-set, fail-fast в `pilot`, без `cluster_*`.

## Product decisions (fixed)
- Единственное имя секрета: `DOGESTONIA_EID_SECRET` → `eid_secret` (без fallback / `EID_HASH_SECRET`)
- Первая валидация: `db_backend ∈ {in_memory, supabase}` (`sqlite` → `ConfigError`)
- Два таймаута: `request_timeout_s=15`, `oidc_request_timeout_s=10`
- `port` default `8100`

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-ids-01-02-t01-config-schema`](./task-ids-01-02-t01-config-schema/README.md) | pkg-000001 |
| 2 | [`task-ids-01-02-t02-config-package-exports`](./task-ids-01-02-t02-config-package-exports/README.md) | pkg-000001 |
| 3 | [`task-ids-01-02-t03-config-schema-tests`](./task-ids-01-02-t03-config-schema-tests/README.md) | pkg-000001 |
| 4 | [`task-ids-01-02-t04-audit-f2-1-pilot-api-base-url-fail-fast`](./task-ids-01-02-t04-audit-f2-1-pilot-api-base-url-fail-fast/README.md) | override epic_ids_01_audit_2026_05_28 |
| 5 | [`task-ids-01-02-t05-audit-f2-2-db-enabled-test-coverage`](./task-ids-01-02-t05-audit-f2-2-db-enabled-test-coverage/README.md) | override epic_ids_01_audit_2026_05_28 |
| 6 | [`task-ids-01-02-t06-audit-f2-3-pilot-oauth-secret-isolated-test`](./task-ids-01-02-t06-audit-f2-3-pilot-oauth-secret-isolated-test/README.md) | override epic_ids_01_audit_2026_05_28 |
| 7 | [`task-ids-01-02-t07-audit-f2-4-eideasy-methods-default-order-alignment`](./task-ids-01-02-t07-audit-f2-4-eideasy-methods-default-order-alignment/README.md) | override epic_ids_01_audit_2026_05_28 |

## AC / DoD (story level)
- [x] Demo config из env mapping без ошибок; defaults таймаутов 15/10
- [x] `supabase` без `SUPABASE_*` → `ConfigError`
- [x] `sqlite` backend → `ConfigError`
- [x] `pilot` без секретов / пустой `DOGESTONIA_EID_SECRET` → `ConfigError`
- [x] `eid_provider` validation (`mock`, `eideasy`, `authentigate`)
- [x] `AppConfig` frozen (`FrozenInstanceError` на mutation)
