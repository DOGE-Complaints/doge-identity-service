## Task workspace — `task-ids-01-02-t02-config-package-exports`

- Story: [`../STORY-IDS-01-02-appconfig.md`](../STORY-IDS-01-02-appconfig.md)
- Decision Ref: [`../../../../../../tech-requirements/impl-epic-01-scaffold-config-launch.md`](../../../../../../tech-requirements/impl-epic-01-scaffold-config-launch.md) Task 2.2; эпик §8 верификация импортов

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000001`  
**Зависимости:** task-ids-01-02-t01-config-schema  
---

## Task: implement — config package public exports

### Цель
Экспортировать `AppConfig`, `ConfigError`, `DeploymentProfile`, `load_config_from_env` из `core.config` (заглушка `provide_app_config` до STORY-IDS-01-03 или re-export после t02 story 03).

### Факты из кода
1. Эпик §8: `from core.config import AppConfig, provide_app_config, ConfigError`.
2. Gateway: [`doge-complaints-gateway/src/core/config/__init__.py`](../../../../../../../doge-complaints-gateway/src/core/config/__init__.py) — `__all__` pattern.

### Gap / Проблема
Прямой импорт `core.config.schema` в application code нарушает границу пакета.

### AC/DoD
- [x] (P0) `src/core/config/__init__.py` экспортирует `AppConfig`, `ConfigError`, `DeploymentProfile`, `load_config_from_env`.
- [x] (P1) После STORY-IDS-01-03 — добавить `provide_app_config` в `__all__` (зафиксировано как follow-up).
- [x] (P0) `python3.11 -c "from core.config import AppConfig, ConfigError, load_config_from_env"` — exit 0.

### Где менять код
- `doge-identity-service/src/core/config/__init__.py`

### Out of scope
- Реализация `provide_app_config` body (STORY-IDS-01-03 T02)

### Команды проверки
```bash
cd doge-identity-service && . .venv/bin/activate
python3.11 -c "from core.config import AppConfig, ConfigError, load_config_from_env; print('OK')"
```
