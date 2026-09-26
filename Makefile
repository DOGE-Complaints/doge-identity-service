.PHONY: serve dev check-env test test-live smoke

# Make start + check-env require cwd ./.env (G8 / REQ9-01/02). Names unchanged: PORT, API_BASE_URL, SERVICE_API_TOKEN.
serve:
	set -a && . ./.env && set +a && \
	.venv/bin/python -m uvicorn --app-dir src core.api.asgi_app:app \
	  --host 127.0.0.1 --port $${PORT:-8100}

dev:
	set -a && . ./.env && set +a && \
	.venv/bin/python -m uvicorn --app-dir src core.api.asgi_app:app \
	  --host 127.0.0.1 --port $${PORT:-8100} --reload --reload-dir src

# Diagnostic print — same required shell-source as serve/dev (REQ9-02); not optional.
check-env:
	set -a && . ./.env && set +a && \
	echo "APP_PROFILE          = $${APP_PROFILE:-demo}" && \
	echo "PORT                 = $${PORT:-8100}" && \
	echo "SUPABASE_URL         = $${SUPABASE_URL:-<not set>}" && \
	echo "SUPABASE_JWT_SECRET  = $${SUPABASE_JWT_SECRET:-<not set>}" && \
	echo "AUTHENTIGATE_ISSUER  = $${AUTHENTIGATE_ISSUER:-<not set>}" && \
	echo "EID_PROVIDER         = $${EID_PROVIDER:-mock}"

test:
	.venv/bin/python -m pytest tests/ -q -m "not live_integration"

test-live:
	.venv/bin/python -m pytest tests/ -m live_integration -v

# HTTP smoke against a RUNNING server (default http://localhost:8100).
# Override target: `make smoke IDENTITY_URL=https://<app>.up.railway.app`
smoke:
	@IDENTITY_URL=$${IDENTITY_URL:-http://localhost:8100} \
	  .venv/bin/python -m pytest tests/smoke/ -q
