# SPIKE-IDS-PV-08 — Telnyx account & sender setup (внешнее)

## Meta
- **Key:** `SPIKE-IDS-PV-08-telnyx-account-setup`
- **Epic:** `EPIC-IDS-PHONE`
- **Status:** ⚪ Todo · **Тип:** Spike / внешняя зависимость (не код)
- **Источник:** спека [`telnyx-integration-spec-dogestonia-2026-06-10.md`](../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md) §7, §8
- **Зависит от:** — (вести параллельно; **обязателен до live-теста** [PV-06](STORY-IDS-PV-06-telnyx-sms-sender.md)/[PV-07](STORY-IDS-PV-07-telnyx-delivery-webhook.md))

## Зачем простыми словами
Часть деталей Telnyx нельзя узнать из кода — только из личного кабинета. Этот спайк — завести аккаунт Telnyx и собрать боевые/тестовые credentials + настроить отправителя, чтобы потом не гадать. Long-lead: верификация аккаунта Level-2 может занять время.

## Scope (получить и зафиксировать)
- **Аккаунт:** создать Telnyx-аккаунт; пройти **Level-2 верификацию** (нужна для буквенного отправителя `DOGEstonia`); добавить оплату/баланс или понять ограничения trial.
- **API key:** создать в Mission Control Portal.
- **Messaging Profile:** создать; в whitelist стран назначения добавить **Эстонию (+372)**; задать **default Alphanumeric Sender ID = `DOGEstonia`** (1–11 символов, есть буква); скопировать **Messaging Profile ID**.
- **Webhook:** решить URL для статусов доставки (PV-07) и **подтвердить механизм подписи** входящих webhook (заголовок/ключ).
- **Подтвердить по докам/кабинету (открытые из спеки §8):** идемпотентность `POST /v2/messages` (есть ли); реальный account-specific throughput для EE; нужен ли brand-proof для `DOGEstonia`; точный лейбл whitelist Эстонии; есть ли отдельный sandbox.
- **Тестовый номер:** для trial — верифицировать номер тестировщика (trial шлёт только на него).

## Вне scope
- Код адаптера/webhook — [PV-06](STORY-IDS-PV-06-telnyx-sms-sender.md)/[PV-07](STORY-IDS-PV-07-telnyx-delivery-webhook.md).

## Acceptance Criteria
- [ ] Аккаунт создан, Level-2 пройдена, credentials у команды.
- [ ] Messaging Profile настроен (EE в whitelist, alpha sender `DOGEstonia`), Profile ID записан.
- [ ] Подтверждён механизм подписи webhook доставки.
- [ ] Закрыты (или зафиксированы как риск) открытые вопросы §8 спеки: идемпотентность, throughput, brand-proof, sandbox.
- [ ] Готов `.env` для live-теста (`TELNYX_API_KEY/FROM/MESSAGING_PROFILE_ID`) + тестовый номер.

## Парадигма-якорь
[06-eid-providers](../../../runtime-docs/06-eid-providers.md); спека Telnyx §7–§8; мануал-образец (eID): [`authentigate-sandbox-setup-howto`](../../../tech-requirements/authentigate-sandbox-setup-howto.md).
