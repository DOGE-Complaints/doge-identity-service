## Task workspace — `task-ids-08-03-t03-req15-deprecated-verify-doc1`

- Story: [`../STORY-IDS-CLEANUP-03-doc-drift.md`](../STORY-IDS-CLEANUP-03-doc-drift.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-03-doc-drift.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-03-doc-drift.md) Scope DOC-1; CLEANUP-01 [`../../STORY-IDS-CLEANUP-01-remove-stories-from-identity/task-ids-08-01-t05-migration-fate-and-req15-deprecated/README.md`](../../STORY-IDS-CLEANUP-01-remove-stories-from-identity/task-ids-08-01-t05-migration-fate-and-req15-deprecated/README.md)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000014`  
**Skill declared:** python-pro  
---

## Task: fix/docs — req-15 deprecated verify (DOC-1)

### Цель
Закрыть gap DOC-1: [`req-15`](../../../../../../../docs/requirements/15-story-authorization.md) помечен deprecated; форвард identity→gateway отменён (пересекается с CLEANUP-01).

### Почему это важно
Story AC #3 (partial); без явного deprecated status req-15 читается как активная спека story endpoints в identity.

### Факты из кода
1. [`req-15:3`](../../../../../../../docs/requirements/15-story-authorization.md) — `> **DEPRECATED (2026-06):**` banner **уже** present (CLEANUP-01 t05).
2. [`req-15:6`](../../../../../../../docs/requirements/15-story-authorization.md) — body still describes story endpoints in identity scope.
3. CLEANUP-01 story AC #4 — req-15 deprecated (Done).

### Gap / Проблема
Backlog Scope просит «пометить устаревшим» — banner exists; task = **verify-first**, enhance header/status only if insufficient for AC#3.

### AC/DoD
- [x] (P0) **Branch A (verify):** DEPRECATED banner at top of req-15 sufficient → document verify-only closure referencing CLEANUP-01 t05.
- [x] (P0) **Branch B (enhance):** if status line still reads as active spec → minimal header alignment (e.g. status DEPRECATED) without rewriting req-15 body.
- [x] (P0) Story AC #3 (partial): req-15 deprecated state evidenced.
- [x] (P1) BULLRUN-PHASE-LOG + acceptance-verification в этой папке (P3).

### Где менять код
- [`docs/requirements/15-story-authorization.md`](../../../../../../../docs/requirements/15-story-authorization.md) — header/status only (Branch B)

### Out of scope
- Удаление req-15 файла
- Rewrite story endpoint specs (historical reference retained)
- Gateway story implementation

### Проверка
```bash
cd doge-identity-service
head -10 docs/requirements/15-story-authorization.md | grep -i deprecated
```
