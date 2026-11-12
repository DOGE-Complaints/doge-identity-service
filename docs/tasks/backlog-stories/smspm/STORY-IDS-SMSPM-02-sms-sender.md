# STORY-IDS-SMSPM-02 — SMSPM SMS sender (доставка OTP)

## Meta
- **Key:** `STORY-IDS-SMSPM-02-sms-sender`
- **Epic:** [`EPIC-IDS-SMSPM`](EPIC-IDS-SMSPM.md) (D-G1, D-G4, D-G5)
- **Status:** 🟢 Done
- **Источник:** [`solution-architecture-smspm-sms-provider.md`](solution-architecture-smspm-sms-provider.md) §4, §6; inbound guide
- **Зависит от:** [SMSPM-01](STORY-IDS-SMSPM-01-provider-config-registry.md); live — после [SPIKE-01](SPIKE-IDS-SMSPM-01-account-sender-setup.md)

## Зачем простыми словами
Когда пользователь запрашивает код, identity должен **реально отправить SMS** через SMSPM. Ядро по-прежнему генерирует OTP и хранит только хэши; адаптер только доставляет готовый текст на номер.

## Scope (outcome)
- При `SMS_PROVIDER=smspm` путь `/auth/phone/request` → `SmsSenderPort.send` → SMSPM POST.
- Успех → `SmsSendResult(accepted=True, provider_message_id=…)`; id в сессии как у Telnyx.
- Ошибки → существующие `SmsErrorCode`; без утечки hash/token/OTP/full MSISDN в логи.
- Offline-тесты с mock HTTP; live skip-without-creds.

## Decisions

| ID | Решение | Почему |
|----|---------|--------|
| **D-02-1** | Success = HTTP 200 + `messages[0].id` (status `"Added to queue"` ok) | Guide response shape; очередь ≠ delivery fail |
| **D-02-2** | Map: 401→`SEND_FAILED`; invalid phone string→`INVALID_PHONE`; 5xx/timeout→`PROVIDER_UNAVAILABLE`; else `SEND_FAILED`/`UNKNOWN` | SA §6; не раскрывать auth клиенту |
| **D-02-3** | `toNumber` = E.164 **без** `+` только в sender (D-G4) | Guide; ядро/HMAC остаются на `+372…` |
| **D-02-4** | Auth: `hash`+`token` в JSON body (D-G5) | Guide; не Bearer |
| **D-02-5** | MVP **без** `report` URL — добавляет [SMSPM-04](STORY-IDS-SMSPM-04-delivery-report-webhook.md) | Не блокировать OTP delivery на webhook |
| **D-02-6** | Optional `smsId` = phone session id (рекомендуем **да**) | Связываемость логов без PII (message id ↔ session) |
| **D-02-7** | Не логировать token/hash/OTP/full MSISDN | GDPR custody + security |

## Паттерн (зеркало)

| Что | Якорь |
|-----|-------|
| Port | [`base.py`](../../../../src/core/phone/base.py) `SmsSenderPort` / `SmsSendResult` / `SmsErrorCode` |
| Sender | [`telnyx/sender.py`](../../../../src/core/phone/telnyx/sender.py) `TelnyxSmsSender.send` |
| Errors | [`telnyx/errors.py`](../../../../src/core/phone/telnyx/errors.py) |
| Descriptor `build` | [`telnyx/descriptor.py`](../../../../src/core/phone/telnyx/descriptor.py) |
| OTP ownership | [`otp_engine.py`](../../../../src/core/phone/otp_engine.py) — не трогать |
| Product analog | [STORY-IDS-PV-06](../phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md) |

## Подзадачи

- **T01 — `SmspmSmsSender.send`.** POST JSON (`hash`, `token`, `toNumber` strip `+`, `fromNumber`, `text`, optional `smsId`); parse `messages[0].id` → `provider_message_id`.
- **T02 — `errors.py`.** Mapping D-02-2 + timeout → `PROVIDER_UNAVAILABLE`.
- **T03 — Wire.** Descriptor `build` + runtime `httpx.Client` (уже через `_needs_sms_http_client`).
- **T04 — Offline tests.** success; 401; invalid phone; 5xx; missing id; assert no secrets/OTP/full MSISDN in log capture.
- **T05 — Live test.** Marker + skip-without-creds; проходит после SPIKE.

## Точки в коде (куда внедрять)

| Файл | Действие |
|------|----------|
| `src/core/phone/smspm/sender.py` | **new** — send |
| `src/core/phone/smspm/errors.py` | **new** — map |
| `src/core/phone/smspm/descriptor.py` | `build` → `SmspmSmsSender` |
| `src/core/phone/smspm/config.py` | settings из SMSPM-01 |
| `tests/…` (зеркало telnyx sender tests) | T04–T05 |

## Вне scope
- Регистрация/config — [SMSPM-01](STORY-IDS-SMSPM-01-provider-config-registry.md).
- Операторский runbook — [SMSPM-03](STORY-IDS-SMSPM-03-operator-runbook-smoke.md).
- Webhook / `report` URL — [SMSPM-04](STORY-IDS-SMSPM-04-delivery-report-webhook.md).
- Замена OTP-движка / SMSPM Verify API (D-G1).

## Acceptance Criteria
- [x] При `SMS_PROVIDER=smspm` и валидных creds `POST /auth/phone/request` доставляет SMS через SMSPM; ответ клиенту без кода.
- [x] При успехе (D-02-1) provider message id сохраняется в phone-сессии.
- [x] Ошибки мапятся по D-02-2; секреты/OTP/full MSISDN не в логах (D-02-7).
- [x] Offline-тесты (T04) зелёные; live (T05) skip без creds и проходит после SPIKE.
- [x] `SMS_PROVIDER=mock|file|telnyx` без регрессий; MVP без `report` (D-02-5).

## Парадигма-якорь
[EPIC-IDS-SMSPM](EPIC-IDS-SMSPM.md); [solution-architecture-smspm-sms-provider.md](solution-architecture-smspm-sms-provider.md); [STORY-IDS-PV-06](../phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md).
