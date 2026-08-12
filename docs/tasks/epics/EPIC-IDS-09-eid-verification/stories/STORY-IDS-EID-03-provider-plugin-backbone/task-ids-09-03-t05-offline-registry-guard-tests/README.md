## Task workspace — `task-ids-09-03-t05-offline-registry-guard-tests`

- Story: [`../STORY-IDS-EID-03-provider-plugin-backbone.md`](../STORY-IDS-EID-03-provider-plugin-backbone.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000016`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §F5, §F13-guard  
---

## Task: test — offline registry build, guard, no network in mock mode

### Цель
Покрыть story AC #4–#5: registry build из дескрипторов, guard вместо `KeyError`, отсутствие httpx/network side effects в mock/in-memory; offline suite green.

### Почему это важно
Story AC #5: «Offline-набор зелёный; тест на guard и на сборку реестра». AC #4: no network clients in mock/in-memory.

### Факты из кода
1. [`test_eid_provider_registry.py`](../../../../../../../tests/test_eid_provider_registry.py) — KeyError expectations → migrate to `ProviderNotRegisteredError`.
2. [`test_eid_providers.py:69-73`](../../../../../../../tests/test_eid_providers.py) — `get_active` KeyError test.
3. [`test_eid_verification_flow.py`](../../../../../../../tests/test_eid_verification_flow.py) — EID-01 regression baseline.
4. [`providers.py`](../../../../../../../src/core/infrastructure/providers.py) — factory path under test.
5. [`conftest.py`](../../../../../../../tests/conftest.py) — offline marker `not live_integration`.

### Gap / Проблема
Нет dedicated tests для plugin backbone; старые тесты ожидают `KeyError`.

### AC/DoD
- [x] (P0) Тест: `build_registry` / factory path registers `mock` via descriptor.
- [x] (P0) Тест: unknown / unregistered provider → `ProviderNotRegisteredError` (not `KeyError`); message lists available names (AC #3).
- [x] (P0) Тест: mock + in_memory — `http_client` not instantiated (AC #4) — mock patch or runtime inspection.
- [x] (P1) Обновить [`test_eid_provider_registry.py`](../../../../../../../tests/test_eid_provider_registry.py), [`test_eid_providers.py`](../../../../../../../tests/test_eid_providers.py) для нового guard.
- [x] (P1) Новый `tests/test_provider_plugin_backbone.py` (или расширение existing) — registry + guard smoke.
- [x] (P1) `pytest -m "not live_integration"` green (story AC #5).

### Где менять код
- `doge-identity-service/tests/test_provider_plugin_backbone.py` (new)
- `doge-identity-service/tests/test_eid_provider_registry.py`
- `doge-identity-service/tests/test_eid_providers.py`

### Out of scope
- Live integration / Supabase network tests
- Authentigate provider e2e — EID-02
- jti replay-cache tests — defer

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_provider_plugin_backbone.py tests/test_eid_provider_registry.py tests/test_eid_providers.py tests/test_eid_verification_flow.py -m "not live_integration" -q
```
