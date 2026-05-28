.PHONY: serve dev check-env test test-live

serve:
	@if [ -f ./.env ]; then set -a && . ./.env && set +a; fi; \
	.venv/bin/python -m uvicorn --app-dir src core.api.asgi_app:app \
	  --host 127.0.0.1 --port $${PORT:-8100}

dev:
	@if [ -f ./.env ]; then set -a && . ./.env && set +a; fi; \
	.venv/bin/python -m uvicorn --app-dir src core.api.asgi_app:app \
	  --host 127.0.0.1 --port $${PORT:-8100} --reload --reload-dir src

check-env:
	@if [ -f ./.env ]; then set -a && . ./.env && set +a; fi; \
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
