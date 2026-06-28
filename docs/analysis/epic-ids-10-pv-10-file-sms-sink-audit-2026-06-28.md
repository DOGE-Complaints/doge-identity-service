# Жёсткий аудит STORY-IDS-PV-10 (File SMS sink) по фактическому коду

> **Дата:** 2026-06-28
> **Объект:** [`STORY-IDS-PV-10-file-sms-sink-dev`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md) (статус в backlog — 🟢 Done) vs реальный код `src/`, `tests/`, конфиги.
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`; регрессии; gaps с severity + как закрыть. Findings, не реализация.
> **Сюита:** **394 passed, 12 deselected** (offline, `pytest -m "not live_integration"`) — без регрессий; целевой тест-файл [`test_phone_file_sms_sender.py`](../../tests/test_phone_file_sms_sender.py) — **8 passed**.

---

## 0. Вердикт

**Стори реализована добросовестно и соответствует заявленному scope.** Все 8 AC подтверждены кодом и тестами. Регрессий нет. Найдены **2 LOW doc-stale** расхождения (исправлены в этом проходе) и **2 INFO** наблюдения (не дефекты). Индекс [`bullrun-launch-index`](../tasks/bullrun-launch-index.md) для PV-10 **уже актуализирован пайплайном** (pkg-000041) и фактически корректен.

---

## 1. Scope → код: построчная сверка (всё ✅)

| Scope-пункт стори | Факт в коде | Статус |
|---|---|---|
| `FileSmsSender` (`provider_name="file"`, append `{utc_iso}\t{text}\n`, create-if-missing, UTF-8, `file-{uuid4}`, при `OSError`→`SEND_FAILED`) | [`file_sender.py:24-44`](../../src/core/phone/file/file_sender.py) — точно как описано | ✅ |
| Санитайз имени файла (только `[+0-9]`, анти-traversal) | [`file_sender.py:11,20-21`](../../src/core/phone/file/file_sender.py) `re.compile(r"[^+0-9]")`; тест `../+372…`→`+372…` ([`test:71-74`](../../tests/test_phone_file_sms_sender.py)) | ✅ |
| Provider-owned config `FILE_SMS_OUTBOX_DIR`, optional, default `var/sms-outbox` | [`config.py:9,13-18,36`](../../src/core/phone/file/config.py) | ✅ |
| Дескриптор `file` + регистрация в `ALL_SMS_PROVIDER_DESCRIPTORS` | [`descriptor.py:19-23`](../../src/core/phone/file/descriptor.py); [`registry_builder.py:4,12`](../../src/core/phone/registry_builder.py) | ✅ |
| `file` не поднимает `httpx.Client` | [`runtime_factory.py:14-15`](../../src/core/phone/runtime_factory.py) `not in {"mock","file"}`; тест `runtime.http_client is None` ([`test:116-127`](../../tests/test_phone_file_sms_sender.py)) | ✅ |
| Demo-only fail-fast: `pilot`+`file`→`ConfigError` | [`schema.py:180-183`](../../src/core/config/schema.py); тест ([`test:104-106`](../../tests/test_phone_file_sms_sender.py)) | ✅ |
| `.gitignore` outbox + `.env.example` (`file` + `FILE_SMS_OUTBOX_DIR` + предупреждение) | [`.gitignore:11`](../../.gitignore) `var/sms-outbox/`; [`.env.example:63,71-72`](../../.env.example) | ✅ |
| Тесты offline (append, разные номера, санитайз, pilot-reject, e2e request, no-http) | [`test_phone_file_sms_sender.py`](../../tests/test_phone_file_sms_sender.py) — 8 тестов, все указанные кейсы | ✅ |

### Интеграционный шов (критичный) — корректен
`file` исключён из `_needs_sms_http_client`, поэтому HTTP-клиент не создаётся. Но `file` требует загруженных settings (иначе [`descriptor.py:14-15`](../../src/core/phone/file/descriptor.py) бросает `RuntimeError`). Загрузка settings **вынесена из http-блока**: [`runtime_factory.py:26-29`](../../src/core/phone/runtime_factory.py) грузит settings для любого провайдера ≠ `mock` **до** проверки http-клиента → `file` получает `FileSmsSettings`, при этом без сети. Подтверждено e2e-тестом `test_phone_request_with_file_provider_writes_outbox_log` ([`test:145-173`](../../tests/test_phone_file_sms_sender.py)): `session.provider_message_id.startswith("file-")` + файл с 6-значным кодом.

### AC → доказательство (все [x] правомерны)
8/8 AC подтверждены кодом+тестами (см. таблицу §1). Отметки `[x]` в стори соответствуют факту.

---

## 2. Findings

### F1 · LOW · doc-stale (исправлено) — пример в стори показывает мс, код пишет секунды
Блок «Целевое поведение» стори ([строки 23-25](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md)) показывает таймстемпы `2026-06-28T10:01:02.345Z` (миллисекунды). Реальный код [`file_sender.py:14-17`](../../src/core/phone/file/file_sender.py) делает `.replace(microsecond=0)` → формат **секундной** точности `2026-06-28T10:01:02Z`. Пример не воспроизводится дословно (нарушение «examples must be real»).
- **Как закрыть:** привести пример к секундной точности (выполнено в этом проходе). Поведение кода менять не нужно — секундная гранулярность достаточна для `tail -f`; тест ордеринга использует `<=` ([`test:90-92`](../../tests/test_phone_file_sms_sender.py)), что корректно для равных таймстемпов в одну секунду.

### F2 · LOW · doc-stale (исправлено) — header EPIC-IDS-PHONE не упоминает PV-10
Сводка в шапке [`EPIC-IDS-PHONE.md:3`](../tasks/backlog-stories/phone-verification/EPIC-IDS-PHONE.md) — «🟢 Done (PV-01…07, PV-09 — pkg-000018…039; SPIKE-08 — внешнее)» — PV-10 добавлен в таблицу стори (строка 31), но не отражён в сводке шапки.
- **Как закрыть:** дополнить сводку до «…PV-09, PV-10 — pkg-000018…041…» (выполнено в этом проходе).

### INFO-1 · не дефект — бесповый `FileSmsProviderConfigSpec` следует прецеденту telnyx
[`config.py:21-36`](../../src/core/phone/file/config.py) определяет собственный класс конфиг-спеки вместо общего `ProviderConfigSpec` ([`providers/config_spec.py:16-29`](../../src/core/providers/config_spec.py)). Это **консистентно**: telnyx делает так же ([`telnyx/config.py:62`](../../src/core/phone/telnyx/config.py) `TelnyxSmsProviderConfigSpec`). `mock` использует общий — но у него нет своих полей. Дублирование протокола (`required/optional_defaults/loader/validate/load`) — осознанный паттерн пакета, не регрессия. (Замечание на будущее: 3 структурно-похожих спеки можно было бы свести к общему дженерику, но это рефактор-долг всего phone-пакета, не PV-10.)

### INFO-2 · не дефект — локальный `_format_utc_iso` в file_sender
[`file_sender.py:14-17`](../../src/core/phone/file/file_sender.py) держит собственный `_format_utc_iso` (есть одноимённый приватный в `api/handlers.py`). Переиспользование из `api/` создало бы зависимость `phone → api` (неверное направление слоёв), поэтому локальная копия в доменном модуле — корректный выбор, не дублирование-долг.

### INFO-3 · пред-существующее, вне scope PV-10 — статус эпика расходится
Пайплайн-индекс [`bullrun-launch-index.md:133`](../tasks/bullrun-launch-index.md) держит EPIC-IDS-10 как «🟡 In Progress» (из-за [`SPIKE-IDS-PV-08`](../tasks/backlog-stories/phone-verification/SPIKE-IDS-PV-08-telnyx-account-setup.md) ⚪ Todo, внешний), а backlog-шапка — «🟢 Done». Расхождение про SPIKE-08, появилось до PV-10; в скоуп этого аудита не входит, фиксируется как наблюдение.

---

## 3. Регрессии
**Не обнаружено.** Полная offline-сюита — 394 passed, 12 deselected (база до PV-09 была 386 → +8 тестов PV-10, рост ожидаемый). Изменения PV-10 аддитивны: новый пакет `phone/file/`, расширение множества в `_needs_sms_http_client`, новая ветка fail-fast в `schema.py`, новые строки в `.env.example`/`.gitignore`. Существующие `mock`/`telnyx` пути не тронуты.

---

## 4. Актуализация отчёта `bullrun-launch-index.md`

Проверено: индекс для PV-10 **уже корректен** (актуализирован пайплайном pkg-000041), правок не требует. Сверка по факту:

| Место в индексе | Запись | Факт | Вердикт |
|---|---|---|---|
| [`:11`](../tasks/bullrun-launch-index.md) | P3 Done PV-10, pkg-000041, «394 pytest offline» | измерено 394 passed | ✅ точно |
| [`:74,76`](../tasks/bullrun-launch-index.md) | active story 🟢 Done; pkg-000041 (7 tasks) | 7 task-dir на диске | ✅ |
| [`:133`](../tasks/bullrun-launch-index.md) | EPIC-IDS-10 … PV-10 🟢 | реализовано | ✅ (см. INFO-3 про статус эпика) |
| [`:642-648`](../tasks/bullrun-launch-index.md) | 7 задач PV-10 t01–t07 🟢 Done | каждая ↔ реальный код-артефакт | ✅ |
| [`:763`](../tasks/bullrun-launch-index.md) | story PV-10 🟢 Done | — | ✅ |

Маппинг задач индекса → код (все подтверждены):
- t01 file sms sender core → [`file_sender.py`](../../src/core/phone/file/file_sender.py)
- t02 file sms config spec → [`config.py`](../../src/core/phone/file/config.py)
- t03 file descriptor registry runtime → [`descriptor.py`](../../src/core/phone/file/descriptor.py) + [`registry_builder.py`](../../src/core/phone/registry_builder.py) + [`runtime_factory.py`](../../src/core/phone/runtime_factory.py)
- t04 pilot file provider fail fast → [`schema.py:180-183`](../../src/core/config/schema.py)
- t05 dev hygiene gitignore env example → [`.gitignore:11`](../../.gitignore) + [`.env.example:63,71-72`](../../.env.example)
- t06 offline file sms tests → [`test_phone_file_sms_sender.py`](../../tests/test_phone_file_sms_sender.py)
- t07 story acceptance verification → AC 8/8 [x]

---

## 5. Применённые правки (doc-only, не код)
- **F1:** пример таймстемпа в стори → секундная точность (соответствие коду).
- **F2:** сводка шапки [`EPIC-IDS-PHONE.md:3`](../tasks/backlog-stories/phone-verification/EPIC-IDS-PHONE.md) → добавлен PV-10/pkg-000041.

Код **не менялся** (правок не требовал). Индекс **не менялся** (уже актуален).
