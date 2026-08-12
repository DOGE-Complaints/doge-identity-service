## Task workspace — `task-ids-09-07-t04-oidc-toolkit-provider-runtime-wire`

- Story: [`../STORY-IDS-EID-07-oidc-toolkit.md`](../STORY-IDS-EID-07-oidc-toolkit.md)
- Prerequisite: t01–t03 ([`../task-ids-09-07-t01-oidc-discovery-client/README.md`](../task-ids-09-07-t01-oidc-discovery-client/README.md), t02, t03)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000020`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/STORY-IDS-EID-07-oidc-toolkit.md`](../../../../../../backlog-stories/STORY-IDS-EID-07-oidc-toolkit.md) Scope #4; [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F8)  
---

## Task: implement — `OidcToolkit` facade and `ProviderRuntime.oidc` wire

### Цель
Собрать `OidcToolkit` (discovery + JWKS + validator) и подключить к `ProviderRuntime.oidc` через `build_provider_runtime` — Story Scope #4, AC #4.

### Почему это важно
EID-03 зарезервировал слот `oidc` в runtime; провайдеры (EID-02) должны получать toolkit через DI, не создавать OIDC клиентов ad-hoc.

### Факты из кода
1. [`runtime.py:15-21`](../../../../../../../src/core/providers/runtime.py) — `oidc: Any | None = None` slot exists.
2. [`runtime_factory.py:23-29`](../../../../../../../src/core/providers/runtime_factory.py) — today `oidc=None` always; `http_client` only when `eid_provider != "mock"`.
3. EID-03 AC: mock/in-memory — no provider network clients ([`STORY-IDS-EID-03-provider-plugin-backbone.md`](../../STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md)).
4. t01–t03 components in `core/security/oidc/`.

### Gap / Проблема
`ProviderRuntime.oidc` never populated; toolkit not exposed to provider builds.

### AC/DoD
- [x] (P0) `OidcToolkit` dataclass/facade exposes `discovery`, `jwks_cache`, `id_token_validator` (or equivalent unified API).
- [x] (P0) `build_provider_runtime` sets `runtime.oidc=OidcToolkit(...)` when `http_client` is not `None`.
- [x] (P0) When `eid_provider == "mock"` / no `http_client`: `oidc=None` (preserve EID-03 no-network guard).
- [x] (P1) Typed export from `core.security.oidc` and optional re-export from `core.providers` if needed by descriptors.
- [x] (P1) Story AC #4 traceability.

### Где менять код
- `doge-identity-service/src/core/security/oidc/toolkit.py` (new)
- `doge-identity-service/src/core/security/oidc/__init__.py`
- `doge-identity-service/src/core/providers/runtime.py` (typed `oidc` slot if replacing `Any`)
- `doge-identity-service/src/core/providers/runtime_factory.py`

### Out of scope
- Authentigate provider using toolkit — EID-02
- Offline mocked tests — t05
- Story acceptance gate — t06
- PKCE secret box — EID-08

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "
from core.providers.runtime_factory import build_provider_runtime
from core.config.schema import load_config_from_env
# smoke: mock provider => oidc is None
"
.venv/bin/python -m pytest tests/ -m "not live_integration" -q --co -q 2>/dev/null | head -1 || true
```
