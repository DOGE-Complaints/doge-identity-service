# STORY-IDS-EID-12 — Authentigate start_flow: PKCE + authorize-URL + session persistence

## Meta
- **Key:** `STORY-IDS-EID-12-authentigate-start-flow`
- **Epic:** `EPIC-IDS-09` (alias `EPIC-IDS-EID`)
- **Status:** ⚪ Todo
- **Источник:** декомпозиция [STORY-IDS-EID-02](STORY-IDS-EID-02-real-eid-providers.md); гайд [`Authentigate Integration guide.md`](../../../tech-requirements/Authentigate%20Integration%20guide.md) §7, §17
- **Зависит от:** [EID-08](../eid/STORY-IDS-EID-08-session-secret-box.md) (Done), [EID-10](STORY-IDS-EID-10-provider-settings-wiring.md), [EID-11](STORY-IDS-EID-11-authentigate-oidc-client.md) (authorize_endpoint из discovery)

## Зачем простыми словами
«Запросная» половина флоу: пользователь жмёт «верифицироваться» → провайдер готовит секреты безопасности (state, nonce, PKCE), сохраняет их в сессию и строит ссылку на Authentigate, куда уйдёт браузер. Проверяется без сети (кроме discovery-мока) — по содержимому ссылки и полям сессии.

## Scope
- **`provider.py::start_flow`** (класс `AuthentigateProvider`, `provider_name="authentigate"`, `callback_path="/auth/authentigate/callback"`):
  - сгенерировать `state`, `nonce`, `code_verifier` + `code_challenge` (BASE64URL(SHA256), `method=S256`).
  - сохранить `VerificationSession` через `session_store.create` **при старте** (нет update): `state`, `nonce`, `code_verifier_encrypted = secret_box.seal(code_verifier)`, `code_verifier_hash = sha256(code_verifier)`, `provider="authentigate"`, `provider_session_data` = {scopes, acr_values, issuer, discovery_url}, `return_url`/`return_context`/`requested_action`, `status="started"`, `expires_at`.
  - построить authorize-URL на `authorization_endpoint` (из discovery): `response_type=code`, `client_id`, `redirect_uri`, `scope`, `state`, `nonce`, `acr_values`, `code_challenge`, `code_challenge_method=S256`, `ui_locales`, `sid_confirmation_message`/`mid_confirmation_message`(+`_format=GSM-7`).
  - вернуть `EIDStartResult(redirect_url, session_id, expires_at)`.

## Вне scope
- Обработка callback / token / id_token — [EID-13](STORY-IDS-EID-13-authentigate-callback-mapping.md).
- Регистрация провайдера в реестре — [EID-14](STORY-IDS-EID-14-authentigate-registration-tests-docs.md) (до неё `handle_callback` может быть заглушкой `NotImplementedError`).

## Решение (зафиксировать)
`sid/mid_confirmation_message` в `AuthentigateSettings` пока нет — захардкодить дефолт «DOGEstonia verification» (или добавить в settings). Рекомендация: дефолт-константа в провайдере, вынести в settings при необходимости локализации.

## Точки в коде (текущее состояние)
- Контракт/возврат: `EIDProviderPort.start_flow`, `EIDStartResult` [`base.py:50-71,32-36`](../../../../src/core/providers/base.py).
- Эталон создания сессии: [`mock_provider.py:24-57`](../../../../src/core/providers/mock/mock_provider.py) (`session_store.create`).
- Поля сессии (state/nonce/code_verifier_encrypted/code_verifier_hash/provider_session_data): [`models.py:44-59`](../../../../src/core/domain/models.py).
- Запечатывание секрета: `runtime.secret_box.seal` [`session_secret.py:38-45`](../../../../src/core/security/session_secret.py).
- Настройки: `runtime.provider_settings` (EID-10) → `AuthentigateSettings` [`authentigate/config.py:25-55`](../../../../src/core/providers/authentigate/config.py).
- discovery authorize_endpoint: [`discovery.py`](../../../../src/core/security/oidc/discovery.py) (через клиент EID-11).

## Acceptance Criteria
- [ ] `start_flow` создаёт сессию `started` с `provider="authentigate"`, запечатанным `code_verifier`, непустыми `state`/`nonce`.
- [ ] `redirect_url` содержит все обязательные params (`response_type=code`, `client_id`, `redirect_uri`, `scope` с openid+personal_code(+country), `state`, `nonce`, `acr_values`, `code_challenge`, `code_challenge_method=S256`).
- [ ] `provider_session_data` хранит scopes/acr/issuer/discovery для последующего callback.
- [ ] Юнит-тесты (URL + поля сессии) зелёные offline (discovery замокан).

## Парадигма-якорь
[04-security](../../../runtime-docs/04-security.md) (PKCE/state/nonce), [05-data-model](../../../runtime-docs/05-data-model.md) (sessions), [06-eid-providers](../../../runtime-docs/06-eid-providers.md).
