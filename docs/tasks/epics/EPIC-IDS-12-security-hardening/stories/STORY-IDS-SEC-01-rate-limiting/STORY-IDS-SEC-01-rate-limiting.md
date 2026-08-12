# STORY-IDS-SEC-01 — Per-user rate limiting + 429/`retry_after` для чувствительных роутов

## Meta
- **Key:** `STORY-IDS-SEC-01-rate-limiting`
- **Parent Epic:** [`../../EPIC-IDS-12-security-hardening.md`](../../EPIC-IDS-12-security-hardening.md)
- **Epic alias (код/backlog):** `EPIC-IDS-SEC` · [`EPIC-IDS-SEC`](../../../../backlog-stories/security-hardening/EPIC-IDS-SEC.md)
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md`](../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md)
- **Decision Ref:** [`../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md`](../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md); [`identity-backend-full-audit-2026-06-24.md`](../../../../../analysis/identity-backend-full-audit-2026-06-24.md) §3 G-1
- **Источник:** [`identity-backend-full-audit-2026-06-24.md`](../../../../../analysis/identity-backend-full-audit-2026-06-24.md) — гэп **G-1** (HIGH)
- **Зависит от:** —

## Зачем простыми словами
Сейчас нет **никакой** защиты от частых повторных запросов: один JWT может сколько угодно раз дёргать «начать eID» или «прислать SMS-код». Единственное ограничение, что есть, — это пауза между двумя SMS подряд (cooldown), и она возвращает не тот ответ, который требует спека. Цель стори — на уровне **требований** зафиксировать: какие роуты считаем чувствительными, сколько запросов на пользователя за окно разрешаем, и как именно отвечаем при превышении (HTTP 429 + «через сколько секунд можно повторить»). Это анти-абьюз и защита от лишних трат на SMS/eID.

## Scope (только требования)
- **Определить набор чувствительных роутов** и лимит на каждый (per-user; для callback-роутов возможно per-ip). Источник целевых значений — [`16:38-53`](../../../../../requirements/16-security-privacy-observability.md) (таблица `RATE_LIMITS`) и [`11:127-130`](../../../../../requirements/11-eid-verification-flow.md):
  - `POST /auth/eid/start` — 5 запросов / 10 минут / пользователь;
  - `POST /auth/phone/request` — лимит на пользователя (значение зафиксировать; согласовать с существующим `PHONE_RESEND_COOLDOWN_S`, чтобы они не противоречили);
  - прочие чувствительные роуты из `RATE_LIMITS` (например `/auth/eid/callback` per-ip), если применимы к identity.
- **Контракт ответа при превышении:** HTTP `429` с конвертом, включающим `retry_after` (секунды до следующего разрешённого запроса), по форме [`16:48-53`](../../../../../requirements/16-security-privacy-observability.md). Согласовать код ошибки в `{error}`-конверте с существующим envelope-контрактом сервиса.
- **Где enforce'ится** (требование, не реализация): лимит должен применяться **до** бизнес-логики хендлера — как сквозной слой (dependency/middleware), а не дублироваться в каждом хендлере. Конкретный механизм и стор (in-memory vs Redis) — выбор реализации, не часть этой стори.
- **Согласование с OTP-cooldown:** существующий cooldown ([`handlers.py:458-473`](../../../../../../src/core/api/handlers.py)) поднимает доменный `SmsSenderError(RATE_LIMITED)`, а не HTTP 429. Требование — определить, остаётся ли cooldown как есть (доменная ошибка флоу) и/или мапится в 429, чтобы поведение было непротиворечивым.
- **Конфигурируемость:** лимиты задаются конфигом (значения и окна), а не зашиты в код.

## Вне scope
- Выбор библиотеки/механизма (middleware vs dependency), стор лимитов (in-memory/Redis), алгоритм окна (sliding/fixed) — этап реализации.
- Rate-limit для роутов, отсутствующих в identity (gateway-only `/stories`, `/gpt/...` из таблицы 16 — reference-only, см. аудит HD-1).
- Durable phone-сессии (G-3) и durable phone-аудит — другие стори.

## Точки в коде (текущее состояние)
- **Rate-limiter отсутствует во всём `src/core/`.** `grep -niE "429|retry_after|RateLimit|rate.limit"` по `src/core/` даёт совпадения **только** в Telnyx-провайдере ([`phone/telnyx/errors.py:12,58-59`](../../../../../../src/core/phone/telnyx/errors.py) — маппинг внешнего 429 Telnyx в `SmsErrorCode.RATE_LIMITED`) и в OTP-cooldown. HTTP-уровневого per-user лимитера нет.
- **Единственный анти-повтор — OTP-cooldown:** [`handlers.py:456-473`](../../../../../../src/core/api/handlers.py) — если активная сессия моложе `phone_resend_cooldown_s`, поднимается `SmsSenderError(code=SmsErrorCode.RATE_LIMITED)` ([handlers.py:470-473](../../../../../../src/core/api/handlers.py)); это доменная ошибка флоу, **не** HTTP 429 и **не** per-user счётчик по окну.
- **`/auth/eid/start`** ([`handlers.py:169`](../../../../../../src/core/api/handlers.py) `handle_auth_eid_start`) — лимита нет вовсе.
- **eID callback (identity):** `GET /auth/{provider}/callback` ([`asgi_app.py:301`](../../../../../../src/core/api/asgi_app.py)) — per-ip лимит из spec 16 применим; путь `/auth/eid/callback` в таблице spec — reference alias.

## Волна pkg-000035 (операторское решение, implementation note)
HTTP rate-limit **не дублирует** OTP-cooldown. В pkg-000035 wire: `POST /auth/eid/start` (5/10min/user) + `GET /auth/{provider}/callback` (5/10min/ip). `POST /auth/phone/request` HTTP rate-limit — **follow-up** (cooldown [`PHONE_RESEND_COOLDOWN_S`](../../../../../../src/core/config/schema.py) остаётся доменным 400 `RATE_LIMITED`).

## Acceptance Criteria
- [x] Зафиксирован перечень чувствительных identity-роутов с лимитом (requests/window/scope) на каждый; значения для `/auth/eid/start` = 5/10мин/user соответствуют [`11:129`](../../../../../requirements/11-eid-verification-flow.md) и [`16:38-53`](../../../../../requirements/16-security-privacy-observability.md).
- [x] При превышении лимита роут отвечает HTTP `429` с `retry_after` (секунды) в конверте ошибки; форма ответа согласована с envelope-контрактом сервиса.
- [x] Лимит применяется до бизнес-логики хендлера (сквозной слой), а не индивидуально внутри каждого хендлера — зафиксировано как требование.
- [x] Описано непротиворечивое сосуществование с OTP-cooldown (`PHONE_RESEND_COOLDOWN_S`): что остаётся доменной ошибкой, что мапится в 429.
- [x] Лимиты и окна задаются конфигом; тест демонстрирует 429+`retry_after` на N+1-м запросе в окне для хотя бы одного роута.
- [ ] (Альтернатива, если оператор решит не строить) — таблица `RATE_LIMITS`/требование 11:127-130 явно помечены **DEFERRED** в спеках с обоснованием; AC закрывается этой пометкой.

## Парадигма-якорь
[`16-security-privacy-observability.md`](../../../../../requirements/16-security-privacy-observability.md) (Rate Limiting + 429/`retry_after`), [`11-eid-verification-flow.md`](../../../../../requirements/11-eid-verification-flow.md) (eID-start лимит), [`runtime-docs/04-security.md`](../../../../../runtime-docs/04-security.md) (anti-abuse).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-12-01-t01-rate-limit-config-schema`](./task-ids-12-01-t01-rate-limit-config-schema/README.md) | pkg-000035 |
| 2 | [`task-ids-12-01-t02-in-memory-rate-limiter-store`](./task-ids-12-01-t02-in-memory-rate-limiter-store/README.md) | pkg-000035 |
| 3 | [`task-ids-12-01-t03-rate-limit-dependency-429-envelope`](./task-ids-12-01-t03-rate-limit-dependency-429-envelope/README.md) | pkg-000035 |
| 4 | [`task-ids-12-01-t04-sensitive-routes-wiring`](./task-ids-12-01-t04-sensitive-routes-wiring/README.md) | pkg-000035 |
| 5 | [`task-ids-12-01-t05-otp-cooldown-coexistence-policy`](./task-ids-12-01-t05-otp-cooldown-coexistence-policy/README.md) | pkg-000035 |
| 6 | [`task-ids-12-01-t06-offline-rate-limit-tests`](./task-ids-12-01-t06-offline-rate-limit-tests/README.md) | pkg-000035 |
| 7 | [`task-ids-12-01-t07-story-acceptance-verification`](./task-ids-12-01-t07-story-acceptance-verification/README.md) | pkg-000035 |
