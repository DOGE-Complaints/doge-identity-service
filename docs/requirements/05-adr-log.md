# 05. ADR Log — Architectural Decision Records

> **Статус:** Зафиксировано. Решения приняты на kick-off CTO-CPO 2026-05-25.
> **Сервис:** `doge-identity-service`

---

## ADR-IDS-001: doge-identity-service как отдельный сервис

**Статус:** Принято (2026-05-25)

**Контекст:**
Изначальная документация (docs/Identity.md) не специфицировала, будет ли identity-layer добавлен в `doge-complaints-gateway` или выделен отдельно.

**Решение:**
`doge-identity-service` — отдельный репозиторий и отдельный деплой.

**Обоснование:**
- Complaints-gateway = pipeline данных (stories → issues → clusters). Identity = trust layer. Смешение нарушает single-responsibility.
- Identity-service будет иметь свои таблицы в Supabase, свои secrets, свои endpoint patterns.
- Независимый деплой: identity можно обновлять без риска для story pipeline.
- OAuth 2.0 server требует собственных client-registered endpoints, несовместимых с gateway-логикой.

**Последствия:**
- doge-complaints-gateway валидирует Bearer token полученный от identity-service.
- Два сервиса на отдельных портах/доменах.
- Каждый сервис имеет свой .env и свой pyproject.toml.

---

## ADR-IDS-002: OAuth 2.0 Authorization Code Flow для Custom GPT

**Статус:** Принято (2026-05-25)

**Контекст:**
Custom GPT (ChatGPT) должен вызывать DOGEstonia API от имени пользователя. Возможные подходы:
1. API key (service token) — не привязан к пользователю
2. Supabase OAuth — Supabase OAuth 2.1 Server
3. Custom OAuth 2.0 server в identity-service

**Решение:**
doge-identity-service реализует собственный OAuth 2.0 Authorization Server: endpoints `/oauth/authorize` + `/oauth/token`.

**Обоснование:**
- OpenAI Custom GPT Actions поддерживает OAuth 2.0 Authorization Code Flow как стандарт.
- Supabase OAuth 2.1 Server — не используется: добавляет зависимость от Supabase-managed OAuth, меньше контроля над token claims и scope model.
- Custom server даёт полный контроль: scope, TTL, revocation, custom claims (eid_verified status).
- Authentigate НИКОГДА не экспонируется GPT: identity-service полностью инкапсулирует eID layer.

**Последствия:**
- Identity-service должен хранить OAuth clients (минимум: ChatGPT client_id + client_secret + redirect_uri).
- Access token выдаётся identity-service, не Supabase.
- doge-complaints-gateway валидирует этот же token.

---

## ADR-IDS-003: One-Time eID verification (не per-action)

**Статус:** Принято (2026-05-25)

**Контекст:**
Два варианта: требовать eID при каждой подаче story ИЛИ однократная привязка.

**Решение:**
eID верификация — однократная. После успешной привязки `profiles.eid_verified = true` и этот статус используется для всех последующих privileged actions.

**Обоснование:**
- UX: требовать eID каждый раз при подаче story — неприемлемо для пользователей.
- Безопасность: duplicate detection работает через `verified_person_hash` (уникальный per-person), а не per-story.
- Отзыв верификации остаётся возможным через admin action или security incident.

**Последствия:**
- Каждый privileged endpoint проверяет `profiles.eid_verified`, не запускает новый OIDC flow.
- Суть проверки: `SELECT eid_verified FROM profiles WHERE supabase_user_id = $1`.
- Periodic re-verification — post-MVP, policy-controlled.

---

## ADR-IDS-004: Mock OIDC сервер для разработки до получения Authentigate credentials

**Статус:** Принято (2026-05-25)

**Контекст:**
Authentigate credentials (client_id, client_secret) от SK ID Solutions не получены. Разработка eID flow не может начаться без credentials или mock.

**Решение:**
Разработка идёт с mock OIDC сервером, совместимым с Authorization Code Flow + PKCE S256.
Рекомендованный вариант: `ghcr.io/navikt/mock-oauth2-server`.

```bash
docker run -p 8080:8080 ghcr.io/navikt/mock-oauth2-server:latest
```

Mock настраивается через env: `AUTHENTIGATE_ISSUER=http://localhost:8080`.
Единственное изменение при переходе на реальный Authentigate — env vars (`AUTHENTIGATE_ISSUER`, `AUTHENTIGATE_CLIENT_ID`, `AUTHENTIGATE_CLIENT_SECRET`). Код не меняется.

**Обоснование:**
- Позволяет строить и тестировать полный eID flow без зависимости от SK ID Solutions.
- OIDC-совместимый mock воспроизводит реальный discovery endpoint, authorize, token endpoints.
- mock-oauth2-server от NaviKT — production-tested в Norwegian government projects.

