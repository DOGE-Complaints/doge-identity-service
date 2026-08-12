# DOC-IDS-ONB-02 — Disclosure-копирайт (SSOT) + граничные сообщения

## Meta
- **Key:** `DOC-IDS-ONB-02-disclosure-copy`
- **Epic:** `EPIC-IDS-ONBOARDING`
- **Type:** doc task
- **Status:** 🟢 Done
- **SSOT:** [`docs/runbook/onboarding-copy.md`](../../../runbook/onboarding-copy.md)
- **Источник:** [`identity-onboarding-ux-2026-06-12.md`](../../../analysis/identity-onboarding-ux-2026-06-12.md) §2 (disclosure) + §4 G4; решение интервью — «только web-экран», дружелюбный тон
- **Зависит от:** —

## Зачем простыми словами
Перед вводом номера пользователь должен понимать, **зачем** мы просим телефон: защита от ботов и чужаков, чистота экосистемы, пока только эстонские номера. Этот текст и сообщения об ошибках сейчас нигде не зафиксированы — UI пишет их «от себя». Нужен единый источник копирайта (SSOT), который использует web-экран verify.

## Что задокументировать (объём)
- **Disclosure-блок** (показывается на web-экране verify перед вводом номера). Канон-драфт (EN) — в [`identity-onboarding-ux-2026-06-12.md`](../../../analysis/identity-onboarding-ux-2026-06-12.md) §2; перенести/закрепить как SSOT.
- **Граничные сообщения** (привязка к кодам ошибок Identity):
  - `COUNTRY_NOT_ALLOWED` (иностранный номер) → **отказ + waitlist** (сбор email на расширение географии).
  - `profile_conflict` / 409 (номер занят) → **мягко «это вы?»** (войдите в тот аккаунт / другой номер; без раскрытия чужого).
- **Тон:** дружелюбный, человеческий, показываем пользу, без канцелярита.
- **Локализация:** EN — канон; ET/RU — follow-up (отметить).

## Целевые файлы
- SSOT: [`docs/runbook/onboarding-copy.md`](../../../runbook/onboarding-copy.md)
- Перекрёстная ссылка из [`identity-onboarding-ux-2026-06-12.md`](../../../analysis/identity-onboarding-ux-2026-06-12.md) и [`08-ui-expectations.md`](../../../runtime-docs/08-ui-expectations.md) §3b.

## Вне scope
- Рендер копирайта в spa-app (это UI-репозиторий).
- Сам waitlist-механизм — [DOC-IDS-ONB-04](DOC-IDS-ONB-04-non-ee-waitlist-spec.md).

## Definition of Done
- [x] Disclosure-текст (EN) закреплён как SSOT в одном месте.
- [x] Сообщения для `COUNTRY_NOT_ALLOWED` (waitlist) и 409 («это вы?») зафиксированы и привязаны к кодам ошибок.
- [x] Отмечена локализация ET/RU как follow-up.
- [x] Ссылка на коды ошибок ([`base.py` `SmsErrorCode`](../../../../src/core/phone/base.py)).

## Парадигма-якорь
[08-ui-expectations](../../../runtime-docs/08-ui-expectations.md), [04-security](../../../runtime-docs/04-security.md) (минимизация/anti-abuse).
