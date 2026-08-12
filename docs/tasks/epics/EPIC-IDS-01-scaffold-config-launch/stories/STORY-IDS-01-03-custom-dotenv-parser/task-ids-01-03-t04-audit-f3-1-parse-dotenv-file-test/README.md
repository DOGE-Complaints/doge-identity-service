## Task workspace — `task-ids-01-03-t04-audit-f3-1-parse-dotenv-file-test`

- Story: [`../STORY-IDS-01-03-custom-dotenv-parser.md`](../STORY-IDS-01-03-custom-dotenv-parser.md)
- Audit source: [`../../../../audit-report-2026-05-28.md`](../../../../audit-report-2026-05-28.md) (F3-1)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** ready  
**Wave:** `override epic_ids_01_audit_2026_05_28`  
---

## Task: tests — покрыть `_parse_dotenv_file()`

### Цель
Добавить unit-тест для `_parse_dotenv_file()` с кейсами comment/empty/quoted values.

### Факты из кода
1. Аудит F3-1: `_parse_dotenv_file()` присутствует в `env_file.py`, но не покрыт тестами.
2. Story 3 outputs включает эту функцию как часть артефакта dotenv-parser.

### AC/DoD
- [ ] (P0) Тест на `_parse_dotenv_file()` добавлен в `tests/test_env_file.py`.
- [ ] (P0) Проверяются parsing rules: комменты, пустые строки, quoted values.

### Где менять код
- `doge-identity-service/tests/test_env_file.py`
