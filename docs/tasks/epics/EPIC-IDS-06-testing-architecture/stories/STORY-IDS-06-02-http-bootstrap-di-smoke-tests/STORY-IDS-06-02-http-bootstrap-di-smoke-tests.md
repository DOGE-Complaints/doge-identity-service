# STORY-IDS-06-02: HTTP Transport smoke + Bootstrap smoke + DI smoke

## Meta
- Key: `STORY-IDS-06-02-http-bootstrap-di-smoke-tests`
- Parent Epic: [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md)
- Type: Technical Story (Testing Architecture)
- Status: Done
- Decision Ref: [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 2

## Story Goal
Пять offline test-модулей: bootstrap, HTTP transport (ASGITransport), DI singleton, service factory, eID registry, JWT validator — без сетевых вызовов.

## AC / DoD (из EPIC-IDS-06 §6 Story 2)
- [x] Все 5 файлов smoke + DI + provider + validator проходят PASSED.
- [x] Тесты не делают сетевых вызовов (ASGITransport + in-memory только).
- [x] Общее время offline-сюиты < 30 секунд.

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-06-02-t01-bootstrap-smoke-tests`](./task-ids-06-02-t01-bootstrap-smoke-tests/README.md) | pkg-000008 |
| 2 | [`task-ids-06-02-t02-http-transport-smoke-tests`](./task-ids-06-02-t02-http-transport-smoke-tests/README.md) | pkg-000008 |
| 3 | [`task-ids-06-02-t03-di-singleton-and-service-factory-tests`](./task-ids-06-02-t03-di-singleton-and-service-factory-tests/README.md) | pkg-000008 |
| 4 | [`task-ids-06-02-t04-eid-registry-and-jwt-validator-tests`](./task-ids-06-02-t04-eid-registry-and-jwt-validator-tests/README.md) | pkg-000008 |
| 5 | [`task-ids-06-02-t05-story2-acceptance-verification`](./task-ids-06-02-t05-story2-acceptance-verification/README.md) | pkg-000008 |
