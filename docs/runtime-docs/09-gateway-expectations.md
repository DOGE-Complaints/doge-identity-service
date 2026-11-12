# 09. Как identity стыкуется с gateway

## О чём этот документ

identity и gateway — два разных сервиса, и важно, чтобы они **не лезли в работу друг друга** (иначе получится «каша-спагетти»). Здесь простыми словами: где проходит граница, кто кого о чём спрашивает, и что для этого ещё нужно достроить в identity. Короткая суть: **истории создаёт gateway**, а identity лишь подтверждает «этот человек существует и прошёл eID». Контент историй через identity не ходит.

> Источник: код identity ([`asgi_app.py`](../../src/core/api/asgi_app.py), [`config/schema.py`](../../src/core/config/schema.py), [`repositories.py`](../../src/core/infrastructure/repositories.py)) + код gateway ([`security.py`](../../../doge-complaints-gateway/src/core/api/security.py)) + решения оператора от 2026-06-04 ([gap-анализ](../analysis/gap-analysis-full-2026-06-04.md)).

## Целевая парадигма (решено 2026-06-04, submit актуализирован 2026-07-04) — «не смешиваем сервисы»

> **Phone-pivot (2026-06):** активный *метод* верификации — SMS-OTP (`phone_verified`); eID **отложен**.  
> **REQ7 consumer canon (2026-09-21, EPIC-IDS-15):** method-opaque **`identity_verified`** на `GET /me` — канон для threads / civic / новых spa gates. Legacy story-draft submit (GW-DRAFT-02) и OAuth introspect пока читают `phone_verified` до sibling cutover (STORY-GW-THR-03 / OAuth follow-up).

> **Browser-submit (2026-07-04, GW-DRAFT-02):** продуктовый user path — GPT стешит → браузер сабмитит через `/story-drafts*`. OAuth/introspection **остаются** для GPT Actions (D-6). As-built: [`API_REFERENCE §6.8`](../../../doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md).

### Подача истории (browser-submit handoff)

**OAuth-преамбула (D-6 — без изменений):**

1. GPT нужен OAuth access token для Actions. Нет токена → редирект на **страницу авторизации в spa-app**, с флагом «нужна верификация» (`requested_action=stories:submit`).
2. Пользователь логинится/регистрируется; **identity** выдаёт OAuth access token через `/oauth/authorize` → `/oauth/token` и знает `phone_verified`.
3. Телефон не подтверждён → inline verify (`/auth/phone/request` → `/auth/phone/confirm`) → `phone_verified=true`. (eID-redirect — DEFERRED.)

**Handoff submit (актуальный user path):**

4. **GPT стешит** черновик: `POST /story-drafts` на gateway (**только service token**, тело = `StoryIntakeRequest`) → `draft_id`. Контент в identity **не** заходит.
5. **GPT редиректит браузер** (spa) на handoff с `draft_id`.
6. **Браузер:** `GET /story-drafts/{draft_id}` (Supabase Bearer) → preview; затем **`POST /story-drafts/{draft_id}/submit`** (тот же Bearer) → gateway форвардит Bearer → identity **`GET /me`**, гейт `phone_verified` → **202** или **403** `verification_required`.

> **Superseded (GW-DRAFT-03):** ранее шаг 4–5 описывались как «GPT **сам шлёт** запрос создания истории напрямую в gateway» с OAuth user token + gateway **`POST /oauth/introspect`**. Это **не** продуктовый user path после handoff.

### Модель аутентификации (по пути)

| Путь | Service token | User auth | Identity check |
|------|---------------|-----------|----------------|
| GPT stash `POST /story-drafts` | ✅ required | ❌ none | identity не участвует |
| Browser read `GET /story-drafts/{id}` | ❌ | Supabase Bearer | **`GET /me`** (session only) |
| Browser submit `POST …/submit` | ❌ | Supabase Bearer | **`GET /me`** + **legacy** `phone_verified` gate (GW-DRAFT-02 as-built; civic REQ7 → THR-03 → `identity_verified`) |
| GPT Actions / lazy-gate (D-6) | varies | OAuth or Supabase | **`POST /oauth/introspect`** → `{active, sub, phone_verified}` (**legacy**) or **`GET /me`** |
| Civic / threads write (REQ7) | — | Bearer / Me client | **`GET /me`** → **`identity_verified`** only (identity Done; gateway gate cutover = GW-THR-03) |

