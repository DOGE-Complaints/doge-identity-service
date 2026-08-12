# STORY-IDS-PV-10 — File SMS sink: ловим OTP-тексты в файлы (dev-провайдер для ручного теста)

## Meta
- **Key:** `STORY-IDS-PV-10-file-sms-sink-dev`
- **Epic:** [`EPIC-IDS-PHONE`](EPIC-IDS-PHONE.md)
- **Status:** 🟢 Done
- **Тип:** провайдер (dev/testing-DX) · **не гейтит MVP** (боевой путь — Telnyx PV-06/07)
- **Источник:** [`sms-mock-testing-2026-06-28.md` — G-SMS-1](../../../analysis/sms-mock-testing-2026-06-28.md) (выбран файловый вариант sink); архитектура [`phone-verification-architecture-2026-06-10.md`](../../../analysis/phone-verification-architecture-2026-06-10.md)
- **Зависит от:** [PV-01](STORY-IDS-PV-01-phone-provider-backbone.md) (контракт `SmsSenderPort`), [PV-02](STORY-IDS-PV-02-provider-owned-config.md) (provider-owned config + выбор активного)

## Зачем простыми словами
В `mock`-режиме OTP-код **никуда не видно**: он оседает только в оперативной памяти отправителя ([`mock_sender.py:13`](../../../../src/core/phone/mock/mock_sender.py)), его читают автотесты в том же процессе, а в ответ/логи код намеренно не пишется. Для **ручного теста через фронт** код взять негде, а Telnyx тратит бюджет (см. [G-SMS-1](../../../analysis/sms-mock-testing-2026-06-28.md)).

Нужен **самый простой dev-приёмник**: новый SMS-провайдер `file`, который вместо реальной отправки **дописывает текст SMS в файл на диске сервера — один файл на номер телефона, строками-логами с таймстемпами**. Тестировщик включает `SMS_PROVIDER=file` и читает коды через `tail -f <outbox>/<номер>.log`. Бюджет не тратится, сети нет.

## Целевое поведение (пример)
```
# .env
SMS_PROVIDER=file
FILE_SMS_OUTBOX_DIR=var/sms-outbox

# после двух POST /auth/phone/request на +37255555555:
$ cat var/sms-outbox/+37255555555.log
2026-06-28T10:01:02Z	Your Dogestonia verification code is 482913.
2026-06-28T10:03:40Z	Your Dogestonia verification code is 105774.

# ручной тест в реальном времени:
$ tail -f var/sms-outbox/+37255555555.log
```

## Scope
- **`FileSmsSender`** (`src/core/phone/file/file_sender.py`): `provider_name="file"`; `send(*, to_e164, text)` — **append** строки `{utc_iso}\t{text}\n` в `<outbox_dir>/<sanitized(to_e164)>.log` (create-if-missing, UTF-8). Возврат `SmsSendResult(provider_message_id=f"file-{uuid4()}", accepted=True)`. На ошибке записи (нет прав/каталога) — `SmsSenderError(code=SmsErrorCode.SEND_FAILED)`.
  - **Санитайз имени файла:** оставить только `[+0-9]` из `to_e164` (номер уже нормализован ядром в E.164 на этапе PV-03/05); никаких `/`, `..` — защита от path-traversal.
  - **Таймстемп:** UTC ISO-8601 (в стиле `_format_utc_iso`/`_utcnow` из ядра) — чтобы строки были упорядочены и читаемы.
- **Provider-owned config** (`src/core/phone/file/config.py` + `config_spec`): `FILE_SMS_OUTBOX_DIR` — **optional**, default `var/sms-outbox` (относительно cwd). Через `SmsProviderConfigSpec` ([`config_spec.py`](../../../../src/core/phone/config_spec.py)), как у telnyx, но **без required** полей.
- **Дескриптор `file`** + регистрация в `ALL_SMS_PROVIDER_DESCRIPTORS` ([`registry_builder.py:9-12`](../../../../src/core/phone/registry_builder.py)); `SMS_PROVIDER=file` → `get_active()` отдаёт `FileSmsSender`.
- **Без сети:** расширить `_needs_sms_http_client` ([`runtime_factory.py:14-15`](../../../../src/core/phone/runtime_factory.py)) — `file`, как и `mock`, **не** поднимает `httpx.Client`.
- **Demo-only fail-fast (анти-leak):** при `APP_PROFILE=pilot` **и** `SMS_PROVIDER=file` → `ConfigError` («plaintext OTP на диск запрещён в pilot»). Встроить в profile-валидацию ([`schema.py:180-194`](../../../../src/core/config/schema.py)) или рядом с `_validate_active_sms_provider_config` ([`schema.py:116-119,170-178`](../../../../src/core/config/schema.py)).
- **Гигиена секретов:** outbox-каталог в `.gitignore`; в `.env.example` — обновить коммент `SMS_PROVIDER=… # mock | file | telnyx` и добавить `FILE_SMS_OUTBOX_DIR` с предупреждением «dev-only: пишет plaintext OTP на диск; никогда в prod/pilot».
- **Тесты (offline):** append двух SMS на один номер → 2 строки, таймстемпы по возрастанию; разные номера → разные файлы; санитайз имени; `APP_PROFILE=pilot`+`file` → `ConfigError`; e2e-флоу `POST /auth/phone/request` при `SMS_PROVIDER=file` создаёт файл с кодом; `file` не создаёт http-клиент.

