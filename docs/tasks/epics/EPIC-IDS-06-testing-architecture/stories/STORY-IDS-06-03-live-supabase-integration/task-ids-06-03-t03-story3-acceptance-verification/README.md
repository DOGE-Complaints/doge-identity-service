## Task workspace — `task-ids-06-03-t03-story3-acceptance-verification`

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000008`  
**Decision Ref:** [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 3  
**Story:** [`../STORY-IDS-06-03-live-supabase-integration.md`](../STORY-IDS-06-03-live-supabase-integration.md)  
---

## Task: tests — Story 3 acceptance verification

### Цель
Верифицировать verbatim AC Story 3 (epic L219–223) после t01–t02.

### Почему это важно
Гарантирует skip-without-creds и отсутствие test-data leak в Supabase.

### Факты из кода
1. Story 3 AC — [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) L219–223.
2. [`task-ids-05-05-t02-ci-test-secrets-layout`](../../../../EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-05-supabase-project-setup-live-credentials/task-ids-05-05-t02-ci-test-secrets-layout/README.md) — `SUPABASE_TEST_*` naming (IDS-05).

### Gap
Нет формальной проверки AC L219–223.

### AC/DoD
- [x] (P0) Без `.env` с Supabase creds — все `live_integration` тесты SKIPPED (не FAILED).
- [x] (P0) С правильными creds (тестового, **не** production проекта) — все тесты PASSED.
- [x] (P0) После тестов в Supabase **не остаётся** новых profiles/sessions/events с `test-*` префиксами (cleanup работает).
- [x] (P0) Тесты используют **тестовый** Supabase проект (`SUPABASE_TEST_URL`, не production URL).

### Где менять код
- N/A (verification)

### Out of scope
- CI live workflow — Story 4

### Проверка
```bash
cd doge-identity-service
unset SUPABASE_URL SUPABASE_SERVICE_ROLE
.venv/bin/python -m pytest -m live_integration -q
# с test .env — all passed, no test-* rows left
```
