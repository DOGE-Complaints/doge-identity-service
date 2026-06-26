# 19. Phone Verification Flow (SMS-OTP)

> **Статус:** реализовано (активный гейт верификации).
> **Связь:** файл 11 (eID flow) — **отложен** (см. `project-eid-authentigate-choice`, ⚠️ подключение eID отложено 2026-06-10). Phone-верификация — текущий пивот: активный гейт `phone_verified` вместо `eid_verified`.
> **Примечание:** Создано 2026-06-24 (решение Q1): фиксирует активный механизм, ранее живший только в `docs/analysis/phone-verification-architecture-2026-06-10.md`. Все утверждения заземлены в коде (`file:line`).

---

## Назначение

SMS-OTP верификация телефона — активный гейт `phone_verified` (пивот от eID).
Колонки `profiles` зеркалят eID-колонки: миграция
`supabase/migrations/20260611000001_profiles_phone_verification.sql:1-2`
(«Phone verification status on profiles (mirror eID columns)»).

Пользователь подтверждает владение номером E.164 (только Эстония, `+372` по умолчанию) одноразовым кодом, доставляемым по SMS. Успешное подтверждение выставляет `profiles.phone_verified = true` и сохраняет `verified_phone_hash`.

---

## Общая схема

```
User (spa-app / Custom GPT)
  │
  ▼
POST /auth/phone/request
  Authorization: Bearer <supabase_jwt>
  Body: { phone }
  │
  │  Backend: normalize→E.164, проверка dial-prefix (+372),
  │           генерация OTP (6 цифр), создание сессии, send SMS,
  │           resend-cooldown
  ▼
Response: { sent: true, expires_at }
  │
  │  Пользователь получает SMS с кодом
  ▼
POST /auth/phone/confirm
  Authorization: Bearer <supabase_jwt>
  Body: { phone, code }
  │
  │  Backend: bind номера к сессии по phone_hash,
  │           constant-time сравнение кода,
  │           attach_phone_verification (conflict detection),
  │           phone_verified=true + verified_phone_hash
  ▼
Response: { status: "verified" }

Telnyx (асинхронно):
POST /webhooks/telnyx/messaging  → Ed25519 signature verify (fail-closed)
                                  → delivery-status ingest
```

---

## POST /auth/phone/request

**Маршрут:** `src/core/api/asgi_app.py:322-336` (`auth_phone_request`).
**Auth required:** да — `Depends(get_current_user)` (`asgi_app.py:325`), Bearer Supabase JWT.
**Handler:** `handle_phone_request` (`src/core/api/handlers.py:432-513`).

### Request body

```json
{ "phone": "+37255512345" }
```

Извлекается через `_phone_payload_from_request` (`asgi_app.py:329`).

### Алгоритм (handler)

1. Проверка конфигурации: если `sms_sender_registry` или `phone_verification_session_store` отсутствуют → `CONFIG_ERROR` / 500 (`handlers.py:441-447`).
2. `e164 = normalize_to_e164(phone)` (`handlers.py:453`, `src/core/phone/e164.py:6-30`): тримминг, удаление пробелов/скобок/дефисов, требование только цифр после `+`; иначе `INVALID_PHONE`.
3. `dial_prefix = resolve_dial_prefix(e164, config.phone_allowed_dial_prefixes)` (`handlers.py:454`, `e164.py:33-42`): если префикс не в allowlist → `COUNTRY_NOT_ALLOWED`. По умолчанию разрешён только `+372` (`src/core/config/schema.py:233`).
4. Resend-cooldown: если есть активная сессия и `now < created_at + phone_resend_cooldown_s` → `RATE_LIMITED`, событие `phone_verification_request_failed` (`handlers.py:456-473`). Cooldown по умолчанию 60 с (`schema.py:237`).
5. `create_phone_verification_session` (`handlers.py:476-484`, `src/core/phone/otp_engine.py:32-64`):
   - предыдущая активная сессия помечается `superseded` (`otp_engine.py:45-47`);
   - OTP генерируется `secrets.choice("0123456789")` длиной `phone_code_length` (`otp_engine.py:23-24`, 6 цифр по умолчанию — `schema.py:234`);
   - `phone_hash` и `code_hash` — HMAC-SHA256 c ключом `config.eid_secret` (`otp_engine.py:19-20,53,55`, `src/core/security/hashing.py:9-11`);
   - `expires_at = created_at + phone_code_ttl_s` (`otp_engine.py:59`, TTL 300 с по умолчанию — `schema.py:235`);
   - `attempts = 0`, `status = "started"`.
