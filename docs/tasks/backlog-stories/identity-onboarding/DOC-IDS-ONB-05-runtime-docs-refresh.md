# DOC-IDS-ONB-05 — Освежить стейл runtime-docs под факт (`01-api`, `08-ui`)

## Meta
- **Key:** `DOC-IDS-ONB-05-runtime-docs-refresh`
- **Epic:** `EPIC-IDS-ONBOARDING`
- **Type:** doc task
- **Status:** 🟢 Done (verified [`01-api.md`](../../../runtime-docs/01-api.md) phone+OAuth+Telnyx routes vs [`asgi_app.py`](../../../../src/core/api/asgi_app.py), 2026-07-09)
- **Источник:** [`identity-onboarding-ux-2026-06-12.md`](../../../analysis/identity-onboarding-ux-2026-06-12.md) §4 G7
- **Зависит от:** —

## Зачем простыми словами
Док `01-api.md` отстал от кода: описывает OAuth как 501 и **не упоминает** телефонный флоу и Telnyx-webhook, которые уже built. Из-за этого читатель видит неверную картину API. Нужно привести таблицу маршрутов к факту.

## Что задокументировать (объём)
Свериться с фактическими роутами ([`asgi_app.py`](../../../../src/core/api/asgi_app.py)) и обновить:
- **Добавить** в `01-api.md` маршруты: `POST /auth/phone/request`, `POST /auth/phone/confirm` (PV-05 ✅), `POST /webhooks/telnyx/messaging` (PV-07 ✅).
- **Пометить план** для OAuth-трио (`/oauth/authorize`, `/oauth/authorize/complete`, `/oauth/token`) — сейчас 501, целевое — OAUTH-01.
- Проверить `08-ui-expectations` на согласованность с онбординг-контрактами (ссылки на DOC-ONB-01/03).

## Целевые файлы
- [`01-api.md`](../../../runtime-docs/01-api.md) — таблица маршрутов.
- [`08-ui-expectations.md`](../../../runtime-docs/08-ui-expectations.md) — перекрёстные ссылки (если не покрыто DOC-ONB-01/03).

## Вне scope
- Сам код OAuth — OAUTH-01.
- Контент контрактов гейта/verify — DOC-ONB-01/03 (тут только сверка ссылок).

## Definition of Done
- [ ] `01-api.md` содержит phone-маршруты и Telnyx-webhook; OAuth помечен как план (не «готово»).
- [ ] Все claims в обновлённых секциях сверены с `asgi_app.py` (`file:line`).
- [ ] Нет противоречий с DOC-ONB-01/03.

## Парадигма-якорь
[01-api](../../../runtime-docs/01-api.md), методология [`analysis.mdc`](../../../../.cursor/rules/analysis.mdc) (doc ↔ код).
