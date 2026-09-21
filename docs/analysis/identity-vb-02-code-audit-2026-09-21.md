# Аудит по коду: STORY-IDS-VB-02 (expose `identity_verified` on `GET /me`) — 2026-09-21

> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — verified-state, только проверяемые claims с путями; регрессии; gaps с severity + как закрыть. Findings-only (без реализации).
> **Объект:** backlog [`STORY-IDS-VB-02-me-expose-identity-verified`](../tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md) · pipeline [`STORY-IDS-VB-02-me-expose-identity-verified`](../tasks/epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-02-me-expose-identity-verified/STORY-IDS-VB-02-me-expose-identity-verified.md) (`input_mode=backlog_story`, pkg-000051).
> **Fence:** AC/Scope из backlog + pipeline; Product Story Done ≠ empty OPEN gap-list — оба явно. `bullrun-launch-index.md` VAL не правил.
> **Claims scope:** Read/Glob (+ write этого отчёта). Live pytest в этой сессии **не** перезапускался → suite green = Unknown (кроме артефакта t04 на диске).

---

## Вердикт

**STORY-IDS-VB-02 = 🟢 Done — подтверждено фактическим кодом.** `build_me_data` отдаёт method-opaque `identity_verified` на существующем `GET /me`; legacy method flags сосуществуют; `account_status` не является verified boolean; MeData в openapi + API_REFERENCE обновлены; offline tests на диске. Pipeline Meta / bullrun / package INDEX: 🟢 — **совпадает** с кодом t01–t04.

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
| §Актуальная точка | bullrun ~11–12 | EPIC-IDS-15 P3 Done VB-02 pkg-000051; 4/4 tasks; 451 pytest | me_response+docs+tests на диске; 451 = claim t04 (live Unknown) | ✅ статусы; suite Unknown |
| input_mode / active story | bullrun ~138 | `backlog_story` · VB-02 🟢 Done pkg-000051 | pipeline Meta 🟢; AC `[x]` | ✅ |
| Active pkg | bullrun ~140 | pkg-000051 🟢 Done, 4 paths | t01–t04 README Done + acceptance PASS | ✅ |
| Epic registry EPIC-IDS-15 | bullrun ~208 | 🟡 — VB-01/VB-02 🟢; VB-03 Todo | package INDEX 2/3 Done | ✅ эпик не Done |
| Task queue VB-02 t01–t04 | bullrun ~876–879 | все 🟢 pkg-000051 | gates + code ниже | ✅ |
| Backlog package INDEX | INDEX:10 | VB-02 🟢 Done pkg-000051 | код + pipeline | ✅ |
| Backlog story AC/Nested | backlog `:38-56` | AC `[x]`; Nested T01–T04 🟢 Done | synced | ✅ нет drift |

**Актуализация в отчёте:** t01–t04 и product story = 🟢 по коду. Строки индекса **факт-верны**. Bullrun Stories drift ⚪ **нет**.

---

## Пер-таск верификация (по коду)

| Task | Требование | Факт | Вердикт |
|------|------------|------|---------|
| **t01** `build_me_data` | default false; profile → `profile.identity_verified`; keep method flags; no new route | [`me_response.py:35,51`](../../src/core/api/me_response.py); `phone_verified`/`eid_verified` retained; sole `@app.get("/me")` [`asgi_app.py:302`](../../src/core/api/asgi_app.py); `account_status` still `"active"` [`:37`](../../src/core/api/me_response.py) | 🟢 Done |
| **t02** API docs MeData | openapi + API_REFERENCE document opaque + coexistence | [`openapi.yaml:98-105`](../../docs/runtime-docs/api-reference/openapi.yaml); [`API_REFERENCE.md:85-98`](../../docs/runtime-docs/api-reference/API_REFERENCE.md) | 🟢 Done |
| **t03** offline tests | key present; no-profile false; profile reflects persist; method fields present | [`test_me_profile.py:90-91,150,154-194,214`](../../tests/test_me_profile.py) | 🟢 Done |
| **t04** story gate | AC-01/03/04 + docs + suite | [t04 acceptance](../tasks/epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-02-me-expose-identity-verified/task-ids-15-02-t04-story-acceptance-verification/acceptance-verification-task-ids-15-02-t04-story-acceptance-verification.md) PASS `2026-09-21T20:40:59Z` claims 451/13 | 🟢 Done (claim); live re-run **Unknown** |

