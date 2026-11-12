# EPIC-IDS-14 — Live SMS через SMSPM (Эстония)

> **ID:** `EPIC-IDS-14` · **Alias (код/backlog):** `EPIC-IDS-SMSPM` · **Статус:** 🟡 In Progress (SMSPM-01 🟢 pkg-000046; SMSPM-02 🟢 pkg-000047; SMSPM-03 ⚪ pkg-000048; SMSPM-04 🟢 pkg-000049) · **Тип:** Функциональный (SMS provider adapter)  
> **Source (backlog):** [`backlog-stories/smspm/EPIC-IDS-SMSPM.md`](../../backlog-stories/smspm/EPIC-IDS-SMSPM.md)  
> **Создан (backlog):** 2026-08-16 · **P1 materialize:** 2026-08-20 · **Decisions locked:** 2026-08-16  
> **Контекст:** phone-verification платформа уже Done ([`EPIC-IDS-10`](../EPIC-IDS-10-phone-verification/EPIC-IDS-10-phone-verification.md) / [`EPIC-IDS-PHONE`](../../backlog-stories/phone-verification/EPIC-IDS-PHONE.md)); нужен боевой провайдер, который работает с Эстонией. Telnyx остаётся опцией в `.env`, но для EE сейчас не подходит (ops/geo).

## Назначение

Добавить **SMSPM** как переключаемый live-бэкенд доставки SMS для OTP-верификации телефона (`SMS_PROVIDER=smspm`). OTP-движок, сессии, `/auth/phone/*` и HMAC-хранение **не переписываем** — только новый адаптер доставки рядом с `mock` / `file` / `telnyx`.

## База (не дублировать в stories)

- Solution architecture: [`solution-architecture-smspm-sms-provider.md`](../../backlog-stories/smspm/solution-architecture-smspm-sms-provider.md)
- Внешний API guide: [`SMSPM_SMS_Delivery_Integration_Guide.md`](../../backlog-stories/inbound/SMSPM_SMS_Delivery_Integration_Guide.md)
- Операторский smoke (сейчас mock/Telnyx): [`phone-sms-verification.md`](../../../runbook/phone-sms-verification.md)

## Locked decisions (epic-wide)

| ID | Решение | Обоснование |
|----|---------|-------------|
| **D-G1** | SMSPM = только `SmsSenderPort` delivery; OTP/TTL/attempts остаются в [`otp_engine.py`](../../../../src/core/phone/otp_engine.py) | Тот же контракт, что Telnyx; SMSPM Verify ломает наш anti-abuse и HMAC-модель ([`10-phone-personal-data-processing.md`](../../../runtime-docs/10-phone-personal-data-processing.md)) |
| **D-G2** | Пакет `src/core/phone/smspm/` зеркало `telnyx/` | Единый plugin-паттерн ([`descriptor.py`](../../../../src/core/phone/descriptor.py), [`registry_builder.py`](../../../../src/core/phone/registry_builder.py)) |
| **D-G3** | `SMS_PROVIDER=telnyx` остаётся в registry | Ops-выбор; EE сейчас ломается у Telnyx — не удалять код |
| **D-G4** | `toNumber` = E.164 **без** `+` только внутри sender | Ядро/хеш остаются на `+372…` (SA §4.3); не менять [`e164.py`](../../../../src/core/phone/e164.py) |
| **D-G5** | Auth SMSPM: `hash` + `token` в JSON POST body | Guide API v2.1; не Bearer (в отличие от Telnyx) |
| **D-G6** | Webhook: **GET** query + тело ответа `OK`; auth = shared secret в path (нет Ed25519 в guide) | Guide § report; не выдумывать crypto; отличие от Telnyx Ed25519 — осознанное |

Детали и субтаски — в story-файлах ниже. Эта волна (pkg-000049) materialize **только SMSPM-04**.

## Stories

| Story | Тема | Статус |
|-------|------|--------|
| [SMSPM-01](stories/STORY-IDS-SMSPM-01-provider-config-registry/STORY-IDS-SMSPM-01-provider-config-registry.md) | Config + дескриптор: `SMS_PROVIDER=smspm`, fail-fast env | 🟢 Done (pkg-000046) |
| [SMSPM-02](stories/STORY-IDS-SMSPM-02-sms-sender/STORY-IDS-SMSPM-02-sms-sender.md) | Отправка OTP-текста через SMSPM + ошибки + offline-тесты | 🟢 Done (pkg-000047) |
| [SMSPM-03](stories/STORY-IDS-SMSPM-03-operator-runbook-smoke/STORY-IDS-SMSPM-03-operator-runbook-smoke.md) | Runbook-режим smspm + live smoke | ⚪ Todo (pkg-000048) |
| [SMSPM-04](stories/STORY-IDS-SMSPM-04-delivery-report-webhook/STORY-IDS-SMSPM-04-delivery-report-webhook.md) | Phase-2: статусы доставки (не gate confirm) | 🟢 Done (pkg-000049) |

### Ops (вне product progress)

