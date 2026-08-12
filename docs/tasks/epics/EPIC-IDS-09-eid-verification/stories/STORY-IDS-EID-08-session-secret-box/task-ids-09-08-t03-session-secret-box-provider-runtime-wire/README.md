## Task workspace — `task-ids-09-08-t03-session-secret-box-provider-runtime-wire`

- Story: [`../STORY-IDS-EID-08-session-secret-box.md`](../STORY-IDS-EID-08-session-secret-box.md)
- Prerequisite: t01–t02 ([`../task-ids-09-08-t01-session-secret-box-fernet-port/README.md`](../task-ids-09-08-t01-session-secret-box-fernet-port/README.md), [`../task-ids-09-08-t02-eid-session-enc-key-config-pilot-failfast/README.md`](../task-ids-09-08-t02-eid-session-enc-key-config-pilot-failfast/README.md))

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000021`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/STORY-IDS-EID-08-session-secret-box.md`](../../../../../../backlog-stories/STORY-IDS-EID-08-session-secret-box.md) Scope #3 (primite + slot); [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F7)  
---

## Task: implement — wire `SessionSecretBox` into `ProviderRuntime.secret_box`

### Цель
Собрать `SessionSecretBox` из config и подключить к `ProviderRuntime.secret_box` через `build_provider_runtime` — Story Scope (primite + slot), AC #3.

### Почему это важно
EID-03 зарезервировал слот `secret_box`; провайдеры (EID-02) должны получать box через DI, не создавать Fernet ad-hoc.

### Факты из кода
1. [`runtime.py:15-22`](../../../../../../../src/core/providers/runtime.py) — `secret_box: Any | None = None` slot exists.
2. [`runtime_factory.py:26-33`](../../../../../../../src/core/providers/runtime_factory.py) — today `secret_box=None` always; `oidc` wired when non-mock.
3. EID-07 pattern: [`runtime_factory.py:22-24`](../../../../../../../src/core/providers/runtime_factory.py) — `build_oidc_toolkit(http_client)` in factory path.
4. t01/t02 deliver `SessionSecretBox` + `config.eid_session_enc_key`.

### Gap / Проблема
`ProviderRuntime.secret_box` never populated; providers cannot seal/open session secrets.

### AC/DoD
- [x] (P0) `build_session_secret_box(config: AppConfig) -> SessionSecretBox` (or inline in factory) uses `eid_session_enc_key`, not `eid_secret`.
- [x] (P0) `build_provider_runtime` sets `runtime.secret_box` to non-None instance (Story AC #3).
- [x] (P1) Typed slot: replace `secret_box: Any | None` with `SessionSecretBox | None` in [`runtime.py`](../../../../../../../src/core/providers/runtime.py).
- [x] (P1) Re-export from `core.security.session_secret` if needed by descriptors.
- [x] (P1) Story AC #3 traceability.

### Где менять код
- `doge-identity-service/src/core/providers/runtime.py`
- `doge-identity-service/src/core/providers/runtime_factory.py`
- `doge-identity-service/src/core/security/session_secret.py` (factory helper if placed here)

### Out of scope
- Provider PKCE `start_flow`/`callback` — EID-02
- Offline tests — t04
- Story acceptance — t05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "
from core.providers.runtime_factory import build_provider_runtime
from core.config.providers import provide_app_config
from core.infrastructure.repositories import InMemoryVerificationSessionStore
cfg = provide_app_config()
rt = build_provider_runtime(config=cfg, session_store=InMemoryVerificationSessionStore())
print(rt.secret_box is not None)
"
```
