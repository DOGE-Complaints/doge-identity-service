# Архитектура верификации телефона (зеркало eID-платформы)

> **Зачем этот документ.** eID-подключение [отложено](../tasks/backlog-stories/eid-deferred/README.md) (доп. расходы SK). Задачу «убедиться, что за аккаунтом реальный человек» решаем дешевле — **разовой верификацией телефона**: один раз подтвердил номер по SMS-коду → ставим флаг, как для eID. Это **отдельный функционал** (eID вернём), но строим его по **тем же архитектурным паттернам**, что уже сделаны для eID-провайдеров.
> **Как читать.** Сначала объясняю, как устроена готовая eID-платформа (с диаграммой), потом — как зеркалим её под телефон, и чем телефон проще. Всё про eID — по фактическому коду; всё про телефон — это проект (ещё не код).
> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc).

---

## 1. Главная идея простыми словами

«Верификация» = разовая проверка, что за аккаунтом живой уникальный человек, с записью результата во флаг профиля.

- **eID** доказывает это через гос-удостоверение (Smart-ID/ID-карта): внешний провайдер ручается за личность.
- **Телефон** доказывает слабее, но дешевле: человек владеет номером → ему шлём 6-значный код по SMS → он вводит код обратно. Если код совпал — считаем, что номер его, ставим `phone_verified=true`.

Оба случая укладываются в одну и ту же схему: **активный провайдер выбирается в `.env`, провайдеры сменные (plugin), список разрешённых стран — в `.env`**. Разница — в том, *что* провайдер делает (см. §4).

---

## 2. Как устроена готовая eID-платформа (факт, по коду)

Ниже — то, что уже реализовано (стори EID-01, 03…08, 🟢 Done) и переиспользуется как образец.

```
                         ┌───────────────────────── .env ─────────────────────────┐
                         │ EID_PROVIDER=mock|authentigate   AUTHENTIGATE_* / ...    │
                         └───────────────────────────┬─────────────────────────────┘
                                                      │ выбирает активного
   HTTP (браузерный redirect-флоу)                    ▼
   ┌────────────────┐   start    ┌─────────────────────────────┐   build_registry   ┌──────────────────────┐
   │ SPA / клиент    │──────────▶│ Оркестратор (handlers.py)    │◀──────────────────│ EIDProviderRegistry  │
   │                 │           │ handle_auth_eid_start        │   get_active()     │ (active + mock)      │
   │  redirect ⟶ IdP │           │ handle_auth_eid_callback     │──────────────────▶│  EIDProviderPort     │
   └────────────────┘   callback └──────────────┬──────────────┘   start/handle     └──────────┬───────────┘
                                                │                                              │ build(runtime)
                                  пишет флаг ▼  │                                    ┌──────────▼───────────┐
                          ┌──────────────────────────┐                              │ ProviderRuntime       │
                          │ ProfileRepository         │                              │ config, session_store │
                          │ profile.eid_verified=true │                              │ http_client, oidc,    │
                          │ verified_person_hash, ... │                              │ secret_box, settings  │
                          └──────────────────────────┘                              └───────────────────────┘
            VerificationSessionStore (create/get_by_state/mark_consumed) ── состояние между start и callback
            EidErrorCode (канон ошибок) · hash_secret (анти-Sybil hash) · EIDAuditEvent (аудит)
```

**Кто за что отвечает (реальные файлы):**
- Контракт провайдера `EIDProviderPort` — [`base.py`](../../src/core/providers/base.py): `provider_name`, `callback_path`, `start_flow(...)`, `handle_callback(...)`.
- Дескриптор + конфиг-спека + DI-контекст — [`descriptor.py`](../../src/core/providers/descriptor.py), [`config_spec.py`](../../src/core/providers/config_spec.py), [`runtime.py`](../../src/core/providers/runtime.py).
- Реестр и сборка активного — [`registry.py`](../../src/core/providers/registry.py), [`registry_builder.py`](../../src/core/providers/registry_builder.py) (`build_registry`, guard `ProviderNotRegisteredError`).
- Оркестрация флоу — [`handlers.py`](../../src/core/api/handlers.py) (`handle_auth_eid_start`/`handle_auth_eid_callback`).
- Состояние флоу — `VerificationSession` + `VerificationSessionStore` ([`models.py`](../../src/core/domain/models.py), [`contracts.py`](../../src/core/domain/contracts.py)).
- Канон — `EidErrorCode`, `EIDVerificationResult` ([`base.py`](../../src/core/providers/base.py)); анти-Sybil — `hash_secret` ([`hashing.py`](../../src/core/security/hashing.py)).
- Флаг в профиле — `ProfileRecord.eid_verified` / `verified_person_hash` / `eid_verified_at` ([`models.py:23-40`](../../src/core/domain/models.py)).

