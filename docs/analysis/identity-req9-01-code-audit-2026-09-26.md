# Аудит по коду: STORY-IDS-REQ9-01 (make `.env` required on serve/dev) — 2026-09-26

> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — verified-state, только проверяемые claims с путями; регрессии; gaps с severity + как закрыть. Findings-only (без реализации).
> **Объект:** backlog [`STORY-IDS-REQ9-01-make-env-required`](../tasks/backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md) · pipeline [`STORY-IDS-REQ9-01-make-env-required`](../tasks/epics/EPIC-IDS-16-make-env-load-parity/stories/STORY-IDS-REQ9-01-make-env-required/STORY-IDS-REQ9-01-make-env-required.md) (`input_mode=backlog_story`, pkg-000053).
> **Fence:** AC/Scope из backlog + pipeline; Product Story Done ≠ empty OPEN gap-list — оба явно. `bullrun-launch-index.md` VAL не правил.
> **Claims scope:** Read/Glob (+ write этого отчёта). Live pytest в этой сессии **не** перезапускался → suite green = Unknown (кроме артефакта t03 на диске).

---

## Вердикт

**STORY-IDS-REQ9-01 product scope = выполнен по фактическому коду/Makefile/docs** относительно 4 Story AC (required shell-source на `serve`/`dev`; probes unchanged; env names unchanged; runbook G8). Pipeline Meta / bullrun / package INDEX: 🟢 Done — **совпадает** с диском t01–t03.

| Метрика | Значение |
|---------|----------|
| Product Story Done (pipeline Meta + bullrun) | **да** |
| vs Story AC | **0 OPEN / 4** |
| Material gaps (Critical/High/Medium) | **0** |
| Doc-only OPEN | **1× Low** (`G-REQ901-DOC-01`) |
| P5 needed? | **Нет** для product; опционально doc-sync Low (не блокирует AC) |

---

## Bullrun status touchpoints (без правок индекса)

| Якорь | Строки (approx) | Заявлено | Факт-код/docs | Вердикт |
|-------|-----------------|----------|---------------|---------|
| §Актуальная точка | bullrun ~11–12 | P3 Done REQ9-01 pkg-000053; 3/3; 456 pytest | Makefile+env.example+runbook на диске; 456 = claim t03 (live Unknown) | ✅; suite Unknown |
| input_mode / active story | bullrun ~133 | `backlog_story` · REQ9-01 🟢 Done | pipeline Meta 🟢; AC `[x]` | ✅ |
| Active pkg | bullrun ~135 | pkg-000053 🟢 Done, 3 paths | t01–t03 Done + acceptance PASS | ✅ |
| Epic registry EPIC-IDS-16 | bullrun ~206 | 🟡 — REQ9-01 🟢; REQ9-02 backlog | package INDEX 1/2 Done | ✅ эпик не Done |
| Task queue t01–t03 | bullrun ~889–891 | все 🟢 pkg-000053 | gates + disk ниже | ✅ |
| Backlog package INDEX | INDEX:35 | REQ9-01 🟢 Done | код + pipeline | ✅ |
| Backlog Nested table | backlog `:55-59` | Meta 🟢 / AC `[x]` но Nested **Todo** + projected names | **drift** → `G-REQ901-DOC-01` | ⚠️ doc |

**Актуализация в отчёте:** t01–t03 и product story = 🟢 по диску. Единственный drift — Nested в backlog-файле (не индекс).

---

## Пер-таск верификация (по коду)

| Task | Требование | Факт | Вердикт |
|------|------------|------|---------|
| **t01** makefile serve/dev | remove `if [ -f ]`; required `set -a && . ./.env` | [`Makefile:3-12`](../../Makefile): serve/dev = `set -a && . ./.env && set +a`; **нет** optional guard на serve/dev | 🟢 Done |
| **t02** env.example + runbook | names unchanged; G8 required wording | [`.env.example:8,11-12,137`](../../.env.example); [`run-and-healthcheck.md:13-15,37,45-52`](../../docs/runbook/run-and-healthcheck.md) | 🟢 Done |
| **t03** story gate | AC-01…04 | [t03 acceptance](../tasks/epics/EPIC-IDS-16-make-env-load-parity/stories/STORY-IDS-REQ9-01-make-env-required/task-ids-16-01-t03-story-gate/acceptance-verification-task-ids-16-01-t03-story-gate.md) PASS `2026-09-26T12:08:20Z` claims 456/13 | 🟢 Done (claim); live **Unknown** |

