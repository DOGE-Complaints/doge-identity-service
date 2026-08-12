# STORY-IDS-02-02: Logging setup

## Meta
- Key: `STORY-IDS-02-02-logging-setup`
- Parent Epic: [`../../../EPIC-IDS-02-fastapi-transport.md`](../../../EPIC-IDS-02-fastapi-transport.md)
- Type: Technical Story (Observability)
- Status: Done
- Decision Ref: [`../../../../requirements/16-security-privacy-observability.md`](../../../../requirements/16-security-privacy-observability.md)

## Story Goal
Сделать минимальный logging setup для runtime/pytest сценариев: конфиг уровня/формата и helper runtime-exception логирования.

## AC / DoD (из EPIC-IDS-02)
- [x] `configure_logging("DEBUG")` выставляет root logger level DEBUG
- [x] `configure_logging("INFO", log_format="json")` выполняется без исключений
- [x] `log_runtime_exception(..., trace_id="abc", path="/me")` логирует через `core.runtime` без исключений

## Story gate
- [story-acceptance-gate-STORY-IDS-02-02.md](./story-acceptance-gate-STORY-IDS-02-02.md) — **PASS** (2026-05-29)

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-02-02-t01-configure-logging-runtime`](./task-ids-02-02-t01-configure-logging-runtime/README.md) | pkg-000003 |
| 2 | [`task-ids-02-02-t02-logging-verification`](./task-ids-02-02-t02-logging-verification/README.md) | pkg-000003 |
