## Task workspace — `task-ids-08-01-t06-story-related-tests-cleanup`

- Story: [`../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md) AC #3

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000011`  
**Skill declared:** python-pro  
---

## Task: tests — story-related tests cleanup

### Цель
Удалить или переписать тесты, завязанные на `StoryDraft` / `story_drafts` / story-роуты, чтобы offline-набор оставался зелёным после t01–t05.

### Почему это важно
Story AC #3: тесты на story должны исчезнуть или быть адаптированы; иначе CI падает после удаления домена.

### Факты из кода
Файлы с упоминаниями `story_drafts` / `StoryDraft` в `tests/`:
1. [`test_db_supabase_healthcheck.py`](../../../../../../../tests/test_db_supabase_healthcheck.py)
2. [`test_inmemory_repositories.py`](../../../../../../../tests/test_inmemory_repositories.py)
3. [`test_db_supabase_repositories.py`](../../../../../../../tests/test_db_supabase_repositories.py)
4. [`test_di_service_factory.py`](../../../../../../../tests/test_di_service_factory.py)
5. [`test_service_factory.py`](../../../../../../../tests/test_service_factory.py)
6. [`test_domain_contracts.py`](../../../../../../../tests/test_domain_contracts.py)
7. [`test_epic_ids_04_integration.py`](../../../../../../../tests/test_epic_ids_04_integration.py)
8. [`test_epic_ids_05_integration.py`](../../../../../../../tests/test_epic_ids_05_integration.py)
9. [`test_supabase_runbook_docs.py`](../../../../../../../tests/test_supabase_runbook_docs.py)
10. [`test_supabase_migrations_sql.py`](../../../../../../../tests/test_supabase_migrations_sql.py)
11. [`tests/integration/supabase/test_supabase_dotenv_connectivity.py`](../../../../../../../tests/integration/supabase/test_supabase_dotenv_connectivity.py)

Smoke/route тесты могут ожидать story endpoints 501 — обновить после t02.

### Gap / Проблема
~11 test-файлов содержат story-специфичные assertions/fixtures.

### AC/DoD
- [x] (P0) Story-related test cases удалены или переписаны без `StoryDraft` / story routes.
- [x] (P0) Story AC #3: `pytest -m "not live_integration" -q` — все passed.
- [x] (P1) Grep `StoryDraft|story_drafts` в `tests/` = 0 (migration doc tests exempt если ссылаются только на файл миграции).

### Где менять код
- `tests/` — перечисленные файлы и любые новые failures после t01–t05

### Out of scope
- Live integration tests (`live_integration` marker)
- Финальный acceptance report — t07

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
rg "StoryDraft|story_drafts" tests --glob '!*migrations*'
```
