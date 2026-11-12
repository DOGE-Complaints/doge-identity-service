# 11. SMS-провайдеры и OTP-доставка

## О чём этот документ

Телефонная верификация в identity — это **два слоя**. Ядро генерирует OTP, хранит только HMAC, считает TTL/попытки/cooldown. Отдельный **разъём** (`SmsSenderPort`) доставляет уже готовый текст SMS. Этот документ — as-built карта разъёма и провайдера **SMSPM** (архитектура, `.env`, аккаунт, как тестировать).

OTP / PII / окна plaintext — [10-phone-personal-data-processing](10-phone-personal-data-processing.md). HTTP-маршруты — [01-api](01-api.md) и [API_REFERENCE](api-reference/API_REFERENCE.md). Операторский how-to (mock / Telnyx / SMSPM curl) — [phone-sms-verification.md](../runbook/phone-sms-verification.md).

Источник: [`src/core/phone/`](../../src/core/phone/), переключатель — `SMS_PROVIDER` в [`schema.py:168-176`](../../src/core/config/schema.py).

---

## OTP vs delivery (общее) ✅

Identity **не** использует SMSPM (или Telnyx) как «verify API». Подтверждение кода — локальное сравнение HMAC в [`otp_engine.py`](../../src/core/phone/otp_engine.py) через `POST /auth/phone/confirm` ([`handlers.py:539-637`](../../src/core/api/handlers.py)). Статус доставки SMS **не** гейтит confirm.

Путь запроса кода ([`handlers.py:496-509`](../../src/core/api/handlers.py)):

```
POST /auth/phone/request (Bearer JWT)
  → normalize E.164 + prefix allowlist
  → create_phone_verification_session (phone_hash / code_hash в БД)
  → registry.get_active(config).send(to_e164, text)
  → store provider_message_id, если отправитель его вернул
```

Текст SMS: [`sms_text.py:4-5`](../../src/core/phone/sms_text.py) — `Your Dogestonia verification code is {code}.` Код **не** в HTTP-ответе и не в audit.

---

## «Разъём» отправителя (порт) ✅

`SmsSenderPort` ([`base.py:38-42`](../../src/core/phone/base.py)):

- `provider_name` — provenance в сессии/профиле (`smspm`, `telnyx`, …);
- `send(*, to_e164, text) -> SmsSendResult` — `accepted` + optional `provider_message_id`.

Ошибки — `SmsSenderError` с каноническим `SmsErrorCode` ([`base.py:8-17`](../../src/core/phone/base.py)): среди прочих `INVALID_PHONE`, `PROVIDER_UNAVAILABLE`, `SEND_FAILED`.

---

## Реестр и выбор активного ✅

Дескрипторы: `ALL_SMS_PROVIDER_DESCRIPTORS` ([`registry_builder.py:11-16`](../../src/core/phone/registry_builder.py)) — `mock`, `file`, `telnyx`, `smspm`.

`SMS_PROVIDER` должен входить в `registered_sms_provider_names()`; иначе `ConfigError` на старте ([`schema.py:168-174`](../../src/core/config/schema.py)). Required-поля активного провайдера валидируются через `descriptor.config_spec.validate` (`_validate_active_sms_provider_config`).

Сборка: `build_sms_registry` регистрирует **`mock` + активное имя** ([`registry_builder.py:29-42`](../../src/core/phone/registry_builder.py)). `get_active(config)` — [`registry.py:24-25`](../../src/core/phone/registry.py).

`SMS_PROVIDER=file` **запрещён** при `APP_PROFILE=pilot` ([`schema.py:178-181`](../../src/core/config/schema.py)).

---

## Какие провайдеры есть

