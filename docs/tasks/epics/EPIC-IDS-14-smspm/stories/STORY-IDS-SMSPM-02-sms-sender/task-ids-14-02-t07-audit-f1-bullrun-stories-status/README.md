## Task workspace — `task-ids-14-02-t07-audit-f1-bullrun-stories-status`

- Story: [`../STORY-IDS-SMSPM-02-sms-sender.md`](../STORY-IDS-SMSPM-02-sms-sender.md)
- Prerequisite: [`task-ids-14-02-t06-story-acceptance-verification`](../task-ids-14-02-t06-story-acceptance-verification/README.md)
- Audit source: [`../../../../../../analysis/identity-smspm-02-code-audit-2026-08-20.md`](../../../../../../analysis/identity-smspm-02-code-audit-2026-08-20.md) (F1)
- P5 scaffold: `2026-08-20T10:34:39Z` (`--print-utc-now` apply-session). Gate `Date:` — only after P6 live verify.

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_14_smspm_02_audit_2026_08_20`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/identity-smspm-02-code-audit-2026-08-20.md`](../../../../../../analysis/identity-smspm-02-code-audit-2026-08-20.md) §Gaps F1  
---

## Task: docs — bullrun Stories EPIC-IDS-14 SMSPM-02 ⚪→🟢 (F1)

### Цель
В таблице Stories (EPIC-IDS-14) индекса выставить SMSPM-02 **🟢 Done (pkg-000047)**, чтобы строка совпадала с pipeline Meta / package INDEX / task queue.

### Почему это важно
Audit F1 LOW: §Актуальная точка и t01–t06 уже 🟢; строка Stories осталась ⚪. Не дефект send-кода; дрейф SSOT индекса.

### Факты из кода
1. Stories row [`bullrun-launch-index.md:887`](../../../../../bullrun-launch-index.md) — `⚪ Todo (pkg-000047)`.
2. Pipeline Meta [`STORY-IDS-SMSPM-02-sms-sender.md:7`](../STORY-IDS-SMSPM-02-sms-sender.md) — 🟢 Done.
3. Package INDEX [`smspm/INDEX.md:8`](../../../../../backlog-stories/smspm/INDEX.md) — 🟢 Done.
4. Task queue t01–t06 🟢 pkg-000047 ([`bullrun-launch-index.md`](../../../../../bullrun-launch-index.md) §Task queue EPIC-IDS-14).

### Gap / Проблема
Index drift одной строки Stories. Статусы 🟢 story/t01–t06 не менять. Product `src/` не трогать.

### AC/DoD
- [x] (P0) Stories (EPIC-IDS-14) SMSPM-02: `⚪ Todo (pkg-000047)` → `🟢 Done (pkg-000047)`.
- [x] (P1) Не менять `src/`, pytest, 🟢 статусы SMSPM-02 t01–t06 / story Done.
- [x] (P1) Не мутировать `pkg-000047`.
- [x] (P1) `acceptance-verification-task-ids-14-02-t07-audit-f1-bullrun-stories-status.md` PASS (`Date:` только P6 + `--print-utc-now`).

### Где менять код
- `doge-identity-service/docs/tasks/bullrun-launch-index.md` (Stories EPIC-IDS-14, строка SMSPM-02)

### Out of scope
- F2 `smsId` wiring (→ [`STORY-IDS-SMSPM-05-smsid-session-wire.md`](../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-05-smsid-session-wire.md))
- Runbook SMSPM-03; webhook SMSPM-04
- Product `src/` / новые тесты
- Новый `pkg-*.yaml`, смена `identity-active-package.current.yaml`

### План выполнения (P6, не P5)
1. Заменить статус строки Stories SMSPM-02 ⚪ → 🟢.
2. `rg` по таблице Stories: SMSPM-02 не ⚪.
3. Написать acceptance-verification t07 с live `--print-utc-now` для `Date:`.

### Проверка
```bash
rg -n 'STORY-IDS-SMSPM-02-sms-sender' doge-identity-service/docs/tasks/bullrun-launch-index.md
```
