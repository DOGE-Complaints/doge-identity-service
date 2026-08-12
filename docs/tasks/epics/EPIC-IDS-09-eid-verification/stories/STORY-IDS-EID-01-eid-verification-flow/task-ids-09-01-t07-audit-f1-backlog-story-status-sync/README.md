## Task workspace — `task-ids-09-01-t07-audit-f1-backlog-story-status-sync`

- Story: [`../STORY-IDS-EID-01-eid-verification-flow.md`](../STORY-IDS-EID-01-eid-verification-flow.md)
- Audit source: [`../../../../../../analysis/epic-ids-09-eid-01-audit-2026-06-06.md`](../../../../../../analysis/epic-ids-09-eid-01-audit-2026-06-06.md) (F1)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_09_eid_01_audit_2026_06_06`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-09-eid-01-audit-2026-06-06.md`](../../../../../../analysis/epic-ids-09-eid-01-audit-2026-06-06.md) §F1  
---

## Task: fix — backlog story status and epic alias sync (F1)

### Цель
Привести backlog SSOT [`STORY-IDS-EID-01-eid-verification-flow.md`](../../../../../../backlog-stories/STORY-IDS-EID-01-eid-verification-flow.md) в соответствие с фактом: story 🟢 Done под **EPIC-IDS-09** (alias `EPIC-IDS-EID`), eID mock-флоу реализован (не stub 501).

### Почему это важно
Backlog INDEX и операторы читают backlog как SSOT; устаревший `⚪ Todo`, «ещё не декомпозирован» и «Заглушки» вводят в заблуждение при следующем intake.

### Факты из кода
1. [`backlog-stories/STORY-IDS-EID-01-eid-verification-flow.md:5-6`](../../../../../../backlog-stories/STORY-IDS-EID-01-eid-verification-flow.md) — `Status: ⚪ Todo`, `Epic: EPIC-IDS-EID` (ещё не декомпозирован).
2. [`backlog-stories/...:24-26`](../../../../../../backlog-stories/STORY-IDS-EID-01-eid-verification-flow.md) — «Точки в коде» — «Заглушки» / refs 171-181, 183-217.
3. Pipeline story: [`../STORY-IDS-EID-01-eid-verification-flow.md`](../STORY-IDS-EID-01-eid-verification-flow.md) — 🟢 Done, AC [x].
4. Runtime start: [`handlers.py:114-173`](../../../../../../../src/core/api/handlers.py) — `handle_auth_eid_start`; [`asgi_app.py:196-212`](../../../../../../../src/core/api/asgi_app.py).
5. Runtime mock callback: [`handlers.py:189-330`](../../../../../../../src/core/api/handlers.py) — `handle_auth_eid_callback`; [`asgi_app.py:238-247`](../../../../../../../src/core/api/asgi_app.py).

### Gap / Проблема
Doc-stale в backlog; расхождение backlog ↔ pipeline ↔ код (audit F1 MEDIUM).

### AC/DoD
- [x] (P0) Backlog Meta: `Status: 🟢 Done`.
- [x] (P0) Epic reference: `EPIC-IDS-09` (alias `EPIC-IDS-EID` — пояснение; pipeline ID, не «ещё не декомпозирован»).
- [x] (P0) Секция «Точки в коде» отражает `handle_auth_eid_start` / `handle_auth_eid_callback` (не stub 501).
- [x] (P0) AC checkboxes в backlog [x] — **verbatim** формулировки AC не менять.
- [x] (P1) Ссылка на pipeline story / pkg-000015 как источник исполнения.

### Где менять код
- `doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-EID-01-eid-verification-flow.md` only

### Out of scope
- Изменение AC текста story (verbatim).
- Код, pytest, runtime-docs.
- F2/F3 из audit (deferred observations).

### Проверка
```bash
grep -n "Status\|501\|EPIC-IDS\|handle_auth_eid\|Заглушки" \
  doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-EID-01-eid-verification-flow.md
```
