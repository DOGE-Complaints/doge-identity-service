# STORY-IDS-EID-14 — Authentigate go-live: регистрация, сквозные тесты, доки

## Meta
- **Key:** `STORY-IDS-EID-14-authentigate-registration-tests-docs`
- **Epic:** `EPIC-IDS-09` (alias `EPIC-IDS-EID`)
- **Status:** ⚪ Todo
- **Источник:** декомпозиция [STORY-IDS-EID-02](STORY-IDS-EID-02-real-eid-providers.md); гайд [`Authentigate Integration guide.md`](../../../tech-requirements/Authentigate%20Integration%20guide.md) §13, §20, §22, §23, §25
- **Зависит от:** [EID-12](STORY-IDS-EID-12-authentigate-start-flow.md), [EID-13](STORY-IDS-EID-13-authentigate-callback-mapping.md); **live-тест — после [SPIKE-IDS-EID-09](SPIKE-IDS-EID-09-authentigate-demo-access.md)**

## Зачем простыми словами
Финальная сборка: «щёлкнуть» готовый `AuthentigateProvider` в реестр (заменить стаб), закрыть полный набор ошибок и тестов, обновить документацию. До этой стори провайдер мог собираться при стабе — теперь он становится боевым выбором `EID_PROVIDER=authentigate`.

## Scope
- **Регистрация:** заменить `_build_authentigate_provider_stub` ([`authentigate/descriptor.py:9-12`](../../../../src/core/providers/authentigate/descriptor.py)) на реальный `build(runtime) -> AuthentigateProvider(runtime, runtime.provider_settings)`.
- **Полный error-маппинг (§20):** свести вендор-коды Authentigate (`user_cancel`, `invalid_scope`, `invalid acr_values`, `invalid_client`, `invalid_grant`, `too_many_requests`, …) к каноническим `EidErrorCode` — централизованно в `errors.py`; покрыть негативами.
- **CI-safe юниты (§22, §23.1):** registry registers authentigate; `EID_PROVIDER=authentigate` → `get_active()` отдаёт провайдер; never-returns-raw-personal_code; собранные start/callback/mapping проходят на мок-HTTP.
- **Live-demo тесты (§23.2):** полный флоу против demo (skip без creds: `AUTHENTIGATE_CLIENT_ID/SECRET/REDIRECT_URI` + demo issuer).
- **Доки:** обновить [06-eid-providers](../../../runtime-docs/06-eid-providers.md) (таблица провайдеров → `authentigate` ✅, статус); сверить с гайдом.

## Вне scope
- Реализация start/callback/client/mapper — [EID-11/12/13](STORY-IDS-EID-13-authentigate-callback-mapping.md).
- `private_key_jwt` (если SK не даст `client_secret_basic`) — отдельная стори при необходимости.

## Точки в коде (текущее состояние)
- Стаб, который надо заменить: [`authentigate/descriptor.py:9-19`](../../../../src/core/providers/authentigate/descriptor.py) (`ProviderNotRegisteredError`).
- Каталог дескрипторов: [`registry_builder.py:10-40`](../../../../src/core/providers/registry_builder.py) (`ALL_EID_PROVIDER_DESCRIPTORS`, `build_registry`).
- Реестр-guard (EID-1): [`registry.py`](../../../../src/core/providers/registry.py), [`descriptor.py:12-13`](../../../../src/core/providers/descriptor.py) (`ProviderNotRegisteredError`).
- `EidErrorCode`: [`base.py:9-18`](../../../../src/core/providers/base.py).
- Таблица провайдеров в доке: [`runtime-docs/06-eid-providers.md`](../../../runtime-docs/06-eid-providers.md).
- Существующие наборы тестов eID: [`tests/test_eid_providers.py`](../../../../tests/test_eid_providers.py), [`tests/test_eid_provider_registry.py`](../../../../tests/test_eid_provider_registry.py), [`tests/test_canonical_provider_contract.py`](../../../../tests/test_canonical_provider_contract.py).

## Acceptance Criteria
- [ ] `EID_PROVIDER=authentigate` (+ creds) → `get_active()` возвращает `AuthentigateProvider`, старт не падает.
- [ ] `EID_PROVIDER=authentigate` без обязательных env → понятная `ConfigError` (EID-1, уже guard) — регресс-тест.
- [ ] Полный вендор-маппинг ошибок §20 → `EidErrorCode`, покрыт негативами.
- [ ] CI-набор зелёный offline (registry/mapping/no-raw-PII); live-тест проходит против demo и **скипается** без creds.
- [ ] [06-eid-providers](../../../runtime-docs/06-eid-providers.md) отражает `authentigate` как ✅.

## Парадигма-якорь
[06-eid-providers](../../../runtime-docs/06-eid-providers.md) (модульность, статус провайдеров), [04-security](../../../runtime-docs/04-security.md), гайд §25 (production readiness).
