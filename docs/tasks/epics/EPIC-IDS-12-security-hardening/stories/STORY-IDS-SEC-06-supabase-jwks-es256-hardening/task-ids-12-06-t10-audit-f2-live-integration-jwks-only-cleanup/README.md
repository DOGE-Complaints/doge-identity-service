## Task workspace — `task-ids-12-06-t10-audit-f2-live-integration-jwks-only-cleanup`

- Story: [`../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md)
- Prerequisite: [`task-ids-12-06-t09-audit-f1-jwks-httpx-client-lifespan-close`](../task-ids-12-06-t09-audit-f1-jwks-httpx-client-lifespan-close/README.md)
- Audit source: [`../../../../../../analysis/epic-ids-12-sec-06-audit-2026-07-04.md`](../../../../../../analysis/epic-ids-12-sec-06-audit-2026-07-04.md) (F2)

---
**Приоритет:** P2  
**Сложность:** M  
**Статус:** done  
**Wave:** `override epic_ids_12_sec_06_audit_2026_07_04`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-12-sec-06-audit-2026-07-04.md`](../../../../../../analysis/epic-ids-12-sec-06-audit-2026-07-04.md) §F2  
---

## Task: fix — live integration JWKS-only cleanup (F2)

### Цель
Привести live-integration ветку к JWKS-only: убрать rudiment `SUPABASE_TEST_JWT_SECRET`, починить live sanity test под текущий API валидатора, синхронизировать runbook/CI.

### Почему это важно
Live conftest и sanity test всё ещё требуют JWT secret и вызывают удалённый `jwt_secret=` конструктор — offline-deselected, но сломан при `make test-live` и расходится с SEC-06 as-built.

### Факты из кода
1. Live sanity использует stale API: [`test_supabase_jwt_live_sanity.py:32-36`](../../../../../../../tests/integration/supabase/test_supabase_jwt_live_sanity.py) — `SupabaseJwtValidatorImpl(jwt_secret=..., supabase_url=...)`.
2. Conftest gate: [`integration/supabase/conftest.py:37-55`](../../../../../../../tests/integration/supabase/conftest.py) — требует `SUPABASE_TEST_JWT_SECRET` / `SUPABASE_JWT_SECRET`.
3. Doc test: [`test_supabase_runbook_docs.py:60-67`](../../../../../../../tests/test_supabase_runbook_docs.py) — assert `SUPABASE_TEST_JWT_SECRET` в runbook.
4. CI: [`.github/workflows/integration-live.yml:6,47`](../../../../../../../.github/workflows/integration-live.yml) — мапит `SUPABASE_JWT_SECRET` из `SUPABASE_TEST_JWT_SECRET`.
5. Env/runbook: [`.env.example:33-37`](../../../../../../../.env.example), [`supabase-project-setup.md:165-172`](../../../../../../../docs/runbook/supabase-project-setup.md).
6. Audit F2: [`epic-ids-12-sec-06-audit-2026-07-04.md`](../../../../../../analysis/epic-ids-12-sec-06-audit-2026-07-04.md) §2 F2.

### Gap / Проблема
Live-ветка не соответствует JWKS-only: мёртвый JWT secret в conftest/docs/CI; live sanity не компилируется с текущим `SupabaseJwtValidatorImpl`.

### AC/DoD
- [x] (P0) `integration/supabase/conftest.py` — skip-gate по URL (+ operator token path), без обязательного JWT secret.
- [x] (P0) `test_supabase_jwt_live_sanity.py` — JWKS-only validator (`supabase_url` + real JWKS fetch или documented operator-assisted token).
- [x] (P0) `.env.example`, runbook, `test_supabase_runbook_docs.py` — без обязательного `SUPABASE_TEST_JWT_SECRET` для Cloud auth.
- [x] (P0) `.github/workflows/integration-live.yml` — убрать `SUPABASE_JWT_SECRET` mapping (JWKS via `SUPABASE_URL` only).
- [x] (P0) Offline suite green: `.venv/bin/python -m pytest -q -m "not live_integration"`.
- [x] (P1) Не добавлять HS256 Supabase minters в tests/ (OAuth access-token HS256 — keep).

### Где менять код
- `doge-identity-service/tests/integration/supabase/conftest.py`
- `doge-identity-service/tests/integration/supabase/test_supabase_jwt_live_sanity.py`
- `doge-identity-service/.env.example`
- `doge-identity-service/docs/runbook/supabase-project-setup.md`
- `doge-identity-service/tests/test_supabase_runbook_docs.py`
- `doge-identity-service/.github/workflows/integration-live.yml`

### Out of scope
- EPIC-IDS-06 / EPIC-IDS-05 historical epic markdown (не runtime).
- Mint HS256 Supabase tokens в live tests.
- Runtime validator changes (t09 covers lifecycle only).

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -q -m "not live_integration"
grep -rn 'SUPABASE_TEST_JWT_SECRET' tests/integration/supabase/conftest.py tests/integration/supabase/test_supabase_jwt_live_sanity.py
grep -n 'SUPABASE_JWT_SECRET' .github/workflows/integration-live.yml || true
```
