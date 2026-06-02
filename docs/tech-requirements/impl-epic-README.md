# Tech Requirements — doge-complaints-gateway

Технические (non-functional) требования к инфраструктурным слоям сервиса.
Каждый документ — самодостаточный эпик, который можно передать агенту в отдельном диалоге для реализации конкретного слоя.

## Порядок выполнения (с учётом зависимостей)

| # | Файл | Слой | Зависит от |
|---|------|------|------------|
| 1 | [impl-epic-01-scaffold-config-launch.md](impl-epic-01-scaffold-config-launch.md) | Scaffold, Config, Launch | — |
| 2 | [impl-epic-02-fastapi-transport.md](impl-epic-02-fastapi-transport.md) | FastAPI Transport Layer | Epic 01 |
| 3 | [impl-epic-03-dependency-injection.md](impl-epic-03-dependency-injection.md) | Dependency Injection | Epic 01, 02 |
| 4 | [impl-epic-04-soa-service-factory.md](impl-epic-04-soa-service-factory.md) | SOA Service Factory | Epic 01, 03 |
| 5 | [impl-epic-05-supabase-persistence.md](impl-epic-05-supabase-persistence.md) | Supabase Persistence | Epic 01, 04 |
| 6 | [impl-epic-06-testing-architecture.md](impl-epic-06-testing-architecture.md) | Testing Architecture | Epic 01–05 |

## Граф зависимостей

```
Epic 01: Scaffold/Config/Launch
    ↓
Epic 02: FastAPI Transport ─────────────────────────┐
    ↓                                                │
Epic 03: Dependency Injection ───────────────────── │
    ↓                                                │
Epic 04: SOA Service Factory                         │
    ↓                                                │
Epic 05: Supabase Persistence                        │
    ↓                                                ↓
Epic 06: Testing Architecture (all layers combined)
```

## Источник паттернов

Каждый эпик основан на верифицированном коде из `docs/runtime-docs/bootstrap-infrastructure/`:

| Эпик | Источник |
|------|---------|
| Epic 01 | `05-env-config-and-launch.md` |
| Epic 02 | `01-fastapi-transport.md` |
| Epic 03 | `02-dependency-injection.md` |
| Epic 04 | `03-soa-service-factory.md` |
| Epic 05 | `04-supabase-persistence.md` |
| Epic 06 | `06-testing-architecture.md` |

## Контекст проекта

- **Проект:** doge-complaints-gateway — Python/FastAPI микросервис
- **Runtime:** Python 3.11, uvicorn, Railway деплой
- **Persistence backends:** `in_memory` (тесты/demo), `sqlite` (локально), `supabase` (prod)
- **Переключение backend:** одна переменная `DB_BACKEND` в `.env`
- **Главный инвариант:** unit/integration тесты никогда не трогают реальный Supabase

## Целевая файловая структура (после выполнения всех эпиков)

```
doge-complaints-gateway/
├── src/
│   └── core/
│       ├── api/
│       │   ├── asgi_app.py          # Epic 02: HTTP transport
│       │   ├── dependencies.py      # Epic 03: DI container
│       │   ├── handlers.py          # Epic 02: request handlers
│       │   ├── envelope.py          # Epic 02: response envelope
│       │   ├── security.py          # Epic 02: auth
│       │   └── idempotency.py       # Epic 02: idempotency
│       ├── config/
│       │   ├── schema.py            # Epic 01: AppConfig dataclass
│       │   ├── env_file.py          # Epic 01: merge_dotenv_from_cwd
│       │   └── providers.py        # Epic 01: provide_app_config
│       ├── domain/
│       │   └── contracts.py        # Epic 04: Protocol interfaces
│       ├── application/
│       │   └── factory.py          # Epic 04: ServiceFactory Protocol
│       └── infrastructure/
│           ├── repositories.py     # Epic 04: InMemory implementations
│           ├── service_factory.py  # Epic 04: DefaultServiceFactory
│           ├── providers.py        # Epic 04: provide_service_factory
│           └── db_supabase.py      # Epic 05: SupabaseDatabase + repos
├── tests/
│   ├── conftest.py                 # Epic 06: autouse fixtures
│   ├── test_*.py                   # Epic 06: domain/service/http tests
│   ├── integration/supabase/       # Epic 06: live_integration tests
│   └── smoke/                      # Epic 06: smoke tests
├── supabase/
│   ├── bootstrap/
│   │   └── 000_full_init.sql       # Epic 05: full schema init
│   └── migrations/                 # Epic 05: incremental migrations
├── pyproject.toml                  # Epic 01: deps, pytest config
├── Makefile                        # Epic 01: serve/dev/check-env
└── railpack.json                   # Epic 01: Railway deploy config
```

## Критические архитектурные решения

| Решение | Обоснование |
|---------|-------------|
| `AppConfig @dataclass(frozen=True)` | Immutable config — нельзя случайно изменить в runtime |
| `@lru_cache(maxsize=1)` для DI | Один singleton на процесс, пересоздаётся только в тестах |
| Protocol-based interfaces | Сервисы не знают о конкретных репозиториях; легко подменить в тестах |
| `_block_dotenv_leakage` autouse fixture | Гарантирует что тесты никогда не попадают в реальный Supabase |
| `service_role` key (не `anon`) | service_role bypasses RLS — нужен для серверных операций |
| `--app-dir src` в uvicorn | Без этого `ModuleNotFoundError: core` |
| `set -a && . ./.env && set +a` | Загрузка `.env` в shell перед uvicorn — единственный способ без python-dotenv |
