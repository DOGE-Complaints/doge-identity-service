# STORY-IDS-PV-06 — Telnyx SMS sender: адаптер + регистрация + тесты

## Meta
- **Key:** `STORY-IDS-PV-06-telnyx-sms-sender`
- **Epic:** `EPIC-IDS-PHONE`
- **Status:** 🟢 Done
- **Источник:** спека [`telnyx-integration-spec-dogestonia-2026-06-10.md`](../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md); архитектура §10
- **Pipeline (исполнение):** [`STORY-IDS-PV-06-telnyx-sms-sender`](../../epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-06-telnyx-sms-sender/STORY-IDS-PV-06-telnyx-sms-sender.md) · pkg-000027
- **Зависит от:** [PV-01](STORY-IDS-PV-01-phone-provider-backbone.md), [PV-02](STORY-IDS-PV-02-provider-owned-config.md), [PV-05](STORY-IDS-PV-05-verification-flow-api.md) (для e2e); live-тест — после [SPIKE-PV-08](SPIKE-IDS-PV-08-telnyx-account-setup.md)

## Зачем простыми словами
Первый боевой провайдер: класс, который реально отправляет SMS через Telnyx (Messaging API). Тонкий — только доставка; всё про OTP уже в ядре. Спека Telnyx уже готова, реализуем строго по ней.

## Scope
- **`TelnyxSettings` + `config_spec`** (`providers/.../telnyx/config.py`): `TELNYX_API_KEY` (required), `TELNYX_API_BASE_URL=https://api.telnyx.com`, `TELNYX_FROM=DOGEstonia`, `TELNYX_MESSAGING_PROFILE_ID`, optional `TELNYX_MESSAGE_TYPE=SMS`/`TELNYX_ENCODING=auto`. **Условная валидация:** буквенный `TELNYX_FROM` (не E.164) → `TELNYX_MESSAGING_PROFILE_ID` обязателен.
- **`TelnyxSmsSender.send(to_e164, text)`:** `POST {base}/v2/messages` с Bearer-auth, тело `{from, to, text, type:"SMS", messaging_profile_id?}`; успех = HTTP 200 + `data.id` + `data.to[0].status ∈ {queued, sent}` → `SmsSendResult(provider_message_id=data.id, accepted=True)`.
- **Маппинг ошибок → `SmsErrorCode`** (по таблице §3 спеки): `40309/40331→COUNTRY_NOT_ALLOWED`; `429/10011/40318→RATE_LIMITED`; `5xx/timeout→PROVIDER_UNAVAILABLE`; невалидный номер→`INVALID_PHONE`; config/sender/content→`SEND_FAILED`; нет `data.id`/неизвестное→`UNKNOWN`. Бросать `SmsSenderError(code=...)`.
- **Дескриптор Telnyx** + регистрация в наборе SMS-дескрипторов; `SMS_PROVIDER=telnyx` → активен.
- **Тесты:** юнит на замоканном `httpx` (успех `queued`; `invalid_grant`-аналоги; 5xx; нет `data.id`→`UNKNOWN`; разбор `errors[].code/title/detail`; no-OTP-in-logs); live-тест против Telnyx trial (skip без creds).
- `.env.example`: блок `TELNYX_*`.

## Вне scope
- Приём статусов доставки (webhook) — [PV-07](STORY-IDS-PV-07-telnyx-delivery-webhook.md).
- `private_key_jwt`/Verify API — не наш путь (managed verify ломает тонкий порт).

## Точки в коде (образец + спека)
- Образец боевого провайдера (eID): структура `providers/authentigate/` (config+descriptor) [`authentigate/config.py`](../../../../src/core/providers/authentigate/config.py), [`authentigate/descriptor.py`](../../../../src/core/providers/authentigate/descriptor.py); реестр [`registry_builder.py`](../../../../src/core/providers/registry_builder.py).
- HTTP-клиент из рантайма (sync `httpx`): [`runtime_factory.py`](../../../../src/core/providers/runtime_factory.py).
- Канон ошибок: `SmsErrorCode` из [PV-01](STORY-IDS-PV-01-phone-provider-backbone.md).
- Спека Telnyx (endpoint/поля/ответ/ошибки/код-скетч): [`telnyx-integration-spec-dogestonia-2026-06-10.md`](../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md) §2, §3, §9.

## Acceptance Criteria
- [x] `SMS_PROVIDER=telnyx` (+ creds) → `get_active()` возвращает `TelnyxSmsSender`; без обязательных env / буквенный from без profile_id → понятная `ConfigError`.
- [x] `send` формирует корректный POST (Bearer, `from/to/text/type`, profile_id при буквенном from); 200+`queued` → `accepted=True` + `provider_message_id`.
- [x] Ошибки Telnyx замаплены в `SmsErrorCode` по таблице спеки; сырой код/номер не логируется.
- [x] Юнит-тесты offline (mocked httpx) зелёные; live-тест проходит против trial и **скипается** без creds.
- [x] `.env.example` содержит `TELNYX_*`.

## Парадигма-якорь
[06-eid-providers](../../../runtime-docs/06-eid-providers.md) (модульность), [04-security](../../../runtime-docs/04-security.md) (PII/секреты).
