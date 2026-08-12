# STORY-IDS-SEC-05 — ADR: модель auth-кредов (Supabase-anon-resource-server vs identity-BFF)

## Meta
- **Key:** `STORY-IDS-SEC-05-auth-credential-model-adr`
- **Epic:** [`EPIC-IDS-SEC`](EPIC-IDS-SEC.md)
- **Status:** 🟢 Решено — **вариант B (identity-BFF)** (оператор, 2026-06-27)
- **Severity:** 🟡 decision (ADR)
- **Источник:** запрос оператора 2026-06-27 «хранить supabase ключ и url на фронте не стоит»; [`split-doc §4.4, §8`](../../../../../spa-app/docs/analysis/identity-supabase-frontend-split-2026-06-16.md)
- **Парная spa-стори:** [`STORY-SPA-SEC-02`](../../../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-02-supabase-credential-boundary.md)

> **🟢 РЕШЕНИЕ (2026-06-27):** выбран **вариант B — identity-BFF**: браузер без Supabase-кредов, identity проксирует Supabase-Auth; сессия — **httpOnly cookie** (refresh на сервере); Supabase **остаётся** движком за proxy. Контракт/дизайн → [`auth-bff-proxy-design-2026-06-27.md`](../../../analysis/auth-bff-proxy-design-2026-06-27.md). Реализация → пакет [`EPIC-IDS-AUTHBFF`](../auth-bff/EPIC-IDS-AUTHBFF.md) (AUTHBFF-01/02/03). Эта стори остаётся как **ADR-запись решения**.
> **Поправка по факту:** `service_role` фронтом **не использовался** (фронт на anon) — решение B про вынос anon-Auth-поверхности, **не** про service_role.

## Зачем простыми словами
Оператор спросил: правильно ли, что браузер вообще держит Supabase-креды. Честно: `anon`-ключ + URL — **публичны by design** (anon защищён RLS, это не секрет), поэтому текущая модель (браузер ↔ Supabase Auth напрямую, identity = resource server) — **стандарт Supabase-SPA, не дыра**. Но есть альтернатива — **BFF**: браузер ходит за логином в **identity**, а identity сам общается с Supabase (server-side), и тогда у браузера **нет вообще никаких** Supabase-кредов. Это меняет роль identity (появляется login-поверхность, которой **сейчас в коде нет**). Стори — принять решение архитектурно (ADR), а не «по ощущению».

## Точки в коде (текущее состояние)
- identity **не** имеет login-эндпоинтов (`/auth/login|signup`, password) — grep по [`asgi_app.py`](../../../../src/core/api/asgi_app.py) пусто. identity только **валидирует** Supabase-JWT ([`supabase_validator.py`](../../../../src/core/auth/supabase_validator.py)).
- Браузер логинится напрямую в Supabase Auth (spa [`LoginPage.jsx`](../../../../../spa-app/src/pages/LoginPage.jsx), `@supabase/supabase-js`).
- Вывод: вариант BFF — **net-new** для identity (login/refresh/session relay), не «доработка».

## Scope (требования — ADR)
- **ADR с двумя вариантами и решением:**
  - **A — anon-resource-server (текущий):** браузер ↔ Supabase Auth (anon), identity = resource server. Anon-ключ публичен by-design; зафиксировать это явно. Минимум изменений.
  - **B — identity-BFF:** браузер ↔ identity (login/signup/session), identity ↔ Supabase (server). Браузер без Supabase-кредов. Требует новых identity-эндпоинтов (login/refresh/logout), хранения/relay сессии (cookie?), CORS/CSRF-модели.
- **Критерии решения:** угроза-модель (что реально защищаем — anon не секрет), latency, сложность, кто владеет refresh-токеном, единый домен.
- **Если выбран B:** зафиксировать контракт auth-proxy-эндпоинтов (метод/тело/ответ/сессия) как отдельный backlog (реализация — вне ADR).
- **Если выбран A:** зафиксировать в 04-security/07-env «anon — публичный, by design; service_role — только identity (SEC-04)»; ничего не строим.

## Вне scope
- Реализация proxy-эндпоинтов (если B) — отдельная стори после ADR.
- Вынос service_role — [SEC-04](STORY-IDS-SEC-04-service-role-isolation.md) / spa [SEC-01](../../../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-01-remove-service-role-from-frontend.md).

## Acceptance Criteria
- [ ] ADR написан (варианты A/B + угроза-модель + решение), парно с spa [SEC-02](../../../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-02-supabase-credential-boundary.md).
- [ ] Явно зафиксировано: anon-ключ публичен by-design (снять у оператора ощущение «дыра»).
- [ ] Если A — пометки в 04-security/07-env; если B — заведён backlog auth-proxy-контракта.

## Парадигма-якорь
[`04-security §A`](../../../runtime-docs/04-security.md), [`split-doc §4.4, §8, §10`](../../../../../spa-app/docs/analysis/identity-supabase-frontend-split-2026-06-16.md), [`ADR-IDS-002`](../../../requirements/05-adr-log.md) (почему identity = свой OAuth-сервер, не Supabase).