6. Отправка SMS: `sender.send(to_e164=e164, text=build_verification_sms_text(plaintext_code))` (`handlers.py:485`, текст `src/core/phone/sms_text.py:4-5`). `provider_message_id` (если есть) сохраняется в сессии (`handlers.py:486-488`).
7. Аудит-событие `phone_verification_requested`, success (`handlers.py:501-508`).

### Response (успех)

```json
HTTP 200
{ "sent": true, "expires_at": "2026-06-25T14:40:00Z" }
```

(`handlers.py:509-513`; `_format_utc_iso` — `handlers.py:90-93`.)

### Errors

| Error code | HTTP | Условие | Заземление |
|-----------|------|---------|-----------|
| `INVALID_PHONE` | 400 | Невалидный E.164 | `e164.py:9,18,27`; статус `handlers.py:96-99` |
| `COUNTRY_NOT_ALLOWED` | 400 | dial-prefix не в allowlist | `e164.py:38-41` |
| `RATE_LIMITED` | 400 | Resend до окончания cooldown | `handlers.py:470-473` |
| `PROVIDER_UNAVAILABLE` / `SEND_FAILED` | 503 | Сбой провайдера SMS | `handlers.py:96-99` |
| `CONFIG_ERROR` | 500 | Сервисы не сконфигурированы | `handlers.py:441-447` |

Маппинг кода→HTTP: `_phone_error_response` + `_sms_error_http_status` (`handlers.py:96-108`).

---

## POST /auth/phone/confirm

**Маршрут:** `src/core/api/asgi_app.py:338-353` (`auth_phone_confirm`).
**Auth required:** да — Bearer Supabase JWT (`asgi_app.py:341`).
**Handler:** `handle_phone_confirm` (`src/core/api/handlers.py:516-610`).

### Request body

```json
{ "phone": "+37255512345", "code": "123456" }
```

### Алгоритм (handler)

1. Проверка конфигурации (`session_store`, `profile_repository`) → `CONFIG_ERROR` / 500 (`handlers.py:526-532`).
2. `e164 = normalize_to_e164(phone)` (`handlers.py:539`).
3. `session = session_store.get_latest_for_confirm(user_id)` (`handlers.py:540`); если нет → `UNKNOWN` / 400 (`handlers.py:541-545`); если `status == "failed"` → `TOO_MANY_ATTEMPTS` (`handlers.py:546-550`).
4. **Bind номера к сессии:** `expected_phone_hash = hash_secret(e164, key=config.eid_secret)`; если `session.phone_hash != expected_phone_hash` → ошибка (номер не соответствует сессии) (`handlers.py:553-558`). Submitted phone привязывается к сессии по `phone_hash`, а не к браузерной сессии.
5. `verify_phone_code` (`handlers.py:560-567`, `otp_engine.py:67-132`):
   - сессия не `started`/истекла → `CODE_EXPIRED` (`otp_engine.py:83-88`);
   - сравнение кода **constant-time:** `hmac.compare_digest` над HMAC-хешами (`otp_engine.py:27-29`);
   - совпадение → `mark_consumed`, возврат `PhoneVerificationResult(subject_hash=HMAC(e164))` (`otp_engine.py:90-98`);
   - несовпадение → инкремент `attempts`; при `attempts >= phone_max_attempts` (5 по умолчанию — `schema.py:236`) сессия → `failed`, `TOO_MANY_ATTEMPTS` (`otp_engine.py:100-116`); иначе `CODE_MISMATCH` (`otp_engine.py:118-132`).
6. `profile_repo.attach_phone_verification(...)` (`handlers.py:580-588`): выставляет `phone_verified=true`, `verified_phone_hash=subject_hash`, `phone_provider`, `phone_dial_prefix`, `phone_verified_at`. Передаётся `one_account_per_number=config.phone_one_account_per_number`.
7. Аудит-событие `phone_verification_confirmed`, success (`handlers.py:602-609`).

### Response (успех)

```json
HTTP 200
{ "status": "verified" }
```

(`handlers.py:610`.)

### Errors

| Error code | HTTP | Условие | Заземление |
|-----------|------|---------|-----------|
| `UNKNOWN` | 400 | Нет активной сессии / номер не совпал с сессией | `handlers.py:541-558` |
| `CODE_MISMATCH` | 400 | Неверный код (есть попытки) | `otp_engine.py:132` |
| `CODE_EXPIRED` | 400 | Код истёк / сессия не активна | `otp_engine.py:83-88` |
| `TOO_MANY_ATTEMPTS` | 400 | Исчерпаны попытки (`>= phone_max_attempts`) | `otp_engine.py:101-116`, `handlers.py:546-550` |
| `profile_conflict` | 409 | Номер уже привязан к другому аккаунту | `handlers.py:589-600` |
| `CONFIG_ERROR` | 500 | Сервисы не сконфигурированы | `handlers.py:526-532` |

