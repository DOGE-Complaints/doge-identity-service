# EPIC-IDS-13 — Онбординг и точки входа (web + GPT)

> **ID:** `EPIC-IDS-13` · **Alias (код/backlog):** `EPIC-IDS-ONBOARDING` · **Статус:** 🟡 In Progress (DOC-ONB-01…05 🟢; STORY-IDS-ONB-01 🟢 Done — email/`Confirm email`; product stories Done; epic gate / CLEANUP вне этого пакета)
> **Source (backlog):** [`backlog-stories/identity-onboarding/EPIC-IDS-ONBOARDING.md`](../../backlog-stories/identity-onboarding/EPIC-IDS-ONBOARDING.md)

## Назначение
Организовать **UX онбординга Identity** для двух точек входа в один аккаунт (Supabase user), с дружелюбным disclosure и гейтами верификации. Источник цели и решений — [`identity-onboarding-ux-2026-06-12.md`](../../../analysis/identity-onboarding-ux-2026-06-12.md) (gap G1–G7, интервью с продактом 2026-06-12).

Две точки входа:
1. **Web signup** (spa-app) — регистрация по email (Supabase Auth); телефон **лениво, по действию**.
2. **Редирект из кастомного GPT** — login/signup с **обязательным** телефоном; ввод номера/OTP — **redirect в наш web** (не через GPT-контекст). Технически гейтится OAuth (OAUTH-01).

OAuth-стори (код) живут под кодовым алиасом `EPIC-IDS-OAUTH` — переподчинены сюда на продуктовом уровне, файлы не перемещаются.

## Контекст и решения (база)
- Целевой UX + gap: [`identity-onboarding-ux-2026-06-12.md`](../../../analysis/identity-onboarding-ux-2026-06-12.md).
- No-frontend API-флоу телефона (готов): [`onboarding-phone-verification-api.md`](../../../runbook/onboarding-phone-verification-api.md).
- Образец-структура пакета: [`EPIC-IDS-PHONE`](../../backlog-stories/phone-verification/EPIC-IDS-PHONE.md).
- CAB-02 email: [`identity-cabinet-me-fields-interview-2026-07-13`](../../../analysis/identity-cabinet-me-fields-interview-2026-07-13.md) (D-CAB-3).

**Продуктовые решения (интервью 2026-06-12):** web-телефон = ленивый гейт по действию; GPT-OTP = redirect в web; email-гейт = полагаемся на Supabase «Confirm email»; disclosure = только web-экран verify; OAuth = код в OAUTH-эпике, тут проектируем UX; номер занят (409) = мягко «это вы?»; иностранный номер = отказ + waitlist.

## Stories
| Story / Doc task | Тема | Слой | Статус |
|------------------|------|------|--------|
| [DOC-IDS-ONB-01](stories/DOC-IDS-ONB-01-lazy-phone-gate-contract/DOC-IDS-ONB-01-lazy-phone-gate-contract.md) | контракт «ленивого гейта телефона» (consumer ↔ `phone_verified`) | контракт | 🟢 Done |
| [STORY-IDS-ONB-01](stories/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md) | `email` в `/me` + Supabase «Confirm email» | данные/конфиг | 🟢 Done (pkg-000045) |
| [DOC-IDS-ONB-02](../../backlog-stories/identity-onboarding/DOC-IDS-ONB-02-disclosure-copy.md) | disclosure-копирайт SSOT | UX-контент | 🟢 Done — [`onboarding-copy.md`](../../../runbook/onboarding-copy.md) |
| [DOC-IDS-ONB-03](../../backlog-stories/identity-onboarding/DOC-IDS-ONB-03-gpt-verify-landing-contract.md) | web-verify landing + возврат в GPT | контракт | 🟢 Done — [`08-ui` §3c](../../../runtime-docs/08-ui-expectations.md) |
| [DOC-IDS-ONB-04](../../backlog-stories/identity-onboarding/DOC-IDS-ONB-04-non-ee-waitlist-spec.md) | waitlist на не-EE номера | продукт | 🟢 Done — [`onboarding-waitlist.md`](../../../runbook/onboarding-waitlist.md) |
| [DOC-IDS-ONB-05](../../backlog-stories/identity-onboarding/DOC-IDS-ONB-05-runtime-docs-refresh.md) | освежить стейл `01-api`/`08-ui` | doc-drift | 🟢 Done (backlog) |
| [STORY-IDS-OAUTH-01](../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) … OAUTH-04 | OAuth + verify-gate (код) | код | 🟢 Done (EPIC-IDS-11) |

## Порядок реализации
**DOC-ONB-01** 🟢 (`pkg-000040`). **ONB-01** 🟢 (`pkg-000045`). **DOC-ONB-02** 🟢. **DOC-ONB-03** 🟢. **DOC-ONB-04** 🟢 (`onboarding-waitlist.md`). **DOC-ONB-05** 🟢. Onboarding doc-tasks закрыты.

```
DOC-ONB-01 🟢 ──► ONB-01 🟢 ──► DOC-ONB-02 🟢 ──► DOC-ONB-03 🟢 ──► DOC-ONB-04 🟢
OAUTH-01…04 🟢 (EPIC-IDS-11)
```

## Связь
Опирается на [`EPIC-IDS-PHONE`](../EPIC-IDS-10-phone-verification/EPIC-IDS-10-phone-verification.md) (телефонная верификация — готова) и [`EPIC-IDS-07-auth-core`](../EPIC-IDS-07-auth-core/EPIC-IDS-07-auth-core.md) (`/me`, профиль; AUTHCORE-02 🟢). Парадигма: [`08-ui-expectations`](../../../runtime-docs/08-ui-expectations.md), [`09-gateway-expectations`](../../../runtime-docs/09-gateway-expectations.md).

### Story 1: DOC-IDS-ONB-01 — Контракт «ленивого гейта телефона» — 🟢 Done

- **Pipeline story:** [`stories/DOC-IDS-ONB-01-lazy-phone-gate-contract/DOC-IDS-ONB-01-lazy-phone-gate-contract.md`](./stories/DOC-IDS-ONB-01-lazy-phone-gate-contract/DOC-IDS-ONB-01-lazy-phone-gate-contract.md)
- **Source (backlog):** [`backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md`](../../backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md)
- **Wave:** `pkg-000040`

**Definition of Done:**
- [x] В `09-gateway-expectations.md` описан контракт: consumer читает `phone_verified`, иначе ведёт на verify.
- [x] В `08-ui-expectations.md` добавлено ожидание verify-экрана по `phone_verified=false`.
- [x] Указан каноничный пример (создание стори) и явно: enforce — на потребителе.
- [x] Ссылка на флоу PV-05 и `onboarding-phone-verification-api.md`.

### Story 2: STORY-IDS-ONB-01 — `email` в `/me` + Supabase «Confirm email» — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md`](./stories/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md)
- **Source (backlog):** [`backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md`](../../backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md)
- **Wave:** `pkg-000045` (P3 Done 2026-07-24)

**Acceptance Criteria:**
- [x] `GET /me` возвращает `email` (из токена; `null`, если в токене нет).
- [x] `GET /me` возвращает `email_verified: true` (D-CAB-3, политика «токен ⇒ подтверждён»).
- [x] `supabase-project-setup.md` содержит обязательный пункт «включить Confirm email» (предусловие корректности `email_verified`).
- [x] `api-reference` (`openapi.yaml` `MeData` + `API_REFERENCE.md §6`) обновлён на `email` + `email_verified`.
- [x] Offline-тест (`test_me_profile.py`) на `email` и `email_verified`; согласовано с AUTHCORE-02 (один билдер `/me`).
