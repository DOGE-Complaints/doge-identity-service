# Жёсткий аудит EPIC-IDS-06 — Testing Architecture

> **Дата:** 2026-06-02
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями; verified-state
> **Предмет:** исполнение [`EPIC-IDS-06-testing-architecture.md`](../tasks/epics/EPIC-IDS-06-testing-architecture/EPIC-IDS-06-testing-architecture.md) (5 stories, 15 tasks, pkg-000008) против фактического кода тестов
> **Объём правок:** только findings (severity + направление закрытия). Реализация не предлагается.

---

## Команды верификации (фактически выполнены)

| # | Команда | Результат |
|---|---------|-----------|
| 1 | `pytest -q -m "not live_integration"` | **193 passed, 10 deselected, 1 warning in 3.39s** |
| 2 | `pytest -q -m live_integration` (без creds) | **1 passed, 9 skipped, 193 deselected in 0.10s** |
| 3 | `pytest --collect-only -q` (из `test_smoke_collection_contract`) | smoke не в коллекции — PASS |
| 4 | `DB_BACKEND=supabase SUPABASE_URL=https://prod.local pytest tests/test_bootstrap_smoke.py` | **ConfigError при сборке** (см. F1) |
| 5 | `grep "async def test" tests/` | **0** (см. F5) |

Итого по дереву: 203 теста собрано; offline-инвариант (<30 c) выполнен (3.39 c). Live-набор: 9 skip (нет creds) + 1 passed (auto-marker contract).

---

## Статус Stories/Tasks по факту кода

Все 5 stories и 15 tasks из [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) §"Task queue (EPIC-IDS-06)" помечены 🟢 Done. Проверка по коду подтверждает: каждый целевой файл существует и тесты проходят.

| Story | Целевые файлы (epic §5) | Факт | AC | Статус |
|-------|--------------------------|------|----|--------|
| S1 conftest autouse | `tests/conftest.py` | [conftest.py:24-93](../../tests/conftest.py) — 3 фикстуры: `_block_dotenv_leakage`, `_pytest_session_logging`, `pytest_collection_modifyitems` | §6 S1 ×5 | ✅ verified |
| S2 bootstrap/http/DI smoke | 6 файлов | `test_bootstrap_smoke.py` (6 тестов), `test_http_transport_smoke.py` (8), `test_di_singleton.py` (4), `test_di_service_factory.py` (3), `test_eid_provider_registry.py` (4), `test_supabase_jwt_validator.py` (5) | §6 S2 ×3 | ✅ verified |
| S3 live supabase | 2 файла + conftest | `integration/supabase/test_supabase_dotenv_connectivity.py` (5), `..._identity_roundtrip.py` (4), `conftest.py` helper | §6 S3 ×4 | ✅ verified (skip без creds) |
| S4 CI workflows | 2 YAML | `.github/workflows/test-offline.yml`, `integration-live.yml` + contract `test_ci_workflows_contract.py` | §6 S4 ×4 | ✅ verified |
| S5 live-server smoke | 2 файла | `tests/smoke/conftest.py`, `tests/smoke/test_local_server_smoke.py` (5) + contract `test_smoke_collection_contract.py` | §6 S5 ×3 | ✅ verified |

Доп. контрактные тесты сверх §5 (усиливают AC): `test_conftest_env_isolation.py`, `test_ci_workflows_contract.py`, `test_smoke_collection_contract.py`, `integration/supabase/test_live_integration_auto_marker.py`.

**Вывод:** на уровне задач эпик исполнен — код есть, тесты зелёные. Findings ниже — кросс-срезовые (изоляция, контракты документ↔код, структура), не «задача не сделана».

---

## Findings (severity)

| ID | Severity | Тип | Суть | Файл:строка |
|----|----------|-----|------|-------------|
| F1 | **MEDIUM** | Изоляция | Модульный `provide_app_config()` исполняется при импорте до autouse-фикстуры; epic §8 verify cmd#3 падает на сборке | `asgi_app.py:346-347` |
| F2 | LOW | Doc↔Code | AC S5 заявляет исключение smoke через `testpaths`; реально — `collect_ignore` | `conftest.py:9` vs epic §6 S5 / §8 |
| F3 | LOW | Структура | `tests/integration/__init__.py` и `tests/smoke/__init__.py` из §5 отсутствуют | epic §5 vs дерево |
| F4 | LOW | SSOT | Маркер `smoke` объявлен дважды, с разной формулировкой | `pyproject.toml:38` + `smoke/conftest.py:11-15` |
| F5 | LOW | Dead config | `asyncio_mode=auto` + `pytest-asyncio` + заявленный паттерн ASGITransport — не используются (0 async-тестов) | `pyproject.toml:30,35` vs tests |
| F6 | LOW | Index | Битая ссылка на файл эпика в индексе | `bullrun-launch-index.md:36` |
| O1 | — | Observation | `.github/` и тесты IDS-06 не закоммичены (как и IDS-05) | git status |

