# Жёсткий аудит исполнения STORY-IDS-EID-05 (канон контракта provider→core)

> **Дата:** 2026-06-08
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-EID-05-canonical-provider-contract`](../tasks/backlog-stories/STORY-IDS-EID-05-canonical-provider-contract.md) vs фактический код. Исполнена под **EPIC-IDS-09-eid-verification** (pkg-000018), 5 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): EPIC-IDS-09, task queue t01–t05 (pkg-000018).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| `EidErrorCode` | `StrEnum`, 9 кодов ([base.py:9-...](../../src/core/providers/base.py)); `EIDProviderError(code=EidErrorCode.UNKNOWN)` (base.py:39-44) |
| Orchestrator split | `except EIDProviderError` → `exc.code.value`; `except Exception` → `UNKNOWN` ([handlers.py:266-302](../../src/core/api/handlers.py)) |
| Канон-идентичность | mock `subject_hash=secrets.token_hex(16)` (без префикса); `verified_person_hash=hash_secret(f"{country}:{subject_hash}")` ([handlers.py:304](../../src/core/api/handlers.py), [mock_provider.py:65-71](../../src/core/providers/mock/mock_provider.py)) |
| Тесты | [test_canonical_provider_contract.py](../../tests/test_canonical_provider_contract.py) — 3 (error-code-audit / unknown / cross-provider-dedup) |
| **Offline-сюита** | **225 passed, 10 deselected** ✅ (было 222 → +3) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-09, pkg-000018) | Факт | Статус |
|--------------------------------|------|--------|
| t01 eid error code enum | `EidErrorCode(StrEnum)` — 9 канон-кодов; `EIDProviderError` несёт `code` | 🟢 |
| t02 orchestrator provider error handling | `except EIDProviderError as exc → reason=exc.code.value`; `except Exception → UNKNOWN`; audit `failure_reason=reason`; `body.error.eid_error_code` только для провайдер-ошибки ([handlers.py:266-302](../../src/core/api/handlers.py)) | 🟢 |
| t03 canonical subject hash contract | mock без `mock-`-префикса; формула `verified_person_hash` неизменна; правило в [06-eid-providers §Каноническая идентичность](../runtime-docs/06-eid-providers.md) | 🟢 |
| t04 offline contract tests | 3 теста (USER_CANCELLED в audit + eid_error_code; RuntimeError→UNKNOWN без утечки; cross-provider dedup) | 🟢 |
| t05 story acceptance verification | AC 5/5 (см. §2) | 🟢 |
| **STORY-IDS-EID-05** | канон-контракт ошибок + идентичности | **🟢 Done** |

Индекс ([`bullrun-launch-index.md:60`](../tasks/bullrun-launch-index.md)) держит эпик `🟡 In Progress — EID-01 🟢; EID-03 🟢; EID-04 🟢; EID-05 🟢` — корректно.

---

## 2. Сверка Acceptance Criteria story

| AC | Факт (код + тест) | Вердикт |
|----|-------------------|---------|
| `EidErrorCode` есть; `EIDProviderError` несёт код | base.py:9,39-44 | ✅ |
| Orchestrator различает `EIDProviderError` (код в `failure_reason`/исход) и `Exception` (`UNKNOWN`); user_cancel отличим | handlers.py:266-302; тест `..._records_canonical_code_in_audit` (USER_CANCELLED) + `..._records_unknown` (RuntimeError→UNKNOWN, нет `eid_error_code` в теле) | ✅ |
| `subject_hash` без имени провайдера; правило задокументировано; cross-provider дедуп тест | mock = `token_hex(16)`; doc 06 §F12; тест `test_same_subject_hash_different_providers_same_verified_person_hash` (mock vs authentigate → одинаковый hash) | ✅ |
| Добавление провайдера не добавляет кодов в ядро | `EidErrorCode` — фиксированный канон-enum, провайдер мапит **в** него | ✅ |
| Offline зелёный; тесты на маппинг ошибок и дедуп | 225 passed; 3 теста контракта | ✅ |

**Вывод:** все 5 AC выполнены и покрыты тестами. F2 (потеря кодов ошибки) и F12 (Sybil через провайдер-префикс) из Authentigate-аудита закрыты.

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| F1 | MEDIUM | Doc-stale | backlog-story помечена `⚪ Todo` (стр.6), реально 🟢 Done под `EPIC-IDS-09` (pkg-000018); «Точки в коде» ссылаются на устаревшие строки (`handlers.py:263-281` except, `283-286` hash) — сместились на 266-302 / 304 | [`STORY-IDS-EID-05...md:6,23-27`](../tasks/backlog-stories/STORY-IDS-EID-05-canonical-provider-contract.md) |
| F2 | MEDIUM | Doc-drift / contradiction | [06-eid-providers.md](../runtime-docs/06-eid-providers.md) обновлён сверху (EidErrorCode/каноническая идентичность — корректно), но секция реестра **устарела после EID-03/04**: стр.41 «реестр… только mock»; стр.48-51 таблица «eideasy/authentigate — конфиг есть, кода нет» + «⚠️ Ловушка (gap EID-1)… `get_active()` упадёт с `KeyError`… безопасно только mock»; стр.62 «зарегистрировать в реестре в `providers.py` (словарь жёстко содержит только mock)». В коде уже `build_registry` + `ProviderNotRegisteredError` (не `KeyError`) + authentigate `config_spec`. Документ внутренне противоречив | `06-eid-providers.md:39-64` |

### F2 — пояснение
EID-05 правил 06-eid-providers (добавил §«Каноническая идентичность»/коды), но **не реконсилил** секцию реестра, которую EID-03 (плагин-платформа, guard вместо KeyError) и EID-04 (provider-owned config) сделали неверной. Итог — один runtime-doc одновременно утверждает «есть guard `ProviderNotRegisteredError`» (неявно, через новые секции) и «упадёт голым `KeyError`, только mock» (стр.51). Накопленный doc-debt EID-03/04, всплывший при правке 06 в EID-05. **Как закрыть (направление):** привести секцию реестра 06 к факту (build_registry/дескрипторы/guard; authentigate config_spec есть). Решение — за владельцем.

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **225 passed** (было 222 → +3 контракт-теста), **ожидаемо** |
| Старый `except Exception` (EID-01) | заменён на `except EIDProviderError / except Exception` — поведенческая смена, согласована со story; eID-флоу EID-01 зелёный |
| `verified_person_hash` формула | **неизменна** (`f"{country}:{subject_hash}"`) — обратная совместимость хэшей сохранена |
| mock `subject_hash` `mock-…` → `token_hex` | смена значения mock — не влияет на прод (mock dev-only); тесты обновлены |
| `eid_error_code` в теле ошибки | добавлен только для `EIDProviderError`; для `Exception` отсутствует (не утечка деталей) |

Регрессий не выявлено.

---

## 5. Итог

- **STORY-IDS-EID-05 — 🟢 исполнена полно:** канон `EidErrorCode`, дифференциация ошибок в orchestrator (provider-код vs UNKNOWN, user_cancel отличим), provider-agnostic `subject_hash` + кросс-провайдерная дедупликация anti-Sybil. AC 5/5, 3 теста. F2/F12 Authentigate-аудита закрыты.
- **Два MEDIUM-findings, оба документные:** F1 (doc-stale backlog-story) и F2 (внутреннее противоречие в 06-eid-providers — секция реестра устарела после EID-03/04). Код чист, регрессий нет.

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; статусы тасков сверены по коду.
- [x] AC сверены по коду **и** тестам (error-mapping + dedup проверены реальными тестами).
- [x] Регрессий нет; 222→225 объяснён; формула хэша — обратная совместимость.
- [x] Doc-drift (F2) в 06 вскрыт как внутреннее противоречие, не скрыт; отделён от чистого кода.
