## Task workspace — `task-ids-05-02-t04-audit-s2-1-oauth-store-env-doc`

- Story: [`../STORY-IDS-05-02-supabase-repositories-identity-set.md`](../STORY-IDS-05-02-supabase-repositories-identity-set.md)
- Re-audit source: [`../../../../re-audit-report-2026-06-02.md`](../../../../re-audit-report-2026-06-02.md) (S2-1)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_05_reaudit_2026_06_02`  
**Decision Ref:** [`../../../../re-audit-report-2026-06-02.md`](../../../../re-audit-report-2026-06-02.md) §S2-1  
---

## Task: docs — explain env-only behavior in `SupabaseOAuthClientStore` (S2-1)

### Цель
Добавить документацию в `SupabaseOAuthClientStore`, что параметр `db` принимается для консистентной сигнатуры, но источник OAuth clients сейчас — env/fallback config.

### Факты из кода
1. [`src/core/infrastructure/db_supabase.py:584-592`](../../../../../../../src/core/infrastructure/db_supabase.py) — конструктор принимает `db`, затем делает `del db`.
2. [`src/core/infrastructure/providers.py:74-86`](../../../../../../../src/core/infrastructure/providers.py) — store инициализируется в supabase-ветке через `fallback_config`.
3. [`../../../../re-audit-report-2026-06-02.md`](../../../../re-audit-report-2026-06-02.md) — S2-1 остаётся открытым именно как documentation gap.

### Gap / Проблема
Поведение env-only не очевидно из кода и выглядит как возможный дефект контракта.

### Out of scope
- Удаление параметра `db` из сигнатуры (сломает единообразие вызова в `providers.py`).
- Загрузка OAuth clients из БД-таблицы (вне scope EPIC-IDS-05 re-audit).

### AC/DoD
- [x] Добавлен class docstring у `SupabaseOAuthClientStore` с явным описанием env-only поведения.
- [x] У `del db` добавлен короткий поясняющий комментарий.
- [x] Поведение класса не меняется.

### Где менять код
- `doge-identity-service/src/core/infrastructure/db_supabase.py`

### План выполнения
1. Добавить docstring над `SupabaseOAuthClientStore`.
2. Уточнить комментарий в `__init__` возле `del db`.
3. Не менять фабрики, сигнатуры и runtime-ветки.

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "from core.infrastructure.db_supabase import SupabaseOAuthClientStore; print(bool(SupabaseOAuthClientStore.__doc__))"
```
