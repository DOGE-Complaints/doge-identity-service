## Task workspace — `task-ids-09-04-t08-audit-f2-eid-provider-membership-from-descriptors`

- Story: [`../STORY-IDS-EID-04-provider-owned-config.md`](../STORY-IDS-EID-04-provider-owned-config.md)
- Audit source: [`../../../../../../analysis/epic-ids-09-eid-04-audit-2026-06-08.md`](../../../../../../analysis/epic-ids-09-eid-04-audit-2026-06-08.md) (F2)

---
**Приоритет:** P1  
**Сложность:** M  
**Статус:** done  
**Wave:** `override epic_ids_09_eid_04_audit_2026_06_08`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-09-eid-04-audit-2026-06-08.md`](../../../../../../analysis/epic-ids-09-eid-04-audit-2026-06-08.md) §F2  
---

## Task: fix — derive EID_PROVIDER membership from descriptor catalog (F2)

### Цель
Убрать дублирование списка допустимых провайдеров: membership check в `load_config_from_env` должен брать имена из каталога дескрипторов, а не из хардкод-литерала в `schema.py` (закрывает AC3 partial из audit).

### Почему это важно
Story AC #3: «добавление нового провайдера не требует правок провайдер-логики в `schema.py`». Сейчас +дескриптор недостаточно — нужно ещё дописать имя в литерал [`schema.py:106-107`](../../../../../../../src/core/config/schema.py).

### Факты из кода
1. Hardcoded membership: [`schema.py:106-107`](../../../../../../../src/core/config/schema.py) — `{"mock", "eideasy", "authentigate"}`.
2. Descriptor catalog: [`registry_builder.py:10-16`](../../../../../../../src/core/providers/registry_builder.py) — `ALL_EID_PROVIDER_DESCRIPTORS`, `_DESCRIPTOR_BY_NAME`.
3. Existing helper: [`registry_builder.py:19-20`](../../../../../../../src/core/providers/registry_builder.py) — `get_provider_descriptor(name)`.
4. Weak test: [`test_provider_owned_config.py:63-70`](../../../../../../../tests/test_provider_owned_config.py) — `test_schema_has_no_provider_specific_ifs` ловит только `==`-ифы, не `in {...}`.
5. Unknown provider test exists: [`test_config_schema.py:63-72`](../../../../../../../tests/test_config_schema.py) — `test_unknown_eid_provider_rejected`.

### Gap / Проблема
Два SSOT для списка провайдеров (литерал в schema vs каталог дескрипторов); acceptance-тест даёт ложное чувство полноты AC3.

### AC/DoD
- [x] (P0) Экспорт `registered_eid_provider_names()` (или аналог) из `registry_builder.py` — frozenset имён из `ALL_EID_PROVIDER_DESCRIPTORS`.
- [x] (P0) `load_config_from_env`: membership check через каталог; **нет** хардкод-литерала `{"mock", "eideasy", "authentigate"}` в `schema.py`.
- [x] (P0) `EID_PROVIDER=unknown` → `ConfigError` с понятным текстом (регрессия `test_unknown_eid_provider_rejected`).
- [x] (P1) Тест: membership не дублируется в source `load_config_from_env` (расширить/заменить `test_schema_has_no_provider_specific_ifs`).
- [x] (P1) Offline suite green: `pytest -m "not live_integration" -q`.

### Где менять код
- `doge-identity-service/src/core/providers/registry_builder.py`
- `doge-identity-service/src/core/config/schema.py`
- `doge-identity-service/tests/test_provider_owned_config.py` (и/или `tests/test_config_schema.py`)

### Out of scope
- Backlog sync (t07).
- Новые провайдеры / runtime provider build (EID-02).
- Flat `AppConfig` fields (owner decision: keep).
- Изменение `ALL_EID_PROVIDER_DESCRIPTORS` состава.

### Проверка
```bash
cd doge-identity-service
grep -n '"mock", "eideasy", "authentigate"' src/core/config/schema.py || echo "no hardcoded literal"
.venv/bin/python -m pytest tests/test_provider_owned_config.py tests/test_config_schema.py -m "not live_integration" -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
