# STORY-IDS-EID-07 — Provider-agnostic OIDC-тулкит: discovery, JWKS, ID-token validation

## Meta
- **Key:** `STORY-IDS-EID-07-oidc-toolkit`
- **Parent Epic:** [`../../../../EPIC-IDS-09-eid-verification.md`](../../../../EPIC-IDS-09-eid-verification.md)
- **Epic alias (код/backlog):** `EPIC-IDS-EID`
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-EID-07-oidc-toolkit.md`](../../../../backlog-stories/eid/STORY-IDS-EID-07-oidc-toolkit.md)
- **Decision Ref:** [`../../../../backlog-stories/STORY-IDS-EID-07-oidc-toolkit.md`](../../../../backlog-stories/eid/STORY-IDS-EID-07-oidc-toolkit.md); [`authentigate-compatibility-audit-2026-06-07`](../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F8)
- **Источник:** аудит [`authentigate-compatibility-audit-2026-06-07`](../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F8)
- **Зависит от:** [STORY-IDS-EID-03-provider-plugin-backbone](../STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md) (`ProviderRuntime` экспонирует тулкит)

## Зачем простыми словами
Authentigate — OIDC-провайдер: он отдаёт подписанный `id_token`, который мы обязаны проверить (подпись по JWKS из discovery, плюс issuer/audience/срок/nonce). Такого кода в сервисе нет — сейчас `joserfc` используется только для симметричного Supabase-JWT. Строим **не «валидатор под Authentigate», а общий OIDC-тулкит**, которым воспользуется любой будущий OIDC-провайдер (eIDAS-node, другой IdP).

## Scope
Новый модуль `src/core/security/oidc/` (provider-agnostic):
- **`OidcDiscoveryClient`** — тянет и кэширует `.well-known/openid-configuration` (authorization_endpoint, token_endpoint, jwks_uri, issuer). HTTP через общий `http_client` из `ProviderRuntime` с таймаутом `oidc_request_timeout_s` ([`schema.py:136`](../../../../../../src/core/config/schema.py)).
- **`JwksCache`** — кэш JWKS с TTL и refresh-on-unknown-kid (ротация ключей), отдаёт `joserfc` `KeySet`.
- **`IdTokenValidator`** — RS256-подпись через `KeySet` + проверка `iss/aud/exp/iat/nonce` через `jwt.JWTClaimsRegistry` (паттерн уже есть в [`supabase_validator.py:18-22`](../../../../../../src/core/auth/supabase_validator.py)).
- Собрать в `OidcToolkit` и добавить слот в `ProviderRuntime` (EID-03).

## Вне scope
- Маппинг claims `id_token` → `EIDVerificationResult` — это адаптер Authentigate ([EID-02](../../../../backlog-stories/STORY-IDS-EID-02-real-eid-providers.md)).
- PKCE `code_verifier` шифрование — [EID-08](../../../../backlog-stories/eid/STORY-IDS-EID-08-session-secret-box.md).
- Конкретные scope/acr — [EID-04](../STORY-IDS-EID-04-provider-owned-config/STORY-IDS-EID-04-provider-owned-config.md).

## Точки в коде (реализовано)
- Provider-agnostic OIDC module: [`src/core/security/oidc/`](../../../../../../src/core/security/oidc/) — `discovery.py`, `jwks_cache.py`, `id_token.py`, `toolkit.py`.
- RS256 + claims registry pattern: [`id_token.py`](../../../../../../src/core/security/oidc/id_token.py) (`JWTClaimsRegistry`, `OidcIdTokenValidationError` → `IDENTITY_VALIDATION_FAILED`).
- Runtime wire: [`runtime.py:15-22`](../../../../../../src/core/providers/runtime.py), [`runtime_factory.py:15-31`](../../../../../../src/core/providers/runtime_factory.py) (`oidc=build_oidc_toolkit(...)` when non-mock).
- Offline tests: [`tests/test_oidc_toolkit.py`](../../../../../../tests/test_oidc_toolkit.py) (12 tests, mocked httpx transport).

## Точки в коде (до реализации, archival)
- `joserfc` только HS256/симметрично: [`supabase_validator.py:3-5,17,26`](../../../../../../src/core/auth/supabase_validator.py) (`OctKey`, `JWTClaimsRegistry`).
- `joserfc>=1.0.0`, `httpx>=0.27.0` в зависимостях: [`pyproject.toml`](../../../../../../pyproject.toml).
- Таймаут OIDC уже в конфиге: [`schema.py:26,136`](../../../../../../src/core/config/schema.py).
- `ProviderRuntime` — слот `oidc` из [EID-03](../STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md): [`runtime.py:15-21`](../../../../../../src/core/providers/runtime.py), [`runtime_factory.py:14-29`](../../../../../../src/core/providers/runtime_factory.py) (`oidc=None` today).

## Acceptance Criteria
- [x] Модуль `core/security/oidc/` содержит `OidcDiscoveryClient`, `JwksCache`, `IdTokenValidator`, не зависящие от конкретного провайдера.
- [x] Discovery и JWKS кэшируются; неизвестный `kid` инициирует обновление JWKS.
- [x] `IdTokenValidator` проверяет подпись RS256 + `iss/aud/exp/iat/nonce`; невалидный токен → доменная ошибка валидации (мапится в `IDENTITY_VALIDATION_FAILED`, см. [EID-05](../STORY-IDS-EID-05-canonical-provider-contract/STORY-IDS-EID-05-canonical-provider-contract.md)).
- [x] Тулкит доступен провайдерам через `ProviderRuntime`.
- [x] Тесты с замоканными discovery/JWKS/подписью; offline-набор зелёный (без сети).

## Парадигма-якорь
[04-security](../../../../../runtime-docs/04-security.md) (валидация токенов), [06-eid-providers](../../../../../runtime-docs/06-eid-providers.md).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-09-07-t01-oidc-discovery-client`](./task-ids-09-07-t01-oidc-discovery-client/README.md) | pkg-000020 |
| 2 | [`task-ids-09-07-t02-jwks-cache-refresh-on-unknown-kid`](./task-ids-09-07-t02-jwks-cache-refresh-on-unknown-kid/README.md) | pkg-000020 |
| 3 | [`task-ids-09-07-t03-id-token-validator-rs256-claims`](./task-ids-09-07-t03-id-token-validator-rs256-claims/README.md) | pkg-000020 |
| 4 | [`task-ids-09-07-t04-oidc-toolkit-provider-runtime-wire`](./task-ids-09-07-t04-oidc-toolkit-provider-runtime-wire/README.md) | pkg-000020 |
| 5 | [`task-ids-09-07-t05-offline-oidc-toolkit-mocked-http-tests`](./task-ids-09-07-t05-offline-oidc-toolkit-mocked-http-tests/README.md) | pkg-000020 |
| 6 | [`task-ids-09-07-t06-story-acceptance-verification`](./task-ids-09-07-t06-story-acceptance-verification/README.md) | pkg-000020 |
