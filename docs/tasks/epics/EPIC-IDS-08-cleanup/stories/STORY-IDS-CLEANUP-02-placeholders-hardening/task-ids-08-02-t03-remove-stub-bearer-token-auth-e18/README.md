## Task workspace — `task-ids-08-02-t03-remove-stub-bearer-token-auth-e18`

- Story: [`../STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../STORY-IDS-CLEANUP-02-placeholders-hardening.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-02-placeholders-hardening.md) Scope E18; [`../task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/owner-decisions-e17-e22.md`](../task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/owner-decisions-e17-e22.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000013`  
**Skill declared:** python-pro  
---

## Task: refactor — remove StubBearerTokenAuth (E18)

### Цель
Удалить неиспользуемый класс `StubBearerTokenAuth` и переписать зависимые тесты на `SupabaseJwtBearerTokenAuth` + mock validator (backlog Scope: «удалить неиспользуемый класс»).

### Почему это важно
Legacy stub не используется в prod wiring ([`04-security`](../../../../../../../runtime-docs/04-security.md):103); оставляет ложное впечатление активного auth-path. Story AC #1, AC #3.

### Факты из кода
1. Определение: [`security.py:22-31`](../../../../../../../src/core/api/security.py) — `StubBearerTokenAuth`.
2. Prod: `build_api_dependencies()` → `SupabaseJwtBearerTokenAuth` ([`dependencies.py`](../../../../../../../src/core/api/dependencies.py) via service factory).
3. Test refs:
   - [`tests/test_security_primitives.py:15,43,48,52`](../../../../../../../tests/test_security_primitives.py)
   - [`tests/test_api_dependencies.py:17,53,65`](../../../../../../../tests/test_api_dependencies.py)
   - [`tests/test_service_factory.py:7,85`](../../../../../../../tests/test_service_factory.py)
4. EPIC-IDS-04 audit task t04 — Protocol check `isinstance(StubBearerTokenAuth(), BearerTokenAuth)` потребует замены.

### Gap / Проблема
Класс помечен backlog как placeholder; grep по `StubBearerTokenAuth` ≠ 0 из-за tests.

### AC/DoD
- [ ] (P0) Story AC #1: решение E18 выполнено (удалить класс per backlog Scope).
- [ ] (P0) Story AC #3: `rg StubBearerTokenAuth src tests` = 0.
- [ ] (P0) `BearerTokenAuth` Protocol coverage сохранён через `SupabaseJwtBearerTokenAuth` + mock.
- [ ] (P1) Offline pytest green.

### Где менять код
- [`src/core/api/security.py`](../../../../../../../src/core/api/security.py) — удалить `StubBearerTokenAuth`, `STUB_SUPABASE_USER_ID` если unused
- [`tests/test_security_primitives.py`](../../../../../../../tests/test_security_primitives.py)
- [`tests/test_api_dependencies.py`](../../../../../../../tests/test_api_dependencies.py)
- [`tests/test_service_factory.py`](../../../../../../../tests/test_service_factory.py)

### Out of scope
- Изменение prod JWT validation logic
- Historical epic audit markdown (docs/tasks) — не править immutable pkg

### Проверка
```bash
cd doge-identity-service
rg "StubBearerTokenAuth" src tests
.venv/bin/python -m pytest tests/test_security_primitives.py tests/test_api_dependencies.py tests/test_service_factory.py -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
