# Индекс backlog-стори identity (2026-09-25)

> **SSOT per package:** [`*/INDEX.md`](./) tables + [bullrun-launch-index](../bullrun-launch-index.md)  
> **Audit:** [backlog-status-audit-2026-07-09.md](../../analysis/backlog-status-audit-2026-07-09.md) · **Dashboard:** [identity-mvp-dashboard.md](../identity-mvp-dashboard.md)

## Карта пакетов

| Пакет | INDEX | Stories (product) | Progress |
|-------|-------|-------------------|----------|
| Auth-core | [auth-core/INDEX.md](auth-core/INDEX.md) | 2 | 100% |
| OAuth | [oauth/INDEX.md](oauth/INDEX.md) | 4 | 100% |
| eID platform | [eid/INDEX.md](eid/INDEX.md) | 7 | 100% |
| Phone verification | [phone-verification/INDEX.md](phone-verification/INDEX.md) | 9 | 100% |
| SMSPM SMS | [smspm/INDEX.md](smspm/INDEX.md) | 4 | 75% |
| Threads verification boolean | [threads-verification-boolean/INDEX.md](threads-verification-boolean/INDEX.md) | 3 | 100% |
| REQ9 make `.env` load | [req9-make-env-load-parity/INDEX.md](req9-make-env-load-parity/INDEX.md) | 2 | 100% |
| Cleanup | [cleanup/INDEX.md](cleanup/INDEX.md) | 4 | 75% |
| Security hardening | [security-hardening/INDEX.md](security-hardening/INDEX.md) | 7 | 86% (SEC-05 Deferred) |
| Identity onboarding | [identity-onboarding/INDEX.md](identity-onboarding/INDEX.md) | 1 | 100% |
| eID deferred | [eid-deferred/INDEX.md](eid-deferred/INDEX.md) | 6 | POST-MVP |
| Auth-BFF | [auth-bff/INDEX.md](auth-bff/INDEX.md) | 3 | POST-MVP |

**Context (narrative):** каждый пакет также имеет `EPIC-IDS-*.md` или `README.md` — см. ссылку «Context» в package INDEX.

## Открытые product stories (identity-backend)

| Story | Пакет | Блокер / evidence |
|-------|-------|-------------------|
| [ONB-01](identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md) | onboarding | 🟢 Done pkg-000045 — `email`/`email_verified` in [`me_response.py`](../../src/core/api/me_response.py); [pipeline](../epics/EPIC-IDS-13-onboarding/stories/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md) |
| [CLEANUP-04](cleanup/STORY-IDS-CLEANUP-04-spec-reconciliation.md) | cleanup | gateway-copy specs в [`06-technical-scaffold.md`](../../requirements/06-technical-scaffold.md) |
| [SMSPM-01](smspm/STORY-IDS-SMSPM-01-provider-config-registry.md) | smspm | 🟢 Done pkg-000046 — [pipeline](../epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-01-provider-config-registry/STORY-IDS-SMSPM-01-provider-config-registry.md); `SMS_PROVIDER=smspm` registered |
| [SMSPM-02](smspm/STORY-IDS-SMSPM-02-sms-sender.md) | smspm | 🟢 Done pkg-000047 — [pipeline](../epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-02-sms-sender/STORY-IDS-SMSPM-02-sms-sender.md); `SmspmSmsSender` POST |
| [SMSPM-03](smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md) | smspm | ⚪ Todo pkg-000048 — [pipeline](../epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-03-operator-runbook-smoke/STORY-IDS-SMSPM-03-operator-runbook-smoke.md); t01–t03 🟢; t04 BLOCKED (SPIKE + `SMSPM_*`) |
| [SMSPM-04](smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md) | smspm | 🟢 Done pkg-000049 — [pipeline](../epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-04-delivery-report-webhook/STORY-IDS-SMSPM-04-delivery-report-webhook.md); GET delivery webhook; confirm ungated |
| [VB-01](threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md) | threads-verification-boolean | 🟢 Done pkg-000050 — [pipeline](../epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-01-persist-identity-verified/STORY-IDS-VB-01-persist-identity-verified.md); persist `identity_verified` + backfill |
| [VB-02](threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md) | threads-verification-boolean | 🟢 Done pkg-000051 — [pipeline](../epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-02-me-expose-identity-verified/STORY-IDS-VB-02-me-expose-identity-verified.md); expose on `GET /me` |
| [VB-03](threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md) | threads-verification-boolean | 🟢 Done pkg-000052 — [pipeline](../epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-03-set-opaque-on-verification-success/STORY-IDS-VB-03-set-opaque-on-verification-success.md); set on phone/eID success; keep audit |
| [REQ9-01](req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md) | req9-make-env-load-parity | 🟢 Done pkg-000053 — [pipeline](../epics/EPIC-IDS-16-make-env-load-parity/stories/STORY-IDS-REQ9-01-make-env-required/STORY-IDS-REQ9-01-make-env-required.md); `make serve`/`dev` require `.env` (G8) |
| [REQ9-02](req9-make-env-load-parity/STORY-IDS-REQ9-02-check-env-required.md) | req9-make-env-load-parity | 🟢 Done pkg-000054 — [pipeline](../epics/EPIC-IDS-16-make-env-load-parity/stories/STORY-IDS-REQ9-02-check-env-required/STORY-IDS-REQ9-02-check-env-required.md); `make check-env` require `.env` |

