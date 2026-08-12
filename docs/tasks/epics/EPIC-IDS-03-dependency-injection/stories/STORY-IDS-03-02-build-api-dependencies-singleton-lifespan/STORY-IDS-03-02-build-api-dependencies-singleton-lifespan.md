# STORY-IDS-03-02: build_api_dependencies + singleton + lifespan integration

## Meta
- Key: `STORY-IDS-03-02-build-api-dependencies-singleton-lifespan`
- Parent Epic: [`../../../EPIC-IDS-03-dependency-injection.md`](../../../EPIC-IDS-03-dependency-injection.md)
- Type: Technical Story (DI Container)
- Status: Done
- Decision Ref: [`../../../EPIC-IDS-03-dependency-injection.md`](../../../EPIC-IDS-03-dependency-injection.md) §6 Story 2

## Story Goal
Реализовать `build_api_dependencies()` factory, per-process singleton через `@lru_cache`, интеграцию в `asgi_app.py` и warmup в lifespan.

## AC / DoD (из EPIC-IDS-03)
- [x] `get_api_dependencies() is get_api_dependencies()` — True.
- [x] После `_clear_api_dependencies_cache()` следующий вызов создаёт новый объект (другое `id()`).
- [x] `monkeypatch.setenv("LOG_LEVEL", "DEBUG"); _clear_api_dependencies_cache(); get_api_dependencies().config.log_level == "DEBUG"`.
- [x] При startup сервера лог содержит запись `configure_logging` уровня deps.config.log_level (см. lifespan).
- [x] Два параллельных HTTP запроса получают один и тот же `ApiDependencies` (verifiable через `id()` логирование).

## Story gate
- [story-acceptance-gate-STORY-IDS-03-02.md](./story-acceptance-gate-STORY-IDS-03-02.md) — **PASS** (2026-05-29)

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-03-02-t01-build-api-dependencies-factory`](./task-ids-03-02-t01-build-api-dependencies-factory/README.md) | pkg-000004 |
| 2 | [`task-ids-03-02-t02-asgi-singleton-lifespan-integration`](./task-ids-03-02-t02-asgi-singleton-lifespan-integration/README.md) | pkg-000004 |
| 3 | [`task-ids-03-02-t03-singleton-behavior-verification`](./task-ids-03-02-t03-singleton-behavior-verification/README.md) | pkg-000004 |
| 4 | [`task-ids-03-02-t04-audit-di-1-lifespan-logging-assertion`](./task-ids-03-02-t04-audit-di-1-lifespan-logging-assertion/README.md) | override epic_ids_03_audit_2026_05_28 |
| 5 | [`task-ids-03-02-t05-audit-di-2-create-app-dual-config-note`](./task-ids-03-02-t05-audit-di-2-create-app-dual-config-note/README.md) | override epic_ids_03_audit_2026_05_28 |

## Open audit gaps (post-audit 2026-05-28)

| Finding | Gap task | Status |
|---------|----------|--------|
| DI-1 [MEDIUM] | [t04 lifespan logging assertion](./task-ids-03-02-t04-audit-di-1-lifespan-logging-assertion/README.md) | done |
| DI-2 [MEDIUM] | [t05 create_app dual-config note](./task-ids-03-02-t05-audit-di-2-create-app-dual-config-note/README.md) | done |