## Вне scope
- **Ротация/чистка/TTL** файлов outbox — не нужно для dev (чистить вручную `rm`).
- **HTTP-эндпоинт** чтения кодов (`GET /dev/last-otp`) — это альтернативный вариант G-SMS-1 №2; здесь выбран файловый, эндпоинт не делаем.
- Изменения `mock`/`telnyx` отправителей — **не трогаем** (mock остаётся для автотестов).
- Реальная доставка SMS и webhooks — Telnyx [PV-06](STORY-IDS-PV-06-telnyx-sms-sender.md)/[PV-07](STORY-IDS-PV-07-telnyx-delivery-webhook.md).
- Маскирование/хеширование номера в имени файла — намеренно нет (это dev-инструмент, читаемость важнее; и поэтому demo-only).

## Точки в коде (образцы + швы)
- Шаблон отправителя (in-memory → файловый аналог): [`mock_sender.py:9-25`](../../../../src/core/phone/mock/mock_sender.py).
- Шаблон дескриптора без обязательной конфигурации: [`mock/descriptor.py:9-24`](../../../../src/core/phone/mock/descriptor.py); провайдер с config-spec — telnyx-дескриптор (см. [PV-06](STORY-IDS-PV-06-telnyx-sms-sender.md)). Реестр: [`registry_builder.py:9-38`](../../../../src/core/phone/registry_builder.py).
- Контракт порта/результата/ошибки: [`base.py:20-42`](../../../../src/core/phone/base.py) (`SmsSenderPort.send`, `SmsSendResult`, `SmsSenderError`, `SmsErrorCode.SEND_FAILED`).
- Текст с кодом формирует ядро: [`sms_text.py:4-5`](../../../../src/core/phone/sms_text.py); отправка из хендлера: [`handlers.py:494,504`](../../../../src/core/api/handlers.py).
- Выбор/валидация провайдера + pilot fail-fast: [`schema.py:170-194`](../../../../src/core/config/schema.py).
- Где не создаётся http-клиент: [`runtime_factory.py:14-15`](../../../../src/core/phone/runtime_factory.py).
- Конфиг-спека SMS-провайдера: [`config_spec.py`](../../../../src/core/phone/config_spec.py).
- Гэп, который закрывает стори: [`sms-mock-testing-2026-06-28.md` §4.3 G-SMS-1](../../../analysis/sms-mock-testing-2026-06-28.md).

## Acceptance Criteria
- [x] `SMS_PROVIDER=file` → `get_active()` возвращает `FileSmsSender`; `POST /auth/phone/request` дописывает строку `{utc-таймстемп}\t{текст с кодом}` в `<outbox>/<номер>.log`.
- [x] Повторные SMS на тот же номер — **append** (не перезапись); разные номера — разные файлы.
- [x] `tail -f <outbox>/<номер>.log` в ручном тесте показывает приходящие коды (DX-цель достигнута).
- [x] Имя файла санитизировано (только `+` и цифры); path-traversal невозможен.
- [x] `APP_PROFILE=pilot` + `SMS_PROVIDER=file` → `ConfigError` (demo-only анти-leak).
- [x] `file`-провайдер **не** создаёт `httpx.Client` (нет сети).
- [x] outbox-каталог в `.gitignore`; `.env.example` обновлён (значение `file` + `FILE_SMS_OUTBOX_DIR` + предупреждение).
- [x] Offline-тесты зелёные: `.venv/bin/python -m pytest -q -m "not live_integration"`.

## Парадигма-якорь
[`06-eid-providers`](../../../runtime-docs/06-eid-providers.md) (плагин-провайдеры), [`04-security`](../../../runtime-docs/04-security.md) (PII/секреты/анти-leak — поэтому demo-only), [`phone-verification-architecture-2026-06-10`](../../../analysis/phone-verification-architecture-2026-06-10.md).
