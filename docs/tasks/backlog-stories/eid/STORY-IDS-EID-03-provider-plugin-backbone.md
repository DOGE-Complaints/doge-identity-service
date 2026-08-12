# STORY-IDS-EID-03 — Plugin-платформа провайдеров: дескрипторы, DI-контекст, реестр-guard

## Meta
- **Key:** `STORY-IDS-EID-03-provider-plugin-backbone`
- **Epic:** `EPIC-IDS-09` (alias `EPIC-IDS-EID`)
- **Status:** 🟢 Done (синхр. 2026-06-26: код построен — [`providers/registry.py`](../../../../src/core/providers/registry.py), [`descriptor.py`](../../../../src/core/providers/descriptor.py); совпадает с `EPIC-IDS-EID`)
- **Источник:** аудит [`authentigate-compatibility-audit-2026-06-07`](../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F5, F9, F13-guard); backlog gap EID-1
- **Зависит от:** [STORY-IDS-EID-01](STORY-IDS-EID-01-eid-verification-flow.md) (оркестрация на mock — Done)

## Зачем простыми словами
Сейчас единственный провайдер (`mock`) **жёстко вшит** в фабрику, а реестр на неизвестном провайдере падает голым `KeyError`. Провайдеров eID будет много — нужно превратить «один захардкоженный mock» в **подключаемую платформу**: каждый провайдер сам описывает, как он называется и как собирается, а ядро только выбирает активного. Это фундамент, на котором стоят остальные EID-стори.

## Scope
- **`EIDProviderDescriptor`** (новый): декларативное описание провайдера — `name`, `config_spec` (наполняется в [EID-04](STORY-IDS-EID-04-provider-owned-config.md)), `build(runtime) -> EIDProviderPort`.
- **`ProviderRuntime`** (новый DI-bundle): общие синглтоны для провайдеров — `config`, `session_store`, `http_client` (`httpx.Client` с таймаутом `oidc_request_timeout_s`), плюс слоты под `secret_box` ([EID-08](STORY-IDS-EID-08-session-secret-box.md)) и `oidc` ([EID-07](STORY-IDS-EID-07-oidc-toolkit.md)), `clock`. Собирается **один раз** в фабрике.
- **Lazy-реестр:** `build_registry(runtime)` регистрирует **активный** провайдер (по `config.eid_provider`) + `mock`; не создаёт сетевые клиенты в mock/in-memory режиме.
- **Guard вместо `KeyError`:** `registry.get(name)` бросает `ProviderNotRegisteredError(ConfigError)` с текстом «доступны: …» (закрывает EID-1). `get_active(config)` использует его же.
- `MockEIDProvider` обёрнут в дескриптор (эталон).

## Вне scope
- Реализация конкретного боевого провайдера — [EID-02](../eid-deferred/STORY-IDS-EID-02-real-eid-providers.md).
- Наполнение `config_spec` валидацией — [EID-04](STORY-IDS-EID-04-provider-owned-config.md); крипто/OIDC слоты — EID-07/EID-08.
- jti replay-cache — **defer** (hardening-бэклог); сессия уже одноразовая (`mark_consumed`).

## Точки в коде (текущее состояние)
- Хардкод реестра: [`providers.py:92`](../../../../src/core/infrastructure/providers.py) (`EIDProviderRegistry({"mock": ...})`).
- Голый `KeyError`: [`registry.py:11-14`](../../../../src/core/providers/registry.py).
- Контракт: [`base.py:32-53`](../../../../src/core/providers/base.py); реэкспорт [`__init__.py`](../../../../src/core/providers/__init__.py).
- DI-сборка: [`service_factory.py`](../../../../src/core/infrastructure/service_factory.py), [`dependencies.py:54-100`](../../../../src/core/api/dependencies.py).
- `ConfigError`: [`schema.py:9`](../../../../src/core/config/schema.py); глобальный handler [`asgi_app.py:141-145`](../../../../src/core/api/asgi_app.py).

## Acceptance Criteria
- [ ] Есть `EIDProviderDescriptor` и `ProviderRuntime`; `mock` собирается через дескриптор.
- [ ] Реестр строится из набора дескрипторов; добавление провайдера не требует правок тела `providers.py`/`registry.py` (только +дескриптор).
- [ ] `EID_PROVIDER=<незарегистрированный>` → `ProviderNotRegisteredError`/`ConfigError` с перечислением доступных, **не** голый `KeyError`; глобальный handler отдаёт чистый ответ.
- [ ] В mock/in-memory режиме сетевые клиенты провайдеров не создаются.
- [ ] Offline-набор зелёный; тест на guard и на сборку реестра.

## Парадигма-якорь
[06-eid-providers](../../../runtime-docs/06-eid-providers.md) (модульность, добавление провайдера), [03-soa-roles](../../../runtime-docs/03-soa-roles.md) (фабрика/DI).
