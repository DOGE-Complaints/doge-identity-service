## Task workspace — `task-ids-01-02-t06-audit-f2-3-pilot-oauth-secret-isolated-test`

- Story: [`../STORY-IDS-01-02-appconfig.md`](../STORY-IDS-01-02-appconfig.md)
- Audit source: [`../../../../audit-report-2026-05-28.md`](../../../../audit-report-2026-05-28.md) (F2-3)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** ready  
**Wave:** `override epic_ids_01_audit_2026_05_28`  
---

## Task: tests — изолировать fail-fast по `OAUTH_ACCESS_TOKEN_SECRET`

### Цель
Добавить тест, где все pilot-required поля заданы, кроме `OAUTH_ACCESS_TOKEN_SECRET`, чтобы валидировать именно эту ветку ошибки.

### Факты из кода
1. Аудит F2-3: текущий тест падает раньше на `SUPABASE_URL`, не доходя до `OAUTH_ACCESS_TOKEN_SECRET`.
2. Story 2 AC явно требует ошибку именно для отсутствующего `OAUTH_ACCESS_TOKEN_SECRET`.

### AC/DoD
- [ ] (P0) Добавлен pytest-кейс, который приводит к `ConfigError` по `OAUTH_ACCESS_TOKEN_SECRET`.
- [ ] (P0) Сообщение ошибки содержит имя поля `OAUTH_ACCESS_TOKEN_SECRET`.

### Где менять код
- `doge-identity-service/tests/test_config_schema.py`