| Провайдер | Статус | Где | Когда |
|-----------|--------|-----|--------|
| `mock` | ✅ default | [`mock/mock_sender.py`](../../src/core/phone/mock/mock_sender.py) | автотесты; код снаружи не виден |
| `file` | ✅ demo-only | [`file/file_sender.py`](../../src/core/phone/file/file_sender.py) | ручной локальный OTP (`var/sms-outbox/`) |
| `telnyx` | ✅ live | [`telnyx/sender.py`](../../src/core/phone/telnyx/sender.py) | Bearer + Ed25519 webhook |
| `smspm` | ✅ live | [`smspm/sender.py`](../../src/core/phone/smspm/sender.py) | POST JSON hash/token; GET webhook + path-secret |

How-to без реального провайдера: [sms-mock-testing.md](../runbook/sms-mock-testing.md).

---

## SMSPM as-built

### Send ✅

[`SmspmSmsSender.send`](../../src/core/phone/smspm/sender.py): `POST` на `SMSPM_API_BASE_URL` (default `https://api.smspm.com`), `Content-Type: application/json`. **Нет** `Authorization: Bearer`.

Тело:

- `hash`, `token`, `fromNumber` — из env;
- `toNumber` = E.164 **без** `+` ([`sender.py:23`](../../src/core/phone/smspm/sender.py)); ядро/HMAC остаются на `+372…`;
- `text` — готовая строка от ядра;
- `report` — только если set `SMSPM_REPORT_URL` ([`sender.py:29-30`](../../src/core/phone/smspm/sender.py));
- `smsId` — поле отправителя есть ([`sender.py:27-28`](../../src/core/phone/smspm/sender.py)); **handler его не передаёт** (`send(to_e164, text)` в [`handlers.py:506`](../../src/core/api/handlers.py)). Optional, не wired — [STORY-IDS-SMSPM-05](../tasks/backlog-stories/smspm/STORY-IDS-SMSPM-05-smsid-session-wire.md).

Успех = HTTP 200 + `messages[0].id` → `SmsSendResult(accepted=True, provider_message_id=…)`. Статус `"Added to queue"` — очередь, не факт доставки.

Маппинг ошибок ([`errors.py:25-49`](../../src/core/phone/smspm/errors.py)): 401 → `SEND_FAILED`; «invalid phone» → `INVALID_PHONE`; 5xx / timeout → `PROVIDER_UNAVAILABLE`; прочий 4xx → `SEND_FAILED`. В warning-логах нет hash/token/OTP/полного MSISDN.

### Delivery webhook ✅

`GET /webhooks/smspm/delivery/{shared_secret}` ([`asgi_app.py:411-423`](../../src/core/api/asgi_app.py)) → [`handle_smspm_delivery_webhook`](../../src/core/api/handlers.py) (`:759-837`).

- Auth: `secrets.compare_digest` path vs `SMSPM_WEBHOOK_SHARED_SECRET` — **не** Ed25519 Telnyx.
- Нет секрета → 503 `CONFIG_ERROR`; mismatch → 401; успех → plain `200` body `OK` (`text/plain`).
- Query: `id` + `status`; `toNumber` **не** пишется ([`delivery_ingest.py:28-46`](../../src/core/phone/smspm/delivery_ingest.py)). Map: `queued`→`queued`, `submitted`/`sent`→`sent`, `delivered`, `failed`. Forward-only ingest по `provider_message_id`.
- Audit: `smspm_delivery_status_updated`, без plaintext phone/OTP.

На OTP-confirm **не влияет**.

### Чего в identity нет (vendor guide ≠ as-built)

В коде **нет** клиентов `/smsdetails` (polling), `/balance`, `/sender-ids`, GET-send, bulk-100. Их не описывать как поведение identity. Для проверки creds без пользователя — прямой curl к SMSPM (runbook §6C0).

---

## Настройка `.env`

Имена — [`.env.example:80-87`](../../.env.example). **Значения секретов в git и в этой доке не класть.**

