# Аудит по коду: STORY-IDS-VB-01 (persist `identity_verified` + backfill) — 2026-09-21

> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — verified-state, только проверяемые claims с путями; регрессии; gaps с severity + как закрыть. Findings-only (без реализации).
> **Объект:** backlog [`STORY-IDS-VB-01-persist-identity-verified`](../tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md) · pipeline [`STORY-IDS-VB-01-persist-identity-verified`](../tasks/epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-01-persist-identity-verified/STORY-IDS-VB-01-persist-identity-verified.md) (`input_mode=backlog_story`, pkg-000050).
> **Fence:** AC/Scope из backlog + pipeline; Product Story Done ≠ empty OPEN gap-list — оба явно. `bullrun-launch-index.md` VAL не правил.
> **Claims scope:** Read/Glob (+ write этого отчёта). Live pytest в этой сессии **не** перезапускался → suite green = Unknown (кроме артефактов t05/run-summary на диске).

---

## Вердикт

**STORY-IDS-VB-01 product scope = выполнен по фактическому коду** относительно 4 Story AC (persist column/model/map + one-shot backfill + no clear-on-failure + offline tests on disk). Pipeline Meta / bullrun / package INDEX: 🟢 Done — **совпадает** с кодом t01–t05.

| Метрика | Значение |
|---------|----------|
| Product Story Done (pipeline Meta + bullrun) | **да** |
| vs Story AC | **0 OPEN / 4** |
| Material gaps (Critical/High/Medium) | **0** |
| Doc-only OPEN | **1× Low** (`G-VB01-DOC-01`) |
| P5 needed? | **Нет** для product code; опционально doc-sync Low (не блокирует wave) |

---

## Bullrun status touchpoints (без правок индекса)

| Якорь | Строки (approx) | Заявлено | Факт-код/docs | Вердикт |
|-------|-----------------|----------|---------------|---------|
| §Актуальная точка | bullrun ~11–12 | EPIC-IDS-15 P3 Done VB-01 pkg-000050; 5/5 tasks; 450 pytest | migration+model+map+backfill+tests на диске; 450 = claim t05 (live Unknown) | ✅ статусы; suite Unknown |
| input_mode / active story | bullrun ~126 | `backlog_story` · VB-01 🟢 Done | pipeline Meta 🟢; AC `[x]` в pipeline | ✅ |
| Active pkg | bullrun ~128 | pkg-000050 🟢 Done, 5 paths | task README t01–t05 Status Done + acceptance gates PASS | ✅ |
| Epic registry EPIC-IDS-15 | bullrun ~195 | 🟡 In Progress — VB-01 🟢; VB-02/VB-03 Todo | package INDEX 1/3 Done | ✅ эпик не Done |
| Task queue t01–t05 | bullrun ~853–861 | все 🟢 pkg-000050 | gates + code ниже | ✅ |
| Backlog package INDEX | INDEX:9 | VB-01 🟢 Done | код + pipeline | ✅ |
| Backlog story body AC/Nested | backlog `:38-61` | Meta 🟢 но AC `[ ]` + Nested Todo | **drift** → `G-VB01-DOC-01` | ⚠️ doc |

**Актуализация в отчёте:** t01–t05 и product story = 🟢 по коду. Строки bullrun task/story 🟢 **факт-верны**. Единственный drift — чекбоксы/Nested внутри backlog-файла (не индекс).

---

## Пер-таск верификация (по коду)

| Task | Требование | Факт | Вердикт |
|------|------------|------|---------|
| **t01** migration + bootstrap | `profiles.identity_verified BOOLEAN NOT NULL DEFAULT FALSE` | [`20260921000001_profiles_identity_verified.sql`](../../supabase/migrations/20260921000001_profiles_identity_verified.sql); bootstrap [`000_full_init.sql:265-266`](../../supabase/bootstrap/000_full_init.sql) | 🟢 Done |
| **t02** model + db map | `ProfileRecord` + `_profile_to_row`/`_profile_from_row` + constructors default false | [`models.py:39`](../../src/core/domain/models.py); [`db_supabase.py:115,143`](../../src/core/infrastructure/db_supabase.py); [`repositories.py:140,203`](../../src/core/infrastructure/repositories.py); create paths [`db_supabase.py:474,560`](../../src/core/infrastructure/db_supabase.py) | 🟢 Done |
| **t03** backfill | `phone_verified OR eid_verified` → opaque true | [`20260921000002_profiles_identity_verified_backfill.sql`](../../supabase/migrations/20260921000002_profiles_identity_verified_backfill.sql); bootstrap [`000_full_init.sql:268-271`](../../supabase/bootstrap/000_full_init.sql) | 🟢 Done |
| **t04** offline tests | default false; map round-trip; backfill semantics | [`tests/test_identity_verified_persist.py`](../../tests/test_identity_verified_persist.py); migration strings also in [`test_supabase_migrations_sql.py:91-106`](../../tests/test_supabase_migrations_sql.py) | 🟢 Done (evidence on disk) |
| **t05** story gate | all VB-01 AC; suite `-m "not live_integration"` | [t05 acceptance](../tasks/epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-01-persist-identity-verified/task-ids-15-01-t05-story-acceptance-verification/acceptance-verification-task-ids-15-01-t05-story-acceptance-verification.md) PASS `2026-09-21T20:24:31Z` claims 450/13 | 🟢 Done (claim); live re-run **Unknown** |

