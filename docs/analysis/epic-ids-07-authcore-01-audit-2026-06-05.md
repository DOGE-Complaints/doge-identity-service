# Жёсткий аудит исполнения STORY-IDS-AUTHCORE-01 (`GET /me`)

> **Дата:** 2026-06-05
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-AUTHCORE-01-profile-and-me`](../tasks/backlog-stories/STORY-IDS-AUTHCORE-01-profile-and-me.md) vs фактический код. Реализована под **EPIC-IDS-07-auth-core** (pkg-000009), не «EPIC-IDS-AUTH-CORE».
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): EPIC-IDS-07, 6 tasks.

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Маршрут `/me` → хендлер | вызывает `handle_me` (не stub) — [`asgi_app.py:159-169`](../../src/core/api/asgi_app.py) |
| Реализация хендлера | `handle_me` читает `profile_repository` — [`handlers.py:55-76`](../../src/core/api/handlers.py) |
| Payload-билдер | `build_me_data` — [`me_response.py`](../../src/core/api/me_response.py) |
| Тесты `/me` | [`test_me_profile.py`](../../tests/test_me_profile.py) (4) + дубли в asgi/transport/jwt |
| **Offline-сюита** | **1 failed, 199 passed, 10 deselected** ⚠️ |

---

## 1. Статус исполнения story и тасков (актуализация)

Сверено по коду (не по индексу). Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo.

| Таск (EPIC-IDS-07) | Что проверял | Факт | Статус |
|--------------------|--------------|------|--------|
| t01 missing-profile decision | поведение «нет профиля» | синтетический 200, `eid_verified=false`, без записи в БД — [`handlers.py:61-63`](../../src/core/api/handlers.py), тест [`test_me_profile.py:98-114`](../../tests/test_me_profile.py) | 🟢 |
| t02 handle-me handler | `handle_me` существует и читает репозиторий | [`handlers.py:55-76`](../../src/core/api/handlers.py) | 🟢 |
| t03 me-response payload | билдер payload | [`me_response.py`](../../src/core/api/me_response.py) — 9 полей | 🟢 |
| t04 asgi route wire | маршрут вызывает `handle_me` | [`asgi_app.py:166`](../../src/core/api/asgi_app.py) | 🟢 |
| t05 me offline tests | оффлайн-тесты `/me` | [`test_me_profile.py`](../../tests/test_me_profile.py) — 401/200-with-profile/200-missing/envelope | 🟢 |
| t06 story acceptance | сверка AC | AC `/me` выполнены (см. §2); ⚠️ но в общей сюите 1 регресс (F1, не из `/me`) | 🟢 c оговоркой |
| **STORY-IDS-AUTHCORE-01** | story-level | реализована, AC выполнены | **🟢 Done** |

Индекс ([`bullrun-launch-index.md:40`](../tasks/bullrun-launch-index.md)) держит эпик как **🟡 In Progress (epic gate pending)** — корректно: story Done, гейт эпика не закрыт.

---

## 2. Сверка Acceptance Criteria story (по коду)

| AC story | Факт | Вердикт |
|----------|------|---------|
| `/me` без токена → 401 `AUTHENTICATION_REQUIRED` | `get_current_user` → 401; тест [`test_me_profile.py:73-76`](../../tests/test_me_profile.py) | ✅ |
| `/me` с валидным JWT → 200, `data` c `supabase_user_id`, `eid_verified`, поля профиля | [`me_response.py:17-34`](../../src/core/api/me_response.py); тест [`:79-95`](../../tests/test_me_profile.py) | ✅ |
| Нет профиля → детерминировано + тест | синтетический 200, без upsert; тест [`:98-114`](../../tests/test_me_profile.py) | ✅ |
| Envelope `{"data": {...}}` | `build_success_envelope`; тест [`:117-122`](../../tests/test_me_profile.py) | ✅ |
| Покрыто оффлайн на `in_memory` | `test_client` = in_memory | ✅ |

**Доп. устойчивость (сверх AC):** `handle_me` отдаёт `CONFIG_ERROR` 500, если `profile_repository is None` ([`handlers.py:66-72`](../../src/core/api/handlers.py)).

**Вывод:** функционально story **исполнена корректно и AC-полно**.

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| F1 | **MEDIUM** | Регрессия (тест) | offline-сюита красная: `test_access_app_with_incomplete_supabase_env_raises_config_error` не падает с `ConfigError` | [`test_asgi_import_config_isolation.py:28-41`](../../tests/test_asgi_import_config_isolation.py) |
| F2 | MEDIUM | Doc-stale | backlog-story помечена `⚪ Todo` / эпик `EPIC-IDS-AUTH-CORE`; реально 🟢 Done под `EPIC-IDS-07` | [`STORY-IDS-AUTHCORE-01...md:5-6,24`](../tasks/backlog-stories/STORY-IDS-AUTHCORE-01-profile-and-me.md) |
| F3 | LOW | Dead code | `handle_me_stub` больше не используется; в тексте — устаревший `EPIC-IDS-AUTH-CORE` | [`handlers.py:41-52`](../../src/core/api/handlers.py) |
| F4 | LOW | Scope-partial | scope обещал «+ базовые права»; в payload только `role` из JWT, отдельной модели прав нет | [`me_response.py:17-34`](../../src/core/api/me_response.py) |
| F5 | MEDIUM | Index-vs-факт | индекс фиксирует «200 pytest offline, 199 passed» и эпик «P3 Execute Done», но в сюите 1 падение (F1) | [`bullrun-launch-index.md:11`](../tasks/bullrun-launch-index.md) |
| F6 | MEDIUM | Security/hygiene | нет `.gitignore`; реальный `SUPABASE_SERVICE_ROLE` лежит в cwd `.env`, git его не игнорирует (сейчас untracked) | корень сервиса |

### F1 — детальный разбор регрессии (приоритет)

**Факт:** тест ожидает `ConfigError` при доступе к `asgi_app.app` с `DB_BACKEND=supabase`, `SUPABASE_URL=…` и **удалённым** `SUPABASE_SERVICE_ROLE` ([`test_asgi_import_config_isolation.py:28-41`](../../tests/test_asgi_import_config_isolation.py)). Падает: `DID NOT RAISE`.

**Корневая причина (верифицирована репро):** в корне сервиса появился реальный `.env` (создан 2026-06-04) с заполненным `SUPABASE_SERVICE_ROLE`. `provide_app_config` подмешивает cwd `.env` для ключей, отсутствующих в `os.environ` ([`config/providers.py:10-23`](../../src/core/config/providers.py) → [`env_file.py:9-29`](../../src/core/config/env_file.py)). Тест **сам удаляет** `SUPABASE_SERVICE_ROLE` из окружения → ключ становится «отсутствующим» → значение подтягивается из `.env` → условие `ConfigError` ([`schema.py:107-108`](../../src/core/config/schema.py)) не срабатывает.

**Прямой репро:** `provide_app_config()` при этом окружении вернул `db_backend=supabase` c непустым `supabase_service_role` (значение из `.env`), `asgi_app.app` собрался без ошибки.

**Важно:**
- Это **не дефект `/me`** — `handle_me`/`me_response` к падению отношения не имеют.
- В CI offline (`.github/workflows/test-offline.yml`, без `.env`) тест **прошёл бы** — падение **локальное**, спровоцировано наличием рабочего `.env`. Это слабость изоляции теста (autouse `_block_dotenv_leakage` не защищает, т.к. тест сам удаляет переменную, открывая merge из `.env`). Совпадает с латентной хрупкостью, отмеченной ранее в [epic-ids-06-audit](epic-ids-06-audit-2026-06-02.md) (F1).

**Как закрыть (направление, без реализации):** изолировать тест от cwd `.env` (например, отдельный рабочий каталог/переопределение чтения `.env`) ИЛИ переформулировать инвариант. Решение — за владельцем.

### F6 — пояснение
`git check-ignore .env` → не игнорируется; `.gitignore` в корне сервиса отсутствует. Сейчас `.env` **untracked** (в индекс не попал), утечки ещё нет, но защиты от случайного `git add` нет, а в файле — рабочий service_role-ключ. Severity MEDIUM (латентно).

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Прежние тесты `/me` (501-эра) | заменены: `test_me_with_stub_bearer_returns_501` отсутствует, вместо него `…returns_200_not_verified` ([`test_http_transport_smoke.py:79`](../../tests/test_http_transport_smoke.py), [`test_asgi_transport.py:63`](../../tests/test_asgi_transport.py)) — ожидаемо |
| `/me` 501→200 | поведенческая смена, согласована со story — не регресс |
| Offline-сюита | **1 падение (F1)** — средовое, не из `/me` |
| `handle_me_stub` | осиротел (F3), но не вызывает падений |

---

## 5. Итог

- **STORY-IDS-AUTHCORE-01 — 🟢 исполнена**, все 6 тасков Done подтверждены кодом, AC выполнены, есть доп. устойчивость (CONFIG_ERROR).
- **Блокеров в самой story нет.** Главное к вниманию — **F1** (красная offline-сюита из-за cwd `.env`) и **F6** (нет `.gitignore` при реальном секрете в `.env`).
- **Doc-долги:** F2 (устаревшая backlog-story), F3 (мёртвый stub), F5 (индекс рапортует зелёным при 1 падении).

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; статусы тасков сверены по коду, не по индексу.
- [x] Регрессия (F1) воспроизведена и локализована до корневой причины (cwd `.env` merge).
- [x] Severity проставлена; «как закрыть» — направление, без кода.
- [x] Расхождения индекс/код и doc-stale зафиксированы, не скрыты.

## P5 gap scaffold (2026-06-05)

- **Порог safe-override:** не пройден (6 gaps, 6 README paths) — секция в `ID_builder.plan.md` **не** добавлялась.
- **Pkg (draft):** [`pkg-000010-20260605-epic-ids-07-authcore-01-audit-gaps.yaml`](../tasks/identity-active-packages/pkg-000010-20260605-epic-ids-07-authcore-01-audit-gaps.yaml) — 6 tasks t07–t12.
- **activation:** [`pkg-000010`](../tasks/identity-active-packages/pkg-000010-20260605-epic-ids-07-authcore-01-audit-gaps.yaml) — P3 Execute Done 2026-06-05 (F1–F6 🟢, 200 pytest offline).
- **run_mode (index only):** `epic_ids_07_authcore_01_audit_2026_06_05`
