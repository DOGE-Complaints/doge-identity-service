# Жёсткий аудит исполнения STORY-IDS-OAUTH-04 (verify-gate + `verification_required`)

> **Дата:** 2026-06-24
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-OAUTH-04-verify-gate-and-verification-required`](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md) vs фактический код. Исполнена под **EPIC-IDS-11** (pkg-000034), 7 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): Текущая волна pkg-000034, OAUTH-04 🟢 (стр.11,62,629-635).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Миграция context-колонок | [`20260624000002_oauth_authorization_request_context.sql`](../../supabase/migrations/20260624000002_oauth_authorization_request_context.sql) — `requested_action` + `return_context` + CHECK (`eid:verify`/`stories:submit`) |
| Нормализация/валидация действия | [`core/oauth/request_context.py`](../../src/core/oauth/request_context.py) — `ALLOWED_REQUESTED_ACTIONS`, `VERIFY_REQUIRED_ACTIONS={stories:submit}`, `normalize_*`, `action_requires_phone_verification` |
| Relay authorize→store | authorize парсит/нормализует/сохраняет ([handlers.py:46-62,94-95](../../src/core/oauth/handlers.py)); невалидное действие → `invalid_request` 400 |
| Relay через оба бэкенда | `_authorization_request_to_row`/`_from_row` пишут/читают обе колонки ([db_supabase.py:686-687,707-708](../../src/core/infrastructure/db_supabase.py)); in-memory — поля модели |
| Verify-gate (complete) | `action_requires_phone_verification` + `phone_verified` из профиля → 403 **до** `consume` ([handlers.py:126-137](../../src/core/oauth/handlers.py)) |
| Канон `verification_required` | [`core/oauth/verification_required.py`](../../src/core/oauth/verification_required.py) — `{error:"verification_required", reason, verify_url}`, HTTP **403** |
| `verify_url` | `build_spa_verify_url(return_context)` → `{base}/verify?context=…` ([spa_login.py:25-31](../../src/core/oauth/spa_login.py)) |
| Отделение от OTP-ошибок | коммент + 403 (не `SmsErrorCode` 400) ([verification_required.py:6-7](../../src/core/oauth/verification_required.py)) |
| Модель | `AuthorizationRequest.requested_action/return_context` ([models.py:11-12](../../src/core/domain/models.py)) |
| Тесты | [test_oauth_verify_gate.py](../../tests/test_oauth_verify_gate.py) — 6; migration — [test_supabase_migrations_sql.py:70-74](../../tests/test_supabase_migrations_sql.py) |
| **Offline-сюита** | **366 passed, 11 deselected** ✅ (совпадает с индексом) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-11, pkg-000034) | Факт | Статус |
|--------------------------------|------|--------|
| t01 oauth request context schema | миграция context-колонок + CHECK ([миграция](../../supabase/migrations/20260624000002_oauth_authorization_request_context.sql)) | 🟢 |
| t02 oauth authorize relay handlers | authorize relay + persist + cross-backend mappers | 🟢 |
| t03 oauth verify gate phone branch | `action_requires_phone_verification` + `phone_verified` → 403 до consume | 🟢 |
| t04 verification required contract | `verification_required.py` (`{error,reason,verify_url}`, 403) | 🟢 |
| t05 verify need vs sms error http mapping | 403 (authz) vs 400 (`SmsErrorCode`) разведены | 🟢 |
| t06 offline oauth verify gate tests | 6 тестов | 🟢 |
| t07 story acceptance verification | AC 5/5 (см. §2) | 🟢 |
| **STORY-IDS-OAUTH-04** | verify-gate + контракт | **🟢 Done** |

Индекс держит эпик корректно: `EPIC-IDS-11 … OAUTH-01 🟢; OAUTH-02 🟢; OAUTH-03 🟢; OAUTH-04 🟢` ([bullrun-launch-index.md:113](../tasks/bullrun-launch-index.md)); pkg-000034 Done, 366 offline (стр.11).

---

## 2. Сверка Acceptance Criteria story (по коду + тестам)

| AC | Факт (код + тест) | Вердикт |
|----|-------------------|---------|
| `requested_action`/`return_context` проходят authorize→complete и доступны после логина | сохранение ([handlers.py:94-95](../../src/core/oauth/handlers.py)), чтение в complete ([handlers.py:126,135](../../src/core/oauth/handlers.py)); тест `..._relay_persists_requested_action_and_return_context` | ✅ |
| При verify-требующем действии и `phone_verified=false` — сигнал «нужен verify», **без** «зелёного» статуса | 403 возвращается **до** `consume`/выдачи кода ([handlers.py:132-137](../../src/core/oauth/handlers.py)); тест `..._unverified_stories_submit_returns_verification_required` | ✅ |
| Канон `verification_required` (403) с `verify_url`; под `phone_verified`, не `eid_verified` | `{error:"verification_required", reason, verify_url}` ([verification_required.py:14-23](../../src/core/oauth/verification_required.py)); гейт по `profile.phone_verified` ([handlers.py:127-131](../../src/core/oauth/handlers.py)) | ✅ |
| verify-need (403) явно отделён от OTP-ошибок (`SmsErrorCode`, 400) | коммент-инвариант ([verification_required.py:6](../../src/core/oauth/verification_required.py)); тест `test_verification_required_separate_from_sms_error_http_mapping` | ✅ |
| Offline-тесты; контракт описан для gateway | 6 тестов; контракт в [`09-gateway-expectations §Контракт verification_required`](../runtime-docs/09-gateway-expectations.md) (стр.37-43) | ✅ |

**Доп. проверки:** верифицированный `stories:submit` → выдаёт код (тест `..._verified_stories_submit_issues_code`); действие без verify-требования → выдаёт код (тест `..._without_verify_requiring_action_issues_code`); невалидный `requested_action` → `invalid_request` (тест `..._rejects_invalid_requested_action`).

**Вывод:** все 5 AC выполнены и покрыты тестами (6). Verify-gate идемпотентен: при 403 запрос **не** consume'ится → после верификации телефона повтор `complete` с тем же `oauth_request_id` проходит.

---

## 3. Findings (severity + как закрыть; без реализации)

Код OAUTH-04 — без материальных дефектов. Findings — **doc-staleness** (рекуррентный паттерн).

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F1** | MEDIUM | Doc-stale (backlog-story) | Story `Status: ⚪ Todo` (стр.7) + AC `[ ]` (стр.32-36) + «Точки в коде»: «relay verify-need — scope OAUTH-04», «`verification_required` под phone — **не определён**» — реально 🟢 Done (pkg-000034), всё построено. **Как закрыть:** Status ⚪→🟢, AC `[ ]`→`[x]`, обновить «Точки в коде» (`request_context.py`, `verification_required.py`, миграция `…000002`). | [`STORY-IDS-OAUTH-04...md:7,26-29,32-36`](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md) |
| **F2** | MEDIUM | Doc-stale (пакет-индекс) | [`EPIC-IDS-OAUTH.md`](../tasks/backlog-stories/oauth/EPIC-IDS-OAUTH.md): состав OAUTH-04 = **⚪ Todo** (стр.20); статус-строка «OAUTH-04 — ⚪ Todo (verify-gate)» (стр.22); Порядок «→ OAUTH-04 (relay…)» как предстоящий (стр.29). Реально 🟢. **Как закрыть:** OAUTH-04 → 🟢; снять «verify-gate не построен»; пометить эпик завершённым по коду (остался gateway-intake). | [`oauth/EPIC-IDS-OAUTH.md`](../tasks/backlog-stories/oauth/EPIC-IDS-OAUTH.md) |
| **F3** | MEDIUM | Cross-doc drift (частичный) | [`04-security:68`](../runtime-docs/04-security.md) as-is «**Оставшийся разрыв: verify-gate (OAUTH-04)**» — построен; [`04-security:92`](../runtime-docs/04-security.md) таблица «Флаг нужна верификация … ⚪ поля есть; relay через OAuth = OAUTH-04» — relay построен. **Как закрыть:** «verify-gate relay + `verification_required` — ✅ построен (OAUTH-04)». | [`04-security`](../runtime-docs/04-security.md) |

> **Положительно (не finding):** [`09-gateway-expectations`](../runtime-docs/09-gateway-expectations.md) **уже актуализирован** под OAUTH-04 — таблица «verify-gate … ✅ (OAUTH-04)» (стр.35), блок «Контракт `verification_required`» (стр.37-43), Итог «verify-gate … построены (OAUTH-01..04); осталась — подключение gateway» (стр.62). SSOT-контракт для gateway зафиксирован.

Наблюдения (severity none/LOW, **не gaps OAUTH-04** — вне AC):
- **O1 (LOW):** TTL handshake-запроса = `oauth_authorization_code_ttl_s` ([handlers.py:69-70](../../src/core/oauth/handlers.py)). При 403 верификация телефона (SMS-OTP) должна уложиться в это окно, иначе request истечёт → `invalid_grant` при повторе. UX-нюанс, вне AC.
- **O2 (none):** `eid:verify` разрешён CHECK'ом и `ALLOWED`, но **не** в `VERIFY_REQUIRED_ACTIONS` → телефонный гейт его не триггерит. Согласовано с phone-pivot (eID отложен; колонка/код — forward-compat).

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **366 passed, 11 deselected** (было 359 → **+7**: verify-gate + migration), совпадает с индексом |
| Новые модули `core/oauth/{request_context,verification_required}.py` | аддитивны |
| `handle_oauth_authorize_complete` | +verify-gate ветка перед consume; happy-path (OAUTH-01) сохранён — тест `..._issues_code` зелёный |
| Cross-backend mappers | обе колонки в Supabase ([db_supabase.py:686-687,707-708](../../src/core/infrastructure/db_supabase.py)) и in-memory — relay не зависит от бэкенда |
| Миграция `…000002` | ALTER (аддитивный), хронологический порядок (migration-тест) |
| OAUTH-01/02/03, phone, eID | не затронуты |

Регрессий не выявлено.

---

## 5. Итог

- **STORY-IDS-OAUTH-04 — 🟢 исполнена полно:** relay `requested_action`/`return_context` (authorize→complete, cross-backend), verify-gate (403 `verification_required` до выдачи кода, идемпотентно), канон `{error, reason, verify_url}` под `phone_verified`, отделение от OTP-ошибок (403 vs 400). AC 5/5, 6 тестов + migration-тест.
- **Findings — только doc-staleness:** **F1** (backlog-story ⚪/AC `[ ]`), **F2** (пакет-индекс OAUTH-04 ⚪), **F3** (04-security as-is/таблица «verify-gate — разрыв»). **09-gateway уже актуализирован** (контракт для gateway зафиксирован).
- **Наблюдения** (O1 TTL-окно verify, O2 `eid:verify` не gated) — LOW/none, вне AC.
- **Регрессий нет** (366 passed, +7 объяснён).
- **Эпик EPIC-IDS-11 по коду завершён** (OAUTH-01..04 🟢); единственный оставшийся разрыв системы — подключение gateway-intake (вызов introspection + enforcement `verification_required`), вне identity-репо.

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; 7 тасков + story сверены по коду (t01–t07 🟢, индекс корректен).
- [x] AC 5/5 сверены по коду **и** тестам (relay/verify-gate/contract/SMS-separation/invalid-action).
- [x] Data-flow проверен сквозь оба бэкенда (Supabase mappers + in-memory) — relay не теряется при `DB_BACKEND=supabase`.
- [x] Регрессий нет; 359→366 (+7) объяснён; индекс 366 = факт.
- [x] Doc-drift пойман дифференцированно: F1/F2/F3 открыты, 09-gateway отмечен как уже закрытый (не выдан за gap).
