# DOC-IDS-ONB-03 — Контракт web-страницы verify + возврат в GPT

## Meta
- **Key:** `DOC-IDS-ONB-03-gpt-verify-landing-contract`
- **Epic:** `EPIC-IDS-ONBOARDING`
- **Type:** doc task
- **Status:** 🟢 Done
- **SSOT:** [`08-ui-expectations.md`](../../../runtime-docs/08-ui-expectations.md) §3c
- **Источник:** [`identity-onboarding-ux-2026-06-12.md`](../../../analysis/identity-onboarding-ux-2026-06-12.md) §2–3 (вход #2) + §4 G5; решение интервью — «redirect в наш web»
- **Зависит от:** [STORY-IDS-OAUTH-01](../oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md)…[OAUTH-04](../oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md) — **Done** (OAuth + verify-gate as-built; премиса «501 блокер» устарела)

## Зачем простыми словами
В GPT-ветке номер и код вводятся **не в чате**, а на нашей web-странице (безопаснее). GPT даёт ссылку → юзер открывает web-страницу verify → проходит OTP → возвращается в GPT уже верифицированным. Сама страница — на стороне UI (spa-app), но **контракт** (что она читает, как возвращает в GPT) нужно зафиксировать, чтобы UI и Identity/OAuth собрались вместе.

## Что задокументировать (объём)
- **Sequence входа #2** (словами): GPT «войти/создать стори» → redirect в web (через OAuth authorize) → Supabase login/signup → `authorize/complete` → если `phone_verified=false`: web verify-экран (disclosure → `/auth/phone/request` → OTP → `/auth/phone/confirm`) → повтор complete → возврат в GPT через OAuth callback (`redirect_uri?code=&state=`).
- **Контракт web verify-страницы:** какие параметры принимает (`context` из `verify_url` / `return_context`), что показывает (disclosure из [DOC-IDS-ONB-02](DOC-IDS-ONB-02-disclosure-copy.md)), как сигналит об успехе/ошибке, как инициирует возврат.
- **Возврат в GPT:** опереть на OAuth-callback (OAUTH-01…04 Done); связка GPT↔Supabase-user замыкается на `authorize/complete` → 302.
- **OAuth-зависимость:** OAUTH-01…04 **построены** — не блокер 501.

## Целевые файлы
- [`08-ui-expectations.md`](../../../runtime-docs/08-ui-expectations.md) §3c — «web verify-страница для GPT-редиректа».
- Перекрёстные ссылки: [`identity-onboarding-ux-2026-06-12.md`](../../../analysis/identity-onboarding-ux-2026-06-12.md), OAUTH-01…04.

## Вне scope
- Реализация OAuth-роутов — [OAUTH-01](../oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) (Done).
- Рендер страницы в spa-app (UI-репозиторий).

## Definition of Done
- [x] Sequence входа #2 задокументирован (redirect → verify → возврат).
- [x] Контракт web verify-страницы (вход/выход/возврат) зафиксирован в `08-ui-expectations.md` §3c.
- [x] Явно отмечена зависимость от OAUTH-01…04 (**Done**, не 501) и ссылка на disclosure-копирайт.

## Парадигма-якорь
[08-ui-expectations §3c](../../../runtime-docs/08-ui-expectations.md), [STORY-IDS-OAUTH-01](../oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md)…[OAUTH-04](../oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md).
