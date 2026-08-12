# STORY-IDS-04-02: InMemory реализации

## Meta
- Key: `STORY-IDS-04-02-inmemory-repositories`
- Parent Epic: [`../../EPIC-IDS-04-soa-service-factory.md`](../../EPIC-IDS-04-soa-service-factory.md)
- Type: Technical Story (SOA Infrastructure)
- Status: Done
- Decision Ref: [`../../EPIC-IDS-04-soa-service-factory.md`](../../EPIC-IDS-04-soa-service-factory.md) §6 Story 2

## Story Goal
InMemory-реализации всех Protocols для unit/service/HTTP-тестов без Supabase; verify `hash_secret` contract перед OAuth store.

## AC / DoD (из EPIC-IDS-04 §6 Story 2)
- [x] `isinstance(InMemoryProfileRepository(), ProfileRepository)` — True (runtime Protocol check).
- [x] `InMemoryProfileRepository().attach_eid_verification(user_id="u1", ..., verified_person_hash="h")` + повторный вызов с тем же `hash` для другого `user_id` → RuntimeError (имитация unique index).
- [x] `InMemoryVerificationSessionStore().get_by_state("unknown")` → `None`.
- [x] `from core.security.hashing import hash_secret` — импортируется без ошибок; unit-тест на детерминизм (опционально, одна строка).
- [x] Все InMemory классы зависят только от stdlib + `core.security.hashing` (нет httpx, joserfc, fastapi импортов).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-04-02-t01-hash-secret-contract-verify`](./task-ids-04-02-t01-hash-secret-contract-verify/README.md) | pkg-000005 |
| 2 | [`task-ids-04-02-t02-inmemory-repositories`](./task-ids-04-02-t02-inmemory-repositories/README.md) | pkg-000005 |
| 3 | [`task-ids-04-02-t03-story2-acceptance-verification`](./task-ids-04-02-t03-story2-acceptance-verification/README.md) | pkg-000005 |