**Последствия:**
- В CI/CD: mock OIDC запускается как service container.
- В production: `AUTHENTIGATE_ISSUER=https://id.authentigate.eu` — реальный Authentigate.
- CPO должен получить credentials от SK ID Solutions до production deploy.

---

## ADR-IDS-005: Supabase PostgREST vs psycopg для DB-доступа

**Статус:** Открытый вопрос (решить при старте реализации 06)

**Контекст:**
doge-complaints-gateway использует оба подхода:
- psycopg (TCP) для прямых SQL-запросов (migrations, complex queries)
- Supabase HTTP API (PostgREST) для стандартных CRUD

**Варианты для identity-service:**
1. psycopg — прямой SQL, максимальный контроль, транзакции, сложные запросы
2. supabase-py — Python client для Supabase API, проще для стандартных запросов
3. Оба — psycopg для транзакционных операций (eID conflict detection), supabase-py для auth operations

**Рекомендация:**
psycopg для всего DB-доступа в identity-service.
Обоснование: транзакционная целостность eID conflict detection (FR-BE-009) требует SQL transactions. PostgREST не поддерживает multi-statement transactions. Единый подход = меньше путаницы.

**Статус:** Требует финального решения CTO до начала реализации файла 08 (migrations).

---

## ADR-IDS-006: eID провайдер — eID Easy вместо Authentigate

**Статус:** Принято (2026-05-26)

**Контекст:**
Authentigate (SK ID Solutions) требует формальной регистрации и credentials, которые не были получены. eID Easy предоставляет тестовый доступ немедленно, аналогичный набор методов (Smart-ID, Mobile-ID, ID-card) и явную поддержку OAuth2 flow (не beta).

**Решение:**
Активный eID провайдер для MVP — **eID Easy** (`EID_PROVIDER=eideasy`). Authentigate остаётся в архитектуре как второй провайдер (файл 17), реализуется при получении credentials.

**Сравнение протоколов:**

| | Authentigate | eID Easy |
|---|---|---|
| Протокол | OIDC + PKCE S256 | OAuth2 Authorization Code |
| ID token | Да (JWT, RS256) | Нет |
| PKCE | S256, обязательно | Не требуется |
| CSRF | state + nonce | state |
| JWKS/Discovery | Да | Нет |
| Test env | Mock OIDC docker | test.eideasy.com (реальный) |
| Credentials | Требует регистрации (SK ID Solutions) | Регистрация через портал |

**Решение по session schema:** PKCE поля (`code_verifier_encrypted`, `nonce`) остаются в `eid_verification_sessions` как nullable (для будущего Authentigate). Provider-специфичные данные → `provider_session_data JSONB`.

**Последствия:**
- Файл 12 (Authentigate OIDC client) — spec остаётся, реализация откладывается.
- Файл 17 (provider abstraction) — новый, SOA слой для переключения провайдеров.
- Файл 18 (eideasy provider) — новый, активный провайдер.
- Env var `EID_PROVIDER` контролирует выбор провайдера.

---

## ADR-IDS-007: Plugin архитектура для eID провайдеров

**Статус:** Принято (2026-05-26)

**Контекст:**
При жёсткой привязке к одному провайдеру смена провайдера требует переписывания flow endpoints и DB схемы. Разные провайдеры используют разные протоколы (OIDC vs OAuth2), разные session артефакты (PKCE vs state-only), разные callback URLs.

**Решение:**
`EIDProviderPort` Protocol (файл 17) — все провайдеры реализуют два метода: `start_flow()` и `handle_callback()`. Публичные HTTP endpoints (`POST /auth/eid/start`, callback routes) не знают про детали протокола. Бизнес-логика (conflict detection, mark verified) — в orchestrator, не в провайдере.

**Структура:**
```
src/core/providers/
├── base.py          ← EIDProviderPort Protocol
├── registry.py      ← get_active_provider() по EID_PROVIDER
├── mock/            ← dev без credentials
├── eideasy/         ← активный MVP провайдер
└── authentigate/    ← будущее
```

**Последствия:**
- Переключение провайдера = изменить EID_PROVIDER в .env, перезапустить сервис.
- Новый провайдер = создать `providers/{name}/provider.py`, добавить case в registry.
- Session store: `provider_session_data JSONB` хранит provider-специфичные данные.

---

## ADR-IDS-008: Унификация HMAC-секрета — `EID_HASH_SECRET` с fallback на `DOGESTONIA_EID_SECRET_PEPPER`

**Статус:** Принято (2026-05-26)