**Особенность eID:** провайдер «толстый» — он сам ведёт криптопротокол (OIDC/PKCE, обмен `code`→токены, валидация `id_token`), а флоу **браузерный** (пользователь уходит на IdP и возвращается через `/auth/{provider}/callback` с redirect назад в SPA).

---

## 3. Как зеркалим под телефон (проект)

Та же скелетная схема, но **провайдер тоньше**, и **нет браузерного redirect** — вместо «ухода к IdP» два обычных API-вызова: запросить код и подтвердить код.

```
                         ┌───────────────────────── .env ─────────────────────────┐
                         │ SMS_PROVIDER=mock|telnyx                                 │
                         │ PHONE_ALLOWED_DIAL_PREFIXES=+372        TELNYX_* / ...    │
                         └───────────────────────────┬─────────────────────────────┘
                                                      │ выбирает активного
   HTTP (без redirect, 2 вызова)                      ▼
   ┌────────────┐ 1.request ┌─────────────────────────────┐  build_registry   ┌──────────────────────┐
   │ SPA / клиент│─────────▶│ Оркестратор (phone flow)     │◀─────────────────│ SmsSenderRegistry    │
   │            │           │ handle_phone_request          │  get_active()     │ (active + mock)      │
   │ вводит код │ 2.confirm │ handle_phone_confirm          │──── send(code) ──▶│  SmsSenderPort       │
   │            │─────────▶ └──────────────┬──────────────┘                    └──────────┬───────────┘
   └────────────┘                          │                                              │ build(runtime)
                              пишет флаг ▼  │  (генерит OTP, сверяет код — это ЯДРО)       │
                       ┌────────────────────────────┐                          ┌──────────▼───────────┐
                       │ ProfileRepository           │                          │ SmsProviderRuntime    │
                       │ profile.phone_verified=true │                          │ config, session_store │
                       │ verified_phone_hash, ...    │                          │ http_client, settings │
                       └────────────────────────────┘                          └───────────────────────┘
            PhoneVerificationSessionStore (create/get/mark_consumed/attempts) ── состояние между request и confirm
            SmsErrorCode (канон) · hash_secret (анти-Sybil hash номера) · PhoneAuditEvent (аудит)
```

**Ключевой сдвиг ответственности:** SMS-провайдер умеет ровно **одно — доставить сообщение** (`send(phone, text)`). Генерация OTP, хранение его хэша, сверка введённого кода, счётчик попыток, срок жизни — это **логика ядра** (provider-agnostic), а не провайдера. Поэтому `SmsSenderPort` намного тоньше, чем `EIDProviderPort`.

---

## 4. Сопоставление eID ↔ Phone (что зеркалим, что меняется)

| Аспект | eID (есть) | Phone (проект) | Комментарий |
|--------|------------|----------------|-------------|
| Контракт провайдера | `EIDProviderPort`: `start_flow` + `handle_callback` (ведёт протокол) | `SmsSenderPort`: `send(phone, text)` — только доставка | провайдер телефона **тоньше** (SRP) |
| Кто доказывает личность | внешний IdP (OIDC) | ядро: владение номером через OTP | разный уровень доверия |
| Транспорт флоу | браузерный redirect → callback → 303 назад | 2 JSON-вызова: `request` + `confirm`, без redirect | **проще**: не нужны EID-06 redirect, OIDC-тулкит, PKCE/secret_box |
| Выбор активного | `EID_PROVIDER` в `.env` | `SMS_PROVIDER` в `.env` | тот же паттерн |
| Plugin-механика | descriptor + config_spec + registry + `build_registry` | те же абстракции, **отдельные классы** для SMS | mirror, не reuse классов eID |
| DI-контекст | `ProviderRuntime` (config, store, http, oidc, secret_box, settings) | `SmsProviderRuntime` (config, store, http, settings) — без oidc/secret_box | меньше зависимостей |
| Список стран | `AUTHENTIGATE_COUNTRY` (на провайдере) | `PHONE_ALLOWED_DIAL_PREFIXES` в `.env` (на **ядре**) | проверяет ядро до отправки SMS (+ whitelist у Telnyx, §10.2) |
| Состояние флоу | `VerificationSession` + store | `PhoneVerificationSession` + store (+ `attempts`) | mirror + счётчик попыток |
| Канон ошибок | `EidErrorCode` | `SmsErrorCode` | отдельный enum |
| Результат | `EIDVerificationResult(country, subject_hash, login_method, …)` | `PhoneVerificationResult(country_code, subject_hash=hash(phone), …)` | subject_hash = хэш E.164-номера |
| Флаг в профиле | `eid_verified` / `verified_person_hash` / `eid_verified_at` | `phone_verified` / `verified_phone_hash` / `phone_verified_at` | новые колонки (миграция) |
| Анти-Sybil | `hash_secret(country:idcode)` | `hash_secret(e164_phone)` | переиспользуем `hash_secret` |
| Аудит | `EIDAuditEvent` | `PhoneAuditEvent` (или общий) | mirror |

