## Task workspace — `task-ids-06-05-t03-audit-f2-smoke-exclusion-ac-doc-align`

- Story: [`../STORY-IDS-06-05-live-server-smoke.md`](../STORY-IDS-06-05-live-server-smoke.md)
- Audit source: [`../../../../../../analysis/epic-ids-06-audit-2026-06-02.md`](../../../../../../analysis/epic-ids-06-audit-2026-06-02.md) (F2)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_06_audit_2026_06_02`  
**Decision Ref:** [`../../../../../../analysis/epic-ids-06-audit-2026-06-02.md`](../../../../../../analysis/epic-ids-06-audit-2026-06-02.md) §F2  
---

## Task: fix — align smoke exclusion AC with `collect_ignore` (F2)

### Цель
Привести текст AC Story 5 и epic §8 к фактическому механизму исключения smoke из default `pytest tests/ -q`: `collect_ignore = ["smoke"]` в `tests/conftest.py`, не `testpaths`.

### Почему это важно
Поведение корректно (`test_smoke_collection_contract.py` PASS), но неверная формулировка в AC создаёт риск регрессии при будущих правках `pyproject.toml`.

### Факты из кода
1. [`tests/conftest.py:9`](../../../../../../../tests/conftest.py) — `collect_ignore = ["smoke"]`.
2. [`pyproject.toml:32`](../../../../../../../pyproject.toml) — `testpaths = ["tests"]` (включает `tests/smoke/` в дерево).
3. [`tests/test_smoke_collection_contract.py`](../../../../../../../tests/test_smoke_collection_contract.py) — подтверждает exclusion.
4. Epic §6 S5 AC и §8 — утверждают `testpaths` как причину exclusion ([`EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md)).

### Gap / Проблема
Doc↔code drift: AC описывает `testpaths`, реализация — `collect_ignore`.

### AC/DoD
- [x] (P0) Epic §6 Story 5 AC и §8 — `collect_ignore` в `tests/conftest.py`.
- [x] (P0) Story AC уже согласован (`collect_ignore`).
- [x] (P1) `pytest tests/test_smoke_collection_contract.py -q` — PASS.

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-06-testing-architecture/EPIC-IDS-06-testing-architecture.md` (§6 S5, §8)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-05-live-server-smoke/STORY-IDS-06-05-live-server-smoke.md`

### Out of scope
- Смена механизма exclusion на `norecursedirs` / сужение `testpaths` (не требуется, если doc-align).
- Smoke test implementation — уже Done.

### План выполнения
1. Найти все упоминания `testpaths` + smoke exclusion в epic/story.
2. Заменить на `collect_ignore` с ссылкой на `tests/conftest.py`.
3. Прогнать contract test.

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_smoke_collection_contract.py -q
grep -n collect_ignore doge-identity-service/docs/tasks/epics/EPIC-IDS-06-testing-architecture/EPIC-IDS-06-testing-architecture.md
```