**Слой доверия сервисов:** `SERVICE_API_TOKEN` / `X-Service-Token` на stash и operator intake ([`gateway security.py`](../../../doge-complaints-gateway/src/core/api/security.py)).

**Слой пользователя:** статус верификации **не** кодируется в JWT навсегда — потребители спрашивают identity свежий флаг. **REQ7 canon:** `data.identity_verified` на **`GET /me`**. Story-draft submit as-built (GW-DRAFT-02) всё ещё гейтит `phone_verified` до THR-03.

Почему так: сервисный токен доказывает «зовёт доверенный сервис», но не доказывает человека. Browser submit без проверки у identity = «confused deputy». Подробный разбор — в gap-отчёте.

## Ленивый гейт телефона (web signup, enforce на потребителе)

> **Источник:** [DOC-IDS-ONB-01](../tasks/backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md) · gap G3 в [`identity-onboarding-ux-2026-06-12`](../analysis/identity-onboarding-ux-2026-06-12.md).

При **web signup** телефон **не** спрашиваем при регистрации — только в момент **защищённого действия** (продуктовое решение 2026-06-12). Identity **не** блокирует действия сам: отдаёт флаги и флоу верификации; **enforce — на потребителе** (spa-app / gateway / threads).

### Контракт (gateway / spa / threads перед действием)

1. Потребитель читает статус верификации:
   - **REQ7 (threads / civic / new spa):** `GET /me` → **`identity_verified`** ([`me_response.py:35,51`](../../src/core/api/me_response.py); [API_REFERENCE §6](api-reference/API_REFERENCE.md); [REQ 21](../requirements/21-verification-boolean-and-audit.md)).
   - **gateway story-draft submit (GW-DRAFT-02, legacy as-built):** `GET /me` → `phone_verified` ([`me_client.py`](../../../doge-complaints-gateway/src/core/identity/me_client.py)) — cutover to opaque = [STORY-GW-THR-03](../../../doge-complaints-gateway/docs/tasks/backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-03-civic-gate-identity-verified.md).
   - **gateway / GPT Actions (D-6, legacy):** `POST /oauth/introspect` → `{active, sub, phone_verified}` ([`introspection.py`](../../src/core/oauth/introspection.py)).
2. Если требуемый флаг false → **не выполнять** действие; направить на verify (PV-05).
3. После успешного confirm (`phone_verified` + **`identity_verified`** true) → повторить действие.

**Каноничный пример (browser-submit, as-built):** `POST /story-drafts/{draft_id}/submit` гейтит **`phone_verified`** через `/me` до THR-03. **Канон REQ7 для новых civic/threads paths:** opaque **`identity_verified`**.

> **Superseded:** «перед `POST …/stories`» как единственный user path — operator/service intake; GPT-direct submit с introspection — см. GW-DRAFT-03.

### Sequence (словами, web)

Пользователь пользуется системой без телефона → инициирует защищённое действие (напр. «создать стори») → потребитель видит `phone_verified=false` → verify-экран (PV-05) → `phone_verified=true` → действие выполняется.

**SSOT флоу верификации:** [STORY-IDS-PV-05](../tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-05-verification-flow-api/STORY-IDS-PV-05-verification-flow-api.md) · [19-phone-verification-flow](../requirements/19-phone-verification-flow.md) · runbook [`onboarding-phone-verification-api.md`](../runbook/onboarding-phone-verification-api.md).

**Вне scope identity:** полный перечень защищённых действий — продукт/gateway; код гейта в этом репозитории **отсутствует намеренно**.

## Что для этого нужно от identity (по факту)

