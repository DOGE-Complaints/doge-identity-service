## Task workspace — `task-ids-09-03-t02-provider-runtime-factory`

- Story: [`../STORY-IDS-EID-03-provider-plugin-backbone.md`](../STORY-IDS-EID-03-provider-plugin-backbone.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000016`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §F9  
---

## Task: implement — `ProviderRuntime` factory (single DI bundle)

### Цель
Собрать `ProviderRuntime` **один раз** в пути `provide_service_factory`: `config`, `session_store`, lazy `http_client` с `oidc_request_timeout_s`; слоты `secret_box`/`oidc`/`clock` = `None` (заглушки под EID-07/EID-08).

### Почему это важно
Story Scope: `ProviderRuntime` DI-bundle; AC #4 — в mock/in-memory не создавать сетевые клиенты провайдеров.

### Факты из кода
1. [`providers.py:52-105`](../../../../../../../src/core/infrastructure/providers.py) — `provide_service_factory` собирает repos + registry.
2. [`schema.py:136`](../../../../../../../src/core/config/schema.py) — `oidc_request_timeout_s` для httpx timeout.
3. [`schema.py:96-98`](../../../../../../../src/core/config/schema.py) — `eid_provider` whitelist.
4. [`dependencies.py:86-97`](../../../../../../../src/core/api/dependencies.py) — consumer `eid_provider_registry`.
5. [`service_factory.py:19-30`](../../../../../../../src/core/infrastructure/service_factory.py) — `DefaultServiceFactory` holds registry.

### Gap / Проблема
Фабрика инжектит провайдеру только `VerificationSessionStore` (audit F9); нет единого runtime bundle.

### AC/DoD
- [x] (P0) `build_provider_runtime(...)` (или inline в factory) создаёт `ProviderRuntime` один раз per `provide_service_factory` call.
- [x] (P0) `session_store` из уже собранного repo path (in_memory / supabase).
- [x] (P0) При `eid_provider=mock` и/или `db_backend=in_memory` — `http_client` **не** создаётся (AC #4 partial).
- [x] (P1) Слоты `secret_box`, `oidc`, `clock` присутствуют как optional `None` без импорта EID-07/08.

### Где менять код
- `doge-identity-service/src/core/infrastructure/providers.py`
- `doge-identity-service/src/core/providers/runtime_factory.py` (optional new module)

### Out of scope
- Descriptor list / `build_registry` — t03
- Registry guard — t04
- Реальный httpx client для authentigate/eideasy — EID-02

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "
from core.config.providers import provide_app_config
from core.infrastructure.providers import provide_service_factory
f = provide_service_factory(provide_app_config())
print(f.get_eid_provider_registry())
"
```
