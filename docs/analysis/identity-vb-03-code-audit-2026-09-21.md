# Аудит по коду: STORY-IDS-VB-03 (set `identity_verified` on phone/eID success) — 2026-09-21

> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — verified-state, только проверяемые claims с путями; регрессии; gaps с severity + как закрыть. Findings-only (без реализации).
> **Объект:** backlog [`STORY-IDS-VB-03-set-opaque-on-verification-success`](../tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md) · pipeline [`STORY-IDS-VB-03-set-opaque-on-verification-success`](../tasks/epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-03-set-opaque-on-verification-success/STORY-IDS-VB-03-set-opaque-on-verification-success.md) (`input_mode=backlog_story`, pkg-000052).
> **Fence:** AC/Scope из backlog + pipeline; Product Story Done ≠ empty OPEN gap-list — оба явно. `bullrun-launch-index.md` VAL не правил.
> **Claims scope:** Read/Glob (+ write этого отчёта). Live pytest в этой сессии **не** перезапускался → suite green = Unknown (кроме артефакта t06 на диске).

---

## Вердикт

**STORY-IDS-VB-03 = 🟢 Done — подтверждено фактическим кодом.** Success `attach_phone_verification` / `attach_eid_verification` (db + in-memory) ставят `identity_verified=true`; conflict/failure не clear’ит opaque; `_log_phone_audit` / `_log_eid_audit` без новой event schema; offline tests on disk. Pipeline Meta / bullrun / package INDEX: 🟢 — **совпадает** с кодом t01–t06. EPIC-IDS-15 package **3/3 Done**.

| Метрика | Значение |
|---------|----------|
| Product Story Done (pipeline Meta + bullrun) | **да** |
| vs Story AC | **0 OPEN / 4** |
| Material gaps (Critical/High/Medium) | **0** |
| Doc-only OPEN | **0** |
| P5 needed? | **Нет** (zero-gap; нет TASKED) |

---

## Bullrun status touchpoints (без правок индекса)

| Якорь | Строки (approx) | Заявлено | Факт-код/docs | Вердикт |
|-------|-----------------|----------|---------------|---------|
| §Актуальная точка | bullrun ~11–12 | P3 Done VB-03 pkg-000052; 6/6; 456 pytest; package 3/3 | attach_* + tests на диске; 456 = claim t06 (live Unknown) | ✅; suite Unknown |
| input_mode / active story | bullrun ~131 | `backlog_story` · VB-03 🟢 Done pkg-000052 | pipeline Meta 🟢; AC `[x]` | ✅ |
| Active pkg | bullrun ~133 | pkg-000052 🟢 Done, 6 paths | t01–t06 Done + acceptance PASS | ✅ |
| Epic registry EPIC-IDS-15 | bullrun ~202 | 🟢 Done — VB-01/02/03 | epic Meta 🟢; INDEX 3/3 | ✅ |
| Task queue VB-03 t01–t06 | bullrun ~874–879 | все 🟢 pkg-000052 | gates + code ниже | ✅ |
| Backlog package INDEX | INDEX:11 | VB-03 🟢 Done pkg-000052 | код + pipeline | ✅ |
| Backlog AC/Nested | backlog `:38-60` | AC `[x]`; Nested T01–T06 🟢 | synced | ✅ нет drift |

**Актуализация в отчёте:** t01–t06 и product story = 🟢 по коду. Строки индекса **факт-верны**.

---

## Пер-таск верификация (по коду)

