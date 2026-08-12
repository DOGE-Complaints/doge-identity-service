# Acceptance verification — task-ids-09-01-t02-asgi-eid-start-wire-body

- **Gate:** PASS · **Wave:** pkg-000015

| Criterion | Result | Evidence |
|-----------|--------|----------|
| JSON body fields wired | PASS | `asgi_app.py:191-204` |
| 200 on valid start | PASS | `test_auth_eid_start_allows_listed_return_url` |
