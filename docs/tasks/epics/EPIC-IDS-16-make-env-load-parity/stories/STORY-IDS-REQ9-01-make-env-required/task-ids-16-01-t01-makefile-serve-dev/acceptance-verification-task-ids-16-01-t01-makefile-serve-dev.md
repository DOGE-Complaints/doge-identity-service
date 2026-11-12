# Acceptance verification — task-ids-16-01-t01-makefile-serve-dev

- **Gate:** PASS
- **Wave:** pkg-000053
- **Story:** STORY-IDS-REQ9-01-make-env-required
- **Date:** 2026-09-26T12:08:20Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| `serve`/`dev` source without `if [ -f ./.env ]` | PASS | [`Makefile:4-11`](../../../../../../../Makefile) — `set -a && . ./.env && set +a && \` |
| Pattern matches gateway/threads | PASS | Same shell line as gateway/threads; optional `if` only remains on `check-env` (REQ9-02) |
| Fail closed if `.env` absent | PASS | Empty-dir `make serve` → `/bin/sh: ./.env: No such file or directory` · `make: *** [serve] Error 1` |
| `check-env` unchanged | PASS | [`Makefile:14-15`](../../../../../../../Makefile) still `if [ -f ./.env ]` |
| Probes `/health` `/ready` unchanged | PASS | [`asgi_app.py:288`](../../../../../../../src/core/api/asgi_app.py), `:295` |