| Task | Требование | Факт | Вердикт |
|------|------------|------|---------|
| **t01** phone attach → opaque | db + repo success set true | PATCH/create/replace [`db_supabase.py:522,563,581`](../../src/core/infrastructure/db_supabase.py); replace [`repositories.py:227`](../../src/core/infrastructure/repositories.py) | 🟢 Done |
| **t02** eID attach → opaque | db + repo success set true | PATCH/create/replace [`db_supabase.py:434,475,494`](../../src/core/infrastructure/db_supabase.py); replace [`repositories.py:161`](../../src/core/infrastructure/repositories.py) | 🟢 Done |
| **t03** failure no clear | conflict raises; no mutate opaque | conflict before write [`repositories.py:178-183`](../../src/core/infrastructure/repositories.py); tests owner+challenger unchanged | 🟢 Done |
| **t04** audit precedent | keep helpers; no new schema | [`handlers.py:114-175`](../../src/core/api/handlers.py); no `opaque_flipped` / new event in `src/` | 🟢 Done |
| **t05** offline tests | success → true; failure → unchanged | [`tests/test_identity_verified_attach.py`](../../tests/test_identity_verified_attach.py); also [`test_inmemory_repositories.py:137`](../../tests/test_inmemory_repositories.py) | 🟢 Done |
| **t06** story gate | AC-02/03/05 + suite | [t06 acceptance](../tasks/epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-03-set-opaque-on-verification-success/task-ids-15-03-t06-story-acceptance-verification/acceptance-verification-task-ids-15-03-t06-story-acceptance-verification.md) PASS `2026-09-21T20:51:27Z` claims 456/13 | 🟢 Done (claim); live **Unknown** |

---

## Сверка Acceptance Criteria (backlog = pipeline Target/AC)

Источник: backlog [`:38-42`](../tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md) = pipeline [`:45-48`](../tasks/epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-03-set-opaque-on-verification-success/STORY-IDS-VB-03-set-opaque-on-verification-success.md).

| # | AC | Факт | Вердикт |
|---|-----|------|---------|
| 1 | AC-ID-THR-02: execute existing verification integrations; no pack/API invent | Changes only in existing `attach_*` (infra); no new pack params / routes | ✅ |
| 2 | AC-ID-THR-03: after success opaque persisted; audit remains; boolean does not disclose method | Success sets `identity_verified=True` (bool only); handlers still call audit helpers; no method name in opaque field | ✅ |
| 3 | AC-ID-THR-05: logging = existing phone/eID audit functions (no new schema) | `_log_phone_audit` / `_log_eid_audit` signatures intact; `PhoneAuditEvent` / `EIDAuditEvent` unchanged for opaque; no new event type in `src/` | ✅ |
| 4 | Offline tests cover success/failure opaque behavior | [`test_identity_verified_attach.py`](../../tests/test_identity_verified_attach.py) success + conflict owner/challenger; suite this session | ✅ tests; **Unknown** live suite |

**Product AC OPEN count: 0.**

Scope failure policy (arch §2.3, covered by t03 + AC tests): conflict raises `ProfileConflictError` **before** profile write when hash owned by another user — no set-true and no clear of already-true.

---

## Регрессии / scope fence

| Аспект | Факт | Вердикт |
|--------|------|---------|
| Method flags as-is | `phone_verified` / `eid_verified` still set True on success alongside opaque | ✅ |
| Blank profile skeleton `identity_verified=False` | only pre-replace construction [`repositories.py:140,204`](../../src/core/infrastructure/repositories.py); success path then `True` | ✅ не clear-on-failure |
| Pack / gateway 52 | не трогалось | ✅ OOS |
| Live EE smoke | OOS (arch offline) | ✅ |
| OAuth introspection rewrite | OOS | ✅ |
| `/me` expose | VB-02; не регрессирует write hooks | ✅ |

---

## Gaps (findings)

**Нет.** vs AC **0 OPEN**. Actionable gap-list пуст.

Наблюдения (**не gap**, severity none):

- Offline attach tests exercise **InMemory** repo; `db_supabase` success paths verified by Read (PATCH body includes `"identity_verified": True`) — AC не требует отдельного supabase-unit для attach opaque.
- §«Verified current state» в story — historical pre-impl snapshot; AC/Nested already synced.
- Live pytest 456 — claim t06; VAL session не перезапускал → Unknown, не OPEN AC.

---

## Product Story Done vs gap-list

| | |
|--|--|
| **Product Story Done** | **да** (pipeline Meta 🟢; bullrun t01–t06 🟢; code satisfies AC 1–4 on disk) |
| **OPEN gap-list** | **пусто** (0 Critical/High/Medium/Low OPEN) |

---

## Итог / P5

- **vs AC: 0 OPEN / 4.** Material actionable set: **пусто**.
- **P5 needed?** **Нет** (zero-gap; не стартовать scaffold из VAL).
- **Next (не VAL):** epic gate EPIC-IDS-15 / OP fence — VAL фазы не двигает.
