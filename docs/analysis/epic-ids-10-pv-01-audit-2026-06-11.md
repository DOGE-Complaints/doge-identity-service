# Жёсткий аудит исполнения STORY-IDS-PV-01 (plugin-платформа SMS-провайдеров)

> **Дата:** 2026-06-11
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-PV-01-phone-provider-backbone`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md) vs фактический код. Исполнена под **EPIC-IDS-10-phone-verification** (alias `EPIC-IDS-PHONE`), pkg-000022, 6 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): Текущая волна pkg-000022, STORY-IDS-PV-01 🟢 (стр.11,35).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Пакет | `src/core/phone/`: `base.py`, `descriptor.py`, `runtime.py`, `registry.py`, `registry_builder.py`, `__init__.py`, `mock/{__init__,descriptor,mock_sender}.py` |
| Порт/DTO/ошибки | `SmsSenderPort` (Protocol, `@runtime_checkable`), `SmsSendResult` (dataclass), `SmsSenderError`, `SmsErrorCode` (StrEnum, 9 кодов) ([base.py](../../src/core/phone/base.py)) |
| Дескриптор + guard | `SmsProviderDescriptor`, `SmsProviderNotRegisteredError(ConfigError)` ([descriptor.py:11,17](../../src/core/phone/descriptor.py)) |
| DI-рантайм | `SmsProviderRuntime(config, http_client, settings)` ([runtime.py:11-15](../../src/core/phone/runtime.py)) |
| Реестр + сборка | `SmsSenderRegistry.get/get_active`, `build_sms_registry`, `registered_sms_provider_names` ([registry.py](../../src/core/phone/registry.py), [registry_builder.py](../../src/core/phone/registry_builder.py)) |
| Mock-эталон | `MockSmsSender` (in-memory capture, `accepted=True`) + `MOCK_SMS_DESCRIPTOR` ([mock/mock_sender.py](../../src/core/phone/mock/mock_sender.py), [mock/descriptor.py](../../src/core/phone/mock/descriptor.py)) |
| Тесты | [test_sms_provider_registry.py](../../tests/test_sms_provider_registry.py) — 6 |
| **Offline-сюита** | **260 passed, 9 skipped** ✅ (было 254 → +6) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-10, pkg-000022) | Факт | Статус |
|--------------------------------|------|--------|
| t01 sms sender port dto error codes | `SmsSenderPort` + `SmsSendResult` + `SmsSenderError`/`SmsErrorCode` (9 кодов: delivery/transport + OTP) ([base.py:8-42](../../src/core/phone/base.py)) | 🟢 |
| t02 sms descriptor provider runtime | `SmsProviderDescriptor` (`name`/`config_spec`/`build`, `__post_init__` guard непустого имени) + `SmsProviderRuntime` ([descriptor.py:18-26](../../src/core/phone/descriptor.py), [runtime.py](../../src/core/phone/runtime.py)) | 🟢 |
| t03 sms registry builder guard | `SmsSenderRegistry.get` → `SmsProviderNotRegisteredError` с перечнем; `build_sms_registry` (active + mock); `registered_sms_provider_names` ([registry.py:16-22](../../src/core/phone/registry.py), [registry_builder.py:24-40](../../src/core/phone/registry_builder.py)) | 🟢 |
| t04 mock sms sender descriptor | `MockSmsSender` собирается через `MOCK_SMS_DESCRIPTOR.build`; capture сообщений ([mock/descriptor.py:16-23](../../src/core/phone/mock/descriptor.py)) | 🟢 |
| t05 offline sms registry tests | 6 тестов (names / build / guard.get / guard.get_active / mock.send / send-via-registry) | 🟢 |
| t06 story acceptance verification | AC 5/5 (см. §2); pipeline-story `Status: 🟢 Done` (стр.7) | 🟢 |
| **STORY-IDS-PV-01** | SMS provider backbone + mock | **🟢 Done** |

Индекс держит корректно: Текущая волна pkg-000022 «STORY-IDS-PV-01 🟢» ([bullrun-launch-index.md:11,35](../tasks/bullrun-launch-index.md)).

---

## 2. Сверка Acceptance Criteria story (по коду + тестам)

| AC | Факт (код + тест) | Вердикт |
|----|-------------------|---------|
| `SmsSenderPort` + `SmsSendResult` + `SmsSenderError`/`SmsErrorCode` + дескриптор + `SmsProviderRuntime` + реестр с guard | всё в `core/phone/` ([base.py](../../src/core/phone/base.py), [descriptor.py](../../src/core/phone/descriptor.py), [runtime.py](../../src/core/phone/runtime.py), [registry.py](../../src/core/phone/registry.py)) | ✅ |
| `MockSmsSender` собирается через дескриптор; реестр строит активный + `mock` | `MOCK_SMS_DESCRIPTOR.build` → `MockSmsSender`; `build_sms_registry` всегда добавляет `mock` + active ([registry_builder.py:26-40](../../src/core/phone/registry_builder.py)); тесты `test_build_sms_registry_registers_mock`, `..._mock_send_via_registry` | ✅ |
| `SMS_PROVIDER=<незарегистрированный>` → `SmsProviderNotRegisteredError`/`ConfigError` с перечнем (не голый `KeyError`) | `registry.get` raise с «доступны: …» ([registry.py:17-21](../../src/core/phone/registry.py)); тесты `test_get_unknown_provider_raises_guard_error`, `test_get_active_unknown_provider_raises_guard_error` (match `доступны: mock`) | ✅ |
| Добавление провайдера = +1 дескриптор, без правок ядра | `ALL_SMS_PROVIDER_DESCRIPTORS` tuple → `_DESCRIPTOR_BY_NAME`; `build_sms_registry` итерирует по имени, ядро реестра не знает конкретных провайдеров ([registry_builder.py:8-21](../../src/core/phone/registry_builder.py)) | ✅ |
| Offline-тесты зелёные (guard + сборка + mock.send) | **260 passed, 9 skipped**; 6 dedicated | ✅ |

**Вывод:** все 5 AC выполнены и покрыты тестами (6). Платформа зеркалит eID-бэкбон (EID-03), без OIDC/secret_box — как и задумано scope'ом.

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F1** | MEDIUM | Doc-stale | Backlog-story `Status: ⚪ Todo` (стр.6) + AC `[ ]` (стр.35-39) — реально 🟢 Done под pkg-000022. Та же рассинхронизация в [`EPIC-IDS-PHONE.md:22`](../tasks/backlog-stories/phone-verification/EPIC-IDS-PHONE.md) (строка PV-01 в таблице stories = ⚪ Todo). **Как закрыть:** Status ⚪→🟢, AC `[ ]`→`[x]`, строка таблицы EPIC.md PV-01 → 🟢. Рекуррентный паттерн (как EID-04…08). | [`STORY-IDS-PV-01...md:6,35-39`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md) |
| **F2** | LOW | Doc-stale | Индекс декларирует «259 pytest offline» ([bullrun-launch-index.md:11](../tasks/bullrun-launch-index.md)), фактически **260 passed**. Off-by-one (тот же тип, что F2 EID-08-аудита). **Как закрыть:** синхронизировать число. | [`bullrun-launch-index.md:11`](../tasks/bullrun-launch-index.md) |

Иных материальных findings нет. Наблюдения (severity none, по scope, **не gap**):
- **Нет поля `config.sms_provider`** в `AppConfig` ([schema.py](../../src/core/config/schema.py) — grep пуст). `registry_builder`/`get_active` читают `getattr(config, "sms_provider", "mock")` → дефолт `mock`. Корректно: конфиг-поля/`SMS_PROVIDER`/`PHONE_ALLOWED_DIAL_PREFIXES` — **явно вне scope PV-01**, отнесены к [PV-02](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-02-provider-owned-config.md). Защитный `getattr` — корректный мост до PV-02.
- **`SmsErrorCode` включает OTP-коды** (`CODE_MISMATCH`/`CODE_EXPIRED`/`TOO_MANY_ATTEMPTS`), которые в PV-01 ещё не используются (OTP-движок — [PV-03](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md)). Канон заведён целиком заранее — соответствует scope story (полный `SmsErrorCode`).
- **Переиспользование `ProviderConfigSpec`/`noop_provider_settings_loader`** из eID-пакета ([providers/config_spec.py:17,32](../../src/core/providers/config_spec.py)) вместо дубля — DRY, зеркало платформы.
- **Эпик-ключ — два имени:** backlog `EPIC-IDS-PHONE`, pipeline/индекс/pkg `EPIC-IDS-10`. Согласовано явно: pipeline-epic декларирует `Alias (код/backlog): EPIC-IDS-PHONE` ([EPIC-IDS-10-phone-verification.md:3](../tasks/epics/EPIC-IDS-10-phone-verification/EPIC-IDS-10-phone-verification.md)). Backlog-story Meta несёт только `EPIC-IDS-PHONE` (без двойного ключа, в отличие от EID-стори «EPIC-IDS-09 (alias EPIC-IDS-EID)») — не противоречие, т.к. alias задокументирован в pipeline-epic.

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **260 passed, 9 skipped** (было 254 → +6 SMS-тестов), **ожидаемо** |
| Новый пакет `core/phone/` | полностью аддитивный; ничего из существующего кода не импортирует phone, кроме теста |
| Переиспованный `ProviderConfigSpec` | импорт из `core/providers/config_spec` — read-only, eID-пакет не изменён |
| `AppConfig`/конфиг | **не трогался** (поля sms — в PV-02); существующие config-тесты зелёные |
| Сеть в offline | нет (`http_client=None` в mock-рантайме; mock пишет в память) |
| eID/OAuth/auth-флоу | не затронуты — сюита зелёная |

Регрессий не выявлено.

---

## 5. Итог

- **STORY-IDS-PV-01 — 🟢 исполнена полно:** provider-agnostic SMS-бэкбон (`SmsSenderPort`/`SmsSendResult`/`SmsSenderError`/`SmsErrorCode`, дескриптор+guard, `SmsProviderRuntime`, реестр+builder, `MockSmsSender`), зеркалит eID-платформу (EID-03) без OIDC/secret_box. AC 5/5, 6 тестов. Фундамент EPIC-IDS-10 заложен.
- **Findings:** **F1 (MEDIUM, doc-stale)** — backlog-story + EPIC.md таблица ⚪→🟢 (рекуррентно); **F2 (LOW)** — индекс 259 vs факт 260 offline.
- Наблюдения (нет `config.sms_provider` → PV-02; OTP-коды заведены под PV-03; DRY-переиспользование `config_spec`; alias EPIC-IDS-PHONE/EPIC-IDS-10) — по scope, не gaps.

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; 6 тасков + story сверены по коду (pipeline-story 🟢).
- [x] AC 5/5 сверены по коду **и** тестам; guard проверен на двух путях (`get` и `get_active`).
- [x] Регрессий нет; 254→260 (+6) объяснён; offline без сети (`http_client=None`).
- [x] Границы scope прослежены: отсутствие `config.sms_provider` атрибутировано PV-02, OTP-коды — PV-03, Telnyx — PV-06 (не gaps PV-01).
- [x] Эпик-ключевой дубль (PHONE/IDS-10) проверен — alias задекларирован в pipeline-epic, не противоречие.
