## Task workspace — `task-ids-05-02-t05-audit-s2-2-mark-consumed-started-guard`

- Story: [`../STORY-IDS-05-02-supabase-repositories-identity-set.md`](../STORY-IDS-05-02-supabase-repositories-identity-set.md)
- Re-audit source: [`../../../../re-audit-report-2026-06-02.md`](../../../../re-audit-report-2026-06-02.md) (S2-2)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_05_reaudit_2026_06_02`  
**Decision Ref:** [`../../../../re-audit-report-2026-06-02.md`](../../../../re-audit-report-2026-06-02.md) §S2-2  
---

## Task: fix — guard `mark_consumed` with `status=eq.started` (S2-2)

### Цель
Добавить lifecycle-guard в PATCH `mark_consumed`, чтобы смена статуса в `consumed` применялась только к сессиям в `started`.

### Факты из кода
1. [`src/core/infrastructure/db_supabase.py:518-524`](../../../../../../../src/core/infrastructure/db_supabase.py) — PATCH идёт только по `id`.
2. [`src/core/infrastructure/db_supabase.py:505-512`](../../../../../../../src/core/infrastructure/db_supabase.py) — паттерн фильтра `status=eq.started` уже используется в `get_by_state`.
3. [`../../../../re-audit-report-2026-06-02.md`](../../../../re-audit-report-2026-06-02.md) — S2-2 подтверждён как открытый.

### Gap / Проблема
Без guard можно перезаписать терминальные статусы (`failed`/`expired`) при повторном вызове.

### Out of scope
- Guard для `mark_failed` (наблюдение re-audit, не gap этой волны).
- InMemory-аналог в `repositories.py`.

### AC/DoD
- [x] В `mark_consumed` params содержит `"status": "eq.started"`.
- [x] Добавлен тест, проверяющий params PATCH-запроса.
- [x] Поведение остальных методов store не меняется.

### Где менять код
- `doge-identity-service/src/core/infrastructure/db_supabase.py`
- `doge-identity-service/tests/test_db_supabase_repositories.py`

### План выполнения
1. Обновить params в `mark_consumed`.
2. Добавить/обновить unit-тест на формирование params.
3. Не менять `mark_failed` и прочие lifecycle-методы в этой задаче.

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_db_supabase_repositories.py -v -k mark_consumed
```
