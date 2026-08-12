## Task workspace — `task-ids-03-02-t04-audit-di-1-lifespan-logging-assertion`

- Story: [`../STORY-IDS-03-02-build-api-dependencies-singleton-lifespan.md`](../STORY-IDS-03-02-build-api-dependencies-singleton-lifespan.md)
- Audit source: [`../../../../../../analysis/epic-ids-03-audit-2026-05-28.md`](../../../../../../analysis/epic-ids-03-audit-2026-05-28.md) (DI-1)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_03_audit_2026_05_28`  
---

## Task: tests — укрепить assertion в `test_lifespan_configures_logging`

### Цель
Закрыть gap DI-1: убрать безусловный `or`-fallback в assertion, чтобы тест явно проверял эффект lifespan/`configure_logging`, а не проходил из-за уровня root logger.

### Почему это важно (риск)
Слабый assertion маскирует регрессии в `_lifespan` — тест проходит даже без захвата caplog, если root logger уже в `WARNING` после предыдущих вызовов `configure_logging`.

### Факты из кода
1. [`epic-ids-03-audit-2026-05-28.md`](../../../../../../analysis/epic-ids-03-audit-2026-05-28.md) DI-1 §Story 2.
2. [`tests/test_api_dependencies.py:118–124`](../../../../../../../tests/test_api_dependencies.py): `assert any(...) or logging.getLogger().level == logging.WARNING` — fallback всегда True после `configure_logging("WARNING")`.
3. [`src/core/api/asgi_app.py:80–85`](../../../../../../../src/core/api/asgi_app.py): `_lifespan` вызывает `configure_logging(deps.config.log_level, ...)`.

### Gap / Проблема
Последний `or logging.getLogger().level == logging.WARNING` делает тест безусловно проходимым; смысл проверки lifespan размыт.

### AC/DoD
- [x] (P0) Убран безусловный `or logging.getLogger().level == logging.WARNING` из assertion.
- [x] (P0) Assertion явно проверяет эффект lifespan: root logger level == `WARNING` после `LOG_LEVEL=WARNING` и `GET /health` (см. audit L94–107).
- [x] (P1) `pytest tests/test_api_dependencies.py -q -k lifespan` проходит.

### Acceptance
- [acceptance-verification-task-ids-03-02-t04-audit-di-1-lifespan-logging-assertion.md](./acceptance-verification-task-ids-03-02-t04-audit-di-1-lifespan-logging-assertion.md) — PASS

### Где менять код
- `doge-identity-service/tests/test_api_dependencies.py` — `test_lifespan_configures_logging`

### Out of scope
- Изменения `_lifespan`, `configure_logging`, `create_app`

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_api_dependencies.py -q -k lifespan
```
