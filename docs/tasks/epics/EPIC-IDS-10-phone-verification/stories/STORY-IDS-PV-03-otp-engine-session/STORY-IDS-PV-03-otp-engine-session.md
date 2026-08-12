# STORY-IDS-PV-03 — OTP-движок + сессия верификации

## Meta
- **Key:** `STORY-IDS-PV-03-otp-engine-session`
- **Parent Epic:** [`../../../../EPIC-IDS-10-phone-verification.md`](../../../../EPIC-IDS-10-phone-verification.md)
- **Epic alias (код/backlog):** `EPIC-IDS-PHONE`
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md`](../../../../backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md)
- **Decision Ref:** [`../../../../backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md`](../../../../backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md); [`phone-verification-architecture-2026-06-10.md`](../../../../../analysis/phone-verification-architecture-2026-06-10.md) §3, §5, §10.1 (P3)
- **Источник:** [`phone-verification-architecture-2026-06-10.md`](../../../../../analysis/phone-verification-architecture-2026-06-10.md) §3, §5, §10.1 (P3)
- **Зависит от:** [STORY-IDS-PV-01-phone-provider-backbone](../STORY-IDS-PV-01-phone-provider-backbone/STORY-IDS-PV-01-phone-provider-backbone.md) (Done), [STORY-IDS-PV-02-provider-owned-config](../STORY-IDS-PV-02-provider-owned-config/STORY-IDS-PV-02-provider-owned-config.md) (параметры OTP, Done)

## Зачем простыми словами
«Сердце» верификации, которое у eID делал внешний провайдер, а здесь делает наше ядро: сгенерировать одноразовый код, безопасно сохранить его (хэш, не открытым), отмерить срок жизни и считать попытки. Сессия — мост между «запросить код» и «подтвердить код».

## Scope
- **`PhoneVerificationSession`** (модель) + store (`create` / `get_by_id` / `get_active_by_user` / `mark_consumed` / `mark_failed` / `expire_pending`) — зеркало `VerificationSession`/`VerificationSessionStore` ([models.py](../../../../../../src/core/domain/models.py), [contracts.py](../../../../../../src/core/domain/contracts.py)).
  - Поля: `id`, `supabase_user_id`, `phone_hash`, `dial_prefix`, `code_hash`, `status` (`started|consumed|failed|expired`), `attempts`, `created_at`, `expires_at`, `provider`, `provider_message_id` (заполнит PV-06/07).
- **OTP-движок:** генерация кода длины `PHONE_CODE_LENGTH` (криптослучайно, `secrets`), `code_hash = hash_secret(code, key=...)` (переиспользуем [`hashing.py`](../../../../../../src/core/security/hashing.py)), `expires_at = now + PHONE_CODE_TTL_S` (P3: 6 цифр, 300с).
- **Сверка:** функция проверки введённого кода (сравнение хэшей), инкремент `attempts`, лимит `PHONE_MAX_ATTEMPTS` (P3: 5) → `TOO_MANY_ATTEMPTS`; просрочка → `CODE_EXPIRED`; несовпадение → `CODE_MISMATCH`.
- **Инвалидация при повторе:** новый `request` инвалидирует прежний незавершённый код того же пользователя (старый код перестаёт действовать).
- `PhoneVerificationResult(provider, dial_prefix, subject_hash, verified_at)` — `subject_hash = hash_secret(e164)` (без префикса провайдера, анти-Sybil).

## Вне scope
- HTTP-эндпоинты/оркестрация/rate-limit на отправку — [PV-05](../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md).
- Запись флага в профиль и дедуп — [PV-04](../../../../backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md).
- Шифрование кода (нам достаточно хэша — код одноразовый, сверяем сравнением хэшей; `SessionSecretBox` eID-специфичен и не нужен).

## Точки в коде (образец eID)
- Сессия/стор: [`models.py:43-59`](../../../../../../src/core/domain/models.py) (`VerificationSession`), [`contracts.py:43-54`](../../../../../../src/core/domain/contracts.py) (`VerificationSessionStore`).
- In-memory стор-образец: [`infrastructure/repositories.py`](../../../../../../src/core/infrastructure/repositories.py).
- HMAC: [`hashing.py:9`](../../../../../../src/core/security/hashing.py).
- Параметры из PV-02 (`PHONE_CODE_LENGTH/TTL/MAX_ATTEMPTS`).

## Acceptance Criteria
- [x] `PhoneVerificationSession` + store (in-memory + supabase-совместимый интерфейс) с `attempts`.
- [x] OTP генерится криптослучайно, хранится только хэш; код не логируется.
- [x] Сверка: верный код → ok; неверный → `CODE_MISMATCH` + `attempts++`; ≥лимита → `TOO_MANY_ATTEMPTS`; просрочка → `CODE_EXPIRED`.
- [x] Повторный `request` инвалидирует прежний код пользователя.
- [x] `subject_hash = hash_secret(e164)` без провайдер-префикса.
- [x] Offline-тесты: успех/несовпадение/просрочка/лимит/повтор-инвалидация.

## Парадигма-якорь
[04-security](../../../../../runtime-docs/04-security.md) (OTP, хэши, PII), [05-data-model](../../../../../runtime-docs/05-data-model.md) (сессии).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-10-03-t01-phone-verification-session-result-models`](./task-ids-10-03-t01-phone-verification-session-result-models/README.md) | pkg-000024 |
| 2 | [`task-ids-10-03-t02-phone-verification-session-store-inmemory`](./task-ids-10-03-t02-phone-verification-session-store-inmemory/README.md) | pkg-000024 |
| 3 | [`task-ids-10-03-t03-otp-generate-session-create-invalidate`](./task-ids-10-03-t03-otp-generate-session-create-invalidate/README.md) | pkg-000024 |
| 4 | [`task-ids-10-03-t04-otp-verify-attempts-expiry-result`](./task-ids-10-03-t04-otp-verify-attempts-expiry-result/README.md) | pkg-000024 |
| 5 | [`task-ids-10-03-t05-offline-phone-otp-session-tests`](./task-ids-10-03-t05-offline-phone-otp-session-tests/README.md) | pkg-000024 |
| 6 | [`task-ids-10-03-t06-story-acceptance-verification`](./task-ids-10-03-t06-story-acceptance-verification/README.md) | pkg-000024 |
