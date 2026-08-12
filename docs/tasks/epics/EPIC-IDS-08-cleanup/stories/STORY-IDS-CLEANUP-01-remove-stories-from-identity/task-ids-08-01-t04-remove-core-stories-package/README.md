## Task workspace — `task-ids-08-01-t04-remove-core-stories-package`

- Story: [`../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md) Scope п.4

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000011`  
**Skill declared:** python-pro  
---

## Task: refactor — remove core.stories package

### Цель
Удалить пустой пакет `src/core/stories/` и все импорты/ссылки на него.

### Почему это важно
Заготовка без поведения создаёт ложное впечатление, что story-логика живёт в identity. Story AC #2.

### Факты из кода
1. [`src/core/stories/__init__.py`](../../../../../../../src/core/stories/__init__.py) — единственный файл, docstring-only.
2. Grep по `core.stories` / `from core.stories` в `src/` и `tests/`.

### Gap / Проблема
Пустой пакет остаётся в дереве модулей после выноса stories в gateway.

### AC/DoD
- [x] (P0) Директория `src/core/stories/` удалена.
- [x] (P0) Нет импортов `core.stories` в кодовой базе.
- [x] (P0) Story AC #2: grep `core\.stories|core/stories` = 0.

### Где менять код
- Удалить [`src/core/stories/`](../../../../../../../src/core/stories/)
- Проверить и убрать импорты в `src/`, `tests/` (если найдены)

### Out of scope
- Gateway story implementation
- Runtime-docs update (вне scope story)

### Проверка
```bash
cd doge-identity-service
test ! -d src/core/stories
rg "core\.stories|core/stories" src tests
# ожидание: 0 matches
```
