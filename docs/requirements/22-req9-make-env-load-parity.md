# 22. REQ9 — make `.env` load parity

Parent: docs/requirements backlog/REQ9-DOGEstonia-Microservices-Ops-Parity-Target.md §3, §8.2, §10.1 G8  
Parent-id: dogestonia-microservices-ops-parity-target  
Siblings:  
- doge-complaints-gateway/docs/requirements/53-req9-ops-parity-env-naming.md (contract: callers use `IDENTITY_BASE_URL` → this service `/me`; no new identity env peer URLs required)  
- doge-threads/docs/requirements/02-req9-ops-peer-token-docs.md (contract: same `IDENTITY_BASE_URL` + user Bearer forward)  
- spa-app/docs/requirements/18-req9-vite-identity-base-url.md (contract: `VITE_IDENTITY_BASE_URL` points at this `API_BASE_URL`/`PORT` origin — naming only)  
Status: Draft — backlog stories materialized ([req9-make-env-load-parity](../tasks/backlog-stories/req9-make-env-load-parity/INDEX.md)); PA.2 optional  
Дата: 2026-09-25  

---

## 1) Goal

Align identity `make serve`/`dev` with required shell-source `.env` policy (gateway/threads majority) per REQ9 G8. Keep inbound `SERVICE_API_TOKEN` and `/health` `/ready`.

## 2) Scope / Out of scope

**In:** Makefile `.env` load policy; document `SERVICE_API_TOKEN` / `API_BASE_URL` / `PORT` unchanged names.

**Out:** renaming `SERVICE_API_TOKEN`; provider env family; product verification flows; spa rename implementation (spa child).

## 3) Verified current state

- identity Makefile optional `if [ -f ./.env ]` — integrity gap G8  
- Probes `/health` `/ready` exist; `SERVICE_API_TOKEN` in `.env.example`

## 4) Target behavior

- `make serve`/`dev` require sourcing `./.env` (fail closed if missing), matching gateway/threads  
- No peer URL renames on this service

## 5) Acceptance criteria

- [ ] G8: `make serve`/`dev` require `.env` shell source  
- [ ] Probes still `/health` `/ready`  
- [ ] `SERVICE_API_TOKEN` inbound name unchanged

## 6) Open questions

None blocking.

## 7) Dependencies

Parent §3 G8, §8.2; sibling gateway `53-…` for `IDENTITY_BASE_URL` documentation on callers.
