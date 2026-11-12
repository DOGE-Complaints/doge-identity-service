# Аудит кода: верификация телефона (EPIC-IDS-PHONE) — 2026-06-11

> **Что это.** Аудит фактической реализации механизма верификации телефона (модуль `src/core/phone/` + API + Telnyx) против архитектуры [`phone-verification-architecture-2026-06-10.md`](phone-verification-architecture-2026-06-10.md) (§10, решения P1–P4) и спеки [`telnyx-integration-spec-dogestonia-2026-06-10.md`](telnyx-integration-spec-dogestonia-2026-06-10.md).
> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — чтение реального кода + прогон тестов. **Тесты:** `330 passed, 10 skipped` (offline).
> **Вердикт:** реализация **полная и соответствует** архитектуре/решениям; критичных дефектов не найдено. Новые стори под mock/тесты **не нужны** (уже есть). Подробности ниже.

---

## 1. Карта компонентов (verified ✅)

| Слой | Файл | Статус |
|------|------|--------|
| Порт/канон | [`phone/base.py`](../../src/core/phone/base.py) (`SmsSenderPort`, `SmsErrorCode`, `SmsSenderError`, `SmsSendResult`) | ✅ |
| Plugin: дескриптор/конфиг/реестр/runtime | [`descriptor.py`](../../src/core/phone/descriptor.py), [`config_spec.py`](../../src/core/phone/config_spec.py), [`registry.py`](../../src/core/phone/registry.py), [`registry_builder.py`](../../src/core/phone/registry_builder.py), [`runtime.py`](../../src/core/phone/runtime.py)/[`runtime_factory.py`](../../src/core/phone/runtime_factory.py) | ✅ |
| Mock | [`phone/mock/mock_sender.py`](../../src/core/phone/mock/mock_sender.py) | ✅ |
| OTP-движок + сессия | [`phone/otp_engine.py`](../../src/core/phone/otp_engine.py) | ✅ |
| Нормализация E.164 + allowlist | [`phone/e164.py`](../../src/core/phone/e164.py) | ✅ |
| Текст SMS | [`phone/sms_text.py`](../../src/core/phone/sms_text.py) | ✅ |
| Telnyx: sender/config/errors/webhook | [`phone/telnyx/sender.py`](../../src/core/phone/telnyx/sender.py), [`config.py`](../../src/core/phone/telnyx/config.py), [`errors.py`](../../src/core/phone/telnyx/errors.py), [`delivery_ingest.py`](../../src/core/phone/telnyx/delivery_ingest.py), [`webhook_signature.py`](../../src/core/phone/telnyx/webhook_signature.py) | ✅ |
| API: хендлеры | [`handlers.py:432`](../../src/core/api/handlers.py#L432) `handle_phone_request`, [`:516`](../../src/core/api/handlers.py#L516) `handle_phone_confirm` | ✅ |
| API: роуты | [`asgi_app.py:286-319`](../../src/core/api/asgi_app.py#L286) `/auth/phone/request`, `/confirm`, `/webhooks/telnyx/messaging` | ✅ |
| Конфиг | [`schema.py:63-69,108,162-170,230-236`](../../src/core/config/schema.py) (`SMS_PROVIDER` + `PHONE_*` + делегированная валидация) | ✅ |
| Профиль + миграция | [`repositories.py:165` `attach_phone_verification`](../../src/core/infrastructure/repositories.py#L165), миграция [`20260611000001_profiles_phone_verification.sql`](../../supabase/migrations/) | ✅ |
| `/me` | [`me_response.py:29-45`](../../src/core/api/me_response.py#L29) (`phone_verified`/`phone_provider`/`phone_dial_prefix`/`phone_verified_at`) | ✅ |

---

## 2. Соответствие решениям P1–P4 и спеке (verified)

- **P1 «один номер = один аккаунт»** ✅ — `attach_phone_verification(..., one_account_per_number=cfg.phone_one_account_per_number)`; при включённом флаге `get_by_verified_phone_hash` на другом юзере → `ProfileConflictError` → HTTP 409 ([`handlers.py:580-600`](../../src/core/api/handlers.py#L580), [`repositories.py:165-180`](../../src/core/infrastructure/repositories.py#L165)).
- **P3 «Стандарт»** ✅ — дефолты `PHONE_CODE_LENGTH=6`, `PHONE_CODE_TTL_S=300`, `PHONE_MAX_ATTEMPTS=5`, `PHONE_RESEND_COOLDOWN_S=60` ([`schema.py:232-235`](../../src/core/config/schema.py#L232)); cooldown в `handle_phone_request` ([`:456-473`](../../src/core/api/handlers.py#L456)).
- **P4 буквенный отправитель** ✅ — Telnyx sender требует `messaging_profile_id` при alphanumeric `from` ([`sender.py:28-34`](../../src/core/phone/telnyx/sender.py#L28)); условная валидация в config.
- **Канон ошибок → ответ** ✅ — `SmsErrorCode` мапится в envelope (`error.code`), без утечки деталей.
- **Telnyx send по спеке** ✅ — `POST /v2/messages`, Bearer, payload `{from,to,text,type,messaging_profile_id?}`, успех = 200 + `data.id` + `data.to[0].status∈{queued,sent}`; ошибки/таймаут → канон ([`sender.py`](../../src/core/phone/telnyx/sender.py), [`errors.py`](../../src/core/phone/telnyx/errors.py)).
- **P2 delivery webhook** ✅ — `/webhooks/telnyx/messaging` + **реальная Ed25519-проверка подписи** ([`webhook_signature.py`](../../src/core/phone/telnyx/webhook_signature.py)) + ingest по `provider_message_id` ([`delivery_ingest.py`](../../src/core/phone/telnyx/delivery_ingest.py)).
- **Дозвонный фильтр в ядре** ✅ — `resolve_dial_prefix` (longest-match, иначе `COUNTRY_NOT_ALLOWED`) до отправки SMS ([`e164.py:33-42`](../../src/core/phone/e164.py#L33)).

---

## 3. Безопасность (verified)

- ✅ **OTP не возвращается** в ответе `/request` (только `{sent, expires_at}`) — [`handlers.py:509-513`](../../src/core/api/handlers.py#L509).
- ✅ **OTP нигде не логируется** — в `phone/` логирование есть только в `telnyx/errors.py` и пишет лишь коды ошибок (без номера/кода).
- ✅ **Хранится только хэш** кода и номера (`hash_secret`/HMAC), сверка — **constant-time** (`hmac.compare_digest`) [`otp_engine.py:27-29`](../../src/core/phone/otp_engine.py#L27).
- ✅ **OTP крипто-случайный** (`secrets.choice`) [`otp_engine.py:23-24`](../../src/core/phone/otp_engine.py#L23).
- ✅ **Session-binding**: пользователь из Bearer JWT (`get_current_user`), не из тела; роуты защищены.
- ✅ **Аудит без PII** — `_log_phone_audit` пишет тип события/код причины, не номер/код.
- ✅ **Повтор инвалидирует прежний код** (`mark_failed("superseded")`) [`otp_engine.py:45-47`](../../src/core/phone/otp_engine.py#L45).
- ✅ **Webhook**: без валидной подписи → отклоняется; ingest идемпотентен.

---

## 4. Ответы на поставленные вопросы

- **Тестирование через mock по `.env`** → **ДА, есть.** `SMS_PROVIDER=mock` — дефолт ([`providers.py:27`](../../src/core/config/providers.py#L27), `.env.example:63`); выбор `mock`/`telnyx` валидируется реестром. Отдельная стори **не нужна**.
- **Тесты на полный OTP-процесс** → **ДА, есть.** [`tests/test_phone_verification_flow.py`](../../tests/test_phone_verification_flow.py) — offline e2e через `TestClient`: request→SMS(mock)→confirm→`/me phone_verified`, плюс негативы (страна, cooldown, инвалидация, дедуп). Также `test_phone_otp_engine`, `test_phone_verification_session_store`, `test_sms_provider_registry`, `test_telnyx_sms_sender`, `test_telnyx_delivery_webhook/ingest/signature`, `test_phone_config_schema`, `test_phone_e164`. Отдельная стори **не нужна**.

---

## 5. Замечания (не дефекты, важно для рунбука/эксплуатации)

1. **🟡 OTP-код невозможно прочитать «снаружи» в mock-режиме** (это **правильно** по безопасности — не логируется, не возвращается). Следствие: полный `request→confirm` через **чистый curl** в mock-режиме недостижим (код негде взять). Поэтому:
   - полный mock-флоу гоняется in-process (pytest/`TestClient`, где доступен `MockSmsSender.sent_messages`) — так и сделано в e2e-тесте;
   - **live-режим (Telnyx)** даёт настоящий curl-smoke (код приходит SMS на телефон).
   - Рунбук учитывает оба пути. **Логировать OTP даже в demo не рекомендуется** (риск PII), поэтому отдельную «dev-видимость кода» не вводим.
2. **ℹ️ Статусы стори в [`EPIC-IDS-PHONE.md`](../tasks/backlog-stories/phone-verification/EPIC-IDS-PHONE.md) отстают от факта** — PV-02/04/05/07 помечены Todo, но реализованы и покрыты тестами (pipeline-исполнение видно в `docs/tasks/epics/EPIC-IDS-10-phone-verification/`). Рекомендация: синхронизировать статусы на 🟢 Done (не входит в код-аудит; отметить владельцу).
3. **ℹ️ Webhook-подпись** опирается на имена заголовков/публичный ключ Telnyx (`webhook_signature.py`) — финально сверить с реальными значениями на [SPIKE-IDS-PV-08](../tasks/backlog-stories/phone-verification/SPIKE-IDS-PV-08-telnyx-account-setup.md) (помечено в коде комментарием).

---

## 6. Итог
Механизм верификации телефона **реализован полностью, безопасно и по архитектуре**; offline-тесты зелёные; mock-режим и OTP-e2e уже покрыты. Новые стори под пункты 2/3 запроса **не требуются**. Создан двухрежимный рунбук: [`docs/runbook/phone-sms-verification.md`](../runbook/phone-sms-verification.md). Не-кодовые follow-up (синк статусов стори, сверка webhook-подписи на SPIKE) — в §5.

## Anchors
- Архитектура: [`phone-verification-architecture-2026-06-10.md`](phone-verification-architecture-2026-06-10.md)
- Спека Telnyx: [`telnyx-integration-spec-dogestonia-2026-06-10.md`](telnyx-integration-spec-dogestonia-2026-06-10.md)
- Эпик/стори: [`EPIC-IDS-PHONE.md`](../tasks/backlog-stories/phone-verification/EPIC-IDS-PHONE.md)
- Рунбук: [`phone-sms-verification.md`](../runbook/phone-sms-verification.md)