---

## Сверка Acceptance Criteria (backlog Scope/AC = pipeline Target/AC)

Источник AC: backlog [`:38-42`](../tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md) / pipeline [`:43-47`](../tasks/epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-01-persist-identity-verified/STORY-IDS-VB-01-persist-identity-verified.md) (одинаковый текст).

| # | AC | Факт | Вердикт |
|---|-----|------|---------|
| 1 | Profile хранит `identity_verified` bool (default false для новых без backfill) | Field [`models.py:39`](../../src/core/domain/models.py); SQL `DEFAULT FALSE`; `_profile_from_row` `row.get(..., False)` [`db_supabase.py:143`](../../src/core/infrastructure/db_supabase.py); constructors `identity_verified=False` | ✅ |
| 2 | Backfill one-shot: `phone_verified OR eid_verified` → opaque true | UPDATE WHERE phone OR eid [`20260921000002…sql`](../../supabase/migrations/20260921000002_profiles_identity_verified_backfill.sql) | ✅ |
| 3 | Failure paths не требуют clear-on-failure | `rg identity_verified` в `src/` — только model/map/defaults; **нет** clear/reset hooks на failure | ✅ (negative) |
| 4 | Offline tests map + backfill; suite `-m "not live_integration"` green | Tests on disk ✅; suite green this session | ✅ tests; **Unknown** live suite |

**Product AC OPEN count: 0** (suite Unknown не поднимает AC #4 в OPEN: offline coverage files verified; green = artifact claim).

---

## Регрессии / scope fence

| Аспект | Факт | Вердикт |
|--------|------|---------|
| `/me` не отдаёт opaque (OOS → VB-02) | [`me_response.py:17-51`](../../src/core/api/me_response.py) — нет ключа `identity_verified` | ✅ в scope |
| Success write hooks phone/eID (OOS → VB-03) | `attach_eid_verification` / `attach_phone_verification` PATCH body без `identity_verified`; `dataclasses.replace` не ставит opaque true ([`db_supabase.py:427-580`](../../src/core/infrastructure/db_supabase.py), [`repositories.py:153-162`](../../src/core/infrastructure/repositories.py)) | ✅ ожидаемый residual пакета |
| Not read-time OR as SoT | Нет вычисления `phone_verified or eid_verified` как источника opaque в runtime map | ✅ first-class persist |
| Clear-on-failure | Не добавлено | ✅ |
| Base `create_profiles.sql` | Колонки нет в CREATE — только later migration (etalon phone pattern) | ✅ |

---

## Gaps (findings)

### OPEN

| ID | Severity | Finding | Как закрыть |
|----|----------|---------|-------------|
| **G-VB01-DOC-01** | Low | Backlog [`STORY-IDS-VB-01…md`](../tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md): Meta Status 🟢 Done, но Target/AC всё ещё `[ ]` (`:38-42`) и Nested tasks Status `Todo` (`:56-61`); pipeline/INDEX/bullrun уже Done | Doc sync: отметить AC `[x]`, Nested → Done + реальные folder names `task-ids-15-01-t0N-*` (как pipeline). Не требует product code |

### Не gap (residual / OOS)

| Note | Почему не OPEN vs VB-01 AC |
|------|----------------------------|
| Post-backfill **новые** successful phone/eID не ставят `identity_verified=true` | Explicit «Вне scope» → VB-03; arch §2.3 write policy = sibling story |
| Pipeline §«Verified current state» still «Нет opaque-поля» | Исторический pre-impl snapshot; не ломает AC; optional doc refresh |
| Live pytest 450 | Claim t05/run-summary; VAL session не перезапускал → Unknown, не OPEN AC |

---

## Product Story Done vs gap-list

| | |
|--|--|
| **Product Story Done** | **да** (pipeline Meta 🟢; bullrun t01–t05 🟢; code satisfies AC 1–3 + offline offline tests) |
| **OPEN gap-list** | **1× Low doc** (`G-VB01-DOC-01`); **0** Critical/High/Medium; **0** product AC OPEN |

---

## Итог / P5

- **vs AC: 0 OPEN / 4.** Material actionable set: **пусто**.
- **P5 needed?** **Нет** для product/gap scaffold. Doc Low можно закрыть lightweight sync без P5 override, либо WAIVED reason=working-doc / operator при disposition.
- **Next (не VAL):** P1.3 VB-02 / VB-03 или OP fence — VAL фазы не двигает.
