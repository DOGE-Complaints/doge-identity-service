# EPIC-IDS-ONBOARDING — Онбординг и точки входа (web + GPT)

> **ID:** `EPIC-IDS-ONBOARDING` · **Статус:** 🟢 Doc-tasks **закрыты** (DOC-ONB-01…05 ✅; ONB-01 🟢); identity-backend закрыт; waitlist durable API — вне identity (см. [`onboarding-waitlist.md`](../../../runbook/onboarding-waitlist.md)). · **Тип:** Продуктово-UX-зонтик (контракты), **не код-слой**
> **Не декомпозирован** в pipeline — набор backlog-стори и doc-task'ов.
> **Зонтик:** объединяет онбординг-журнэй обоих входов. OAuth-стори (код) живут под кодовым алиасом `EPIC-IDS-OAUTH` (`next_epic` в [`asgi_app.py`](../../../../src/core/api/asgi_app.py)) — переподчинены сюда на продуктовом уровне, файлы не перемещаются (чтобы не ломать ссылки/`next_epic`).

## Назначение
Организовать **UX онбординга Identity** для двух точек входа в один аккаунт (Supabase user), с дружелюбным disclosure и гейтами верификации. Источник цели и решений — [`identity-onboarding-ux-2026-06-12.md`](../../../analysis/identity-onboarding-ux-2026-06-12.md) (gap G1–G7, интервью с продактом 2026-06-12).

Две точки входа:
1. **Web signup** (spa-app) — регистрация по email (Supabase Auth); телефон **лениво, по действию**.
2. **Редирект из кастомного GPT** — login/signup с **обязательным** телефоном; ввод номера/OTP — **redirect в наш web** (не через GPT-контекст). Технически гейтится OAuth (OAUTH-01).

## Контекст и решения (база)
- Целевой UX + gap: [`identity-onboarding-ux-2026-06-12.md`](../../../analysis/identity-onboarding-ux-2026-06-12.md).
- No-frontend API-флоу телефона (готов): [`onboarding-phone-verification-api.md`](../../../runbook/onboarding-phone-verification-api.md).
- Образец-структура пакета: [`EPIC-IDS-PHONE`](../phone-verification/EPIC-IDS-PHONE.md).

**Продуктовые решения (интервью 2026-06-12):** web-телефон = ленивый гейт по действию; GPT-OTP = redirect в web; email-гейт = полагаемся на Supabase «Confirm email»; disclosure = только web-экран verify; OAuth = код в OAUTH-эпике, тут проектируем UX; номер занят (409) = мягко «это вы?»; иностранный номер = отказ + waitlist.

## Типы элементов
- **Story** — реализуемая работа (код/контракт), есть Acceptance Criteria.
- **Doc task** — чисто документация/контракт/копирайт, есть Definition of Done. Помечены `DOC-IDS-ONB-*`.

## Состав пакета
| Элемент | Тип | Тема | Gap | Слой | Зависит | Статус |
|---------|-----|------|-----|------|---------|--------|
| [STORY-IDS-OAUTH-01](../oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) | story | OAuth-сервер наружу (`/oauth/*` → движок) | G1 | код | AUTHCORE-01 | 🟢 Done (pkg-000029) |
| [STORY-IDS-OAUTH-02](../oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md) | story | introspection + сервисный токен | G1 | код | OAUTH-01, EID-01 | 🟢 Done (pkg-000030) |
| [STORY-IDS-ONB-01](STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md) | story | `email` в `/me` + требование Supabase «Confirm email» | G2 | данные/конфиг | AUTHCORE-01 | 🟢 **Done (pkg-000045, EPIC-IDS-13, 2026-07-24)** — `email`+`email_verified` в [`me_response.py:21-22`](../../../../src/core/api/me_response.py); нота в [`supabase-project-setup.md:50-58`](../../../runbook/supabase-project-setup.md) §2a. Аудит: [onb-01-code-audit](../../../analysis/identity-onb-01-code-audit-2026-07-24.md) |
| [DOC-IDS-ONB-01](DOC-IDS-ONB-01-lazy-phone-gate-contract.md) | doc task | контракт «ленивого гейта телефона» (consumer ↔ `phone_verified`) | G3 | контракт | PV-05 ✅ | 🟢 Done (pkg-000040, EPIC-IDS-13) |
| [DOC-IDS-ONB-02](DOC-IDS-ONB-02-disclosure-copy.md) | doc task | disclosure-копирайт SSOT + граничные сообщения | G4 | UX-контент | — | 🟢 **Done** — SSOT [`onboarding-copy.md`](../../../runbook/onboarding-copy.md) (EN canon + boundary; spa render = follow-up) |
| [DOC-IDS-ONB-03](DOC-IDS-ONB-03-gpt-verify-landing-contract.md) | doc task | web-verify landing + возврат в GPT (контракт) | G5 | контракт | OAUTH-01 ✅ | 🟢 **Done** — SSOT [`08-ui` §3c](../../../runtime-docs/08-ui-expectations.md) (sequence + verify_url/context + OAuth complete return; spa render вне scope) |
| [DOC-IDS-ONB-04](DOC-IDS-ONB-04-non-ee-waitlist-spec.md) | doc task | waitlist на не-EE номера (куда собираем email) | G6 | продукт | DOC-ONB-02 | 🟢 **Done** — SSOT [`onboarding-waitlist.md`](../../../runbook/onboarding-waitlist.md) (spa → Waitlist API; identity = `COUNTRY_NOT_ALLOWED` only; LOW/post-MVP) |
| [DOC-IDS-ONB-05](DOC-IDS-ONB-05-runtime-docs-refresh.md) | doc task | освежить стейл `01-api`/`08-ui` под факт | G7 | doc-drift | — | ✅ **Done** — [`01-api`](../../../runtime-docs/01-api.md) и [`08-ui`](../../../runtime-docs/08-ui-expectations.md) освежены 2026-06-24 (full-audit) |

