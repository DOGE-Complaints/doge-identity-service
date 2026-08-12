# STORY-IDS-EID-11 — Authentigate OIDC client: discovery binding + token exchange

## Meta
- **Key:** `STORY-IDS-EID-11-authentigate-oidc-client`
- **Epic:** `EPIC-IDS-09` (alias `EPIC-IDS-EID`)
- **Status:** ⚪ Todo
- **Источник:** декомпозиция [STORY-IDS-EID-02](STORY-IDS-EID-02-real-eid-providers.md); гайд [`Authentigate Integration guide.md`](../../../tech-requirements/Authentigate%20Integration%20guide.md) §10, §11
- **Зависит от:** [EID-07](../eid/STORY-IDS-EID-07-oidc-toolkit.md) (Done), [EID-10](STORY-IDS-EID-10-provider-settings-wiring.md)

## Зачем простыми словами
Это «вендорный транспорт» Authentigate: найти у провайдера адреса (через OIDC discovery) и обменять `code` на токены (token endpoint). Изолируем сетевую/протокольную часть в отдельном клиенте, чтобы оркестрация провайдера (start/callback) её не знала и чтобы это легко тестировалось с замоканным HTTP.

## Scope
- **`client.py` (`providers/authentigate/`):** обёртка над `runtime.oidc` + `runtime.http_client`:
  - резолв endpoints через `runtime.oidc.discovery.get_discovery(issuer)` → `authorization_endpoint`/`token_endpoint`/`jwks_uri`.
  - token-обмен: POST на `token_endpoint`, `grant_type=authorization_code`, `code`, `redirect_uri` (идентичный authorize), `code_verifier`; аутентификация клиента — `client_secret_basic` (HTTP Basic `client_id:client_secret`).
  - разбор token-ответа: `{access_token, id_token, token_type, expires_in, scope}`; проверка наличия `id_token` и `token_type=Bearer`.
- **Маппинг ошибок транспорта → `EidErrorCode`:** сетевой/HTTP-сбой → `PROVIDER_UNAVAILABLE`/`TOKEN_EXCHANGE_FAILED`; `invalid_grant` → `TOKEN_EXCHANGE_FAILED`; отсутствие `id_token` → `IDENTITY_VALIDATION_FAILED`. Бросать `EIDProviderError(code=...)`.

## Вне scope
- Валидация подписи/claims `id_token` — делает `IdTokenValidator` из тулкита, вызывается в [EID-13](STORY-IDS-EID-13-authentigate-callback-mapping.md).
- Генерация authorize-URL — [EID-12](STORY-IDS-EID-12-authentigate-start-flow.md).
- `private_key_jwt` — вне MVP (гайд §10.3); только `client_secret_basic`.

## Открытый пункт (из SPIKE-09)
Доступность `client_secret_basic` для нашего клиента подтверждается [SPIKE-IDS-EID-09](SPIKE-IDS-EID-09-authentigate-demo-access.md). Юниты на mock не блокируются этим.

## Точки в коде (текущее состояние)
- OIDC-тулкит: `runtime.oidc.discovery.get_discovery(issuer)` → [`discovery.py:26-44`](../../../../src/core/security/oidc/discovery.py) (`OidcDiscoveryDocument`); `runtime.oidc` слот [`runtime.py`](../../../../src/core/providers/runtime.py).
- HTTP-клиент с таймаутом `oidc_request_timeout_s`: [`runtime_factory.py:21-26`](../../../../src/core/providers/runtime_factory.py).
- `EidErrorCode`/`EIDProviderError`: [`base.py:9-47`](../../../../src/core/providers/base.py).
- Настройки (issuer/redirect_uri/client_id/secret): `AuthentigateSettings` [`authentigate/config.py:25-55`](../../../../src/core/providers/authentigate/config.py) (через `runtime.provider_settings`, EID-10).

## Acceptance Criteria
- [ ] Клиент резолвит token/authorization endpoints через discovery (с кэшем тулкита).
- [ ] Token-обмен формирует корректный POST (`grant_type`, `code`, `redirect_uri`, `code_verifier`) + HTTP Basic; возвращает структурированный token-ответ.
- [ ] Ошибки транспорта/`invalid_grant`/нет `id_token` → `EIDProviderError` с корректным `EidErrorCode` (не голое исключение).
- [ ] Юнит-тесты с замоканным `httpx` (успех, `invalid_grant`, сетевой сбой, нет `id_token`); сеть в offline не дёргается.

## Парадигма-якорь
[04-security](../../../runtime-docs/04-security.md) (token-обмен), [06-eid-providers](../../../runtime-docs/06-eid-providers.md).
