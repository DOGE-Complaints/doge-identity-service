# STORY-IDS-PV-01 — Plugin-платформа SMS-провайдеров + канон контракта

## Meta
- **Key:** `STORY-IDS-PV-01-phone-provider-backbone`
- **Parent Epic:** [`../../../../EPIC-IDS-10-phone-verification.md`](../../../../EPIC-IDS-10-phone-verification.md)
- **Epic alias (код/backlog):** `EPIC-IDS-PHONE`
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md`](../../../../backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md)
- **Decision Ref:** [`../../../../backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md`](../../../../backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md); [`phone-verification-architecture-2026-06-10.md`](../../../../../analysis/phone-verification-architecture-2026-06-10.md) §3, §6
- **Источник:** [`phone-verification-architecture-2026-06-10.md`](../../../../../analysis/phone-verification-architecture-2026-06-10.md) §3, §6
- **Зависит от:** — (фундамент; зеркалит готовую eID-платформу)

## Зачем простыми словами
Фундамент модульности: «разъём» для SMS-провайдеров, в который можно вставить любого (Telnyx, потом другие), а активный выбирается в `.env`. Провайдер **тонкий** — умеет только доставить SMS; генерация и сверка кода живут в ядре. Это зеркало готовой eID-платформы ([EID-03](../../../../backlog-stories/eid/STORY-IDS-EID-03-provider-plugin-backbone.md)), но без OIDC/secret_box.

## Scope
Новый пакет `src/core/phone/`:
- **`SmsSenderPort`** (Protocol): `provider_name: str`, `send(*, to_e164: str, text: str) -> SmsSendResult`; при сбое — `raise SmsSenderError(message, code: SmsErrorCode)`.
- DTO: `SmsSendResult(provider_message_id: str | None, accepted: bool)`.
- **Канон ошибок `SmsErrorCode` (StrEnum):** `INVALID_PHONE`, `COUNTRY_NOT_ALLOWED`, `RATE_LIMITED`, `PROVIDER_UNAVAILABLE`, `SEND_FAILED`, `CODE_MISMATCH`, `CODE_EXPIRED`, `TOO_MANY_ATTEMPTS`, `UNKNOWN` (delivery/transport — провайдер; OTP-сверка — ядро).
- **`SmsProviderDescriptor`** (`name`, `config_spec`, `build(runtime) -> SmsSenderPort`) + **`SmsProviderRuntime`** (DI-bundle: `config`, `http_client: httpx.Client`, `settings`) + **`SmsSenderRegistry`** + `build_sms_registry(runtime)` + guard `SmsProviderNotRegisteredError(ConfigError)`.
- **`MockSmsSender`** (dev: «отправка» в память/лог, всегда `accepted=True`) — эталон + образец для тестов.

## Вне scope
- Конфиг-поля/валидация — [PV-02](../../../../backlog-stories/phone-verification/STORY-IDS-PV-02-provider-owned-config.md).
- OTP/сессия/флоу — [PV-03](../../../../backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md)/[PV-05](../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md).
- Реальный Telnyx — [PV-06](../../../../backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md).

## Точки в коде (образец-зеркало eID, Done)
- Порт/DTO/ошибки: [`providers/base.py`](../../../../../../src/core/providers/base.py) (`EIDProviderPort`, `EidErrorCode`).
- Дескриптор + guard: [`providers/descriptor.py`](../../../../../../src/core/providers/descriptor.py) (`EIDProviderDescriptor`, `ProviderNotRegisteredError`).
- DI-рантайм: [`providers/runtime.py`](../../../../../../src/core/providers/runtime.py).
- Реестр + сборка активного+mock: [`providers/registry.py`](../../../../../../src/core/providers/registry.py), [`registry_builder.py`](../../../../../../src/core/providers/registry_builder.py).
- Mock-эталон: [`providers/mock/mock_provider.py`](../../../../../../src/core/providers/mock/mock_provider.py).
- `ConfigError`: [`config/errors.py`](../../../../../../src/core/config/errors.py).

## Точки в коде (реализовано)
- Порт/DTO/ошибки: [`phone/base.py`](../../../../../../src/core/phone/base.py).
- Дескриптор + guard: [`phone/descriptor.py`](../../../../../../src/core/phone/descriptor.py).
- DI-рантайм: [`phone/runtime.py`](../../../../../../src/core/phone/runtime.py).
- Реестр + сборка: [`phone/registry.py`](../../../../../../src/core/phone/registry.py), [`phone/registry_builder.py`](../../../../../../src/core/phone/registry_builder.py).
- Mock-эталон: [`phone/mock/mock_sender.py`](../../../../../../src/core/phone/mock/mock_sender.py), [`phone/mock/descriptor.py`](../../../../../../src/core/phone/mock/descriptor.py).
- Тесты: [`test_sms_provider_registry.py`](../../../../../../tests/test_sms_provider_registry.py).

## Acceptance Criteria
- [x] Есть `SmsSenderPort` + `SmsSendResult` + `SmsSenderError`/`SmsErrorCode` + дескриптор + `SmsProviderRuntime` + реестр с guard.
- [x] `MockSmsSender` собирается через дескриптор; реестр строит активный + `mock`.
- [x] `SMS_PROVIDER=<незарегистрированный>` → `SmsProviderNotRegisteredError`/`ConfigError` с перечислением доступных (не голый `KeyError`).
- [x] Добавление провайдера = +1 дескриптор, без правок ядра реестра.
- [x] Offline-тесты зелёные (guard + сборка реестра + mock.send).

## Парадигма-якорь
[06-eid-providers](../../../../../runtime-docs/06-eid-providers.md) (модульность провайдеров), [03-soa-roles](../../../../../runtime-docs/03-soa-roles.md) (DI/фабрика).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-10-01-t01-sms-sender-port-dto-error-codes`](./task-ids-10-01-t01-sms-sender-port-dto-error-codes/README.md) | pkg-000022 |
| 2 | [`task-ids-10-01-t02-sms-descriptor-provider-runtime`](./task-ids-10-01-t02-sms-descriptor-provider-runtime/README.md) | pkg-000022 |
| 3 | [`task-ids-10-01-t03-sms-registry-builder-guard`](./task-ids-10-01-t03-sms-registry-builder-guard/README.md) | pkg-000022 |
| 4 | [`task-ids-10-01-t04-mock-sms-sender-descriptor`](./task-ids-10-01-t04-mock-sms-sender-descriptor/README.md) | pkg-000022 |
| 5 | [`task-ids-10-01-t05-offline-sms-registry-tests`](./task-ids-10-01-t05-offline-sms-registry-tests/README.md) | pkg-000022 |
| 6 | [`task-ids-10-01-t06-story-acceptance-verification`](./task-ids-10-01-t06-story-acceptance-verification/README.md) | pkg-000022 |
