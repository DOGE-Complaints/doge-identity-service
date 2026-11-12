# Telnyx SMS-OTP: gap-анализ готовности + план включения (2026-07-10)

> **Задача:** (1) что фактически готово в коде для отправки OTP через Telnyx; (2) разбор присланного Verify-quickstart и план включения (SMS-канал), **без реализации**.
> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — claims по коду с `file:line`; Verify API — по [официальному quickstart](https://developers.telnyx.com/docs/identity/verify/quickstart).
> **Не дублирует:** архитектурную спеку [`telnyx-integration-spec-dogestonia-2026-06-10.md`](./telnyx-integration-spec-dogestonia-2026-06-10.md) и внешний спайк [`SPIKE-IDS-PV-08`](../tasks/backlog-stories/phone-verification/SPIKE-IDS-PV-08-telnyx-account-setup.md) — ссылается на них.

---

## 0. TL;DR + вердикт по сложности

- **Код готов на 100%** для отправки OTP через Telnyx **Messaging API** (`POST /v2/messages`). Провайдер `telnyx` построен, зарегистрирован, покрыт офлайн-тестами; delivery-webhook тоже есть (PV-06/PV-07 🟢 Done).
- **Включить = НЕ писать код**, а: настроить Telnyx-аккаунт/профиль (внешнее, SPIKE-08) + проставить 2 значения в `.env`. **Сложность кода — нулевая; сложность внешней настройки — низкая-средняя** (long-lead: Level-2 верификация аккаунта для буквенного отправителя `DOGEstonia`).
- **Присланный quickstart — это Verify API (другой продукт Telnyx)**, где Telnyx сам генерит и проверяет код. Наш код так **не** работает (у нас свой OTP-движок). Идти по Verify = выбросить готовое и переписать флоу. **Рекомендация: Messaging API (наш путь), Verify не брать** — это уже зафиксировано в спеке §1.
- **Единственный блокер включения сейчас:** `TELNYX_MESSAGING_PROFILE_ID` в `.env` **пуст**, а `TELNYX_FROM=DOGEstonia` (буквенный) требует профиль → при `SMS_PROVIDER=telnyx` сервис упадёт на валидации конфига.

---

## 1. Что уже построено (verified по коду 2026-07-10)

| Компонент | Где | Статус |
|-----------|-----|--------|
| SMS-отправитель Telnyx (`POST {base}/v2/messages`, Bearer, `from/to/text/type[/messaging_profile_id/encoding]`) | [`telnyx/sender.py:21-54`](../../src/core/phone/telnyx/sender.py) | ✅ |
| Разбор успеха (200 + `data.id` + `to[0].status ∈ {queued,sent}`) → `SmsSendResult` | [`sender.py:56-76`](../../src/core/phone/telnyx/sender.py) | ✅ |
| Конфиг `TelnyxSettings` + валидация (буквенный `from` → `messaging_profile_id` обязателен) | [`telnyx/config.py:25-58`](../../src/core/phone/telnyx/config.py) | ✅ |
| Маппинг ошибок Telnyx → `SmsErrorCode`; timeout | [`telnyx/errors.py`](../../src/core/phone/telnyx/errors.py) | ✅ |
| Дескриптор + регистрация (`SMS_PROVIDER=telnyx` → активный) | [`telnyx/descriptor.py`](../../src/core/phone/telnyx/descriptor.py), [`registry_builder.py`](../../src/core/phone/registry_builder.py) | ✅ |
| HTTP-клиент для telnyx (не mock/file) | [`runtime_factory.py:14-15`](../../src/core/phone/runtime_factory.py) | ✅ |
| Delivery-webhook `POST /webhooks/telnyx/messaging` + Ed25519-подпись + ingest статусов | [`asgi_app.py:395-403`](../../src/core/api/asgi_app.py), [`telnyx/webhook_signature.py`](../../src/core/phone/telnyx/webhook_signature.py), [`telnyx/delivery_ingest.py`](../../src/core/phone/telnyx/delivery_ingest.py) | ✅ (PV-07) |
| **OTP-движок наш** (генерация кода, `code_hash`, TTL, попытки, cooldown) — Telnyx только доставляет текст | [`phone/otp_engine.py`](../../src/core/phone/otp_engine.py), текст [`sms_text.py`](../../src/core/phone/sms_text.py) | ✅ |
| Офлайн-тесты (mocked httpx: успех/ошибки/no-`data.id`); live-тест скипается без creds | `tests/` (telnyx sender+webhook) | ✅ |

**Вывод:** отправка OTP по Telnyx — это уже работающий путь в коде. Не хватает только конфигурации/аккаунта.

---

## 2. Gap-анализ: что мешает включить сейчас

| ID | Severity | Гэп | Доказательство | Как закрыть |
|----|----------|-----|----------------|-------------|
| **G1** | 🔴 **блокер** | `TELNYX_MESSAGING_PROFILE_ID` **пуст** в `.env` (стр. 37), а `TELNYX_FROM=DOGEstonia` (буквенный) → `validate_telnyx_config` бросит `ConfigError` при старте с `SMS_PROVIDER=telnyx` | [`config.py:30-35`](../../src/core/phone/telnyx/config.py); `.env:36-37` (from set, profile empty) | Получить Messaging Profile ID из Telnyx-кабинета (SPIKE-08) → вписать в `.env` |
| **G2** | 🟠 | `SMS_PROVIDER` ≠ `telnyx` (сейчас эффективно `file`; в `.env` **две** строки `SMS_PROVIDER` — mock:25 и file:65) | `.env:25,65` | Поставить `SMS_PROVIDER=telnyx`; **убрать дубль** (config-гигиена, см. G6) |
| **G3** | 🟠 (внешнее) | Telnyx-аккаунт не настроен: Level-2 верификация (нужна для буквенного `DOGEstonia`), Messaging Profile, whitelist Эстонии (+372) | [`SPIKE-IDS-PV-08`](../tasks/backlog-stories/phone-verification/SPIKE-IDS-PV-08-telnyx-account-setup.md) ⚪ Todo | Выполнить SPIKE-08 (long-lead: верификация аккаунта) |
| **G4** | 🟡 | `TELNYX_WEBHOOK_PUBLIC_KEY` пуст (стр. 40). Endpoint `POST /webhooks/telnyx/messaging` **построен и публичен** ([`asgi_app.py:395`](../../src/core/api/asgi_app.py)), но при пустом ключе хендлер отвечает **503 CONFIG_ERROR** ([`handlers.py:660-667`](../../src/core/api/handlers.py)) → каждый callback Telnyx упадёт 503 | `.env:40` | Не блокирует **отправку** OTP (webhook = только статусы доставки). Если в профиле указан Webhook URL — **обязательно** задать `TELNYX_WEBHOOK_PUBLIC_KEY` (публичный ключ из Telnyx), иначе 503 |
| **G5** | 🟡 (trial) | Telnyx trial шлёт SMS **только на верифицированный тестовый номер** | Telnyx trial-ограничение (SPIKE-08 §Тестовый номер) | Верифицировать номер тестировщика ИЛИ пополнить аккаунт |
| **G6** | 🟢 (гигиена) | Дубли в `.env`: `SMS_PROVIDER` (25/65) и `PHONE_ALLOWED_DIAL_PREFIXES` (26/67) | `.env` | Оставить по одной строке каждой переменной (последняя выигрывает при dotenv-парсинге — легко ошибиться) |

**Ключевой факт:** `TELNYX_API_KEY` — **задан** в `.env` (стр. 34), как ты и сказала. То есть из 3 обязательных для буквенного отправителя (`API_KEY`, `FROM`, `MESSAGING_PROFILE_ID`) не хватает **только profile_id** (G1).

---

## 3. Присланный quickstart — это Verify API, не наш путь

Ты дала ссылку на **Telnyx Verify API** ([quickstart](https://developers.telnyx.com/docs/identity/verify/quickstart)). Это **другой продукт**, чем то, на чём построен наш код. Разница принципиальна:

| | **Messaging API** (наш код) | **Verify API** (quickstart) |
|---|---|---|
| Кто генерит OTP | **наше ядро** ([`otp_engine.py`](../../src/core/phone/otp_engine.py)) | **Telnyx** (managed) |
| Кто проверяет код | наше ядро (сверка `code_hash`) | **Telnyx** (`.../actions/verify`) |
| Endpoint отправки | `POST /v2/messages` (`from/to/text`) | `POST /v2/verifications/sms` (`phone_number`, `verify_profile_id`) |
| Настройка | Messaging Profile + sender ID | **Verify Profile** (`POST /v2/verify_profiles`) + шаблон |
| Контроль над кодом/текстом/TTL/попытками | **полный** (наш) | у Telnyx (шаблон/дефолт) |
| Наш контракт `SmsSenderPort.send(to, text)` | **совпадает** | **не совпадает** (verify ≠ «отправь текст») |

**Что было бы при переходе на Verify (для честности):** пришлось бы завести новый порт-провайдер (не `SmsSenderPort`), **выбросить/обойти** `otp_engine` (генерацию, `code_hash`, TTL, попытки, cooldown — всё уже построено и протестировано), переписать `POST /auth/phone/confirm` на вызов Telnyx verify вместо локальной сверки, потерять контроль над текстом/лимитами. Это уже **явно отклонено** в спеке ([`telnyx-integration-spec §1`](./telnyx-integration-spec-dogestonia-2026-06-10.md): «Verify API не включать в MVP-контракт»).

**Оценка сложности Verify-пути:** сам по себе Verify **проще завести** (3 вызова, Telnyx всё делает), но **для нас** это **средняя-высокая переделка** + потеря готового кода → нецелесообразно. Managed-verify имеет смысл только если захотим отдать OTP-жизненный-цикл Telnyx (меньше контроля, оплата per-verification).

**Рекомендация:** идти по **Messaging API** — код готов, OTP остаётся у нас. Verify держать как возможный будущий альтернативный адаптер (спека §1 уже предусмотрела `PhoneVerifyProviderPort`), не для MVP.

---

## 4. План включения Messaging-пути (инструкция, без реализации)

### Этап A — внешнее (Telnyx-кабинет, = SPIKE-08)
1. Создать/войти в Telnyx-аккаунт (API key уже есть). Пройти **Level-2 верификацию** — обязательна для буквенного отправителя `DOGEstonia` (long-lead).
2. Создать **Messaging Profile**; добавить **Эстонию (+372)** в whitelist стран назначения; задать **Alphanumeric Sender ID = `DOGEstonia`** (1–11 симв., есть буква). Скопировать **Messaging Profile ID**.
3. (Для webhook, опц.) Настроить в профиле webhook-URL для статусов доставки → на наш `POST /webhooks/telnyx/messaging`; забрать **Ed25519 public key** (для `TELNYX_WEBHOOK_PUBLIC_KEY`).
4. Trial: верифицировать номер тестировщика (иначе SMS не уйдёт) ИЛИ пополнить баланс.
5. Закрыть открытые вопросы SPIKE-08 §8 (идемпотентность `/v2/messages`, throughput EE, brand-proof для `DOGEstonia`, sandbox).

### Этап B — локально (`.env`, идентичный код — только конфиг)
6. `SMS_PROVIDER=telnyx` (и **убрать дубль** SMS_PROVIDER/PHONE_ALLOWED — G6).
7. `TELNYX_MESSAGING_PROFILE_ID=<profile_id из шага 2>` (закрывает G1).
8. Проверить: `TELNYX_API_KEY` (есть), `TELNYX_FROM=DOGEstonia`, `TELNYX_API_BASE_URL=https://api.telnyx.com`, `PHONE_ALLOWED_DIAL_PREFIXES=+372`.
9. (Опц.) `TELNYX_WEBHOOK_PUBLIC_KEY=<из шага 3>` — для проверки подписи delivery-webhook.

### Этап C — валидация (без изменения кода)
10. Старт сервиса: не должно быть `ConfigError` (значит профиль/from консистентны).
11. Live-smoke: `POST /auth/phone/request {phone:"+372…"}` → реальная SMS на телефон → `POST /auth/phone/confirm {phone, code}` → `GET /me` `phone_verified:true`.
12. Прогон live-теста Telnyx (тот, что скипается без creds) против trial.

### Railway-нюанс
- На railway (`APP_PROFILE=pilot`) провайдер `telnyx` **разрешён** (в отличие от `file`). После этого реальные SMS уходят на телефон — отдельный «OTP-в-лог» механизм не нужен (в интервью `DEV_OTP_ECHO` уже снят, [update 2026-07-09](./identity-mvp-hardening-interview-2026-07-04.md)).
- Секреты (`TELNYX_API_KEY`, `TELNYX_MESSAGING_PROFILE_ID`, `TELNYX_WEBHOOK_PUBLIC_KEY`) — только в railway variables, не в репозитории.

---

## 5. Итоговая оценка усилий

| Направление | Объём | Кто |
|-------------|-------|-----|
| **Код** | **0** (всё построено PV-06/07) | — |
| **`.env`** | 1 значение (profile_id) + 1 переключатель + чистка дублей | оператор, минуты |
| **Внешняя настройка Telnyx** | Аккаунт + Level-2 + Messaging Profile + EE whitelist + (опц.) webhook | SPIKE-08, low-mid; **long-lead — верификация аккаунта** |
| **Валидация** | live-smoke на тестовом номере | оператор, минуты |

**Критический путь:** SPIKE-08 (Level-2 верификация аккаунта) → profile_id в `.env` → `SMS_PROVIDER=telnyx` → live-smoke. Всё остальное готово.

---

## 6. Ссылки
- Архитектурный выбор Messaging vs Verify + контракт `send`: [`telnyx-integration-spec-dogestonia-2026-06-10.md`](./telnyx-integration-spec-dogestonia-2026-06-10.md) §1–§2.
- Бриф: [`telnyx-integration-architecture-brief-2026-06-10.md`](./telnyx-integration-architecture-brief-2026-06-10.md); архитектура phone: [`phone-verification-architecture-2026-06-10.md`](./phone-verification-architecture-2026-06-10.md).
- Внешний setup (SSOT задачи): [`SPIKE-IDS-PV-08`](../tasks/backlog-stories/phone-verification/SPIKE-IDS-PV-08-telnyx-account-setup.md); провайдер-стори [`PV-06`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md)/[`PV-07`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md).
- Verify API (не наш путь): https://developers.telnyx.com/docs/identity/verify/quickstart
- Код: [`telnyx/sender.py`](../../src/core/phone/telnyx/sender.py), [`telnyx/config.py`](../../src/core/phone/telnyx/config.py), [`otp_engine.py`](../../src/core/phone/otp_engine.py).
