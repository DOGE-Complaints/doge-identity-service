# STORY-IDS-OAUTH-04 — Verify-gate в OAuth-флоу: relay действия + контракт `verification_required`

## Meta
- **Key:** `STORY-IDS-OAUTH-04-verify-gate-and-verification-required`
- **Parent Epic:** [`../../EPIC-IDS-11-oauth-server.md`](../../EPIC-IDS-11-oauth-server.md)
- **Epic alias (код/backlog):** `EPIC-IDS-OAUTH` · продуктовый зонтик [`EPIC-IDS-ONBOARDING`](../../../../backlog-stories/identity-onboarding/EPIC-IDS-ONBOARDING.md)
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md)
- **Decision Ref:** [`../../../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md); исследование флоу «GPT → submit → авторизация» 2026-06-23/24 ([`04-security §A`](../../../../../runtime-docs/04-security.md))
- **Источник:** исследование флоу «GPT → submit → авторизация» 2026-06-23/24 ([04-security §A](../../../../../runtime-docs/04-security.md)); gap «verify-need не пробрасывается, контракт `verification_required` под phone не зафиксирован».
- **Зависит от:** [STORY-IDS-OAUTH-01](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) (authorize/complete handshake — **🟢 построен**), [STORY-IDS-OAUTH-02](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md) (источник статуса), [PV-05](../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md) ✅ (phone verify готов)

## Зачем простыми словами
Когда юзер из GPT хочет подать историю, действие **требует верификации**. Нужно, чтобы это требование **доехало по цепочке**: GPT → authorize (с флагом «действие = подача истории») → после логина identity видит `phone_verified` → если не верифицирован, **ведём на verify (телефон)** прежде чем действие станет доступным; а downstream-потребитель (gateway) на submit получает **единый понятный отказ** `verification_required` (403) с тем, куда вести юзера. Сейчас этот «relay + контракт» нигде не зафиксирован: поля `return_context`/`requested_action` в модели есть, но через OAuth-флоу не прокидываются, а формат `verification_required` под phone не определён. **Это и есть та «связка submit-после-авторизации», вокруг которой возникала путаница** — она НЕ про «слать submit сразу», а про «донести требование verify и дать единый отказ».

## Scope
- **Relay действия через authorize→complete:** `/oauth/authorize` принимает/сохраняет `requested_action` (`stories:submit`) и `return_context`; `/oauth/authorize/complete` (после Supabase-логина) резолвит их вместе с пользователем. Поля уже в модели сессии ([`models.py`](../../../../../../src/core/domain/models.py) `return_context`/`requested_action`) — пробросить в OAuth-handshake (OAUTH-01).
- **Ветка «не верифицирован → verify»:** при `requested_action` требующем verify и `phone_verified=false` — identity сигналит «нужен verify» (маркер в ответе/redirect к verify-странице), reuse phone-флоу [PV-05](../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md). Зеркалит eID-флаг «нужен eID» из [04-security §A](../../../../../runtime-docs/04-security.md), но под **phone**.
- **Канон `verification_required` (403):** единый payload для downstream (gateway/GPT-петля): `{ "error": "verification_required", "reason": "...", "verify_url": "https://…/verify?context=…" }` — что отдаёт identity/gateway, когда `phone_verified=false`. Зафиксировать формат + verify-URL (gateway-сторона — в его репо; identity отдаёт через introspection/`/me` факт `phone_verified` + канон сообщения).
- **Маппинг на `SmsErrorCode`/HTTP:** verify-need ≠ ошибка телефона; это 403 авторизации, не 400 OTP. Развести явно.

## Вне scope
- Сам механизм introspection + сервисный токен — [OAUTH-02](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md).
- Сам OTP-флоу — [PV-05](../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md) ✅.
- Enforcement `verification_required` **на стороне gateway** (его репо) — здесь только identity-контракт + формат, который gateway переиспользует (см. [09-gateway-expectations](../../../../../runtime-docs/09-gateway-expectations.md)).
- eID-ветка (DEFERRED).

## Точки в коде (текущее состояние)
- Поля сигнала на `VerificationSession`, не на OAuth handshake: `return_context`/`requested_action` в [`models.py`](../../../../../../src/core/domain/models.py); `AuthorizationRequest` ([`models.py:138-147`](../../../../../../src/core/domain/models.py)) — **без** этих полей. `/oauth/*` — **построены** ([`asgi_app.py:370-416`](../../../../../../src/core/api/asgi_app.py), OAUTH-01 ✅); relay verify-need — scope OAUTH-04.
- OAuth handlers не читают контекст: [`handlers.py:22-116`](../../../../../../src/core/oauth/handlers.py).
- Durable handshake без колонок контекста: [`20260624000001_oauth_authorization_tables.sql`](../../../../../../supabase/migrations/20260624000001_oauth_authorization_tables.sql).
- Гейт-источник — `phone_verified` в [`me_response.py`](../../../../../../src/core/api/me_response.py), [`introspection.py:23-31`](../../../../../../src/core/oauth/introspection.py).
- `verification_required` под phone — **не определён** (стейл eID-вариант — в [`identity-backend.md`](../../../../../../../docs/Identity/identity-backend.md) FR-BE-010).
- OTP errors → 400: [`handlers.py:96-99`](../../../../../../src/core/api/handlers.py) (`_sms_error_http_status`).

## Acceptance Criteria
- [x] `requested_action`/`return_context` проходят authorize→complete и доступны после логина.
- [x] При действии, требующем verify, и `phone_verified=false` — identity сигналит «нужен verify» (маркер/redirect на verify), без выдачи «зелёного» статуса.
- [x] Зафиксирован канон `verification_required` (403) с `verify_url`; единый для web-gate и GPT-петли; **под `phone_verified`**, не `eid_verified`.
- [x] verify-need (403 авторизации) явно отделён от OTP-ошибок (`SmsErrorCode`, 400).
- [x] Покрыто offline-тестами; контракт описан для gateway ([09-gateway-expectations](../../../../../runtime-docs/09-gateway-expectations.md)).

## Парадигма-якорь
[04-security §A](../../../../../runtime-docs/04-security.md) (флоу подачи истории), [09-gateway-expectations](../../../../../runtime-docs/09-gateway-expectations.md) (стык), [DOC-IDS-ONB-01](../../../../backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md) (consumer-side гейт).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-11-04-t01-oauth-request-context-schema`](./task-ids-11-04-t01-oauth-request-context-schema/README.md) | pkg-000034 |
| 2 | [`task-ids-11-04-t02-oauth-authorize-relay-handlers`](./task-ids-11-04-t02-oauth-authorize-relay-handlers/README.md) | pkg-000034 |
| 3 | [`task-ids-11-04-t03-oauth-verify-gate-phone-branch`](./task-ids-11-04-t03-oauth-verify-gate-phone-branch/README.md) | pkg-000034 |
| 4 | [`task-ids-11-04-t04-verification-required-contract`](./task-ids-11-04-t04-verification-required-contract/README.md) | pkg-000034 |
| 5 | [`task-ids-11-04-t05-verify-need-vs-sms-error-http-mapping`](./task-ids-11-04-t05-verify-need-vs-sms-error-http-mapping/README.md) | pkg-000034 |
| 6 | [`task-ids-11-04-t06-offline-oauth-verify-gate-tests`](./task-ids-11-04-t06-offline-oauth-verify-gate-tests/README.md) | pkg-000034 |
| 7 | [`task-ids-11-04-t07-story-acceptance-verification`](./task-ids-11-04-t07-story-acceptance-verification/README.md) | pkg-000034 |
