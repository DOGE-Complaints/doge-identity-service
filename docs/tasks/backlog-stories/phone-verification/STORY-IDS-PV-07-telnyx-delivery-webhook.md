# STORY-IDS-PV-07 — Telnyx delivery webhook ingestion (MVP)

## Meta
- **Key:** `STORY-IDS-PV-07-telnyx-delivery-webhook`
- **Epic:** `EPIC-IDS-PHONE`
- **Status:** 🟢 Done (pkg-000028; [`asgi_app.py`](../../../../src/core/api/asgi_app.py) `/webhooks/telnyx/messaging`)
- **Источник:** [`phone-verification-architecture-2026-06-10.md`](../../../analysis/phone-verification-architecture-2026-06-10.md) §10.1 (P2); спека Telnyx §2.7, §6.2
- **Зависит от:** [PV-06](STORY-IDS-PV-06-telnyx-sms-sender.md) (есть `provider_message_id`)

## Зачем простыми словами
`send` подтверждает только, что Telnyx **принял** SMS в очередь. Финальный факт «доставлено/не доставлено на телефон» Telnyx присылает позже отдельным уведомлением — **webhook** (Telnyx сам стучится на наш URL). По продуктовому решению (P2) принимаем эти уведомления уже в MVP — для наблюдаемости и борьбы с фродом. На сам флоу верификации это не влияет (код всё равно подтверждает пользователь).

## Scope
- **Эндпоинт** `POST /webhooks/telnyx/messaging` (публичный, без Bearer — это сервер Telnyx): принимает события `message.sent` / `message.delivered` / `message.finalized`.
- **Верификация подлинности** входящего webhook (Telnyx подписывает запросы — Ed25519 signature header; точный механизм подтвердить по спеке/докам в [SPIKE-PV-08](SPIKE-IDS-PV-08-telnyx-account-setup.md)). Без валидной подписи → 401/403, не обрабатываем.
- **Хранение статуса доставки** по `provider_message_id`: таблица/поле `delivery_status` (`queued|sent|delivered|failed|gw_timeout|dlr_timeout`) + `delivery_updated_at`; связать с `PhoneVerificationSession.provider_message_id` (PV-03).
- **Идемпотентность приёма:** повторное событие по тому же id не ломает состояние; принимаем только «вперёд» по финальности.
- **Аудит** события доставки (без PII).

## Вне scope
- Логика верификации/флаг профиля — PV-03/04/05 (доставка их не меняет).
- Ретраи отправки на основе `failed` — отдельное продуктовое решение позже (можно показать пользователю «не дошло, отправить ещё раз»).

## Точки в коде (образец)
- Публичные роуты/эндпоинты: [`asgi_app.py`](../../../../src/core/api/asgi_app.py) (регистрация маршрутов, без `get_current_user`).
- `provider_message_id` в сессии: [PV-03](STORY-IDS-PV-03-otp-engine-session.md).
- Аудит: `EIDAuditLogRepository`-образец [`contracts.py:58`](../../../../src/core/domain/contracts.py).
- Статусы доставки Telnyx + подпись webhook: спека [`telnyx-integration-spec-dogestonia-2026-06-10.md`](../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md) §2.7 (+ уточнить подпись на SPIKE).

## Acceptance Criteria
- [ ] `POST /webhooks/telnyx/messaging` принимает события и обновляет `delivery_status` по `provider_message_id`.
- [ ] Невалидная/отсутствующая подпись Telnyx → отклонение (401/403), не обрабатываем.
- [ ] Повторное/устаревшее событие идемпотентно (не откатывает финальный статус).
- [ ] Событие доставки пишется в аудит без PII.
- [ ] Offline-тесты: валидный/невалидный webhook, идемпотентность, маппинг статусов.

## Парадигма-якорь
[01-api](../../../runtime-docs/01-api.md) (webhook-контракт), [04-security](../../../runtime-docs/04-security.md) (валидация подписи, без PII).
