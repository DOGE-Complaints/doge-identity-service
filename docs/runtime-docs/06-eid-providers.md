# 06. eID-верификация и сменные провайдеры

## О чём этот документ

eID — это подтверждение, что за аккаунтом стоит **реальный, уникальный человек** (через эстонский Smart-ID / Mobile-ID / ID-карту). Поставщиков такой проверки несколько (Authentigate, eID Easy), и завтра может появиться ещё. Чтобы не переписывать сервис под каждого, identity устроен так: есть **единый «разъём» (порт)**, в который можно вставить любого провайдера, и **реестр**, который выбирает активного по настройке. Этот документ — про то, как этот разъём устроен и как добавить нового провайдера.

Источник: [`src/core/providers/`](../../src/core/providers/), конфиг — [`schema.py`](../../src/core/config/schema.py).

## «Разъём» провайдера (порт) ✅

`EIDProviderPort` ([`base.py:32-53`](../../src/core/providers/base.py)) — это интерфейс-обещание: любой провайдер обязан уметь четыре вещи:

- сказать своё имя (`provider_name`) и путь callback'а (`callback_path`);
- `start_flow(...)` — начать проверку: создать сессию и вернуть, куда редиректить пользователя (`EIDStartResult`);
- `handle_callback(...)` — обработать возврат от провайдера и вернуть результат проверки (`EIDVerificationResult`: страна, `subject_hash`, метод, время).

Если что-то идёт не так — провайдер бросает `EIDProviderError` с каноническим кодом `EidErrorCode` (см. ниже).

## Каноническая идентичность (F12) ✅

`EIDVerificationResult.subject_hash` — **provider-agnostic** стабильный идентификатор человека (нормализованный digest, **без префикса имени провайдера**). Поле `provider` — только provenance (кто провёл проверку); в identity-хэш **не входит**.

Оркестратор считает anti-Sybil хэш:

```text
verified_person_hash = hash_secret(f"{country}:{subject_hash}", key=eid_secret)
```

([`handlers.py:304-307`](../../src/core/api/handlers.py))

Один и тот же человек через разных провайдеров при одинаковых `country` + `subject_hash` даёт **одинаковый** `verified_person_hash`.

## Коды ошибок провайдера (`EidErrorCode`) ✅

Канонический enum в [`base.py`](../../src/core/providers/base.py): `USER_CANCELLED`, `STATE_MISMATCH`, `TOKEN_EXCHANGE_FAILED`, `IDENTITY_VALIDATION_FAILED`, `MISSING_REQUIRED_CLAIM`, `COUNTRY_NOT_ALLOWED`, `METHOD_NOT_ALLOWED`, `PROVIDER_UNAVAILABLE`, `UNKNOWN`.

Провайдер мапит вендор-коды в этот enum и бросает `EIDProviderError(code=EidErrorCode.X)`. Оркестратор сохраняет `e.code.value` в audit `failure_reason`; неожиданные исключения → `UNKNOWN`.

## Реестр и выбор активного ✅

`EIDProviderRegistry` ([`registry.py`](../../src/core/providers/registry.py)): `get(name)` возвращает провайдера или бросает `ProviderNotRegisteredError` (`ConfigError`, не `KeyError`); `get_active(config)` — активный по `EID_PROVIDER`.

Реестр собирается лениво через `build_registry` ([`registry_builder.py:27-40`](../../src/core/providers/registry_builder.py)) из каталога дескрипторов `ALL_EID_PROVIDER_DESCRIPTORS` (mock, eideasy, authentigate). Фабрика DI: [`providers.py:92-96`](../../src/core/infrastructure/providers.py) — `build_provider_runtime` → `build_registry`.

При `EID_PROVIDER=authentigate`/`eideasy` без реализации runtime-провайдера (EID-02) `get_active()` получит stub, который бросает `ProviderNotRegisteredError` с понятным текстом — не голый `KeyError`.

## Какие провайдеры есть

| Провайдер | Статус | Где |
|-----------|--------|-----|
| `mock` | ✅ runtime работает | [`mock/descriptor.py`](../../src/core/providers/mock/descriptor.py), [`mock/mock_provider.py`](../../src/core/providers/mock/mock_provider.py) |
| `eideasy` | 🟡 descriptor + `config_spec`; runtime stub (EID-02) | [`eideasy/descriptor.py`](../../src/core/providers/eideasy/descriptor.py), [`eideasy/config.py`](../../src/core/providers/eideasy/config.py) |
| `authentigate` | 🟡 descriptor + `config_spec`; runtime stub (EID-02) | [`authentigate/descriptor.py`](../../src/core/providers/authentigate/descriptor.py), [`authentigate/config.py`](../../src/core/providers/authentigate/config.py) |

Членство `EID_PROVIDER` и required-поля валидируются через `descriptor.config_spec.validate` ([`schema.py:88-93,118`](../../src/core/config/schema.py)); список имён — из `registered_eid_provider_names()` ([`registry_builder.py`](../../src/core/providers/registry_builder.py)).

## Как работает mock (чтобы понять контракт на примере) ✅

[`mock_provider.py`](../../src/core/providers/mock/mock_provider.py): `provider_name="mock"`, `callback_path="/auth/mock/callback"`.
- `start_flow` — создаёт сессию (статус `started`, живёт 10 минут, случайный `state`), кладёт её в хранилище сессий и возвращает redirect на свой callback с `session_id`.
- `handle_callback` — отдаёт фиктивный результат (страна EE, provider-agnostic `subject_hash` без префикса `mock-`). Удобно гонять весь флоу офлайн, без реального ID.

## Как добавить настоящего провайдера

1. Написать класс по контракту `EIDProviderPort` (4 метода выше).
2. Добавить `EIDProviderDescriptor` в `ALL_EID_PROVIDER_DESCRIPTORS` ([`registry_builder.py:10-14`](../../src/core/providers/registry_builder.py)) с `config_spec` и `build(runtime)` — **без** правок hardcode-словаря в `providers.py`.
3. Колонки `provider`/`provider_session_data` в таблице сессий под это уже готовы (миграция `20260526000001`).
4. Callback — **один** параметризованный маршрут `GET /auth/{provider}/callback` ([`asgi_app.py`](../../src/core/api/asgi_app.py)); новый провайдер не требует нового роута. Незарегистрированный `provider` → `ProviderNotRegisteredError` (`ConfigError`).

## Браузерный callback и SPA-first redirect ✅

Живой eID-флоу (full-page redirect):

1. UI вызывает `POST /auth/eid/start` с `return_url` из allowlist.
2. Пользователь уходит к провайдеру; провайдер редиректит браузер на `GET /auth/{provider}/callback?...`.
3. Identity завершает оркестрацию (`handle_auth_eid_callback` → `EidCallbackOutcome`) и по умолчанию отвечает **`303 See Other`** на сохранённый `return_url` с маркерами:
   - успех: `?eid_status=verified`
   - ошибка провайдера: `?eid_status=error&eid_error=<EidErrorCode>`
4. Если сессия/`return_url` неизвестны — **безопасный 400 JSON** без redirect (open-redirect guard).
5. Для offline-тестов и API-клиентов: `Accept: application/json` → JSON envelope (как раньше).

Рендер: [`eid_callback.py`](../../src/core/api/eid_callback.py), [`asgi_app.py`](../../src/core/api/asgi_app.py) (`_render_eid_callback_outcome`).

## Текущее состояние целиком

Инфраструктура и mock-флоу работают: `POST /auth/eid/start`, динамический callback, redirect в SPA, audit, профиль. Реальные runtime-провайдеры eideasy/authentigate — EID-02.
