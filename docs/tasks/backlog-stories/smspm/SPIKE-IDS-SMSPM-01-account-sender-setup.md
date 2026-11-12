# SPIKE-IDS-SMSPM-01 — SMSPM account & sender setup (внешнее)

## Meta
- **Key:** `SPIKE-IDS-SMSPM-01-account-sender-setup`
- **Epic:** [`EPIC-IDS-SMSPM`](EPIC-IDS-SMSPM.md)
- **Status:** ⚪ Todo · **Тип:** Spike / внешняя зависимость (не код)
- **Источник:** [`solution-architecture-smspm-sms-provider.md`](solution-architecture-smspm-sms-provider.md); [`../inbound/SMSPM_SMS_Delivery_Integration_Guide.md`](../inbound/SMSPM_SMS_Delivery_Integration_Guide.md); epic D-G*
- **Зависит от:** — (вести параллельно; **обязателен до live** [SMSPM-02](STORY-IDS-SMSPM-02-sms-sender.md) / [SMSPM-03](STORY-IDS-SMSPM-03-operator-runbook-smoke.md))

## Зачем простыми словами
Без кабинета SMSPM нельзя получить рабочие credentials и одобренный sender. Этот спайк — завести аккаунт и зафиксировать значения для `.env`, чтобы live-smoke не упирался в «нет доступа».

## Decisions

| ID | Решение | Почему |
|----|---------|--------|
| **D-S1** | Секреты (`hash`/`token`) только Railway variables / 1Password — **не** в git и не в story-файлах | Миссия security: тот же инвариант, что Telnyx keys ([`04-security`](../../../runtime-docs/04-security.md)) |
| **D-S2** | Целевой sender — брендовый `DOGEstonia` (если SMSPM approve); иначе временный dashboard default **только для smoke** с пометкой risk | Бренд и trust; smoke не блокируем навсегда на brand-proof |
| **D-S3** | Webhook URL / shared secret для [SMSPM-04](STORY-IDS-SMSPM-04-delivery-report-webhook.md) можно отложить до phase-2 | MVP OTP не зависит от delivery (D-G1); SPIKE не блокирует SMSPM-01/02 offline |

## Scope
- Создать / подтвердить аккаунт SMSPM и доступ в dashboard (`https://app.smspm.com`).
- Получить **hash** и **token**; положить в секрет-хранилище команды.
- Запросить / подтвердить **sender ID** (D-S2).
- Проверить, что Эстония / целевые операторы доступны для отправки с этого аккаунта.
- Зафиксировать тестовый номер (E.164 `+372…`) для live-smoke.
- Краткая operator-note: имена env из SA (`SMSPM_HASH`, `SMSPM_TOKEN`, `SMSPM_FROM`, …) — **без значений секретов**.

## Подзадачи

- **T01 — Account.** Аккаунт создан / доступен; dashboard открывается.
- **T02 — Credentials.** `hash` + `token` получены; сохранены вне git (D-S1).
- **T03 — Sender.** Sender запрошен/approved или выбран временный default + risk-note (D-S2).
- **T04 — EE reachability.** Подтверждено (доками кабинета или пробной отправкой из UI SMSPM), что EE reachable.
- **T05 — Test MSISDN.** Согласован тестовый `+372…` для smoke.
- **T06 — Env cheat-sheet.** Короткая заметка (run-report или private ops doc): какие ключи `.env` заполнять — без секретов.

## Вне scope
- Код адаптера / runbook — [SMSPM-01](STORY-IDS-SMSPM-01-provider-config-registry.md)…[SMSPM-03](STORY-IDS-SMSPM-03-operator-runbook-smoke.md).
- Реализация webhook — [SMSPM-04](STORY-IDS-SMSPM-04-delivery-report-webhook.md).

## Acceptance Criteria
- [ ] T01–T05 выполнены; у команды есть рабочие credentials вне git.
- [ ] Sender ID согласован (prod brand или smoke default + risk).
- [ ] Есть согласованный тестовый номер для live-smoke.
- [ ] T06: cheat-sheet с именами env (без секретов) доступен оператору.

## Парадигма-якорь
[EPIC-IDS-SMSPM](EPIC-IDS-SMSPM.md) D-G*; SA §4–5; inbound guide § Authentication / Sender ID; аналог [SPIKE-IDS-PV-08](../phone-verification/SPIKE-IDS-PV-08-telnyx-account-setup.md).
