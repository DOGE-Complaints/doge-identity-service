# Run summary — identity Railway 502 fix (2026-07-07)

> **Wave:** identity railpack startCommand fix  
> **Date:** 2026-07-07T10:45:00Z  
> **Commit:** `76a11bf` on `origin/dev` — `fix(ids-deploy): use system python in railpack startCommand`

## Root cause (verified)

Deploy Logs: `.venv/bin/python: No such file or directory` → crash loop → **502** на всех маршрутах.

## Code fix

[`railpack.json`](../../railpack.json) — как gateway:

```json
{
  "packages": { "python": "3.11" },
  "deploy": {
    "startCommand": "python -m uvicorn --app-dir src core.api.asgi_app:app --host 0.0.0.0 --port ${PORT:-8100}"
  }
}
```

Runbook §3 обновлён: [`run-and-healthcheck.md`](../runbook/run-and-healthcheck.md).

## Local verification (pre-push)

```bash
# uvicorn + .env (demo profile)
curl http://127.0.0.1:8100/health   # 200 ok
curl -w "%{http_code}" /ready       # 200
curl -w "%{http_code}" /me          # 401 (норма)
make smoke IDENTITY_URL=http://127.0.0.1:8100  # 5 passed
```

## Push

```bash
git push origin dev   # e4d6e0c..76a11bf
```

## Live verification (post-push, 2026-07-07T10:45Z)

URL: `https://doge-identity-service-tallinn-demo.up.railway.app`

| Check | Result |
|-------|--------|
| `GET /health` | ❌ **502** (`Application failed to respond`) |
| `make smoke` | 5 skipped (health unreachable) |
| spa `verify:cors:preflight` gateway | ✅ |
| spa `verify:cors:preflight` identity | ❌ 502 |

**Вывод:** кодовый фикс в репо; Railway **ещё не отдаёт 200** — вероятно redeploy не завершён или нужен **Manual Deploy** в dashboard (подтвердить ветку `dev` и новый commit `76a11bf`).

## Railway Variables checklist (operator)

После успешного старта uvicorn сверить **pilot** vars ([`schema.py`](../../src/core/config/schema.py) `pilot_required`):

| Variable | Notes |
|----------|-------|
| `APP_PROFILE` | `pilot` |
| `DB_BACKEND` | `supabase` |
| `API_BASE_URL` | `https://doge-identity-service-tallinn-demo.up.railway.app` |
| `SUPABASE_URL` | реальный Cloud URL |
| `SUPABASE_SERVICE_ROLE` | server-only |
| `DATABASE_URL` | Postgres connection |
| `DOGESTONIA_EID_SECRET` | required |
| `EID_SESSION_ENC_KEY` | required |
| `OAUTH_ACCESS_TOKEN_SECRET` | required |
| `GPT_OAUTH_CLIENT_SECRET` | required |
| `SERVICE_API_TOKEN` | required |
| `SMS_PROVIDER` | `mock` (не `file` на pilot) |
| `CORS_ALLOWED_ORIGINS` | `https://dogestonia-spa-tallinn-demo.up.railway.app` |

См. также [`cors-allowed-origins.md`](../runbook/cors-allowed-origins.md).

## Re-verify after Railway green

```bash
curl -s https://doge-identity-service-tallinn-demo.up.railway.app/health
curl -s -o /dev/null -w "%{http_code}\n" https://doge-identity-service-tallinn-demo.up.railway.app/me   # expect 401

cd doge-identity-service
make smoke IDENTITY_URL=https://doge-identity-service-tallinn-demo.up.railway.app

cd ../spa-app
SPA_ORIGIN=https://dogestonia-spa-tallinn-demo.up.railway.app \
GATEWAY_BASE_URL=https://dogestonia-tallinn.up.railway.app \
IDENTITY_SERVICE_URL=https://doge-identity-service-tallinn-demo.up.railway.app \
  npm run verify:cors:preflight
```

Ожидание: `/health` 200, `/me` 401, CORS preflight identity → 200 + `Access-Control-Allow-Origin` = spa origin.

## SPA AC #4

Закрыть `[x]` в [STORY-SPA-DEPLOY-01](../../../spa-app/docs/tasks/backlog-stories/railway-deploy/STORY-SPA-DEPLOY-01-railway-deployability.md) после green `verify:cors:preflight`.
