# 03. Внутреннее устройство: слои и модули identity

## О чём этот документ и что такое «SOA» простыми словами

SOA (service-oriented architecture) здесь — это **не** «много микросервисов». Речь про то, как устроен **сам identity внутри**: он разбит на несколько слоёв-компонентов с чёткими границами и контрактами, где каждый слой отвечает за своё и общается с соседями только через объявленные интерфейсы. Это даёт две вещи: (1) бизнес-логику можно тестировать без поднятия HTTP и без реальной базы; (2) хранилище (память или Supabase) меняется одним переключателем, не трогая остальной код.

Этот документ — про модули **внутри** одного сервиса. Как identity стыкуется с соседними сервисами (gateway, Supabase) — отдельно в [09-gateway-expectations](09-gateway-expectations.md).

Источник: пакеты в [`src/core/`](../../src/core/).

## Поток одного запроса (чтобы увидеть слои в работе)

```
Входящий HTTP-запрос
   │
   ▼
[1] Transport (FastAPI)          ── принять, завернуть ответ в envelope, CORS, ошибки
   │   спрашивает «кто ты?»
   ▼
[2] Security / Auth              ── проверить Bearer-токен → UserClaims
   │
   ▼
[3] DI-контейнер                 ── достать готовые зависимости (один раз на процесс)
   │
   ▼
[4] Service Factory              ── выбрать реализацию под backend (память/Supabase)
   │
   ▼
[5] Domain-контракты             ── вызвать репозиторий/сервис ЧЕРЕЗ интерфейс (Protocol)
   │
   ▼
[6] Persistence                  ── in-memory dict ИЛИ Supabase PostgREST
```

## Модули внутри identity (что за что отвечает)

| Слой | Модуль (пакет) | Роль простыми словами | Ключевой файл | Статус |
|------|----------------|------------------------|---------------|--------|
| 1. Transport | `core.api` | Двери наружу: маршруты, конверт-ответ, CORS, перехват ошибок | [`asgi_app.py`](../../src/core/api/asgi_app.py), [`envelope.py`](../../src/core/api/envelope.py), [`handlers.py`](../../src/core/api/handlers.py) | ✅ |
| 2. Auth/Security | `core.api.security`, `core.auth`, `core.security` | Проверка токена, разбор Supabase JWT, HMAC-хэш персональных данных | [`security.py`](../../src/core/api/security.py), [`auth/supabase_validator.py`](../../src/core/auth/supabase_validator.py), [`security/hashing.py`](../../src/core/security/hashing.py) | ✅ |
| 3. DI-контейнер | `core.api.dependencies` | Собирает все зависимости один раз (singleton через `lru_cache`) и раздаёт хендлерам | [`dependencies.py`](../../src/core/api/dependencies.py) | ✅ |
| 4. Service Factory | `core.application` + `core.infrastructure.providers` | «Сборщик»: по настройке решает, какие реализации подставить | [`application/factory.py`](../../src/core/application/factory.py), [`infrastructure/providers.py`](../../src/core/infrastructure/providers.py), [`infrastructure/service_factory.py`](../../src/core/infrastructure/service_factory.py) | ✅ |
| 5. Domain | `core.domain` | Контракты (интерфейсы) и модели данных — «язык», на котором говорят слои | [`contracts.py`](../../src/core/domain/contracts.py), [`models.py`](../../src/core/domain/models.py) | ✅ |
| 6. Persistence | `core.infrastructure` | Две взаимозаменяемые реализации хранилищ | [`repositories.py`](../../src/core/infrastructure/repositories.py) (память), [`db_supabase.py`](../../src/core/infrastructure/db_supabase.py) (Supabase) | ✅ |
| eID | `core.providers` | Модульные провайдеры eID-верификации (порт + реестр + mock) | [`providers/base.py`](../../src/core/providers/base.py), [`registry.py`](../../src/core/providers/registry.py), [`mock/mock_provider.py`](../../src/core/providers/mock/mock_provider.py) | ✅ mock |
| Config | `core.config` | Чтение настроек из env/.env, профили demo/pilot | [`schema.py`](../../src/core/config/schema.py), [`providers.py`](../../src/core/config/providers.py), [`env_file.py`](../../src/core/config/env_file.py) | ✅ |
| Логи | `core.logging_setup` | Единая настройка логирования (text/json) | [`logging_setup.py`](../../src/core/logging_setup.py) | ✅ |

## Ключевые контракты домена (на чём держатся границы)

В [`contracts.py`](../../src/core/domain/contracts.py) объявлены интерфейсы-`Protocol` (это «обещание методов» без привязки к реализации): репозиторий профилей, хранилище eID-сессий, журнал аудита, реестр OAuth-клиентов, сервис OAuth-токенов, валидатор Supabase JWT, Bearer-auth, healthcheck. Любой слой выше зависит от **этих интерфейсов**, а не от конкретного класса — поэтому in-memory и Supabase-реализации взаимозаменяемы.

## Два хранилища одним переключателем

`provide_service_factory` ([`providers.py:57-89`](../../src/core/infrastructure/providers.py)) смотрит на `DB_BACKEND`:
- `in_memory` → быстрые dict-репозитории (dev/тесты, без сети);
- `supabase` → реальные репозитории поверх PostgREST;
- иначе → ошибка `ValueError` (fail-fast, чтобы не запуститься «наполовину»).

DI-контейнер собирается один раз через `@lru_cache` ([`asgi_app.py:47-57`](../../src/core/api/asgi_app.py)); для тестов есть сброс `_clear_api_dependencies_cache()`.

## Пустые модули-заготовки (честно)

Пустые placeholder-пакеты `core.audit`, `core.oauth`, `core.profiles`, `core.stories` удалены в EPIC-IDS-08 CLEANUP-02/01 ([gap](../analysis/gap-analysis-full-2026-06-04.md)).

## Конфигурационные профили

`AppConfig` ([`config/schema.py`](../../src/core/config/schema.py)) знает два режима ([`schema.py:13-16`](../../src/core/config/schema.py)): **demo** (мягкая валидация, для разработки) и **pilot** (строгая: при отсутствии критичных секретов сервис намеренно не стартует — `ConfigError`). Загрузка — `provide_app_config` ([`config/providers.py`](../../src/core/config/providers.py)) с подмешиванием `.env` (свой минимальный парсер, без сторонней библиотеки).
