## Task workspace — `task-ids-10-10-t08-audit-f1-pipeline-story-timestamp-example-sync`

- Story: [`../STORY-IDS-PV-10-file-sms-sink-dev.md`](../STORY-IDS-PV-10-file-sms-sink-dev.md)
- Audit source: [`../../../../../../analysis/epic-ids-10-pv-10-file-sms-sink-audit-2026-06-28.md`](../../../../../../analysis/epic-ids-10-pv-10-file-sms-sink-audit-2026-06-28.md) (F1)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** 🟢 Done  
**Wave:** `override epic_ids_10_pv_10_audit_2026_06_28`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-10-pv-10-file-sms-sink-audit-2026-06-28.md`](../../../../../../analysis/epic-ids-10-pv-10-file-sms-sink-audit-2026-06-28.md) §F1; backlog already synced (P4 audit pass)  
---

## Task: fix — pipeline story timestamp example sync (F1)

### Цель
Привести секцию «Целевое поведение» pipeline story к секундной точности UTC ISO — parity с кодом `FileSmsSender` и backlog story (уже исправлен в P4 audit).

### Почему это важно
Пример с миллисекундами (`.345Z`) не воспроизводится дословно при `SMS_PROVIDER=file`; нарушает «examples must be real» для операторов ручного теста.

### Факты из кода
1. Pipeline stale: [`../STORY-IDS-PV-10-file-sms-sink-dev.md:27-28`](../STORY-IDS-PV-10-file-sms-sink-dev.md) — `2026-06-28T10:01:02.345Z`, `.118Z`.
2. Backlog OK: [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md:24-25`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md) — `T10:01:02Z`, `T10:03:40Z`.
3. Код: [`file_sender.py:14-17`](../../../../../../../src/core/phone/file/file_sender.py) — `.replace(microsecond=0)` → секундная точность.
4. Audit F1: [`epic-ids-10-pv-10-file-sms-sink-audit-2026-06-28.md`](../../../../../../analysis/epic-ids-10-pv-10-file-sms-sink-audit-2026-06-28.md) §2 F1.

### Gap / Проблема
Pipeline story example показывает ms; backlog + runtime пишут секунды (audit F1 LOW, open at P5 scaffold).

### AC/DoD
- [x] (P0) Pipeline «Целевое поведение»: заменить `.345Z`/`.118Z` → `T10:01:02Z` / `T10:03:40Z` (match backlog verbatim).
- [x] (P1) `grep` не находит `345Z`/`118Z` в pipeline story.
- [x] (P1) Backlog + pipeline examples aligned on second-precision timestamps.

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/STORY-IDS-PV-10-file-sms-sink-dev.md` (§«Целевое поведение» only)

### Out of scope
- `file_sender.py`, pytest, runtime code.
- Backlog story (already fixed).
- Epic §Story 10 (no ms example there unless found at P6 — mirror only if needed).
- F2 EPIC-IDS-PHONE header (closed inline in P4 audit).

### Проверка
```bash
grep -n "345Z\|118Z" \
  doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/STORY-IDS-PV-10-file-sms-sink-dev.md
# expect: no matches
grep -n "T10:01:02Z" \
  doge-identity-service/docs/tasks/backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md \
  doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/STORY-IDS-PV-10-file-sms-sink-dev.md
```
