# STORY-IDS-SEC-01 — Per-user rate limiting + 429/`retry_after` для чувствительных роутов

## Meta
- **Key:** `STORY-IDS-SEC-01-rate-limiting`
- **Epic:** [`EPIC-IDS-SEC`](EPIC-IDS-SEC.md)
- **Status:** 🟢 Done (волна pkg-000035, 2026-06-26)
- **Остаток G-1:** [`STORY-IDS-SEC-01b-phone-request-http-rate-limit`](STORY-IDS-SEC-01b-phone-request-http-rate-limit.md) (`POST /auth/phone/request` HTTP rate-limit)
- **Split-analysis:** [`sec-01-g1-rate-limit-split-2026-06-26.md`](../../../analysis/sec-01-g1-rate-limit-split-2026-06-26.md)
- **Источник:** [`full-audit §3`](../../../analysis/identity-backend-full-audit-2026-06-24.md) — гэп **G-1** (HIGH)
- **Зависит от:** —

## Зачем простыми словами
Сейчас нет **никакой** защиты от частых повторных запросов: один JWT может сколько угодно раз дёргать «начать eID» или «прислать SMS-код». Единственное ограничение, что есть, — это пауза между двумя SMS подряд (cooldown), и она возвращает не тот ответ, который требует спека. Цель стори — на уровне **требований** зафиксировать: какие роуты считаем чувствительными, сколько запросов на пользователя за окно разрешаем, и как именно отвечаем при превышении (HTTP 429 + «через сколько секунд можно повторить»). Это анти-абьюз и защита от лишних трат на SMS/eID.

## Scope (только требования)
- **Определить набор чувствительных роутов** и лимит на каждый (per-user; для callback-роутов возможно per-ip). Источник целевых значений — [`16:38-53`](../../../requirements/16-security-privacy-observability.md) (таблица `RATE_LIMITS`) и [`11:127-130`](../../../requirements/11-eid-verification-flow.md):
  - `POST /auth/eid/start` — 5 запросов / 10 минут / пользователь — **доставлено** (pkg-000035);
  - `GET /auth/{provider}/callback` — 5 запросов / 10 минут / IP — **доставлено** (pkg-000035);
  - `POST /auth/phone/request` — **вынесен в [SEC-01b](STORY-IDS-SEC-01b-phone-request-http-rate-limit.md)** (не доставлено волной pkg-000035; cooldown `PHONE_RESEND_COOLDOWN_S` остаётся доменным 400);
  - прочие чувствительные роуты из `RATE_LIMITS` (gateway-only `/stories`, `/gpt/...`) — reference-only для identity.
- **Контракт ответа при превышении:** HTTP `429` с конвертом, включающим `retry_after` (секунды до следующего разрешённого запроса), по форме [`16:48-53`](../../../requirements/16-security-privacy-observability.md). Согласовать код ошибки в `{error}`-конверте с существующим envelope-контрактом сервиса.
- **Где enforce'ится:** сквозной слой `rate_limit_dependency` (FastAPI Depends) **до** бизнес-логики хендлера. Стор — in-memory (pkg-000035); Redis — deployment follow-up.
- **Согласование с OTP-cooldown:** cooldown ([`handlers.py:458-473`](../../../../src/core/api/handlers.py)) остаётся доменным `SmsSenderError(RATE_LIMITED)` → HTTP 400; HTTP 429 не дублирует cooldown на `phone/request`.
- **Конфигурируемость:** лимиты задаются `RATE_LIMIT_*` env ([`schema.py`](../../../../src/core/config/schema.py)).

## Вне scope
- `POST /auth/phone/request` HTTP rate-limit — [SEC-01b](STORY-IDS-SEC-01b-phone-request-http-rate-limit.md).
- Rate-limit для gateway-only роутов из таблицы 16.
- Durable phone-сессии (G-3) и durable phone-аудит — другие стори.

## Точки в коде (as-built, pkg-000035)
- **Конфиг:** [`rate_limit_config.py`](../../../../src/core/security/rate_limit_config.py), env `RATE_LIMIT_*` в [`schema.py`](../../../../src/core/config/schema.py).
- **Стор + sliding window:** [`rate_limit.py`](../../../../src/core/security/rate_limit.py).
- **Dependency + IP resolution:** [`rate_limit_dependency.py`](../../../../src/core/api/rate_limit_dependency.py) (`TRUSTED_PROXY_COUNT` для callback IP — audit F2, override t09).
- **Wiring:** [`asgi_app.py`](../../../../src/core/api/asgi_app.py) — `Depends(require_eid_start_rate_limit)` на `POST /auth/eid/start`, `Depends(require_callback_rate_limit)` на `GET /auth/{provider}/callback`.
- **429 envelope:** [`envelope.py`](../../../../src/core/api/envelope.py) `build_rate_limit_envelope`.
- **OTP-cooldown (не HTTP 429):** [`handlers.py:456-473`](../../../../src/core/api/handlers.py).
- **Тесты:** [`test_rate_limiting.py`](../../../../tests/test_rate_limiting.py).

## Acceptance Criteria
- [x] Зафиксирован перечень чувствительных identity-роутов с лимитом (requests/window/scope) на каждый; значения для `/auth/eid/start` = 5/10мин/user соответствуют [`11:129`](../../../requirements/11-eid-verification-flow.md) и [`16:38-53`](../../../requirements/16-security-privacy-observability.md).
- [x] При превышении лимита роут отвечает HTTP `429` с `retry_after` (секунды) в конверте ошибки; форма ответа согласована с envelope-контрактом сервиса.
- [x] Лимит применяется до бизнес-логики хендлера (сквозной слой), а не индивидуально внутри каждого хендлера — зафиксировано как требование.
- [x] Описано непротиворечивое сосуществование с OTP-cooldown (`PHONE_RESEND_COOLDOWN_S`): cooldown остаётся доменной ошибкой 400; HTTP 429 на eid/start и callback.
- [x] Лимиты и окна задаются конфигом; тест демонстрирует 429+`retry_after` на N+1-м запросе в окне для хотя бы одного роута.
- [ ] (Альтернатива DEFERRED) — не выбрана оператором.

## Парадигма-якорь
[`16-security-privacy-observability.md`](../../../requirements/16-security-privacy-observability.md) (Rate Limiting + 429/`retry_after`), [`11-eid-verification-flow.md`](../../../requirements/11-eid-verification-flow.md) (eID-start лимит), [`runtime-docs/04-security.md`](../../../runtime-docs/04-security.md) (anti-abuse).
