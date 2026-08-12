## Task workspace — `task-ids-03-03-t04-audit-di-4-optional-fields-test-cleanup`

- Story: [`../STORY-IDS-03-03-epic-ids-04-extension-hook-contract.md`](../STORY-IDS-03-03-epic-ids-04-extension-hook-contract.md)
- Audit source: [`../../../../../../analysis/epic-ids-03-audit-2026-05-28.md`](../../../../../../analysis/epic-ids-03-audit-2026-05-28.md) (DI-4)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_03_audit_2026_05_28`  
---

## Task: tests — убрать тавтологичный assert в alignment test

### Цель
Закрыть gap DI-4: удалить полу-тавтологичное сравнение `getter_names == {hardcoded set}`; сохранить проверку, что все имена из `EPIC_IDS_04_OPTIONAL_FIELDS` — реальные поля `ApiDependencies`.

### Почему это важно (риск)
Hardcoded set дублирует вычисление из константы — тест не ловит рассинхрон, только создаёт шум при рефакторинге.

### Факты из кода
1. [`epic-ids-03-audit-2026-05-28.md`](../../../../../../analysis/epic-ids-03-audit-2026-05-28.md) DI-4 §Story 3.
2. [`tests/test_api_dependencies.py:144–159`](../../../../../../../tests/test_api_dependencies.py): loop L147–148 — ценная проверка; L149–159 — tautology.
3. [`src/core/api/dependencies.py:13–22`](../../../../../../../src/core/api/dependencies.py): `EPIC_IDS_04_OPTIONAL_FIELDS` — 8 имён.

### Gap / Проблема
`getter_names` из константы сравнивается с hardcoded set тех же 8 `get_*` имён — минимальная защита от ошибок.

### AC/DoD
- [x] (P0) Удалён `assert getter_names == {hardcoded ...}` (L149–159).
- [x] (P0) Сохранены: `len(EPIC_IDS_04_OPTIONAL_FIELDS) == 8` и loop `field_name in ApiDependencies.__dataclass_fields__`.
- [x] (P1) `pytest tests/test_api_dependencies.py -q -k optional_fields` проходит.

### Acceptance
- [acceptance-verification-task-ids-03-03-t04-audit-di-4-optional-fields-test-cleanup.md](./acceptance-verification-task-ids-03-03-t04-audit-di-4-optional-fields-test-cleanup.md) — PASS

### Где менять код
- `doge-identity-service/tests/test_api_dependencies.py` — `test_epic_ids_04_optional_fields_match_factory_getters`

### Out of scope
- Изменения `EPIC_IDS_04_OPTIONAL_FIELDS`, dataclass fields, commented factory block

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_api_dependencies.py -q -k optional_fields
```
