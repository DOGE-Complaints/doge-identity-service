# Продуктовое интервью: поля `/me` для кабинета (CAB-02) — 2026-07-13

> **Контекст:** depth-проход по MVP-гапу кабинета (extend `GET /me`). Стори: [`AUTHCORE-02`](../tasks/backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md) (`created_at`+`account_status`) и [`ONB-01`](../tasks/backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md) (`email`).
> **Источник контракта:** [`STORY-SPA-CAB-api-requirements §0`](../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-api-requirements.md).
> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc); решения приняты оператором, обоснованы кодом.
> **Назначение:** SSOT решений D-CAB-1…3 — референс для доводки стори.

## Сводка решений

| # | Тема | Решение | Стори |
|---|------|---------|-------|
| **D-CAB-1** | `account_status` | **Константа `"active"`** (без колонки/миграции); enum остаётся в контракте на будущее | AUTHCORE-02 |
| **D-CAB-2** | `created_at` | **`profiles.created_at` при наличии профиля, иначе `null`** (без доп. вызовов Supabase) | AUTHCORE-02 |
| **D-CAB-3** | `email_verified` | **Добавить `email_verified: true`** (политика «валидный токен ⇒ email подтверждён») | ONB-01 |

---

## Проверенные факты (по коду)
- Profile-строка **ленивая** — создаётся только при первой верификации телефона/eID ([`handlers.py:397,604`](../../src/core/api/handlers.py) → `upsert`), значит у только что зарегистрированного юзера **профиля нет** → `/me` отдаёт null по profile-полям ([`me_response.py:20-31`](../../src/core/api/me_response.py)).
- `profiles.created_at` = `DEFAULT NOW()` в момент создания строки ([`000_full_init.sql:61`](../../supabase/bootstrap/000_full_init.sql)) — т.е. «профиль впервые создан», **не** дата регистрации.
- Истинная дата регистрации — в Supabase `auth.users.created_at` (нет ни в JWT, ни в `public.profiles`).
- `account_status`-концепта нет нигде (grep пусто); механизма suspend/pending/archive не существует.
- `email` уже парсится в `UserClaims.email` ([`models.py:18`](../../src/core/domain/models.py)); в `/me` не выставляется.

---

## D-CAB-1 · `account_status` = константа `"active"`

**Решение:** `/me` всегда отдаёт `account_status: "active"`. Никакой колонки/миграции. Enum `active|pending|suspended|archived` остаётся в контракте (§0) для будущего.

**Почему.** В системе **нет ни одного механизма**, переводящего аккаунт в suspended/pending/archived — все юзеры фактически active. Колонка `profiles.account_status`, значение которой всегда `active`, была бы косметической (+ profile ленивый → новым юзерам всё равно нужен дефолт в ответе). Синтетическая константа честно отражает MVP-реальность и стоит ~1 строку.

**Аналитика / когда пересмотреть:** как только появится **реальный lifecycle** (бан/приостановка/архив) — тогда завести колонку `profiles.account_status` + CHECK-enum + миграцию отдельной стори. Сейчас это преждевременно (YAGNI).

**Изменяемый код:** [`me_response.py`](../../src/core/api/me_response.py) — `data["account_status"] = "active"` (в базовом dict, до `if profile`, т.к. верно и для no-profile).

---

## D-CAB-2 · `created_at` = `profiles.created_at` или `null`

**Решение:** `created_at` = `profiles.created_at`, когда профиль есть; **`null`**, когда профиля нет. Без обращения к Supabase Auth.

**Почему.** Настоящая `auth.users.created_at` семантически вернее, но требует запрос к Supabase Admin API / доступ к схеме `auth` под service_role — **+1 внешний вызов на `/me`** (хот-путь). Для MVP-кабинета это дорого; `profiles.created_at` доступно без доп. вызова.

**Аналитика / ограничения (задокументировать во фронт-контракте):**
- ⚠️ Семантика: это «дата создания профиля» (первая верификация телефона/eID), **не** дата регистрации. Для большинства верифицированных юзеров разница мала, но формально label «Account Created» неточен.
- ⚠️ У **новых юзеров без профиля** → `null` → фронт показывает placeholder («—»). Это норма для MVP (карточка неполная до первой верификации).
- Точную `auth.users.created_at` добавим позже, если потребуется (отдельная задача: Supabase Admin-запрос + кэш).

**Изменяемый код:** [`me_response.py`](../../src/core/api/me_response.py) — `created_at` в блок `if profile is not None:` через существующий `_format_datetime(profile.created_at)`; в базовом dict = `None`.

---

## D-CAB-3 · `email_verified: true` (ONB-01)

**Решение:** `/me` отдаёт `email_verified: true` — политика «есть валидный токен ⇒ Supabase подтвердил email».

**Почему.** При включённой в Supabase настройке **«Confirm email»** неподтверждённый пользователь не получает токен; раз identity видит валидный токен — email подтверждён. Явное поле убирает неявное предположение для UI/gateway.

**Аналитика / предусловие (критично):**
- Поле `email_verified:true` **истинно только если «Confirm email» включён** в Supabase. Поэтому оно **связано с runbook-требованием ONB-01**: [`supabase-project-setup.md`](../runbook/supabase-project-setup.md) должен мандатить включение «Confirm email» (Auth → Providers → Email). Если настройка выключена — утверждение ложно.
- Это **политика-константа**, а не проверка per-request (в токене нет `email_verified`-claim, на который мы бы опирались) → корректность держится на конфигурации проекта.

**Изменяемый код:** [`me_response.py`](../../src/core/api/me_response.py) — `data["email"] = current_user.email`; `data["email_verified"] = True`.

---

## Влияние на стори (доводка после отчёта)

| Стори | Правки от решений |
|-------|-------------------|
| **AUTHCORE-02** | `account_status="active"` (D-CAB-1, без миграции); `created_at` profile-or-null (D-CAB-2); субтаски: me_response + api-reference + `test_me_profile.py`; в §0-контракте пометить «MVP эмитит только `active`». |
| **ONB-01** | `email` + `email_verified:true` (D-CAB-3); субтаска runbook «Confirm email required» как предусловие; api-reference + тест. |
| **Координация** | Обе трогают [`me_response.py`](../../src/core/api/me_response.py) и [`api-reference`](../runtime-docs/api-reference/) + `test_me_profile.py` — делать согласованно (одна волна или явная очередь), иначе конфликт в билдере `/me`. |

**Общий вывод:** ни одно решение не требует **миграции БД** (D-CAB-1/2 используют существующее/константу; D-CAB-3 — константа). Весь identity-контракт CAB-02 закрывается правками `me_response.py` + доки/тесты — низкая сложность.
