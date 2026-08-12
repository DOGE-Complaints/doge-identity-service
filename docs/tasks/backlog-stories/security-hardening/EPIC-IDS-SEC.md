# EPIC-IDS-SEC — Security hardening (cross-cutting gaps аудита 2026-06-24)

> **ID:** `EPIC-IDS-SEC` (pipeline `EPIC-IDS-12`) · **Статус:** 🟡 In Progress (SEC-01/01b/02/03/04/06 🟢 — pkg-000035…043; **открыто:** SEC-05 Accumulating — ADR variant B, реализация в auth-bff POST-MVP) · **Тип:** Сквозной (security/NFR)
> **Источник:** [`identity-backend-full-audit-2026-06-24.md`](../../../analysis/identity-backend-full-audit-2026-06-24.md) §3 (реальные code-гэпы)
> **Не декомпозирован** в pipeline — набор backlog-стори (requirements-only, без implementation proposals).

## Назначение
Закрыть **сквозные security-гэпы**, найденные жёстким аудитом backend identity (2026-06-24, §3). Это не про новый функционал, а про защитные NFR, которые спеки требуют, но код **не реализует**: отсутствие rate-limiting, аудит без хэшированных IP/UA, и недо-валидация Supabase-JWT. Гэпы кросс-режимные — затрагивают и eID (отложен), и активный phone-гейт. Решение оператора по аудиту (Q2): «только отчёт + severity, сборку решаем позже» — этот эпик переводит §3 в проверяемые backlog-стори **уровня требований**.

Каждая стори: только **что должно быть истинно** (требования + критерии приёмки), без выбора middleware/библиотек/схемы — это решается на этапе реализации.

## Контекст и решения (база)
- Аудит-источник: [`identity-backend-full-audit-2026-06-24.md`](../../../analysis/identity-backend-full-audit-2026-06-24.md) §3 (таблица G-1…G-5), §0 (решения оператора).
- Спеки-требования: [`16-security-privacy-observability.md`](../../../requirements/16-security-privacy-observability.md), [`11-eid-verification-flow.md`](../../../requirements/11-eid-verification-flow.md), [`09-supabase-jwt-validation.md`](../../../requirements/09-supabase-jwt-validation.md).
- Парадигма-якорь: [`runtime-docs/04-security.md`](../../../runtime-docs/04-security.md).
- Связанный пакет: [`EPIC-IDS-PHONE`](../phone-verification/EPIC-IDS-PHONE.md) (durable phone-аудит PV-09 пересекается с SEC-02).

**Объём по severity (из §3):** G-1 (HIGH, rate-limit), G-2b (HIGH, IP/UA-хэш аудита — durable-часть G-2 живёт в phone-пакете), G-5 (LOW, JWT-hardening). G-3/G-4 — вне этого эпика (durable phone-сессии и eID session-enc, deferred-домены).

## Состав
| Story | Тема | Слой | Зависит | Статус |
|-------|------|------|---------|--------|
| [STORY-IDS-SEC-01](STORY-IDS-SEC-01-rate-limiting.md) | Per-user rate limiting + 429/`retry_after` для чувствительных роутов (G-1) | оркестрация / cross-cutting | — | 🟢 Done (pkg-000035; phone/request → [SEC-01b](STORY-IDS-SEC-01b-phone-request-http-rate-limit.md)) |
| [STORY-IDS-SEC-01b](STORY-IDS-SEC-01b-phone-request-http-rate-limit.md) | HTTP rate-limit `POST /auth/phone/request` (остаток G-1) | оркестрация / phone | SEC-01 | 🟢 Done (pkg-000036) |
| [STORY-IDS-SEC-02](STORY-IDS-SEC-02-audit-ip-ua-hashing.md) | Хэшированные IP/UA в аудит-событиях (eID + phone) (G-2b) | аудит / cross-cutting | SEC-01 (источник request-контекста) | 🟢 Done (pkg-000037) |
| [STORY-IDS-SEC-03](STORY-IDS-SEC-03-jwt-validation-hardening.md) | Валидация `aud` + сверка формы импорта ключа Supabase-JWT (G-5) | auth | — | 🟢 Done |
| [STORY-IDS-SEC-04](STORY-IDS-SEC-04-service-role-isolation.md) | Изоляция Supabase `service_role` — identity единственный держатель + rotation runbook | cross-service boundary | — | 🟢 Done (парно spa [SEC-01](../../../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-01-remove-service-role-from-frontend.md); pkg-000043) |
| [STORY-IDS-SEC-05](STORY-IDS-SEC-05-auth-credential-model-adr.md) | ADR: модель auth-кредов (Supabase-anon-resource-server vs identity-BFF) | auth / arch | — | ⚪ Todo (парно spa [SEC-02](../../../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-02-supabase-credential-boundary.md)) |
| [STORY-IDS-SEC-06](STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md) | Довести ES256/JWKS Supabase-JWT валидацию: чистка debug, DI, тесты, доки (W1–W6) | auth | SEC-03 | 🟢 Done (pkg-000042, 2026-07-04) |

## Порядок реализации
**SEC-03** (LOW, изолированный, быстрый) — можно первым/параллельно. **SEC-01** (HIGH) — фундамент анти-абьюза; вводит сквозной слой enforcement и доступ к request-контексту (IP/UA), который **SEC-02** переиспользует для хэширования. Поэтому **SEC-01 → SEC-02**. SEC-02 пересекается с durable phone-аудитом [PV-09] (phone-пакет): durable-хранилище — там, проброс+хэш IP/UA — здесь.

```
SEC-03 (параллельно, изолированно)

SEC-01 ── SEC-02 ⇄ [PV-09] (phone durable audit, phone-пакет)
```

## Связь
Сквозной NFR-эпик поверх функциональных [`EPIC-IDS-EID`](../eid/EPIC-IDS-EID.md) и [`EPIC-IDS-PHONE`](../phone-verification/EPIC-IDS-PHONE.md). Парадигма: [`runtime-docs/04-security.md`](../../../runtime-docs/04-security.md).
