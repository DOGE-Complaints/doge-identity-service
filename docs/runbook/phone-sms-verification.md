# Runbook: верификация телефона по SMS — настройка и smoke-проверка

> **Для кого.** Для человека, который хочет настроить и «прощупать» (smoke-test) механизм отправки SMS-кода и полный процесс OTP-верификации.
> **Два режима:** **A — mock** (локально, бесплатно, без реальных SMS) и **B — live Telnyx** (настоящая SMS на телефон, после настройки аккаунта Telnyx, см. [SPIKE-IDS-PV-08](../tasks/backlog-stories/phone-verification/SPIKE-IDS-PV-08-telnyx-account-setup.md)).
> **Что проверяем.** Пользователь вводит номер → получает 6-значный код по SMS → вводит код → в профиле ставится `phone_verified=true`.
> Аудит реализации: [`phone-verification-code-audit-2026-06-11.md`](../analysis/phone-verification-code-audit-2026-06-11.md).

---

## 0. Словарик
- **OTP** — одноразовый код из SMS (One-Time Password).
- **mock-провайдер** — «ненастоящий» отправитель: ничего реально не шлёт, а запоминает SMS в памяти процесса. Для отладки без затрат.
- **Bearer JWT** — токен авторизации в заголовке `Authorization: Bearer <token>`; эндпоинты телефона защищены и требуют его (как «вошедший пользователь»).
- **E.164** — международный формат номера с `+` и кодом страны, напр. `+37255555555`.

---

## 1. Эндпоинты (что дёргаем)
| Метод | Путь | Назначение | Тело |
|------|------|-----------|------|
| POST | `/auth/phone/request` | запросить код (шлёт SMS) | `{"phone":"+372..."}` |
| POST | `/auth/phone/confirm` | подтвердить код | `{"phone":"+372...","code":"123456"}` |
| GET | `/me` | проверить флаг `phone_verified` | — |
| POST | `/webhooks/telnyx/messaging` | статусы доставки от Telnyx (только live) | приходит от Telnyx |

Успех `/request` → `200 {"data":{"sent":true,"expires_at":"...Z"}}`. **Код в ответе НЕ приходит** (специально, ради безопасности). Ошибки → `{"error":{"code":"COUNTRY_NOT_ALLOWED|RATE_LIMITED|CODE_MISMATCH|CODE_EXPIRED|TOO_MANY_ATTEMPTS|..."}}`.

---

## 2. Подготовка `.env`

### Общее (ядро)
```env
APP_PROFILE=demo
SMS_PROVIDER=mock                 # mock | telnyx
PHONE_ALLOWED_DIAL_PREFIXES=+372  # разрешённые префиксы, через запятую
PHONE_CODE_LENGTH=6
PHONE_CODE_TTL_S=300
PHONE_MAX_ATTEMPTS=5
PHONE_RESEND_COOLDOWN_S=60
PHONE_ONE_ACCOUNT_PER_NUMBER=true
```

### Режим B (добавить только для live Telnyx)
```env
SMS_PROVIDER=telnyx
TELNYX_API_KEY=KEY_xxx
TELNYX_API_BASE_URL=https://api.telnyx.com
TELNYX_FROM=DOGEstonia
TELNYX_MESSAGING_PROFILE_ID=<profile-uuid>   # обязателен при буквенном TELNYX_FROM
```
Значения берутся из [SPIKE-IDS-PV-08](../tasks/backlog-stories/phone-verification/SPIKE-IDS-PV-08-telnyx-account-setup.md).

Проверить, что подхватилось: `make check-env`.

---

## 3. Запуск сервиса
```bash
make serve     # поднимает API на http://127.0.0.1:8100
# проверка живости:
curl -s http://127.0.0.1:8100/health
```

## 4. Тестовый токен (нужен для обоих режимов)
Эндпоинты требуют Bearer JWT, подписанный ключом из JWKS вашего Supabase-проекта. Для локальной разработки используйте реальный access token после login в Supabase Auth или offline-харнес из [`tests/supabase_jwt_harness.py`](../../tests/supabase_jwt_harness.py) (ES256 + mock JWKS).

Для ручного smoke с реальным Cloud-проектом: залогиньтесь через Supabase Auth и возьмите `access_token` из session.

Скопировать в переменную: `TOKEN=<access_token>`.
> `iss` токена должен быть `<SUPABASE_URL>/auth/v1`, `aud=authenticated`, `role=authenticated`.

---

## 5. Режим A — mock (локально, бесплатно)

### 5A.1. Быстрый полный smoke (рекомендуется) — через тесты
Полный процесс request→SMS→confirm→`/me` уже автоматизирован (mock внутри процесса, где код доступен коду теста):
```bash
make test                                              # весь offline-набор
# или точечно полный OTP-флоу:
.venv/bin/python -m pytest tests/test_phone_verification_flow.py -v
```
Зелёный прогон = механизм работает end-to-end на mock.

