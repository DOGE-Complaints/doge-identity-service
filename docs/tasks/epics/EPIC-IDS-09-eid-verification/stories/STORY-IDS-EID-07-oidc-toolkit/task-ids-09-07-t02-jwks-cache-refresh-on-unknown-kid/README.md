## Task workspace — `task-ids-09-07-t02-jwks-cache-refresh-on-unknown-kid`

- Story: [`../STORY-IDS-EID-07-oidc-toolkit.md`](../STORY-IDS-EID-07-oidc-toolkit.md)
- Prerequisite: t01 `OidcDiscoveryClient` ([`../task-ids-09-07-t01-oidc-discovery-client/README.md`](../task-ids-09-07-t01-oidc-discovery-client/README.md))

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000020`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/STORY-IDS-EID-07-oidc-toolkit.md`](../../../../../../backlog-stories/STORY-IDS-EID-07-oidc-toolkit.md) Scope #2; [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F8)  
---

## Task: implement — `JwksCache` with TTL and refresh-on-unknown-kid

### Цель
Реализовать `JwksCache`: кэш JWKS с TTL, refresh-on-unknown-`kid`, возврат `joserfc` `KeySet` для RS256 verify.

### Почему это важно
Story Scope #2 и AC #2: ротация ключей IdP требует refresh при неизвестном `kid`; без KeySet невозможен `IdTokenValidator` (t03).

### Факты из кода
1. [`supabase_validator.py:3-5,17`](../../../../../../../src/core/auth/supabase_validator.py) — `joserfc.jwt`, `OctKey` (symmetric only today).
2. [`pyproject.toml`](../../../../../../../pyproject.toml) — `joserfc>=1.0.0`.
3. t01 provides `jwks_uri` from discovery document.
4. [`runtime_factory.py:19-21`](../../../../../../../src/core/providers/runtime_factory.py) — shared `http_client` for JWKS HTTP fetch.

### Gap / Проблема
Нет JWKS cache; key rotation unsupported.

### AC/DoD
- [x] (P0) `JwksCache` fetches JWKS JSON from `jwks_uri` via `httpx.Client`.
- [x] (P0) TTL cache: valid KeySet served without refetch until TTL expires.
- [x] (P0) Unknown `kid` on lookup triggers JWKS refresh and retry (Story AC #2).
- [x] (P0) Returns `joserfc` `KeySet` suitable for RS256 decode.
- [x] (P1) Story AC #1 traceability (`JwksCache` provider-agnostic).

### Где менять код
- `doge-identity-service/src/core/security/oidc/jwks_cache.py` (new)
- `doge-identity-service/src/core/security/oidc/__init__.py` (exports)

### Out of scope
- Discovery fetch — t01
- ID token claims validation — t03
- Provider-specific claim mapping — EID-02
- Live network in unit tests — t05 (mock HTTP)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.security.oidc.jwks_cache import JwksCache; print(JwksCache)"
```
