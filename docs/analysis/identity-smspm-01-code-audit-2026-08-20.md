# Аудит по коду: STORY-IDS-SMSPM-01 (provider config + registry `SMS_PROVIDER=smspm`) — 2026-08-20

> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — verified-state, только проверяемые claims с путями; регрессии; gaps с severity + как закрыть. Findings-only (реализацию не предлагаю).
> **Объект:** pipeline [`STORY-IDS-SMSPM-01-provider-config-registry`](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-01-provider-config-registry/STORY-IDS-SMSPM-01-provider-config-registry.md) · backlog [`STORY-IDS-SMSPM-01-provider-config-registry`](../tasks/backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md) (`input_mode=backlog_story`, pkg-000046).
> **HTTP-отправка SMS — вне DoD этой story** (SMSPM-02). AC не invent.
> **Синхронизирован отчёт:** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) — статусы task/story сверены с кодом (drift статусов 🟢 не найден). Правки индекса не требуются.

---

## Вердикт

**STORY-IDS-SMSPM-01 = 🟢 Done — подтверждено фактическим кодом.** Все 5 pipeline-тасков (t01–t05) закрыты; 5 parent AC backlog/pipeline исполнены. `smspm` в registry; fail-fast HASH/TOKEN/FROM только при активном `smspm`; mock/file/telnyx без `SMSPM_*` не ломаются; `.env.example` содержит блок SMSPM. HTTP POST к SMSPM API в пакете `smspm/` нет (stub `SmspmSmsStub` — допустимо T02 / SMSPM-02).

Найдено **2 gap'а** (0×HIGH, 0×MEDIUM, 2×LOW). Ни один не ломает AC этой story. **vs story AC/DoD: 0 OPEN.**

Независимо перепрогнано (2026-08-20): `tests/test_smspm_config.py` → **11 passed**; `pytest -q -m "not live_integration"` → **417 passed, 12 deselected**. Полная сюита совпадает с [run-summary](../tasks/run-reports/identity-build-windows/run-summary-20260820-0959-epic-ids-14-smspm-01-pkg-000046.md); счётчик «12 passed» по файлу SMSPM-тестов — нет (F1).

---

## Bullrun status touchpoints (без правок индекса)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду + файлам тасков.

| Якорь индекса | Строки | Заявлено | Факт-код | Вердикт |
|---------------|--------|----------|----------|---------|
| §Актуальная точка SMSPM-01 | [bullrun:11-13](../tasks/bullrun-launch-index.md) | 🟢 pkg-000046; P3 Done 5/5; 417 pytest | пакет `src/core/phone/smspm/` + registry append + 417 offline | ✅ совпадает |
| input_mode / active story | [bullrun:102](../tasks/bullrun-launch-index.md) | `backlog_story` · SMSPM-01 🟢 | pipeline Meta Status 🟢; backlog Status 🟢 | ✅ |
| Active pkg | [bullrun:104](../tasks/bullrun-launch-index.md) | pkg-000046 🟢 5 paths | 5 task README + acceptance gates PASS | ✅ |
| Epic registry EPIC-IDS-14 | [bullrun:167](../tasks/bullrun-launch-index.md) | 🟡 In Progress — SMSPM-01 🟢; SMSPM-02…04 backlog | HTTP send / runbook / webhook отсутствуют в `smspm/` | ✅ эпик не Done |
| Task queue EPIC-IDS-14 t01–t05 | [bullrun:800-804](../tasks/bullrun-launch-index.md) | все 🟢 Done | см. таблицу тасков ниже | ✅ |
| Stories EPIC-IDS-14 | [bullrun:873](../tasks/bullrun-launch-index.md) | SMSPM-01 🟢 pkg-000046 | AC `[x]` в pipeline и backlog | ✅ |

**Актуализация:** статусы t01–t05 и story в `$bullrun` **факт-верны**. Менять 🟢→другое не нужно. Эпик EPIC-IDS-14 остаётся 🟡 (SMSPM-02…04 ⚪) — корректно.

---

## Пер-таск верификация (по коду)

