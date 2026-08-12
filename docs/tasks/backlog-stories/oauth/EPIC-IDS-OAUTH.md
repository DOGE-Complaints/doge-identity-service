# EPIC-IDS-OAUTH — OAuth-сервер для GPT + межсервисная валидация

> **ID:** `EPIC-IDS-OAUTH` (код-алиас, `next_epic` в [`asgi_app.py`](../../../../src/core/api/asgi_app.py); pipeline `EPIC-IDS-11`) · **Статус:** 🟢 Done (OAUTH-01…04 — pkg-000029…034) · **Тип:** Функциональный
> **Продуктовый зонтик:** [`EPIC-IDS-ONBOARDING`](../identity-onboarding/EPIC-IDS-ONBOARDING.md) — эти стори обеспечивают вход #2 (редирект из кастомного GPT).
> **Pipeline:** [`EPIC-IDS-11`](../../epics/EPIC-IDS-11-oauth-server/EPIC-IDS-11-oauth-server.md) (OAUTH-01 🟢, OAUTH-02 🟢, OAUTH-03 🟢, OAUTH-04 🟢 Done; pkg-000029…034).

## Назначение
Подключить identity как **OAuth 2.0 сервер** для Custom GPT: выдать authorization code, обменять на access-токен, затем дать gateway межсервисную валидацию (introspection + сервисный токен). **OAUTH-01**, **OAUTH-02** и **OAUTH-03 построены** (маршруты `/oauth/*`, `POST /oauth/introspect`, durable Supabase-стор при `DB_BACKEND=supabase`, [`core/oauth/`](../../../../src/core/oauth/)).

## Контекст
- Источник: backlog [`identity-todo-backlog-2026-06-04`](../../../analysis/identity-todo-backlog-2026-06-04.md) (A4/C7/C8/B5/B6; gaps SEC-1 ✅, API-1, CFG-1).
- Целевой UX входа из GPT: [`identity-onboarding-ux-2026-06-12`](../../../analysis/identity-onboarding-ux-2026-06-12.md) (gap G1).

## Состав
| Story | Тема | Слой | Зависит | Статус |
|-------|------|------|---------|--------|
| [STORY-IDS-OAUTH-01](STORY-IDS-OAUTH-01-oauth-server-endpoints.md) | OAuth-сервер наружу (`/oauth/*` → движок, PKCE, client_secret) | код | [AUTHCORE-01](../auth-core/STORY-IDS-AUTHCORE-01-profile-and-me.md) | 🟢 Done ([pipeline](../../epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-01-oauth-server-endpoints/STORY-IDS-OAUTH-01-oauth-server-endpoints.md), pkg-000029) |
| [STORY-IDS-OAUTH-02](STORY-IDS-OAUTH-02-introspection-and-service-token.md) | introspection + сервисный токен (склейка с gateway) | код | OAUTH-01 ✅, [EID-01](../eid/STORY-IDS-EID-01-eid-verification-flow.md) | 🟢 Done ([pipeline](../../epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-02-introspection-and-service-token/STORY-IDS-OAUTH-02-introspection-and-service-token.md), pkg-000030) |
| [STORY-IDS-OAUTH-03](STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) | durable стор codes/handshake в Supabase Postgres (надёжность от редеплоя) | код/данные | OAUTH-01 ✅ | 🟢 Done ([pipeline](../../epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-03-persistent-token-store-supabase/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md), pkg-000033) |
| [STORY-IDS-OAUTH-04](STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md) | verify-gate в OAuth-флоу: relay `requested_action` + канон `verification_required` (phone) | код/контракт | OAUTH-01 ✅, OAUTH-02, PV-05 ✅ | 🟢 Done (pkg-000034) |

> **Статус (2026-06-26):** OAUTH-01…04 — **🟢 Done** (роуты `/oauth/*`, `POST /oauth/introspect`, service token gate, durable Supabase-стор при `DB_BACKEND=supabase`, verify-gate `verification_required`). Эпик закрыт по коду. doc-PLAN актуализации — **🟢 выполнен**. `/me` и телефонная верификация — построены.

## Документация
- [PLAN-IDS-OAUTH-docs-actualization](PLAN-IDS-OAUTH-docs-actualization.md) — план актуализации флоу-докатов. **🟢 Выполнен 2026-06-24:** `04-security §A` (диаграмма+текст+таблица под phone, `/me`✅, eID→DEFERRED) и `09-gateway-expectations` (introspection→`phone_verified`, `/me` не 501) приведены к факту. Шаг 4 (сводный explainer) — не делался (опционально).

## Порядок реализации
**Доки:** [PLAN-IDS-OAUTH-docs-actualization](PLAN-IDS-OAUTH-docs-actualization.md) — 🟢 выполнен.
**Код:** **OAUTH-01** ✅ → **OAUTH-02** ✅ → **OAUTH-03** ✅ (durable Supabase-стор codes/handshake) → **OAUTH-04** (relay verify-need + канон `verification_required` — замыкает «submit-после-авторизации» под phone).

> **Phone-pivot:** активный гейт — `phone_verified` (eID отложен). Introspection/verify-контракт — под телефон.

> **Почему не Supabase-OAuth-сервер:** ADR-IDS-002 отклонил Supabase OAuth 2.1 Server (меньше контроля над claims/scope); Supabase используется только как Postgres-персистентность (OAUTH-03), сервер — наш. Access-токены — stateless HS256, редеплой их не ломает.

## Связь
Зонтик: [`EPIC-IDS-ONBOARDING`](../identity-onboarding/EPIC-IDS-ONBOARDING.md). Парадигма: [`04-security`](../../../runtime-docs/04-security.md), [`09-gateway-expectations`](../../../runtime-docs/09-gateway-expectations.md).
