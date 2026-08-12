## Task workspace — `task-ids-04-05-t04-audit-s5-1-bearer-protocol-ssot`

- Story: [`../STORY-IDS-04-05-supabase-jwt-bearer-auth.md`](../STORY-IDS-04-05-supabase-jwt-bearer-auth.md)
- Audit source: [`../../../../epic-ids-04-audit-2026-05-30.md`](../../../../epic-ids-04-audit-2026-05-30.md) (S5-1)

---
**Приоритет:** P1  
**Сложность:** M  
**Статус:** ready  
**Wave:** `override epic_ids_04_audit_2026_05_30`  
---

## Task: refactor — single BearerTokenAuth Protocol source (S5-1)

### Цель
Устранить дублирование `BearerTokenAuth` Protocol: единственный SSOT — `core.domain.contracts`; `security.py` импортирует, не определяет.

### Почему это важно (риск)
Два Protocol-класса с одинаковой сигнатурой нарушают Single Source of Truth; type-checker и архитектурный контракт расходятся между `dependencies.py` и `service_factory.py`.

### Факты из кода
1. [`epic-ids-04-audit-2026-05-30.md`](../../../../epic-ids-04-audit-2026-05-30.md) S5-1 (L181–205).
2. [`src/core/api/security.py:22-24`](../../../../../../../src/core/api/security.py): локальный `@runtime_checkable class BearerTokenAuth(Protocol)`.
3. [`src/core/domain/contracts.py:116-118`](../../../../../../../src/core/domain/contracts.py): канонический `BearerTokenAuth` Protocol.
4. [`src/core/api/dependencies.py:9-10`](../../../../../../../src/core/api/dependencies.py): `TYPE_CHECKING` import из `core.api.security`.
5. [`src/core/infrastructure/service_factory.py:7`](../../../../../../../src/core/infrastructure/service_factory.py): import из `core.domain.contracts`.

### Gap / Проблема
Два отдельных Python-класса Protocol с идентичным API — SSOT нарушен.

### AC/DoD
- [ ] (P0) `BearerTokenAuth` определён **только** в `core.domain.contracts`.
- [ ] (P0) `security.py` импортирует `BearerTokenAuth` из domain; локальное определение удалено.
- [ ] (P0) `StubBearerTokenAuth` и `SupabaseJwtBearerTokenAuth` по-прежнему удовлетворяют Protocol (`isinstance(..., BearerTokenAuth)`).
- [ ] (P1) `pytest tests/test_security_primitives.py tests/test_supabase_jwt_auth.py -q` проходит.

### Где менять код
- `doge-identity-service/src/core/api/security.py`
- `doge-identity-service/src/core/api/dependencies.py` (TYPE_CHECKING import → domain при необходимости)

### Out of scope
- Перенос `UnauthorizedError` в domain (audit H-4: остаётся в security)
- Изменения JWT validator body

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "
from core.domain.contracts import BearerTokenAuth
from core.api.security import StubBearerTokenAuth, SupabaseJwtBearerTokenAuth
assert isinstance(StubBearerTokenAuth(), BearerTokenAuth)
print('BearerTokenAuth SSOT OK')
"
```