| Task | Требование стори | Факт в коде | Вердикт |
|------|------------------|-------------|---------|
| **t01** SmspmSettings | `config.py` load/validate HASH/TOKEN/FROM + optional base URL + `SMSPM_SMS_CONFIG_SPEC` | [`config.py:10-54`](../../src/core/phone/smspm/config.py) — `SMSPM_REQUIRED_ENV`, `validate_smspm_config` → `ConfigError` «missing or empty»; `SmspmSettings.load`; spec `validate`/`load`; default `https://api.smspm.com`; exports [`__init__.py:1-8`](../../src/core/phone/smspm/__init__.py) | ✅ Done |
| **t02** Descriptor + registry | `SMSPM_SMS_DESCRIPTOR` `name="smspm"`; stub build ок; append в `ALL_SMS_PROVIDER_DESCRIPTORS`; mock/file/telnyx остаются; не хардкодить HTTP allow-list | [`descriptor.py:33-37`](../../src/core/phone/smspm/descriptor.py); stub [`descriptor.py:11-23`](../../src/core/phone/smspm/descriptor.py); tuple [`registry_builder.py:11-16`](../../src/core/phone/registry_builder.py) = mock, file, telnyx, smspm; [`runtime_factory.py:14-15`](../../src/core/phone/runtime_factory.py) `_needs_sms_http_client` = `not in {"mock","file"}` (D-01-4, без allow-list) | ✅ Done |
| **t03** Config tests | accept `smspm`+env; fail missing required; mock\|file\|telnyx без SMSPM ok; unknown rejected | [`tests/test_smspm_config.py`](../../tests/test_smspm_config.py) — 11 тестов (collect 2026-08-20); покрытие AC #1–#3 + stub registry | ✅ Done (счётчик «12» в gate — F1) |
| **t04** `.env.example` | комментарий `mock \| file \| telnyx \| smspm`; блок `SMSPM_*` пустые, без секретов | [`.env.example:60`](../../.env.example); блок [`80-84`](../../.env.example) (`SMSPM_HASH=`/`TOKEN=`/`FROM=` пустые; `SMSPM_API_BASE_URL=https://api.smspm.com`) | ✅ Done |
| **t05** story gate | 5 parent AC + live pytest | [acceptance-verification t05](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-01-provider-config-registry/task-ids-14-01-t05-story-acceptance-verification/acceptance-verification-task-ids-14-01-t05-story-acceptance-verification.md) PASS `2026-08-20T09:59:19Z`; сюита 417 подтверждена независимо | ✅ Done |

---

## Сверка Acceptance Criteria (verbatim backlog = pipeline)

Источник AC: backlog [`STORY-IDS-SMSPM-01:64-69`](../tasks/backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md) = pipeline [`:66-71`](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-01-provider-config-registry/STORY-IDS-SMSPM-01-provider-config-registry.md). Формулировки не менялись.

| AC | Факт (код + тест) | Вердикт |
|----|-------------------|---------|
| `SMS_PROVIDER=smspm` принимается конфигом; неизвестное имя по-прежнему отклоняется | `schema.py` членство из `registered_sms_provider_names()` ([`schema.py:168-174`](../../src/core/config/schema.py)); имена из tuple registry ([`registry_builder.py:11-22`](../../src/core/phone/registry_builder.py)); тесты `test_smspm_sms_provider_loads_with_required_env`, `test_unknown_sms_provider_still_rejected`, `test_registered_sms_provider_names_includes_smspm` | ✅ |
| При `smspm` без `SMSPM_HASH` / `SMSPM_TOKEN` / `SMSPM_FROM` сервис не стартует с ясной config-ошибкой | `_validate_active_sms_provider_config` → `config_spec.validate` только для активного имени ([`schema.py:115-120,176`](../../src/core/config/schema.py)); `ConfigError(f"Required env var {key!r} is missing or empty")` ([`config.py:15-18`](../../src/core/phone/smspm/config.py)); boot: `create_app(provide_app_config())` ([`asgi_app.py:474`](../../src/core/api/asgi_app.py)) → `provide_app_config` → `load_config_from_env` ([`providers.py:19-34`](../../src/core/config/providers.py)); тесты `test_smspm_sms_provider_requires_{hash,token,from}` (пустая строка ≡ missing: `_env_value` `.get(key,"")`+[`.strip()`](../../src/core/providers/config_spec.py)) | ✅ |
| При `SMS_PROVIDER=mock\|file\|telnyx` поведение не регрессирует (SMSPM env не обязательны) | validate чужого descriptor, не SMSPM ([`schema.py:115-120`](../../src/core/config/schema.py)); тесты `test_{mock,file,telnyx}_without_smspm_env_ok`; mock/file/telnyx остаются в tuple (D-01-5) | ✅ |
| `.env.example` содержит блок SMSPM и обновлённый комментарий провайдеров | [`.env.example:60,80-84`](../../.env.example) | ✅ |
| T01–T04 закрыты; descriptor в `ALL_SMS_PROVIDER_DESCRIPTORS` | см. пер-таск; `SMSPM_SMS_DESCRIPTOR` 4-й элемент tuple ([`registry_builder.py:11-16`](../../src/core/phone/registry_builder.py)) | ✅ |

**D-01-\* (не AC, зеркало решений):** D-01-1/2/3 — в `config.py` + schema validate-only-active. D-01-4 — `_needs_sms_http_client` без allow-list → для `smspm` создаётся `httpx.Client` ([`runtime_factory.py:31-32`](../../src/core/phone/runtime_factory.py)); stub его не использует (ожидаемо до SMSPM-02). D-01-5 — mock/file/telnyx в tuple.

---

## Регрессии

**Не найдено в коде этой волны.**

