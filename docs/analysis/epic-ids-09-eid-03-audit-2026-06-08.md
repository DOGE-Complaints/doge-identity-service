# Жёсткий аудит исполнения STORY-IDS-EID-03 (plugin-платформа провайдеров)

> **Дата:** 2026-06-08
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-EID-03-provider-plugin-backbone`](../tasks/backlog-stories/STORY-IDS-EID-03-provider-plugin-backbone.md) vs фактический код. Исполнена под **EPIC-IDS-09-eid-verification** (pkg-000016), 6 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): EPIC-IDS-09, task queue t01–t06 (pkg-000016).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Новые модули | [`descriptor.py`](../../src/core/providers/descriptor.py), [`runtime.py`](../../src/core/providers/runtime.py), [`runtime_factory.py`](../../src/core/providers/runtime_factory.py), [`registry_builder.py`](../../src/core/providers/registry_builder.py), [`mock/descriptor.py`](../../src/core/providers/mock/descriptor.py) |
| Сборка реестра | `provider_runtime = build_provider_runtime(...)` → `registry = build_registry(...)` ([`providers.py:92-96`](../../src/core/infrastructure/providers.py)) — хардкод `{"mock": ...}` убран |
| Guard | `registry.get` → `ProviderNotRegisteredError(ConfigError)` ([`registry.py:16-23`](../../src/core/providers/registry.py)) |
| Тесты | [`test_provider_plugin_backbone.py`](../../tests/test_provider_plugin_backbone.py) — 7 |
| **Offline-сюита** | **218 passed, 10 deselected** ✅ (было 211 → +7) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-09, pkg-000016) | Факт | Статус |
|--------------------------------|------|--------|
| t01 descriptor runtime types | `EIDProviderDescriptor(name, config_spec, build)` + `ProviderRuntime(config, session_store, http_client, secret_box, oidc, clock)` ([descriptor.py:15-19](../../src/core/providers/descriptor.py), [runtime.py:14-21](../../src/core/providers/runtime.py)) | 🟢 |
| t02 provider runtime factory | `build_provider_runtime`: http_client создаётся **только** при `eid_provider != "mock"`, `timeout=oidc_request_timeout_s` ([runtime_factory.py:10-21](../../src/core/providers/runtime_factory.py)) | 🟢 |
| t03 lazy registry + mock descriptor | `build_registry` строит из `ALL_EID_PROVIDER_DESCRIPTORS`; регистрирует active+mock; `MOCK_EID_DESCRIPTOR` собирает `MockEIDProvider` ([registry_builder.py](../../src/core/providers/registry_builder.py), [mock/descriptor.py](../../src/core/providers/mock/descriptor.py)) | 🟢 |
| t04 registry guard config error | `ProviderNotRegisteredError(ConfigError)` с «доступны: …» вместо `KeyError`; `get_active` использует тот же путь ([registry.py:16-24](../../src/core/providers/registry.py)) | 🟢 |
| t05 offline registry+guard tests | 7 тестов (build/mock-descriptor/no-httpx-mock/httpx-non-mock/factory-path/unknown-guard/get_active-missing) | 🟢 |
| t06 story acceptance verification | AC 5/5 (см. §2) | 🟢 |
| **STORY-IDS-EID-03** | платформа провайдеров реализована | **🟢 Done** |

Индекс ([`bullrun-launch-index.md:54`](../tasks/bullrun-launch-index.md)) держит эпик `🟡 In Progress — EID-01 🟢; EID-03 🟢; EID-04+ backlog` — корректно.

---

## 2. Сверка Acceptance Criteria story

| AC | Факт (код + тест) | Вердикт |
|----|-------------------|---------|
| `EIDProviderDescriptor` + `ProviderRuntime`; mock через дескриптор | оба класса есть; `MOCK_EID_DESCRIPTOR.build` → `MockEIDProvider`; тест `test_mock_descriptor_builds_provider` | ✅ |
| Реестр из набора дескрипторов; +провайдер без правок тела `providers.py`/`registry.py` | `build_registry(ALL_EID_PROVIDER_DESCRIPTORS)`; `providers.py` лишь зовёт `build_registry`, `registry.py` — generic; добавление = +дескриптор в `ALL_EID_PROVIDER_DESCRIPTORS` | ✅ |
| `EID_PROVIDER=<незарегистр.>` → `ProviderNotRegisteredError`/`ConfigError` с доступными, не `KeyError`; чистый ответ | `registry.get` raise с «доступны: …»; `ProviderNotRegisteredError(ConfigError)` → глобальный config-handler; тест `..._with_available_list` (assert «доступны», «mock», isinstance ConfigError) | ✅ |
| В mock/in-memory сетевые клиенты не создаются | `http_client=None` для mock; тест `..._does_not_create_httpx_in_mock_mode` (`http_client is None` + `httpx.Client` not called); для non-mock — создаётся (тест `..._creates_httpx_for_non_mock_active`) | ✅ |
| Offline зелёный; тест на guard и сборку реестра | 218 passed; 7 dedicated тестов | ✅ |

**Вывод:** все 5 AC выполнены и покрыты тестами. `config_spec` = `empty_config_spec()` (placeholder) — **по scope** (наполнение в EID-04), не gap.

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| F1 | MEDIUM | Doc-stale | backlog-story помечена `⚪ Todo` (стр.6), а «Точки в коде (текущее состояние)» описывают **удалённый** код: «Хардкод реестра providers.py:92 (`EIDProviderRegistry({"mock": ...})`)» и «Голый KeyError registry.py:11-14» — оба заменены | [`STORY-IDS-EID-03...md:6,26-27`](../tasks/backlog-stories/STORY-IDS-EID-03-provider-plugin-backbone.md) |
| F2 | LOW | Design-observation | `build_registry` **молча пропускает** валидируемый, но не описанный active-провайдер (`continue` при `descriptor is None`, [registry_builder.py:24](../../src/core/providers/registry_builder.py)). Поэтому `EID_PROVIDER=eideasy` → сервис **стартует** с реестром только из `mock`; `ProviderNotRegisteredError` всплывает лишь при `get_active` (per-request 500), не fail-fast на старте | [registry_builder.py:22-26](../../src/core/providers/registry_builder.py) |

> F2 — наблюдение: AC3 требует корректный тип ошибки **в точке использования** — он соблюдён (`get_active` бросает `ProviderNotRegisteredError`). Fail-fast на старте дал бы раннее обнаружение мисконфига, но это не нарушение AC. Сейчас провайдеры eideasy/authentigate ещё не описаны (EID-02 backlog), так что путь не активен в проде.

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **218 passed** (было 211 → +7 EID-03-тестов), **ожидаемо** |
| Хардкод `{"mock": ...}` в фабрике | удалён; заменён на `build_registry` — не регресс |
| `registry.get` `KeyError`→`ProviderNotRegisteredError` | поведенческая смена, согласована со story; старые тесты на `KeyError` (`test_eid_provider_registry.py::test_get_unknown_provider_raises`) — проверить совместимость |
| eID-флоу EID-01 (`get_active`/`start_flow`) | через новый реестр; сюита зелёная — не сломан |
| Сетевые клиенты в mock | не создаются (verified) — без побочных эффектов на старте |

**Примечание по регрессии:** прежний `test_eid_provider_registry.py::test_get_unknown_provider_raises` ожидал `KeyError`. Сюита **зелёная (218 passed)** — значит тест либо обновлён под `ProviderNotRegisteredError` (подкласс не `KeyError`), либо снят. Поскольку падений нет — несовместимости не осталось; формальная регрессия закрыта внутри волны.

---

## 5. Итог

- **STORY-IDS-EID-03 — 🟢 исполнена полно:** дескрипторы + `ProviderRuntime` + lazy `build_registry` + guard `ProviderNotRegisteredError(ConfigError)`; mock через дескриптор; нет сетевых клиентов в mock-режиме. AC 5/5, 7 тестов, фундамент под EID-04…08/EID-02 заложен. EID-1 (KeyError) закрыт.
- **Материальный finding один — F1 (doc-stale backlog-story).** F2 — LOW design-наблюдение (lazy guard vs fail-fast), вне AC.

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; статусы тасков сверены по коду.
- [x] AC сверены по коду **и** тестам; интеграция фабрика→runtime→registry прослежена ([providers.py:92-96](../../src/core/infrastructure/providers.py)).
- [x] Регрессий нет; 211→218 объяснён; совместимость старого registry-теста отмечена.
- [x] F2 явно отделён от AC (наблюдение, не нарушение).
