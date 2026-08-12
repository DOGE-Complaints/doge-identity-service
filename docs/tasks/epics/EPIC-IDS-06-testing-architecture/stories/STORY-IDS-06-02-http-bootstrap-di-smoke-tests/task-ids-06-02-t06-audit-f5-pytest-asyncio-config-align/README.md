## Task workspace — `task-ids-06-02-t06-audit-f5-pytest-asyncio-config-align`

- Story: [`../STORY-IDS-06-02-http-bootstrap-di-smoke-tests.md`](../STORY-IDS-06-02-http-bootstrap-di-smoke-tests.md)
- Audit source: [`../../../../../../analysis/epic-ids-06-audit-2026-06-02.md`](../../../../../../analysis/epic-ids-06-audit-2026-06-02.md) (F5)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_06_audit_2026_06_02`  
**Decision Ref:** [`../../../../../../analysis/epic-ids-06-audit-2026-06-02.md`](../../../../../../analysis/epic-ids-06-audit-2026-06-02.md) §F5  
---

## Task: refactor — align pytest async config with actual TestClient pattern (F5)

### Цель
Устранить мёртвую конфигурацию `asyncio_mode=auto` + `pytest-asyncio` при 0 async-тестов; согласовать документацию §6 S2 «Pattern source» с фактическим `fastapi.testclient.TestClient`.

### Почему это важно
Epic декларирует `httpx.AsyncClient(ASGITransport)`; реализация — синхронный TestClient ([`test_http_transport_smoke.py`](../../../../../../../tests/test_http_transport_smoke.py)). Legacy Accumulation в `pyproject.toml`.

### Факты из кода
1. [`pyproject.toml:30,35`](../../../../../../../pyproject.toml) — `asyncio_mode = "auto"`, dev dep `pytest-asyncio>=0.24.0`.
2. `grep "async def test" tests/` → **0** (audit F5).
3. [`tests/conftest.py:96-104`](../../../../../../../tests/conftest.py) — `TestClient` fixture.
4. [`docs/tech-requirements/impl-epic-06-testing-architecture.md`](../../../../../../../docs/tech-requirements/impl-epic-06-testing-architecture.md) §Story 2 — ASGITransport pattern.

### Gap / Проблема
Неиспользуемые async-настройки и расхождение pattern source vs implementation.

### AC/DoD
- [x] (P0) Путь A: удалены `asyncio_mode` + `pytest-asyncio`; epic §6 S2 → TestClient.
- [x] (P0) `pytest -m "not live_integration" -q` — 196 passed.
- [x] (P1) pytest-asyncio не в dev deps / ini — предупреждений нет.

### Где менять код
- Путь A: `doge-identity-service/pyproject.toml`
- Путь B: `doge-identity-service/docs/tasks/epics/EPIC-IDS-06-testing-architecture/EPIC-IDS-06-testing-architecture.md` §6 S2, `doge-identity-service/docs/tech-requirements/impl-epic-06-testing-architecture.md` §Story 2

### Out of scope
- Миграция HTTP smoke на `AsyncClient` / ASGITransport (отдельный scope, не требуется для gap-close).
- Live integration tests.

### План выполнения
1. Зафиксировать A/B в BULLRUN.
2. Минимальный diff по выбранному пути.
3. Полный offline suite.

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest -m "not live_integration" -q
grep -c "async def test" tests/**/*.py 2>/dev/null || true
```
