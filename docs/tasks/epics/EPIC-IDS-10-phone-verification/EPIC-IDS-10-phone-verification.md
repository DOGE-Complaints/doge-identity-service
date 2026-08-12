# EPIC-IDS-10 — Верификация телефона (разовая, замена eID на MVP)

> **ID:** `EPIC-IDS-10` · **Alias (код/backlog):** `EPIC-IDS-PHONE` · **Статус:** ⚪ Todo · **Тип:** Функциональный
> **Source (backlog):** [`backlog-stories/phone-verification/EPIC-IDS-PHONE.md`](../../backlog-stories/phone-verification/EPIC-IDS-PHONE.md)

## Назначение
Разовая **верификация телефона** как дешёвая замена eID на MVP (eID [отложен](../../backlog-stories/eid-deferred/README.md) — доп. расходы SK). Цель та же — подтвердить, что за аккаунтом реальный уникальный человек: пользователь один раз вводит номер → получает OTP по SMS → вводит код → ставим флаг `phone_verified`. **Отдельный функционал** (eID вернём), но построен по тем же plugin-паттернам, что и провайдер-платформа eID (🟢 Done).

SMS-провайдеры **сменные**, активный выбирается в `.env` (`SMS_PROVIDER`), разрешённые дозвонные префиксы — в `.env` (`PHONE_ALLOWED_DIAL_PREFIXES`). **Первый боевой провайдер — Telnyx** (Messaging API).

## Контекст и решения (база)
- Архитектура: [`phone-verification-architecture-2026-06-10.md`](../../../analysis/phone-verification-architecture-2026-06-10.md) (§10 — продуктовые решения + уточнения Telnyx).
- Бриф для интегратора: [`telnyx-integration-architecture-brief-2026-06-10.md`](../../../analysis/telnyx-integration-architecture-brief-2026-06-10.md).
- Спека Telnyx (от агента): [`telnyx-integration-spec-dogestonia-2026-06-10.md`](../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md).
- Образец-платформа (код, Done): [`EPIC-IDS-EID`](../../backlog-stories/eid/EPIC-IDS-EID.md).

**Продуктовые решения (интервью 2026-06-11):** P1 один номер = один аккаунт (конфликт 409); P2 отслеживание доставки (webhook) — **в MVP**; P3 правила кода «Стандарт» (6 цифр, TTL 5 мин, 5 попыток, повтор 60 сек); P4 буквенный отправитель `DOGEstonia`.

## Stories
| Story | Тема | Слой | Статус |
|-------|------|------|--------|
| [STORY-IDS-PV-01](stories/STORY-IDS-PV-01-phone-provider-backbone/STORY-IDS-PV-01-phone-provider-backbone.md) | Plugin-платформа SMS-провайдеров + канон контракта | платформа | 🟢 Done |
| [STORY-IDS-PV-02](stories/STORY-IDS-PV-02-provider-owned-config/STORY-IDS-PV-02-provider-owned-config.md) | Provider-owned config + выбор активного + allowlist префиксов | платформа | 🟢 Done |
| [STORY-IDS-PV-03](stories/STORY-IDS-PV-03-otp-engine-session/STORY-IDS-PV-03-otp-engine-session.md) | OTP-движок + сессия верификации | ядро | 🟢 Done |
| [STORY-IDS-PV-04](stories/STORY-IDS-PV-04-profile-flag-migration/STORY-IDS-PV-04-profile-flag-migration.md) | Флаг профиля + модель + миграция + дедуп (P1) | данные | 🟢 Done |
| [STORY-IDS-PV-05](stories/STORY-IDS-PV-05-verification-flow-api/STORY-IDS-PV-05-verification-flow-api.md) | Flow API: request/confirm + rate-limit + аудит | оркестрация | 🟢 Done |
| [STORY-IDS-PV-06](stories/STORY-IDS-PV-06-telnyx-sms-sender/STORY-IDS-PV-06-telnyx-sms-sender.md) | Telnyx SMS sender (адаптер + регистрация + тесты) | провайдер | 🟢 Done |
| [STORY-IDS-PV-07](stories/STORY-IDS-PV-07-telnyx-delivery-webhook/STORY-IDS-PV-07-telnyx-delivery-webhook.md) | Telnyx delivery webhook ingestion (P2, MVP) | провайдер | 🟢 Done |
| [STORY-IDS-PV-09](stories/STORY-IDS-PV-09-durable-phone-persistence/STORY-IDS-PV-09-durable-phone-persistence.md) | Durable Supabase phone-персистентность (sessions + audit + bootstrap) | данные | 🟢 Done |
| [STORY-IDS-PV-10](stories/STORY-IDS-PV-10-file-sms-sink-dev/STORY-IDS-PV-10-file-sms-sink-dev.md) | File SMS sink (dev) | провайдер | 🟢 Done |
| [SPIKE-IDS-PV-08](../../backlog-stories/phone-verification/SPIKE-IDS-PV-08-telnyx-account-setup.md) | Telnyx account & sender setup (внешнее) | внешнее | ⚪ Todo |

