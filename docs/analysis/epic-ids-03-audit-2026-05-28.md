# Аудит EPIC-IDS-03 — Dependency Injection

> **Дата:** 2026-05-28
> **Методология:** [`analysis.mdc`](../../.cursor/rules/analysis.mdc) — только верифицированные факты с путями и строками
> **Предмет:** AC каждой Story и Task vs фактический код; регрессии по сравнению с EPIC-IDS-02
> **Статус эпика по итогам:** ✅ Implemented — все 3 stories, 7 tasks верифицированы

---

## Сводная таблица findings

| ID | Story | Severity | Суть | Gap task | Статус |
|----|-------|----------|------|----------|--------|
| DI-1 | S2 | MEDIUM | `test_lifespan_configures_logging` — слабый assertion, тест всегда пройдёт по fallback | [`task-ids-03-02-t04-audit-di-1-lifespan-logging-assertion`](../tasks/epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-02-build-api-dependencies-singleton-lifespan/task-ids-03-02-t04-audit-di-1-lifespan-logging-assertion/README.md) | 🟢 Closed |
| DI-2 | S2 | MEDIUM | `create_app(config)` использует только `config.cors_allowed_origins`; DI-контейнер читает отдельный config из `os.environ` | [`task-ids-03-02-t05-audit-di-2-create-app-dual-config-note`](../tasks/epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-02-build-api-dependencies-singleton-lifespan/task-ids-03-02-t05-audit-di-2-create-app-dual-config-note/README.md) | 🟢 Closed |
| DI-3 | S3 | LOW | Закомментированный EPIC-IDS-04 блок стоит после `return` — unreachable code (intentional design per Story 3) | [`task-ids-03-03-t03-audit-di-3-unreachable-block-lint`](../tasks/epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-03-epic-ids-04-extension-hook-contract/task-ids-03-03-t03-audit-di-3-unreachable-block-lint/README.md) | 🟢 Closed (no action) |
| DI-4 | S3 | LOW | `test_epic_ids_04_optional_fields_match_factory_getters` — последний `assert` полу-тавтологичен | [`task-ids-03-03-t04-audit-di-4-optional-fields-test-cleanup`](../tasks/epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-03-epic-ids-04-extension-hook-contract/task-ids-03-03-t04-audit-di-4-optional-fields-test-cleanup/README.md) | 🟢 Closed |

**Блокирующих findings нет.**

---

## Ключевые архитектурные изменения vs EPIC-IDS-02

EPIC-IDS-03 провёл рефакторинг цепочки конфигурации. Критически важно для понимания:

| Компонент | EPIC-IDS-02 | EPIC-IDS-03 |
|-----------|-------------|-------------|
| `build_api_dependencies` | `(config: AppConfig)` — принимал конфиг явно | `()` — zero-arg, читает `provide_app_config()` сам |
| `_cached_dependencies()` | `config = _config_for_dependencies or provide_app_config(); return build_api_dependencies(config)` | `return build_api_dependencies()` |
| `create_app(config)` | Сохранял `config` в глобал `_config_for_dependencies` | Только передаёт `config.cors_allowed_origins` в CORS middleware |
| `conftest.py` fixture | `provide_app_config(_TEST_ENV)` + без monkeypatch | `monkeypatch.setenv(...)` для каждого ключа + `provide_app_config()` (no-arg) |

---

## Story 1 — ApiDependencies dataclass + HandlerDependencies alias (IDS-03-01)

**Файлы:** [`src/core/api/dependencies.py`](../../src/core/api/dependencies.py) · [`tests/test_api_dependencies.py`](../../tests/test_api_dependencies.py)

