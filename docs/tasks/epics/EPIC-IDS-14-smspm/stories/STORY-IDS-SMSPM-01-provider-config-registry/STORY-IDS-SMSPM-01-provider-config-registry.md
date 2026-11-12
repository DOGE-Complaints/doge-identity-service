# STORY-IDS-SMSPM-01 — Provider config + registry: `SMS_PROVIDER=smspm`

## Meta
- **Key:** `STORY-IDS-SMSPM-01-provider-config-registry`
- **Parent Epic:** [`../../EPIC-IDS-14-smspm.md`](../../EPIC-IDS-14-smspm.md)
- **Epic alias (код):** `EPIC-IDS-SMSPM`
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md`](../../../../backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md)
- **Decision Ref:** [`../../../../backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md`](../../../../backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md); [`solution-architecture-smspm-sms-provider.md`](../../../../backlog-stories/smspm/solution-architecture-smspm-sms-provider.md) §3, §5; parent epic D-G1…D-G3
- **Зависит от:** phone SMS backbone Done ([`EPIC-IDS-10`](../../../EPIC-IDS-10-phone-verification/EPIC-IDS-10-phone-verification.md) / [`EPIC-IDS-PHONE`](../../../../backlog-stories/phone-verification/EPIC-IDS-PHONE.md))
- **Wave:** `pkg-000046`

## Зачем простыми словами
Нужно, чтобы identity **узнавал** провайдера `smspm` из `.env` так же, как `telnyx` / `mock` / `file`: при выборе — грузить настройки и падать на старте, если обязательные секреты забыли.

## Scope (outcome)
- `SMS_PROVIDER=smspm` — валидное имя в registry.
- Fail-fast: при активном `smspm` обязательные env обязательны; при других провайдерах SMSPM-env не требуются.
- `.env.example` документирует блок SMSPM и комментарий `mock|file|telnyx|smspm`.
- HTTP-отправка **не** в этой story (SMSPM-02).

## Decisions

| ID | Решение | Почему |
|----|---------|--------|
| **D-01-1** | Required: `SMSPM_HASH`, `SMSPM_TOKEN`, `SMSPM_FROM` | Guide auth + sender; без них send бесполезен |
| **D-01-2** | Optional: `SMSPM_API_BASE_URL` default `https://api.smspm.com` | Как Telnyx `TELNYX_API_BASE_URL`; override для staging |
| **D-01-3** | Validate SMSPM settings **только** когда active provider = `smspm` (через `config_spec.load`) | Зеркало Telnyx: не ломать старт с `SMS_PROVIDER=mock` |
| **D-01-4** | `_needs_sms_http_client` автоматически подхватит `smspm` (исключает только `mock`/`file`) | [`runtime_factory.py`](../../../../../../src/core/phone/runtime_factory.py) — не хардкодить allow-list HTTP-провайдеров |
| **D-01-5** | Telnyx / mock / file остаются в `ALL_SMS_PROVIDER_DESCRIPTORS` (D-G3) | Ops-выбор; EE-проблема ≠ удаление кода |

## Паттерн (зеркало)

| Что | Якорь |
|-----|-------|
| Settings + validate | [`telnyx/config.py`](../../../../../../src/core/phone/telnyx/config.py) `TelnyxSettings` |
| Descriptor | [`telnyx/descriptor.py`](../../../../../../src/core/phone/telnyx/descriptor.py) `TELNYX_SMS_DESCRIPTOR` |
| Registry tuple | [`registry_builder.py`](../../../../../../src/core/phone/registry_builder.py) `ALL_SMS_PROVIDER_DESCRIPTORS` |
| Switch | [`schema.py`](../../../../../../src/core/config/schema.py) `SMS_PROVIDER` ∈ registered names |
| HTTP client gate | [`runtime_factory.py`](../../../../../../src/core/phone/runtime_factory.py) `_needs_sms_http_client` |
| Env docs | [`.env.example`](../../../../../../.env.example) блок Telnyx (~L60–78) |

