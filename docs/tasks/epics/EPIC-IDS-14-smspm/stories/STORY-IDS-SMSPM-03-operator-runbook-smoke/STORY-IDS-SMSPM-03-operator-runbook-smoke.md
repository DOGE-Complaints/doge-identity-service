# STORY-IDS-SMSPM-03 — Operator runbook + live smoke (smspm)

## Meta
- **Key:** `STORY-IDS-SMSPM-03-operator-runbook-smoke`
- **Parent Epic:** [`../../EPIC-IDS-14-smspm.md`](../../EPIC-IDS-14-smspm.md)
- **Epic alias (код):** `EPIC-IDS-SMSPM` (D-G3)
- **Status:** ⚪ Todo
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md`](../../../../backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md)
- **Decision Ref:** [`../../../../backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md`](../../../../backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md); [`solution-architecture-smspm-sms-provider.md`](../../../../backlog-stories/smspm/solution-architecture-smspm-sms-provider.md) §8; [`phone-sms-verification.md`](../../../../../runbook/phone-sms-verification.md); parent epic D-G3
- **Зависит от:** [SMSPM-02](../STORY-IDS-SMSPM-02-sms-sender/STORY-IDS-SMSPM-02-sms-sender.md) 🟢 pkg-000047; [SPIKE-01](../../../../backlog-stories/smspm/SPIKE-IDS-SMSPM-01-account-sender-setup.md) (ops, out of queue)
- **Wave:** `pkg-000048`

## Зачем простыми словами
Оператору нужен понятный рецепт: как включить SMSPM в `.env` и как за 5 минут проверить, что на эстонский номер реально приходит код и confirm ставит `phone_verified`.

## Scope (outcome)
- Один SSOT smoke: расширить существующий [`phone-sms-verification.md`](../../../../../runbook/phone-sms-verification.md) **режимом C** (`smspm`), не новый файл.
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
| Runbook SSOT | [`phone-sms-verification.md`](../../../../../runbook/phone-sms-verification.md) (mock / Telnyx §) |
| Env names | SA §5 / `.env.example` после SMSPM-01 |
| SPIKE creds | [SPIKE-01](../../../../backlog-stories/smspm/SPIKE-IDS-SMSPM-01-account-sender-setup.md) |

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
- Реализация sender — [SMSPM-02](../STORY-IDS-SMSPM-02-sms-sender/STORY-IDS-SMSPM-02-sms-sender.md).
- Webhook доставки — [SMSPM-04](../../../../backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md).
- Настройка аккаунта — [SPIKE-01](../../../../backlog-stories/smspm/SPIKE-IDS-SMSPM-01-account-sender-setup.md).
- Правки `src/` в этой story (только docs/runbook + evidence).

## Acceptance Criteria
- [x] В [`phone-sms-verification.md`](../../../../../runbook/phone-sms-verification.md) есть режим C `SMS_PROVIDER=smspm` с env-чеклистом (T01).
- [x] Описан live-smoke curl-путь (T02); Telnyx и mock по-прежнему описаны (D-03-2).
- [x] Troubleshooting rows добавлены (T03).
- [ ] Live-smoke на тестовом EE-номере выполнен; summary в `docs/tasks/run-reports/` без секретов/PII (T04, D-03-3).

## Парадигма-якорь
[`phone-sms-verification.md`](../../../../../runbook/phone-sms-verification.md); [EPIC-IDS-14 / EPIC-IDS-SMSPM](../../EPIC-IDS-14-smspm.md); [solution-architecture-smspm-sms-provider.md](../../../../backlog-stories/smspm/solution-architecture-smspm-sms-provider.md).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-14-03-t01-runbook-mode-c-env-table`](./task-ids-14-03-t01-runbook-mode-c-env-table/README.md) | pkg-000048 |
| 2 | [`task-ids-14-03-t02-runbook-curl-smoke`](./task-ids-14-03-t02-runbook-curl-smoke/README.md) | pkg-000048 |
| 3 | [`task-ids-14-03-t03-runbook-troubleshooting`](./task-ids-14-03-t03-runbook-troubleshooting/README.md) | pkg-000048 |
| 4 | [`task-ids-14-03-t04-live-ee-smoke-run-summary`](./task-ids-14-03-t04-live-ee-smoke-run-summary/README.md) | pkg-000048 |
| 5 | [`task-ids-14-03-t05-story-acceptance-verification`](./task-ids-14-03-t05-story-acceptance-verification/README.md) | pkg-000048 |
