# EPIC-IDS-12 — Security hardening (cross-cutting gaps аудита 2026-06-24)

> **ID:** `EPIC-IDS-12` · **Alias (код/backlog):** `EPIC-IDS-SEC` · **Статус:** 🟡 In Progress · **Тип:** Сквозной (security/NFR)
> **Source (backlog):** [`backlog-stories/security-hardening/EPIC-IDS-SEC.md`](../../backlog-stories/security-hardening/EPIC-IDS-SEC.md)

## Назначение
Закрыть **сквозные security-гэпы**, найденные жёстким аудитом backend identity (2026-06-24, §3). Это не про новый функционал, а про защитные NFR, которые спеки требуют, но код **не реализует**: отсутствие rate-limiting, аудит без хэшированных IP/UA, и недо-валидация Supabase-JWT. Гэпы кросс-режимные — затрагивают и eID (отложен), и активный phone-гейт. Решение оператора по аудиту (Q2): «только отчёт + severity, сборку решаем позже» — этот эпик переводит §3 в проверяемые backlog-стори **уровня требований**.

Каждая стори: только **что должно быть истинно** (требования + критерии приёмки), без выбора middleware/библиотек/схемы — это решается на этапе реализации.

## Контекст и решения (база)
- Аудит-источник: [`identity-backend-full-audit-2026-06-24.md`](../../../analysis/identity-backend-full-audit-2026-06-24.md) §3 (таблица G-1…G-5), §0 (решения оператора).
- Спеки-требования: [`16-security-privacy-observability.md`](../../../requirements/16-security-privacy-observability.md), [`11-eid-verification-flow.md`](../../../requirements/11-eid-verification-flow.md), [`09-supabase-jwt-validation.md`](../../../requirements/09-supabase-jwt-validation.md).
- Парадигма-якорь: [`runtime-docs/04-security.md`](../../../runtime-docs/04-security.md).
- Связанный пакет: [`EPIC-IDS-PHONE`](../../backlog-stories/phone-verification/EPIC-IDS-PHONE.md) (durable phone-аудит PV-09 пересекается с SEC-02).

**Объём по severity (из §3):** G-1 (HIGH, rate-limit), G-2b (HIGH, IP/UA-хэш аудита — durable-часть G-2 живёт в phone-пакете), G-5 (LOW, JWT-hardening). G-3/G-4 — вне этого эпика (durable phone-сессии и eID session-enc, deferred-домены).

## Stories
| Story | Тема | Слой | Зависит | Статус |
|-------|------|------|---------|--------|
| [STORY-IDS-SEC-01](stories/STORY-IDS-SEC-01-rate-limiting/STORY-IDS-SEC-01-rate-limiting.md) | Per-user rate limiting + 429/`retry_after` для чувствительных роутов (G-1) | оркестрация / cross-cutting | — | 🟢 Done |
| [STORY-IDS-SEC-01b](stories/STORY-IDS-SEC-01b-phone-request-http-rate-limit/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md) | HTTP rate-limit `POST /auth/phone/request` (остаток G-1) | оркестрация / phone | SEC-01 | 🟢 Done |
| [STORY-IDS-SEC-02](stories/STORY-IDS-SEC-02-audit-ip-ua-hashing/STORY-IDS-SEC-02-audit-ip-ua-hashing.md) | Хэшированные IP/UA в аудит-событиях (eID + phone) (G-2b) | аудит / cross-cutting | SEC-01 | 🟢 Done |
| [STORY-IDS-SEC-03](stories/STORY-IDS-SEC-03-jwt-validation-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md) | Валидация `aud` + сверка формы импорта ключа Supabase-JWT (G-5) | auth | — | 🟢 Done |
| [STORY-IDS-SEC-04](stories/STORY-IDS-SEC-04-service-role-isolation/STORY-IDS-SEC-04-service-role-isolation.md) | service_role isolation boundary + rotation | cross-service | — | 🟢 Done |
| [STORY-IDS-SEC-06](stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md) | Supabase-JWT: JWKS-only, DI, ES256-тесты, удаление `SUPABASE_JWT_SECRET` | auth | SEC-03 | 🟢 Done |

