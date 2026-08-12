## Task workspace — `task-ids-06-03-t04-audit-f3-tests-package-init-files`

- Story: [`../STORY-IDS-06-03-live-supabase-integration.md`](../STORY-IDS-06-03-live-supabase-integration.md)
- Audit source: [`../../../../../../analysis/epic-ids-06-audit-2026-06-02.md`](../../../../../../analysis/epic-ids-06-audit-2026-06-02.md) (F3)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_06_audit_2026_06_02`  
**Decision Ref:** [`../../../../../../analysis/epic-ids-06-audit-2026-06-02.md`](../../../../../../analysis/epic-ids-06-audit-2026-06-02.md) §F3  
---

## Task: fix — tests package `__init__.py` vs epic §5 (F3)

### Цель
Закрыть расхождение epic §5 «Целевые файлы» и фактического дерева: отсутствуют `tests/integration/__init__.py` и `tests/smoke/__init__.py` (есть только `tests/integration/supabase/__init__.py`).

### Почему это важно
Architectural drift в SSOT эпика; импорты работают через `pythonpath` + namespace packages, но spec-vs-reality путает операторов и CI.

### Факты из кода
1. Epic §5 — перечисляет три `__init__.py` под `tests/integration/` и `tests/smoke/`.
2. Факт: [`tests/integration/supabase/__init__.py`](../../../../../../../tests/integration/supabase/__init__.py) существует; `tests/integration/__init__.py` и `tests/smoke/__init__.py` — **нет** (audit F3).
3. [`tests/integration/supabase/test_supabase_identity_roundtrip.py:18`](../../../../../../../tests/integration/supabase/test_supabase_identity_roundtrip.py) — импорт из `tests.integration.supabase.conftest` работает.
4. [`pyproject.toml:31`](../../../../../../../pyproject.toml) — `pythonpath = ["src", "tests"]`.

### Gap / Проблема
§5 эпика не совпадает с деревом; нужно явное решение: добавить файлы **или** обновить §5.

### AC/DoD
- [x] (P0) Вариант A: пустые `__init__.py` добавлены.
- [x] (P0) Epic §5 и дерево совпадают.
- [x] (P1) `pytest -m "not live_integration" -q` — 196 passed.

### Где менять код
- Вариант A: `doge-identity-service/tests/integration/__init__.py`, `doge-identity-service/tests/smoke/__init__.py` (пустые)
- Вариант B: `doge-identity-service/docs/tasks/epics/EPIC-IDS-06-testing-architecture/EPIC-IDS-06-testing-architecture.md` §5

### Out of scope
- Live Supabase test logic (Story 3 Done).
- Перенос `tests/integration/supabase/conftest.py`.

### План выполнения
1. Зафиксировать выбор A/B в BULLRUN (одна строка обоснования).
2. Применить минимальный diff.
3. Offline pytest.

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest -m "not live_integration" -q
ls -la tests/integration/__init__.py tests/smoke/__init__.py 2>/dev/null || true
```
