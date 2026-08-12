## Task workspace — `task-ids-01-01-t03-editable-install-verify`

- Story: [`../STORY-IDS-01-01-init-package-and-dependencies.md`](../STORY-IDS-01-01-init-package-and-dependencies.md)
- Decision Ref: [`../../../../../../tech-requirements/impl-epic-01-scaffold-config-launch.md`](../../../../../../tech-requirements/impl-epic-01-scaffold-config-launch.md) Task 1.3; эпик §Story 1 AC

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000001`  
**Зависимости:** task-ids-01-01-t01, task-ids-01-01-t02  
---

## Task: implement — editable install and import gates

### Цель
Создать `.venv`, выполнить `pip install -e ".[dev]"` (zsh: кавычки обязательны), подтвердить import/collect gates Story 1.

### Факты из кода
1. Эпик §7 Critical Pitfalls: zsh `.[dev]` требует кавычек.
2. Эпик §Story 1 AC: `import core`, `pytest --collect-only`, `pip show doge-identity-service`.

### Gap / Проблема
Без editable install CI и локальные тесты не резолвят `core.*`.

### AC/DoD
- [x] (P0) `.venv` создан; `pip install -e ".[dev]"` без ошибок.
- [x] (P0) `python3.11 -c "import core"` — exit 0.
- [x] (P0) `python3.11 -m pytest --collect-only -q` — `no tests ran`, **без** `ModuleNotFoundError`.
- [x] (P0) `pip show doge-identity-service` → Version: 0.1.0.

### Где менять код
- `doge-identity-service/.venv/` (local, не коммитить)
- Документировать в project `README.md` (P1) команды venv — опционально

### Out of scope
- Написание unit-тестов (позже stories 02–03)
- `make serve`

### Команды проверки
```bash
cd doge-identity-service
python3.11 -m venv .venv && . .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"
python3.11 -c "import core"
python3.11 -m pytest --collect-only -q
pip show doge-identity-service | grep '^Version:'
```

### Риски
- Pitfall: `uvicorn` без `--app-dir src` — документировать для STORY-IDS-01-04, не для этой задачи.
