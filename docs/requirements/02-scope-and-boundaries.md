# 02. Scope и границы сервиса

> **Статус:** НЕ реализовано. Requirements document.
> **Сервис:** `doge-identity-service`

---

## Что входит в scope (MVP)

| Область | Описание |
|---------|---------|
| **Supabase Auth integration** | Login/signup через email+password и magic link; валидация Supabase JWT в каждом защищённом запросе |
| **eID verification flow** | POST /auth/eid/start → Authentigate OIDC → GET /auth/authentigate/callback → привязка к профилю |
| **verified_person_hash** | Генерация HMAC_SHA256, хранение в profiles, conflict detection |
| **User profile** | public.profiles: eid_verified status, wallet placeholder, display_name |
| **GET /me endpoint** | Отдаёт профиль и permissions для текущего залогиненного пользователя |
| **OAuth 2.0 Authorization Server** | GET /oauth/authorize + POST /oauth/token для Custom GPT (ChatGPT) |
| **Supabase migrations** | 4 operational migrations: 3 base tables (profiles, eid_verification_sessions, eid_audit_events) + provider abstraction alter |
| **Audit logging** | Запись событий eID flow без PII |
| **Health + Readiness endpoints** | /health, /ready |

---

## Что НЕ входит в scope (MVP)

| Область | Причина |
|---------|---------|
| Social login (Google, GitHub) | Post-MVP, включается в Supabase настройках без изменения кода сервиса |
| Wallet address linking | Post-MVP, data model уже содержит поля |
| Story signing via wallet | Post-MVP |
| Periodic eID re-verification | Post-MVP, только при policy-enabled |
| Auto-merge дублирующих аккаунтов | Явно запрещён в MVP |
| Admin panel / backoffice | Отдельная задача |
| Passkeys / WebAuthn | Post-MVP |
| Multi-tenancy | DOGEstonia — одна нода |
| Rate limiting per-IP (global) | Post-MVP; MVP — только per-user rate limits на eid/start |
| Email notifications | Не входит в identity-service |
| Story intake / drafts / submit | Домен doge-complaints-gateway; GPT шлёт истории напрямую в gateway ([09-gateway-expectations](../runtime-docs/09-gateway-expectations.md)) |

---

## Матрица интеграций

| Внешняя система | Направление | Протокол | Что делает identity-service |
|----------------|-------------|----------|----------------------------|
| **Supabase Auth** | outbound | HTTPS/JWT | Валидирует JWT пользователей; не управляет пользователями напрямую |
| **Supabase Postgres** | outbound | HTTPS (PostgREST) или TCP (psycopg) | Читает/пишет profiles, eid_verification_sessions, eid_audit_events |
| **Authentigate** | outbound | OIDC over HTTPS | OIDC Authorization Code Flow + PKCE для eID верификации |
| **spa-app (React)** | inbound | HTTPS | Получает redirect URLs, делает запросы к /me, /auth/eid/start, /oauth/authorize |
| **Custom GPT (ChatGPT)** | inbound | OAuth 2.0 + HTTPS | OAuth Authorization Code Flow; Bearer token в каждом API-запросе |
| **doge-complaints-gateway** | ← calls identity-service | HTTPS | Валидирует Bearer token от identity-service перед приёмом stories |
| **Mock OIDC** (dev only) | outbound | OIDC over HTTP | Заменяет Authentigate до получения credentials |

---

## Чего identity-service НЕ делает

- Не хранит stories, issues, кластеры.
- Не вызывает doge-complaints-gateway напрямую (только complaints-gateway вызывает identity-service для валидации).
- Не экспонирует Authentigate наружу (ни Custom GPT, ни spa-app не видят Authentigate endpoint).
- Не хранит personal_code, legal_name, birthdate, document_number, raw_id_token, raw_access_token.
- Не записывает personal data on-chain.
- Не является первичным OAuth провайдером для пользователей (пользователи логинятся через Supabase, не через OAuth 2.0 server identity-service напрямую — OAuth server только для Custom GPT).

---

## Границы ответственности по таблицам Supabase

| Таблица | Владелец | Кто пишет | Кто читает |
|---------|---------|-----------|-----------|
| `auth.users` | Supabase Auth (managed) | Supabase Auth только | identity-service читает через JWT claims |
| `public.profiles` | identity-service | identity-service | identity-service, /me endpoint |
| `public.eid_verification_sessions` | identity-service | identity-service | identity-service (callback handler) |
| `public.eid_audit_events` | identity-service | identity-service | Admin/analytics только |

---

## Порты и URL

| Среда | URL сервиса | Порт |
|-------|------------|------|
| Local dev | `http://localhost:8100` | 8100 |
| Production | `https://identity.dogestonia.ee` | 443 (через reverse proxy) |

Порт 8100 выбран чтобы не конфликтовать с doge-complaints-gateway (по умолчанию 8000).
