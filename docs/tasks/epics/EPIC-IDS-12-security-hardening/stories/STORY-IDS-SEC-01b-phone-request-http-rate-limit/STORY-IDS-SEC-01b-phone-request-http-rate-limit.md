# STORY-IDS-SEC-01b — HTTP rate-limit на `POST /auth/phone/request` (follow-up G-1)

## Meta
- **Key:** `STORY-IDS-SEC-01b-phone-request-http-rate-limit`
- **Parent Epic:** [`../../EPIC-IDS-12-security-hardening.md`](../../EPIC-IDS-12-security-hardening.md)
- **Epic alias (код/backlog):** `EPIC-IDS-SEC` · [`EPIC-IDS-SEC`](../../../../backlog-stories/security-hardening/EPIC-IDS-SEC.md)
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md)
- **Decision Ref:** [`../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md); [`sec-01-g1-rate-limit-split-2026-06-26.md`](../../../../../analysis/sec-01-g1-rate-limit-split-2026-06-26.md)
- **Источник:** [`sec-01-g1-rate-limit-split-2026-06-26.md`](../../../../../analysis/sec-01-g1-rate-limit-split-2026-06-26.md) — остаток **G-1** после pkg-000035
- **Зависит от:** [STORY-IDS-SEC-01](../STORY-IDS-SEC-01-rate-limiting/STORY-IDS-SEC-01-rate-limiting.md) 🟢 (инфраструктура rate-limit)

## Зачем простыми словами
В первой волне SEC-01 мы включили HTTP-лимиты на eID-start и callback, но **намеренно не трогали** `POST /auth/phone/request`. Там уже есть OTP cooldown (пауза между SMS), и он отвечает **400**, а не **429**. Отдельная стори нужна, чтобы добавить **второй**, независимый слой — per-user лимит запросов за окно (как в spec 16 для чувствительных роутов) — **не ломая** cooldown и не смешивая семантику ошибок.

## Scope (только требования)
- Подключить `POST /auth/phone/request` к сквозному HTTP rate-limit слою (тот же паттерн, что SEC-01: dependency до handler).
- Зафиксировать лимит requests/window/per-user и env-конфиг; **согласовать** с `PHONE_RESEND_COOLDOWN_S`, чтобы политики не противоречили (см. analysis §4).
- Политика: cooldown = доменный **400** `RATE_LIMITED`; превышение HTTP-окна = **429** `rate_limit_exceeded` + `retry_after`.
- Offline-тест: N+1 → 429; regression cooldown → 400.
- Обновить as-built: [`19-phone-verification-flow.md`](../../../../../requirements/19-phone-verification-flow.md), [`04-security.md`](../../../../../runtime-docs/04-security.md).

## Вне scope
- Замена OTP-cooldown на 429.
- Redis store, gateway `/stories`/`/gpt/...`.
- Изменение Telnyx provider 429 mapping.

## Точки в коде (текущее состояние)
- Роут без rate-limit Depends: [`asgi_app.py:344-358`](../../../../../../src/core/api/asgi_app.py).
- Cooldown: [`handlers.py:456-473`](../../../../../../src/core/api/handlers.py).
- Готовая инфраструктура SEC-01: [`rate_limit_config.py`](../../../../../../src/core/security/rate_limit_config.py), [`rate_limit_dependency.py`](../../../../../../src/core/api/rate_limit_dependency.py).

## Acceptance Criteria
- [x] `POST /auth/phone/request` wired на HTTP rate-limit (per-user); лимит и окно в конфиге.
- [x] При превышении HTTP-окна — 429 + `retry_after` в envelope; cooldown по-прежнему 400 без `retry_after`.
- [x] Политика сосуществования задокументирована (analysis + runtime-docs/spec 19).
- [x] Offline-тест демонстрирует оба сценария (429 window vs 400 cooldown).

## Парадигма-якорь
[`sec-01-g1-rate-limit-split-2026-06-26.md`](../../../../../analysis/sec-01-g1-rate-limit-split-2026-06-26.md), [`16-security-privacy-observability.md`](../../../../../requirements/16-security-privacy-observability.md), [`19-phone-verification-flow.md`](../../../../../requirements/19-phone-verification-flow.md).
