## Task workspace — `task-ids-01-03-t03-dotenv-parser-tests`

- Story: [`../STORY-IDS-01-03-custom-dotenv-parser.md`](../STORY-IDS-01-03-custom-dotenv-parser.md)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000001`  
**Зависимости:** task-ids-01-03-t01-env-file-merge, task-ids-01-03-t02-provide-app-config  
---

## Task: tests — dotenv merge and provide_app_config

### Цель
Автотесты AC Story 3: shell priority, quoted values, comments, `provide_app_config` без файла.

### Факты из кода
1. Gateway tests (если есть): поиск `test_env` в [`doge-complaints-gateway/tests/`](../../../../../../../doge-complaints-gateway/tests/) — reference при реализации.
2. Эпик §Story 3 Acceptance Criteria — 3 пункта.

### Gap / Проблема
Регрессии merge ломают локальный `make serve` тихо (wrong `DB_BACKEND`).

### AC/DoD
- [x] (P0) `tests/test_env_file.py` — tmp `.env` + `merge_dotenv_from_path` priority case.
- [x] (P0) Test: `provide_app_config` explicit env без `.env` on disk.
- [x] (P0) `pytest tests/test_env_file.py -q` — passed.

### Где менять код
- `doge-identity-service/tests/test_env_file.py`

### Команды проверки
```bash
cd doge-identity-service && . .venv/bin/activate
python3.11 -m pytest tests/test_env_file.py -q
```
