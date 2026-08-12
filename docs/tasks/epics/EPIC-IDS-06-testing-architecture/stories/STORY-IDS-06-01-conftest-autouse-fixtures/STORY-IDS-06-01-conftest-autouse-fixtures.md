# STORY-IDS-06-01: `conftest.py` — три обязательные autouse-фикстуры

## Meta
- Key: `STORY-IDS-06-01-conftest-autouse-fixtures`
- Parent Epic: [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md)
- Type: Technical Story (Testing Architecture)
- Status: Done
- Decision Ref: [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 1

## Story Goal
Три autouse-фикстуры в `tests/conftest.py`: `_block_dotenv_leakage`, `_pytest_session_logging`, `pytest_collection_modifyitems` (auto `live_integration` marker).

## AC / DoD (из EPIC-IDS-06 §6 Story 1)
- [x] `pytest tests/ -q` без `.env` файла — все unit-тесты `DB_BACKEND=in_memory`, `EID_PROVIDER=mock`.
- [x] `pytest tests/ -q` с `.env` содержащим `DB_BACKEND=supabase` + реальные creds — тесты используют in_memory (env перезаписан).
- [x] `tests/integration/supabase/*.py` автоматически помечены `live_integration` без явного декоратора.
- [x] `pytest -m "not live_integration" -q` — пропускает все Supabase тесты.
- [x] В тесте, переопределяющем env через свой `monkeypatch.setenv()` ПОСЛЕ autouse — переопределение работает (autouse применяется первым).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-06-01-t01-conftest-autouse-fixtures`](./task-ids-06-01-t01-conftest-autouse-fixtures/README.md) | pkg-000008 |
| 2 | [`task-ids-06-01-t02-story1-acceptance-verification`](./task-ids-06-01-t02-story1-acceptance-verification/README.md) | pkg-000008 |
