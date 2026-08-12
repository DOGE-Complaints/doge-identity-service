# STORY-IDS-03-01: ApiDependencies dataclass + HandlerDependencies alias

## Meta
- Key: `STORY-IDS-03-01-api-dependencies-dataclass-handler-alias`
- Parent Epic: [`../../../EPIC-IDS-03-dependency-injection.md`](../../../EPIC-IDS-03-dependency-injection.md)
- Type: Technical Story (DI Container)
- Status: Done
- Decision Ref: [`../../../EPIC-IDS-03-dependency-injection.md`](../../../EPIC-IDS-03-dependency-injection.md) §6 Story 1

## Story Goal
Зафиксировать frozen `ApiDependencies` dataclass с identity-слотами (Optional, `None` в EPIC-IDS-03) и алиас `HandlerDependencies = ApiDependencies`.

## AC / DoD (из EPIC-IDS-03)
- [x] `from core.api.dependencies import ApiDependencies, HandlerDependencies`.
- [x] `HandlerDependencies is ApiDependencies` — True.
- [x] `ApiDependencies(config=..., bearer_token_auth=..., db_backend="in_memory", db_ready=True)` — конструируется; все identity-сервисы дефолтятся в `None`.
- [x] Попытка `deps.config = new_config` → `FrozenInstanceError`.

## Story gate
- [story-acceptance-gate-STORY-IDS-03-01.md](./story-acceptance-gate-STORY-IDS-03-01.md) — **PASS** (2026-05-29)

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-03-01-t01-api-dependencies-dataclass-handler-alias`](./task-ids-03-01-t01-api-dependencies-dataclass-handler-alias/README.md) | pkg-000004 |
| 2 | [`task-ids-03-01-t02-api-dependencies-dataclass-verification`](./task-ids-03-01-t02-api-dependencies-dataclass-verification/README.md) | pkg-000004 |