## Aux (excluded from product denominator)

| Артефакт | Назначение |
|----------|------------|
| [GAP-CLOSURE-INDEX.md](GAP-CLOSURE-INDEX.md) | Gap-closure registry |
| [story-draft-handoff/INDEX.md](story-draft-handoff/INDEX.md) | DOC-DRAFT-05 canon sync (Done) |
| `DOC-IDS-ONB-*` | Doc tasks — см. [identity-onboarding/INDEX.md](identity-onboarding/INDEX.md); в active % MVP dashboard |
| `SPIKE-IDS-*` | External ops spikes |

## Эпики (pipeline)

| Эпик | Назначение |
|------|------------|
| `EPIC-IDS-AUTH-CORE` | профиль, `/me` |
| `EPIC-IDS-OAUTH` | OAuth-сервер для GPT |
| `EPIC-IDS-ONBOARDING` | UX-зонтик (web + GPT) |
| `EPIC-IDS-EID` | eID-платформа (провайдеры — deferred) |
| `EPIC-IDS-PHONE` | верификация телефона |
| `EPIC-IDS-SMSPM` / [`EPIC-IDS-14`](../epics/EPIC-IDS-14-smspm/EPIC-IDS-14-smspm.md) | live SMS через SMSPM (EE); SMSPM-01 pkg-000046; SMSPM-02 pkg-000047; SMSPM-03 pkg-000048 |
| Threads verification boolean (REQ21) / [`EPIC-IDS-15`](../epics/EPIC-IDS-15-threads-verification-boolean/EPIC-IDS-15-threads-verification-boolean.md) | VB-01/02/03 🟢 pkg-000050/051/052; backlog [`threads-verification-boolean/`](threads-verification-boolean/INDEX.md) |
| REQ9 make `.env` load (G8) / [`EPIC-IDS-16`](../epics/EPIC-IDS-16-make-env-load-parity/EPIC-IDS-16-make-env-load-parity.md) | REQ9-01 🟢 pkg-000053; REQ9-02 🟢 pkg-000054; backlog [`req9-make-env-load-parity/`](req9-make-env-load-parity/INDEX.md) |
| `EPIC-IDS-CLEANUP` | scope/doc hygiene |
| `EPIC-IDS-SEC` | security NFR |
| `EPIC-IDS-AUTHBFF` | POST-MVP BFF proxy |

## Порядок реализации (исторический)

См. предыдущую версия индекса (2026-06-04) — последовательность CLEANUP → AUTHCORE → OAuth/eID → phone → gateway glue остаётся справочной. **Next waves (2026-09-26):** SMSPM-03; CLEANUP-04; epic gates. **Closed:** EPIC-IDS-16 REQ9-01/02 🟢 (pkg-000053/054, 2026-09-26). **Closed:** EPIC-IDS-15 VB-01/02/03 🟢 (pkg-000050/051/052). **Closed:** SMSPM-04 🟢 (pkg-000049); SMSPM-02 🟢 (pkg-000047); SMSPM-01 🟢 (pkg-000046); ONB-01 🟢 (pkg-000045); AUTHCORE-02 🟢 (pkg-000044); SEC-04 🟢 (pkg-000043); DEPLOY-01 retired — deployability superseded by [`run-and-healthcheck.md`](../../runbook/run-and-healthcheck.md).

## Не вошло в стори

- **web3 wallet** — post-MVP ([gap §10](../../analysis/gap-analysis-full-2026-06-04.md))
- Полный сборный бэклог: [identity-todo-backlog-2026-06-04.md](../../analysis/identity-todo-backlog-2026-06-04.md)