| Переменная | Обязательна при `SMS_PROVIDER=smspm` | Назначение |
|------------|--------------------------------------|------------|
| `SMS_PROVIDER=smspm` | да (выбор) | активный дескриптор |
| `SMSPM_HASH` | да ([`config.py:12`](../../src/core/phone/smspm/config.py)) | API hash аккаунта |
| `SMSPM_TOKEN` | да | API token |
| `SMSPM_FROM` | да | approved sender ID |
| `SMSPM_API_BASE_URL` | нет (default `https://api.smspm.com`) | base send |
| `SMSPM_WEBHOOK_SHARED_SECRET` | нет (не в `SMSPM_REQUIRED_ENV`) | path-secret webhook; без него callback → 503 |
| `SMSPM_REPORT_URL` | нет | URL, который уходит как send `report` |
| `SMSPM_TEST_PHONE` | нет (только live-smoke) | тестовый E.164 для прямой отправки без JWT |

Пустые HASH/TOKEN/FROM при `SMS_PROVIDER=smspm` → `ConfigError` на старте, сервис не поднимается.

Пример `SMSPM_REPORT_URL`: `https://<public-api>/webhooks/smspm/delivery/<shared-secret>` (тот же secret, что в path).

Ядро OTP (любой провайдер): `PHONE_ALLOWED_DIAL_PREFIXES`, `PHONE_CODE_*`, `PHONE_RESEND_COOLDOWN_S`, `PHONE_ONE_ACCOUNT_PER_NUMBER` — [`.env.example:61-66`](../../.env.example).

---

## Требования к аккаунту SMSPM

Внешний SPIKE (оператор, не код): [SPIKE-IDS-SMSPM-01](../tasks/backlog-stories/smspm/SPIKE-IDS-SMSPM-01-account-sender-setup.md). API-детали вендора: [SMSPM_SMS_Delivery_Integration_Guide.md](../tasks/backlog-stories/inbound/SMSPM_SMS_Delivery_Integration_Guide.md) § Authentication / Sender ID.

Чеклист (без секретов в git):

1. Аккаунт и dashboard `https://app.smspm.com`.
2. **Hash** + **token** (token — секрет; Railway / 1Password).
3. **Sender ID** pre-approved (цель бренда `DOGEstonia`; dashboard default только для smoke + risk-note).
4. Эстония / целевые операторы reachable с этого аккаунта.
5. Согласованный тестовый MSISDN `+372…` (`SMSPM_TEST_PHONE`).
6. Публичный HTTPS identity, если нужны callbacks (`SMSPM_WEBHOOK_SHARED_SECRET` + `SMSPM_REPORT_URL`).

SPIKE-01 на диске **⚪ Todo** — live-отправка BLOCKED, пока creds/sender/номер не заведены.

---

## Как тестировать

| Режим | Что проверяет | JWT / пользователь | Команда / якорь |
|-------|---------------|--------------------|-----------------|
| **Offline** | адаптер, config, webhook parse, реестр | нет | `pytest -q -m "not live_integration"`; `tests/test_smspm_*.py` |
| **Прямой live (C0)** | creds + sender + EE доставка **без** OTP-сессии | нет | runbook [§6C0](../runbook/phone-sms-verification.md); `pytest -m live_integration` + `SMSPM_HASH/TOKEN/FROM/TEST_PHONE` |
| **Полный OTP (C)** | request → SMS → confirm → `phone_verified` | да, Bearer | runbook §6C |

Прямой live **не** создаёт `phone_verification_sessions` / не трогает `profiles`. Текст — фиксированный smoke, не OTP из ядра.

Полный OTP требует JWT и идёт через `/auth/phone/*` — это продуктовый путь, не проверка «просто интеграции».

---

## Как добавить ещё одного SMS-провайдера

1. Пакет по образцу `telnyx/` / `smspm/`: `config` + `descriptor` + `sender` + `errors`.
2. Класс по `SmsSenderPort`; `SmsProviderDescriptor` в `ALL_SMS_PROVIDER_DESCRIPTORS`.
3. Fail-fast через `config_spec` при активном `SMS_PROVIDER`.
4. Delivery webhook — **новый маршрут**, если вендор не вписывается в существующий Telnyx POST / SMSPM GET (в отличие от eID: там один `GET /auth/{provider}/callback`).
