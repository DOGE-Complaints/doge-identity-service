# Жёсткий аудит исполнения STORY-IDS-PV-02 (provider-owned config + allowlist префиксов)

> **Дата:** 2026-06-11
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-PV-02-provider-owned-config`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-02-provider-owned-config.md) vs фактический код. Исполнена под **EPIC-IDS-10-phone-verification** (alias `EPIC-IDS-PHONE`), pkg-000023, 6 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): Текущая волна pkg-000023, STORY-IDS-PV-02 🟢 (стр.11,37,491-496).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Config-spec алиас | `SmsProviderConfigSpec = ProviderConfigSpec` ([config_spec.py:5](../../src/core/phone/config_spec.py)); дескриптор переключён на него ([descriptor.py:9,19](../../src/core/phone/descriptor.py)) |
| Ядро env (provider-agnostic) | `SMS_PROVIDER`, `PHONE_ALLOWED_DIAL_PREFIXES`, `PHONE_CODE_LENGTH/TTL_S/MAX_ATTEMPTS/RESEND_COOLDOWN_S/ONE_ACCOUNT_PER_NUMBER` ([schema.py:162-170,230-236](../../src/core/config/schema.py), [providers.py:23-29](../../src/core/config/providers.py)) |
| Членство по реестру | `SMS_PROVIDER not in registered_sms_provider_names()` → `ConfigError` ([schema.py:165-168](../../src/core/config/schema.py)) |
| Делегированная валидация | `_validate_active_sms_provider_config` → `descriptor.config_spec.validate(env)` ([schema.py:108-113,170](../../src/core/config/schema.py)) |
| E.164 + prefix-gate | `normalize_to_e164`, `assert_allowed_dial_prefix` → `COUNTRY_NOT_ALLOWED` ([e164.py](../../src/core/phone/e164.py)) |
| AppConfig phone-поля | 7 ядровых полей; провайдер-полей нет ([schema.py:63-69](../../src/core/config/schema.py)) |
| `.env.example` | phone-блок строки 63-69 + Telnyx-секция стр.71 ([.env.example](../../.env.example)) |
| Тесты | [test_phone_e164.py](../../tests/test_phone_e164.py) — 5; [test_phone_config_schema.py](../../tests/test_phone_config_schema.py) — 4 |
| **Offline-сюита** | **269 passed, 9 skipped** ✅ (было 260 → +9) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-10, pkg-000023) | Факт | Статус |
|--------------------------------|------|--------|
| t01 sms provider config spec | `core/phone/config_spec.py` (`SmsProviderConfigSpec` алиас `ProviderConfigSpec` + `noop_provider_settings_loader`); дескриптор+mock переведены на него ([config_spec.py](../../src/core/phone/config_spec.py), [mock/descriptor.py:7-9](../../src/core/phone/mock/descriptor.py)) | 🟢 |
| t02 appconfig phone fields + sms provider validation | 7 phone-полей в `AppConfig` ([schema.py:63-69](../../src/core/config/schema.py)); чтение+дефолты ([schema.py:230-236](../../src/core/config/schema.py)); членство `SMS_PROVIDER` + делегированная валидация ([schema.py:162-170](../../src/core/config/schema.py)) | 🟢 |
| t03 e164 normalize + prefix allowlist | `normalize_to_e164` (strip пробелов/скобок/дефисов, опц. `+`, иначе `INVALID_PHONE`); `assert_allowed_dial_prefix` → `COUNTRY_NOT_ALLOWED`; `_dial_prefixes` парсит CSV→tuple ([e164.py](../../src/core/phone/e164.py), [schema.py:125-130](../../src/core/config/schema.py)) | 🟢 |
| t04 env example phone block | `.env.example:63-69` phone-блок с комментариями + Telnyx-плейсхолдер стр.71 | 🟢 |
| t05 offline phone config + e164 tests | 5 e164 + 4 config = 9 тестов | 🟢 |
| t06 story acceptance verification | AC 5/5 (см. §2); pipeline-story `Status: 🟢 Done` (стр.7), индекс t06 🟢 ([bullrun-launch-index.md:496](../tasks/bullrun-launch-index.md)) | 🟢 |
| **STORY-IDS-PV-02** | provider-owned config + allowlist | **🟢 Done** |

Индекс держит эпик корректно: `EPIC-IDS-10 … 🟡 In Progress — PV-01 🟢; PV-02 🟢` ([bullrun-launch-index.md:78](../tasks/bullrun-launch-index.md)).

---

## 2. Сверка Acceptance Criteria story (по коду + тестам)

| AC | Факт (код + тест) | Вердикт |
|----|-------------------|---------|
| `SMS_PROVIDER` валидируется по реестру; неизвестный → понятная `ConfigError` | членство ([schema.py:165-168](../../src/core/config/schema.py)); тесты `test_unknown_sms_provider_rejected` (`SMS_PROVIDER must be mock`), `test_sms_provider_membership_lists_registered_names` | ✅ |
| `PHONE_ALLOWED_DIAL_PREFIXES` парсится; неразрешённый префикс → `COUNTRY_NOT_ALLOWED` (`+372` ок / `+1` отклонён) | `_dial_prefixes` CSV→tuple ([schema.py:125-130](../../src/core/config/schema.py)); `assert_allowed_dial_prefix` ([e164.py:33-42](../../src/core/phone/e164.py)); тесты `test_prefix_gate_allows_estonia`, `test_prefix_gate_rejects_us` (`code is COUNTRY_NOT_ALLOWED`), `test_phone_allowed_dial_prefixes_parsed_to_tuple` | ✅ |
| Нормализация E.164 покрыта тестами (пробелы/скобки/без `+`) | `normalize_to_e164` ([e164.py:6-30](../../src/core/phone/e164.py)); тесты `test_normalize_strips_spaces_and_parens`, `test_normalize_without_plus_prefix`, `test_invalid_phone_raises` | ✅ |
| Ядровые phone-параметры доступны ядру; провайдер-поля не в `AppConfig` | 7 полей ([schema.py:63-69](../../src/core/config/schema.py)); тест `test_core_phone_params_on_app_config` (+ `assert not hasattr(cfg, "telnyx_api_key")`) | ✅ |
| `.env.example` дополнен phone-блоком; offline зелёный | `.env.example:63-69`; **269 passed** | ✅ |

**Вывод:** все 5 AC выполнены и покрыты тестами (9). Provider-agnostic фильтр префиксов и делегированная валидация зеркалят eID-конфиг (EID-04).

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F1** | MEDIUM | Doc-stale | Backlog-story `Status: ⚪ Todo` (стр.6) + AC `[ ]` (стр.30-34) — реально 🟢 Done под pkg-000023. Та же рассинхронизация в [`EPIC-IDS-PHONE.md`](../tasks/backlog-stories/phone-verification/EPIC-IDS-PHONE.md) (строка PV-02 в таблице stories = ⚪ Todo). **Как закрыть:** Status ⚪→🟢, AC `[ ]`→`[x]`, строка таблицы EPIC.md PV-02 → 🟢. Рекуррентный паттерн (как PV-01). | [`STORY-IDS-PV-02...md:6,30-34`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-02-provider-owned-config.md) |
| **F2** | LOW | Doc-stale | Индекс декларирует «268 pytest offline» ([bullrun-launch-index.md:11](../tasks/bullrun-launch-index.md)), фактически **269 passed** (off-by-one, тот же тип, что PV-01/EID-08). **Как закрыть:** синхронизировать число. | [`bullrun-launch-index.md:11`](../tasks/bullrun-launch-index.md) |

Иных материальных findings нет. Наблюдения (severity none, по scope, **не gap**):
- **`SmsProviderConfigSpec` — алиас** `ProviderConfigSpec` ([config_spec.py:5](../../src/core/phone/config_spec.py)), не отдельный класс. DRY-переиспользование eID-инфраструктуры (`validate`/`required`/`optional_defaults`/`loader`) — соответствует story («по образцу `config_spec.py`»); даёт SMS-неймспейс без дубля логики.
- **PV-02 модифицировала файлы PV-01** (`descriptor.py`, `mock/descriptor.py` теперь импортируют `SmsProviderConfigSpec` из `core.phone.config_spec` вместо прямого `core.providers.config_spec`). Прогрессивное уточнение, не регресс — реестр-тесты PV-01 зелёные (часть 269).
- **`assert_allowed_dial_prefix` с пустым allowlist → пропускает всё** ([e164.py:34-35](../../src/core/phone/e164.py)). Безопасно: `_dial_prefixes` гарантирует ≥1 префикс (`ConfigError` при пустом, [schema.py:128-129](../../src/core/config/schema.py)), так что пустой tuple до гейта не доходит из конфига.
- **Сам OTP/prefix-гейт ещё не вызывается во флоу** (`normalize_to_e164`/`assert_allowed_dial_prefix` не подключены к request/confirm) — **вне scope PV-02** (флоу → [PV-05](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md)); здесь только утилита+валидация. Параметры `PHONE_MAX_ATTEMPTS`/`RESEND_COOLDOWN` объявлены, используются с PV-03/05.

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **269 passed, 9 skipped** (было 260 → +9 phone-config/e164 тестов), **ожидаемо** |
| `AppConfig` | +7 phone-полей (обязательные в dataclass); все конструкторы получают значения через `load_config_from_env`/`provide_app_config` — существующие config-тесты зелёные |
| `load_config_from_env` | +блок SMS (членство+делегированная валидация) после eID-блока; eID-валидация не тронута |
| Файлы PV-01 | `descriptor.py`/`mock/descriptor.py` переведены на алиас `SmsProviderConfigSpec` — поведение идентично (алиас того же класса); PV-01 тесты зелёные |
| `core/phone/e164.py` | новый модуль, аддитивный; ни на что не влияет до подключения во флоу (PV-05) |
| Сеть в offline | нет |
| eID/OAuth/auth-флоу | не затронуты — сюита зелёная |

Регрессий не выявлено.

---

## 5. Итог

- **STORY-IDS-PV-02 — 🟢 исполнена полно:** `SmsProviderConfigSpec` (алиас, DRY), ядровые phone-env (`SMS_PROVIDER` членство + делегированная `config_spec.validate`, `PHONE_ALLOWED_DIAL_PREFIXES` фильтр в ядре, OTP/rate-параметры), утилита `normalize_to_e164` + `assert_allowed_dial_prefix`→`COUNTRY_NOT_ALLOWED`, 7 phone-полей в `AppConfig` (провайдер-поля исключены), phone-блок в `.env.example`. Зеркалит eID-конфиг (EID-04). AC 5/5, 9 тестов.
- **Findings:** **F1 (MEDIUM, doc-stale)** — backlog-story + EPIC.md таблица ⚪→🟢 (рекуррентно); **F2 (LOW)** — индекс 268 vs факт 269 offline.
- Наблюдения (alias `SmsProviderConfigSpec`; правка файлов PV-01; гейт не во флоу → PV-05) — по scope, не gaps.

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; 6 тасков + story сверены по коду (pipeline-story 🟢, индекс t01–t06 🟢).
- [x] AC 5/5 сверены по коду **и** тестам; prefix-гейт проверен на `+372` ок / `+1`→`COUNTRY_NOT_ALLOWED`, E.164-нормализация — 3 кейса.
- [x] Регрессий нет; 260→269 (+9) объяснён; правка PV-01-файлов на алиас проверена (без поведенческой смены).
- [x] Границы scope прослежены: подключение гейта во флоу → PV-05, использование rate-параметров → PV-03/05 (не gaps PV-02).
- [x] Провайдер-поля не в `AppConfig` подтверждено тестом (`not hasattr telnyx_api_key`).
