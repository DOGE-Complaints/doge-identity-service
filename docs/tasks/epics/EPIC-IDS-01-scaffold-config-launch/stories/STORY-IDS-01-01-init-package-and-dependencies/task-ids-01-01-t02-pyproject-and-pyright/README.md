## Task workspace — `task-ids-01-01-t02-pyproject-and-pyright`

- Story: [`../STORY-IDS-01-01-init-package-and-dependencies.md`](../STORY-IDS-01-01-init-package-and-dependencies.md)
- Decision Ref: [`../../../../../../requirements/06-technical-scaffold.md`](../../../../../../requirements/06-technical-scaffold.md) §Шаг 2–3; [`../../../../EPIC-IDS-01-scaffold-config-launch.md`](../../../../EPIC-IDS-01-scaffold-config-launch.md) §Story 1 Outputs

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000001`  
---

## Task: implement — pyproject.toml and pyrightconfig.json

### Цель
Зафиксировать `name = "doge-identity-service"`, setuptools `where = ["src"]`, pytest `pythonpath`, markers `live_integration` + `mock_oidc`, deps `joserfc` + `cryptography`.

### Факты из кода
1. `pyproject.toml` в [`doge-identity-service/`](../../../../../../../) — отсутствует.
2. Spec: [`requirements/06-technical-scaffold.md`](../../../../../../requirements/06-technical-scaffold.md) §Шаг 2 — полный TOML-образец.
3. Эпик Story 1: `requires-python >=3.11`, dev pytest stack, **без** `python-dotenv`.

### Gap / Проблема
Без manifest Python не находит `core` при editable install; pytest collect падает.

### AC/DoD
- [x] (P0) `[project] name = "doge-identity-service"`, `version = "0.1.0"`, `requires-python = ">=3.11"`.
- [x] (P0) Runtime deps: `fastapi`, `uvicorn`, `psycopg[binary]`, `httpx`, `joserfc>=1.0.0`, `cryptography>=42.0.0`.
- [x] (P0) `[tool.pytest.ini_options] pythonpath = ["src", "tests"]`, markers `live_integration`, `mock_oidc`.
- [x] (P0) `pyrightconfig.json`: `include` src/tests, `pythonVersion` 3.11 (req-06 §Шаг 3).
- [x] (P1) Нет зависимости `python-dotenv` / `pydantic-settings`.

### Где менять код
- `doge-identity-service/pyproject.toml`
- `doge-identity-service/pyrightconfig.json`

### Out of scope
- `pip install` (T03)
- Реализация config modules

### Команды проверки
```bash
cd doge-identity-service && python3.11 -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"
test -f pyrightconfig.json && echo OK
```
