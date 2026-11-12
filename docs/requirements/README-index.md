# Requirements Index — doge-identity-service

> Последовательно выполняемые requirements для `doge-identity-service`.
> Каждый файл — независимая задача с acceptance criteria.
> Статус: "Не реализовано" — нет кода. "In progress" — есть код без полного покрытия. "Реализовано" — пройдены acceptance criteria.

---

## Порядок реализации

| # | Файл | Назначение | Блок | Статус |
|---|------|-----------|------|--------|
| 01 | [01-service-mission.md](01-service-mission.md) | Миссия, KPI, CTO framing | Foundation | Не реализовано |
| 02 | [02-scope-and-boundaries.md](02-scope-and-boundaries.md) | Scope, границы, матрица интеграций | Foundation | Не реализовано |
| 03 | [03-architecture-formula.md](03-architecture-formula.md) | 4 слоя, компонентная схема, flow-диаграммы | Foundation | Не реализовано |
| 04 | [04-design-principles.md](04-design-principles.md) | 10 принципов: account-first, privacy-by-design, session-binding | Foundation | Не реализовано |
| 05 | [05-adr-log.md](05-adr-log.md) | ADR-001..005: ключевые архитектурные решения | Foundation | Не реализовано |
| 06 | [06-technical-scaffold.md](06-technical-scaffold.md) | **Runbook**: project layout, pyproject.toml, Makefile, config schema, bootstrap | Scaffold | Не реализовано |
| 07 | [07-env-configuration-spec.md](07-env-configuration-spec.md) | 23 env vars + example.env + генерация секретов | Scaffold | Не реализовано |
| 08 | [08-supabase-migrations.md](08-supabase-migrations.md) | 3 SQL миграции: profiles, eid_verification_sessions, eid_audit_events | Data | Не реализовано |
| 09 | [09-supabase-jwt-validation.md](09-supabase-jwt-validation.md) | Модуль валидации Supabase JWT, FastAPI Depends паттерн | Auth Core | Не реализовано |
| 10 | [10-me-endpoint.md](10-me-endpoint.md) | GET /me: профиль + permissions | Auth Core | Не реализовано |
| 11 | [11-eid-verification-flow.md](11-eid-verification-flow.md) | POST /auth/eid/start + GET /auth/eid/callback, session state machine | eID Flow | Не реализовано |
| 12 | [12-authentigate-oidc-client.md](12-authentigate-oidc-client.md) | OIDC client: PKCE S256, code exchange, ID token validation, mock OIDC | eID Flow | Не реализовано |
| 13 | [13-verified-person-hash-and-conflict.md](13-verified-person-hash-and-conflict.md) | HMAC_SHA256 hash, 3-кейсовый conflict detection, транзакция | eID Flow | Не реализовано |
| 14 | [14-oauth-server-custom-gpt.md](14-oauth-server-custom-gpt.md) | OAuth 2.0 AS: /oauth/authorize, /oauth/token, scope model | OAuth Server | Не реализовано |
| 15 | [15-story-authorization.md](15-story-authorization.md) | /story-drafts, /stories, /gpt/actions/submit-story, eID gate | Story Auth | Не реализовано |
| 16 | [16-security-privacy-observability.md](16-security-privacy-observability.md) | Rate limits, PII prohibitions, 17 audit events, CORS, readiness | Security | Не реализовано |
| 17 | [17-eid-provider-abstraction.md](17-eid-provider-abstraction.md) | **SOA**: EIDProviderPort, provider registry, session store redesign | eID Provider | Не реализовано |
| 18 | [18-eideasy-provider.md](18-eideasy-provider.md) | eID Easy OAuth2 provider: client, state store, env vars, tests | eID Provider | Не реализовано |
| 19 | [19-phone-verification-flow.md](19-phone-verification-flow.md) | POST /auth/phone/request + /auth/phone/confirm + Telnyx webhook: SMS-OTP, активный `phone_verified` гейт (пивот от eID) | Phone Flow | Реализовано (активный гейт верификации) |
| 20 | [20-semantic-schema-identity-boundary.md](20-semantic-schema-identity-boundary.md) | REQ3: identity не владеет semantic schemas; AC-011 / FLOW-002; без новых identity API | Cross-project | Accepted — boundary freeze 2026-09-01 |
| 21 | [21-verification-boolean-and-audit.md](21-verification-boolean-and-audit.md) | REQ7 shell: pack type + integration name; method-opaque **`identity_verified`** on `GET /me` (+ audit); legacy `phone_verified` may coexist; метрики → REQ8 | Cross-project | Реализовано (EPIC-IDS-15 VB-01…03) |
| 22 | [22-req9-make-env-load-parity.md](22-req9-make-env-load-parity.md) | REQ9: required `.env` shell source on `make serve`/`dev` (G8); keep `SERVICE_API_TOKEN` / probes | Cross-project | Draft — stories [req9-make-env-load-parity](../tasks/backlog-stories/req9-make-env-load-parity/INDEX.md) |

