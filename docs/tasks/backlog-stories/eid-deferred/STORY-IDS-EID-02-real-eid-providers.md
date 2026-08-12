# STORY-IDS-EID-02 — Authentigate provider (capstone): сборка боевого OIDC-провайдера

## Meta
- **Key:** `STORY-IDS-EID-02-real-eid-providers`
- **Epic:** `EPIC-IDS-09` (alias `EPIC-IDS-EID`)
- **Status:** 🔵 Декомпозирована (umbrella) → реализуется в [EID-10…14](../eid/EPIC-IDS-EID.md)
- **Источник:** backlog [`identity-todo-backlog-2026-06-04`](../../../analysis/identity-todo-backlog-2026-06-04.md) — E19, F23; gap EID-1, EID-2 · аудит [`authentigate-compatibility-audit-2026-06-07`](../../../analysis/authentigate-compatibility-audit-2026-06-07.md)
- **Зависит от:** [EID-01](../eid/STORY-IDS-EID-01-eid-verification-flow.md) (Done); платформа [EID-03…08](../eid/EPIC-IDS-EID.md) (Done)

> **⚠️ Эта стори декомпозирована.** Реальная работа ведётся в под-стори (читать их, не эту как задачу):
> [EID-10 settings-wiring](STORY-IDS-EID-10-provider-settings-wiring.md) → [EID-11 OIDC client](STORY-IDS-EID-11-authentigate-oidc-client.md) → [EID-12 start_flow](STORY-IDS-EID-12-authentigate-start-flow.md) + [EID-13 callback](STORY-IDS-EID-13-authentigate-callback-mapping.md) → [EID-14 go-live](STORY-IDS-EID-14-authentigate-registration-tests-docs.md); внешнее — [SPIKE-09](SPIKE-IDS-EID-09-authentigate-demo-access.md). Ниже — исходная capstone-формулировка как контекст/AC верхнего уровня.

## Зачем простыми словами
**Решение:** primary MVP eID-провайдер — **Authentigate** (SK ID Solutions, OIDC-gateway): EE Smart-ID/Mobile-ID/ID-card через один OIDC-флоу, demo бесплатно. eID Easy отложен (дорогой). Это **capstone**: когда платформа провайдеров готова (EID-03…08), здесь собираем конкретный `AuthentigateProvider` по контракту `EIDProviderPort` поверх готовых абстракций — без костылей.

## Scope
- **`AuthentigateProvider`** (`src/core/providers/authentigate/`, пакет: `provider.py`, `client.py`, `mapper.py`, `errors.py`) реализует `EIDProviderPort` (sync, 4 члена) и собирается через дескриптор/`ProviderRuntime` ([EID-03](../eid/STORY-IDS-EID-03-provider-plugin-backbone.md)).
- **`start_flow`:** генерирует `state`/`nonce`/PKCE (`code_challenge` S256), сохраняет в сессию при `create` (`code_verifier` через `SessionSecretBox` [EID-08](../eid/STORY-IDS-EID-08-session-secret-box.md); `scopes`/`acr`/`issuer` в `provider_session_data`), строит authorize-URL (endpoint из discovery [EID-07](../eid/STORY-IDS-EID-07-oidc-toolkit.md)).
- **`handle_callback`:** перечитывает сессию по `state`, обмен `code→token` (`client_secret_basic`), валидирует `id_token` через `IdTokenValidator` [EID-07](../eid/STORY-IDS-EID-07-oidc-toolkit.md), мапит `attributes.*` → `EIDVerificationResult` с нормализованным `subject_hash` **без префикса провайдера** ([EID-05](../eid/STORY-IDS-EID-05-canonical-provider-contract.md)).
- **Маппинг ошибок:** вендор-коды Authentigate → `EidErrorCode` ([EID-05](../eid/STORY-IDS-EID-05-canonical-provider-contract.md)).
- **Регистрация:** дескриптор Authentigate в наборе провайдеров; `EID_PROVIDER=authentigate` → активен (фикс EID-1 как guard сделан в EID-03).
- **Тесты:** юнит (start/callback/mapping/negative — в канон-кодах), live-тест против demo (скип без creds).

## Вне scope
- Платформенные доработки (реестр/конфиг/контракт/redirect/OIDC/крипто) — вынесены в [EID-03…08](../eid/EPIC-IDS-EID.md).
- eID Easy — отдельный провайдер позже (та же платформа, +1 дескриптор).

## Точки в коде (текущее состояние)
- Контракт/реестр: [`base.py`](../../../../src/core/providers/base.py), [`registry.py`](../../../../src/core/providers/registry.py); фабрика [`providers.py:92`](../../../../src/core/infrastructure/providers.py).
- Конфиг Authentigate: [`schema.py:31-35,141-145`](../../../../src/core/config/schema.py) (рефакторится в [EID-04](../eid/STORY-IDS-EID-04-provider-owned-config.md)).
- Callback-роут: динамический после [EID-06](../eid/STORY-IDS-EID-06-browser-callback-redirect.md); сейчас заглушка [`asgi_app.py:214-236`](../../../../src/core/api/asgi_app.py).
- Эталон провайдера: [`mock_provider.py`](../../../../src/core/providers/mock/mock_provider.py).

## Acceptance Criteria
- [ ] `AuthentigateProvider` реализует `EIDProviderPort` и зарегистрирован; `EID_PROVIDER=authentigate` → `get_active()` возвращает его, не падает.
- [ ] Полный OIDC-флоу (authorize → callback → token → id_token validation → map) проходит против demo (live-тест, скип без creds).
- [ ] Сырой `personal_code` никогда не возвращается/не логируется; `subject_hash` нормализован без провайдер-префикса.
- [ ] Вендор-ошибки замаплены в `EidErrorCode`; `user_cancel` доходит до SPA как `?eid_error=USER_CANCELLED` (через [EID-06](../eid/STORY-IDS-EID-06-browser-callback-redirect.md)).
- [ ] `EID_PROVIDER=<валидируемый, но не зарегистрированный>` → понятная `ConfigError` (EID-1).
- [ ] Юнит-тесты (разбор callback'а, маппинг, негативы) зелёные offline.

## Парадигма-якорь
[06-eid-providers](../../../runtime-docs/06-eid-providers.md), [04-security §Часть A](../../../runtime-docs/04-security.md) (шаги eID, PII), гайд [`Authentigate Integration guide.md`](../../../tech-requirements/Authentigate%20Integration%20guide.md).
