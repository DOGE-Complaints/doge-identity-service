# STORY-IDS-PV-05 — Flow API: request/confirm + rate-limit + аудит

## Meta
- **Key:** `STORY-IDS-PV-05-verification-flow-api`
- **Parent Epic:** [`../../../../EPIC-IDS-10-phone-verification.md`](../../../../EPIC-IDS-10-phone-verification.md)
- **Epic alias (код/backlog):** `EPIC-IDS-PHONE`
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md`](../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md)
- **Decision Ref:** [`../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md`](../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md); [`phone-verification-architecture-2026-06-10.md`](../../../../../analysis/phone-verification-architecture-2026-06-10.md) §5, §10
- **Источник:** [`phone-verification-architecture-2026-06-10.md`](../../../../../analysis/phone-verification-architecture-2026-06-10.md) §5, §10
- **Зависит от:** [STORY-IDS-PV-02-provider-owned-config](../STORY-IDS-PV-02-provider-owned-config/STORY-IDS-PV-02-provider-owned-config.md), [STORY-IDS-PV-03-otp-engine-session](../STORY-IDS-PV-03-otp-engine-session/STORY-IDS-PV-03-otp-engine-session.md), [STORY-IDS-PV-04-profile-flag-migration](../STORY-IDS-PV-04-profile-flag-migration/STORY-IDS-PV-04-profile-flag-migration.md), [STORY-IDS-PV-01-phone-provider-backbone](../STORY-IDS-PV-01-phone-provider-backbone/STORY-IDS-PV-01-phone-provider-backbone.md)

## Зачем простыми словами
Сам пользовательский флоу из двух обычных вызовов (без браузерного redirect, в отличие от eID): `request` — проверить номер, сгенерировать код, отправить SMS; `confirm` — сверить код и поставить флаг. Плюс защита от спама SMS (повтор не чаще, чем раз в N секунд) и аудит каждого шага.

## Scope
- **`POST /auth/phone/request`** (Bearer JWT): нормализовать номер → префикс ∈ `PHONE_ALLOWED_DIAL_PREFIXES`? (иначе `COUNTRY_NOT_ALLOWED`) → rate-limit (`PHONE_RESEND_COOLDOWN_S`, инвалидация прежнего кода) → OTP+сессия (PV-03) → `registry.get_active().send(to_e164, text)` → ответ `{ sent: true, expires_at }`. Текст SMS формирует ядро (с кодом).
- **`POST /auth/phone/confirm`** (Bearer JWT): найти активную сессию пользователя → сверка кода (PV-03) → `attach_phone_verification` (PV-04, дедуп→409) → `mark_consumed` → ответ `{ status: "verified" }`.
- **Оркестратор-хендлеры** `handle_phone_request` / `handle_phone_confirm` (по образцу [`handlers.py`](../../../../../../src/core/api/handlers.py)); ошибки провайдера (`SmsSenderError`) → канон `SmsErrorCode` в ответе (по образцу eID `except EIDProviderError`).
- **Аудит** каждого события без PII (по образцу `_log_eid_audit`/`EIDAuditEvent`; зеркальный `PhoneAuditEvent` или общий — решить при реализации, рекомендую отдельный).
- **Привязка по сессии**, а не по браузеру (`supabase_user_id` из JWT) — принцип session-binding, как в eID.

## Вне scope
- Telnyx-специфика отправки — [PV-06](../../../../backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md) (флоу работает на `MockSmsSender`).
- Приём статусов доставки — [PV-07](../../../../backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md).

## Точки в коде (образец eID)
- Оркестрация start/confirm-аналог: [`handlers.py`](../../../../../../src/core/api/handlers.py) (`handle_auth_eid_start`/`handle_auth_eid_callback`, разбор `EIDProviderError`).
- Конверты ответов: [`api/envelope.py`](../../../../../../src/core/api/envelope.py) (`build_success_envelope`/`build_error_envelope`).
- Аудит: `_log_eid_audit` ([`handlers.py:83-111`](../../../../../../src/core/api/handlers.py)), `EIDAuditLogRepository` ([`contracts.py:58`](../../../../../../src/core/domain/contracts.py)).
- Роуты + DI: [`asgi_app.py`](../../../../../../src/core/api/asgi_app.py), [`dependencies.py`](../../../../../../src/core/api/dependencies.py), [`service_factory.py`](../../../../../../src/core/infrastructure/service_factory.py) (добавить phone-сервисы в фабрику/DI).
- Bearer-auth: `get_current_user` ([`api/security.py`](../../../../../../src/core/api/security.py)).

## Acceptance Criteria
- [x] `POST /auth/phone/request` (валидный JWT, разрешённый префикс) → создаёт сессию `started`, шлёт SMS через активный провайдер, возвращает `expires_at`.
- [x] Неразрешённый префикс → `COUNTRY_NOT_ALLOWED`; повтор раньше cooldown → `RATE_LIMITED` (старый код инвалидирован при новом).
- [x] `POST /auth/phone/confirm` верный код → `phone_verified=true`; неверный/просрочка/лимит → корректные `SmsErrorCode`; дубль номера → 409.
- [x] Все события в аудите без PII (нет сырого номера/кода).
- [x] Полный флоу проходит на `MockSmsSender` офлайн-тестом.

## Парадигма-якорь
[01-api](../../../../../runtime-docs/01-api.md) (контракты эндпоинтов), [04-security](../../../../../runtime-docs/04-security.md) (session-binding, anti-abuse), [06-eid-providers](../../../../../runtime-docs/06-eid-providers.md).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-10-05-t01-phone-audit-event-repository`](./task-ids-10-05-t01-phone-audit-event-repository/README.md) | pkg-000026 |
| 2 | [`task-ids-10-05-t02-phone-services-di-wiring`](./task-ids-10-05-t02-phone-services-di-wiring/README.md) | pkg-000026 |
| 3 | [`task-ids-10-05-t03-handle-phone-request-orchestrator`](./task-ids-10-05-t03-handle-phone-request-orchestrator/README.md) | pkg-000026 |
| 4 | [`task-ids-10-05-t04-handle-phone-confirm-orchestrator`](./task-ids-10-05-t04-handle-phone-confirm-orchestrator/README.md) | pkg-000026 |
| 5 | [`task-ids-10-05-t05-asgi-routes-offline-flow-tests`](./task-ids-10-05-t05-asgi-routes-offline-flow-tests/README.md) | pkg-000026 |
| 6 | [`task-ids-10-05-t06-story-acceptance-verification`](./task-ids-10-05-t06-story-acceptance-verification/README.md) | pkg-000026 |
