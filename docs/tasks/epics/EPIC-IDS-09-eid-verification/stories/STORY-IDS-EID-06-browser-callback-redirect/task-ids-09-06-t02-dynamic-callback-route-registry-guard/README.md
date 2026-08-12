## Task workspace — `task-ids-09-06-t02-dynamic-callback-route-registry-guard`

- Story: [`../STORY-IDS-EID-06-browser-callback-redirect.md`](../STORY-IDS-EID-06-browser-callback-redirect.md)
- Prerequisite: t01 (`EidCallbackOutcome`)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000019`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md`](../../../../../../backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md) Scope #5; [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F6)  
---

## Task: implement — dynamic `GET /auth/{provider}/callback` with registry guard

### Цель
Заменить три захардкоженных callback-роута одним параметризованным `GET /auth/{provider}/callback`; резолвить `provider` из пути, проверять регистрацию в реестре, делегировать в оркестратор — story Scope #5 и AC #4.

### Почему это важно
Добавление провайдера (EID-02) не должно требовать нового роута в `asgi_app`. Audit F6 — хардкод блокирует plugin-модель EID-03.

### Факты из кода
1. [`asgi_app.py:214-236`](../../../../../../../src/core/api/asgi_app.py) — eideasy/authentigate stub callbacks через `handle_public_stub`.
2. [`asgi_app.py:238-248`](../../../../../../../src/core/api/asgi_app.py) — mock callback с `provider_name="mock"` hardcoded.
3. [`mock_provider.py:21-22`](../../../../../../../src/core/providers/mock/mock_provider.py) — `callback_path == "/auth/mock/callback"` (совместим с `/auth/{provider}/callback` при `provider=mock`).
4. [`registry.py:16-22`](../../../../../../../src/core/providers/registry.py) — `get(name)` → `ProviderNotRegisteredError` (`ConfigError` subclass).
5. [`asgi_app.py:141-145`](../../../../../../../src/core/api/asgi_app.py) — global `ConfigError` handler → JSON 500.

### Gap / Проблема
Три отдельных роута; eideasy/authentigate — заглушки, не registry-driven callback.

### AC/DoD
- [x] (P0) Один роут `GET /auth/{provider}/callback`; старые три роута удалены.
- [x] (P0) `provider` из path передаётся в `handle_auth_eid_callback` как `provider_name`.
- [x] (P0) Незарегистрированный `provider` → `ProviderNotRegisteredError` / `ConfigError` (per EID-03 guard).
- [x] (P1) Mock path `/auth/mock/callback?...` продолжает резолвиться (динамический `{provider}=mock`).
- [x] (P1) Story AC #4 traceability.

### Где менять код
- `doge-identity-service/src/core/api/asgi_app.py`

### Out of scope
- Redirect render / Accept negotiate — t03
- E2E redirect tests — t04
- Регистрация eideasy/authentigate в реестре — EID-02

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_eid_verification_flow.py tests/test_asgi_transport.py -m "not live_integration" -q -k callback
.venv/bin/python -c "
from core.api.asgi_app import create_app
from core.config.schema import AppConfig
# smoke: app builds with dynamic route registered
app = create_app(AppConfig.from_env())
paths = [getattr(r, 'path', '') for r in app.routes]
assert any('{provider}' in p or 'provider' in str(p) for p in paths if p)
"
```
