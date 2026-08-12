## Task workspace — `task-ids-04-01-t01-domain-contracts-protocols`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000005`  
**Decision Ref:** [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) §6 Story 1  
**Story:** [`../STORY-IDS-04-01-domain-protocols-contracts.md`](../STORY-IDS-04-01-domain-protocols-contracts.md)  
---

## Task: implement — domain contracts Protocols

### Цель
Создать `src/core/domain/contracts.py` с полным набором `@runtime_checkable` Protocols из EPIC-IDS-04 Story 1 Outputs (L92–122): `HealthRepository`, `ProfileRepository`, `VerificationSessionStore`, `EIDAuditLogRepository`, `OAuthClientStore`, `OAuthTokenService`, `StoryDraftRepository`, `SupabaseJwtValidator`, `BearerTokenAuth`.

### Почему это важно
Protocols — единственный источник истины об интерфейсах репозиториев и auth-портов. Без них InMemory/Supabase реализации и factory не имеют общего контракта; domain-слой остаётся пустым.

### Факты из кода
1. Каталог [`src/core/domain/`](../../../../../../../src/core/domain/) **отсутствует** — ни `contracts.py`, ни `models.py`.
2. [`src/core/api/security.py:28-30`](../../../../../../../src/core/api/security.py) — локальный `BearerTokenAuth(Protocol)`; после EPIC-IDS-04 канонический Protocol живёт в domain, security импортирует или дублирует через re-export (решение в t02/t05).
3. [`src/core/security/hashing.py`](../../../../../../../src/core/security/hashing.py) — уже существует; domain не должен его импортировать.
4. [`src/core/api/dependencies.py:12-22`](../../../../../../../src/core/api/dependencies.py) — `EPIC_IDS_04_OPTIONAL_FIELDS` зарезервированы под Protocol-типы из этого модуля.

### Gap
Нет `core/domain/contracts.py`; epic §6 Story 1 Outputs L92–122 не реализованы.

### AC/DoD
- [ ] (P0) `from core.domain.contracts import ProfileRepository, VerificationSessionStore, EIDAuditLogRepository, OAuthClientStore, OAuthTokenService, StoryDraftRepository, BearerTokenAuth, SupabaseJwtValidator, HealthRepository` — без ошибок.
- [ ] (P0) Все Protocols имеют `@runtime_checkable`.
- [ ] (P0) Сигнатуры методов соответствуют epic L94–122 (forward refs на модели из `models.py` через `TYPE_CHECKING` или строковые аннотации).
- [ ] (P0) Domain-слой не импортирует `core.infrastructure.*`, `httpx`, `fastapi`, `joserfc`.

### Где менять код
- `doge-identity-service/src/core/domain/__init__.py` (новый)
- `doge-identity-service/src/core/domain/contracts.py` (новый)

### Out of scope
- Dataclasses в `models.py` — [`task-ids-04-01-t02-domain-models-dataclasses`](../task-ids-04-01-t02-domain-models-dataclasses/README.md)
- InMemory-реализации — Story 2
- `EIDProviderPort` — Story 4 (`core/providers/base.py`)
- pytest AC Story 1 — [`task-ids-04-01-t03-story1-acceptance-verification`](../task-ids-04-01-t03-story1-acceptance-verification/README.md)

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "
from core.domain.contracts import (
    ProfileRepository, VerificationSessionStore, EIDAuditLogRepository,
    OAuthClientStore, OAuthTokenService, StoryDraftRepository,
    BearerTokenAuth, SupabaseJwtValidator, HealthRepository,
)
import typing
for p in (ProfileRepository, VerificationSessionStore, EIDAuditLogRepository,
          OAuthClientStore, OAuthTokenService, StoryDraftRepository,
          BearerTokenAuth, SupabaseJwtValidator, HealthRepository):
    assert typing.runtime_checkable(p) or hasattr(p, '__protocol_attrs__')
print('contracts import OK')
"
```
