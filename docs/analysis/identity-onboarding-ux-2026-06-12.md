# Целевой UX онбординга Identity + gap-анализ (интервью 2026-06-12)

> **Назначение:** зафиксировать целевое состояние UX Identity-модуля (две точки входа, гейты, disclosure) и gap к фактическому коду — чтобы решения не потерялись.
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — текущее состояние по коду (`file:line`); целевое — продуктовые решения интервью; gap с severity + как закрыть. Реализацию не предлагаем — фиксируем направление.
> **Роль источника:** продуктовое интервью (продакт), 2026-06-12. Термины расшифрованы в [§6 Глоссарий](#6-глоссарий).

---

## 1. Текущее состояние (зеркало по коду)

| Возможность | Эндпоинт / факт | Статус |
|-------------|-----------------|--------|
| Профиль по Supabase JWT | `GET /me` → `eid_verified`/`phone_verified`/`role` ([me_response.py](../../src/core/api/me_response.py)) | ✅ |
| Телефонная верификация (OTP) | `POST /auth/phone/request` + `/confirm` ([handlers.py:425,506](../../src/core/api/handlers.py)) | ✅ (mock; Telnyx PV-06; webhook PV-07) |
| Дедуп «один номер = один аккаунт» | `attach_phone_verification` → `ProfileConflictError`/409 ([repositories.py](../../src/core/infrastructure/repositories.py)) | ✅ |
| Только эстонские номера | префикс-гейт → `COUNTRY_NOT_ALLOWED` ([e164.py](../../src/core/phone/e164.py), `PHONE_ALLOWED_DIAL_PREFIXES=+372`) | ✅ |
| eID-верификация | `POST /auth/eid/start` + callback (mock) | 🟡 mock; реальный провайдер отложен |
| **Вход из GPT (OAuth)** | `/oauth/authorize`, `/oauth/authorize/complete`, `/oauth/token` → **501** (`EPIC-IDS-OAUTH`) | ❌ не построен |
| signup + верификация **email** | **нет в Identity** — это Supabase Auth (внешний); Identity только проверяет JWT ([08-ui-expectations.md](../runtime-docs/08-ui-expectations.md) §2) | ✅ (внешне) |
| `email_verified` в `/me` | Identity достаёт `email` из токена ([models.py:18](../../src/core/domain/models.py)), но статус подтверждения не выносит | ❌ нет поля |

---

## 2. Целевое состояние UX (решения интервью 2026-06-12)

Два **входа** (entry points), один аккаунт (один Supabase user), общий профиль с флагами `email`/`phone_verified`/`eid_verified`.

### Вход #1 — web signup (spa-app)
- Регистрация/логин **по email** через Supabase Auth. Телефон при регистрации **не спрашиваем**.
- **Ленивый гейт телефона (по действию):** телефон требуется только в момент, когда пользователь пытается выполнить **защищённое действие** (каноничный пример — создать/опубликовать стори). До этого аккаунт полноценно живёт без телефона.
- Гейт **энфорсит потребитель** (web/gateway), читая `phone_verified` из `/me`; Identity предоставляет флаг + флоу верификации.

### Вход #2 — редирект из кастомного GPT
- GPT инициирует **login или signup** с **обязательной** верификацией телефона: либо сразу при signup, либо «дозаполнение», если был логин, но `phone_verified=false`.
- **Где вводится номер и OTP:** **redirect в наш web** — GPT даёт ссылку → пользователь открывает нашу web-страницу верификации (вводит номер и код там) → возвращается в GPT уже верифицированным. Номер/код **не проходят через контекст GPT** (безопаснее).
- Технически вход GPT→Identity требует **OAuth** (см. §4 — сейчас 501). **На этом этапе только проектируем**; код OAuth — отдельный эпик.

### Email-гейт
- **Полагаемся на Supabase «Confirm email»:** при включённой настройке неподтверждённый email = нет токена = Identity такого юзера не видит. **Единый гейт в Supabase, без дублирования в Identity.**
- **Требование к конфигурации (зафиксировать):** в Supabase-проекте **включить «Confirm email»** (Auth → Providers → Email). Иначе токены выдаются неподтверждённым — гейт не работает.

### Disclosure «зачем телефон»
- **Где:** только **web-экран** верификации (перед вводом номера). В GPT-ветке disclosure тоже виден, т.к. ввод номера происходит на нашей web-странице (см. redirect).
- **Тон:** дружелюбный, человеческий, с пояснением пользы (анти-боты, защита экосистемы), без юридического канцелярита.
- **Драфт-копирайт (EN, канон; локализация ET/RU — follow-up):**
  > **One quick step — verify your phone**
  > We ask for your phone number to keep DOGEstonia free of bots and bad actors, so the people you interact with are real. We currently support **Estonian numbers (+372)** only — this is part of how we protect the integrity of our ecosystem.
  > Your number is stored only as a secure hash, never shown to others, and used once to confirm it's really you.
- **Граничные сообщения (UX-копирайт, драфт):**
  - Иностранный номер (`COUNTRY_NOT_ALLOWED`): *«Right now we support Estonian numbers (+372) only — it's part of keeping our ecosystem safe. Want us to open your country? Leave your email and we'll let you know.»* (**отказ + waitlist** — сбор email на расширение географии).
  - Номер занят (`profile_conflict`/409): *«This number is already in use. If it's you — sign in to that account; otherwise please use a different number.»* (**мягко «это вы?»**, без раскрытия чужого аккаунта).

**SSOT (DOC-IDS-ONB-02):** канон EN + привязка к кодам ошибок — [`onboarding-copy.md`](../runbook/onboarding-copy.md).

---

## 3. Целевые потоки (sequence, словами)

**#1 Web, ленивый гейт:**
```
signup/login (Supabase, email) → токен → пользуется системой без телефона
 → пытается «создать стори» → потребитель видит /me phone_verified=false
 → web-экран verify (disclosure) → POST /auth/phone/request → SMS OTP
 → POST /auth/phone/confirm → phone_verified=true → действие разрешено
```

**#2 GPT, обязательный телефон:**
```
в GPT: «войти/создать стори» → GPT редиректит в наш web (OAuth authorize)
 → spa /login?oauth_request_id=… → Supabase login/signup
 → POST /oauth/authorize/complete → если phone_verified=false: 403 + verify_url
 → /verify?context=… (disclosure) → request → OTP → confirm
 → повтор authorize/complete → 302 GPT redirect_uri?code=&state=
```
**SSOT контракт (DOC-IDS-ONB-03):** [`08-ui-expectations.md`](../runtime-docs/08-ui-expectations.md) §3c. OAuth (OAUTH-01…04) — **as-built**, не 501.

Технический no-frontend проход #1 (готов сегодня) — в [`onboarding-phone-verification-api.md`](../runbook/onboarding-phone-verification-api.md).

---

## 4. Gap-анализ (target ↔ код)

| # | Gap | Severity | Где | Как закрыть |
|---|-----|----------|-----|-------------|
| G1 | **OAuth-вход из GPT** | ~~HIGH~~ **CLOSED** | `/oauth/*` as-built (OAUTH-01…04) | — |
| G2 | **Нет `email_verified`/email-гейта** — целевое решение «полагаться на Supabase» требует включённой настройки, которая нигде не зафиксирована как требование | MEDIUM | `/me` без email-флага; нет runbook-пункта | Зафиксировать в [`supabase-project-setup.md`](../runbook/supabase-project-setup.md): **включить «Confirm email»**. (Опц.) вынести `email`/`email_verified` в `/me` для наглядности. |
| G3 | **«Ленивый гейт по действию» не специфицирован** — где и как потребитель требует телефон | ~~MEDIUM~~ **CLOSED** (DOC-ONB-01) | — | [`09-gateway-expectations`](../runtime-docs/09-gateway-expectations.md) + [`08-ui` §3b](../runtime-docs/08-ui-expectations.md) |
| G4 | **Disclosure-копирайт нигде не зафиксирован** | ~~MEDIUM~~ **CLOSED** (DOC-ONB-02) | — | [`onboarding-copy.md`](../runbook/onboarding-copy.md) |
| G5 | **Web-страница verify (для редиректа из GPT)** — контракт не зафиксирован | ~~MEDIUM~~ **CLOSED** (DOC-ONB-03) | — | [`08-ui-expectations.md`](../runtime-docs/08-ui-expectations.md) §3c |
| G6 | **Waitlist на не-EE страны** — целевое сообщение требует сбора email | LOW | в коде нет | Продуктовый бэклог: куда собирать (форма/таблица). Не блокер MVP. |
| G7 | **Стейл-доки:** [`01-api.md`](../runtime-docs/01-api.md) описывает OAuth как 501 и не упоминает phone-флоу/`/webhooks/telnyx` | LOW | `01-api.md` | Обновить таблицу маршрутов (добавить `/auth/phone/*`, `/webhooks/telnyx/messaging`; OAuth — пометить план). |
---

## 5. Решения интервью (лог, не потерять)

| Тема | Решение |
|------|---------|
| Web: когда телефон | **Лениво, по действию** (signup только email; телефон в момент защищённого действия) |
| GPT: где вводится OTP | **Redirect в наш web** (номер/код не через GPT-контекст) |
| Email-гейт | **Полагаться на Supabase «Confirm email»** (единый гейт, без дубля в Identity) |
| Disclosure: место | **Только web-экран** verify (он же виден GPT-ветке через redirect) |
| GPT/OAuth scope | **Только проектируем сейчас**; код OAuth — отдельный эпик |
| Номер занят (409) | **Мягко «это вы?»** — предложить вход в тот аккаунт / другой номер |
| Иностранный номер | **Отказ + waitlist** (сбор email на расширение географии) |

---

## 6. Глоссарий

- **Supabase Auth (GoTrue)** — внешний хостовый сервис аутентификации; шлёт письма подтверждения и выдаёт JWT. Формы рисует наш web.
- **JWT (Bearer-токен)** — подписанный пропуск пользователя; кладётся в заголовок `Authorization: Bearer …`. Identity его проверяет, сам не выдаёт.
- **OAuth** — протокол «войти через»; им ChatGPT Actions логинят пользователя в наш сервис и получают токен для вызовов API.
- **OTP** — одноразовый код (6 цифр), приходит по SMS; TTL 5 мин, 5 попыток.
- **Disclosure** — пояснение-обоснование «зачем нам это», показывается пользователю до запроса данных.
- **Ленивый гейт** — требование (телефон) включается не сразу, а в момент конкретного действия.
- **E.164 / дозвонный префикс** — международный формат номера (`+372…`); префикс = код страны.

## 7. Связанные документы
- [`08-ui-expectations.md`](../runtime-docs/08-ui-expectations.md) §3c — **SSOT** GPT verify landing + возврат в GPT (DOC-IDS-ONB-03).
- [`onboarding-copy.md`](../runbook/onboarding-copy.md) — **SSOT** disclosure + boundary copy (DOC-IDS-ONB-02).
- [`onboarding-phone-verification-api.md`](../runbook/onboarding-phone-verification-api.md) — no-frontend API-флоу телефонной верификации (готов сегодня).
- [`phone-verification-architecture-2026-06-10.md`](./phone-verification-architecture-2026-06-10.md) — архитектура телефонной платформы.
- [`09-gateway-expectations.md`](../runtime-docs/09-gateway-expectations.md) — контракты к gateway.
- [`project-gpt-intake-contract`] — решения по интеграции GPT (интервью 2026-05-17).
