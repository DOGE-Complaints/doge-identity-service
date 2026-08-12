## Task workspace — `task-ids-04-06-t05-audit-rg-2-zero-arg-assertion`

- Story: [`../STORY-IDS-04-06-provide-factory-di-integration.md`](../STORY-IDS-04-06-provide-factory-di-integration.md)
- Audit source: [`../../../../epic-ids-04-audit-2026-05-30.md`](../../../../epic-ids-04-audit-2026-05-30.md) (RG-2)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** ready  
**Wave:** `override epic_ids_04_audit_2026_05_30`  
---

## Task: tests — align zero-arg DI test with EPIC-IDS-04 factory wiring (RG-2)

### Цель
Закрыть gap RG-2: `test_build_api_dependencies_zero_arg` отражает EPIC-IDS-04 — identity-слоты заполнены InMemory-репозиториями, не `None`.

### Почему это важно (риск)
Устаревший `profile_repository is None` ломает test suite и маскирует успешную DI-интеграцию Story 6.

### Факты из кода
1. [`epic-ids-04-audit-2026-05-30.md`](../../../../epic-ids-04-audit-2026-05-30.md) RG-2 §Story 6 (L272–297).
2. [`tests/test_api_dependencies.py:82-88`](../../../../../../../tests/test_api_dependencies.py): уже `profile_repository is not None` и `SupabaseJwtBearerTokenAuth` — частично исправлено.
3. [`src/core/infrastructure/providers.py`](../../../../../../../src/core/infrastructure/providers.py): `provide_service_factory()` создаёт `InMemoryProfileRepository()` при `DB_BACKEND=in_memory`.
4. Audit рекомендует: `isinstance(deps.profile_repository, InMemoryProfileRepository)` — **ещё не добавлено**.

### Gap / Проблема
Assert `is None` заменён на `is not None`, но audit AC требует типовую проверку InMemory-реализации.

### AC/DoD
- [ ] (P0) `test_build_api_dependencies_zero_arg`: `isinstance(deps.profile_repository, InMemoryProfileRepository)` — True.
- [ ] (P0) `type(deps.bearer_token_auth).__name__ == "SupabaseJwtBearerTokenAuth"`.
- [ ] (P0) `pytest tests/test_api_dependencies.py -q -k zero_arg` проходит.

### Где менять код
- `doge-identity-service/tests/test_api_dependencies.py` — `test_build_api_dependencies_zero_arg`

### Out of scope
- Изменения `provide_service_factory()` body
- Новые runtime-поля в `ApiDependencies`

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_api_dependencies.py -q -k zero_arg
```
