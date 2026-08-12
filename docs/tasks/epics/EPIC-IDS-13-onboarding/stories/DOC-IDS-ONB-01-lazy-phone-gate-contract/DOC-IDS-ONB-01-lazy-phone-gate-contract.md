# DOC-IDS-ONB-01 — Контракт «ленивого гейта телефона»

## Meta
- **Key:** `DOC-IDS-ONB-01-lazy-phone-gate-contract`
- **Parent Epic:** [`../../EPIC-IDS-13-onboarding.md`](../../EPIC-IDS-13-onboarding.md)
- **Epic alias (код/backlog):** `EPIC-IDS-ONBOARDING` · [`EPIC-IDS-ONBOARDING`](../../../../backlog-stories/identity-onboarding/EPIC-IDS-ONBOARDING.md)
- **Type:** doc task
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md`](../../../../backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md)
- **Decision Ref:** [`../../../../backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md`](../../../../backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md); [`identity-onboarding-ux-2026-06-12.md`](../../../../../analysis/identity-onboarding-ux-2026-06-12.md) §4 G3
- **Источник:** [`identity-onboarding-ux-2026-06-12.md`](../../../../../analysis/identity-onboarding-ux-2026-06-12.md) §4 G3; решение интервью — «лениво, по действию»
- **Зависит от:** [STORY-IDS-PV-05-verification-flow-api](../../../EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-05-verification-flow-api/STORY-IDS-PV-05-verification-flow-api.md) 🟢

## Зачем простыми словами
Телефон в web не спрашиваем при регистрации, а требуем **в момент защищённого действия** (напр. создать/опубликовать стори). Identity уже отдаёт `phone_verified` и умеет верифицировать — но **кто и когда требует телефон** нигде не описано. Нужно зафиксировать контракт: потребитель (web/gateway) перед защищённым действием смотрит `phone_verified`, иначе ведёт на верификацию.

## Что задокументировать (объём)
- **Контракт гейта:** consumer (spa-app / gateway) перед защищённым действием читает `GET /me.phone_verified`. Если `false` → не выполняет действие, ведёт пользователя на web-экран верификации (флоу PV-05: `/auth/phone/request` → OTP → `/auth/phone/confirm`).
- **Где enforce:** гейт — на стороне **потребителя**, не в Identity (Identity provider-agnostic, отдаёт только флаг + флоу). Зафиксировать явно.
- **Каноничный пример действия:** создание/публикация стори (стори живут в gateway).
- **Sequence** (словами): использует систему без телефона → защищённое действие → `phone_verified=false` → verify → действие разрешено.

## Целевые файлы
- [`09-gateway-expectations.md`](../../../../../runtime-docs/09-gateway-expectations.md) — секция «ленивый гейт телефона» (gateway читает `/me`/introspection).
- [`08-ui-expectations.md`](../../../../../runtime-docs/08-ui-expectations.md) — ожидание к spa-app (показать verify при `phone_verified=false`).

## Вне scope
- Код гейта в Identity (его там нет и не должно быть).
- Список всех защищённых действий — за gateway/продуктом.

## Definition of Done
- [x] В `09-gateway-expectations.md` описан контракт: consumer читает `phone_verified`, иначе ведёт на verify.
- [x] В `08-ui-expectations.md` добавлено ожидание verify-экрана по `phone_verified=false`.
- [x] Указан каноничный пример (создание стори) и явно: enforce — на потребителе.
- [x] Ссылка на флоу PV-05 и `onboarding-phone-verification-api.md`.

## Парадигма-якорь
[09-gateway-expectations](../../../../../runtime-docs/09-gateway-expectations.md), [08-ui-expectations](../../../../../runtime-docs/08-ui-expectations.md).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-13-01-t01-lazy-gate-doc-gap-audit`](./task-ids-13-01-t01-lazy-gate-doc-gap-audit/README.md) | pkg-000040 |
| 2 | [`task-ids-13-01-t02-gateway-lazy-phone-gate-section`](./task-ids-13-01-t02-gateway-lazy-phone-gate-section/README.md) | pkg-000040 |
| 3 | [`task-ids-13-01-t03-ui-lazy-verify-screen-expectation`](./task-ids-13-01-t03-ui-lazy-verify-screen-expectation/README.md) | pkg-000040 |
| 4 | [`task-ids-13-01-t04-pv05-runbook-crosslinks-sequence`](./task-ids-13-01-t04-pv05-runbook-crosslinks-sequence/README.md) | pkg-000040 |
| 5 | [`task-ids-13-01-t05-story-acceptance-verification`](./task-ids-13-01-t05-story-acceptance-verification/README.md) | pkg-000040 |
