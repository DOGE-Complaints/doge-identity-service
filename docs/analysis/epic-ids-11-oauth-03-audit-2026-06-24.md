# Жёсткий аудит исполнения STORY-IDS-OAUTH-03 (durable OAuth-стор, Supabase)

> **Дата:** 2026-06-24
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-OAUTH-03-persistent-token-store-supabase`](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) vs фактический код. Исполнена под **EPIC-IDS-11** (pkg-000033), 7 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): Текущая волна pkg-000033, OAUTH-03 🟢 (стр.11,62,621-627).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Миграция | [`20260624000001_oauth_authorization_tables.sql`](../../supabase/migrations/20260624000001_oauth_authorization_tables.sql) — `oauth_authorization_requests` + `oauth_authorization_codes` |
| TTL-индексы | `..._requests_expires_idx` (стр.18-19), `..._codes_expires_idx … WHERE consumed=FALSE` (стр.41-43) |
| Single-use | `oauth_authorization_codes.consumed BOOLEAN` (стр.37) + атомарный consume (ниже) |
| RLS | `ENABLE ROW LEVEL SECURITY` + политики `service_role` (стр.45-60) |
| Request-store | `SupabaseAuthorizationRequestStore` save/get/consume ([db_supabase.py:708-740](../../src/core/infrastructure/db_supabase.py)) |
| Token-service | `SupabaseOAuthTokenService` ([db_supabase.py:743+](../../src/core/infrastructure/db_supabase.py)) — контракт `OAuthTokenService` |
| Атомарный single-use кода | `PATCH … consumed=eq.false & expires_at=gt.now → consumed=true`, `return=representation`, нет строки → `invalid_grant` ([db_supabase.py:810-824](../../src/core/infrastructure/db_supabase.py)) |
| `client_secret`/PKCE в Supabase-пути | `verify_client_secret` + S256 ([db_supabase.py:799-837](../../src/core/infrastructure/db_supabase.py)) |
| `validate_access_token` — stateless | `claims_from_access_token_jwt(config, token)` — **без обращения к БД** ([db_supabase.py](../../src/core/infrastructure/db_supabase.py)) |
| DI-переключение | `db_backend=="supabase"` → Supabase-стор; иначе `InMemoryOAuthTokenService` ([providers.py:91-99](../../src/core/infrastructure/providers.py)) |
| Тесты | [test_oauth_supabase_stores.py](../../tests/test_oauth_supabase_stores.py) — 7; [test_supabase_migrations_sql.py](../../tests/test_supabase_migrations_sql.py) — таблицы/индексы/политики |
| **Offline-сюита** | **359 passed, 11 deselected** ✅ (совпадает с индексом) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-11, pkg-000033) | Факт | Статус |
|--------------------------------|------|--------|
| t01 oauth supabase migration sql | 2 таблицы + TTL-индексы + RLS ([миграция](../../supabase/migrations/20260624000001_oauth_authorization_tables.sql)) | 🟢 |
| t02 supabase authorization request store | `SupabaseAuthorizationRequestStore` save/get/consume (TTL, single-use) | 🟢 |
| t03 supabase oauth token service | `SupabaseOAuthTokenService` (issue code/token, validate; атомарный consume) | 🟢 |
| t04 di oauth store backend selection | switch по `db_backend` ([providers.py:91-99](../../src/core/infrastructure/providers.py)) | 🟢 |
| t05 offline supabase oauth store tests | 5 store-тестов (mock PostgREST) | 🟢 |
| t06 durability and stateless jwt tests | `test_durability_authorization_code_survives_store_recreate`, `test_stateless_access_token_validates_without_db_reads` | 🟢 |
| t07 story acceptance verification | AC 6/6 (см. §2) | 🟢 |
| **STORY-IDS-OAUTH-03** | durable OAuth-стор | **🟢 Done** |

Индекс держит эпик корректно: `EPIC-IDS-11 … OAUTH-01 🟢; OAUTH-02 🟢; OAUTH-03 🟢` ([bullrun-launch-index.md:112](../tasks/bullrun-launch-index.md)); pkg-000033 Done, 359 offline (стр.11).

---

## 2. Сверка Acceptance Criteria story (по коду + тестам)

| AC | Факт (код + тест) | Вердикт |
|----|-------------------|---------|
| Миграция: `oauth_authorization_requests` + `oauth_authorization_codes` (TTL-индекс, single-use) | [миграция:4-43](../../supabase/migrations/20260624000001_oauth_authorization_tables.sql); тест `test_supabase_migrations_sql` (таблицы/индексы/политики, стр.59-66) | ✅ |
| `SupabaseOAuthTokenService` реализует контракт + хранение request-state; single-use/TTL в БД | [db_supabase.py:743+](../../src/core/infrastructure/db_supabase.py); атомарный PATCH-consume; тесты `..._issue_and_consume_code`, `..._rejects_consumed_code`, `..._rejects_expired_code` | ✅ |
| `DB_BACKEND=supabase` → Supabase-стор; `in_memory` → прежний (тесты зелёные) | [providers.py:91-99](../../src/core/infrastructure/providers.py); вся сюита (in_memory) зелёная | ✅ |
| Durability: code/request, выданный до пересоздания стора, валиден после; просрочен/использован → `invalid_grant` | тест `test_durability_authorization_code_survives_store_recreate`; `OAuthGrantError("invalid_grant")` на consumed/expired | ✅ |
| Access-токен валиден после пересоздания стора **без** БД (stateless) | `validate_access_token`→`claims_from_access_token_jwt` (no DB); тест `test_stateless_access_token_validates_without_db_reads` | ✅ |
| Offline-тесты (mock PostgREST) зелёные; миграция — в `test_supabase_migrations_sql` | 7 store-тестов + migration-тест; 359 passed | ✅ |

**Вывод:** все 6 AC выполнены и покрыты тестами. Архитектурно корректно: durable только для codes/handshake (короткоживущее состояние), access-токен остаётся stateless HS256 (редеплой не ломает) — соответствует ADR-IDS-002.

---

## 3. Findings (severity + как закрыть; без реализации)

Код OAUTH-03 — без материальных дефектов. Findings — **doc-staleness** (рекуррентный паттерн: код 🟢, но соседние доки описывают «не построено/in-memory»).

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F1** | MEDIUM | Doc-stale (внутр. противоречие) | Backlog-story Status `🟢 Done` + AC `[x]`, но секция «Точки в коде (текущее состояние)» всё ещё пишет «**DI всегда in-memory:** `providers.py:88` (`oauth_token_service = InMemoryOAuthTokenService`)» — по факту DI **переключается** ([providers.py:91-99](../../src/core/infrastructure/providers.py)), а Supabase-стор построен. **Как закрыть:** обновить «Точки в коде» (DI-switch, `SupabaseOAuthTokenService`/`SupabaseAuthorizationRequestStore`, миграция) или пометить секцию как pre-state. | [`STORY-IDS-OAUTH-03...md` §Точки в коде](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) | **🟢 закрыт** — секция «Точки в коде (построено)» обновлена (backlog + pipeline story) |
| **F2** | MEDIUM | Doc-stale (пакет-индекс) | [`EPIC-IDS-OAUTH.md`](../tasks/backlog-stories/oauth/EPIC-IDS-OAUTH.md): состав OAUTH-03 = **⚪ Todo** (стр.19); статус-строка «OAUTH-03..04 — ⚪ Todo (durable store, verify-gate)» (стр.22); Назначение «durable store — OAUTH-03» (стр.8); Порядок «→ OAUTH-03 (durable…)» как предстоящий (стр.29). Реально 🟢 Done. **Как закрыть:** OAUTH-03 → 🟢 в составе/статус-строке/порядке. | [`oauth/EPIC-IDS-OAUTH.md`](../tasks/backlog-stories/oauth/EPIC-IDS-OAUTH.md) | **🟢 закрыт** — OAUTH-03 🟢 Done в составе, статус-строке, порядке, назначении |
| **F3** | MEDIUM | Cross-doc drift (свежий) | После билда OAUTH-03 устарели: [`04-security:68`](../runtime-docs/04-security.md) as-is «Оставшийся разрыв: … **durable handshake/codes (OAUTH-03)**»; [`04-security:95`](../runtime-docs/04-security.md) «Handshake/codes — **in-memory** (OAUTH-03)»; [`04-security:111`](../runtime-docs/04-security.md) «⚠️ Handshake/codes — **in-memory** (редеплой) → OAUTH-03»; [`09-gateway:47`](../runtime-docs/09-gateway-expectations.md) Итог «Оставшиеся задачи — **OAUTH-03**/04». **Как закрыть:** «durable-стор построен (OAUTH-03), активен при `DB_BACKEND=supabase`; demo остаётся in-memory» — не подавать in-memory как единственное/целевое состояние. | runtime-docs 04/09 | **🟢 закрыт** — `04-security` §A/таблица/§3 и `09-gateway` Итог актуализированы |

Наблюдения (severity none/LOW, **не gaps OAUTH-03** — вне AC):
- **O1 (LOW):** `SupabaseAuthorizationRequestStore.consume` — `get`+`DELETE` (две операции, не атомарно) ([db_supabase.py:729-740](../../src/core/infrastructure/db_supabase.py)). Гонка двойного consume handshake'а теоретически выдаст 2 кода на один логин. Риск низкий (одно-пользовательское окно логина); **consume самого кода — атомарен** (conditional PATCH). Вне AC.
- **O2 (LOW):** нет джоба очистки просроченных строк (только индекс `expires_at`). Корректность не страдает (запросы фильтруют `expires_at`/`consumed`), но строки накапливаются. Story-scope упоминал индекс «для очистки», джоб — не в AC.
- **O3 (none):** `key=…oauth_access_token_secret or "demo-key"` ([db_supabase.py:806](../../src/core/infrastructure/db_supabase.py)) — fallback только в demo; в pilot секрет обязателен (fail-fast). Согласовано с demo-позой.

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **359 passed, 11 deselected** (было 351 → **+8**: 7 store-тестов + migration), совпадает с индексом |
| Новые классы `db_supabase.py` | аддитивны; `InMemoryOAuthTokenService` (demo/tests) не изменён |
| DI `providers.py` | +ветка `supabase`; `in_memory`-путь прежний — вся сюита (in_memory) зелёная |
| Миграция | новый файл, хронологический порядок (тест `test_migration_filenames_are_chronological`) |
| OAUTH-01/02, phone, eID | не затронуты |

Регрессий не выявлено.

---

## 5. Итог

- **STORY-IDS-OAUTH-03 — 🟢 исполнена полно:** миграция (2 таблицы, TTL-индексы, RLS), `SupabaseAuthorizationRequestStore` + `SupabaseOAuthTokenService` (атомарный single-use кода, TTL, PKCE, client_secret), DI-switch по `db_backend`, stateless access-token. AC 6/6, 7 store + durability/stateless/migration тесты.
- **Findings — doc-staleness (закрыты):** **F1** (backlog/pipeline «точки в коде»), **F2** (пакет-индекс OAUTH-03), **F3** (`04-security` / `09-gateway`). Severity MEDIUM, рекуррентный паттерн — исправлено docs-only 2026-06-24.
- **Наблюдения** (O1 non-atomic request-consume, O2 нет cleanup-джоба) — LOW, вне AC, не gaps.
- **Регрессий нет** (359 passed, +8 объяснён).

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; 7 тасков + story сверены по коду (t01–t07 🟢, индекс корректен).
- [x] AC 6/6 сверены по коду **и** тестам (durability + stateless + single-use + expired + migration).
- [x] Data-flow проверен: атомарный consume кода (conditional PATCH) vs неатомарный consume handshake (O1) разведены.
- [x] Регрессий нет; 351→359 (+8) объяснён; индекс 359 = факт.
- [x] Doc-drift «in-memory/OAUTH-03 не построен» (F1/F2/F3) закрыт в backlog-story, pipeline story, пакет-индексе и 04/09; demo-нюанс (`in_memory` только demo) зафиксирован честно.
