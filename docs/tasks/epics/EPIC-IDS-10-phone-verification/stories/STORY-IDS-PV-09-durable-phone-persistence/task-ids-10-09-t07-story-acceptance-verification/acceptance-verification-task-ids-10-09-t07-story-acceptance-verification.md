# Story acceptance gate — STORY-IDS-PV-09-durable-phone-persistence

- **Story:** STORY-IDS-PV-09 — Durable Supabase phone-персистентность (sessions + audit + bootstrap parity)
- **Package:** `pkg-000039-20260626-epic-ids-10-pv-09-durable-phone-persistence.yaml`
- **Result:** PASS
- **Date:** 2026-06-26

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| При `DB_BACKEND=supabase` pending OTP-сессия переживает пересоздание стора; expired/consumed корректны | PASS | `SupabasePhoneVerificationSessionStore`; `test_durability_phone_session_survives_store_recreate`, mark_consumed/expired tests |
| При `DB_BACKEND=supabase` phone-аудит переживает пересоздание репо | PASS | `SupabasePhoneAuditLogRepository`; `test_durability_phone_audit_survives_repo_recreate` |
| Protocol parity `PhoneVerificationSessionStore` / `PhoneAuditLogRepository` | PASS | 10 session ops + log/list in `db_supabase.py`; mirrors `InMemory*` |
| DI: supabase → Supabase*; in_memory → InMemory*; offline tests green | PASS | `providers.py:121+`; `test_epic_ids_05_integration.py` phone store assertions |
| Migration `phone_audit_events` + `phone_verification_sessions` + migration test | PASS | `20260626000001_phone_persistence_tables.sql`; `test_supabase_migrations_sql.py` |
| Bootstrap parity `000_full_init.sql` | PASS | blocks [5/8]–[8/8] fold phone profile, OAuth, phone persistence |
| Аудит IP/UA не вводится (SEC-02 boundary) | PASS | storage-only columns; no new hashing; existing SEC-02 tests unchanged |

## Commands (live verification 2026-06-26)

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
# 386 passed
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
# ok 7 paths · ok date-check
```
