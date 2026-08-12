## Task workspace — `task-ids-08-01-t10-audit-f3-remove-empty-stories-directory`

- Story: [`../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md)
- Audit source: [`../../../../../../analysis/epic-ids-08-cleanup-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-08-cleanup-01-audit-2026-06-05.md) (F3)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000012` (draft, `activation: none`)  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-08-cleanup-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-08-cleanup-01-audit-2026-06-05.md) §F3 · t04 follow-up  
---

## Task: refactor — remove empty core/stories directory (F3)

### Цель
Удалить пустой каталог `src/core/stories/` после удаления `__init__.py` в t04.

### Почему это важно
t04 DoD требовал удалить пакет; пустая директория — residual-мусор, создаёт ложное впечатление наличия модуля.

### Факты из кода
1. `src/core/stories/` — существует, **0 файлов** (проверено 2026-06-05; `__init__.py` удалён в P3 t04).
2. [`src/`](../../../../../../../src/) — grep `core.stories` = 0.
3. Audit t04: [`epic-ids-08-cleanup-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-08-cleanup-01-audit-2026-06-05.md) §1 t04 «🟢 c оговоркой».

### Gap / Проблема
Git не отслеживает пустые каталоги; директория осталась локально после удаления единственного файла.

### AC/DoD
- [x] (P0) `src/core/stories/` отсутствует в рабочем дереве (или не создаётся при checkout).
- [x] (P1) Story AC #2: grep `core/stories` = 0 (уже выполнено для импортов).

### Где менять код
- Удалить [`src/core/stories/`](../../../../../../../src/core/stories/) (пустой каталог)

### Out of scope
- Gateway story implementation
- Reopen t04 README status (audit gap only)

### Проверка
```bash
test ! -d doge-identity-service/src/core/stories
```
