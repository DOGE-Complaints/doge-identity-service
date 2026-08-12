# Security hardening — backlog package

> Context: [EPIC-IDS-SEC.md](EPIC-IDS-SEC.md)

| Order | Story | Status | Depends |
|-------|-------|--------|---------|
| 1 | [STORY-IDS-SEC-01-rate-limiting](STORY-IDS-SEC-01-rate-limiting.md) | Done | — |
| 2 | [STORY-IDS-SEC-01b-phone-request-http-rate-limit](STORY-IDS-SEC-01b-phone-request-http-rate-limit.md) | Done | SEC-01 |
| 3 | [STORY-IDS-SEC-02-audit-ip-ua-hashing](STORY-IDS-SEC-02-audit-ip-ua-hashing.md) | Done | SEC-01 |
| 4 | [STORY-IDS-SEC-03-jwt-validation-hardening](STORY-IDS-SEC-03-jwt-validation-hardening.md) | Done | — |
| 5 | [STORY-IDS-SEC-06-supabase-jwks-es256-hardening](STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md) | Done | SEC-03 |
| 6 | [STORY-IDS-SEC-04-service-role-isolation](STORY-IDS-SEC-04-service-role-isolation.md) | Done | — | pipeline 🟢 · pkg-000043 · rotation operator manual (spa [`rotation-decision-sec01.md`](../../../../../spa-app/docs/tasks/epics/EPIC-SPA-05-security-hardening/stories/STORY-SPA-SEC-01-remove-service-role-from-frontend/task-spa-sec-01-t05-rotation-decision-sec04-sync/rotation-decision-sec01.md)) |
| 7 | [STORY-IDS-SEC-05-auth-credential-model-adr](STORY-IDS-SEC-05-auth-credential-model-adr.md) | Accumulating | — |

**Progress:** 6/7 Done (86%) — SEC-05 ADR decided; BFF implementation in [auth-bff](../auth-bff/INDEX.md)
