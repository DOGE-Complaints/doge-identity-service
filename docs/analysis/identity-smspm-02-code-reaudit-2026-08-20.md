# Re-audit gaps STORY-IDS-SMSPM-02 (post-override `epic_ids_14_smspm_02_audit_2026_08_20`) — 2026-08-20

> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями. Findings-only.
> **P4:** [`identity-smspm-02-code-audit-2026-08-20.md`](./identity-smspm-02-code-audit-2026-08-20.md) (`$priorReaudit` = тот же файл, pass N−1).
> **P5 SSOT:** [`.cursor/plans/ID_builder.plan.md`](../../../.cursor/plans/ID_builder.plan.md) §«Явно прописанный safe-override (EPIC-IDS-14 SMSPM-02 audit 2026-08-20)» (`run_mode=epic_ids_14_smspm_02_audit_2026_08_20`).
> **P8 не стартовать.**

---

## Вердикт

**WAVE COMPLETE.** Disposition P5 полная (F1+F2). **OPEN = 0. Incomplete TASKED = 0.**

Правки по **actionable** gap-листу **выполнены** (F1 TASKED t07 — Stories SMSPM-02 ⚪→🟢 на диске). F2 остаётся **WAIVED** (reason=out-of-DoD всё ещё верен; handler/`SmsSenderPort` без `sms_id` — не требовать патч в этой wave).

**Product Story SMSPM-02 = 🟢 Done (vs AC 0 OPEN)** ≠ исторический gap-list: F1 CLOSED, F2 WAIVED recorded → SMSPM-05 draft.

**Не WAVE_STALLED_NO_DELTA:** vs P4 есть delta по F1 (Stories row ⚪ Todo → 🟢 Done). Нет новых Critical/Medium OPEN.

**Не P5_DISPOSITION_INCOMPLETE:** у обоих gap ID есть Disposition + Follow_up.

---

## P5 map (принято)

Источник: [`ID_builder.plan.md:58-63`](../../../.cursor/plans/ID_builder.plan.md).

| Gap | Sev | P5 Disposition | Follow_up | Path на диске | P7 result |
|-----|-----|----------------|-----------|---------------|-----------|
| **F1** | LOW | TASKED | none | [`task-ids-14-02-t07-…/README.md`](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-02-sms-sender/task-ids-14-02-t07-audit-f1-bullrun-stories-status/README.md) exists; README Status `done` | **CLOSED** |
| **F2** | LOW | WAIVED reason=out-of-DoD | new_story | [`STORY-IDS-SMSPM-05-smsid-session-wire.md`](../tasks/backlog-stories/smspm/STORY-IDS-SMSPM-05-smsid-session-wire.md) exists (Meta ⚪ Todo draft) | **WAIVED** (keep) |

Missing disposition: **нет**.

---

## Per-gap verify

### F1 — TASKED / claimed CLOSED → **CLOSED**

P4: Stories EPIC-IDS-14 SMSPM-02 = ⚪ Todo при Meta/INDEX/t01–t06 🟢 ([P4 §Gaps F1](./identity-smspm-02-code-audit-2026-08-20.md); тогда `:887`).

| Проверка | Факт | Вердикт |
|----------|------|---------|
| Stories SMSPM-02 status | [`bullrun-launch-index.md:891`](../tasks/bullrun-launch-index.md) = `🟢 Done (pkg-000047)` | ✅ |
| нет ⚪ Todo на этой story | строка `:891` не содержит `⚪ Todo` | ✅ |
| t07 gate | PASS `2026-08-20T10:37:37Z` ([t07 acceptance](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-02-sms-sender/task-ids-14-02-t07-audit-f1-bullrun-stories-status/acceptance-verification-task-ids-14-02-t07-audit-f1-bullrun-stories-status.md)) | ✅ |
| bullrun t07 | 🟢 Done override ([bullrun:821](../tasks/bullrun-launch-index.md)) | ✅ |
| product `src/` не «закрывал» F1 | t07 docs-only; HTTP send не регрессировал | ✅ |

**Delta vs P4:** Stories ⚪→🟢 (ожидаемая). Не reopen.

Наблюдение (не gap): t07 evidence ссылался на `:890`; сейчас SMSPM-02 = `:891` (в `:890` — SMSPM-01 🟢). Сдвиг строк индекса; статус целевой story 🟢.

### F2 — WAIVED → **WAIVED** (reason still applies)

P4: D-02-6 optional `smsId` не с `/auth/phone/request`; не AC SMSPM-02.

| Проверка | Факт | Вердикт |
|----------|------|---------|
| reason=out-of-DoD | SMSPM-05 D-05-3: вне AC SMSPM-02; Port+all senders = новая поверхность ([SMSPM-05:15-25](../tasks/backlog-stories/smspm/STORY-IDS-SMSPM-05-smsid-session-wire.md)) | ✅ всё ещё верно |
| follow_up=new_story | файл [`STORY-IDS-SMSPM-05-smsid-session-wire.md`](../tasks/backlog-stories/smspm/STORY-IDS-SMSPM-05-smsid-session-wire.md) на диске; INDEX row 5 draft ([INDEX:11](../tasks/backlog-stories/smspm/INDEX.md)) | ✅ |
| нет патча handler/port | [`handlers.py:504`](../../src/core/api/handlers.py) `send(to_e164=…, text=…)`; [`base.py:42`](../../src/core/phone/base.py) без `sms_id` | **не reopen OPEN** |

---

## Stop-rule vs `$priorReaudit` (P4)

| Gap | P4 status+evidence | P7 | Delta? |
|-----|-------------------|-----|--------|
| F1 | OPEN residual: Stories ⚪ Todo (`:887`) | CLOSED: 🟢 Done (`:891`) | **да** |
| F2 | residual optional smsId / new surface | WAIVED, handler unchanged, SMSPM-05 exists | evidence handler same (ожидаемо WAIVED) |

Новых Critical/Medium OPEN: **0**. WAVE_STALLED_NO_DELTA **не** срабатывает (F1 delta nonempty).

---

## Product vs gap-list

| Метрика | Значение |
|---------|----------|
| Product Story Done (AC/DoD SMSPM-02) | 🟢 да (P4: 5/5 AC; P7 не переоткрывает) |
| OPEN gaps this wave | **0** |
| Incomplete TASKED | **0** |
| WAIVED recorded | F2 → SMSPM-05 draft |
| HTTP send / live skip | вне этой gap-волны (уже в P3) |

---

## Handoff

- WAVE COMPLETE. P8 не стартовать из этого отчёта.
- Следующий продукт (не эта VAL-волна): SMSPM-03 / SPIKE-01; F2 живёт в SMSPM-05 (optional PA.3).
