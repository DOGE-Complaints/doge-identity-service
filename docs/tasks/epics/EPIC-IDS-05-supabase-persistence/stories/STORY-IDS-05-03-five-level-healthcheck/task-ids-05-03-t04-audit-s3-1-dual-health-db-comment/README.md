## Task workspace — `task-ids-05-03-t04-audit-s3-1-dual-health-db-comment`

- Story: [`../STORY-IDS-05-03-five-level-healthcheck.md`](../STORY-IDS-05-03-five-level-healthcheck.md)
- Re-audit source: [`../../../../re-audit-report-2026-06-02.md`](../../../../re-audit-report-2026-06-02.md) (S3-1)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_05_reaudit_2026_06_02`  
**Decision Ref:** [`../../../../re-audit-report-2026-06-02.md`](../../../../re-audit-report-2026-06-02.md) §S3-1  
---

## Task: docs — explain dual `SupabaseDatabase` startup instances (S3-1)

### Цель
Добавить явный комментарий в `build_api_dependencies`, что `health_db` и `supabase_db` создаются отдельно и зачем это сделано на текущем этапе.

### Факты из кода
1. [`src/core/api/dependencies.py:70-73`](../../../../../../../src/core/api/dependencies.py) — создаётся `health_db` для startup `db_checks`.
2. [`src/core/infrastructure/providers.py:74-78`](../../../../../../../src/core/infrastructure/providers.py) — отдельно создаётся `supabase_db` для runtime-репозиториев.
3. [`src/core/infrastructure/db_supabase.py:651-658`](../../../../../../../src/core/infrastructure/db_supabase.py) — `SupabaseHealthRepository` работает через `supabase_db`.
4. [`../../../../re-audit-report-2026-06-02.md`](../../../../re-audit-report-2026-06-02.md) — S3-1 помечен открытым как documentation gap.

### Gap / Проблема
В коде нет пояснения, почему используются два экземпляра DB-клиента, что повышает риск неверных предположений при доработках.

### Out of scope
- Рефактор единого `SupabaseDatabase` из фабрики (EPIC-IDS-06 / полный рефактор S3-1+S3-2).
- Изменение `providers.py` wiring.

### AC/DoD
- [x] Над созданием `health_db` добавлен комментарий о dual-instance.
- [x] Комментарий указывает, что унификация инстанса — отдельный рефактор (вне этого таска).
- [x] Runtime-поведение не меняется (docs-only для S3-1; S3-2 добавляет timeout без смены wiring).

### Где менять код
- `doge-identity-service/src/core/api/dependencies.py`

### План выполнения
1. Добавить короткий архитектурный комментарий в `dependencies.py`.
2. Не менять wiring в `providers.py`.
3. Ограничиться docs-only изменением.

### Проверка
```bash
rg "health_db|supabase_db" doge-identity-service/src/core/api/dependencies.py doge-identity-service/src/core/infrastructure/providers.py
```