| Нужно (по парадигме) | Факт в коде identity | Статус |
|----------------------|----------------------|--------|
| Introspection-endpoint (или рабочий `/me`), отдающий `active/sub/phone_verified` для токена пользователя | `/me` — ✅ **построен** (AUTHCORE-01); `/oauth/introspect` — ✅ **построен** ([`introspection.py`](../../src/core/oauth/introspection.py), [OAUTH-02](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md)) | ✅ |
| Выдача OAuth-токена | [`core/oauth/handlers.py`](../../src/core/oauth/handlers.py), маршруты [`asgi_app.py:368-403`](../../src/core/api/asgi_app.py) | ✅ ([OAUTH-01](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md)) |
| Проверка сервисного токена на входе identity | `AppConfig.service_api_token` + `ServiceTokenAuth` ([`schema.py`](../../src/core/config/schema.py), [`security.py`](../../src/core/api/security.py)); обязателен в `APP_PROFILE=pilot` | ✅ |
| OAuth verify-gate relay + `verification_required` (403) при `phone_verified=false` | [`handlers.py`](../../src/core/oauth/handlers.py), [`verification_required.py`](../../src/core/oauth/verification_required.py) — `POST /oauth/authorize/complete` с `requested_action=stories:submit` → `{error, reason, verify_url}` | ✅ ([OAUTH-04](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md)) |

### Контракт `verification_required` (identity, OAUTH-04)

Когда OAuth complete-path требует phone verify (`requested_action=stories:submit`, `phone_verified=false`), identity отвечает **HTTP 403** (не 400 OTP):

```json
{
  "error": "verification_required",
  "reason": "Phone verification is required before this action can proceed.",
  "verify_url": "https://<spa>/verify?context=<return_context>"
}
```

Gateway при **`POST /story-drafts/{id}/submit`** отдаёт тот же shape, опираясь на **`GET /me`** (`phone_verified:false` → 403). Introspection-контракт остаётся для других путей (D-6). Enforcement на стороне gateway — в его репо.

## Чего identity НЕ должен делать (следствие парадигмы)

- ❌ **НЕ форвардить истории** в gateway. Поэтому `COMPLAINTS_GATEWAY_URL` identity **не нужен** (его отсутствие — корректно, не gap).
- ❌ **НЕ** экспонировать story HTTP-маршруты в identity (удалены в CLEANUP-01; см. [01-api](01-api.md)).
- ❌ НЕ хранить контент историй (`story_drafts` — вне operational bootstrap; deprecated migration historical only).

## Связь по значению (остаётся)

gateway хранит `stories.submitter_identity_issuer` (строка, NOT NULL — [gateway миграция `20260515_1200`](../../../doge-complaints-gateway/supabase/migrations/20260515_1200_submitter_identity_issuer_not_null.sql)) — слабая связанность, корректна при раздельных сервисах/Supabase-проектах ([../analysis/supabase-project-separation-audit-2026-06-03.md](../analysis/supabase-project-separation-audit-2026-06-03.md)).

## Итог

В коде identity OAuth-выдача, **introspection+сервисный gate**, **durable handshake/codes при `DB_BACKEND=supabase`**, **verify-gate relay + `verification_required`** **построены** (OAUTH-01…OAUTH-04). Gateway story-draft handoff (**GW-DRAFT-01/02**) **подключён**: read/submit вызывают identity **`GET /me`**. Story-маршруты в identity убраны (CLEANUP-01). OAuth-канон для GPT Actions **без изменений** (D-6).

## As-built references (cross-repo)

- Gateway [`API_REFERENCE.md §6.8`](../../../doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md)
- Gateway [`story-draft-handoff/INDEX.md`](../../../doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/INDEX.md)
- Gateway [`security-env-api-access.md §4`](../../../doge-complaints-gateway/docs/runtime-docs/security-env-api-access.md)
- Identity story [`STORY-IDS-DOC-DRAFT-05`](../tasks/backlog-stories/story-draft-handoff/STORY-IDS-DOC-DRAFT-05-browser-submit-security-canon-sync.md)
