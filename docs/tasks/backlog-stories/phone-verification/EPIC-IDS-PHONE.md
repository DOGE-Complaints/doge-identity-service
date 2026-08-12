# EPIC-IDS-PHONE — Верификация телефона (разовая, замена eID на MVP)

> **ID:** `EPIC-IDS-PHONE` (pipeline `EPIC-IDS-10`) · **Статус:** 🟢 Done (PV-01…07, PV-09, PV-10 — pkg-000018…041; SPIKE-08 — внешнее) · **Тип:** Функциональный
> **Синхронизировано с** [`bullrun-launch-index`](../../bullrun-launch-index.md) 2026-06-26.

## Назначение
Разовая **верификация телефона** как дешёвая замена eID на MVP (eID [отложен](../eid-deferred/README.md) — доп. расходы SK). Цель та же — подтвердить, что за аккаунтом реальный уникальный человек: пользователь один раз вводит номер → получает OTP по SMS → вводит код → ставим флаг `phone_verified`. **Отдельный функционал** (eID вернём), но построен по тем же plugin-паттернам, что и провайдер-платформа eID (🟢 Done).

SMS-провайдеры **сменные**, активный выбирается в `.env` (`SMS_PROVIDER`), разрешённые дозвонные префиксы — в `.env` (`PHONE_ALLOWED_DIAL_PREFIXES`). **Первый боевой провайдер — Telnyx** (Messaging API).

## Контекст и решения (база)
- Архитектура: [`phone-verification-architecture-2026-06-10.md`](../../../analysis/phone-verification-architecture-2026-06-10.md) (§10 — продуктовые решения + уточнения Telnyx).
- Бриф для интегратора: [`telnyx-integration-architecture-brief-2026-06-10.md`](../../../analysis/telnyx-integration-architecture-brief-2026-06-10.md).
- Спека Telnyx (от агента): [`telnyx-integration-spec-dogestonia-2026-06-10.md`](../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md).
- Образец-платформа (код, Done): [`EPIC-IDS-EID`](../eid/EPIC-IDS-EID.md).

**Продуктовые решения (интервью 2026-06-11):** P1 один номер = один аккаунт (конфликт 409); P2 отслеживание доставки (webhook) — **в MVP**; P3 правила кода «Стандарт» (6 цифр, TTL 5 мин, 5 попыток, повтор 60 сек); P4 буквенный отправитель `DOGEstonia`.

## Stories
| Story | Тема | Слой | Статус |
|-------|------|------|--------|
| [STORY-IDS-PV-01](STORY-IDS-PV-01-phone-provider-backbone.md) | Plugin-платформа SMS-провайдеров + канон контракта | платформа | 🟢 Done |
| [STORY-IDS-PV-02](STORY-IDS-PV-02-provider-owned-config.md) | Provider-owned config + выбор активного + allowlist префиксов | платформа | 🟢 Done |
| [STORY-IDS-PV-03](STORY-IDS-PV-03-otp-engine-session.md) | OTP-движок + сессия верификации | ядро | 🟢 Done |
| [STORY-IDS-PV-04](STORY-IDS-PV-04-profile-flag-migration.md) | Флаг профиля + модель + миграция + дедуп (P1) | данные | 🟢 Done |
| [STORY-IDS-PV-05](STORY-IDS-PV-05-verification-flow-api.md) | Flow API: request/confirm + rate-limit + аудит | оркестрация | 🟢 Done |
| [STORY-IDS-PV-06](STORY-IDS-PV-06-telnyx-sms-sender.md) | Telnyx SMS sender (адаптер + регистрация + тесты) | провайдер | 🟢 Done |
| [STORY-IDS-PV-07](STORY-IDS-PV-07-telnyx-delivery-webhook.md) | Telnyx delivery webhook ingestion (P2, MVP) | провайдер | 🟢 Done |
| [SPIKE-IDS-PV-08](SPIKE-IDS-PV-08-telnyx-account-setup.md) | Telnyx account & sender setup (внешнее) | внешнее | ⚪ Todo |
| [STORY-IDS-PV-09](STORY-IDS-PV-09-durable-phone-persistence.md) | durable Supabase phone-persistence (sessions+audit+bootstrap parity) | данные / durability | 🟢 Done |
| [STORY-IDS-PV-10](STORY-IDS-PV-10-file-sms-sink-dev.md) | File SMS sink: ловим OTP в файлы (dev-провайдер для ручного теста) | провайдер / dev-DX | 🟢 Done |

## Порядок реализации
**PV-01** (фундамент) → параллельно **PV-02 / PV-03 / PV-04** → **PV-05** (нужны 02/03/04) → **PV-06** (Telnyx, нужны 01/02 + 05 для e2e) → **PV-07** (webhook, после 06). **SPIKE-08** — параллельно с начала (long-lead: аккаунт Telnyx + Level-2 верификация), гейтит только live-тест PV-06/07.

```
PV-01 ──┬─ PV-02 ─┐
        ├─ PV-03 ─┼─ PV-05 ── PV-06 ── PV-07 (webhook)
        └─ PV-04 ─┘
SPIKE-08 (параллельно) ─────────┘ (gate live-test)
```

## Связь
Зеркалит [`EPIC-IDS-EID`](../eid/EPIC-IDS-EID.md) (плагин-платформа провайдеров). Парадигма: [`runtime-docs/06-eid-providers.md`](../../../runtime-docs/06-eid-providers.md).
