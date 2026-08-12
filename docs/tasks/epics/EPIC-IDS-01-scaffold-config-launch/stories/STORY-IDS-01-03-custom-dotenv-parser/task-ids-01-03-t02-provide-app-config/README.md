## Task workspace — `task-ids-01-03-t02-provide-app-config`

- Story: [`../STORY-IDS-01-03-custom-dotenv-parser.md`](../STORY-IDS-01-03-custom-dotenv-parser.md)
- Epic: [`../../../../EPIC-IDS-01-scaffold-config-launch.md`](../../../../EPIC-IDS-01-scaffold-config-launch.md) §Story 3 Outputs

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000001`  
**Зависимости:** task-ids-01-03-t01-env-file-merge, task-ids-01-02-t01-config-schema  
---

## Task: implement — provide_app_config provider

### Цель
`provide_app_config(env=None)`: production — `os.environ` + `.env` merge; tests — explicit mapping only. Defaults: `APP_PROFILE=demo`, `API_BASE_URL=http://localhost:8100`.

### Факты из кода
1. Reference: [`doge-complaints-gateway/src/core/config/providers.py`](../../../../../../../doge-complaints-gateway/src/core/config/providers.py) — заменить default API URL `8000` → `8100`.
2. Эпик §Story 3 AC: `provide_app_config({...})` без `.env` file.

### Gap / Проблема
Application entrypoints не должны вызывать `load_config_from_env(os.environ)` напрямую.

### AC/DoD
- [x] (P0) `src/core/config/providers.py` реализует контракт impl-epic Task 3.2.
- [x] (P0) `core.config.__init__` экспортирует `provide_app_config`.
- [x] (P0) `provide_app_config({"APP_PROFILE":"demo","API_BASE_URL":"http://localhost:8100","DB_BACKEND":"in_memory"})` → `AppConfig`.

### Где менять код
- `doge-identity-service/src/core/config/providers.py`
- `doge-identity-service/src/core/config/__init__.py`

### Out of scope
- Makefile `set -a` (STORY-IDS-01-04) — complementary

### Команды проверки
```bash
cd doge-identity-service && . .venv/bin/activate
python3.11 -c "from core.config import provide_app_config; c=provide_app_config({'APP_PROFILE':'demo','API_BASE_URL':'http://localhost:8100','DB_BACKEND':'in_memory','EID_PROVIDER':'mock'}); print(c.port)"
```