---

## Сверка Acceptance Criteria (backlog = pipeline Target/AC)

Источник: backlog [`:37-40`](../tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md) = pipeline [`:43-47`](../tasks/epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-02-me-expose-identity-verified/STORY-IDS-VB-02-me-expose-identity-verified.md).

| # | AC | Факт | Вердикт |
|---|-----|------|---------|
| 1 | AC-ID-THR-01: no new HTTP path; surface = `/me`; wire key `identity_verified` | Routes: единственный `@app.get("/me")` [`asgi_app.py:302`](../../src/core/api/asgi_app.py); нет нового verified-path в route list; wire key в payload [`me_response.py:35`](../../src/core/api/me_response.py) | ✅ |
| 2 | AC-ID-THR-03: opaque present; does not disclose method; method flags may coexist | Opaque bool only (no phone/eID label in `identity_verified`); `phone_verified`/`eid_verified` still emitted [`me_response.py:23,31,40,47`](../../src/core/api/me_response.py); tests assert coexistence | ✅ |
| 3 | AC-ID-THR-04: same boolean regardless of method (no second method bit) | Maps only `profile.identity_verified` [`me_response.py:51`](../../src/core/api/me_response.py); not computed as OR | ✅ |
| 4 | Docs + offline tests; suite green for touched | Docs ✅; tests on disk ✅; suite green this session | ✅ docs/tests; **Unknown** live suite |

**Product AC OPEN count: 0.**

Scope extras (не отдельные AC IDs, но в Scope):
- no-profile → `false`: default [`me_response.py:35`](../../src/core/api/me_response.py); `test_me_missing_profile…` asserts false.
- `account_status` ≠ verified boolean: still synthetic `"active"`; openapi note [`:105`](../../docs/runtime-docs/api-reference/openapi.yaml); API_REFERENCE [`:85`](../../docs/runtime-docs/api-reference/API_REFERENCE.md).

---

## Регрессии / scope fence

| Аспект | Факт | Вердикт |
|--------|------|---------|
| No new path | Route inventory [`asgi_app.py:288-462`](../../src/core/api/asgi_app.py) — no `/verified` / alternate me | ✅ |
| Legacy method fields kept | still in defaults + profile copy | ✅ |
| Write hooks success (OOS → VB-03) | attach_* still do not set opaque (VB-01 residual; not VB-02 AC) | ✅ OOS |
| Pack / gateway / threads clients | не трогались этой story (out of scope) | ✅ |
| Remove `phone_verified` | не удалено | ✅ |

---

## Gaps (findings)

**Нет.** vs AC **0 OPEN**. Actionable gap-list пуст.

Наблюдения (**не gap**, severity none):

- Pipeline/backlog §«Verified current state» всё ещё pre-impl snapshot (`me_response.py:17-51` без opaque) — historical; AC/Nested уже synced (в отличие от VB-01 P4 DOC drift).
- Live pytest 451 — claim t04; VAL session не перезапускал → Unknown, не OPEN AC.
- Phone-verified profile с `identity_verified=False` в `test_me_with_phone_verified_profile…` — ожидаемо до VB-03 write hooks.

---

## Product Story Done vs gap-list

| | |
|--|--|
| **Product Story Done** | **да** (pipeline Meta 🟢; bullrun t01–t04 🟢; code satisfies AC 1–4 on disk) |
| **OPEN gap-list** | **пусто** (0 Critical/High/Medium/Low OPEN) |

---

## Итог / P5

- **vs AC: 0 OPEN / 4.** Material actionable set: **пусто**.
- **P5 needed?** **Нет** (zero-gap; не стартовать scaffold из VAL).
- **Next (не VAL):** P1.3 VB-03 или OP fence — VAL фазы не двигает.
