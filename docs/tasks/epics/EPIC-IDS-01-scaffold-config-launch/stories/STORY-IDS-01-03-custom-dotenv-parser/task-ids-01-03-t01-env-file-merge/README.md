## Task workspace — `task-ids-01-03-t01-env-file-merge`

- Story: [`../STORY-IDS-01-03-custom-dotenv-parser.md`](../STORY-IDS-01-03-custom-dotenv-parser.md)
- Decision Ref: [`../../../../../../tech-requirements/impl-epic-01-scaffold-config-launch.md`](../../../../../../tech-requirements/impl-epic-01-scaffold-config-launch.md) Task 3.1; [`../../../../../../requirements/06-technical-scaffold.md`](../../../../../../requirements/06-technical-scaffold.md) §Шаг 2

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000001`  
**Зависимости:** STORY-IDS-01-02  
---

## Task: implement — env_file.py dotenv merge

### Цель
Скопировать 1:1 паттерн gateway: `merge_dotenv_from_cwd`, `merge_dotenv_from_path`, `_parse_dotenv_file`; shell keys в `priority` не перезаписываются.

### Факты из кода
1. Reference: [`doge-complaints-gateway/src/core/config/env_file.py`](../../../../../../../doge-complaints-gateway/src/core/config/env_file.py).
2. Эпик §Story 3: без identity-specific изменений в парсере.

### Gap / Проблема
Без merge `.env` uvicorn/Makefile не видят переменные (нет python-dotenv).

### AC/DoD
- [x] (P0) `src/core/config/env_file.py` с тремя функциями из impl-epic Task 3.1.
- [x] (P0) `priority` frozenset — ключи из shell не перезаписываются файлом.
- [x] (P0) `#` comments и пустые строки игнорируются; quote stripping.

### Где менять код
- `doge-identity-service/src/core/config/env_file.py`

### Out of scope
- `provide_app_config` (T02)

### Команды проверки
```bash
cd doge-identity-service && . .venv/bin/activate
python3.11 -c "from core.config.env_file import merge_dotenv_from_path; print('OK')"
```