---

## One-number-one-account

`409 profile_conflict` поднимается, когда `verified_phone_hash` уже принадлежит другому пользователю.

- Гейт включается флагом `phone_one_account_per_number` (`schema.py:238`, по умолчанию `true`).
- Проверка in-memory: `attach_phone_verification` сверяет существующего владельца, иначе `ProfileConflictError` (`src/core/infrastructure/repositories.py:176-181`); Supabase-путь: `get_by_verified_phone_hash` (`src/core/infrastructure/db_supabase.py:390-394,490-501`).
- В Supabase целостность дополнительно гарантирует уникальный частичный индекс `unique_verified_phone_hash` (`supabase/migrations/20260611000001_profiles_phone_verification.sql:11-13`).
- Handler ловит `ProfileConflictError` → `profile_conflict` / 409, событие `phone_verification_confirm_failed` с `failure_reason="profile_conflict"` (`handlers.py:589-600`).

---

## SMS-провайдеры (registry / абстракция)

Зеркалит eID provider-абстракцию (registry pattern, descriptor + runtime).

- **Port:** `SmsSenderPort` (Protocol) с `provider_name` и `send(to_e164, text) -> SmsSendResult` (`src/core/phone/base.py:37-42`).
- **Descriptor:** `SmsProviderDescriptor(name, config_spec, build)` (`src/core/phone/descriptor.py:16-24`).
- **Registry:** `SmsSenderRegistry.get_active(config) → get(config.sms_provider)` (`src/core/phone/registry.py:24-25`).
- **Builder:** `build_sms_registry` всегда регистрирует `mock` + активного провайдера (`src/core/phone/registry_builder.py:25-38`).
- **Mock:** `MockSmsSender` — собирает сообщения в памяти, всегда принимает (`src/core/phone/mock/mock_sender.py:9-25`).
- **Telnyx:** `TelnyxSmsSender.send` — POST `{api_base}/v2/messages` с Bearer (`src/core/phone/telnyx/sender.py:21-54`); успех при `message_id` + статус `queued`/`sent` (`sender.py:9,70-71`). Маппинг ошибок Telnyx→`SmsErrorCode` (`src/core/phone/telnyx/errors.py:52-78`).

### Telnyx webhook

**Маршрут:** `POST /webhooks/telnyx/messaging` (`asgi_app.py:355-368`, без Bearer-зависимости).
**Handler:** `handle_telnyx_messaging_webhook` (`handlers.py:628-729`).

1. **Ed25519 verify (fail-closed):** если `TELNYX_WEBHOOK_PUBLIC_KEY` пуст → 503 (`handlers.py:635-642`); если подпись невалидна → 401, событие `failure_reason="invalid_signature"` (`handlers.py:644-663`). Проверка над `{timestamp}|{body}` (`src/core/phone/telnyx/webhook_signature.py:22-42`); при любой ошибке/отсутствии заголовков возвращает `False` (fail-closed).
2. Парсинг payload → `parse_telnyx_messaging_webhook` (`handlers.py:693-694`, `src/core/phone/telnyx/delivery_ingest.py:40-68`).
3. Delivery-status ingest: `apply_delivery_update` обновляет `delivery_status` сессии с защитой от регресса статуса и финальных статусов (`handlers.py:712-717`, `delivery_ingest.py:71-101`).
4. Событие `telnyx_delivery_status_updated`; всегда возвращает **204** (`handlers.py:719-729`).

---

## Конфигурация

Все ключи — `src/core/config/schema.py:232-239`:

| Env var | Поле | Default | Заземление |
|---------|------|---------|-----------|
| `SMS_PROVIDER` | `sms_provider` | `mock` | `schema.py:163,232` |
| `PHONE_ALLOWED_DIAL_PREFIXES` | `phone_allowed_dial_prefixes` | `+372` | `schema.py:233` |
| `PHONE_CODE_LENGTH` | `phone_code_length` | `6` | `schema.py:234` |
| `PHONE_CODE_TTL_S` | `phone_code_ttl_s` | `300` | `schema.py:235` |
| `PHONE_MAX_ATTEMPTS` | `phone_max_attempts` | `5` | `schema.py:236` |
| `PHONE_RESEND_COOLDOWN_S` | `phone_resend_cooldown_s` | `60` | `schema.py:237` |
| `PHONE_ONE_ACCOUNT_PER_NUMBER` | `phone_one_account_per_number` | `true` | `schema.py:238` |

