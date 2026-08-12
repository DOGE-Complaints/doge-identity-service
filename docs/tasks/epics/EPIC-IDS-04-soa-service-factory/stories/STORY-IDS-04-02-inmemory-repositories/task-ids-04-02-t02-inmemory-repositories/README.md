## Task workspace — `task-ids-04-02-t02-inmemory-repositories`

---
**Приоритет:** P0  
**Сложность:** L  
**Статус:** done  
**Wave:** `pkg-000005`  
**Decision Ref:** [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) §6 Story 2  
**Story:** [`../STORY-IDS-04-02-inmemory-repositories.md`](../STORY-IDS-04-02-inmemory-repositories.md)  
---

## Task: implement — InMemory repository classes

### Цель
Создать `src/core/infrastructure/repositories.py` со всеми InMemory-классами из epic L159–200: `InMemoryHealthRepository`, `InMemoryProfileRepository`, `InMemoryVerificationSessionStore`, `InMemoryEIDAuditLogRepository`, `InMemoryOAuthClientStore` (+ `from_config`), `InMemoryOAuthTokenService`, `InMemoryStoryDraftRepository`.

### Почему это важно
Все unit/service/HTTP-тесты идут через InMemory (EPIC-IDS-06 инвариант). Без реализаций factory и `build_api_dependencies` не могут заполнить identity-слоты реальными объектами.

### Факты из кода
1. [`src/core/infrastructure/repositories.py`](../../../../../../../src/core/infrastructure/repositories.py) — **отсутствует**; [`infrastructure/__init__.py`](../../../../../../../src/core/infrastructure/__init__.py) — пустой пакет.
2. [`src/core/security/hashing.py`](../../../../../../../src/core/security/hashing.py) — `hash_secret` готов для `InMemoryOAuthClientStore.from_config`.
3. [`src/core/domain/`](../../../../../../../src/core/domain/) — **отсутствует** (зависимость Story 1).
4. [`src/core/api/dependencies.py:36-44`](../../../../../../../src/core/api/dependencies.py) — слоты под репозитории зарезервированы как `object | None`.

### Gap
Epic §6 Story 2 Outputs L159–200 не реализованы; нет `isinstance(repo, ProfileRepository)` support.

### AC/DoD
- [ ] (P0) `isinstance(InMemoryProfileRepository(), ProfileRepository)` — True (после Story 1).
- [ ] (P0) `InMemoryProfileRepository().attach_eid_verification(...)` + повтор с тем же `verified_person_hash` для другого `user_id` → `RuntimeError`.
- [ ] (P0) `InMemoryVerificationSessionStore().get_by_state("unknown")` → `None`.
- [ ] (P0) `InMemoryOAuthClientStore.from_config(config)` — GPT client из `AppConfig` с demo-fallback (epic L164–197).
- [ ] (P0) Все InMemory классы зависят только от stdlib + `core.security.hashing` + domain (нет httpx, joserfc, fastapi).

### Где менять код
- `doge-identity-service/src/core/infrastructure/repositories.py` (новый)

### Out of scope
- `hash_secret` verify — t01
- Story 2 pytest AC — t03
- Supabase repositories — EPIC-IDS-05
- `provide_service_factory` wiring — Story 6

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "
from core.domain.contracts import ProfileRepository
from core.infrastructure.repositories import InMemoryProfileRepository
assert isinstance(InMemoryProfileRepository(), ProfileRepository)
print('InMemoryProfileRepository Protocol OK')
"
```
