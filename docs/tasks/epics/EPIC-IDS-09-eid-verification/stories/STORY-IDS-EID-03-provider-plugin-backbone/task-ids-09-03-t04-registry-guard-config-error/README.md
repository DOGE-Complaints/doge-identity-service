## Task workspace — `task-ids-09-03-t04-registry-guard-config-error`

- Story: [`../STORY-IDS-EID-03-provider-plugin-backbone.md`](../STORY-IDS-EID-03-provider-plugin-backbone.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000016`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §F5 (EID-1 guard)  
---

## Task: fix — registry guard `ProviderNotRegisteredError` instead of `KeyError`

### Цель
`EIDProviderRegistry.get(name)` и `get_active(config)` бросают `ProviderNotRegisteredError` с текстом «доступны: …», не голый `KeyError`; глобальный `ConfigError` handler отдаёт envelope (audit EID-1).

### Почему это важно
Story AC #3: понятная ошибка при `EID_PROVIDER=<незарегистрированный>` (whitelist config, но не в lazy-реестре — e.g. `eideasy` до EID-02).

### Факты из кода
1. [`registry.py:11-14`](../../../../../../../src/core/providers/registry.py) — `raise KeyError(name)`.
2. [`test_eid_provider_registry.py:29-33`](../../../../../../../tests/test_eid_provider_registry.py) — ожидает `KeyError` (обновить в t05).
3. [`test_eid_providers.py:69-73`](../../../../../../../tests/test_eid_providers.py) — `get_active` → `KeyError`.
4. [`asgi_app.py:141-145`](../../../../../../../src/core/api/asgi_app.py) — `@app.exception_handler(ConfigError)`.
5. [`schema.py:96-98`](../../../../../../../src/core/config/schema.py) — `unknown` отсекается at config load; runtime guard для `eideasy`/`authentigate` not in registry.

### Gap / Проблема
Голый `KeyError` при неизвестном провайдере в реестре (audit F5 / backlog EID-1).

### AC/DoD
- [x] (P0) `registry.get(unknown)` → `ProviderNotRegisteredError` с перечислением зарегистрированных имён.
- [x] (P0) `get_active(config)` при незарегистрированном `config.eid_provider` → тот же guard.
- [x] (P0) Сообщение содержит «доступны» (или эквивалент из backlog) и список provider names.
- [x] (P1) `ProviderNotRegisteredError` наследует `ConfigError` — handler [`asgi_app.py:141-145`](../../../../../../../src/core/api/asgi_app.py) применим на startup/import paths где registry built.

### Где менять код
- `doge-identity-service/src/core/providers/registry.py`

### Out of scope
- Изменение whitelist `EID_PROVIDER` в schema — out of story
- HTTP-level e2e test guard response — t05
- jti replay-cache — defer

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "
from core.config.schema import ConfigError
from core.infrastructure.repositories import InMemoryVerificationSessionStore
from core.providers.mock.mock_provider import MockEIDProvider
from core.providers.registry import EIDProviderRegistry
r = EIDProviderRegistry({'mock': MockEIDProvider(InMemoryVerificationSessionStore())})
try:
    r.get('eideasy')
except ConfigError as e:
    print('ok', str(e)[:80])
"
```