Telnyx (`src/core/phone/telnyx/config.py:38-58`): `TELNYX_API_KEY` (required — `config.py:16,25-28`), `TELNYX_API_BASE_URL` (`https://api.telnyx.com`), `TELNYX_FROM` (`DOGEstonia`), `TELNYX_MESSAGING_PROFILE_ID`, `TELNYX_MESSAGE_TYPE` (`SMS`), `TELNYX_ENCODING` (`auto`), `TELNYX_WEBHOOK_PUBLIC_KEY`.

---

## Приватность

**Сырой номер телефона НИКОГДА не хранится** — хранятся только хеши.

- `phone_hash` / `verified_phone_hash` / `code_hash` — HMAC-SHA256 hex с ключом `config.eid_secret` (`src/core/security/hashing.py:9-11`, `otp_engine.py:53,55,96`).
- DB-колонки `profiles` (миграция `20260611000001_profiles_phone_verification.sql:4-9`): `phone_verified BOOLEAN`, `verified_phone_hash TEXT`, `phone_provider TEXT`, `phone_dial_prefix TEXT`, `phone_verified_at TIMESTAMPTZ`. Сырого номера среди колонок нет.
- CHECK-констрейнт `phone_consistency`: `phone_verified=true` требует непустых `verified_phone_hash` и `phone_verified_at` (`...20260611000001...:18-26`).
- Аудит-события не содержат PII — только `event_type`, `provider`, `success`, `failure_reason`, `request_id` (`handlers.py:124-135`).

---

## Ограничения (известные, НЕ скрыты)

Зафиксированы при аудите; см. `docs/analysis/identity-backend-full-audit-2026-06-24.md` (G-1/G-2/G-3). Сборка durable — решается отдельно.

- **G-1:** Сессии phone-верификации только в памяти — `InMemoryPhoneVerificationSessionStore` (`src/core/infrastructure/repositories.py:284`), создаётся в `src/core/infrastructure/providers.py:121`. Не переживают рестарт; durable Supabase phone-session store отсутствует.
- **G-2:** Аудит-лог phone — только в памяти: `InMemoryPhoneAuditLogRepository` (`repositories.py:362`), создаётся `providers.py:122`. Таблицы `phone_audit_events` нет (в отличие от `eid_audit_events` — `db_supabase.py:305`).
- **G-3:** HTTP rate-limit на `POST /auth/phone/request` — per-user окно (`RATE_LIMIT_PHONE_REQUEST_*`, default 5/600s) через `rate_limit_dependency` **до** handler (pkg-000036, SEC-01b). OTP resend-cooldown (`handlers.py:456-473`, default 60s) остаётся доменным **400** `RATE_LIMITED` — не заменяется 429. `/auth/phone/confirm` без HTTP rate-limit в этой волне.

---

## Acceptance Criteria

Заземлены в существующих тестах `tests/test_phone_verification_flow.py`:

- [x] `request` создаёт сессию, отправляет SMS, возвращает `expires_at` — `test_phone_request_creates_session_sends_sms_and_returns_expires_at`
- [x] `request` с запрещённым префиксом → `COUNTRY_NOT_ALLOWED` — `test_phone_request_country_not_allowed`
- [x] `request` до окончания cooldown → rate-limited — `test_phone_request_rate_limited_before_cooldown`
- [x] `request` после cooldown инвалидирует прежний код — `test_phone_request_after_cooldown_invalidates_previous_code`
- [x] полный `confirm` выставляет `phone_verified` — `test_phone_confirm_full_flow_sets_phone_verified`
- [x] неверный код → `CODE_MISMATCH` — `test_phone_confirm_wrong_code_returns_code_mismatch`
- [x] истёкший код — `test_phone_confirm_expired_code`
- [x] исчерпание попыток — `test_phone_confirm_too_many_attempts`
- [x] дубликат номера → 409 — `test_phone_confirm_duplicate_number_returns_409`
- [x] аудит-события без PII — `test_phone_audit_events_contain_no_pii`

Дополнительные модульные тесты: `tests/test_phone_e164.py`, `tests/test_phone_otp_engine.py`, `tests/test_phone_config_schema.py`, `tests/test_phone_verification_session_store.py`.
