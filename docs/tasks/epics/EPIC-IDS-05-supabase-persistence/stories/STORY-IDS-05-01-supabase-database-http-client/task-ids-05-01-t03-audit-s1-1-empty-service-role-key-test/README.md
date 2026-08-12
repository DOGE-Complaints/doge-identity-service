## Task workspace — `task-ids-05-01-t03-audit-s1-1-empty-service-role-key-test`

- Story: [`../STORY-IDS-05-01-supabase-database-http-client.md`](../STORY-IDS-05-01-supabase-database-http-client.md)
- Re-audit source: [`../../../../re-audit-report-2026-06-02.md`](../../../../re-audit-report-2026-06-02.md) (S1-1)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_05_reaudit_2026_06_02`  
**Decision Ref:** [`../../../../re-audit-report-2026-06-02.md`](../../../../re-audit-report-2026-06-02.md) §S1-1  
---

## Task: tests — `from_http` rejects empty service_role_key (S1-1)

### Цель
Добавить тест, что `SupabaseDatabase.from_http(url, "")` поднимает `ValueError` с сообщением `service_role_key is required`.

### Факты из кода
1. [`src/core/infrastructure/db_supabase.py:252-253`](../../../../../../../src/core/infrastructure/db_supabase.py) — есть fail-fast валидация пустого `service_role_key`.
2. [`tests/test_db_supabase_client.py`](../../../../../../../tests/test_db_supabase_client.py) — есть тест пустого URL, но нет теста пустого service role key.
3. [`../../../../re-audit-report-2026-06-02.md`](../../../../re-audit-report-2026-06-02.md) — finding S1-1 отмечен как открытый.

### Gap / Проблема
Ветка валидации реализована, но не зафиксирована отдельным unit-тестом.

### Out of scope
- Изменение `SupabaseDatabase.from_http` (логика уже корректна).
- Объединение dual-instance `health_db` / `supabase_db` (S3-1, EPIC-IDS-06).

### AC/DoD
- [x] Добавлен тест `test_from_http_empty_service_role_key_raises_value_error`.
- [x] Тест проверяет `ValueError` и сообщение `service_role_key is required`.

### Где менять код
- `doge-identity-service/tests/test_db_supabase_client.py`

### План выполнения
1. Добавить новый unit-тест рядом с `test_from_http_empty_url_raises_value_error`.
2. Не менять runtime-код `SupabaseDatabase.from_http`.
3. Зафиксировать изменение только в тестах и task-артефактах.

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_db_supabase_client.py -v -k empty_service_role
```
