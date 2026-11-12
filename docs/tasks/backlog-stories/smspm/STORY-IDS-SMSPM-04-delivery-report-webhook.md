# STORY-IDS-SMSPM-04 — Delivery report / webhook (phase-2)

## Meta
- **Key:** `STORY-IDS-SMSPM-04-delivery-report-webhook`
- **Epic:** [`EPIC-IDS-SMSPM`](EPIC-IDS-SMSPM.md) (D-G6)
- **Status:** 🟢 Done
- **Источник:** [`solution-architecture-smspm-sms-provider.md`](solution-architecture-smspm-sms-provider.md) §4.4; inbound guide § Delivery reports
- **Зависит от:** [SMSPM-02](STORY-IDS-SMSPM-02-sms-sender.md)

## Зачем простыми словами
`send` говорит только «принято в очередь». Финальный статус «доставлено / failed» SMSPM может прислать позже. Это нужно для наблюдаемости, **не** для подтверждения OTP пользователем (код по-прежнему вводит человек).

## Scope (outcome)
- Принимать GET delivery callbacks SMSPM; обновлять `delivery_status` сессии по provider message id.
- Не влиять на `/auth/phone/confirm` и `phone_verified`.
- Идемпотентность forward-only (зеркало PV-07).
- При `SMSPM_REPORT_URL` — передавать `report` на send.
- Аудит без plaintext `toNumber`.

## Decisions

| ID | Решение | Почему |
|----|---------|--------|
| **D-04-1** | Endpoint `GET /webhooks/smspm/delivery/{shared_secret}` (или `?key=` эквивалент); mismatch → 401; ответ plain `200` body `OK` | Guide: GET query + `OK`; D-G6 — нет Ed25519 в SMSPM guide |
| **D-04-2** | Map SMSPM statuses → existing session `delivery_status` vocabulary (`queued`/`sent`/`delivered`/`failed`/…) | Переиспользовать store fields / [`CANONICAL_DELIVERY_STATUSES`](../../../../src/core/phone/telnyx/delivery_ingest.py); не плодить вторую схему |
| **D-04-3** | Idempotent **forward-only** updates (mirror PV-07 rank) | Повторные/устаревшие callbacks не откатывают статус |
| **D-04-4** | Если `SMSPM_REPORT_URL` set — передавать `report` на send (URL с secret path от public API base) | Guide optional `report`; без env — поведение MVP SMSPM-02 |
| **D-04-5** | **Не** gate confirm по delivery | Тот же posture, что Telnyx webhook |
| **D-04-6** | Audit: omit plaintext phone; store message id + status (hash optional — prefer omit) | GDPR; query `toNumber` от SMSPM не писать в audit plaintext |
| **D-04-7** | Env: `SMSPM_WEBHOOK_SHARED_SECRET` + `SMSPM_REPORT_URL` (optional until phase-2 live) | Auth path + outbound report URL |

## Паттерн (зеркало)

| Что | Якорь |
|-----|-------|
| Route | [`asgi_app.py`](../../../../src/core/api/asgi_app.py) `POST /webhooks/telnyx/messaging` — **формат GET + secret path** отличается (D-G6) |
| Handler | [`handlers.py`](../../../../src/core/api/handlers.py) `handle_telnyx_messaging_webhook` |
| Ingest / ranks | [`telnyx/delivery_ingest.py`](../../../../src/core/phone/telnyx/delivery_ingest.py) |
| Product analog | [STORY-IDS-PV-07](../phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md) |
| Guide callback | inbound guide: `GET …?id=…&status=…&toNumber=…` → respond `OK` |

## Подзадачи

- **T01 — Route + handler.** `GET /webhooks/smspm/delivery/{shared_secret}`; reject 401 on secret mismatch; body `OK`.
- **T02 — Parse query.** `id`, `status` (+ ignore/omit storing `toNumber` plaintext).
- **T03 — Update session.** Map status (D-04-2); forward-only (D-04-3) по `provider_message_id`.
- **T04 — Audit.** Event without phone plaintext (D-04-6).
- **T05 — Sender `report`.** Если `SMSPM_REPORT_URL` set — включать в POST send (D-04-4).
- **T06 — Offline tests.** Happy-path status update; 401 bad secret; idempotent replay; confirm path unchanged.
- **T07 — Env.** Document `SMSPM_WEBHOOK_SHARED_SECRET`, `SMSPM_REPORT_URL` in `.env.example` / runbook pointer.

## Точки в коде (куда внедрять)

| Файл | Действие |
|------|----------|
| `src/core/api/asgi_app.py` | route GET webhook |
| `src/core/api/handlers.py` | handler |
| `src/core/phone/smspm/delivery_ingest.py` (или аналог) | **new** — parse/map/update |
| `src/core/phone/smspm/sender.py` | optional `report` field |
| `src/core/phone/smspm/config.py` | secret + report URL settings |
| `tests/…` | T06 |

## Вне scope
- Сама отправка SMS без webhook — [SMSPM-02](STORY-IDS-SMSPM-02-sms-sender.md).
- Авто-ретраи отправки при `failed`.
- Gate верификации по delivery status (D-04-5).
- Ed25519 / Telnyx-style signature (не в SMSPM guide).

## Acceptance Criteria
- [x] Статусы доставки обновляются по provider message id без изменения OTP-confirm флоу (D-04-5).
- [x] Endpoint отвечает `OK` при валидном secret; 401 при mismatch (D-04-1).
- [x] Повторные/устаревшие события идемпотентны forward-only (D-04-3).
- [x] Аудит без сырого номера/OTP (D-04-6).
- [x] При set `SMSPM_REPORT_URL` sender передаёт `report` (D-04-4).
- [x] Offline-тесты T06 зелёные; env задокументированы (T07).

## Парадигма-якорь
[EPIC-IDS-SMSPM](EPIC-IDS-SMSPM.md) D-G6; [solution-architecture-smspm-sms-provider.md](solution-architecture-smspm-sms-provider.md) §4.4; [STORY-IDS-PV-07](../phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md).