## Порядок реализации
**SEC-03** (LOW, изолированный, быстрый) — можно первым/параллельно. **SEC-01** (HIGH) — фундамент анти-абьюза; вводит сквозной слой enforcement и доступ к request-контексту (IP/UA), который **SEC-02** переиспользует для хэширования. Поэтому **SEC-01 → SEC-02**. SEC-02 пересекается с durable phone-аудитом [PV-09] (phone-пакет): durable-хранилище — там, проброс+хэш IP/UA — здесь.

```
SEC-03 (параллельно, изолированно)

SEC-01 ── SEC-02 ⇄ [PV-09] (phone durable audit, phone-пакет)
```

## Связь
Сквозной NFR-эпик поверх функциональных [`EPIC-IDS-EID`](../../backlog-stories/eid/EPIC-IDS-EID.md) и [`EPIC-IDS-PHONE`](../../backlog-stories/phone-verification/EPIC-IDS-PHONE.md). Парадигма: [`runtime-docs/04-security.md`](../../../runtime-docs/04-security.md).

### Story 1: STORY-IDS-SEC-01 — Per-user rate limiting + 429/`retry_after` — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-SEC-01-rate-limiting/STORY-IDS-SEC-01-rate-limiting.md`](./stories/STORY-IDS-SEC-01-rate-limiting/STORY-IDS-SEC-01-rate-limiting.md)
- **Source (backlog):** [`backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md`](../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md)
- **Wave:** pkg-000035 (7 tasks, P3 Done 2026-06-26, 369 pytest offline)

**Acceptance Criteria:**
- [x] Зафиксирован перечень чувствительных identity-роутов с лимитом (requests/window/scope) на каждый; значения для `/auth/eid/start` = 5/10мин/user соответствуют [`11-eid-verification-flow.md`](../../../requirements/11-eid-verification-flow.md) и [`16-security-privacy-observability.md`](../../../requirements/16-security-privacy-observability.md).
- [x] При превышении лимита роут отвечает HTTP `429` с `retry_after` (секунды) в конверте ошибки; форма ответа согласована с envelope-контрактом сервиса.
- [x] Лимит применяется до бизнес-логики хендлера (сквозной слой), а не индивидуально внутри каждого хендлера — зафиксировано как требование.
- [x] Описано непротиворечивое сосуществование с OTP-cooldown (`PHONE_RESEND_COOLDOWN_S`): что остаётся доменной ошибкой, что мапится в 429.
- [x] Лимиты и окна задаются конфигом; тест демонстрирует 429+`retry_after` на N+1-м запросе в окне для хотя бы одного роута.
- [ ] (Альтернатива, если оператор решит не строить) — таблица `RATE_LIMITS`/требование 11:127-130 явно помечены **DEFERRED** в спеках с обоснованием; AC закрывается этой пометкой.

### Story 2: STORY-IDS-SEC-01b — HTTP rate-limit на `POST /auth/phone/request` — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-SEC-01b-phone-request-http-rate-limit/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](./stories/STORY-IDS-SEC-01b-phone-request-http-rate-limit/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md)
- **Source (backlog):** [`backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../../backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md)
- **Wave:** pkg-000036 (6 tasks, P3 Done 2026-06-26, 371 pytest offline)

**Acceptance Criteria:**
- [x] `POST /auth/phone/request` wired на HTTP rate-limit (per-user); лимит и окно в конфиге.
- [x] При превышении HTTP-окна — 429 + `retry_after` в envelope; cooldown по-прежнему 400 без `retry_after`.
- [x] Политика сосуществования задокументирована (analysis + runtime-docs/spec 19).
- [x] Offline-тест демонстрирует оба сценария (429 window vs 400 cooldown).

### Story 3: STORY-IDS-SEC-02 — Хэшированные IP/UA в аудит-событиях (eID + phone) — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-SEC-02-audit-ip-ua-hashing/STORY-IDS-SEC-02-audit-ip-ua-hashing.md`](./stories/STORY-IDS-SEC-02-audit-ip-ua-hashing/STORY-IDS-SEC-02-audit-ip-ua-hashing.md)
- **Source (backlog):** [`backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md`](../../backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md)
- **Wave:** pkg-000037 (6 tasks, P3 Done 2026-06-26, 375 pytest offline)

