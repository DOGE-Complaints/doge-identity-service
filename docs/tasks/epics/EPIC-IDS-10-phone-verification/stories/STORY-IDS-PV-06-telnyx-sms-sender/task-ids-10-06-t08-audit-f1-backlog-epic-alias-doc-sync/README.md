## Task workspace — `task-ids-10-06-t08-audit-f1-backlog-epic-alias-doc-sync`

- Story: [`../STORY-IDS-PV-06-telnyx-sms-sender.md`](../STORY-IDS-PV-06-telnyx-sms-sender.md)
- Audit source: [`../../../../../../analysis/epic-ids-10-pv-06-audit-2026-06-11.md`](../../../../../../analysis/epic-ids-10-pv-06-audit-2026-06-11.md) (F1)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_10_pv_06_audit_2026_06_11`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-10-pv-06-audit-2026-06-11.md`](../../../../../../analysis/epic-ids-10-pv-06-audit-2026-06-11.md) §F1  
---

## Task: fix — backlog story + EPIC-IDS-PHONE alias sync (F1)

### Цель
Привести backlog SSOT и alias-таблицу `EPIC-IDS-PHONE` в соответствие с фактом: STORY-IDS-PV-06 🟢 Done под **EPIC-IDS-10** (pkg-000027).

### Почему это важно
Backlog и alias-epic читаются при intake; устаревший `⚪ Todo` и AC `[ ]` вводят в заблуждение (рекуррентный паттерн PV-01..05).

### Факты из кода
1. [`backlog-stories/STORY-IDS-PV-06-telnyx-sms-sender.md:6`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md) — `Status: ⚪ Todo`.
2. [`backlog-stories/...:32-36`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md) — AC checkboxes `[ ]`.
3. [`EPIC-IDS-PHONE.md:27`](../../../../../../backlog-stories/phone-verification/EPIC-IDS-PHONE.md) — строка PV-06 = `⚪ Todo`.
4. Pipeline story: [`../STORY-IDS-PV-06-telnyx-sms-sender.md`](../STORY-IDS-PV-06-telnyx-sms-sender.md) — 🟢 Done, AC [x].
5. Epic Story 6: [`EPIC-IDS-10-phone-verification.md`](../../../../EPIC-IDS-10-phone-verification.md) — 🟢 Done.

### Gap / Проблема
Doc-stale в backlog + alias epic; расхождение backlog ↔ pipeline ↔ epic (audit F1 MEDIUM).

### AC/DoD
- [x] (P0) Backlog Meta: `Status: 🟢 Done`.
- [x] (P0) AC checkboxes в backlog [x] — **verbatim** формулировки AC не менять.
- [x] (P0) `EPIC-IDS-PHONE.md` строка PV-06 → 🟢 Done.
- [x] (P1) Ссылка на pipeline story / pkg-000027 как источник исполнения.

### Где менять код
- `doge-identity-service/docs/tasks/backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md`
- `doge-identity-service/docs/tasks/backlog-stories/phone-verification/EPIC-IDS-PHONE.md` (только строка PV-06)

### Out of scope
- Изменение AC текста story (verbatim).
- Код, pytest, runtime-docs.
- Полная синхронизация таблицы `EPIC-IDS-PHONE` (PV-02/04/05 stale — отдельные волны).

### Проверка
```bash
grep -n "Status\|PV-06\|\[x\]\|\[ \]" \
  doge-identity-service/docs/tasks/backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md \
  doge-identity-service/docs/tasks/backlog-stories/phone-verification/EPIC-IDS-PHONE.md
```
