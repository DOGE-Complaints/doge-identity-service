## Task workspace — `task-ids-06-05-t04-audit-f4-smoke-marker-ssot`

- Story: [`../STORY-IDS-06-05-live-server-smoke.md`](../STORY-IDS-06-05-live-server-smoke.md)
- Audit source: [`../../../../../../analysis/epic-ids-06-audit-2026-06-02.md`](../../../../../../analysis/epic-ids-06-audit-2026-06-02.md) (F4)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_06_audit_2026_06_02`  
**Decision Ref:** [`../../../../../../analysis/epic-ids-06-audit-2026-06-02.md`](../../../../../../analysis/epic-ids-06-audit-2026-06-02.md) §F4  
---

## Task: refactor — single SSOT for `smoke` pytest marker (F4)

### Цель
Убрать дублирование объявления маркера `smoke`: оставить одно SSOT (рекомендация audit: `pyproject.toml`), синхронизировать формулировку.

### Почему это важно
Два источника (`pyproject.toml` + `pytest_configure` в smoke conftest) нарушают Single Source of Truth; при расхождении текстов — путаница для `-m smoke`.

### Факты из кода
1. [`pyproject.toml:38`](../../../../../../../pyproject.toml) — `"smoke: tests requiring a running identity server (IDENTITY_URL)"`.
2. [`tests/smoke/conftest.py:11-15`](../../../../../../../tests/smoke/conftest.py) — `pytest_configure` → `addinivalue_line("markers", "smoke: …")`.
3. [`tests/smoke/test_local_server_smoke.py:9`](../../../../../../../tests/smoke/test_local_server_smoke.py) — `pytestmark = pytest.mark.smoke`.

### Gap / Проблема
Маркер зарегистрирован дважды с чуть разными описаниями.

### AC/DoD
- [x] (P0) Маркер `smoke` только в `pyproject.toml`.
- [x] (P0) smoke collect-only 5 tests (runtime unchanged).
- [x] (P1) offline suite — 196 passed.

### Где менять код
- `doge-identity-service/pyproject.toml` (оставить SSOT)
- `doge-identity-service/tests/smoke/conftest.py` (убрать дублирующий `pytest_configure` для markers, сохранить `identity_url` fixture)

### Out of scope
- Изменение smoke test assertions.
- Регистрация маркера в CI workflows.

### План выполнения
1. Удалить `pytest_configure` marker registration из `tests/smoke/conftest.py` (или оставить только fixtures).
2. Сверить текст маркера в `pyproject.toml` с epic Story 5.
3. Прогнать smoke + offline.

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/smoke/ --collect-only -q 2>&1 | head -5
# с сервером:
# IDENTITY_URL=http://localhost:8100 .venv/bin/python -m pytest tests/smoke/ -v
```
