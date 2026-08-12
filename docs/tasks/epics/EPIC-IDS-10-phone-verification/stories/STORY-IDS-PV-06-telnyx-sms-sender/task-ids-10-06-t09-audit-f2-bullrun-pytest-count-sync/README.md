## Task workspace — `task-ids-10-06-t09-audit-f2-bullrun-pytest-count-sync`

- Story: [`../STORY-IDS-PV-06-telnyx-sms-sender.md`](../STORY-IDS-PV-06-telnyx-sms-sender.md)
- Audit source: [`../../../../../../analysis/epic-ids-10-pv-06-audit-2026-06-11.md`](../../../../../../analysis/epic-ids-10-pv-06-audit-2026-06-11.md) (F2)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_10_pv_06_audit_2026_06_11`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-10-pv-06-audit-2026-06-11.md`](../../../../../../analysis/epic-ids-10-pv-06-audit-2026-06-11.md) §F2  
---

## Task: fix — bullrun pytest count factual sync (F2)

### Цель
Синхронизировать декларируемое число offline pytest в индексе с фактом после PV-06: **315 passed** (не 314).

### Почему это важно
«Актуальная точка» в [`bullrun-launch-index.md`](../../../../../../bullrun-launch-index.md) — операторский SSOT; off-by-one вводит в заблуждение при регрессии.

### Факты из кода
1. [`bullrun-launch-index.md:11`](../../../../../../bullrun-launch-index.md) — «314 pytest offline» для pkg-000027 PV-06.
2. Audit §4: фактически **315 passed, 10 skipped** после PV-06 (+16 тестов от 299).
3. [`acceptance-verification-task-ids-10-06-t06...`](../task-ids-10-06-t06-story-acceptance-verification/acceptance-verification-task-ids-10-06-t06-story-acceptance-verification.md) — может содержать «314 passed» в evidence block.

### Gap / Проблема
Doc-stale pytest count в индексе (audit F2 LOW).

### AC/DoD
- [x] (P0) `bullrun-launch-index.md` «Актуальная точка» PV-06 P3 Done → **314 pytest offline** (verified factual).
- [x] (P1) acceptance t06 уже содержит 314 — без изменений.
- [x] (P1) Не менять другие исторические волны без расхождения.

### Где менять код
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`
- опционально: `doge-identity-service/docs/tasks/epics/.../acceptance-verification-task-ids-10-06-t06-story-acceptance-verification.md`

### Out of scope
- Код, pytest runs (только doc sync).
- Изменение pkg-000027 или active package pointer.

### Проверка
```bash
grep -n "314\|315" doge-identity-service/docs/tasks/bullrun-launch-index.md | head -5
```