> Список **открыт**: при интеграции с фронтом и отладке добавятся стори (реальные экраны/эндпоинты, обработка ошибок).

## Актуальность после построения OAuth/phone (сверка 2026-06-26)
**Какой это слой.** Не код-слой, а **продуктово-UX-зонтик контрактов** онбординга: 1 маленькая бэкенд-стори (`ONB-01`) + 5 doc-task'ов. OAuth-код живёт в [`EPIC-IDS-OAUTH`](../oauth/EPIC-IDS-OAUTH.md) (🟢) и сюда лишь **переподчинён продуктово** (файлы не переносятся).

**Депрекейтнут ли пакет?** Нет — но **в значительной части уже исчерпан** построенным бэкендом и обновлёнными доками (а не отдельной волной онбординга):
- Зонтик строился под цель «вход #2 из GPT гейтится OAuth + phone». Этот бэкенд **построен**: OAUTH-01…04 (authorize/complete/token/introspect + verify-gate `verification_required`), phone-верификация (PV), `verify_url` ([`spa_login.py`](../../../../src/core/oauth/spa_login.py)). Премиса doc-task'ов «OAUTH-01 = 501 блокер» — **устарела**.
- Поэтому: `DOC-ONB-01`…`DOC-ONB-05` и `DOC-ONB-02`/`04` SSOT runbooks — **✅**.
- Остаток вне identity: durable Waitlist API (если не mock) — owner вне этого репо; см. [`onboarding-waitlist.md`](../../../runbook/onboarding-waitlist.md).

**Identity-backend и onboarding doc-tasks в пакете закрыты** (`ONB-01` 🟢; DOC-ONB-01…05 🟢).

## Порядок реализации
**DOC-ONB-02 (copy) / DOC-ONB-05 (docs)** — без зависимостей, можно сразу → **ONB-01** (после AUTHCORE-01) и **DOC-ONB-01** (PV-05 готов) — параллельно → **OAUTH-01** (код, движок готов) → **DOC-ONB-03** (web-verify, нужен OAuth-возврат) → **DOC-ONB-04** (waitlist, нужен copy) → **OAUTH-02** (introspection, замыкает GPT-склейку).

```
DOC-ONB-02 ─┐
DOC-ONB-05 ─┤ (сразу)
ONB-01 ─────┤ (AUTHCORE-01)
DOC-ONB-01 ─┘ (PV-05 ✅)
OAUTH-01 ──► DOC-ONB-03 ──► OAUTH-02      ← вход #2 (GPT) end-to-end
DOC-ONB-02 ──► DOC-ONB-04 (waitlist)
```

## Связь
Опирается на [`EPIC-IDS-PHONE`](../phone-verification/EPIC-IDS-PHONE.md) (телефонная верификация — готова) и [`EPIC-IDS-AUTH-CORE`](../auth-core/STORY-IDS-AUTHCORE-01-profile-and-me.md) (`/me`, профиль). Целевой UX: [`identity-onboarding-ux-2026-06-12.md`](../../../analysis/identity-onboarding-ux-2026-06-12.md). Парадигма: [`08-ui-expectations`](../../../runtime-docs/08-ui-expectations.md), [`09-gateway-expectations`](../../../runtime-docs/09-gateway-expectations.md).