| Аспект | Факт |
|--------|------|
| Telnyx / mock / file descriptors | все три в `ALL_SMS_PROVIDER_DESCRIPTORS` ([`registry_builder.py:12-14`](../../src/core/phone/registry_builder.py)); telnyx-тесты сюиты зелёные (417) |
| `SMS_PROVIDER` allow-list | не захардкожен в `schema.py` — `registered_sms_provider_names()` ([`schema.py:169-174`](../../src/core/config/schema.py)) |
| Env-источник runtime vs AppConfig | `build_sms_provider_runtime` грузит spec из `resolve_config_env(env)` ([`runtime_factory.py:25-29`](../../src/core/phone/runtime_factory.py)); factory передаёт `merged_env` ([`infrastructure/providers.py:133-136`](../../src/core/infrastructure/providers.py)) — бывший PV-06 F3 (сырой `os.environ`) на этом шве не воспроизведён |
| HTTP send | в `src/core/phone/smspm/` нет `sender.py` / `httpx` / POST; glob = `config.py`, `descriptor.py`, `__init__.py` | вне DoD |
| Offline-сюита | **417 passed, 12 deselected** (совпадает с run-summary) |

---

## Gaps (findings)

| ID | Severity | Суть | Файл:строка | Как закрыть |
|----|----------|------|-------------|-------------|
| **F1** | **LOW** | **Off-by-one в P3-артефактах SMSPM-тестов.** t05 gate и run-summary пишут `pytest tests/test_smspm_config.py` → «12 passed». На диске collect/run = **11** тестов (11 имён, см. collect-list ниже). Полная сюита «417 passed, 12 deselected» при этом верна. Не дефект продукта; ложный счётчик файла. | [acceptance t05:24-25](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-01-provider-config-registry/task-ids-14-01-t05-story-acceptance-verification/acceptance-verification-task-ids-14-01-t05-story-acceptance-verification.md); [run-summary:24-25](../tasks/run-reports/identity-build-windows/run-summary-20260820-0959-epic-ids-14-smspm-01-pkg-000046.md); [`tests/test_smspm_config.py`](../../tests/test_smspm_config.py) | Поправить комментарий «12 passed» → «11 passed» в t05 gate и run-summary. Не менять 🟢 статусы. |
| **F2** | **LOW** | **Runbook SMS всё ещё без `smspm` (и без `file`).** [`.env.example:60`](../../.env.example) = `mock \| file \| telnyx \| smspm`; runbook §2: `SMS_PROVIDER=mock # mock \| telnyx` ([`phone-sms-verification.md:35`](../runbook/phone-sms-verification.md)). T04 этой story **запрещает** правку runbook (SMSPM-03). Не регрессия кода SMSPM-01. | [`phone-sms-verification.md:4,35,46`](../runbook/phone-sms-verification.md); backlog [SMSPM-03](../tasks/backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md) D-03-1 режим C | Не в этой wave. Закрытие = SMSPM-03 (уже ⚪ backlog). P5: WAIVED reason=out-of-DoD, follow_up=new_story (путь уже есть). |

**Collect-list F1 (11):** `test_registered_sms_provider_names_includes_smspm`, `test_smspm_sms_provider_loads_with_required_env`, `test_smspm_sms_provider_requires_{hash,token,from}`, `test_smspm_optional_base_url_default`, `test_{mock,file,telnyx}_without_smspm_env_ok`, `test_unknown_sms_provider_still_rejected`, `test_build_sms_registry_active_smspm_stub`.

Наблюдения (**не gap**, severity none):

- **Stub send:** `SmspmSmsStub.send` бросает `SmsSenderError` / `PROVIDER_UNAVAILABLE` ([`descriptor.py:19-23`](../../src/core/phone/smspm/descriptor.py)). При валидном `SMS_PROVIDER=smspm` процесс **стартует**, OTP send падает в runtime — явно T02 «stub до SMSPM-02», не AC-нарушение.
- **Override `SMSPM_API_BASE_URL`:** реализован в `SmspmSettings.load` ([`config.py:34`](../../src/core/phone/smspm/config.py)); тест покрывает только default. AC этого не требует.
- **t01/t02/t04 README «Факты из кода»** описывают pre-state («пакета нет») — P1 snapshot; AC/DoD `[x]`. Working-doc, не продукт.

---

## Итог для индекса / P5

- Статусы task/story SMSPM-01 в `bullrun-launch-index.md` — **факт-верны** ([11-13], [102], [104], [167], [800-804], [873]); drift 🟢 нет.
- **vs story AC: 0 OPEN.** Product Story Done (5/5 AC) ≠ пустой gap-list: F1–F2 LOW residual.
- F1 — docs-only счётчик в gate/run-summary (не код).
- F2 — out-of-DoD, follow_up уже SMSPM-03; не reopen как дефект SMSPM-01.
- **P5 не стартовать из этого отчёта** (fence VAL). HTTP send = SMSPM-02.