---

## 5. Поток данных телефона (request → confirm)

```
1) POST /auth/phone/request   (Bearer JWT)         2) POST /auth/phone/confirm   (Bearer JWT)
   body: { phone: "+372..." }                          body: { code: "123456" }
        │                                                    │
        ▼                                                    ▼
   нормализовать в E.164                               найти активную сессию юзера
        │                                                    │
   код страны ∈ PHONE_ALLOWED_COUNTRY_CODES?            статус=started? не истекла? attempts<N?
   нет → SmsErrorCode.COUNTRY_NOT_ALLOWED                    │
        │ да                                            сверить hash(code) == session.code_hash
   сгенерировать OTP (6 цифр)                                ├─ нет  → attempts++ (≥N → TOO_MANY_ATTEMPTS) → CODE_MISMATCH
   создать PhoneVerificationSession                          └─ да   → profile.phone_verified=true,
     { phone_hash, country_code, code_hash,                            verified_phone_hash, phone_verified_at
       status=started, attempts=0, expires_at=+5мин }        mark_consumed(session); audit success
        │                                                    return { status: "verified" }
   SmsSenderRegistry.get_active().send(phone, code)
        │  ошибка доставки → SmsErrorCode.SEND_FAILED
   audit "phone_request_sent"; return { sent, expires_at }
```

Никакого внешнего redirect: SPA после `request` показывает поле ввода кода, после `confirm` — результат. (Это и есть упрощение относительно eID-06.)

---

## 6. Что создаём и что переиспользуем

**Создать (зеркало `providers/`, отдельный пакет `src/core/phone/` — решено, см. §10):**
- `SmsSenderPort` (Protocol) + `SmsSendResult` + `SmsSenderError(code: SmsErrorCode)`.
- `SmsProviderDescriptor` + `SmsProviderConfigSpec` + `SmsProviderRuntime` + `SmsSenderRegistry` + `build_sms_registry` (по образцу [`registry_builder.py`](../../src/core/providers/registry_builder.py)).
- `MockSmsSender` (dev, «отправка» в лог/память — как `mock` eID).
- **Боевой провайдер: Telnyx** (`TelnyxSmsSender`) — первый, по [спеке Telnyx](telnyx-integration-spec-dogestonia-2026-06-10.md).
- Ядро флоу: `handle_phone_request` / `handle_phone_confirm` (по образцу [`handlers.py`](../../src/core/api/handlers.py)); OTP-генерация, нормализация E.164, проверка дозвонного префикса, **дедупликация номера (один номер = один аккаунт)**, rate-limit на отправку.
- `PhoneVerificationSession` + store; `PhoneVerificationResult`; `SmsErrorCode`.
- Колонки профиля `phone_verified` / `verified_phone_hash` / `phone_verified_at` (+ миграция, по образцу [`20260525000001_create_profiles.sql`](../../supabase/migrations/)).
- Роуты `POST /auth/phone/request`, `POST /auth/phone/confirm`.
- **Приём статуса доставки (решено — в MVP):** webhook-эндпоинт Telnyx + хранение статуса доставки по `provider_message_id` (см. §10).

**Переиспользуем как есть:** `hash_secret` (анти-Sybil), `ProfileRepository`/`/me`-механику (добавить поля), паттерн делегированной валидации конфига, аудит-подход, deployment.

**НЕ нужно для телефона:** OIDC-тулкит, `SessionSecretBox`/PKCE, redirect-рендеринг (EID-06), `callback_path` — всё это eID-специфично.

---

