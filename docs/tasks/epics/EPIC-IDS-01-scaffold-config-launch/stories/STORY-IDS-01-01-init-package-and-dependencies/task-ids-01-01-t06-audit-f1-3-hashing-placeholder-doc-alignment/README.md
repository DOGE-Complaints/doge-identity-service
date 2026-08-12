## Task workspace — `task-ids-01-01-t06-audit-f1-3-hashing-placeholder-doc-alignment`

- Story: [`../STORY-IDS-01-01-init-package-and-dependencies.md`](../STORY-IDS-01-01-init-package-and-dependencies.md)
- Audit source: [`../../../../audit-report-2026-05-28.md`](../../../../audit-report-2026-05-28.md) (F1-3)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** ready  
**Wave:** `override epic_ids_01_audit_2026_05_28`  
---

## Task: fix — согласовать документацию `hashing.py` с реализацией

### Цель
Убрать слово `placeholder` в Story 1 там, где `hash_secret(...)` уже реализован.

### Факты из кода
1. Аудит F1-3 фиксирует полноценную реализацию `hash_secret` в `src/core/security/hashing.py`.
2. В story/epic тексте ещё встречается формулировка `placeholder`.

### Gap / Проблема
Документация расходится с фактическим состоянием кода.

### AC/DoD
- [ ] (P0) Формулировка Story 1 Outputs обновлена на «реализован».
- [ ] (P0) Нет упоминания `placeholder` для `hashing.py` в Story 1 артефактах.

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-01-scaffold-config-launch/EPIC-IDS-01-scaffold-config-launch.md`
- `.../STORY-IDS-01-01-init-package-and-dependencies.md`
