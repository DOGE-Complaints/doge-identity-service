## Task workspace — `task-ids-04-06-t04-audit-rg-1-epic-hook-test-cleanup`

- Story: [`../STORY-IDS-04-06-provide-factory-di-integration.md`](../STORY-IDS-04-06-provide-factory-di-integration.md)
- Audit source: [`../../../../epic-ids-04-audit-2026-05-30.md`](../../../../epic-ids-04-audit-2026-05-30.md) (RG-1)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** ready  
**Wave:** `override epic_ids_04_audit_2026_05_30`  
---

## Task: tests — verify-and-close epic hook test regression (RG-1)

### Цель
Закрыть gap RG-1: тест больше не ищет удалённый `# TODO EPIC-IDS-04: replace with provide_service_factory(...)`; подтвердить актуальные проверки интеграции factory в `dependencies.py`.

### Почему это важно (риск)
Audit помечает test suite как FAIL из-за устаревшего assert; после Story 06 код уже интегрирован — gap закрывается верификацией, не откатом реализации.

### Факты из кода
1. [`epic-ids-04-audit-2026-05-30.md`](../../../../epic-ids-04-audit-2026-05-30.md) RG-1 §Story 6 (L247–268).
2. [`tests/test_api_dependencies.py:152-160`](../../../../../../../tests/test_api_dependencies.py): `test_build_api_dependencies_uses_provide_service_factory` — assert на TODO **отсутствует**; проверяются `provide_service_factory` import/call и EPIC-IDS-05 hook.
3. [`src/core/api/dependencies.py:63-88`](../../../../../../../src/core/api/dependencies.py): `service_factory = provide_service_factory(config)` — реальная интеграция без TODO EPIC-IDS-04.

### Gap / Проблема
Audit ссылается на удалённый тест `test_build_api_dependencies_has_epic_hook_comments` с assert TODO; текущий код уже исправлен при Story 06 P3 — task = verify-and-close.

### AC/DoD
- [ ] (P0) В `tests/test_api_dependencies.py` **нет** assert `"# TODO EPIC-IDS-04: replace with provide_service_factory(...)" in text`.
- [ ] (P0) Сохранены проверки: `provide_service_factory` import, `service_factory = provide_service_factory(config)`, `# TODO EPIC-IDS-05: run 5-level Supabase healthchecks`.
- [ ] (P0) `pytest tests/test_api_dependencies.py -q -k provide_service_factory` проходит.

### Где менять код
- `doge-identity-service/tests/test_api_dependencies.py` — только если assert TODO всё ещё присутствует (ожидается: уже исправлено)

### Out of scope
- Откат `build_api_dependencies()` на stub
- Изменения `src/core/api/dependencies.py` runtime

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_api_dependencies.py -q -k provide_service_factory
```