---

## Блоки и зависимости

```
Block 1: Foundation (01-05)
  └── Читать перед первым коммитом. Нет зависимостей от кода.

Block 2: Scaffold (06-07)
  └── Первый реальный код. Зависит от: ничего.
  └── Результат: `make dev` работает, /health отвечает.

Block 3: Data (08)
  └── Предусловие: Supabase проект есть, URL/ключи в .env.
  └── Результат: 3 таблицы + миграция провайдер-абстракции (файл 17).

Block 4: Auth Core (09-10)
  └── Предусловие: Block 2 + Block 3.
  └── Результат: /me работает с реальным Supabase JWT.

Block 5: eID Provider Layer (17 → 18)
  └── Предусловие: Block 2.
  └── 17: EIDProviderPort + registry + mock provider
  └── 18: EIDEasyProvider (OAuth2 flow)
  └── Результат: EID_PROVIDER=eideasy работает в test env.
       EID_PROVIDER=mock работает без credentials.

Block 6: eID Flow (11-13)
  └── Предусловие: Block 4 + Block 5.
  └── Файл 11 рефакторится: POST /auth/eid/start → тонкий orchestrator.
  └── Результат: полный eID flow через eideasy.

Block 7: OAuth Server (14)
  └── Предусловие: Block 4.
  └── Результат: ChatGPT может получить access_token.

Block 8: Story Auth (15)
  └── Предусловие: Block 4 + Block 6 + Block 7.
  └── Результат: верифицированный пользователь может подать story.

Block 9: Security (16)
  └── Применяется ко всем блокам. Частично реализуется параллельно.
```

---

## Открытые вопросы

- [ ] **ADR-IDS-005** (файл 05): psycopg vs supabase-py — решить перед реализацией файла 08.
- [ ] **eideasy credentials**: зарегистрировать на test.eideasy.com → получить EIDEASY_CLIENT_ID + EIDEASY_CLIENT_SECRET.
- [ ] **Authentigate**: Authentigate остаётся как второй провайдер в архитектуре (файл 17). Реализовать `authentigate/provider.py` при получении credentials от SK ID Solutions.
- [ ] **COMPLAINTS_GATEWAY_URL + SERVICE_API_TOKEN**: добавить в env spec (файл 07) когда определится деплой complaints-gateway.
- [x] **EID_HASH_SECRET vs DOGESTONIA_EID_SECRET_PEPPER**: закрыто в `ADR-IDS-008` (файл 05, пересмотр 2026-05-27). Единственное имя: `DOGESTONIA_EID_SECRET` → `AppConfig.eid_secret`. См. также файл 07.

---

## Версионирование

- Документы обновляются при изменении requirements (не при изменении кода).
- При реализации: обновить статус в этой таблице.
- При расхождении code vs requirements: requirements — истина, код нужно исправить (analysis.mdc principle).
