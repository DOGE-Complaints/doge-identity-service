# Re-audit EPIC-IDS-05 — закрытие gap'ов по факту кода

> **Дата:** 2026-06-02
> **Методология:** [`analysis.mdc`](../../../../.cursor/rules/analysis.mdc) — только верифицированные факты с путями и строками; код = истина
> **Предмет:** проверка фактического закрытия 6 findings из [`audit-report-2026-05-31.md`](./audit-report-2026-05-31.md) по реальному коду рабочего дерева (ветка `dev`)
> **Базовый аудит:** [`audit-report-2026-05-31.md`](./audit-report-2026-05-31.md) (RG-1 HIGH, S2-1/S3-1 MEDIUM, S1-1/S2-2/S3-2 LOW)

---

## Метод верификации

1. Полностью прочитаны файлы, на которые ссылается базовый аудит: `src/core/infrastructure/db_supabase.py` (659 строк), `src/core/api/dependencies.py`, `src/core/infrastructure/providers.py`, `tests/test_db_supabase_client.py`, `tests/test_epic_ids_04_integration.py`.
2. `grep` по идентификаторам: `falls_back_with_warning`, `InMemoryProfileRepository`, `warning|fallback|TODO EPIC-IDS-05`.
3. Прогон всего теста: `python -m pytest -q` → **154 passed in 0.56s**.

Каждое утверждение ниже привязано к строке кода. Где исправление не найдено в коде — статус ❌.

---

## Сводная таблица

| ID | Severity | Файл:строка (текущий код) | Предложение базового аудита | Статус по коду |
|----|----------|---------------------------|-----------------------------|----------------|
| RG-1 | HIGH | `tests/test_epic_ids_04_integration.py:99–104` | заменить assertion на `SupabaseProfileRepository` | ✅ **ЗАКРЫТ** (альтернативная реализация) |
| S2-1 | MEDIUM | `db_supabase.py:584–592` | docstring у `SupabaseOAuthClientStore` про `del db` | ❌ **ОТКРЫТ** |
| S3-1 | MEDIUM | `dependencies.py:70–73` + `providers.py:74–78` | комментарий про dual-instance `SupabaseDatabase` | ❌ **ОТКРЫТ** |
| S1-1 | LOW | `tests/test_db_supabase_client.py` | тест `from_http(url, "")` | ❌ **ОТКРЫТ** |
| S2-2 | LOW | `db_supabase.py:518–524` | `"status": "eq.started"` guard в `mark_consumed` | ❌ **ОТКРЫТ** |
| S3-2 | LOW | `dependencies.py:70–73` | передать `timeout_s` из config в `health_db` | ❌ **ОТКРЫТ** |

**Итог: закрыт 1 из 6 (только HIGH-блокер CI). Открыто 5: 2 MEDIUM + 3 LOW.**

Этот результат совпадает со статусами в [`bullrun-launch-index.md`](../../bullrun-launch-index.md) §"Gap queue (override-only, audit EPIC-IDS-05 2026-05-31)": RG-1 = `superseded (Story 06)`, S2-1/S3-2/S3-1/S2-2/S1-1 = ⚪ Todo. Расхождения между индексом и кодом нет.

---

## RG-1 [HIGH] — Регрессия теста supabase-fallback — ✅ ЗАКРЫТ

**Что требовалось:** базовый аудит ([`audit-report-2026-05-31.md`](./audit-report-2026-05-31.md) §RG-1, строки 309–344) зафиксировал, что после EPIC-IDS-05 ветка `db_backend=supabase` в `provide_service_factory` перестала быть InMemory-fallback'ом и теперь возвращает реальные Supabase-репозитории. Старый тест `test_provide_service_factory_supabase_falls_back_with_warning` ожидал `InMemoryProfileRepository` + warning в логе → падал на CI (severity HIGH).

**Факт по коду:** старый тест **удалён**, а не переписан под `SupabaseProfileRepository`, как предлагал аудит. Вместо него — `tests/test_epic_ids_04_integration.py:99–104`:

```python
def test_provide_service_factory_supabase_missing_creds_raises_value_error() -> None:
    """EPIC-IDS-05 replaces EPIC-IDS-04 InMemory fallback (see EPIC-IDS-06 L316)."""
    config = provide_app_config(_SUPABASE_ENV)
    broken = AppConfig(**{**config.__dict__, "supabase_url": ""})
    with pytest.raises(ValueError, match="SUPABASE_URL and SUPABASE_SERVICE_ROLE"):
        provide_service_factory(broken)
```