**Acceptance Criteria:**
- [x] Request-контекст (IP, User-Agent) доходит до аудит-функций для **обоих** режимов — eID и phone (а не передаётся `None`, как сейчас в [`handlers.py:162-163`](../../../src/core/api/handlers.py)).
- [x] IP и UA сохраняются исключительно как хэш (через [`hash_secret`](../../../src/core/security/hashing.py)); сырой IP/UA в хранилище аудита отсутствует — проверяемо тестом.
- [x] `PhoneAuditEvent` ([`models.py:92`](../../../src/core/domain/models.py)) получает поля `ip_hash`/`user_agent_hash`, согласованные с eID-аудитом и со стори PV-09.
- [x] Инвариант «нет PII в аудите» сохранён: ни сырого IP/UA, ни сырого телефона/кода — тест подтверждает.
- [x] Выбор алгоритма хэша (HMAC-с-ключом vs sha256 из примера спеки 16) зафиксирован; при расхождении со спекой 16 — спека обновлена под фактический выбор.

### Story 4: STORY-IDS-SEC-03 — Валидация `aud` + сверка формы импорта ключа Supabase-JWT — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-SEC-03-jwt-validation-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md`](./stories/STORY-IDS-SEC-03-jwt-validation-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md)
- **Source (backlog):** [`backlog-stories/security-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md`](../../backlog-stories/security-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md)
- **Wave:** pkg-000038 (6 tasks, P3 Done 2026-06-26, 379 pytest offline)

**Acceptance Criteria:**
- [x] Принято и задокументировано решение по `aud`: либо `aud=authenticated` валидируется (зафиксировано как требование к валидатору), либо в спеке [`09`](../../../requirements/09-supabase-jwt-validation.md) явно зафиксировано «намеренно не валидируется» с обоснованием.
- [x] Если решение — валидировать: критерий проверяем тестом (токен с `aud≠authenticated` отклоняется; токен с `aud=authenticated` проходит).
- [x] Форма импорта ключа подтверждена против **реального** Supabase-токена (сырая строка vs base64url-обёртка); код и спека [`09`](../../../requirements/09-supabase-jwt-validation.md) приведены к одной форме.
- [x] Расхождение G-5 между [`supabase_validator.py`](../../../src/core/auth/supabase_validator.py) и спекой 09 устранено (нет открытых «честных note» о несоответствии).
- [x] Регрессий нет: ранее-корректные проверки `iss`/`sub`/`exp`/`role` сохранены (базовая линия — зелёная сюита из аудита §6).

### Story 5: STORY-IDS-SEC-04 — Изоляция Supabase `service_role`: identity — единственный держатель — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-SEC-04-service-role-isolation/STORY-IDS-SEC-04-service-role-isolation.md`](./stories/STORY-IDS-SEC-04-service-role-isolation/STORY-IDS-SEC-04-service-role-isolation.md)
- **Source (backlog):** [`backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md`](../../backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md)
- **Wave:** pkg-000043 (5 tasks, P3 Done 2026-07-09, 402 pytest offline)

**Acceptance Criteria:**
- [x] Зафиксировано требование «identity — единственный держатель `service_role`; не в браузере» (в 04-security / 07-env / runbook).
- [x] No-expose подтверждён (нет в логах/ответах/trace) — проверяемо.
- [x] Rotation runbook написан (Dashboard → identity env; триггеры).
- [x] Ротация скоординирована с spa [SEC-01](../../../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-01-remove-service-role-from-frontend.md) (если был фронт-bundle).

### Story 6: STORY-IDS-SEC-06 — Supabase-JWT: JWKS-only, DI, честные тесты — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](./stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md)
- **Source (backlog):** [`backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md)
- **Wave:** pkg-000042 (8 tasks, P3 Done 2026-07-04, 398 pytest offline)

**Acceptance Criteria:** см. pipeline story (verbatim из backlog); P3 Done 2026-07-04.
