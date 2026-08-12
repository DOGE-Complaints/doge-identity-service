# Acceptance verification — task-ids-08-02-t08-audit-f1-return-url-validator-enforcement

- **Branch:** A (enforce at handler boundary)
- **Audit:** F1 ([`epic-ids-08-cleanup-02-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-08-cleanup-02-audit-2026-06-05.md))

## Evidence

- `src/core/api/handlers.py` — `validate_return_url` + `parse_allowed_return_urls(deps.config.allowed_return_urls)` before 501 stub
- `src/core/api/asgi_app.py` — `_return_url_from_request` passes JSON `return_url` to handler
- `tests/test_asgi_transport.py::test_auth_eid_start_rejects_foreign_return_url` — 400 `invalid_return_url`
- `tests/test_asgi_transport.py::test_auth_eid_start_allows_listed_return_url_before_stub` — allowlisted URL reaches 501 stub

## AC/DoD

| Criterion | Result |
|-----------|--------|
| Branch A: runtime enforcement | PASS |
| Branch A: integration/route test | PASS |
| Offline pytest | PASS (206 passed) |
