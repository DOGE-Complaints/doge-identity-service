## Task workspace — `task-ids-09-07-t01-oidc-discovery-client`

- Story: [`../STORY-IDS-EID-07-oidc-toolkit.md`](../STORY-IDS-EID-07-oidc-toolkit.md)
- Prerequisite: STORY-IDS-EID-03 Done ([`../STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md`](../STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md))

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000020`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/STORY-IDS-EID-07-oidc-toolkit.md`](../../../../../../backlog-stories/STORY-IDS-EID-07-oidc-toolkit.md) Scope #1; [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F8)  
---

## Task: implement — `OidcDiscoveryClient` with cached openid-configuration

### Цель
Реализовать provider-agnostic `OidcDiscoveryClient`: fetch/cache `.well-known/openid-configuration` (`authorization_endpoint`, `token_endpoint`, `jwks_uri`, `issuer`) через `http_client` из `ProviderRuntime`.

### Почему это важно
Story Scope #1 и AC #1–2: без discovery нельзя получить `jwks_uri` для JWKS cache (t02) и RS256 validation (t03).

### Факты из кода
1. Модуля `src/core/security/oidc/` **нет** (glob 0 files).
2. [`runtime.py:15-21`](../../../../../../../src/core/providers/runtime.py) — `ProviderRuntime.http_client: httpx.Client | None`.
3. [`runtime_factory.py:19-21`](../../../../../../../src/core/providers/runtime_factory.py) — `httpx.Client(timeout=float(config.oidc_request_timeout_s))` when `eid_provider != "mock"`.
4. [`schema.py:27,146`](../../../../../../../src/core/config/schema.py) — `oidc_request_timeout_s` field + env default `10`.
5. [`pyproject.toml`](../../../../../../../pyproject.toml) — `httpx>=0.27.0` dependency present.

### Gap / Проблема
Нет OIDC discovery client; JWKS/validation blocked.

### AC/DoD
- [x] (P0) `OidcDiscoveryClient` in `core/security/oidc/` fetches `{issuer}/.well-known/openid-configuration` via injected `httpx.Client`.
- [x] (P0) Parsed fields: `authorization_endpoint`, `token_endpoint`, `jwks_uri`, `issuer` (typed dataclass/TypedDict).
- [x] (P0) In-memory cache: repeat fetch for same issuer returns cached document without HTTP (Story AC #2 partial).
- [x] (P1) Story AC #1 traceability (`OidcDiscoveryClient` provider-agnostic).
- [x] (P1) No Authentigate-specific imports or claim mapping.

### Где менять код
- `doge-identity-service/src/core/security/oidc/__init__.py` (new)
- `doge-identity-service/src/core/security/oidc/discovery.py` (new)

### Out of scope
- JWKS fetch/cache — t02
- ID token signature/claims — t03
- `OidcToolkit` assembly / `ProviderRuntime.oidc` wire — t04
- Claims → `EIDVerificationResult` — EID-02 (backlog)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.security.oidc.discovery import OidcDiscoveryClient; print(OidcDiscoveryClient)"
```