## Порядок реализации
**PV-01** (фундамент) → параллельно **PV-02 / PV-03 / PV-04** → **PV-05** (нужны 02/03/04) → **PV-06** (Telnyx, нужны 01/02 + 05 для e2e) → **PV-07** (webhook, после 06) → **PV-09** (durable phone persistence, после 03/04; прецедент OAUTH-03) → **PV-10** (file SMS sink dev-DX, после 01/02/05; не блокирует MVP Telnyx). **SPIKE-08** — параллельно с начала (long-lead: аккаунт Telnyx + Level-2 верификация), гейтит только live-тест PV-06/07.

```
PV-01 ──┬─ PV-02 ─┐
        ├─ PV-03 ─┼─ PV-05 ── PV-06 ── PV-07 ── PV-09 (durability) ── PV-10 (dev file sink)
        └─ PV-04 ─┘
SPIKE-08 (параллельно) ─────────┘ (gate live-test)
```

## Связь
Зеркалит [`EPIC-IDS-EID`](../../backlog-stories/eid/EPIC-IDS-EID.md) (плагин-платформа провайдеров). Парадигма: [`runtime-docs/06-eid-providers.md`](../../../runtime-docs/06-eid-providers.md), [`runtime-docs/03-soa-roles.md`](../../../runtime-docs/03-soa-roles.md).

### Story 1: STORY-IDS-PV-01 — Plugin-платформа SMS-провайдеров + канон контракта — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-PV-01-phone-provider-backbone/STORY-IDS-PV-01-phone-provider-backbone.md`](./stories/STORY-IDS-PV-01-phone-provider-backbone/STORY-IDS-PV-01-phone-provider-backbone.md)
- **Source (backlog):** [`backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md`](../../backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md)

**Acceptance Criteria:**
- [x] Есть `SmsSenderPort` + `SmsSendResult` + `SmsSenderError`/`SmsErrorCode` + дескриптор + `SmsProviderRuntime` + реестр с guard.
- [x] `MockSmsSender` собирается через дескриптор; реестр строит активный + `mock`.
- [x] `SMS_PROVIDER=<незарегистрированный>` → `SmsProviderNotRegisteredError`/`ConfigError` с перечислением доступных (не голый `KeyError`).
- [x] Добавление провайдера = +1 дескриптор, без правок ядра реестра.
- [x] Offline-тесты зелёные (guard + сборка реестра + mock.send).

### Story 2: STORY-IDS-PV-02 — Provider-owned config + выбор активного + allowlist префиксов — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-PV-02-provider-owned-config/STORY-IDS-PV-02-provider-owned-config.md`](./stories/STORY-IDS-PV-02-provider-owned-config/STORY-IDS-PV-02-provider-owned-config.md)
- **Source (backlog):** [`backlog-stories/phone-verification/STORY-IDS-PV-02-provider-owned-config.md`](../../backlog-stories/phone-verification/STORY-IDS-PV-02-provider-owned-config.md)

**Acceptance Criteria:**
- [x] `SMS_PROVIDER` валидируется по реестру; неизвестный → понятная `ConfigError`.
- [x] `PHONE_ALLOWED_DIAL_PREFIXES` парсится; номер с неразрешённым префиксом → `COUNTRY_NOT_ALLOWED` (тест на `+372` ок / `+1` отклонён).
- [x] Нормализация E.164 покрыта тестами (пробелы/скобки/без `+`).
- [x] Ядровые phone-параметры доступны ядру; провайдер-поля не в `AppConfig`.
- [x] `.env.example` дополнен phone-блоком; offline-набор зелёный.

