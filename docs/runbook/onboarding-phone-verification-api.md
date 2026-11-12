# Runbook — регистрация нового пользователя с верификацией телефона через API (без фронта)

> **Назначение:** полный no-frontend флоу «новый пользователь → подтверждённый телефон» последовательными HTTP-вызовами. Для ручной проверки, интеграционных тестов, отладки.
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только реальные эндпоинты/поля из кода; внешние (Supabase) и нереализованные (OAuth) части помечены явно.
> **Якоря:** [`asgi_app.py`](../../src/core/api/asgi_app.py) (роуты), [`handlers.py`](../../src/core/api/handlers.py) (`handle_phone_request`/`handle_phone_confirm`), [`me_response.py`](../../src/core/api/me_response.py).
> **Запуск сервера:** см. [`run-and-healthcheck.md`](./run-and-healthcheck.md).

---

## Карта флоу

```
[Supabase Auth]                         [doge-identity-service]
  (внешний, выдаёт JWT)
   0. signup/login по email  ──► access_token (Supabase JWT)
                                          │ Authorization: Bearer <jwt>
   1. POST /auth/phone/request {phone}  ──► SMS с OTP-кодом (через активный провайдер)
   2. (пользователь читает код из SMS)
   3. POST /auth/phone/confirm {phone,code} ──► phone_verified = true
   4. GET /me                            ──► профиль с "phone_verified": true
```

**Важно про роли сервисов:** регистрацию/логин и верификацию **email** делает **Supabase Auth** (внешний сервис). `doge-identity-service` сам signup не делает — он только **проверяет** Supabase JWT и ведёт верификацию **телефона**. Поэтому шаг 0 идёт к Supabase, шаги 1–4 — к identity.

---

## Предусловия

| Что | Откуда |
|-----|--------|
| Запущенный identity (`make serve`, `http://localhost:8100`) | [`run-and-healthcheck.md`](./run-and-healthcheck.md) |
| Supabase-проект (URL + anon key) | дашборд Supabase → Settings → API |
| `SUPABASE_URL` в env identity совпадает с проектом | [`.env.example`](../../.env.example), [`supabase-project-setup.md`](./supabase-project-setup.md) |
| Для **реального** SMS: `SMS_PROVIDER=telnyx` + `TELNYX_*` + эстонский номер | [`phone-sms-verification.md`](./phone-sms-verification.md) |

> **Профиль `pilot`** требует полный набор секретов (fail-fast `ConfigError`): см. [`run-and-healthcheck.md`](./run-and-healthcheck.md) §3.

---

## Шаг 0 — получить Supabase JWT (внешний, GoTrue)

Идентити требует `Authorization: Bearer <supabase_jwt>` ([security.py](../../src/core/api/security.py) `get_current_user`; токен с `role="authenticated"`, [supabase_validator.py:34](../../src/core/auth/supabase_validator.py)). Получаем его у Supabase Auth (GoTrue API). `$SB` = ваш `SUPABASE_URL`, `$ANON` = anon-ключ проекта.

**Регистрация по email+паролю:**
```bash
curl -s -X POST "$SB/auth/v1/signup" \
  -H "apikey: $ANON" -H "Content-Type: application/json" \
  -d '{"email":"newuser@example.com","password":"S3cret-pass"}'
```
- Если в Supabase включён **«Confirm email»** — в ответе **не будет** `access_token`: Supabase шлёт письмо со ссылкой, и токен выдаётся только **после** подтверждения email (пользователь кликает ссылку из письма). Это наш единый email-гейт (решение по UX — полагаемся на Supabase).
- Если «Confirm email» выключен — `access_token` приходит сразу.

**Логин (получить свежий токен по паролю):**
```bash
curl -s -X POST "$SB/auth/v1/token?grant_type=password" \
  -H "apikey: $ANON" -H "Content-Type: application/json" \
  -d '{"email":"newuser@example.com","password":"S3cret-pass"}'
# → {"access_token":"eyJ...","token_type":"bearer","expires_in":3600,...}
```

Сохраняем токен:
```bash
JWT="eyJ..."   # access_token из ответа выше
```

> Это **внешний** Supabase/GoTrue API, не код этого репозитория. Точные поля писем/редиректов настраиваются в дашборде Supabase (Auth → Email Templates / URL Configuration).

---

## Шаг 1 — запросить код на телефон

```bash
curl -s -X POST http://localhost:8100/auth/phone/request \
  -H "Authorization: Bearer $JWT" -H "Content-Type: application/json" \
  -d '{"phone":"+37255555555"}'
# 200 → {"data":{"sent":true,"expires_at":"2026-06-12T12:05:00+00:00"}}
```
Тело — JSON с полем `phone` ([asgi_app.py `_phone_payload_from_request`](../../src/core/api/asgi_app.py)). Сервер ([handlers.py:425](../../src/core/api/handlers.py)): нормализует номер в E.164 → проверяет дозвонный префикс (`PHONE_ALLOWED_DIAL_PREFIXES`, по умолчанию `+372`) → проверяет cooldown → создаёт сессию с OTP → шлёт SMS активным провайдером. Текст SMS формирует ядро ([sms_text.py](../../src/core/phone/sms_text.py)).

**Коды кода (TTL/попытки):** 6 цифр, TTL 300 с, 5 попыток, повтор не чаще 60 с — из `PHONE_CODE_LENGTH/TTL_S/MAX_ATTEMPTS/RESEND_COOLDOWN_S` ([schema.py](../../src/core/config/schema.py)).

