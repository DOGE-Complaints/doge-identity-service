# EPIC-IDS-SMSPM — Live SMS через SMSPM (Эстония)

> **ID:** `EPIC-IDS-SMSPM` · **Pipeline:** [`EPIC-IDS-14-smspm`](../../epics/EPIC-IDS-14-smspm/EPIC-IDS-14-smspm.md) · **Статус:** 🟡 In Progress (SMSPM-01 🟢 pkg-000046; SMSPM-02 🟢 pkg-000047; SMSPM-03 ⚪ pkg-000048; SMSPM-04 🟢 pkg-000049) · **Тип:** Функциональный (SMS provider adapter)  
> **Создан:** 2026-08-16 · **Decisions locked:** 2026-08-16  
> **Контекст:** phone-verification платформа уже Done ([`EPIC-IDS-PHONE`](../phone-verification/EPIC-IDS-PHONE.md)); нужен боевой провайдер, который работает с Эстонией. Telnyx остаётся опцией в `.env`, но для EE сейчас не подходит (ops/geo).

## Назначение

Добавить **SMSPM** как переключаемый live-бэкенд доставки SMS для OTP-верификации телефона (`SMS_PROVIDER=smspm`). OTP-движок, сессии, `/auth/phone/*` и HMAC-хранение **не переписываем** — только новый адаптер доставки рядом с `mock` / `file` / `telnyx`.

## База (не дублировать в stories)

- Solution architecture: [`solution-architecture-smspm-sms-provider.md`](solution-architecture-smspm-sms-provider.md)
- Внешний API guide: [`../inbound/SMSPM_SMS_Delivery_Integration_Guide.md`](../inbound/SMSPM_SMS_Delivery_Integration_Guide.md)
- Операторский smoke (сейчас mock/Telnyx): [`../../../runbook/phone-sms-verification.md`](../../../runbook/phone-sms-verification.md)

## Locked decisions (epic-wide)

| ID | Решение | Обоснование |
|----|---------|-------------|
| **D-G1** | SMSPM = только `SmsSenderPort` delivery; OTP/TTL/attempts остаются в [`otp_engine.py`](../../../../src/core/phone/otp_engine.py) | Тот же контракт, что Telnyx; SMSPM Verify ломает наш anti-abuse и HMAC-модель ([`10-phone-personal-data-processing.md`](../../../runtime-docs/10-phone-personal-data-processing.md)) |
| **D-G2** | Пакет `src/core/phone/smspm/` зеркало `telnyx/` | Единый plugin-паттерн ([`descriptor.py`](../../../../src/core/phone/descriptor.py), [`registry_builder.py`](../../../../src/core/phone/registry_builder.py)) |
| **D-G3** | `SMS_PROVIDER=telnyx` остаётся в registry | Ops-выбор; EE сейчас ломается у Telnyx — не удалять код |
| **D-G4** | `toNumber` = E.164 **без** `+` только внутри sender | Ядро/хеш остаются на `+372…` (SA §4.3); не менять [`e164.py`](../../../../src/core/phone/e164.py) |
| **D-G5** | Auth SMSPM: `hash` + `token` в JSON POST body | Guide API v2.1; не Bearer (в отличие от Telnyx) |
| **D-G6** | Webhook: **GET** query + тело ответа `OK`; auth = shared secret в path (нет Ed25519 в guide) | Guide § report; не выдумывать crypto; отличие от Telnyx Ed25519 — осознанное |

Детали и субтаски — в story-файлах ниже.

## Stories

| Story | Тема | Статус |
|-------|------|--------|
| [SMSPM-01](STORY-IDS-SMSPM-01-provider-config-registry.md) | Config + дескриптор: `SMS_PROVIDER=smspm`, fail-fast env | 🟢 Done (pkg-000046) |
| [SMSPM-02](STORY-IDS-SMSPM-02-sms-sender.md) | Отправка OTP-текста через SMSPM + ошибки + offline-тесты | 🟢 Done (pkg-000047) |
| [SMSPM-03](STORY-IDS-SMSPM-03-operator-runbook-smoke.md) | Runbook-режим smspm + live smoke | ⚪ Todo |
| [SMSPM-04](STORY-IDS-SMSPM-04-delivery-report-webhook.md) | Phase-2: статусы доставки (не gate confirm) | 🟢 Done (pkg-000049) |
| [SMSPM-05](STORY-IDS-SMSPM-05-smsid-session-wire.md) | Optional `smsId` = session id (D-02-6) | ⚪ Todo (draft; excluded from 2/4) |

### Ops (вне product progress)

| Spike | Тема | Статус |
|-------|------|--------|
| [SPIKE-SMSPM-01](SPIKE-IDS-SMSPM-01-account-sender-setup.md) | Аккаунт SMSPM, hash/token, approved sender | ⚪ Todo |

## Порядок

**SMSPM-01** → **SMSPM-02** → **SMSPM-03**. **SMSPM-04** после 02. **SPIKE-01** параллельно с начала; гейтит live-часть 02/03.

## Non-goals эпика

- Удаление Telnyx / замена OTP-движка продуктом SMSPM Verify.
- Изменения spa / gateway / privacy landing в этом пакете.