### Story 3: STORY-IDS-PV-03 — OTP-движок + сессия верификации — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-PV-03-otp-engine-session/STORY-IDS-PV-03-otp-engine-session.md`](./stories/STORY-IDS-PV-03-otp-engine-session/STORY-IDS-PV-03-otp-engine-session.md)
- **Source (backlog):** [`backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md`](../../backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md)

**Acceptance Criteria:**
- [x] `PhoneVerificationSession` + store (in-memory + supabase-совместимый интерфейс) с `attempts`.
- [x] OTP генерится криптослучайно, хранится только хэш; код не логируется.
- [x] Сверка: верный код → ok; неверный → `CODE_MISMATCH` + `attempts++`; ≥лимита → `TOO_MANY_ATTEMPTS`; просрочка → `CODE_EXPIRED`.
- [x] Повторный `request` инвалидирует прежний код пользователя.
- [x] `subject_hash = hash_secret(e164)` без провайдер-префикса.
- [x] Offline-тесты: успех/несовпадение/просрочка/лимит/повтор-инвалидация.

### Story 4: STORY-IDS-PV-04 — Флаг профиля + модель данных + миграция + дедуп — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-PV-04-profile-flag-migration/STORY-IDS-PV-04-profile-flag-migration.md`](./stories/STORY-IDS-PV-04-profile-flag-migration/STORY-IDS-PV-04-profile-flag-migration.md)
- **Source (backlog):** [`backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md`](../../backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md)

**Acceptance Criteria:**
- [x] Миграция добавляет phone-колонки + индекс на `verified_phone_hash`.
- [x] `attach_phone_verification` ставит `phone_verified=true` + хэш/префикс/время.
- [x] При `PHONE_ONE_ACCOUNT_PER_NUMBER=true` повтор номера на другом аккаунте → `ProfileConflictError`/409 (тест на дедуп).
- [x] `/me` отдаёт `phone_verified` и поля.
- [x] Offline-набор зелёный (in-memory + миграционный тест если применимо).

### Story 5: STORY-IDS-PV-05 — Flow API: request/confirm + rate-limit + аудит — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-PV-05-verification-flow-api/STORY-IDS-PV-05-verification-flow-api.md`](./stories/STORY-IDS-PV-05-verification-flow-api/STORY-IDS-PV-05-verification-flow-api.md)
- **Source (backlog):** [`backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md`](../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md)

**Acceptance Criteria:**
- [x] `POST /auth/phone/request` (валидный JWT, разрешённый префикс) → создаёт сессию `started`, шлёт SMS через активный провайдер, возвращает `expires_at`.
- [x] Неразрешённый префикс → `COUNTRY_NOT_ALLOWED`; повтор раньше cooldown → `RATE_LIMITED` (старый код инвалидирован при новом).
- [x] `POST /auth/phone/confirm` верный код → `phone_verified=true`; неверный/просрочка/лимит → корректные `SmsErrorCode`; дубль номера → 409.
- [x] Все события в аудите без PII (нет сырого номера/кода).
- [x] Полный флоу проходит на `MockSmsSender` офлайн-тестом.

### Story 6: STORY-IDS-PV-06 — Telnyx SMS sender: адаптер + регистрация + тесты — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-PV-06-telnyx-sms-sender/STORY-IDS-PV-06-telnyx-sms-sender.md`](./stories/STORY-IDS-PV-06-telnyx-sms-sender/STORY-IDS-PV-06-telnyx-sms-sender.md)
- **Source (backlog):** [`backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md`](../../backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md)

**Acceptance Criteria:**
- [x] `SMS_PROVIDER=telnyx` (+ creds) → `get_active()` возвращает `TelnyxSmsSender`; без обязательных env / буквенный from без profile_id → понятная `ConfigError`.
- [x] `send` формирует корректный POST (Bearer, `from/to/text/type`, profile_id при буквенном from); 200+`queued` → `accepted=True` + `provider_message_id`.
- [x] Ошибки Telnyx замаплены в `SmsErrorCode` по таблице спеки; сырой код/номер не логируется.
- [x] Юнит-тесты offline (mocked httpx) зелёные; live-тест проходит против trial и **скипается** без creds.
- [x] `.env.example` содержит `TELNYX_*`.

