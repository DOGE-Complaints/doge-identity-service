## Task workspace — `task-ids-01-01-t05-audit-f1-2-story1-ac-collect-wording`

- Story: [`../STORY-IDS-01-01-init-package-and-dependencies.md`](../STORY-IDS-01-01-init-package-and-dependencies.md)
- Audit source: [`../../../../audit-report-2026-05-28.md`](../../../../audit-report-2026-05-28.md) (F1-2)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** ready  
**Wave:** `override epic_ids_01_audit_2026_05_28`  
---

## Task: fix — скорректировать формулировку AC про pytest collect

### Цель
Заменить устаревшую формулировку AC `"no tests ran"` на корректную проверку отсутствия `ModuleNotFoundError`.

### Факты из кода
1. В аудите F1-2 зафиксировано несоответствие между AC и фактическим наличием тестов.
2. В проекте присутствуют `tests/test_config_schema.py` и `tests/test_env_file.py` ([`audit-report-2026-05-28.md`](../../../../audit-report-2026-05-28.md)).

### Gap / Проблема
Текст AC вводит в заблуждение при уже существующих тестах.

### AC/DoD
- [ ] (P0) AC Story 1 обновлён: `pytest --collect-only` проходит без `ModuleNotFoundError`.
- [ ] (P0) Story gate файл отражает новую формулировку.

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-01-scaffold-config-launch/EPIC-IDS-01-scaffold-config-launch.md`
- `.../STORY-IDS-01-01-init-package-and-dependencies.md`
- `.../story-acceptance-gate-STORY-IDS-01-01.md`