Регрессий в offline-наборе нет (193 passed). Блокирующих findings нет.

---

### F1 [MEDIUM] — Изоляция не покрывает import-time оценку конфига

**Факт.** [`asgi_app.py:346-347`](../../src/core/api/asgi_app.py) на уровне модуля:
```python
_config = provide_app_config()
app = create_app(_config)
```
Это исполняется при **импорте** модуля. `tests/conftest.py:12` импортирует `core.api.asgi_app` на этапе сбора (collection), т.е. **до** применения autouse-фикстуры `_block_dotenv_leakage` (фикстуры применяются per-test, не при импорте).

**Доказательство** (команда #4):
```
DB_BACKEND=supabase SUPABASE_URL=https://prod.local pytest tests/test_bootstrap_smoke.py
→ src/core/config/schema.py:108: ConfigError:
  DB_BACKEND=supabase requires SUPABASE_URL and SUPABASE_SERVICE_ROLE
```
С валидными creds (`+SUPABASE_SERVICE_ROLE`) — collection проходит (проверено: 1 passed). То есть epic §8 verification cmd#3 (записан именно как `DB_BACKEND=supabase SUPABASE_URL=https://prod.local …`, без service_role) **не исполним** — крэшит сбор, а не демонстрирует изоляцию.

**Почему MEDIUM.** Security-инвариант про реальный Supabase (§1 эпика) фактически держится: DI ленивый (`build_api_dependencies` зовётся через `get_api_dependencies` в lifespan/handlers, не при импорте), а per-test фикстура сбрасывает env до первого обращения; сетевого контакта при импорте нет. Но: (а) собственная verify-команда эпика §8 #3 сломана; (б) латентная хрупкость — любой запуск в окружении с `DB_BACKEND=supabase` + неполными creds (process env или `.env`) роняет всю коллекцию на этапе импорта, и autouse-фикстура это не предотвращает. Заявление AC S1 «pytest с .env содержащим DB_BACKEND=supabase + реальные creds → тесты используют in_memory» верно только при *полных* creds; при неполных — крэш сбора.

**Направление закрытия (без реализации):** убрать import-time оценку конфига/построение `app` на уровне модуля `asgi_app` (вынести в фабрику/`__main__`), либо привести §8 cmd#3 к исполнимому виду. Решение об уровне (код vs verify-doc) — за владельцем.

---

### F2 [LOW] — Механизм исключения smoke не тот, что в AC

**Факт.** AC S5 (epic §6 Story 5) и §8: *«Smoke тесты НЕ входят в `pytest tests/ -q` (testpaths контролирует это, см. EPIC-IDS-01 pyproject)»*. Реально `testpaths = ["tests"]` ([`pyproject.toml:32`](../../pyproject.toml)) **включает** `tests/smoke`. Исключение обеспечивает [`conftest.py:9`](../../tests/conftest.py) `collect_ignore = ["smoke"]`. Контракт-тест `test_smoke_collection_contract.py` это подтверждает (PASS), но заявленный в AC механизм (`testpaths`) — неверен.

**Почему LOW.** Поведение корректно (smoke исключены), расходится только формулировка причины. Риск — при будущей правке кто-то «починит testpaths» и сломает изоляцию, не зная про `collect_ignore`.

**Направление закрытия:** привести формулировку AC/§8 к фактическому механизму (`collect_ignore`).

---

### F3 [LOW] — Отсутствуют `__init__.py`, перечисленные в §5

**Факт.** Epic §5 «Целевые файлы» перечисляет `tests/integration/__init__.py`, `tests/integration/supabase/__init__.py`, `tests/smoke/__init__.py`. По дереву существует только `tests/integration/supabase/__init__.py`; `tests/integration/__init__.py` и `tests/smoke/__init__.py` **отсутствуют** (проверено `ls`). Импорт `from tests.integration.supabase.conftest import …` ([roundtrip:18](../../tests/integration/supabase/test_supabase_identity_roundtrip.py)) работает за счёт `pythonpath=["src","tests"]` + implicit namespace packages — модули корректно собираются (10 deselected в offline-прогоне = импортированы).

**Почему LOW.** Функционально работает; расхождение со списком целевых файлов §5 (Architectural Drift / spec-vs-reality).

**Направление закрытия:** либо создать недостающие `__init__.py`, либо убрать их из §5 как намеренный namespace-package выбор.

---

### F4 [LOW] — Дублирование маркера `smoke`

**Факт.** Маркер объявлен в двух местах с разной формулировкой:
- [`pyproject.toml:38`](../../pyproject.toml): `"smoke: tests requiring a running identity server (IDENTITY_URL)"`
- [`tests/smoke/conftest.py:11-15`](../../tests/smoke/conftest.py): `pytest_configure` → `addinivalue_line("markers", "smoke: smoke tests against a running identity server (IDENTITY_URL)")`

**Почему LOW.** Нарушение Single Source of Truth; функционально безвредно (pytest не падает на дубль). При расхождении описаний — путаница.

**Направление закрытия:** оставить одно объявление (pyproject как SSOT маркеров) либо синхронизировать тексты.

---

### F5 [LOW] — Неиспользуемая async-конфигурация и расхождение с заявленным паттерном

**Факт.** `grep "async def test" tests/` → **0**; `grep "ASGITransport\|AsyncClient" tests/` → **0**. При этом [`pyproject.toml:30`](../../pyproject.toml) `asyncio_mode = "auto"` + `:35` зависимость `pytest-asyncio>=0.24.0`, а epic §6 S2 «Pattern source» декларирует `httpx.AsyncClient(ASGITransport(app=app))`. Фактически HTTP-слой тестируется синхронным `fastapi.testclient.TestClient` ([conftest.py:10,96-104](../../tests/conftest.py), [test_http_transport_smoke.py:8](../../tests/test_http_transport_smoke.py)).

**Почему LOW.** No-network инвариант держится (TestClient — in-process ASGI). Но: `pytest-asyncio`/`asyncio_mode` — мёртвая конфигурация (Legacy Accumulation), а реализация отклоняется от документированного паттерна §6 S2.

**Направление закрытия:** либо удалить неиспользуемую async-конфигурацию/зависимость, либо обновить §6 S2 на фактический `TestClient`-паттерн.

---

### F6 [LOW] — Битая ссылка на файл эпика в индексе

**Факт.** [`bullrun-launch-index.md:36`](../tasks/bullrun-launch-index.md) ссылается на `./epics/EPIC-IDS-06-testing-architecture.md`, но файл лежит в подкаталоге: `./epics/EPIC-IDS-06-testing-architecture/EPIC-IDS-06-testing-architecture.md` (проверено `ls` — целевой путь не существует). Остальные строки индекса (task queue, stories) ссылаются корректно с подкаталогом.

**Почему LOW.** Навигационная ошибка индекса.

**Направление закрытия:** исправить путь (актуализировано в этом проходе — см. ниже).

---

### O1 [Observation] — IDS-06 не закоммичен

`git status` показывает `.github/` и тесты IDS-06 как untracked/modified (ветка `dev`), как и весь IDS-05. Не дефект кода; зафиксировано для consistency — runtime-артефакты эпика существуют только в рабочем дереве.

---

## Регрессионная проверка (IDS-01..05 vs IDS-06)

| Аспект | Проверка | Результат |
|--------|----------|-----------|
| Старые тесты не сломаны | offline-прогон | 193 passed (включает test_db_supabase_*, test_epic_ids_04/05_*) |
| `test_factory_*` переключён под IDS-05 | [test_di_service_factory.py:30-36](../../tests/test_di_service_factory.py) | `test_factory_raises_without_supabase_creds` (raise ValueError) — соответствует §9 эпика |
| `_block_dotenv_leakage` не ломает per-test override | [test_conftest_env_isolation.py:33-35](../../tests/test_conftest_env_isolation.py) | PASS |
| live auto-marker без декоратора | [test_live_integration_auto_marker.py](../../tests/integration/supabase/test_live_integration_auto_marker.py) | PASS (1 live passed) |

Регрессий не выявлено.

---

## Актуализация индекса (выполнено в этом проходе)

[`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): Task queue (EPIC-IDS-06, 15 строк) и Stories (EPIC-IDS-06, 5 строк) уже присутствовали с верным статусом 🟢 Done — подтверждено по коду, не менялись. Внесено: (1) исправлена битая ссылка F6 (строка 36); (2) registry-ячейка Decompose обновлена с «P2/P3» на фактическое «5/5 stories Done + audit 2026-06-02»; (3) «Рекомендуемый next» обновлён (audit выполнен); (4) добавлена секция «Gap queue (EPIC-IDS-06 audit 2026-06-02)» со ссылкой на этот отчёт.

---

## Quality gate (analysis.mdc)

- [x] Все claims привязаны к путям/строкам реального кода.
- [x] Findings выполнены фактическими командами (не предположения); результаты приведены.
- [x] Severity проставлена; регрессии проверены отдельно (нет).
- [x] Реализация не предлагалась — только направление закрытия.
- [x] Расхождения spec↔code зафиксированы, не скрыты (F1–F6).