**Подтверждения:**
- `grep "falls_back_with_warning"` по `tests/` и `src/` → 0 совпадений (тест не существует ни в одном виде).
- `src/core/infrastructure/providers.py:70–73` — ветка supabase бросает `ValueError`, без InMemory-fallback и без `logger.warning`:
  ```python
  elif resolved_config.db_backend == "supabase":
      if not resolved_config.supabase_url or not resolved_config.supabase_service_role:
          raise ValueError(
              "DB_BACKEND=supabase requires SUPABASE_URL and SUPABASE_SERVICE_ROLE"
          )
  ```
- `grep "warning|fallback"` по `providers.py` → единственное совпадение `fallback_config=resolved_config` (параметр `SupabaseOAuthClientStore`, не относится к fallback-логике).
- Полный прогон: **154 passed** — теста, блокирующего CI, больше нет.

**Оценка способа закрытия:** альтернатива корректна и даже строже предложения аудита. Предложенный вариант (assert `SupabaseProfileRepository`) на самом деле потребовал бы реального инстанцирования Supabase-репозитория в юнит-тесте; выбранный вариант проверяет fail-fast контракт без сетевой зависимости. Регрессии нет. **Закрыт.**

---

## S2-1 [MEDIUM] — `SupabaseOAuthClientStore` отбрасывает `db` без документации — ❌ ОТКРЫТ

**Что требовалось:** добавить docstring классу `SupabaseOAuthClientStore`, объясняющий, что параметр `db` принимается для единообразия сигнатуры с остальными Supabase-репозиториями, но не используется (OAuth-клиенты грузятся из `fallback_config` env, не из БД-таблицы; см. §9 Open Questions эпика).

**Факт по коду** (`db_supabase.py:584–607`):

```python
class SupabaseOAuthClientStore:
    def __init__(
        self,
        db: SupabaseDatabase,
        *,
        fallback_config: AppConfig | None = None,
        clients: dict[str, OAuthClient] | None = None,
    ) -> None:
        del db
        if clients is not None:
            self._clients = clients
        elif fallback_config is not None:
            client = OAuthClient(...)
            self._clients = {client.client_id: client}
        else:
            self._clients = {}
```

- Docstring у класса **отсутствует** (строка 584 — сразу `class ...:` без `"""`).
- `del db` на строке 592 — без поясняющего комментария.

**Почему важно (MEDIUM):** разработчик, ожидающий, что при `DB_BACKEND=supabase` OAuth-клиенты читаются из БД, получит неожиданное поведение — они всегда берутся из env через `fallback_config`. Поведение нигде в коде не задокументировано. Тест `test_supabase_repositories_satisfy_protocols` передаёт `clients={}` явно, маскируя факт игнорирования `db`.

**Контракт-расхождение:** остальные 5 Supabase-классов (`SupabaseProfileRepository`, `...VerificationSessionStore`, `...EIDAuditLogRepository`, `...StoryDraftRepository`, `...HealthRepository`) реально используют `self._db` (см. `db_supabase.py:382–658`). `SupabaseOAuthClientStore` — единственный, кто принимает, но игнорирует `db`. Это и есть «Contract Violation» по терминологии analysis.mdc, не зафиксированный документально.

**Как закрыть (без изменения поведения):** docstring + комментарий у `del db` (вариант из базового аудита, строки 93–105). Альтернатива — убрать параметр `db` из сигнатуры, но это сломало бы единообразие вызова в `providers.py:83–86` и потребовало бы спец-кейса в фабрике → не рекомендуется в этой волне.

**Validation:** наличие docstring у класса; `inspect.getdoc(SupabaseOAuthClientStore)` непустой.

---

## S3-1 [MEDIUM] — Два независимых `SupabaseDatabase` на старте — ❌ ОТКРЫТ

**Что требовалось:** задокументировать комментарием в `dependencies.py`, что `health_db` (startup probe) и `supabase_db` (репозитории) — два отдельных HTTP-клиента; либо передавать единый инстанс (рефактор, отнесён к scope IDS-06).

**Факт по коду — два места создания `SupabaseDatabase`:**

