# Аудит по коду: STORY-IDS-REQ9-02 (`make check-env` require `.env`) — 2026-09-26

> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — verified-state, только проверяемые claims с путями; регрессии; gaps с severity + как закрыть. Findings-only (без реализации).
> **Объект:** backlog [`STORY-IDS-REQ9-02-check-env-required`](../tasks/backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-02-check-env-required.md) · pipeline [`STORY-IDS-REQ9-02-check-env-required`](../tasks/epics/EPIC-IDS-16-make-env-load-parity/stories/STORY-IDS-REQ9-02-check-env-required/STORY-IDS-REQ9-02-check-env-required.md) (`input_mode=backlog_story`, pkg-000054).
> **Fence:** AC/Scope из backlog + pipeline; Product Story Done ≠ empty OPEN gap-list — оба явно. `bullrun-launch-index.md` VAL не правил.
> **Claims scope:** Read/Glob (+ write этого отчёта). Live pytest в этой сессии **не** перезапускался → suite green = Unknown (кроме артефакта t02 на диске).

---

## Вердикт

**STORY-IDS-REQ9-02 = 🟢 Done — подтверждено фактическим Makefile.** `check-env` требует `set -a && . ./.env && set +a` (тот же stanza, что `serve`/`dev`); нет `if [ -f ./.env ]`; hard dep REQ9-01 Done cited в gate. Pipeline Meta / bullrun / package INDEX: 🟢 — **совпадает** с диском t01–t02. EPIC-IDS-16 package **2/2 Done**.

| Метрика | Значение |
|---------|----------|
| Product Story Done (pipeline Meta + bullrun) | **да** |
| vs Story AC | **0 OPEN / 3** |
| Material gaps (Critical/High/Medium) | **0** |
| Doc-only OPEN | **0** |
| P5 needed? | **Нет** (zero-gap; нет TASKED) |

---

## Bullrun status touchpoints (без правок индекса)

| Якорь | Строки (approx) | Заявлено | Факт-код/docs | Вердикт |
|-------|-----------------|----------|---------------|---------|
| §Актуальная точка | bullrun ~11–12 | P3 Done REQ9-02 pkg-000054; 2/2; 456 pytest; package 2/2 | Makefile `check-env` required; 456 = claim t02 (live Unknown) | ✅; suite Unknown |
| input_mode / active story | bullrun ~134 | `backlog_story` · REQ9-02 🟢 Done | pipeline Meta 🟢; AC `[x]` | ✅ |
| Active pkg | bullrun ~136 | pkg-000054 🟢 Done, 2 paths | t01–t02 Done + acceptance PASS | ✅ |
| Epic registry EPIC-IDS-16 | bullrun ~208 | 🟢 Done — REQ9-01/02 | epic + INDEX 2/2 | ✅ |
| Task queue REQ9-02 t01–t02 | bullrun ~895–896 | все 🟢 pkg-000054 | gates + disk ниже | ✅ |
| Backlog package INDEX | INDEX:36 | REQ9-02 🟢 Done | код + pipeline | ✅ |
| Backlog Nested | backlog `:58-61` | T01–T02 🟢 Done `task-ids-16-02-*` | synced | ✅ нет Nested drift |

**Актуализация в отчёте:** t01–t02 и product story = 🟢 по диску. Строки индекса **факт-верны**.

---

## Пер-таск верификация (по коду)

| Task | Требование | Факт | Вердикт |
|------|------------|------|---------|
| **t01** check-env source | copy post-01 stanza; no `if [ -f ]`; comment not optional | [`Makefile:14-22`](../../Makefile): `set -a && . ./.env && set +a`; comment «not optional»; `rg` no optional guard in Makefile | 🟢 Done |
| **t02** story gate | AC-01…03 + dep proof | [t02 acceptance](../tasks/epics/EPIC-IDS-16-make-env-load-parity/stories/STORY-IDS-REQ9-02-check-env-required/task-ids-16-02-t02-story-gate/acceptance-verification-task-ids-16-02-t02-story-gate.md) PASS `2026-09-26T12:21:29Z`; cites REQ9-01 Done pkg-000053 | 🟢 Done (claim); live suite **Unknown** |

---

## Сверка Acceptance Criteria (backlog = pipeline Target/AC)

Источник: backlog [`:53-55`](../tasks/backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-02-check-env-required.md) = pipeline [`:56-58`](../tasks/epics/EPIC-IDS-16-make-env-load-parity/stories/STORY-IDS-REQ9-02-check-env-required/STORY-IDS-REQ9-02-check-env-required.md).

| # | AC | Факт | Вердикт |
|---|-----|------|---------|
| 1 | AC-IDS-REQ902-01: `make check-env` requires sourcing `./.env` (fail closed if absent) | [`Makefile:15-16`](../../Makefile) required source; t01 acceptance claims empty-dir fail `/bin/sh: ./.env: No such file or directory` | ✅ (pattern on disk; fail-closed = claim t01) |
| 2 | AC-IDS-REQ902-02: pattern matches post-REQ9-01 `serve`/`dev` (no optional `if [ -f ]` divergence) | Identical `set -a && . ./.env && set +a` on serve [`:4`](../../Makefile), dev [`:10`](../../Makefile), check-env [`:16`](../../Makefile); no `if [ -f ./.env ]` in Makefile | ✅ |
| 3 | AC-IDS-REQ902-03: REQ9-01 Done evidence cited in story gate | t02 gate cites pipeline REQ9-01 Meta 🟢 · pkg-000053 · P3 `2026-09-26T12:08:20Z`; REQ9-01 serve/dev required on disk | ✅ |

**Product AC OPEN count: 0.**

---

## Регрессии / scope fence

| Аспект | Факт | Вердикт |
|--------|------|---------|
| Printed keys unchanged | APP_PROFILE/PORT/SUPABASE_*/AUTHENTIGATE_ISSUER/EID_PROVIDER | ✅ |
| serve/dev stanza | unchanged required pattern (REQ9-01) | ✅ |
| No new product env keys | diagnostic echo only | ✅ |
| Runbook body | Out of scope this story (REQ9-01 owned) | ✅ OOS |

---

## Gaps (findings)

**Нет.** vs AC **0 OPEN**. Actionable gap-list пуст.

Наблюдения (**не gap**, severity none — не invent AC):

- [`run-and-healthcheck.md:47`](../../docs/runbook/run-and-healthcheck.md) всё ещё: `make check-env` … «optional `.env` until REQ9-02». После Done REQ9-02 формулировка **устарела**, но story Out of scope явно: runbook owned by REQ9-01 — **не** OPEN vs AC-IDS-REQ902-*. Optional lightweight doc refresh вне этой wave.
- §Verified current state / Dependency TODO в story — historical pre-impl; AC/Nested already Done.
- Live pytest 456 — claim t02; VAL session не перезапускал → Unknown, не OPEN AC.

---

## Product Story Done vs gap-list

| | |
|--|--|
| **Product Story Done** | **да** (pipeline Meta 🟢; bullrun t01–t02 🟢; Makefile satisfies AC 1–3) |
| **OPEN gap-list** | **пусто** (0 Critical/High/Medium/Low OPEN) |

---

## Итог / P5

- **vs AC: 0 OPEN / 3.** Material actionable set: **пусто**.
- **P5 needed?** **Нет** (zero-gap; не стартовать scaffold из VAL).
- **Next (не VAL):** epic gate EPIC-IDS-16 / optional runbook refresh / OP fence — VAL фазы не двигает.
