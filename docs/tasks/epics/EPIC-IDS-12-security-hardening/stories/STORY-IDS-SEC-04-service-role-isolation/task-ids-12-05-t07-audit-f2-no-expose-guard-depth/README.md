## Task workspace — `task-ids-12-05-t07-audit-f2-no-expose-guard-depth`

- Story: [`../STORY-IDS-SEC-04-service-role-isolation.md`](../STORY-IDS-SEC-04-service-role-isolation.md)
- Prerequisite: [`task-ids-12-05-t02-no-expose-service-role-guard-tests`](../task-ids-12-05-t02-no-expose-service-role-guard-tests/README.md)
- Audit source: [`../../../../../../analysis/epic-ids-12-sec-04-audit-2026-07-09.md`](../../../../../../analysis/epic-ids-12-sec-04-audit-2026-07-09.md) (F2)

---
**Приоритет:** P2  
**Сложность:** M  
**Статус:** done  
**Wave:** `override epic_ids_12_sec_04_audit_2026_07_09`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-12-sec-04-audit-2026-07-09.md`](../../../../../../analysis/epic-ids-12-sec-04-audit-2026-07-09.md) §3 F2  
---

## Task: tests — deepen no-expose guard (500, ConfigError, caplog)

### Цель
Закрыть F2 test-coverage gap: расширить guard beyond `/health`, `/ready`, `/me` 401 — покрыть error paths и runtime logs.

### Почему это важно
Baseline [`test_service_role_no_expose.py`](../../../../../../../tests/test_service_role_no_expose.py) (4 tests) не покрывает middleware 500 ([`asgi_app.py:267-283`](../../../../../../../src/core/api/asgi_app.py)), `ConfigError` handler ([`asgi_app.py:258-262`](../../../../../../../src/core/api/asgi_app.py)), caplog; audit F2 MEDIUM.

### Факты из кода
1. Current tests — [`test_service_role_no_expose.py`](../../../../../../../tests/test_service_role_no_expose.py): health/ready/me + static grep.
2. 500 handler — [`asgi_app.py:267-283`](../../../../../../../src/core/api/asgi_app.py): generic `INTERNAL_ERROR` envelope.
3. ConfigError — [`asgi_app.py:258-262`](../../../../../../../src/core/api/asgi_app.py): `str(exc)` in body (must not contain sentinel key value).
4. PostgREST logger — [`db_supabase.py:281-287`](../../../../../../../src/core/infrastructure/db_supabase.py): logs response body snippet (optional stretch — mock only).
5. Patterns — [`test_asgi_transport.py`](../../../../../../../tests/test_asgi_transport.py).

### Gap / Проблема
No-expose guard shallow; t02 marked 🟡 Partial in bullrun after audit.

### AC/DoD
- [x] (P0) Extend `tests/test_service_role_no_expose.py`: sentinel `SUPABASE_SERVICE_ROLE` not in 500 `INTERNAL_ERROR` response body.
- [x] (P0) Test `ConfigError` path (or equivalent config failure route) — response body excludes sentinel value.
- [x] (P1) caplog assertion: no sentinel in error logs on triggered failure path.
- [x] (P0) `.venv/bin/python -m pytest tests/test_service_role_no_expose.py -q` green.
- [x] (P1) Full offline suite: `.venv/bin/python -m pytest -q -m "not live_integration"` green.
- [x] (P1) Bullrun: t02 status → 🟢 after F2 closed.

### Где менять код
- `doge-identity-service/tests/test_service_role_no_expose.py`

### Out of scope
- Live PostgREST integration for `db_supabase.py:281-287` (optional stretch)
- Doc wording (t06)
- F3 ops run-summary
- Новый `pkg-*.yaml`, смена `identity-active-package.current.yaml`

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_service_role_no_expose.py -q
.venv/bin/python -m pytest -q -m "not live_integration"
grep -rn 'log\|print\|debug' src/ | grep -i service_role && exit 1 || true
```