`dependencies.py:70–73` (для healthcheck'ов):
```python
elif db_backend == "supabase":
    health_db = SupabaseDatabase.from_http(
        config.supabase_url,
        config.supabase_service_role,
    )
    db_checks = {
        "connectivity": health_db.healthcheck(),
        "schema": health_db.required_tables_ready(),
        "columns": health_db.required_columns_ready(),
        "provider_state": health_db.provider_state_ready(),
        "policy_probe": health_db.service_role_policy_probe(),
    }
```

`providers.py:74–78` (для репозиториев, отдельный объект):
```python
supabase_db = SupabaseDatabase.from_http(
    supabase_url=resolved_config.supabase_url,
    service_role_key=resolved_config.supabase_service_role,
    timeout_s=float(resolved_config.request_timeout_s or 15),
)
```

- В `dependencies.py:70–73` **нет комментария** про dual-instance.
- При `DB_BACKEND=supabase` на старте процесса (`build_api_dependencies` через `lru_cache`) выполняется: `health_db` делает **6 HTTP-запросов** — `healthcheck` (1) + `required_tables_ready` (4 таблицы, `db_supabase.py:315–332`) + `required_columns_ready` (1) + `provider_state_ready` (1) + `service_role_policy_probe` (POST+DELETE = 2). Итого ≈ 9 запросов одним клиентом, который дальше нигде не используется.
- `SupabaseHealthRepository` в фабрике (`providers.py:79`) оборачивает **другой** объект — `supabase_db`, не `health_db`. То есть `/ready` (`deps.db_checks`) отражает результат стартового `health_db`, а `SupabaseHealthRepository.ping()` (`db_supabase.py:657–658`) ходит через `supabase_db`.

**Почему важно (MEDIUM):** концептуально два разных объекта мониторят одну БД; лишние HTTP-соединения при старте; источник `db_checks` и источник runtime-`ping()` различаются. Функционального бага нет (оба читают одну БД с одним service_role), но это архитектурное рассогласование без документации → риск неверных допущений при доработке.

**Как закрыть:** минимально — комментарий в `dependencies.py:70` (вариант аудита, строки 189–194). Полноценно — пробросить единый `SupabaseDatabase` из фабрики в `build_api_dependencies` (рефактор сигнатуры `provide_service_factory`/`build_api_dependencies`); базовый аудит явно относит это к scope **EPIC-IDS-06**.

**Validation:** наличие комментария-маркера в `dependencies.py` ИЛИ единый инстанс (тогда `id(health_db) == id(factory._db)` — недостижимо при текущей сигнатуре).

---

## S1-1 [LOW] — Нет теста на пустой `service_role_key` — ❌ ОТКРЫТ

**Что требовалось:** добавить `test_from_http_empty_service_role_key_raises_value_error` в `tests/test_db_supabase_client.py`.

**Факт по коду:** сама валидация в продукте есть и работает (`db_supabase.py:252–253`):
```python
if not service_role_key:
    raise ValueError("service_role_key is required")
```

Но в `tests/test_db_supabase_client.py` (67 строк, прочитан полностью) присутствует только покрытие пустого URL — `test_from_http_empty_url_raises_value_error` (строки 15–17). Теста на пустой `service_role_key` **нет**.

**Почему важно (LOW):** недопокрытие — ветка `db_supabase.py:252–253` не защищена регрессионным тестом. Severity LOW, т.к. логика реализована корректно; риск только в будущей регрессии.

**Как закрыть:**
```python
def test_from_http_empty_service_role_key_raises_value_error() -> None:
    with pytest.raises(ValueError, match="service_role_key is required"):
        SupabaseDatabase.from_http(SUPABASE_URL, "")
```

**Validation:** тест существует и проходит; `pytest -k empty_service_role_key` → 1 passed.

---

## S2-2 [LOW] — `mark_consumed` перезаписывает `failed`/`expired` — ❌ ОТКРЫТ

**Что требовалось:** добавить guard `"status": "eq.started"` в params PATCH-запроса `mark_consumed`, чтобы перевод в `consumed` применялся только к активным сессиям.

**Факт по коду** (`db_supabase.py:518–524`):
```python
def mark_consumed(self, session_id: str) -> None:
    self._db._request(
        method="PATCH",
        path="/rest/v1/eid_verification_sessions",
        params={"id": f"eq.{session_id}"},
        json_body={"status": "consumed"},
    )
```

PATCH выполняется **безусловно** по `id` — guard'а по статусу нет.

**Кросс-проверка с соседними методами того же класса:**
- `get_by_state` (`db_supabase.py:505–516`) — уже использует `"status": "eq.started"` (паттерн в коде существует, его можно переиспользовать).
- `expire_pending` (`db_supabase.py:534–547`) — использует `"status": "eq.started"` в params.
- `mark_failed` (`db_supabase.py:526–532`) — тоже без guard'а (аналогичная, но не зафиксированная в аудите проблема — см. примечание ниже).
- InMemory-аналог `repositories.py:158–166` имеет частичный guard (`if session.status == "consumed": return`), но тоже не защищает от перезаписи `failed`/`expired`.

**Почему важно (LOW):** при гонке или ошибке в flow вызов `mark_consumed` после `mark_failed`/`expire_pending` перезапишет терминальный статус в `consumed` → некорректное состояние в БД и в аудите. LOW, т.к. orchestrator eID-flow ещё не реализован (endpoint'ы `/auth/eid/*` — заглушки 501, см. `handlers.py:54–65`), и реальных вызовов в проде пока нет.

**Как закрыть:**
```python
params={"id": f"eq.{session_id}", "status": "eq.started"},
```
+ тест, проверяющий, что params содержат `status=eq.started`.

**Примечание (вне scope базового аудита):** `mark_failed` (`db_supabase.py:526–532`) обладает тем же свойством безусловной перезаписи. Базовый аудит его не отметил; формально это не «не закрытый gap», а потенциально новый. Фиксирую как наблюдение, не как gap EPIC-IDS-05.

**Validation:** params `mark_consumed` содержат `"status": "eq.started"`; новый тест проходит.

---

## S3-2 [LOW] — `health_db` игнорирует `config.request_timeout_s` — ❌ ОТКРЫТ

**Что требовалось:** передать `timeout_s=float(config.request_timeout_s or 15)` при создании `health_db`.

**Факт по коду** (`dependencies.py:70–73`):
```python
health_db = SupabaseDatabase.from_http(
    config.supabase_url,
    config.supabase_service_role,
)
```
Параметр `timeout_s` не передан → используется default `15.0` (`db_supabase.py:241` и `:248` — `timeout_s: float = 15.0`).

**Рассогласование подтверждено кросс-ссылкой:** `providers.py:77` создаёт `supabase_db` с `timeout_s=float(resolved_config.request_timeout_s or 15)`. Следовательно при `REQUEST_TIMEOUT_S=30` в `.env`:
- `supabase_db` (репозитории) → timeout 30s;
- `health_db` (стартовые проверки) → timeout 15s.

`request_timeout_s` реально читается из env (`schema.py:137`: `request_timeout_s=_int(env, "REQUEST_TIMEOUT_S", "15")`), т.е. конфиг-значение существует и применяется только в одном из двух мест.

**Почему важно (LOW):** при кастомном `REQUEST_TIMEOUT_S` стартовые healthcheck'и используют не тот таймаут, что репозитории. Severity LOW — затрагивает только окно startup-проверок; дефолтные значения совпадают (15 = 15), расхождение проявляется лишь при переопределении env.

**Как закрыть:**
```python
health_db = SupabaseDatabase.from_http(
    config.supabase_url,
    config.supabase_service_role,
    timeout_s=float(config.request_timeout_s or 15),
)
```

**Validation:** `health_db.timeout_s == config.request_timeout_s` при заданном `REQUEST_TIMEOUT_S`.

**Связь с S3-1:** оба finding'а указывают на одну точку (`dependencies.py:70–73`). Объединённый рефактор (единый `SupabaseDatabase` из фабрики) закрыл бы S3-1 и S3-2 одновременно — таймаут наследовался бы от `supabase_db`. Это аргумент в пользу переноса обоих в EPIC-IDS-06.

---

## Приоритет закрытия оставшихся 5

| Приоритет | ID | Severity | Объём | Где |
|-----------|-----|----------|-------|-----|
| 1 | S2-1 | MEDIUM | docstring + 1 комментарий | `db_supabase.py:584,592` |
| 2 | S3-1 | MEDIUM | 1 комментарий (или рефактор → IDS-06) | `dependencies.py:70` |
| 3 | S2-2 | LOW | +1 ключ в params + тест | `db_supabase.py:522` |
| 4 | S3-2 | LOW | +1 аргумент | `dependencies.py:70–73` |
| 5 | S1-1 | LOW | +1 тест | `test_db_supabase_client.py` |

**Группировка для эффективного закрытия:**
- Файл `db_supabase.py`: S2-1 (docstring) + S2-2 (params guard) — один заход.
- Файл `dependencies.py`: S3-1 (комментарий) + S3-2 (timeout) — один заход; либо оба отложить в IDS-06 как единый рефактор dual-instance.
- Файл `test_db_supabase_client.py`: S1-1 (один тест).

Все 5 — локальные, без изменения публичных контрактов; функциональный риск минимален (1× MEDIUM-дизайн, 1× MEDIUM-документация, 3× LOW). После правок обязателен повторный прогон `pytest` (текущий baseline: **154 passed**).

---

## Quality gate (analysis.mdc)

- [x] Все утверждения привязаны к строкам реального кода.
- [x] Нет допущений — где исправление не найдено, статус ❌ с цитатой текущего кода.
- [x] Примеры реальны и взяты из кодовой базы.
- [x] Кросс-ссылки проверены (`providers.py` ↔ `dependencies.py` ↔ `db_supabase.py`, соседние методы класса).
- [x] Расхождение «код vs индекс» проверено — расхождений нет.
- [x] Прогон тестов выполнен: 154 passed.
