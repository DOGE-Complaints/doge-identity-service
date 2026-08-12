# STORY-IDS-EID-13 — Authentigate handle_callback: token + id_token validation + claims mapping

## Meta
- **Key:** `STORY-IDS-EID-13-authentigate-callback-mapping`
- **Epic:** `EPIC-IDS-09` (alias `EPIC-IDS-EID`)
- **Status:** ⚪ Todo
- **Источник:** декомпозиция [STORY-IDS-EID-02](STORY-IDS-EID-02-real-eid-providers.md); гайд [`Authentigate Integration guide.md`](../../../tech-requirements/Authentigate%20Integration%20guide.md) §11, §12, §19
- **Зависит от:** [EID-11](STORY-IDS-EID-11-authentigate-oidc-client.md), [EID-12](STORY-IDS-EID-12-authentigate-start-flow.md), [EID-05](../eid/STORY-IDS-EID-05-canonical-provider-contract.md) (Done), [EID-07](../eid/STORY-IDS-EID-07-oidc-toolkit.md) (Done)

## Зачем простыми словами
«Ответная» половина: Authentigate вернул `code`+`state` — провайдер достаёт из сессии секреты, меняет код на токены, проверяет подпись и claims `id_token`, и достаёт из него страну + идентификатор личности. На выходе — провайдер-агностичный `EIDVerificationResult`, без сырого `personal_code`. Это главный data-flow контракт адаптера.

## Scope
- **`provider.py::handle_callback(raw_params)`:**
  - разобрать `state`/`code`/`error`; нет `state` → `EidErrorCode.STATE_MISMATCH`, нет `code` (или есть `error=user_cancel`) → `USER_CANCELLED`/`STATE_MISMATCH`.
  - перечитать сессию по `state` (`runtime.session_store.get_by_state`), достать `nonce` и `secret_box.open(code_verifier_encrypted)`.
  - token-обмен через клиент ([EID-11](STORY-IDS-EID-11-authentigate-oidc-client.md)).
  - валидация `id_token` через `runtime.oidc.id_token_validator(jwks_uri).validate(id_token, expected_iss=issuer, expected_aud=client_id, expected_nonce=session.nonce)`.
- **`mapper.py`:** claims → `EIDVerificationResult`:
  - `country = attributes[PERSONAL_CODE_COUNTRY]`, `personal_code = attributes[PERSONAL_CODE]`, `login_method = acr` (или `amr`).
  - **canonical** `subject_hash = hash_secret(f"{country}:{personal_code}", key=config.eid_secret)` — **без префикса провайдера** (по [EID-05](../eid/STORY-IDS-EID-05-canonical-provider-contract.md); расхождение с гайдом §12.3, который устарел).
  - country-allowlist (EE) → `COUNTRY_NOT_ALLOWED`; нет нужного claim → `MISSING_REQUIRED_CLAIM`.
  - **никогда** не возвращать/не логировать сырой `personal_code`.
  - вернуть `EIDVerificationResult(provider="authentigate", country, subject_hash, login_method, verified_at)`.

## Вне scope
- Двойной HMAC `verified_person_hash` и запись в профиль — делает оркестратор ([`handlers.py`](../../../../src/core/api/handlers.py), готово в EID-01/05/06).
- Проброс кода ошибки в redirect — оркестратор + EID-06 (готово).

## Решение (зафиксировать)
Ключи claim'ов вынести в **одну константу** в `mapper.py` (`PERSONAL_CODE`, `PERSONAL_CODE_COUNTRY`) — точное имя `attributes.*` подтверждается [SPIKE-IDS-EID-09](SPIKE-IDS-EID-09-authentigate-demo-access.md) (в доках возможна опечатка `attribues`), чтобы правка была однострочной.

## Точки в коде (текущее состояние)
- Контракт результата: `EIDVerificationResult` [`base.py:21-29`](../../../../src/core/providers/base.py).
- Оркестратор зовёт `provider.handle_callback(raw_params=...)`, ловит `EIDProviderError`→код, делает двойной HMAC: [`handlers.py:191-375`](../../../../src/core/api/handlers.py) (callback), формула `verified_person_hash` ~[`handlers.py:304-307`](../../../../src/core/api/handlers.py).
- id_token-валидатор: `IdTokenValidator.validate(id_token, expected_iss, expected_aud, expected_nonce)` [`id_token.py:33-74`](../../../../src/core/security/oidc/id_token.py); `jwks_cache`/`id_token_validator(jwks_uri)` [`toolkit.py:20-29`](../../../../src/core/security/oidc/toolkit.py).
- Распечатывание секрета: `secret_box.open` [`session_secret.py:41-45`](../../../../src/core/security/session_secret.py).
- `hash_secret`: [`hashing.py:9`](../../../../src/core/security/hashing.py); `eid_secret` в `AppConfig` [`schema.py`](../../../../src/core/config/schema.py).
- Эталон возврата result (без префикса): [`mock_provider.py:59-71`](../../../../src/core/providers/mock/mock_provider.py).

## Acceptance Criteria
- [ ] `handle_callback` перечитывает сессию по `state`, делает token-обмен и валидирует `id_token` (iss/aud/exp/iat/nonce, подпись по JWKS).
- [ ] mapper отдаёт `EIDVerificationResult` с `country`, `login_method`, каноническим `subject_hash` (без провайдер-префикса).
- [ ] Сырой `personal_code` не возвращается и не попадает в логи.
- [ ] Негативы → корректные `EidErrorCode`: нет state/code, `country≠EE`, нет personal_code, невалидный `id_token`, `user_cancel`.
- [ ] Юнит-тесты (mapping + негативы, замоканный token/JWKS) зелёные offline.

## Парадигма-якорь
[04-security §Часть A](../../../runtime-docs/04-security.md) (id_token, PII, anti-Sybil), [06-eid-providers](../../../runtime-docs/06-eid-providers.md), [05-data-model](../../../runtime-docs/05-data-model.md).
