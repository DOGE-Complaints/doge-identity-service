# Жёсткий аудит исполнения STORY-IDS-PV-06 (Telnyx SMS sender)

> **Дата:** 2026-06-11
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-PV-06-telnyx-sms-sender`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md) vs фактический код. Исполнена под **EPIC-IDS-10-phone-verification** (alias `EPIC-IDS-PHONE`), pkg-000027, 6 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): Текущая волна pkg-000027, STORY-IDS-PV-06 🟢 (стр.11,45,527-532).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Пакет | `src/core/phone/telnyx/`: `config.py`, `sender.py`, `errors.py`, `descriptor.py`, `__init__.py` |
| Config + spec | `TelnyxSettings` + `TelnyxSmsProviderConfigSpec` + `validate_telnyx_config` (условная: alphanumeric from → profile_id required) ([config.py:24-79](../../src/core/phone/telnyx/config.py)) |
| Sender | `TelnyxSmsSender.send` → `POST {base}/v2/messages` Bearer, `{from,to,text,type,messaging_profile_id?,encoding?}`; 200+`data.id`+status∈{queued,sent} → `accepted` ([sender.py:21-76](../../src/core/phone/telnyx/sender.py)) |
| Маппинг ошибок | `map_telnyx_error`/`map_telnyx_timeout`/`extract_telnyx_error_codes` → канон `SmsErrorCode` ([errors.py](../../src/core/phone/telnyx/errors.py)) |
| Дескриптор + регистрация | `TELNYX_SMS_DESCRIPTOR` в `ALL_SMS_PROVIDER_DESCRIPTORS` ([descriptor.py:18-22](../../src/core/phone/telnyx/descriptor.py), [registry_builder.py:9-14](../../src/core/phone/registry_builder.py)) |
| Рантайм | non-mock → `httpx.Client` + `config_spec.load(...)` в `settings["telnyx"]` ([runtime_factory.py:13-26](../../src/core/phone/runtime_factory.py)) |
| `.env.example` | `TELNYX_*` блок ([.env.example:72-77](../../.env.example)) |
| Тесты | [test_telnyx_sms_sender.py](../../tests/test_telnyx_sms_sender.py) — 15 (14 offline + 1 live-skip) |
| **Offline-сюита** | **315 passed, 10 skipped** ✅ (было 299 → +16; live-тест в skip) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-10, pkg-000027) | Факт | Статус |
|--------------------------------|------|--------|
| t01 telnyx settings + config spec | `TelnyxSettings.load`, `TelnyxSmsProviderConfigSpec` (required/defaults/loader+validate), условная валидация alphanumeric→profile_id ([config.py](../../src/core/phone/telnyx/config.py)) | 🟢 |
| t02 telnyx sms sender http send | `TelnyxSmsSender.send` POST v2/messages Bearer; 200+`data.id`+queued/sent → `SmsSendResult` ([sender.py:21-76](../../src/core/phone/telnyx/sender.py)) | 🟢 |
| t03 telnyx error code mapping | таблица кодов спеки → `COUNTRY_NOT_ALLOWED`/`RATE_LIMITED`/`PROVIDER_UNAVAILABLE`/`INVALID_PHONE`/`SEND_FAILED`/`UNKNOWN`; 429→rate, 5xx/timeout→unavailable; лог без PII ([errors.py:11-83](../../src/core/phone/telnyx/errors.py)) | 🟢 |
| t04 telnyx descriptor + registry + runtime | дескриптор зарегистрирован; non-mock рантайм грузит settings+http_client ([descriptor.py](../../src/core/phone/telnyx/descriptor.py), [registry_builder.py:11](../../src/core/phone/registry_builder.py), [runtime_factory.py](../../src/core/phone/runtime_factory.py)) | 🟢 |
| t05 offline telnyx sender tests | 14 offline (mocked httpx) + 1 live-skip | 🟢 |
| t06 story acceptance verification | AC 5/5 (см. §2); pipeline-story `Status: 🟢 Done` (стр.7), индекс t06 🟢 ([bullrun-launch-index.md:532](../tasks/bullrun-launch-index.md)) | 🟢 |
| **STORY-IDS-PV-06** | Telnyx SMS sender | **🟢 Done** |

Индекс держит эпик корректно: `EPIC-IDS-10 … 🟡 In Progress — PV-01..PV-06 🟢` ([bullrun-launch-index.md:90](../tasks/bullrun-launch-index.md)).

---

## 2. Сверка Acceptance Criteria story (по коду + тестам)

| AC | Факт (код + тест) | Вердикт |
|----|-------------------|---------|
| `SMS_PROVIDER=telnyx`(+creds) → `get_active()`=`TelnyxSmsSender`; без env / alphanumeric-from без profile_id → `ConfigError` | регистрация+`get_active` ([registry_builder.py](../../src/core/phone/registry_builder.py)); `validate_telnyx_config` ([config.py:24-34](../../src/core/phone/telnyx/config.py)); тесты `test_build_sms_registry_active_telnyx`, `..._requires_api_key`, `..._alphanumeric_from_requires_profile_id` | ✅ (с оговоркой F3 о env-источнике) |
| `send` → POST (Bearer, from/to/text/type, profile_id при alphanumeric); 200+`queued` → `accepted`+`provider_message_id` | [sender.py:23-52](../../src/core/phone/telnyx/sender.py); тест `test_telnyx_send_success_queued` (проверяет URL/Bearer/тело/`msg-queued`) | ✅ |
| Ошибки Telnyx → `SmsErrorCode` по таблице; сырой код/номер не логируется | [errors.py:56-83](../../src/core/phone/telnyx/errors.py); тесты `..._maps_country_not_allowed/rate_limited/provider_unavailable_on_5xx/invalid_phone/send_failed`, `..._missing_data_id_maps_unknown`, `..._parses_errors_array_fields`, `..._does_not_log_otp_text` | ✅ |
| Юнит offline (mocked httpx) зелёные; live-тест skip без creds | `httpx.MockTransport`; `test_telnyx_live_send_skips_without_credentials` (skip без `TELNYX_API_KEY`/`PROFILE_ID`) | ✅ |
| `.env.example` содержит `TELNYX_*` | [.env.example:72-77](../../.env.example) | ✅ |

**Вывод:** все 5 AC функционально выполнены и покрыты тестами (15). Тонкий боевой провайдер по спеке Telnyx; OTP остаётся в ядре. **Оговорка:** AC1 в реальном деплое зависит от источника env — см. F3.

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F3** | MEDIUM | Config-source inconsistency / integration gap | `AppConfig` строится из `environ` **+ merge cwd `.env`** ([providers.py:11-15](../../src/core/config/providers.py) — `merge_dotenv_from_cwd`, **без** мутации `os.environ`), но Telnyx-настройки грузятся из **сырого `os.environ`**: `descriptor.config_spec.load(os.environ)` ([runtime_factory.py:24](../../src/core/phone/runtime_factory.py)). Если `TELNYX_*` заданы только в cwd `.env` (как описывает [`.env.example:72-77`](../../.env.example)), то `config.sms_provider="telnyx"` резолвится из merged-source и проходит load-time валидацию, **но** `build_sms_provider_runtime` затем зовёт `validate_telnyx_config(os.environ)` → `ConfigError: TELNYX_API_KEY missing` на старте, хотя ключ есть в `.env`. В тесте замаскировано `patch.dict(os.environ, _minimal_env())` ([test:114](../../tests/test_telnyx_sms_sender.py)). Расходится с eID, где провайдер-настройки из `os.environ` не грузятся ([providers/runtime_factory.py](../../src/core/providers/runtime_factory.py)). **Как закрыть:** грузить настройки активного провайдера из того же merged-источника, что и `provide_app_config` (пробросить resolved env/source в `build_sms_provider_runtime`), а не из `os.environ`; добавить тест с `.env`-only creds (без `patch.dict(os.environ)`). | [`runtime_factory.py:24`](../../src/core/phone/runtime_factory.py) |
| **F1** | MEDIUM | Doc-stale | Backlog-story `Status: ⚪ Todo` (стр.6) + AC `[ ]` (стр.32-36) — реально 🟢 Done под pkg-000027. Та же рассинхронизация в [`EPIC-IDS-PHONE.md`](../tasks/backlog-stories/phone-verification/EPIC-IDS-PHONE.md) (строка PV-06 = ⚪ Todo). **Как закрыть:** Status ⚪→🟢, AC `[ ]`→`[x]`, строка таблицы EPIC.md PV-06 → 🟢. Рекуррентный паттерн (PV-01..05). | [`STORY-IDS-PV-06...md:6,32-36`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md) |
| **F2** | LOW | Doc-stale | Индекс декларирует «314 pytest offline» ([bullrun-launch-index.md:11](../tasks/bullrun-launch-index.md)), фактически **315 passed** (off-by-one). **Как закрыть:** синхронизировать число. | [`bullrun-launch-index.md:11`](../tasks/bullrun-launch-index.md) |

Иных материальных findings нет. Наблюдения (severity none, по scope, **не gap**):
- **`TelnyxSmsProviderConfigSpec` — отдельный класс** (не алиас `ProviderConfigSpec`, в отличие от mock/PV-02), т.к. нужен типизированный `TelnyxSettings`-loader + условная валидация. Использует `_env_value` из общего `config_spec` — частичное переиспользование. Корректно.
- **Двойная защита alphanumeric-from→profile_id:** на уровне config (`validate_telnyx_config`) и в `send` (если нет profile_id и from не E.164 → `SEND_FAILED`, [sender.py:30-34](../../src/core/phone/telnyx/sender.py)). Избыточно, но безвредно (defense-in-depth).
- **Маппинг кодов — фиксированные frozenset'ы** ([errors.py:11-33](../../src/core/phone/telnyx/errors.py)); конкретные коды (10002/40012/…) сверены со story-таблицей рамочно (явные из story: 40309/40331→country, 10011/40318→rate, 429→rate, 5xx/timeout→unavailable, no `data.id`→UNKNOWN — все ✅). Полная сверка с §3 спеки — вне объёма code-аудита (спека = внешний источник).
- **Webhook/delivery-статусы** не реализованы — **вне scope PV-06** ([PV-07](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md)).

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **315 passed, 10 skipped** (было 299 → +16; +1 skip = live Telnyx) **ожидаемо** |
| Новый пакет `telnyx/` | аддитивный; mock-провайдер и ядро не изменены |
| `ALL_SMS_PROVIDER_DESCRIPTORS` | +`TELNYX_SMS_DESCRIPTOR`; `registered_sms_provider_names()` теперь `{mock, telnyx}` → `SMS_PROVIDER=telnyx` проходит членство в `schema.py` |
| `runtime_factory` | non-mock-ветка активируется впервые (для mock остаётся `settings={}`, http_client=None) |
| Флоу PV-05 на mock | не затронут (mock-ветка без изменений) — сюита зелёная |
| eID/OAuth/PV-01..05 | не затронуты |

Регрессий не выявлено. **F3 — латентный (не регресс):** проявляется только при `SMS_PROVIDER=telnyx` с creds в cwd `.env` (в проде с реальным process-env работает).

---

## 5. Итог

- **STORY-IDS-PV-06 — 🟢 исполнена (с одной материальной оговоркой):** `TelnyxSmsSender` (POST v2/messages, Bearer, success queued/sent→`accepted`), полный маппинг ошибок→`SmsErrorCode` без PII в логах, условная config-валидация, дескриптор зарегистрирован, `.env.example` дополнен. AC 5/5 функционально, 15 тестов (live-skip).
- **Findings:** **F3 (MEDIUM)** — Telnyx-настройки грузятся из `os.environ`, а `AppConfig` — из `environ + cwd .env` merge: при `.env`-only creds старт упадёт `ConfigError`, в тесте замаскировано `patch.dict`; **F1 (MEDIUM, doc-stale)** — backlog-story + EPIC.md ⚪→🟢; **F2 (LOW)** — индекс 314 vs факт 315.
- Наблюдения (отдельный config-spec; двойная alphanumeric-защита; коды-frozenset; webhook→PV-07) — по scope, не gaps.

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; 6 тасков + story сверены по коду (pipeline-story 🟢, индекс t01–t06 🟢).
- [x] AC 5/5 сверены по коду **и** тестам; маппинг ошибок проверен на 6 ветках + no-OTP-log.
- [x] **Config-source consistency** проверен (analysis.mdc §1/§4): найдено расхождение `os.environ` vs merged-source → F3 (MEDIUM), подтверждено маскировкой через `patch.dict` в тесте.
- [x] Change propagation: telnyx проведён descriptor→registry_builder→runtime_factory→`registered_sms_provider_names`→schema-членство.
- [x] Регрессий нет; 299→315 (+16) объяснён; F3 классифицирован как латентный (условие: `.env`-only creds).