| Spike | Тема | Статус |
|-------|------|--------|
| [SPIKE-SMSPM-01](../../backlog-stories/smspm/SPIKE-IDS-SMSPM-01-account-sender-setup.md) | Аккаунт SMSPM, hash/token, approved sender | ⚪ Todo |

## Порядок

**SMSPM-01** → **SMSPM-02** → **SMSPM-03**. **SMSPM-04** после 02. **SPIKE-01** параллельно с начала; гейтит live-часть 02/03.

## Non-goals эпика

- Удаление Telnyx / замена OTP-движка продуктом SMSPM Verify.
- Изменения spa / gateway / privacy landing в этом пакете.

### Story 1: STORY-IDS-SMSPM-01 — Provider config + registry: `SMS_PROVIDER=smspm` — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-SMSPM-01-provider-config-registry/STORY-IDS-SMSPM-01-provider-config-registry.md`](./stories/STORY-IDS-SMSPM-01-provider-config-registry/STORY-IDS-SMSPM-01-provider-config-registry.md)
- **Source (backlog):** [`backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md`](../../backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md)
- **Wave:** `pkg-000046` (P3 Done 2026-08-20)

**Acceptance Criteria:**
- [x] `SMS_PROVIDER=smspm` принимается конфигом; неизвестное имя по-прежнему отклоняется.
- [x] При `smspm` без `SMSPM_HASH` / `SMSPM_TOKEN` / `SMSPM_FROM` сервис не стартует с ясной config-ошибкой.
- [x] При `SMS_PROVIDER=mock|file|telnyx` поведение не регрессирует (SMSPM env не обязательны).
- [x] `.env.example` содержит блок SMSPM и обновлённый комментарий провайдеров.
- [x] T01–T04 закрыты; descriptor в `ALL_SMS_PROVIDER_DESCRIPTORS`.

### Story 2: STORY-IDS-SMSPM-02 — SMSPM SMS sender (доставка OTP) — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-SMSPM-02-sms-sender/STORY-IDS-SMSPM-02-sms-sender.md`](./stories/STORY-IDS-SMSPM-02-sms-sender/STORY-IDS-SMSPM-02-sms-sender.md)
- **Source (backlog):** [`backlog-stories/smspm/STORY-IDS-SMSPM-02-sms-sender.md`](../../backlog-stories/smspm/STORY-IDS-SMSPM-02-sms-sender.md)
- **Wave:** `pkg-000047` (P3 Done 2026-08-20)

**Acceptance Criteria:**
- [x] При `SMS_PROVIDER=smspm` и валидных creds `POST /auth/phone/request` доставляет SMS через SMSPM; ответ клиенту без кода.
- [x] При успехе (D-02-1) provider message id сохраняется в phone-сессии.
- [x] Ошибки мапятся по D-02-2; секреты/OTP/full MSISDN не в логах (D-02-7).
- [x] Offline-тесты (T04) зелёные; live (T05) skip без creds и проходит после SPIKE.
- [x] `SMS_PROVIDER=mock|file|telnyx` без регрессий; MVP без `report` (D-02-5).

### Story 3: STORY-IDS-SMSPM-03 — Operator runbook + live smoke (smspm) — ⚪ Todo

- **Pipeline story:** [`stories/STORY-IDS-SMSPM-03-operator-runbook-smoke/STORY-IDS-SMSPM-03-operator-runbook-smoke.md`](./stories/STORY-IDS-SMSPM-03-operator-runbook-smoke/STORY-IDS-SMSPM-03-operator-runbook-smoke.md)
- **Source (backlog):** [`backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md`](../../backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md)
- **Wave:** `pkg-000048` (P1 materialize 2026-08-20)

**Acceptance Criteria:**
- [x] В [`phone-sms-verification.md`](../../../runbook/phone-sms-verification.md) есть режим C `SMS_PROVIDER=smspm` с env-чеклистом (T01).
- [x] Описан live-smoke curl-путь (T02); Telnyx и mock по-прежнему описаны (D-03-2).
- [x] Troubleshooting rows добавлены (T03).
- [ ] Live-smoke на тестовом EE-номере выполнен; summary в `docs/tasks/run-reports/` без секретов/PII (T04, D-03-3).

### Story 4: STORY-IDS-SMSPM-04 — Delivery report / webhook (phase-2) — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-SMSPM-04-delivery-report-webhook/STORY-IDS-SMSPM-04-delivery-report-webhook.md`](./stories/STORY-IDS-SMSPM-04-delivery-report-webhook/STORY-IDS-SMSPM-04-delivery-report-webhook.md)
- **Source (backlog):** [`backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md`](../../backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md)
- **Wave:** `pkg-000049` (P3 Done 2026-08-20)

**Acceptance Criteria:**
- [x] Статусы доставки обновляются по provider message id без изменения OTP-confirm флоу (D-04-5).
- [x] Endpoint отвечает `OK` при валидном secret; 401 при mismatch (D-04-1).
- [x] Повторные/устаревшие события идемпотентны forward-only (D-04-3).
- [x] Аудит без сырого номера/OTP (D-04-6).
- [x] При set `SMSPM_REPORT_URL` sender передаёт `report` (D-04-4).
- [x] Offline-тесты T06 зелёные; env задокументированы (T07).
