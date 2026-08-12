## Task workspace — `task-ids-12-06-t09-audit-f1-jwks-httpx-client-lifespan-close`

- Story: [`../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md)
- Prerequisite: [`task-ids-12-06-t08-story-acceptance-verification`](../task-ids-12-06-t08-story-acceptance-verification/README.md)
- Audit source: [`../../../../../../analysis/epic-ids-12-sec-06-audit-2026-07-04.md`](../../../../../../analysis/epic-ids-12-sec-06-audit-2026-07-04.md) (F1)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_12_sec_06_audit_2026_07_04`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-12-sec-06-audit-2026-07-04.md`](../../../../../../analysis/epic-ids-12-sec-06-audit-2026-07-04.md) §F1  
---

## Task: fix — JWKS httpx client lifespan shutdown (F1)

### Цель
Зарегистрировать JWKS `httpx.Client` из DI и явно закрыть его на shutdown приложения — закрыть частичный gap AC W2 «клиент … закрывается».

### Почему это важно
[`providers.py:115`](../../../../../../../src/core/infrastructure/providers.py) создаёт клиент для `JwksCache` без `close()`; process-singleton приемлем, но AC W2 и audit F1 требуют явного lifecycle.

### Факты из кода
1. JWKS client создаётся в [`providers.py:111-116`](../../../../../../../src/core/infrastructure/providers.py): `httpx.Client(...)` → `JwksCache(http_client, jwks_uri)`.
2. Валидатор не создаёт свой клиент — только принимает `jwks_cache` ([`supabase_validator.py:30-37`](../../../../../../../src/core/auth/supabase_validator.py)).
3. Lifespan hook существует: [`asgi_app.py:216-228`](../../../../../../../src/core/api/asgi_app.py) `_lifespan` — после `yield` нет cleanup.
4. Audit F1: [`epic-ids-12-sec-06-audit-2026-07-04.md`](../../../../../../analysis/epic-ids-12-sec-06-audit-2026-07-04.md) §2 F1.

### Gap / Проблема
JWKS HTTP-клиент живёт до конца процесса без явного `close()`; AC W2 выполнен частично (DI ✅, close ✗).

### AC/DoD
- [x] (P0) Ссылка на JWKS `httpx.Client` доступна на shutdown (через `ApiDependencies` или эквивалент).
- [x] (P0) `_lifespan` после `yield` вызывает `http_client.close()` (или context-manager pattern).
- [x] (P0) Offline suite green: `.venv/bin/python -m pytest -q -m "not live_integration"`.
- [x] (P1) `grep -rn 'supabase_jwt_secret\|SUPABASE_JWT_SECRET\|test-secret-for-demo' src/` пусто (без регрессии SEC-06).

### Где менять код
- `doge-identity-service/src/core/infrastructure/providers.py`
- `doge-identity-service/src/core/api/asgi_app.py`
- при необходимости `doge-identity-service/src/core/api/dependencies.py` / `ApiDependencies`

### Out of scope
- Shared HTTP-слой / переиспользование клиента между OIDC и JWKS.
- OAuth, live integration, `SUPABASE_TEST_JWT_SECRET` (t10).
- Новый `pkg-*.yaml`, смена `identity-active-package.current.yaml`.

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -q -m "not live_integration"
grep -rn 'supabase_jwt_secret\|SUPABASE_JWT_SECRET' src/ && exit 1 || true
```