**Контекст:**
В документации сложилось два имени одной и той же сущности — HMAC-SHA256 secret для генерации `verified_person_hash` / `subject_hash`:

- Файл 07 (env-configuration) определяет `DOGESTONIA_EID_SECRET_PEPPER` (исторически из ранней спеки identity-сервиса).
- Файл 17 (eID provider abstraction) и файл 18 (eideasy provider) переименовали в `EID_HASH_SECRET` как provider-agnostic имя.
- `README-index` фиксировал это как открытый вопрос: "при реализации унифицировать в одну переменную `EID_HASH_SECRET`".

В аудитном отчёте `docs/analysis/epic-validation-report-2026-05-26.md` §M-1 показано, что без явного решения `AppConfig` будет содержать оба поля и реализующий агент может взять одно из них — что приведёт к непредсказуемому поведению при стандартном `.env`, где задана только одна переменная.

**Решение:**
В `AppConfig` существует **одно** поле — `eid_hash_secret: str`. Loader (`load_config_from_env`) читает значение по следующему приоритету:

1. `EID_HASH_SECRET` — основной env var (соответствует req-17, req-18, req-13 обновлённой версии).
2. Если `EID_HASH_SECRET` пустой/отсутствует — fallback на `DOGESTONIA_EID_SECRET_PEPPER` (для совместимости с существующими `.env` файлами).
3. Если оба пустые — в `pilot` профиле `ConfigError`, в `demo` — пустая строка (с warning при production-like запуске).

`req-07` помечает `DOGESTONIA_EID_SECRET_PEPPER` как **deprecated/fallback**; `EID_HASH_SECRET` становится primary.

**Обоснование:**
- Один env var = один потребитель в коде. Никаких `or` цепочек в бизнес-логике.
- Provider-agnostic имя `EID_HASH_SECRET` корректнее семантически (один HMAC ключ для всех eID провайдеров — req-17 §"Важно").
- Fallback на старое имя избегает breaking change для существующих deployments — миграция = добавить `EID_HASH_SECRET` в `.env`, удалить старое имя позже.

**Последствия:**
- `EPIC-IDS-01` Story 2 — единое поле `eid_hash_secret` с двойным чтением env.
- `EPIC-IDS-06` conftest продолжает сетать оба var, чтобы валидировать обе ветки loader'а.
- `req-07` обновлён: `EID_HASH_SECRET` — primary, `DOGESTONIA_EID_SECRET_PEPPER` — deprecated.
- `README-index` §"Открытые вопросы" — пункт закрыт ссылкой на этот ADR.
- При переходе на pilot в production: рекомендуется задать только `EID_HASH_SECRET`. После того как все деплои мигрированы — `DOGESTONIA_EID_SECRET_PEPPER` можно удалить из спеки (отдельная задача, не входит в этот ADR).

---

### Пересмотр (2026-05-27) — интервью CPO×CTO

**Статус:** Принято (пересмотрено). Решение от 2026-05-26 (dual-name + fallback) **отменено**.

**Контекст пересмотра:**
После audit-fixes осталась двусмысленность: два env-имени (`EID_HASH_SECRET`, `DOGESTONIA_EID_SECRET_PEPPER`), fallback-цепочка в loader'е, pilot-таблица и conftest с двумя переменными. CPO зафиксировал: одно имя, без fallback, без «или» в валидации.

**Новое решение:**
- Единственная env-переменная: **`DOGESTONIA_EID_SECRET`** (без суффикса `_PEPPER`).
- Единственное поле в `AppConfig`: **`eid_secret: str`**, читается только из `DOGESTONIA_EID_SECRET`.
- **Нет** fallback на `EID_HASH_SECRET` или `DOGESTONIA_EID_SECRET_PEPPER`.
- В `pilot`: пустой `DOGESTONIA_EID_SECRET` → `ConfigError` (явный AC в EPIC-IDS-01 Story 2).

**Обоснование:**
- Один источник истины — агент не выберет «не то» имя при реализации.
- Проще conftest и CI (одна строка в `_block_dotenv_leakage`).
- Семантика «секрет DOGEstonia для eID-хеширования» сохраняется в имени `DOGESTONIA_EID_SECRET`.

**Последствия (документация):**
- `req-07`, `req-13`, `req-17`, `req-18` — только `DOGESTONIA_EID_SECRET` / `config.eid_secret`.
- `EPIC-IDS-01` Story 2, `EPIC-IDS-06` Story 1 — без dual env.
- `README-index` — закрытый вопрос ссылается на этот пересмотр.

Источник: [`docs/analysis/interview-cpo-cto-epics-2026-05-27.md`](../analysis/interview-cpo-cto-epics-2026-05-27.md).
