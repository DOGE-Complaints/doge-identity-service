# DOC-IDS-ONB-04 — Waitlist на не-эстонские номера (продуктовая спека)

## Meta
- **Key:** `DOC-IDS-ONB-04-non-ee-waitlist-spec`
- **Epic:** `EPIC-IDS-ONBOARDING`
- **Type:** doc task
- **Status:** 🟢 Done
- **SSOT:** [`docs/runbook/onboarding-waitlist.md`](../../../runbook/onboarding-waitlist.md)
- **Источник:** [`identity-onboarding-ux-2026-06-12.md`](../../../analysis/identity-onboarding-ux-2026-06-12.md) §2 + §4 G6; решение интервью — «отказ + waitlist»
- **Зависит от:** [DOC-IDS-ONB-02](DOC-IDS-ONB-02-disclosure-copy.md) (сообщение про waitlist) ✅

## Зачем простыми словами
Сейчас разрешены только эстонские номера (+372); иностранный → `COUNTRY_NOT_ALLOWED`. По решению — не просто отказ, а **сбор интереса**: «хотите свою страну? оставьте email». Нужно определить, **куда** этот email собираем и как это выглядит, чтобы спрос на расширение географии не терялся.

## Что задокументировать (объём)
- **Точка отказа:** `assert_allowed_dial_prefix` → `COUNTRY_NOT_ALLOWED` ([`e164.py`](../../../../src/core/phone/e164.py)); префиксы — `PHONE_ALLOWED_DIAL_PREFIXES` ([`schema.py`](../../../../src/core/config/schema.py)).
- **Куда собираем email (выбрано):** **spa → dedicated Waitlist API** (`POST /waitlist` при `VITE_WAITLIST_API_*`); не identity Supabase / не identity log-event. Identity только сигналит `COUNTRY_NOT_ALLOWED`. Поля: `email`, `country`, опц. `organization`; `created_at` на API.
- **UX-сообщение:** из [DOC-IDS-ONB-02](DOC-IDS-ONB-02-disclosure-copy.md) / [`onboarding-copy.md`](../../../runbook/onboarding-copy.md).
- **Граница MVP:** LOW / post-MVP для identity; spa UI waitlist уже Done (SPA-ID-07).

## Целевые файлы
- SSOT: [`docs/runbook/onboarding-waitlist.md`](../../../runbook/onboarding-waitlist.md)
- Pointers: [`onboarding-copy.md`](../../../runbook/onboarding-copy.md), [`08-ui-expectations.md`](../../../runtime-docs/08-ui-expectations.md)

## Вне scope
- Реальный сбор/хранение в identity (код) — только если продукт потребует identity-owned endpoint (см. promotion criterion в SSOT).
- Расширение списка стран в `PHONE_ALLOWED_DIAL_PREFIXES` — отдельное продуктовое решение.
- Правки `docs/analysis/**` в этой задаче.

## Definition of Done
- [x] Зафиксировано, **куда** собираем waitlist-email (выбран вариант + поля).
- [x] UX-сообщение согласовано с DOC-IDS-ONB-02.
- [x] Помечено как LOW / post-MVP; критерий, когда превращается в identity story.

## Парадигма-якорь
[04-security](../../../runtime-docs/04-security.md) (минимизация данных), [`onboarding-waitlist.md`](../../../runbook/onboarding-waitlist.md).