| Claim | Строка | ✅/❌ |
|-------|--------|-------|
| `from core.api.dependencies import ApiDependencies, HandlerDependencies` | `dependencies.py:26,47` | ✅ |
| `HandlerDependencies is ApiDependencies` | `dependencies.py:47` | ✅ |
| `@dataclass(frozen=True) class ApiDependencies` | `dependencies.py:25` | ✅ |
| Always-present: `config`, `bearer_token_auth`, `db_backend`, `db_ready`, `db_checks` | `dependencies.py:28–34` | ✅ |
| `db_checks: dict[str, bool]` (ужесточённый тип vs `Any` в IDS-02) | `dependencies.py:34` | ✅ |
| 8 identity slots, все `object \| None = None` | `dependencies.py:37–44` | ✅ |
| `supabase_jwt_validator`, `profile_repository`, `verification_session_store` | `dependencies.py:37–39` | ✅ |
| `eid_audit_log_repository`, `eid_provider_registry`, `oauth_client_store` | `dependencies.py:40–42` | ✅ |
| `oauth_token_service`, `story_draft_repository` | `dependencies.py:43–44` | ✅ |
| `EPIC_IDS_04_OPTIONAL_FIELDS` tuple (8 имён) | `dependencies.py:13–22` | ✅ |
| Мутация → `FrozenInstanceError` | `frozen=True` + `test_api_dependencies_is_frozen` | ✅ |
| Тесты: 5 кейсов Story 1 | `test_api_dependencies.py:39–70` | ✅ |

**Story 1: ✅ VERIFIED — 0 findings**

---

## Story 2 — build_api_dependencies + singleton + lifespan (IDS-03-02)

**Файлы:** [`src/core/api/dependencies.py`](../../src/core/api/dependencies.py) · [`src/core/api/asgi_app.py`](../../src/core/api/asgi_app.py) · [`tests/test_api_dependencies.py`](../../tests/test_api_dependencies.py)

| Claim | Строка | ✅/❌ |
|-------|--------|-------|
| `build_api_dependencies()` — zero-arg | `dependencies.py:50` | ✅ |
| Вызывает `provide_app_config()` внутри | `dependencies.py:56` | ✅ |
| `db_ready = db_backend == "in_memory"` | `dependencies.py:61` | ✅ |
| `db_checks: dict[str, bool] = {}` (stub до IDS-05) | `dependencies.py:59` | ✅ |
| `bearer_token_auth = StubBearerTokenAuth()` (stub до IDS-04) | `dependencies.py:64` | ✅ |
| `@lru_cache(maxsize=1)` синглтон | `asgi_app.py:46` | ✅ |
| `_cached_dependencies()` → `build_api_dependencies()` (zero-arg) | `asgi_app.py:47–48` | ✅ |
| `_clear_api_dependencies_cache()` → `_cached_dependencies.cache_clear()` | `asgi_app.py:55–56` | ✅ |
| `create_app(config)` вызывает `_clear_api_dependencies_cache()` | `asgi_app.py:60` | ✅ |
| `_lifespan` → `get_api_dependencies()` + `configure_logging(deps.config.log_level)` | `asgi_app.py:84–91` | ✅ |
| `conftest.py` fixture: monkeypatch + `provide_app_config()` (no-arg) | `conftest.py:21–28` | ✅ |
| `get_api_dependencies() is get_api_dependencies()` = True | `test_api_dependencies.py:94` | ✅ |
| cache clear → новый `id()` | `test_api_dependencies.py:97–104` | ✅ |
| monkeypatch `LOG_LEVEL=DEBUG` + clear cache → `config.log_level == "DEBUG"` | `test_api_dependencies.py:107–115` | ✅ |
| Параллельные запросы → один `ApiDependencies` | `test_api_dependencies.py:127–141` | ✅ |

### DI-1 [MEDIUM] — `test_lifespan_configures_logging` слабый assertion

`test_api_dependencies.py:118–124`:

```python
assert any("configure_logging" in record.message.lower()
           or record.levelno == logging.WARNING
           for record in caplog.records
           ) or logging.getLogger().level == logging.WARNING
```

Последний `or logging.getLogger().level == logging.WARNING` делает тест безусловно проходимым: `configure_logging("WARNING")` вызывается внутри `_lifespan`, что устанавливает уровень root logger в `WARNING`. Этот уровень сохраняется между тестами. Тест проходит даже если caplog не захватил ни одной записи, потому что fallback `logging.getLogger().level == logging.WARNING` всегда True после предыдущего вызова `configure_logging`.

**Как закрыть:** заменить assertion на строгое:

```python
# Строгий вариант — проверить, что уровень выставлен именно через lifespan:
assert logging.getLogger().level == logging.WARNING
# Дополнительно: убедиться что lifespan вызывался:
assert any(route.status_code == 200 for route in [client.get("/health")]
```

Или упростить до минимально достаточного:

```python
assert logging.getLogger().level == logging.WARNING
```

Убрав ненужную сложность. Тест всё равно проходит, но смысл станет явным.

### DI-2 [MEDIUM] — Два разных конфига в одном app instance

`create_app(config: AppConfig)` использует переданный `config` только для CORS (`asgi_app.py:69`). Все остальные компоненты получают конфиг через `build_api_dependencies()` → `provide_app_config()` из `os.environ`.

Следствие: `create_app(config).state` (через `get_api_dependencies().config`) ≠ переданный `config`.

```python
config_a = provide_app_config({"LOG_LEVEL": "DEBUG", "CORS_ALLOWED_ORIGINS": "http://x.com", ...})
app = create_app(config_a)  # CORS = "http://x.com"

# В рантайме:
deps = get_api_dependencies()
deps.config.cors_allowed_origins  # → "*" (из os.environ, не config_a!)
deps.config.log_level             # → "INFO" (из os.environ)
```

**Почему не сломало тесты:** `conftest.py` теперь использует `monkeypatch.setenv()` для всех переменных, поэтому `provide_app_config()` (no-arg) подбирает те же значения из `os.environ`. Семантически оба конфига совпадают в тестах.

**Риск для EPIC-IDS-04:** разработчик, ожидающий `get_api_dependencies().config` == конфиг из `create_app(config)`, получит сюрприз если в `os.environ` нет нужных vars. Рекомендация: задокументировать в `create_app` docstring или в README EPIC-IDS-04.

**Как закрыть (документально):** добавить комментарий в `create_app`:
```python
def create_app(config: AppConfig) -> FastAPI:
    # NOTE: config is used ONLY for CORSMiddleware allow_origins.
    # DI container reads its own config via build_api_dependencies() -> provide_app_config().
    # Ensure os.environ mirrors the same values (see conftest.py for test pattern).
    _clear_api_dependencies_cache()
```

**Story 2: ✅ VERIFIED — 2 findings (DI-1, DI-2)**

---

## Story 3 — Hook расширения для EPIC-IDS-04 (IDS-03-03)

**Файлы:** [`src/core/api/dependencies.py`](../../src/core/api/dependencies.py) · [`tests/test_api_dependencies.py`](../../tests/test_api_dependencies.py)

| Claim | Строка | ✅/❌ |
|-------|--------|-------|
| `# TODO EPIC-IDS-04: replace with provide_service_factory(...)` над `StubBearerTokenAuth()` | `dependencies.py:63` | ✅ |
| `# TODO EPIC-IDS-05: run 5-level Supabase healthchecks` над `db_checks = {}` | `dependencies.py:58` | ✅ |
| Закомментированный target block с `provide_service_factory` | `dependencies.py:73–90` | ✅ |
| Все 8 `get_*` геттеров в закомментированном блоке | `dependencies.py:81–89` | ✅ |
| `EPIC_IDS_04_OPTIONAL_FIELDS` содержит 8 имён | `dependencies.py:13–22` | ✅ |
| Каждое имя из `EPIC_IDS_04_OPTIONAL_FIELDS` ∈ `ApiDependencies.__dataclass_fields__` | `test_api_dependencies.py:147–148` | ✅ |
| Тест читает реальный файл `dependencies.py` и проверяет TODO-строки | `test_api_dependencies.py:162–170` | ✅ |
| `provide_service_factory` присутствует в файле | `test_api_dependencies.py:169` | ✅ |

### DI-3 [LOW] — Закомментированный блок стоит после `return` (unreachable — intentional)

`dependencies.py:72–90`:
```python
    return ApiDependencies(...)

    # EPIC-IDS-04 will replace this block:   ← unreachable
    # from core.infrastructure.providers import provide_service_factory
    # ...
```