### 5A.2. API-smoke через curl (что можно и чего нельзя)
При поднятом сервере (`SMS_PROVIDER=mock`):
```bash
# 1) запросить код — проверяем, что флоу/отправка SMS отрабатывают:
curl -s -X POST http://127.0.0.1:8100/auth/phone/request \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"phone":"+37255555555"}'
#   → ожидаем 200 {"data":{"sent":true,"expires_at":"...Z"}}
```
> ⚠️ **Подтвердить код (`/confirm`) через curl в mock-режиме нельзя** — mock реально SMS не шлёт, а код по дизайну не возвращается и не логируется. Для проверки `/confirm` в mock используйте путь 5A.1 (тест). Полный «живой» curl request→confirm доступен **только в режиме B** (там код приходит реальной SMS).

Негативы, которые можно прогнать curl'ом в mock:
```bash
# чужая страна → COUNTRY_NOT_ALLOWED (400)
curl -s -X POST .../auth/phone/request -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" -d '{"phone":"+15555555555"}'
# повтор сразу же → RATE_LIMITED (400)  (повторить запрос с +372 второй раз подряд)
```

---

## 6. Режим B — live Telnyx (настоящая SMS)
Предусловие: выполнен [SPIKE-IDS-PV-08](../tasks/backlog-stories/phone-verification/SPIKE-IDS-PV-08-telnyx-account-setup.md) (аккаунт, Level-2, Messaging Profile с Эстонией и sender `DOGEstonia`), `.env` из §2 (режим B), сервис перезапущен.

```bash
# 1) запросить код — на телефон придёт реальная SMS:
curl -s -X POST http://127.0.0.1:8100/auth/phone/request \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"phone":"+372XXXXXXXX"}'         # ваш тестовый номер (для trial — верифицированный)
#   → 200 {"data":{"sent":true,"expires_at":"..."}}

# 2) подсмотреть код в пришедшей SMS, затем подтвердить:
curl -s -X POST http://127.0.0.1:8100/auth/phone/confirm \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"phone":"+372XXXXXXXX","code":"123456"}'
#   → 200 {"data":{"status":"verified"}}  (поле статуса см. в ответе)

# 3) проверить флаг в профиле:
curl -s http://127.0.0.1:8100/me -H "Authorization: Bearer $TOKEN"
#   → "phone_verified": true, "phone_provider": "telnyx"
```

**Прямой smoke только отправки (без нашего API)** — если нужно проверить сами creds/sender Telnyx, см. cURL из спеки [`telnyx-integration-spec-dogestonia-2026-06-10.md`](../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md) §2.5 (`POST https://api.telnyx.com/v2/messages`).

### (Опц.) Доставка — webhook
Telnyx присылает статусы доставки на `POST /webhooks/telnyx/messaging` (нужен публичный URL и настроенный в профиле webhook). Это для наблюдаемости; на саму верификацию не влияет.

---

## 7. Если что-то не так (быстрая таблица)
| Симптом | Причина | Что делать |
|---------|---------|-----------|
| `401` на `/auth/phone/*` | нет/неверный Bearer токен | сминтить токен (§4); проверить секрет/iss |
| `error.code = COUNTRY_NOT_ALLOWED` | префикс номера не в `PHONE_ALLOWED_DIAL_PREFIXES` (или не в whitelist Telnyx) | добавить префикс в `.env` (и в Messaging Profile для live) |
| `error.code = RATE_LIMITED` | повтор быстрее `PHONE_RESEND_COOLDOWN_S` | подождать (по умолч. 60 сек) |
| `error.code = CODE_MISMATCH/CODE_EXPIRED/TOO_MANY_ATTEMPTS` | неверный/просроченный код или лимит попыток | запросить новый код |
| `409 profile_conflict` | номер уже подтверждён на другом аккаунте (P1) | это ожидаемо при `PHONE_ONE_ACCOUNT_PER_NUMBER=true` |
| `CONFIG_ERROR` при старте | для `SMS_PROVIDER=telnyx` не заданы обязательные `TELNYX_*` (или буквенный `from` без `MESSAGING_PROFILE_ID`) | заполнить `.env` (§2, режим B) |
| live: SMS не приходит | Telnyx: страна не в whitelist / sender не настроен / trial шлёт только на верифицированный номер | проверить Messaging Profile и SPIKE-08 |

---

## Связанное
- Аудит кода: [`phone-verification-code-audit-2026-06-11.md`](../analysis/phone-verification-code-audit-2026-06-11.md)
- Архитектура: [`phone-verification-architecture-2026-06-10.md`](../analysis/phone-verification-architecture-2026-06-10.md)
- Спека Telnyx: [`telnyx-integration-spec-dogestonia-2026-06-10.md`](../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md)
- Настройка Telnyx-аккаунта: [`SPIKE-IDS-PV-08`](../tasks/backlog-stories/phone-verification/SPIKE-IDS-PV-08-telnyx-account-setup.md)
