## Task workspace — `task-ids-12-06-t03-jwks-cache-di-wiring`

- Story: [`../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md)
- Prerequisite: [`task-ids-12-06-t02-jwks-only-validator`](../task-ids-12-06-t02-jwks-only-validator/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000042`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md) §Подзадачи T03 (W2/W6); Story AC #3  
---

## Task: refactor — inject JwksCache from providers (W2)

### Цель
Вынести создание `JwksCache`/`httpx.Client` в `providers.py` по образцу OIDC toolkit; валидатор принимает `JwksCache | None` снаружи, не создаёт свой клиент; сузить `except Exception` (W6).

### Почему это важно
Текущий `http_client or httpx.Client(...)` в `__init__` — утечка незакрытого клиента и нарушение DI-паттерна проекта.

### Факты из кода
1. Internal client — [`supabase_validator.py:51-54`](../../../../../../../src/core/auth/supabase_validator.py).
2. DI этalon — [`toolkit.py:20-35`](../../../../../../../src/core/security/oidc/toolkit.py) `OidcToolkit.jwks_cache`.
3. Wiring point — [`providers.py:107-111`](../../../../../../../src/core/infrastructure/providers.py) `SupabaseJwtValidatorImpl(...)`.
4. JwksCache API — [`jwks_cache.py`](../../../../../../../src/core/security/oidc/jwks_cache.py).

### Gap / Проблема
Валидатор сам создаёт HTTP-клиент и кэш; lifecycle не управляется factory.

### AC/DoD
- [ ] (P0) `SupabaseJwtValidatorImpl` принимает `jwks_cache: JwksCache | None` (или эквивалент) — без `http_client`/`request_timeout_s` для self-created client.
- [ ] (P0) `provide_service_factory` создаёт/переиспользует `httpx.Client` + `JwksCache` по образцу `build_oidc_toolkit`.
- [ ] (P0) Валидатор не вызывает `httpx.Client(...)` внутри себя.
- [ ] (P1) `except Exception` в `validate` сужен до ожидаемых типов (W6).
- [ ] (P1) Story AC #3 traceability.

### Где менять код
- `doge-identity-service/src/core/auth/supabase_validator.py`
- `doge-identity-service/src/core/infrastructure/providers.py`

### Out of scope
- Test harness ES256 helper (t05) — но DI должен быть готов для инъекции мок-кэша в тестах
- OIDC toolkit refactor

### Проверка
```bash
cd doge-identity-service
grep -n 'httpx.Client' src/core/auth/supabase_validator.py && exit 1 || true
grep -n 'JwksCache' src/core/infrastructure/providers.py
.venv/bin/python -m pytest tests/test_di_service_factory.py tests/test_epic_ids_05_integration.py -q
```
