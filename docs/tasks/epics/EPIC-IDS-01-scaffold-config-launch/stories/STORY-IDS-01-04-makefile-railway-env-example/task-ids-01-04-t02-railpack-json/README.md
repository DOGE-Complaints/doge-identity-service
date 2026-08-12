## Task workspace — `task-ids-01-04-t02-railpack-json`

- Story: [`../STORY-IDS-01-04-makefile-railway-env-example.md`](../STORY-IDS-01-04-makefile-railway-env-example.md)
- Decision Ref: [`../../../../../../tech-requirements/impl-epic-01-scaffold-config-launch.md`](../../../../../../tech-requirements/impl-epic-01-scaffold-config-launch.md) Task 4.2; эпик §7 (`${PORT:-8100}`)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000001`  
---

## Task: implement — railpack.json Railway start command

### Цель
JSON deploy config: `--host 0.0.0.0`, `--port ${PORT:-8100}`, `--app-dir src`, module `core.api.asgi_app:app`.

### Факты из кода
1. Эпик §Story 4 Outputs — `railpack.json` shape.
2. Gateway reference: [`doge-complaints-gateway/railpack.json`](../../../../../../../doge-complaints-gateway/railpack.json) если существует.

### Gap / Проблема
Railway без `0.0.0.0` / dynamic PORT не биндит контейнер.

### AC/DoD
- [x] (P0) `railpack.json` валидный JSON (`python3 -m json.tool`).
- [x] (P0) `startCommand` содержит `--host 0.0.0.0`, `${PORT:-8100}`, `--app-dir src`, `core.api.asgi_app:app`.

### Где менять код
- `doge-identity-service/railpack.json`

### Команды проверки
```bash
cd doge-identity-service && python3 -m json.tool railpack.json > /dev/null && echo OK
```
