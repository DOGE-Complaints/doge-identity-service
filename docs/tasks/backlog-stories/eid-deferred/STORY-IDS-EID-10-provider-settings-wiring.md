# STORY-IDS-EID-10 — Provider settings wiring: типизированные настройки через ProviderRuntime

## Meta
- **Key:** `STORY-IDS-EID-10-provider-settings-wiring`
- **Epic:** `EPIC-IDS-09` (alias `EPIC-IDS-EID`)
- **Status:** ⚪ Todo
- **Источник:** readiness-проверка EID-03…08 (шов, найден при аудите готовности 2026-06-09); декомпозиция [STORY-IDS-EID-02](STORY-IDS-EID-02-real-eid-providers.md)
- **Зависит от:** [EID-03](../eid/STORY-IDS-EID-03-provider-plugin-backbone.md) (Done), [EID-04](../eid/STORY-IDS-EID-04-provider-owned-config.md) (Done)

## Зачем простыми словами
Провайдеру для сборки нужны его типизированные настройки (`AuthentigateSettings` с `acr_values`/`ui_locales`/`country`/`discovery_url`). Но сейчас `build(runtime)` получает только `ProviderRuntime`, в котором лежит `AppConfig`, а в `AppConfig` этих полей нет — они есть только в env-loader'е провайдера. Лоадер `config_spec.load(env)` умеет вернуть типизированные настройки, но при валидации конфига его результат **выбрасывается**. Нужно дотянуть типизированные настройки активного провайдера до `ProviderRuntime` — провайдер-агностично (пригодится и eideasy).

## Scope
- Протянуть `env` в сборку runtime: `build_provider_runtime` ([`runtime_factory.py`](../../../../src/core/providers/runtime_factory.py)) получает источник env (или `Mapping`), вызывает `descriptor.config_spec.load(env)` для **активного** провайдера и кладёт результат в `ProviderRuntime`.
- Добавить поле `provider_settings: object | None` (типизированный объект провайдера) в `ProviderRuntime` ([`runtime.py`](../../../../src/core/providers/runtime.py)).
- Для `mock` (нет настроек, `noop_provider_settings_loader` → `None`) — `provider_settings=None`, ничего не ломается.
- **Не** раздувать `AppConfig` новыми полями (acr/ui_locales/country/discovery остаются в `AuthentigateSettings`).

## Вне scope
- Использование настроек в самом провайдере — [EID-11/12/13](STORY-IDS-EID-11-authentigate-oidc-client.md).
- Любая Authentigate-специфика.

## Решение (зафиксировать)
`provider_settings` — нетипизированный слот (`object | None`), провайдер кастует к своему типу при `build`. Источник env: тот же, что у `provide_app_config` (env+dotenv), чтобы значения совпадали с уже загруженным `AppConfig` (без второго, рассинхронного чтения окружения).

## Точки в коде (текущее состояние)
- `ProviderRuntime` несёт только `config: AppConfig`, без settings-слота: [`runtime.py:15-22`](../../../../src/core/providers/runtime.py).
- `build_provider_runtime(config, session_store)` — без env, settings не грузятся: [`runtime_factory.py:16-36`](../../../../src/core/providers/runtime_factory.py).
- `ProviderConfigSpec.load(env)` уже умеет вернуть типизированные настройки, но при старте вызывается только `validate`: [`config_spec.py:22-29`](../../../../src/core/providers/config_spec.py); делегированная валидация [`schema.py:93`](../../../../src/core/config/schema.py) (`_validate_active_eid_provider_config`).
- Сборка фабрики: [`providers.py:92-96`](../../../../src/core/infrastructure/providers.py) (`build_provider_runtime` → `build_registry`).
- `AuthentigateSettings.load`: [`authentigate/config.py:37-55`](../../../../src/core/providers/authentigate/config.py).

## Acceptance Criteria
- [ ] `ProviderRuntime` имеет `provider_settings`; для активного провайдера он заполнен типизированным объектом из `config_spec.load(env)`.
- [ ] При `EID_PROVIDER=authentigate` (+ валидные creds) `runtime.provider_settings` — `AuthentigateSettings` с корректными `acr_values`/`ui_locales`/`country`/`discovery_url`.
- [ ] `EID_PROVIDER=mock` → `provider_settings is None`, существующие тесты зелёные.
- [ ] `AppConfig` не пополнен провайдер-специфичными полями.
- [ ] Offline-набор зелёный; тест на проброс настроек.

## Парадигма-якорь
[06-eid-providers](../../../runtime-docs/06-eid-providers.md) (provider-owned config), [03-soa-roles](../../../runtime-docs/03-soa-roles.md) (DI/фабрика).