## Подзадачи

- **T01 — `SmspmSettings`.** Пакет `src/core/phone/smspm/`: `config.py` с load/validate (`SMSPM_HASH`, `SMSPM_TOKEN`, `SMSPM_FROM`, optional base URL) + `config_spec` / `SMSPM_SMS_CONFIG_SPEC`.
- **T02 — Descriptor + registry.** `SMSPM_SMS_DESCRIPTOR` (`name="smspm"`); stub или no-op `build` допустим до SMSPM-02, либо wire после 02 в той же PR-серии; **обязательно** append в `ALL_SMS_PROVIDER_DESCRIPTORS`.
- **T03 — Config tests.** Accept `smspm` + full env; fail missing required when active=`smspm`; `mock|file|telnyx` без SMSPM env — ok.
- **T04 — `.env.example`.** Комментарий `mock | file | telnyx | smspm`; блок `SMSPM_*` (пустые значения, без секретов).

## Точки в коде (куда внедрять)

| Файл | Действие |
|------|----------|
| `src/core/phone/smspm/config.py` | **new** — settings |
| `src/core/phone/smspm/descriptor.py` | **new** — descriptor |
| `src/core/phone/smspm/__init__.py` | **new** — exports |
| `src/core/phone/registry_builder.py` | import + append descriptor |
| `.env.example` | comment + SMSPM block |
| `tests/…` (зеркало telnyx config tests) | T03 |

## Вне scope
- HTTP-отправка SMS — [SMSPM-02](../../../../backlog-stories/smspm/STORY-IDS-SMSPM-02-sms-sender.md).
- Runbook / live smoke — [SMSPM-03](../../../../backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md).
- Webhook доставки — [SMSPM-04](../../../../backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md).

## Acceptance Criteria
- [x] `SMS_PROVIDER=smspm` принимается конфигом; неизвестное имя по-прежнему отклоняется.
- [x] При `smspm` без `SMSPM_HASH` / `SMSPM_TOKEN` / `SMSPM_FROM` сервис не стартует с ясной config-ошибкой.
- [x] При `SMS_PROVIDER=mock|file|telnyx` поведение не регрессирует (SMSPM env не обязательны).
- [x] `.env.example` содержит блок SMSPM и обновлённый комментарий провайдеров.
- [x] T01–T04 закрыты; descriptor в `ALL_SMS_PROVIDER_DESCRIPTORS`.

## Парадигма-якорь
[EPIC-IDS-14 / EPIC-IDS-SMSPM](../../EPIC-IDS-14-smspm.md) D-G*; [solution-architecture-smspm-sms-provider.md](../../../../backlog-stories/smspm/solution-architecture-smspm-sms-provider.md); образец PV-06 Telnyx config/registry.

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-14-01-t01-smspm-settings-config`](./task-ids-14-01-t01-smspm-settings-config/README.md) | pkg-000046 |
| 2 | [`task-ids-14-01-t02-smspm-descriptor-registry`](./task-ids-14-01-t02-smspm-descriptor-registry/README.md) | pkg-000046 |
| 3 | [`task-ids-14-01-t03-smspm-config-tests`](./task-ids-14-01-t03-smspm-config-tests/README.md) | pkg-000046 |
| 4 | [`task-ids-14-01-t04-env-example-smspm-block`](./task-ids-14-01-t04-env-example-smspm-block/README.md) | pkg-000046 |
| 5 | [`task-ids-14-01-t05-story-acceptance-verification`](./task-ids-14-01-t05-story-acceptance-verification/README.md) | pkg-000046 |
| 6 | [`task-ids-14-01-t06-audit-f1-smspm-test-count-docs`](./task-ids-14-01-t06-audit-f1-smspm-test-count-docs/README.md) | override `epic_ids_14_smspm_01_audit_2026_08_20` (F1 🟢) |
