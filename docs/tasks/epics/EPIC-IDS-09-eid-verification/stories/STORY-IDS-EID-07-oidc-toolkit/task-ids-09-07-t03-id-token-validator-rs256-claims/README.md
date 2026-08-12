## Task workspace — `task-ids-09-07-t03-id-token-validator-rs256-claims`

- Story: [`../STORY-IDS-EID-07-oidc-toolkit.md`](../STORY-IDS-EID-07-oidc-toolkit.md)
- Prerequisite: t02 `JwksCache` ([`../task-ids-09-07-t02-jwks-cache-refresh-on-unknown-kid/README.md`](../task-ids-09-07-t02-jwks-cache-refresh-on-unknown-kid/README.md)); EID-05 `EidErrorCode` ([`../../STORY-IDS-EID-05-canonical-provider-contract/STORY-IDS-EID-05-canonical-provider-contract.md`](../../STORY-IDS-EID-05-canonical-provider-contract/STORY-IDS-EID-05-canonical-provider-contract.md))

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000020`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/STORY-IDS-EID-07-oidc-toolkit.md`](../../../../../../backlog-stories/STORY-IDS-EID-07-oidc-toolkit.md) Scope #3; [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F8)  
---

## Task: implement — `IdTokenValidator` RS256 + claims registry

### Цель
Реализовать `IdTokenValidator`: RS256 signature via `KeySet` + `iss/aud/exp/iat/nonce` через `jwt.JWTClaimsRegistry`; invalid token → domain validation error mappable to `IDENTITY_VALIDATION_FAILED`.

### Почему это важно
Story Scope #3 и AC #3: OIDC providers return signed `id_token`; core must validate before any adapter maps claims (EID-02).

### Факты из кода
1. [`supabase_validator.py:18-22,24-29`](../../../../../../../src/core/auth/supabase_validator.py) — `JWTClaimsRegistry` pattern with `iss`, `exp`, `sub`.
2. [`base.py:9-18,39-44`](../../../../../../../src/core/providers/base.py) — `EidErrorCode.IDENTITY_VALIDATION_FAILED`, `EIDProviderError`.
3. t02 provides `KeySet` lookup by `kid` from JWT header.
4. [`pyproject.toml`](../../../../../../../pyproject.toml) — `joserfc>=1.0.0`.

### Gap / Проблема
Only HS256 Supabase JWT validation exists; no RS256 OIDC id_token path.

### AC/DoD
- [x] (P0) `IdTokenValidator.validate(id_token, *, expected_iss, expected_aud, expected_nonce)` verifies RS256 signature.
- [x] (P0) Claims checked: `iss`, `aud`, `exp`, `iat`, `nonce` via `JWTClaimsRegistry` (Story AC #3).
- [x] (P0) Invalid/expired/wrong-issuer token raises domain error (not bare `JoseError` leak) mappable to `EidErrorCode.IDENTITY_VALIDATION_FAILED`.
- [x] (P1) Story AC #1 traceability (`IdTokenValidator` provider-agnostic).
- [x] (P1) Returns decoded claims dict on success (no Authentigate field mapping).

### Где менять код
- `doge-identity-service/src/core/security/oidc/id_token.py` (new)
- `doge-identity-service/src/core/security/oidc/__init__.py` (exports)

### Out of scope
- Mapping claims → `EIDVerificationResult` — EID-02
- Discovery/JWKS HTTP — t01/t02
- `OidcToolkit` / runtime wire — t04
- PKCE `code_verifier` crypto — EID-08

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.security.oidc.id_token import IdTokenValidator; print(IdTokenValidator)"
```
