# 09. Как identity стыкуется с gateway

## О чём этот документ

identity и gateway — два разных сервиса, и важно, чтобы они **не лезли в работу друг друга** (иначе получится «каша-спагетти»). Здесь простыми словами: где проходит граница, кто кого о чём спрашивает, и что для этого ещё нужно достроить в identity. Короткая суть: **истории создаёт gateway**, а identity лишь подтверждает «этот человек существует и прошёл eID». Контент историй через identity не ходит.

> Источник: код identity ([`asgi_app.py`](../../src/core/api/asgi_app.py), [`config/schema.py`](../../src/core/config/schema.py), [`repositories.py`](../../src/core/infrastructure/repositories.py)) + код gateway ([`security.py`](../../../doge-complaints-gateway/src/core/api/security.py)) + решения оператора от 2026-06-04 ([gap-анализ](../analysis/gap-analysis-full-2026-06-04.md)).

## Целевая парадигма (решено 2026-06-04) — «не смешиваем сервисы»

> **Phone-pivot (2026-06):** активный гейт — `phone_verified` (SMS-OTP); eID **отложен**. Везде ниже, где «eID», читать как «верификация (телефон)»; introspection отдаёт `phone_verified`.

Подача истории из GPT:
1. GPT нужен OAuth-токен. Нет токена → редирект на **страницу авторизации в общем UI**, с флагом «нужна верификация» (т.к. действие = подача истории).
2. Пользователь логинится/регистрируется; **identity** выдаёт OAuth access-токен и знает статус `phone_verified`.
3. Телефон не подтверждён → inline-экран verify (ввод номера +372 → SMS-код, `/auth/phone/request` → `/auth/phone/confirm`) → identity ставит `phone_verified=true`. (Внешнего redirect нет — это наши же API; eID-redirect — DEFERRED.)
4. GPT получает токен и **сам шлёт запрос создания истории напрямую в gateway**. Контент в identity не заходит.
5. **gateway** принимает историю, проверяет доступ (см. модель ниже) и создаёт её.

### Модель аутентификации (решено: сервисный токен + introspection)

Два независимых слоя:
- **Слой доверия сервисов:** сервисный токен (gateway уже умеет — `SERVICE_API_TOKEN` / `X-Service-Token`, [`gateway security.py:17-20,69`](../../../doge-complaints-gateway/src/core/api/security.py)) или mTLS. Отсекает левых клиентов.
- **Слой пользователя (introspection):** gateway берёт **пользовательский** OAuth-токен и **спрашивает identity** (introspection / `/me`): `{active, sub, phone_verified}`. Статус верификации в самом токене НЕ кодируется (решение оператора) — gateway всегда получает свежий статус у identity.

Почему так (best practice): сервисный токен доказывает «зовёт доверенный сервис», но НЕ доказывает, какой человек и пройдена ли верификация. Для платформы, где проверенная личность — суть подотчётности, gateway обязан проверить пользователя (иначе «confused deputy» — подача за кого угодно). Подробный разбор — в gap-отчёте.

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

Gateway при submit может отдавать тот же shape, опираясь на introspection `{active, sub, phone_verified:false}`. Enforcement на стороне gateway — в его репо.

## Чего identity НЕ должен делать (следствие парадигмы)

- ❌ **НЕ форвардить истории** в gateway. Поэтому `COMPLAINTS_GATEWAY_URL` identity **не нужен** (его отсутствие — корректно, не gap).
- ❌ **НЕ** экспонировать story HTTP-маршруты в identity (удалены в CLEANUP-01; см. [01-api](01-api.md)).
- ❌ НЕ хранить контент историй (`story_drafts` — вне operational bootstrap; deprecated migration historical only).

## Связь по значению (остаётся)

gateway хранит `stories.submitter_identity_issuer` (строка, NOT NULL — [gateway миграция `20260515_1200`](../../../doge-complaints-gateway/supabase/migrations/20260515_1200_submitter_identity_issuer_not_null.sql)) — слабая связанность, корректна при раздельных сервисах/Supabase-проектах ([../analysis/supabase-project-separation-audit-2026-06-03.md](../analysis/supabase-project-separation-audit-2026-06-03.md)).

## Итог
В коде identity OAuth-выдача, **introspection+сервисный gate**, **durable handshake/codes при `DB_BACKEND=supabase`**, **verify-gate relay + `verification_required`** **построены** (OAUTH-01, OAUTH-02, OAUTH-03, OAUTH-04); gateway intake (вызов introspection при создании истории) — **ещё не подключён**. Story-маршруты и `story_drafts` уже убраны (CLEANUP-01). Оставшаяся задача — подключение gateway.
