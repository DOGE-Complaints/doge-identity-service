## Task workspace — `task-ids-05-03-t05-audit-s3-2-health-db-request-timeout`

- Story: [`../STORY-IDS-05-03-five-level-healthcheck.md`](../STORY-IDS-05-03-five-level-healthcheck.md)
- Re-audit source: [`../../../../re-audit-report-2026-06-02.md`](../../../../re-audit-report-2026-06-02.md) (S3-2)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_05_reaudit_2026_06_02`  
**Decision Ref:** [`../../../../re-audit-report-2026-06-02.md`](../../../../re-audit-report-2026-06-02.md) §S3-2  
---

## Task: fix — align `health_db` timeout with `request_timeout_s` (S3-2)

### Цель
Передать timeout из конфига в `health_db`, чтобы startup-check и runtime-репозитории использовали согласованный `request_timeout_s`.

### Факты из кода
1. [`src/core/api/dependencies.py:70-73`](../../../../../../../src/core/api/dependencies.py) — `health_db` создаётся без явного `timeout_s`.
2. [`src/core/infrastructure/providers.py:74-78`](../../../../../../../src/core/infrastructure/providers.py) — в runtime уже используется `timeout_s=float(resolved_config.request_timeout_s or 15)`.
3. [`../../../../re-audit-report-2026-06-02.md`](../../../../re-audit-report-2026-06-02.md) — S3-2 отмечен открытым.

### Gap / Проблема
Timeout для startup health-check и runtime-пути расходится при нестандартном `REQUEST_TIMEOUT_S`.

### Out of scope
- Объединение `health_db` и `supabase_db` в один инстанс (закрывает S3-1+S3-2 вместе; отдельный рефактор).
- Изменение default timeout в `db_supabase.py:241`.

### AC/DoD
- [x] `health_db` инициализируется с `timeout_s=float(config.request_timeout_s or 15)`.
- [x] Набор `db_checks` ключей не меняется.
- [x] Изменение ограничено `dependencies.py`.

### Где менять код
- `doge-identity-service/src/core/api/dependencies.py`

### План выполнения
1. Добавить аргумент `timeout_s` в вызов `SupabaseDatabase.from_http` для `health_db`.
2. Сохранить текущую структуру `db_checks`.
3. Не объединять `health_db` и `supabase_db` в рамках этого таска.

### Проверка
```bash
rg "health_db = SupabaseDatabase.from_http|request_timeout_s" doge-identity-service/src/core/api/dependencies.py doge-identity-service/src/core/infrastructure/providers.py
```
