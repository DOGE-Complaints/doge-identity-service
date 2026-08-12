# Индекс backlog-стори identity (2026-07-24)

> **SSOT per package:** [`*/INDEX.md`](./) tables + [bullrun-launch-index](../bullrun-launch-index.md)  
> **Audit:** [backlog-status-audit-2026-07-09.md](../../analysis/backlog-status-audit-2026-07-09.md) · **Dashboard:** [identity-mvp-dashboard.md](../identity-mvp-dashboard.md)

## Карта пакетов

| Пакет | INDEX | Stories (product) | Progress |
|-------|-------|-------------------|----------|
| Auth-core | [auth-core/INDEX.md](auth-core/INDEX.md) | 2 | 100% |
| OAuth | [oauth/INDEX.md](oauth/INDEX.md) | 4 | 100% |
| eID platform | [eid/INDEX.md](eid/INDEX.md) | 7 | 100% |
| Phone verification | [phone-verification/INDEX.md](phone-verification/INDEX.md) | 9 | 100% |
| Cleanup | [cleanup/INDEX.md](cleanup/INDEX.md) | 4 | 75% |
| Security hardening | [security-hardening/INDEX.md](security-hardening/INDEX.md) | 7 | 86% (SEC-05 Deferred) |
| Identity onboarding | [identity-onboarding/INDEX.md](identity-onboarding/INDEX.md) | 1 | 0% |
| eID deferred | [eid-deferred/INDEX.md](eid-deferred/INDEX.md) | 6 | POST-MVP |
| Auth-BFF | [auth-bff/INDEX.md](auth-bff/INDEX.md) | 3 | POST-MVP |

**Context (narrative):** каждый пакет также имеет `EPIC-IDS-*.md` или `README.md` — см. ссылку «Context» в package INDEX.

## Открытые product stories (identity-backend)

| Story | Пакет | Блокер / evidence |
|-------|-------|-------------------|
| [ONB-01](identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md) | onboarding | 🟢 Done pkg-000045 — `email`/`email_verified` in [`me_response.py`](../../src/core/api/me_response.py); [pipeline](../epics/EPIC-IDS-13-onboarding/stories/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md) |
| [CLEANUP-04](cleanup/STORY-IDS-CLEANUP-04-spec-reconciliation.md) | cleanup | gateway-copy specs в [`06-technical-scaffold.md`](../../requirements/06-technical-scaffold.md) |

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
| `EPIC-IDS-CLEANUP` | scope/doc hygiene |
| `EPIC-IDS-SEC` | security NFR |
| `EPIC-IDS-AUTHBFF` | POST-MVP BFF proxy |

## Порядок реализации (исторический)

См. предыдущую версия индекса (2026-06-04) — последовательность CLEANUP → AUTHCORE → OAuth/eID → phone → gateway glue остаётся справочной. **Next waves (2026-07-24):** CLEANUP-04. **Closed:** ONB-01 🟢 (pkg-000045); AUTHCORE-02 🟢 (pkg-000044); SEC-04 🟢 (pkg-000043); DEPLOY-01 retired — deployability superseded by [`run-and-healthcheck.md`](../../runbook/run-and-healthcheck.md).

## Не вошло в стори

- **web3 wallet** — post-MVP ([gap §10](../../analysis/gap-analysis-full-2026-06-04.md))
- Полный сборный бэклог: [identity-todo-backlog-2026-06-04.md](../../analysis/identity-todo-backlog-2026-06-04.md)