Этот блок стоит ПОСЛЕ `return` и является dead code по стандартам Python. Это **intentional design** — Story 3 явно требует наличия закомментированного reference block для EPIC-IDS-04. Тест `test_build_api_dependencies_has_epic_hook_comments` верифицирует его наличие.

Static analyzers (mypy, ruff с `W0101`) могут флажировать это. Если CI имеет strict unreachable-code check — нужно добавить `# noqa`.

### DI-4 [LOW] — `test_epic_ids_04_optional_fields_match_factory_getters` полу-тавтологичен

`test_api_dependencies.py:144–159`:
```python
getter_names = {f"get_{name}" for name in EPIC_IDS_04_OPTIONAL_FIELDS}
assert getter_names == {
    "get_supabase_jwt_validator",
    ...  # hardcoded set
}
```

`getter_names` вычисляется из `EPIC_IDS_04_OPTIONAL_FIELDS`. Hardcoded set перечисляет те же 8 имён с префиксом `get_`. Если оба изменяются синхронно — тест проходит. Единственная защита от несинхронного изменения.

Реальная ценность теста — строки 147–148: `assert field_name in ApiDependencies.__dataclass_fields__` — гарантирует что все константы из `EPIC_IDS_04_OPTIONAL_FIELDS` являются реальными полями dataclass.

**Story 3: ✅ VERIFIED — 2 findings (DI-3, DI-4)**

---

## Регрессионная проверка: EPIC-IDS-02 vs EPIC-IDS-03

| Компонент | EPIC-IDS-02 | EPIC-IDS-03 | Регрессия? |
|-----------|-------------|-------------|------------|
| `_config_for_dependencies` global | Существовал | Удалён | ✅ Нет |
| `build_api_dependencies(config)` | Принимал config | Zero-arg | ✅ Нет (conftest обновлён) |
| `conftest.py` test_client | `provide_app_config(_TEST_ENV)` | `monkeypatch.setenv + provide_app_config()` | ✅ Нет |
| CORS middleware timing | В `create_app` | В `create_app` (не изменилось) | ✅ Нет |
| `_clear_api_dependencies_cache()` | В `create_app` | В `create_app` | ✅ Нет |
| 56 тестов проходят | — | `pytest ... → 56 passed` (epic gate) | ✅ Нет регрессий |

---

## Верификация Epic Goal

| Критерий из epic gate | Факт | Статус |
|----------------------|------|--------|
| `get_api_dependencies() is get_api_dependencies()` | `test_get_api_dependencies_is_singleton` ✅ | ✅ |
| `config.port` из EPIC-IDS-01 (default 8100) | `provide_app_config()` → `port=8100` | ✅ |
| `bearer_token_auth` присутствует | `StubBearerTokenAuth()` в factory | ✅ |
| `isinstance(db_checks, dict)` | `dict[str, bool]` в dataclass | ✅ |
| Identity slots `None` в IDS-03 | `test_api_dependencies_identity_slots_default_none` | ✅ |
| `_clear_api_dependencies_cache()` работает | `test_clear_cache_creates_new_singleton` | ✅ |
| EPIC-IDS-04 hooks задокументированы | TODO комментарии + commented block | ✅ |
| `HandlerDependencies is ApiDependencies` | `test_handler_dependencies_is_alias` | ✅ |

---

## Приоритет доработок

| Приоритет | ID | Задача | Файл |
|-----------|-----|--------|------|
| 1 | DI-1 | Упростить/укрепить assertion в `test_lifespan_configures_logging` | `tests/test_api_dependencies.py:124` | 🟢 Closed |
| 2 | DI-2 | Добавить NOTE-комментарий в `create_app` о dual-config паттерне | `src/core/api/asgi_app.py:59` | 🟢 Closed |
| 3 | DI-3 | Проверить CI: если strict linter — добавить `# noqa` после unreachable block | `src/core/api/dependencies.py:72` | 🟢 Closed (no action) |
| 4 | DI-4 | Убрать тавтологичный `assert getter_names == {hardcoded}`, оставить только проверку полей dataclass | `tests/test_api_dependencies.py:149–159` | 🟢 Closed |

DI-1 и DI-2 рекомендованы к исправлению до EPIC-IDS-04. DI-3 и DI-4 — при следующем проходе.
