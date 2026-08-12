# DOC-IDS-ONB-01 — Контракт «ленивого гейта телефона»

## Meta
- **Key:** `DOC-IDS-ONB-01-lazy-phone-gate-contract`
- **Epic:** `EPIC-IDS-ONBOARDING`
- **Type:** doc task
- **Status:** 🟢 Done
- **Источник:** [`identity-onboarding-ux-2026-06-12.md`](../../../analysis/identity-onboarding-ux-2026-06-12.md) §4 G3; решение интервью — «лениво, по действию»
- **Зависит от:** [PV-05](../phone-verification/STORY-IDS-PV-05-verification-flow-api.md) ✅ (флоу + `/me.phone_verified` уже есть)

## Зачем простыми словами
Телефон в web не спрашиваем при регистрации, а требуем **в момент защищённого действия** (напр. создать/опубликовать стори). Identity уже отдаёт `phone_verified` и умеет верифицировать — но **кто и когда требует телефон** нигде не описано. Нужно зафиксировать контракт: потребитель (web/gateway) перед защищённым действием смотрит `phone_verified`, иначе ведёт на верификацию.

## Что задокументировать (объём)
- **Контракт гейта:** consumer (spa-app / gateway) перед защищённым действием читает `GET /me.phone_verified`. Если `false` → не выполняет действие, ведёт пользователя на web-экран верификации (флоу PV-05: `/auth/phone/request` → OTP → `/auth/phone/confirm`).
- **Где enforce:** гейт — на стороне **потребителя**, не в Identity (Identity provider-agnostic, отдаёт только флаг + флоу). Зафиксировать явно.
- **Каноничный пример действия:** создание/публикация стори (стори живут в gateway).
- **Sequence** (словами): использует систему без телефона → защищённое действие → `phone_verified=false` → verify → действие разрешено.

## Целевые файлы
- [`09-gateway-expectations.md`](../../../runtime-docs/09-gateway-expectations.md) — секция «ленивый гейт телефона» (gateway читает `/me`/introspection).
- [`08-ui-expectations.md`](../../../runtime-docs/08-ui-expectations.md) — ожидание к spa-app (показать verify при `phone_verified=false`).

## Вне scope
- Код гейта в Identity (его там нет и не должно быть).
- Список всех защищённых действий — за gateway/продуктом.

## Definition of Done
- [x] В `09-gateway-expectations.md` описан контракт: consumer читает `phone_verified`, иначе ведёт на verify.
- [x] В `08-ui-expectations.md` добавлено ожидание verify-экрана по `phone_verified=false`.
- [x] Указан каноничный пример (создание стори) и явно: enforce — на потребителе.
- [x] Ссылка на флоу PV-05 и `onboarding-phone-verification-api.md`.

## Парадигма-якорь
[09-gateway-expectations](../../../runtime-docs/09-gateway-expectations.md), [08-ui-expectations](../../../runtime-docs/08-ui-expectations.md).
