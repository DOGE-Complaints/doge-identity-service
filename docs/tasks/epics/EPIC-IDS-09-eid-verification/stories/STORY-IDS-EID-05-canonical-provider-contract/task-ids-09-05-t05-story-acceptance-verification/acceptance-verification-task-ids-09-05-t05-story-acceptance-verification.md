# Acceptance verification — task-ids-09-05-t05-story-acceptance-verification

- **Gate:** PASS (2026-06-09)
- **Wave:** pkg-000018
- **Story:** STORY-IDS-EID-05-canonical-provider-contract

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| Есть `EidErrorCode`; `EIDProviderError` несёт канонический код | PASS | t01 — `base.py`, `__init__.py` |
| Оркестратор различает `EIDProviderError` / `Exception`; `user_cancel` в audit | PASS | t02/t04 — `handlers.py`, contract tests |
| `subject_hash` без имени провайдера; правило задокументировано; dedup test | PASS | t03/t04 — `06-eid-providers.md`, mock, unit test |
| Добавление провайдера не добавляет кодов ошибок в ядро | PASS | fixed `EidErrorCode` enum; vendor maps in adapter (EID-02) |
| Offline green; тесты на маппинг ошибок и dedup | PASS | 225 pytest |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
# 225 passed; ok 5 paths (pkg-000018)
```
