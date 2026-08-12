## Task workspace — `task-ids-08-01-t11-audit-f4-backlog-story-status-sync`

- Story: [`../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md)
- Audit source: [`../../../../../../analysis/epic-ids-08-cleanup-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-08-cleanup-01-audit-2026-06-05.md) (F4)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000012` (draft, `activation: none`)  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-08-cleanup-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-08-cleanup-01-audit-2026-06-05.md) §F4  
---

## Task: fix/docs — backlog story status and code refs sync (F4)

### Цель
Синхронизировать backlog SSOT [`STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md) с фактом P3: статус Done, AC [x], актуальные `file:line` в «Точки в коде».

### Почему это важно
Backlog-story всё ещё `⚪ Todo` с устаревшими ссылками (`db_supabase.py:315-320`, `asgi_app.py:258-310` — роуты удалены). Оператор и intake путают статус.

### Факты из кода
1. [`backlog-stories/STORY-IDS-CLEANUP-01...md:6`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md) — `Status: ⚪ Todo`.
2. [`backlog-stories/...:24-27`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md) — «Точки в коде» ссылаются на удалённые story-роуты и старые строки healthcheck.
3. [`db_supabase.py:287-291`](../../../../../../../src/core/infrastructure/db_supabase.py) — актуальный `_REQUIRED_TABLES` (3 таблицы).
4. [`asgi_app.py:26-32`](../../../../../../../src/core/api/asgi_app.py) — актуальный `PROTECTED_OPTIONS_PATHS` (без story).
5. Pipeline story: [`../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md) — 🟢 Done, AC [x].

### Gap / Проблема
Backlog SSOT не отражает завершение story; устаревшие line refs нарушают analysis.mdc traceability.

### AC/DoD
- [x] (P0) Backlog Meta `Status` → 🟢 Done (или эквивалент «Done under EPIC-IDS-08»).
- [x] (P0) AC чекбоксы [x] в backlog (формулировки AC **не менять**).
- [x] (P1) «Точки в коде» обновлены на актуальные пути/строки **или** помечены «removed in P3» без dead links на удалённый код.
- [x] (P1) Epic alias указывает на pipeline `EPIC-IDS-08` (backlog `EPIC-IDS-CLEANUP` → materialized).

### Где менять код
- [`docs/tasks/backlog-stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md) — **только** status/AC/refs (Scope/AC wording verbatim)

### Out of scope
- Изменение Scope/AC формулировок story
- Runtime code changes

### Проверка
```bash
grep -n "Status\|Todo\|Done" doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md
grep -n "258-310\|315-320" doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md
# после P3: нет устаревших dead refs
```
