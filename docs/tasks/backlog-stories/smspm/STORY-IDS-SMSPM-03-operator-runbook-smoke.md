# STORY-IDS-SMSPM-03 — Operator runbook + live smoke (smspm)

## Meta
- **Key:** `STORY-IDS-SMSPM-03-operator-runbook-smoke`
- **Epic:** [`EPIC-IDS-SMSPM`](EPIC-IDS-SMSPM.md) (D-G3)
- **Status:** ⚪ Todo
- **Источник:** [`solution-architecture-smspm-sms-provider.md`](solution-architecture-smspm-sms-provider.md) §8; [`../../../runbook/phone-sms-verification.md`](../../../runbook/phone-sms-verification.md)
- **Зависит от:** [SMSPM-02](STORY-IDS-SMSPM-02-sms-sender.md), [SPIKE-01](SPIKE-IDS-SMSPM-01-account-sender-setup.md)

## Зачем простыми словами
Оператору нужен понятный рецепт: как включить SMSPM в `.env` и как за 5 минут проверить, что на эстонский номер реально приходит код и confirm ставит `phone_verified`.

## Scope (outcome)
- Один SSOT smoke: расширить существующий [`phone-sms-verification.md`](../../../runbook/phone-sms-verification.md) **режимом C** (`smspm`), не новый файл.
- Telnyx остаётся §B / опция (D-G3).
- Live evidence → краткий summary в `docs/tasks/run-reports/`.

## Decisions

| ID | Решение | Почему |
|----|---------|--------|
| **D-03-1** | Расширять существующий runbook режимом C — **не** новый файл | Один SSOT; оператор не ищет второй документ |
| **D-03-2** | Telnyx §B остаётся | D-G3; EE-проблема ≠ удаление режима |
| **D-03-3** | Live evidence → `docs/tasks/run-reports/` (краткий summary: дата, env names без секретов, pass/fail) | Аудит пилота без PII/секретов в git |
| **D-03-4** | Smoke критерий = request → SMS на EE → confirm → `phone_verified` / provider отражает `smspm` | Тот же продуктовый исход, что Telnyx live |

## Паттерн

| Что | Якорь |
|-----|-------|
| Runbook SSOT | [`phone-sms-verification.md`](../../../runbook/phone-sms-verification.md) (mock / Telnyx §) |
| Env names | SA §5 / `.env.example` после SMSPM-01 |
| SPIKE creds | [SPIKE-01](SPIKE-IDS-SMSPM-01-account-sender-setup.md) |

## Подзадачи

- **T01 — Env table.** В runbook: таблица `SMS_PROVIDER=smspm` + `SMSPM_HASH` / `SMSPM_TOKEN` / `SMSPM_FROM` / optional base URL (без значений секретов).
- **T02 — Curl smoke.** Шаги request → confirm → `/me` (зеркало Telnyx-секции).
- **T03 — Troubleshooting.** Строки: missing creds, country/prefix, rate limit / SEND_FAILED — кратко, без дублирования всего SMSPM guide.
- **T04 — Execute + run-summary.** После SPIKE: live EE smoke; файл в `docs/tasks/run-reports/` (D-03-3).

## Точки в доках

| Файл | Действие |
|------|----------|
| `docs/runbook/phone-sms-verification.md` | режим C + env + curl + troubleshooting |
| `docs/tasks/run-reports/*` | краткий live summary после T04 |

## Вне scope
- Реализация sender — [SMSPM-02](STORY-IDS-SMSPM-02-sms-sender.md).
- Webhook доставки — [SMSPM-04](STORY-IDS-SMSPM-04-delivery-report-webhook.md).
- Настройка аккаунта — [SPIKE-01](SPIKE-IDS-SMSPM-01-account-sender-setup.md).
- Правки `src/` в этой story (только docs/runbook + evidence).

## Acceptance Criteria
- [x] В [`phone-sms-verification.md`](../../../runbook/phone-sms-verification.md) есть режим C `SMS_PROVIDER=smspm` с env-чеклистом (T01).
- [x] Описан live-smoke curl-путь (T02); Telnyx и mock по-прежнему описаны (D-03-2).
- [x] Troubleshooting rows добавлены (T03).
- [ ] Live-smoke на тестовом EE-номере выполнен; summary в `docs/tasks/run-reports/` без секретов/PII (T04, D-03-3).

## Парадигма-якорь
[`phone-sms-verification.md`](../../../runbook/phone-sms-verification.md); [EPIC-IDS-SMSPM](EPIC-IDS-SMSPM.md); [solution-architecture-smspm-sms-provider.md](solution-architecture-smspm-sms-provider.md).