---

## Сверка Acceptance Criteria (backlog = pipeline Target/AC)

Источник: backlog [`:48-51`](../tasks/backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md) = pipeline [`:48-51`](../tasks/epics/EPIC-IDS-16-make-env-load-parity/stories/STORY-IDS-REQ9-01-make-env-required/STORY-IDS-REQ9-01-make-env-required.md).

| # | AC | Факт | Вердикт |
|---|-----|------|---------|
| 1 | AC-IDS-REQ901-01 (G8): `make serve`/`dev` require sourcing `./.env` (fail closed), same pattern as gateway/threads | Identity [`Makefile:4-12`](../../Makefile) mirrors gateway [`:14-22`](../../../doge-complaints-gateway/Makefile) / threads [`:16-24`](../../../doge-threads/Makefile): `set -a && . ./.env && set +a` без `if [ -f ]` | ✅ |
| 2 | AC-IDS-REQ901-02: `GET /health` and `GET /ready` remain (no rename) | [`asgi_app.py:288`](../../src/core/api/asgi_app.py), [`:295`](../../src/core/api/asgi_app.py) | ✅ |
| 3 | AC-IDS-REQ901-03: `SERVICE_API_TOKEN` unchanged in `.env.example` (no rename in Makefile) | `.env.example:137` `SERVICE_API_TOKEN=`; Makefile comment lists name, no rename | ✅ |
| 4 | AC-IDS-REQ901-04: `API_BASE_URL`/`PORT` stay; runbook states required `./.env` for serve/dev | `.env.example:11-12`; runbook §1–2 required / fail if absent | ✅ |

**Product AC OPEN count: 0.**

---

## Регрессии / scope fence

| Аспект | Факт | Вердикт |
|--------|------|---------|
| `make check-env` still optional `.env` | [`Makefile:14-15`](../../Makefile) `if [ -f ./.env ]` — **OOS → REQ9-02** | ✅ |
| Probes not renamed | `/health` `/ready` only | ✅ |
| No SERVICE_API_TOKEN / peer URL rename | names present as-is | ✅ |
| `make test` / `make smoke` | untouched policy | ✅ OOS |

---

## Gaps (findings)

### OPEN

| ID | Severity | Finding | Как закрыть |
|----|----------|---------|-------------|
| **G-REQ901-DOC-01** | Low | Backlog [`STORY-IDS-REQ9-01…md`](../tasks/backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md): Meta 🟢 Done + AC `[x]`, но Nested (`:55-59`) всё ещё `Todo` + projected `task-ids-req9-01-t0N-*`; pipeline Nested = Done `task-ids-16-01-t0N-*` | Doc sync: Nested Status → Done; folder names → `task-ids-16-01-t01…t03` (как pipeline). Не требует product/Makefile patch |

### Не gap (residual / OOS)

| Note | Почему не OPEN vs REQ9-01 AC |
|------|------------------------------|
| `check-env` optional until REQ9-02 | Explicit Out of scope |
| Live pytest 456 | Claim t03; VAL session не перезапускал → Unknown, не OPEN AC |
| §Verified current state still «optional `.env`» | Historical pre-impl snapshot; AC/Meta already Done |

---

## Product Story Done vs gap-list

| | |
|--|--|
| **Product Story Done** | **да** (pipeline Meta 🟢; bullrun t01–t03 🟢; disk satisfies AC 1–4) |
| **OPEN gap-list** | **1× Low doc** (`G-REQ901-DOC-01`); **0** Critical/High/Medium; **0** product AC OPEN |

---

## Итог / P5

- **vs AC: 0 OPEN / 4.** Material actionable set: **пусто**.
- **P5 needed?** **Нет** для product. Doc Low — lightweight sync или P5 TASKED (как VB-01 G-VB01-DOC-01) по решению OP; не блокирует Story Done.
- **Next (не VAL):** P1.3/P3 REQ9-02 или OP fence — VAL фазы не двигает.
