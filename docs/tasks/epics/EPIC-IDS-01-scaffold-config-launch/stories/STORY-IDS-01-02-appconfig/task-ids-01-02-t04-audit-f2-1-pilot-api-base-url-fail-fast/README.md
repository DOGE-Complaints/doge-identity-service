## Task workspace — `task-ids-01-02-t04-audit-f2-1-pilot-api-base-url-fail-fast`

- Story: [`../STORY-IDS-01-02-appconfig.md`](../STORY-IDS-01-02-appconfig.md)
- Audit source: [`../../../../audit-report-2026-05-28.md`](../../../../audit-report-2026-05-28.md) (F2-1)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** ready  
**Wave:** `override epic_ids_01_audit_2026_05_28`  
---

## Task: fix — добавить `API_BASE_URL` в pilot-required матрицу

### Цель
Явно включить `API_BASE_URL` в `pilot_required` блок (`load_config_from_env`) для последовательного fail-fast поведения в pilot.

### Факты из кода
1. Аудит F2-1: `API_BASE_URL` проверяется через `_required(...)` позже, но отсутствует в пилотной матрице.
2. Story 2 требует единый fail-fast набор обязательных полей для `APP_PROFILE=pilot`.

### AC/DoD
- [ ] (P0) `API_BASE_URL` включён в pilot-required список.
- [ ] (P0) Добавлен тест на pilot-конфиг без `API_BASE_URL` с ожидаемым `ConfigError`.

### Где менять код
- `doge-identity-service/src/core/config/schema.py`
- `doge-identity-service/tests/test_config_schema.py`