### Story 7: STORY-IDS-PV-07 — Telnyx delivery webhook ingestion (MVP) — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-PV-07-telnyx-delivery-webhook/STORY-IDS-PV-07-telnyx-delivery-webhook.md`](./stories/STORY-IDS-PV-07-telnyx-delivery-webhook/STORY-IDS-PV-07-telnyx-delivery-webhook.md)
- **Source (backlog):** [`backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md`](../../backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md)

**Acceptance Criteria:**
- [x] `POST /webhooks/telnyx/messaging` принимает события и обновляет `delivery_status` по `provider_message_id`.
- [x] Невалидная/отсутствующая подпись Telnyx → отклонение (401/403), не обрабатываем.
- [x] Повторное/устаревшее событие идемпотентно (не откатывает финальный статус).
- [x] Событие доставки пишется в аудит без PII.
- [x] Offline-тесты: валидный/невалидный webhook, идемпотентность, маппинг статусов.

### Story 9: STORY-IDS-PV-09 — Durable Supabase phone-персистентность (sessions + audit + bootstrap parity) — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-PV-09-durable-phone-persistence/STORY-IDS-PV-09-durable-phone-persistence.md`](./stories/STORY-IDS-PV-09-durable-phone-persistence/STORY-IDS-PV-09-durable-phone-persistence.md)
- **Source (backlog):** [`backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md`](../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md)
- **Wave:** `pkg-000039`

**Acceptance Criteria:**
- [x] При `DB_BACKEND=supabase` pending OTP-сессия, созданная до пересоздания стора (эмуляция редеплоя/рестарта), **остаётся доступной** для `confirm` (G-3 закрыт); просроченная/использованная сессия даёт корректный статус (`expired`/`consumed`).
- [x] При `DB_BACKEND=supabase` событие phone-аудита, записанное до пересоздания репо, **читается после** (строка персистирована в Postgres; G-2a закрыт).
- [x] Durable phone-session store удовлетворяет тому же протоколу `PhoneVerificationSessionStore`, durable phone-audit repo — протоколу `PhoneAuditLogRepository`, без изменения контракта.
- [x] DI-переключатель: `DB_BACKEND=supabase` → Supabase-реализации; `DB_BACKEND=in_memory` → прежние `InMemory*`; **in-memory путь не изменён, существующие офлайн-тесты зелёные**.
- [x] Новая миграция создаёт `phone_audit_events` (+ `phone_verification_sessions`, если сессии персистятся) с RLS и индексом по `expires_at`/времени; миграция покрыта в `test_supabase_migrations_sql`.
- [x] Bootstrap-parity: свежий накат [`000_full_init.sql`](../../../../supabase/bootstrap/000_full_init.sql) создаёт phone-колонки профиля, OAuth-таблицы и новые phone-persistence-таблицы — т.е. fresh bootstrap эквивалентен полному накату миграций (проверяемо diff'ом схемы bootstrap vs миграции).
- [x] Аудит-содержимое (IP/UA) **не вводится** этой стори (остаётся как есть до SEC-02) — scope-граница не нарушена.

### Story 10: STORY-IDS-PV-10 — File SMS sink (dev) — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-PV-10-file-sms-sink-dev/STORY-IDS-PV-10-file-sms-sink-dev.md`](./stories/STORY-IDS-PV-10-file-sms-sink-dev/STORY-IDS-PV-10-file-sms-sink-dev.md)
- **Source (backlog):** [`backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md`](../../backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md)
- **Wave:** `pkg-000041`

**Acceptance Criteria:**
- [x] `SMS_PROVIDER=file` → `get_active()` возвращает `FileSmsSender`; `POST /auth/phone/request` дописывает строку `{utc-таймстемп}\t{текст с кодом}` в `<outbox>/<номер>.log`.
- [x] Повторные SMS на тот же номер — **append** (не перезапись); разные номера — разные файлы.
- [x] `tail -f <outbox>/<номер>.log` в ручном тесте показывает приходящие коды (DX-цель достигнута).
- [x] Имя файла санитизировано (только `+` и цифры); path-traversal невозможен.
- [x] `APP_PROFILE=pilot` + `SMS_PROVIDER=file` → `ConfigError` (demo-only анти-leak).
- [x] `file`-провайдер **не** создаёт `httpx.Client` (нет сети).
- [x] outbox-каталог в `.gitignore`; `.env.example` обновлён (значение `file` + `FILE_SMS_OUTBOX_DIR` + предупреждение).
- [x] Offline-тесты зелёные: `.venv/bin/python -m pytest -q -m "not live_integration"`.
