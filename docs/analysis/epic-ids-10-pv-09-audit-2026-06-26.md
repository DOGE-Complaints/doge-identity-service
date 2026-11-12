# Жёсткий аудит исполнения STORY-IDS-PV-09 (durable Supabase phone-persistence)

> **Дата:** 2026-06-26
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity. Не предлагаю реализацию — только findings.
> **Предмет:** [`STORY-IDS-PV-09-durable-phone-persistence`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md) vs фактический код. Исполнена под **EPIC-IDS-10** (pkg-000039), 7 tasks.
> **Контекст:** гэпы **G-2a** (durable phone-аудит) + **G-3** (durable phone-сессии) + bootstrap-parity из [full-audit §3](./identity-backend-full-audit-2026-06-24.md).
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): pkg-000039, PV-09 🟢 (стр.11,72,127,628-634).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Миграция | [`20260626000001_phone_persistence_tables.sql`](../../supabase/migrations/20260626000001_phone_persistence_tables.sql) — `phone_verification_sessions` + `phone_audit_events` + индексы + RLS |
| Session-индексы | user/created, `expires_idx … WHERE status='started'`, provider_message (стр.28-39 миграции) |
| Audit-колонки | `ip_hash/user_agent_hash` (стр.49-50 миграции) — согласовано с SEC-02 |
| Supabase session-стор | `SupabasePhoneVerificationSessionStore` ([db_supabase.py:747](../../src/core/infrastructure/db_supabase.py)) — 10 методов |
| Supabase audit-репо | `SupabasePhoneAuditLogRepository` ([db_supabase.py:866](../../src/core/infrastructure/db_supabase.py)) |
| DI-переключение | `db_backend=="supabase"` → Supabase; иначе `InMemory*` ([providers.py:124-128](../../src/core/infrastructure/providers.py)) |
| Bootstrap-parity | `000_full_init.sql` 8/8 секций: oauth (264,281) + phone sessions (348) + phone audit (383) + phone-колонки (235-254) |
| Миграция в тесте | [test_supabase_migrations_sql.py:80-88](../../tests/test_supabase_migrations_sql.py) (таблицы/индексы/RLS) |
| Тесты | [test_phone_supabase_stores.py](../../tests/test_phone_supabase_stores.py) — 6 (incl. durability) |
| **Offline-сюита** | **386 passed, 12 deselected** ✅ (совпадает с индексом) |

---

## 1. Актуализация тасков и story (по коду)

| Таск (EPIC-IDS-10, pkg-000039) | Факт | Статус |
|--------------------------------|------|--------|
| t01 phone persistence migration sql | 2 таблицы + индексы + RLS ([миграция](../../supabase/migrations/20260626000001_phone_persistence_tables.sql)) | 🟢 |
| t02 supabase phone verification session store | `SupabasePhoneVerificationSessionStore` (10 методов) | 🟢 |
| t03 supabase phone audit log repository | `SupabasePhoneAuditLogRepository` ([db_supabase.py:866](../../src/core/infrastructure/db_supabase.py)) | 🟢 |
| t04 di phone store backend selection | switch по `db_backend` ([providers.py:124-128](../../src/core/infrastructure/providers.py)) | 🟢 |
| t05 bootstrap full init parity | `000_full_init.sql` 8/8 (oauth + phone-таблицы + колонки) | 🟢 |
| t06 offline phone durability regression tests | `test_durability_phone_session_survives_store_recreate`, `..._audit_survives_repo_recreate` | 🟢 |
| t07 story acceptance verification | AC 7/7 (см. §2) | 🟢 |
| **STORY-IDS-PV-09** | durable phone-persistence | **🟢 Done** |

**Индекс корректен (bullrun):** `EPIC-IDS-10 … PV-01..07 🟢; PV-09 🟢` ([bullrun-launch-index.md:127](../tasks/bullrun-launch-index.md)); pkg-000039 Done, 386 offline (стр.11).

> **G-2a + G-3 закрыты.** Вместе с SEC-02 (G-2b) full-audit **G-2 полностью закрыт**; bootstrap-gap закрыт. Остаток full-audit §3: только **G-4** (doc, CLEANUP-04) — все реальные code-гэпы (G-1, G-2a/b, G-3, G-5) исчерпаны.

---

## 2. Сверка Acceptance Criteria (по коду + тестам)

| AC | Факт | Вердикт |
|----|------|---------|
| Сессия, созданная до пересоздания стора (`supabase`), доступна для confirm (G-3); expired/consumed-статус корректен | `test_durability_phone_session_survives_store_recreate` ([test:243](../../tests/test_phone_supabase_stores.py)); `mark_consumed/expired`; `get_active_by_user` исключает `expires_at < now` ([db_supabase.py](../../src/core/infrastructure/db_supabase.py)) | ✅ |
| Audit-событие, записанное до пересоздания репо, читается после (G-2a) | `test_durability_phone_audit_survives_repo_recreate` ([test:256](../../tests/test_phone_supabase_stores.py)) | ✅ |
| Тот же протокол `PhoneVerificationSessionStore` / `PhoneAuditLogRepository` без изменения контракта | 10/10 методов совпадают с протоколом ([contracts.py](../../src/core/domain/contracts.py)) | ✅ |
| DI-switch; in-memory не изменён, офлайн-тесты зелёные | [providers.py:124-128](../../src/core/infrastructure/providers.py); 386 passed (in_memory) | ✅ |
| Миграция создаёт таблицы + RLS + индекс; покрыта в `test_supabase_migrations_sql` | [test:80-88](../../tests/test_supabase_migrations_sql.py) | ✅ |
| Bootstrap-parity: fresh `000_full_init` ≡ полный накат миграций | секции 6/8 (oauth) + 8/8 (phone) + phone-колонки | ✅ |
| Аудит-содержимое IP/UA не вводится этой стори (SEC-02) | scope-граница соблюдена; колонки есть, заполнение — SEC-02 | ✅ |

