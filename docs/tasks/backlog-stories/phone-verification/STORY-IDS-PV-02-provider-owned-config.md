# STORY-IDS-PV-02 — Provider-owned config + выбор активного + allowlist префиксов

## Meta
- **Key:** `STORY-IDS-PV-02-provider-owned-config`
- **Epic:** `EPIC-IDS-PHONE`
- **Status:** 🟢 Done (pkg-000023; [`registry_builder.py`](../../../../src/core/phone/registry_builder.py), [`schema.py`](../../../../src/core/config/schema.py) `SMS_PROVIDER`)
- **Источник:** [`phone-verification-architecture-2026-06-10.md`](../../../analysis/phone-verification-architecture-2026-06-10.md) §7, §10.2
- **Зависит от:** [PV-01](STORY-IDS-PV-01-phone-provider-backbone.md) (`config_spec` живёт в дескрипторе)

## Зачем простыми словами
Каждый SMS-провайдер сам объявляет свои настройки и сам себя проверяет, а ядро только выбирает активного по `.env` и держит **список разрешённых дозвонных префиксов** (например `+372`). Зеркало eID-конфига ([EID-04](../eid/STORY-IDS-EID-04-provider-owned-config.md)).

## Scope
- **`SmsProviderConfigSpec`** (часть дескриптора): `required`, `optional_defaults`, `load(env) -> <Settings>` (по образцу [`config_spec.py`](../../../../src/core/providers/config_spec.py)).
- **Ядро (provider-agnostic) env:** `SMS_PROVIDER` (членство по реестру дескрипторов), `PHONE_ALLOWED_DIAL_PREFIXES` (список E.164-префиксов, фильтр **в ядре**), плюс параметры OTP/rate-limit (используются в PV-03/05): `PHONE_CODE_LENGTH=6`, `PHONE_CODE_TTL_S=300`, `PHONE_MAX_ATTEMPTS=5`, `PHONE_RESEND_COOLDOWN_S=60`, `PHONE_ONE_ACCOUNT_PER_NUMBER=true`.
- **Утилита нормализации в E.164** + проверка дозвонного префикса (`+372`) → при несовпадении ядро вернёт `COUNTRY_NOT_ALLOWED` (до отправки SMS).
- **Делегированная валидация:** на старте `descriptor.config_spec.validate(env)` активного → fail-fast `ConfigError` (по образцу [`schema.py`](../../../../src/core/config/schema.py) `_validate_active_eid_provider_config`).
- Дополнить `AppConfig` ядровыми phone-полями; провайдер-специфичные — в settings провайдера (не в `AppConfig`).

## Вне scope
- `TELNYX_*` поля и их settings — [PV-06](STORY-IDS-PV-06-telnyx-sms-sender.md) (со своим `config_spec`, как у Authentigate).
- Использование `RESEND_COOLDOWN`/`MAX_ATTEMPTS` — PV-03/PV-05 (здесь только объявление+валидация).

## Точки в коде (образец eID)
- `ProviderConfigSpec`: [`config_spec.py`](../../../../src/core/providers/config_spec.py).
- Делегированная валидация + членство: [`schema.py`](../../../../src/core/config/schema.py) (`_validate_active_eid_provider_config`, `registered_eid_provider_names`), [`registry_builder.py`](../../../../src/core/providers/registry_builder.py).
- Дефолты env: [`config/providers.py`](../../../../src/core/config/providers.py); `.env.example` (EID-блок как образец).

## Acceptance Criteria
- [ ] `SMS_PROVIDER` валидируется по реестру; неизвестный → понятная `ConfigError`.
- [ ] `PHONE_ALLOWED_DIAL_PREFIXES` парсится; номер с неразрешённым префиксом → `COUNTRY_NOT_ALLOWED` (тест на `+372` ок / `+1` отклонён).
- [ ] Нормализация E.164 покрыта тестами (пробелы/скобки/без `+`).
- [ ] Ядровые phone-параметры доступны ядру; провайдер-поля не в `AppConfig`.
- [ ] `.env.example` дополнен phone-блоком; offline-набор зелёный.

## Парадигма-якорь
[06-eid-providers](../../../runtime-docs/06-eid-providers.md), [04-security](../../../runtime-docs/04-security.md) (минимизация/гейты).
