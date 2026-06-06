# 09. Как identity стыкуется с gateway

## О чём этот документ

identity и gateway — два разных сервиса, и важно, чтобы они **не лезли в работу друг друга** (иначе получится «каша-спагетти»). Здесь простыми словами: где проходит граница, кто кого о чём спрашивает, и что для этого ещё нужно достроить в identity. Короткая суть: **истории создаёт gateway**, а identity лишь подтверждает «этот человек существует и прошёл eID». Контент историй через identity не ходит.

> Источник: код identity ([`asgi_app.py`](../../src/core/api/asgi_app.py), [`config/schema.py`](../../src/core/config/schema.py), [`repositories.py`](../../src/core/infrastructure/repositories.py)) + код gateway ([`security.py`](../../../doge-complaints-gateway/src/core/api/security.py)) + решения оператора от 2026-06-04 ([gap-анализ](../analysis/gap-analysis-full-2026-06-04.md)).

## Целевая парадигма (решено 2026-06-04) — «не смешиваем сервисы»

Подача истории из GPT:
1. GPT нужен OAuth-токен. Нет токена → редирект на **страницу авторизации в общем UI**, с флагом «нужна eID-верификация» (т.к. действие = подача истории).
2. Пользователь логинится/регистрируется; **identity** выдаёт OAuth access-токен и знает eID-статус.
3. eID не пройден → редирект на активный eID-провайдер → callback → identity ставит eID=verified.
4. GPT получает токен и **сам шлёт запрос создания истории напрямую в gateway**. Контент в identity не заходит.
5. **gateway** принимает историю, проверяет доступ (см. модель ниже) и создаёт её.

### Модель аутентификации (решено: сервисный токен + introspection)

Два независимых слоя:
- **Слой доверия сервисов:** сервисный токен (gateway уже умеет — `SERVICE_API_TOKEN` / `X-Service-Token`, [`gateway security.py:17-20,69`](../../../doge-complaints-gateway/src/core/api/security.py)) или mTLS. Отсекает левых клиентов.
- **Слой пользователя (introspection):** gateway берёт **пользовательский** OAuth-токен и **спрашивает identity** (introspection / `/me`): `{active, sub, eid_verified}`. eID-статус в самом токене НЕ кодируется (решение оператора) — gateway всегда получает свежий статус у identity.

Почему так (best practice): сервисный токен доказывает «зовёт доверенный сервис», но НЕ доказывает, какой человек и пройден ли eID. Для платформы, где eID — суть подотчётности, gateway обязан проверить пользователя (иначе «confused deputy» — подача за кого угодно). Подробный разбор — в gap-отчёте.

## Что для этого нужно от identity (по факту — пока нет)

| Нужно (по парадигме) | Факт в коде identity | Статус |
|----------------------|----------------------|--------|
| Introspection-endpoint (или рабочий `/me`), отдающий `active/sub/eid_verified` для токена пользователя | `/me` — 🟡 заглушка 501 ([`asgi_app.py:159-169`](../../src/core/api/asgi_app.py)); `/oauth/introspect` — **отсутствует** | ❌/🟡 |
| Выдача OAuth-токена | `InMemoryOAuthTokenService` ([`repositories.py:238-346`](../../src/core/infrastructure/repositories.py)) — логика есть, но роуты `/oauth/*` — 🟡 501 | 🟡 |
| Проверка сервисного токена на входе identity | в identity-конфиге **нет** `SERVICE_API_TOKEN` ([`schema.py`](../../src/core/config/schema.py)) | ❌ |

## Чего identity НЕ должен делать (следствие парадигмы)

- ❌ **НЕ форвардить истории** в gateway. Поэтому `COMPLAINTS_GATEWAY_URL` identity **не нужен** (его отсутствие — корректно, не gap).
- ❌ **НЕ** экспонировать story HTTP-маршруты в identity (удалены в CLEANUP-01; см. [01-api](01-api.md)).
- ❌ НЕ хранить контент историй (`story_drafts` — вне operational bootstrap; deprecated migration historical only).

## Связь по значению (остаётся)

gateway хранит `stories.submitter_identity_issuer` (строка, NOT NULL — [gateway миграция `20260515_1200`](../../../doge-complaints-gateway/supabase/migrations/20260515_1200_submitter_identity_issuer_not_null.sql)) — слабая связанность, корректна при раздельных сервисах/Supabase-проектах ([../analysis/supabase-project-separation-audit-2026-06-03.md](../analysis/supabase-project-separation-audit-2026-06-03.md)).

## Итог
В коде identity стык с gateway **ещё не реализован** под решённую парадигму: нет introspection-endpoint, нет проверки сервисного токена, OAuth-роуты — заглушки. Story-маршруты и `story_drafts` уже убраны (CLEANUP-01). Оставшиеся задачи — в gap-отчёте как будущие эпики.
