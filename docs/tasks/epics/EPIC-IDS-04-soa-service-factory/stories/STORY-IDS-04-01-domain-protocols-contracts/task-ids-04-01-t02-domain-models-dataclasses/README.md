## Task workspace — `task-ids-04-01-t02-domain-models-dataclasses`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000005`  
**Decision Ref:** [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) §6 Story 1  
**Story:** [`../STORY-IDS-04-01-domain-protocols-contracts.md`](../STORY-IDS-04-01-domain-protocols-contracts.md)  
---

## Task: implement — domain models dataclasses

### Цель
Создать `src/core/domain/models.py` с frozen dataclasses и domain-исключением `JwtValidationError` по epic L123–131. **`UnauthorizedError` здесь НЕ определяется** — единственный источник `core.api.security` (audit H-4, epic L131–132).

### Почему это важно
Protocols ссылаются на типы записей; без моделей type-checker и runtime Protocol checks неполны. Дублирование `UnauthorizedError` в domain сломает exception handler в `asgi_app.py` (500 вместо 401).

### Факты из кода
1. [`src/core/domain/`](../../../../../../../src/core/domain/) — каталог **отсутствует**.
2. [`src/core/api/security.py:13-18`](../../../../../../../src/core/api/security.py) — `UnauthorizedError` уже определён; domain и auth импортируют отсюда.
3. [`src/core/api/security.py:21-25`](../../../../../../../src/core/api/security.py) — `UserClaims` в security; epic требует копию в `core.domain.models` (req-09); Story 5 переэкспортирует из domain.
4. [`src/core/api/dependencies.py`](../../../../../../../src/core/api/dependencies.py) — identity-слоты пока `object | None`, типизация Protocol-ами — Story 6.

### Gap
Нет `ProfileRecord`, `VerificationSession`, `EIDAuditEvent`, `OAuthClient`, `OAuthTokenClaims`, `StoryDraft`, `UserClaims`, `JwtValidationError` в domain.

### AC/DoD
- [ ] (P0) `from core.domain.models import ProfileRecord, VerificationSession, EIDAuditEvent, OAuthClient, OAuthTokenClaims, StoryDraft, UserClaims, JwtValidationError` — без ошибок.
- [ ] (P0) Все record-dataclasses — `@dataclass(frozen=True)`.
- [ ] (P0) `UnauthorizedError` **не** определён в `core.domain.models` (импорт только из `core.api.security` где нужен).
- [ ] (P0) Domain-слой не импортирует `core.infrastructure.*`, `httpx`, `fastapi`, `joserfc`.

### Где менять код
- `doge-identity-service/src/core/domain/models.py` (новый)
- `doge-identity-service/src/core/domain/__init__.py` (re-export при необходимости)

### Out of scope
- Protocols — [`task-ids-04-01-t01-domain-contracts-protocols`](../task-ids-04-01-t01-domain-contracts-protocols/README.md)
- `EIDVerificationResult`, `EIDStartResult` — Story 4
- Supabase JWT impl — Story 5
- pytest Story 1 — t03

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "
from core.domain.models import (
    ProfileRecord, VerificationSession, EIDAuditEvent,
    OAuthClient, OAuthTokenClaims, StoryDraft, UserClaims, JwtValidationError,
)
from dataclasses import is_dataclass
for cls in (ProfileRecord, VerificationSession, EIDAuditEvent,
            OAuthClient, OAuthTokenClaims, StoryDraft, UserClaims):
    assert is_dataclass(cls) and cls.__dataclass_params__.frozen
import core.domain.models as m
assert not hasattr(m, 'UnauthorizedError') or 'UnauthorizedError' not in m.__all__ if hasattr(m, '__all__') else True
print('models OK')
"
```