---

## Шаг 2 — получить OTP-код

| Режим | Где код |
|-------|---------|
| `SMS_PROVIDER=telnyx` (боевой) | приходит **реальной SMS** на эстонский номер |
| `SMS_PROVIDER=mock` (demo) | **кода не достать** — он генерится на сервере, но **не возвращается в ответе и не пишется в лог** (анти-leak, [тест `test_plaintext_code_not_logged`](../../tests/test_phone_verification_flow.py)) |

> **Поэтому полный no-frontend проход «по сети» возможен только с Telnyx + реальным номером.** Для локальной проверки без SMS используйте offline-тест [`test_phone_verification_flow.py`](../../tests/test_phone_verification_flow.py) (`make test`), который строит сессию и читает код **в процессе** (in-memory), не по HTTP. Демо-«backdoor» для выдачи кода по API намеренно отсутствует.

```bash
CODE="123456"   # из полученной SMS
```

---

## Шаг 3 — подтвердить код

```bash
curl -s -X POST http://localhost:8100/auth/phone/confirm \
  -H "Authorization: Bearer $JWT" -H "Content-Type: application/json" \
  -d "{\"phone\":\"+37255555555\",\"code\":\"$CODE\"}"
# 200 → {"data":{"status":"verified"}}
```
Сервер ([handlers.py:506](../../src/core/api/handlers.py)): находит активную сессию пользователя → сверяет код (constant-time) → ставит `phone_verified=true` в профиле через `attach_phone_verification` (дедуп «один номер = один аккаунт») → `mark_consumed`.

---

## Шаг 4 — проверить результат

```bash
curl -s http://localhost:8100/me -H "Authorization: Bearer $JWT"
# {"data":{ ..., "phone_verified":true, "phone_dial_prefix":"+372", "phone_verified_at":"..." }}
```
`/me` ([me_response.py](../../src/core/api/me_response.py)) отдаёт `phone_verified`, `phone_provider`, `phone_dial_prefix`, `phone_verified_at` (а также `eid_verified`, `role`). Сырой номер/хэш **не** отдаются.

---

## Ошибки и коды (что вернёт API)

Канон ошибок — `SmsErrorCode` ([base.py](../../src/core/phone/base.py)); HTTP-маппинг — [`handlers.py` `_sms_error_http_status`](../../src/core/api/handlers.py) (400, кроме `PROVIDER_UNAVAILABLE`/`SEND_FAILED` → 503; конфликт номера → 409).

| Ситуация | Код / HTTP | Когда |
|----------|------------|-------|
| Иностранный номер (не `+372`) | `COUNTRY_NOT_ALLOWED` / 400 | префикс вне `PHONE_ALLOWED_DIAL_PREFIXES` |
| Повтор раньше 60 с | `RATE_LIMITED` / 400 | анти-спам SMS на `/request` |
| Неверный код | `CODE_MISMATCH` / 400 | `attempts++` |
| Просрочен (>5 мин) | `CODE_EXPIRED` / 400 | сессия → `expired` |
| Исчерпаны попытки (≥5) | `TOO_MANY_ATTEMPTS` / 400 | сессия → `failed` |
| Номер занят другим аккаунтом | `profile_conflict` / **409** | правило «один номер = один аккаунт» |
| Нет/битый JWT | `AUTHENTICATION_REQUIRED` / 401 | заголовок `Authorization` |
| Провайдер недоступен | `PROVIDER_UNAVAILABLE` / 503 | сбой/таймаут Telnyx |

Все события пишутся в аудит **без PII** (нет сырого номера/кода) — `PhoneAuditEvent`.

---

## Быстрый прогон одной строкой (Telnyx + свой номер)

```bash
JWT="eyJ..."; PHONE="+372XXXXXXXX"
curl -s -X POST localhost:8100/auth/phone/request -H "Authorization: Bearer $JWT" \
     -H 'Content-Type: application/json' -d "{\"phone\":\"$PHONE\"}" | jq
read -p "Код из SMS: " CODE
curl -s -X POST localhost:8100/auth/phone/confirm -H "Authorization: Bearer $JWT" \
     -H 'Content-Type: application/json' -d "{\"phone\":\"$PHONE\",\"code\":\"$CODE\"}" | jq
curl -s localhost:8100/me -H "Authorization: Bearer $JWT" | jq '.data.phone_verified'
```

---

## Чего этот флоу НЕ покрывает (по коду)
- **eID-верификацию** (`/auth/eid/start` + callback) — отдельный флоу, реальный провайдер отложен.
- **Вход из кастомного GPT** (`/oauth/*`) — сейчас **501-заглушки** (`EPIC-IDS-OAUTH` не построен). Целевой UX — в [`identity-onboarding-ux-2026-06-12.md`](../analysis/identity-onboarding-ux-2026-06-12.md).
- **email-верификацию** — полностью на стороне Supabase (шаг 0).

## Связанные документы
- [`run-and-healthcheck.md`](./run-and-healthcheck.md) — запуск/healthcheck/smoke.
- [`phone-sms-verification.md`](./phone-sms-verification.md) — Telnyx/`SMS_PROVIDER`.
- [`identity-onboarding-ux-2026-06-12.md`](../analysis/identity-onboarding-ux-2026-06-12.md) — целевой UX онбординга + gap.
