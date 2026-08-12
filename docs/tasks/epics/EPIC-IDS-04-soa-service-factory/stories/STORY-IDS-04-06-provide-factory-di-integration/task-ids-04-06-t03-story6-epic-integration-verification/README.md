## Task workspace — `task-ids-04-06-t03-story6-epic-integration-verification`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** ready  
**Wave:** `pkg-000005`  
**Decision Ref:** [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) §6 Story 6, §8  
**Story:** [`../STORY-IDS-04-06-provide-factory-di-integration.md`](../STORY-IDS-04-06-provide-factory-di-integration.md)  
---

## Task: tests — Story 6 + epic §8 integration verification

### Цель
Добавить pytest/smoke-покрытие AC Story 6 (epic L355–360) и bash-сценариев epic §8 (L376–420): imports, Protocol isinstance, factory creation, `build_api_dependencies` integration.

### Почему это важно
Story 6 — финальная склейка эпика; §8 smoke — операторская верификация перед EPIC-IDS-06 unit-тестами.

### Факты из кода
1. Story 6 AC — [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) L355–360.
2. Epic §8 verification — [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) L374–424.
3. [`src/core/api/dependencies.py`](../../../../../../../src/core/api/dependencies.py) — EPIC-IDS-04 hooks; integration после t02.
4. [`tests/test_di_service_factory.py`](../../../../../../../tests/test_di_service_factory.py) — **не создавать** (target EPIC-IDS-06, epic §8 step 5 L422–423).

### Gap
Нет integration test file для Story 6 / epic §8 steps 1–4.

### AC/DoD
- [ ] (P0) `provide_service_factory()` при `DB_BACKEND=in_memory` возвращает `DefaultServiceFactory` с InMemory-репозиториями.
- [ ] (P0) `provide_service_factory(config_with_supabase)` — fallback на InMemory + warning (до EPIC-IDS-05), не падает.
- [ ] (P0) `build_api_dependencies().profile_repository is not None` (после EPIC-IDS-04 уже не `None`).
- [ ] (P0) `build_api_dependencies().eid_provider_registry.get("mock").provider_name == "mock"`.
- [ ] (P0) `build_api_dependencies().bearer_token_auth.__class__.__name__ == "SupabaseJwtBearerTokenAuth"`.
- [ ] (P0) Epic §8 steps 1–4 (imports, Protocol isinstance, factory, DI) проходят в pytest или documented smoke script.

### Где менять код
- `doge-identity-service/tests/test_epic_ids_04_integration.py` (новый)

### Out of scope
- `tests/test_di_service_factory.py` — EPIC-IDS-06 (epic §8 step 5)
- `asgi_app.py` changes
- Plan files (`.cursor/plans/*`)

### Проверка
```bash
cd doge-identity-service

# Epic §8 step 1 — imports
.venv/bin/python -c "
from core.domain.contracts import ProfileRepository, VerificationSessionStore, EIDAuditLogRepository, OAuthClientStore, OAuthTokenService, StoryDraftRepository, BearerTokenAuth, SupabaseJwtValidator
from core.infrastructure.repositories import InMemoryProfileRepository
from core.infrastructure.service_factory import DefaultServiceFactory
from core.infrastructure.providers import provide_service_factory
from core.providers.base import EIDProviderPort, EIDVerificationResult, EIDStartResult
from core.providers.registry import EIDProviderRegistry
from core.providers.mock.mock_provider import MockEIDProvider
from core.auth.supabase_validator import SupabaseJwtValidatorImpl, JwtValidationError
from core.api.security import SupabaseJwtBearerTokenAuth
print('Imports OK')
"

# Epic §8 steps 2–4 + Story 6 AC
.venv/bin/python -m pytest tests/test_epic_ids_04_integration.py -v
```