**Вывод:** все 7 AC выполнены кодом+тестами. **Story AC проставлены `[x]`** (в отличие от SEC-01b/02/03 — здесь story-чекбоксы синхронны). Контракт-парити точный; durability подтверждена прямыми тестами «survives recreate».

---

## 3. Findings (severity + как закрыть; без реализации)

Код PV-09 — без материальных дефектов; backlog-story актуальна. Finding — **doc-staleness в пакет-индексе**.

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F1** | MEDIUM | Doc-stale (пакет-индекс) | [`EPIC-IDS-PHONE.md`](../tasks/backlog-stories/phone-verification/EPIC-IDS-PHONE.md): состав **PV-09 = ⚪ Todo** (стр.30) при 🟢 (pkg-000039). Шире: **эпик-статус «⚪ Todo»** (стр.3) и **PV-02/04/05 = ⚪** (стр.23,25,26) — при том что bullrun ([стр.127](../tasks/bullrun-launch-index.md)) держит PV-01..07 + PV-09 все 🟢. **Как закрыть:** синхронизировать EPIC-IDS-PHONE состав (PV-09 + PV-02/04/05 → 🟢) и эпик-статус с bullrun. *(PV-09 верифицирован по коду; PV-02/04/05 — по bullrun-SSOT, отдельно не пере-аудировались.)* | [`EPIC-IDS-PHONE.md:3,23,25,26,30`](../tasks/backlog-stories/phone-verification/EPIC-IDS-PHONE.md) |

Наблюдения (severity none/LOW, **не gaps**):
- **O1:** `expire_pending(now)` — метод ленивой очистки просроченных сессий ([db_supabase.py](../../src/core/infrastructure/db_supabase.py)); его планирование (cron) — deployment-вопрос. **Корректность не зависит**: `get_active_by_user` исключает `expires_at < now` даже без запуска cleanup → просроченная «started»-сессия не вернётся как активная. Аналог OAUTH-03 O2 (индекс есть, джоб опционален).
- **O2:** phone-аудит теперь durable (Supabase при `supabase`-backend) — закрыт разрыв с eID-аудитом; IP/UA-хэши пишутся (SEC-02), тест `test_supabase_phone_audit_stores_ip_ua_hashes_when_present`.

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **386 passed, 12 deselected** (было 379 → **+7**: phone supabase-store + durability + migration) |
| Новые классы `db_supabase.py` | аддитивны; `InMemory*` (demo/tests) не изменены |
| DI `providers.py` | +ветка `supabase` для phone-стора/аудита; `in_memory`-путь прежний — сюита зелёная |
| Bootstrap `000_full_init.sql` | расширен (8/8 секций) — fresh-накат теперь включает oauth + phone-таблицы |
| Phone-флоу (PV-05), OAuth, eID | не затронуты |

Регрессий не выявлено.

---

## 5. Итог

- **PV-09 — 🟢 исполнена полно:** миграция `phone_verification_sessions` + `phone_audit_events` (индексы, RLS); `SupabasePhoneVerificationSessionStore` (10 методов, контракт-парити) + `SupabasePhoneAuditLogRepository`; DI-switch по `db_backend`; bootstrap-parity (8/8). AC 7/7 (story-чекбоксы `[x]`), 6 store/durability тестов + migration-тест. Таски t01–t07 🟢; bullrun-индекс корректен.
- **G-2a + G-3 + bootstrap закрыты** → с SEC-02/SEC-01/01b/SEC-03 **все реальные code-гэпы full-audit §3 исчерпаны** (остаток — G-4 doc в CLEANUP-04).
- **Findings:** только **F1** — пакет-индекс `EPIC-IDS-PHONE` отстал (PV-09 ⚪ + эпик ⚪ + PV-02/04/05 ⚪) от факта/bullrun.
- **Регрессий нет** (386 passed).

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; 7 тасков + story + 7 AC сверены по коду, тестам и миграции/bootstrap.
- [x] Контракт-парити проверен пометодно (10/10 протокола `PhoneVerificationSessionStore`).
- [x] Durability подтверждена прямыми тестами «survives recreate» (session + audit); expiry-корректность проверена в `get_active_by_user`.
- [x] Bootstrap-parity проверена пофайлово (`000_full_init` секции oauth + phone).
- [x] Регрессий нет; 379→386 (+7) объяснён; индекс 386 = факт. Drift вынесен в F1, отделён от кода (дефектов нет).