## 7. Конфигурация `.env` (зеркало EID-блока, значения зафиксированы — §10)

```env
# --- Phone verification (ядро, provider-agnostic) ---
SMS_PROVIDER=mock                       # активный провайдер: mock | telnyx
PHONE_ALLOWED_DIAL_PREFIXES=+372        # разрешённые дозвонные префиксы E.164, список через запятую (фильтр в ядре ДО отправки)
PHONE_CODE_LENGTH=6                     # длина OTP
PHONE_CODE_TTL_S=300                    # срок жизни кода (5 минут)
PHONE_MAX_ATTEMPTS=5                    # попыток ввода кода до блокировки сессии
PHONE_RESEND_COOLDOWN_S=60              # минимум между повторными отправками (анти-спам SMS)
PHONE_ONE_ACCOUNT_PER_NUMBER=true       # один номер = один аккаунт (дедупликация)

# --- Telnyx (заполнить при SMS_PROVIDER=telnyx) ---
TELNYX_API_KEY=
TELNYX_API_BASE_URL=https://api.telnyx.com
TELNYX_FROM=DOGEstonia                  # буквенный отправитель (alphanumeric sender ID)
TELNYX_MESSAGING_PROFILE_ID=            # обязателен при буквенном TELNYX_FROM
# (другой SMS-провайдер позже — свой блок, как у eID EIDEASY_*/AUTHENTIGATE_*)
```

- Членство `SMS_PROVIDER` валидируется по списку зарегистрированных SMS-дескрипторов; обязательные поля активного провайдера — его `config_spec` (делегированная валидация, fail-fast).
- **Условная валидация Telnyx:** если `TELNYX_FROM` буквенный (не E.164) → `TELNYX_MESSAGING_PROFILE_ID` обязателен (требование Telnyx для alphanumeric sender).
- Фильтр стран в ядре — по **дозвонному префиксу** (`+372`), т.к. номер в E.164 несёт префикс, а не ISO-код страны (`EE`). Это снимает дрейф имён из спеки Telnyx.

---

## 8. Ключевые архитектурные решения (✅ подтверждены, см. §10)

1. **Тонкий `SmsSenderPort` (только `send`), OTP-логика в ядре.** Почему: доставка SMS — единственное, что отличается между провайдерами; генерация/сверка кода одинакова → держим её в ядре (SRP, DRY). Альтернатива (толстый провайдер «verify») — лишняя дупликация и риск рассинхрона.
2. **Отдельный модуль `src/core/phone/`, а не обобщение eID-классов.** Почему: eID отложен, но вернётся; телефон — «отдельный функционал». Низкая связанность позволяет включить eID обратно без конфликтов. Если появится **третий** метод верификации — тогда рассмотреть вынос общего «verification-kernel» (YAGNI до того).
3. **Список стран — в ядре (`PHONE_ALLOWED_DIAL_PREFIXES`), проверка ДО отправки SMS.** Почему: экономит деньги (не шлём в неразрешённые страны) и провайдер-агностично. Дублируется whitelist'ом у Telnyx (§10.2).
4. **subject_hash = `hash_secret(E.164)`; отдельный флаг `phone_verified`; один номер = один аккаунт (P1).** Почему: анти-Sybil по номеру, не смешиваем с eID-идентичностью; явный отдельный флаг (eID вернём — будут сосуществовать). Trade-off честно: телефон слабее eID (один человек может иметь несколько номеров / виртуальные номера) — осознанный компромисс; дедуп номера поднимает планку.
5. **Без redirect — два JSON-вызова.** Почему: SMS-флоу challenge-response, браузер никуда не уходит → не нужны redirect-оркестрация/OIDC/PKCE. Существенное упрощение против eID.

## 9. Открытые вопросы — РАЗРЕШЕНЫ (2026-06-11)
- Модуль → `src/core/phone/` ✅. Боевой провайдер → **Telnyx** ✅. Привязка к залогиненному (Bearer JWT) → да ✅. Rate-limit на `request` → да (`PHONE_RESEND_COOLDOWN_S`) ✅. Детали продуктовых решений — §10.

---

## 10. Уточнения по итогам спеки Telnyx + продуктовые решения (2026-06-11)

> База: [`telnyx-integration-spec-dogestonia-2026-06-10.md`](telnyx-integration-spec-dogestonia-2026-06-10.md). Архитектура **не меняется** — «тонкий» `SmsSenderPort` подтверждён; уточняются детали и зафиксированы продуктовые решения.

