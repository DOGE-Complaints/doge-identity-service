## Task workspace — `task-ids-05-01-t02-story1-acceptance-verification`

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000006`  
**Decision Ref:** [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 1  
**Story:** [`../STORY-IDS-05-01-supabase-database-http-client.md`](../STORY-IDS-05-01-supabase-database-http-client.md)  
---

## Task: tests — Story 1 acceptance verification

### Цель
Добавить pytest-покрытие verbatim AC Story 1 (epic L69–73): `from_http` validation, header parity, `_request` 5xx logging/error propagation.

### Почему это важно
HTTP-клиент — фундамент всех Supabase-операций; AC фиксируют контракт до реализации репозиториев.

### Факты из кода
1. Story 1 AC — [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) L69–73.
2. [`task-ids-05-01-t01-supabase-database-http-client`](../task-ids-05-01-t01-supabase-database-http-client/README.md) — реализует `SupabaseDatabase`.
3. `tests/test_db_supabase_client.py` — **отсутствует**.

### Gap
Нет unit-тестов для AC L69–73.

### AC/DoD
- [x] (P0) `SupabaseDatabase.from_http("", "key")` → `ValueError`.
- [x] (P0) `SupabaseDatabase.from_http("https://x.co/", "key").base_url == "https://x.co"` (без trailing slash).
- [x] (P0) `_headers()["apikey"] == _headers()["Authorization"].split()[-1]` (одинаковое значение).
- [x] (P0) `_request` при HTTP 5xx логирует через `logger.error` и пробрасывает `httpx.HTTPError`.

### Где менять код
- `doge-identity-service/tests/test_db_supabase_client.py` (новый)

### Out of scope
- Repository tests — Story 2
- Live Supabase connectivity — Story 5

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_db_supabase_client.py -v
```