### 10.1. Продуктовые решения (интервью 2026-06-11)
| # | Решение | Влияние |
|---|---------|---------|
| P1 | **Один номер = один аккаунт** (`PHONE_ONE_ACCOUNT_PER_NUMBER=true`) | если `verified_phone_hash` уже на другом профиле → конфликт `409` (зеркало eID `ProfileConflictError`). Усиливает анти-Sybil |
| P2 | **Отслеживание доставки — в MVP** | webhook-эндпоинт Telnyx + хранение статуса по `provider_message_id` входит в MVP-объём (не откладываем) |
| P3 | **Правила кода — «Стандарт»** | 6 цифр, TTL 5 мин, 5 попыток, повтор не чаще 60 сек |
| P4 | **Отправитель — буквенный «DOGEstonia»** (alphanumeric) | требует `TELNYX_MESSAGING_PROFILE_ID` + верификации аккаунта Level-2; SMS односторонняя (для OTP норма) |

### 10.2. Уточнения из спеки Telnyx, влияющие на ядро
- **Два «гейта» по стране:** наш `PHONE_ALLOWED_DIAL_PREFIXES` (бизнес-фильтр ДО отправки) + whitelist стран на Messaging Profile у Telnyx (иначе ошибки `40309/40331`). Оба нужны; коды `40309/40331` → `COUNTRY_NOT_ALLOWED`.
- **Подтверждение приёма синхронно, доставка — асинхронно:** `send` возвращает `accepted=True` при HTTP 200 + `data.id` + `data.to[0].status ∈ {queued, sent}`. Финальный исход — через webhook (P2).
- **Нет идемпотентности `POST /v2/messages`:** не делать слепой ретрай; сессию создавать ДО отправки; повтор — только через `PHONE_RESEND_COOLDOWN_S`, старый код инвалидируется.
- **Нет sandbox:** юниты — на `MockSmsSender`/замоканном HTTP; live — на trial Telnyx (на верифицированный номер). `TELNYX_API_BASE_URL` оставить конфигурируемым для фейкового сервера в тестах.
- **Rate-limit Telnyx ~0.1 MPS на один буквенный sender** (≈1 SMS/10 сек). Для MVP-объёма OTP достаточно; наш `PHONE_RESEND_COOLDOWN_S=60` сильно ниже. ⚠️ **Scaling-нота:** общий sender на всех пользователей → при росте всплески могут упираться в `40318 queue full`; тогда увеличивать лимиты у Telnyx / менять стратегию sender.

### 10.3. Влияние на план стори (PV-*)
- **PV-02** (config): фильтр по `PHONE_ALLOWED_DIAL_PREFIXES`; условная валидация Telnyx (буквенный `from` → нужен profile_id).
- **PV-03** (OTP-движок/сессия): значения «Стандарт» (P3); инвалидация старого кода при повторе.
- **PV-04** (профиль): дедуп-конфликт `409` (P1) — зеркало `ProfileConflictError`/`get_by_verified_person_hash`.
- **PV-05** (flow API): `PHONE_RESEND_COOLDOWN_S`; маппинг `40309/40331→COUNTRY_NOT_ALLOWED`.
- **PV-06** (Telnyx-адаптер): `send` по спеке; маппинг ошибок; condition profile_id.
- **PV-08** (delivery webhook): **переходит из «опционально/потом» в MVP** (P2).
- **SPIKE**: добавить Level-2 верификацию аккаунта и whitelist Эстонии на Messaging Profile.

### 10.4. Осталось подтвердить на SPIKE (не блокеры кода)
Точные числовые коды ошибок Telnyx и account-specific лимиты — взять из реального ответа при ручном тесте; нужен ли brand-proof для `DOGEstonia`; точный лейбл whitelist Эстонии в портале. (Список — §8 спеки Telnyx.)

---

## Связанные документы
- eID-платформа (образец, Done): [`EPIC-IDS-EID.md`](../tasks/backlog-stories/eid/EPIC-IDS-EID.md)
- Отложенное eID-подключение: [`eid-deferred/README.md`](../tasks/backlog-stories/eid-deferred/README.md)
- Парадигма провайдеров: [`runtime-docs/06-eid-providers.md`](../runtime-docs/06-eid-providers.md)
- Потребности кода (eID, как контекст контракта): [`eid-provider-integration-needs-2026-06-07.md`](eid-provider-integration-needs-2026-06-07.md)
