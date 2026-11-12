# Сквозной gap-анализ doge-identity-service (2026-06-04)

> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, severity, и классификацией «ожидаемо/косяк» по решениям оператора.
> **Призма:** story/issues/аналитика — домен **gateway**; identity = OAuth-сервер + eID-авторитет.
> **Решения оператора (2026-06-04)** зафиксированы в разделе 0 и вшиты в классификацию.
> **Не дублирует** (см. также): [epic-ids-05-scope-validation-2026-06-03.md](epic-ids-05-scope-validation-2026-06-03.md), [supabase-project-separation-audit-2026-06-03.md](supabase-project-separation-audit-2026-06-03.md), [epic-ids-06-audit-2026-06-02.md](epic-ids-06-audit-2026-06-02.md).

## 0. Решения оператора (интервью 2026-06-04)

| # | Вопрос | Решение |
|---|--------|---------|
| D1 | Направление подачи истории | **GPT → gateway напрямую**; gateway валидирует у identity (gateway→identity). identity истории НЕ форвардит. |
| D2 | story-роуты/`story_drafts` в identity | story-форвард-роуты — **misplaced (на вынос)**; `story_drafts` (контент) — **убрать**; identity остаётся eID/OAuth-авторитетом. |
| D3 | Модель auth | **сервисный токен (доверие сервисов) + introspection пользовательского токена** (gateway спрашивает identity). eID-статус **не в токене**. |
| D4 | Заготовки без кода | **разобрать по одному** (раздел 10). |
| D5 | bootstrap | `story_drafts` исключён ([`supabase/bootstrap/000_full_init.sql`](../../supabase/bootstrap/000_full_init.sql)). |

## 1. Границы scope (story/issues)

| ID | Severity | Факт | Файл:строка | Класс |
|----|----------|------|-------------|-------|
| SB-1 | **HIGH** | `story_drafts` в `_REQUIRED_TABLES` healthcheck → при bootstrap без неё `/ready`=503 | [`db_supabase.py:315-320`](../../src/core/infrastructure/db_supabase.py) | косяк (D2): убрать из required |
| SB-2 | MEDIUM | story-форвард-роуты живут в identity (наследие req-15) | [`asgi_app.py:258-310`](../../src/core/api/asgi_app.py) | misplaced (D1/D2): на вынос |
| SB-3 | MEDIUM | `story_drafts` таблица + `StoryDraftRepository`/`SupabaseStoryDraftRepository` + `StoryDraft` модель хранят контент истории — ↔ [req-02:59](../requirements/02-scope-and-boundaries.md) «identity не хранит stories» | [миграция](../../supabase/migrations/20260527000001_create_story_drafts.sql), [`models.py:95-103`](../../src/core/domain/models.py), [`db_supabase.py:616-648`](../../src/core/infrastructure/db_supabase.py) | косяк (D2): убрать |

> Детальная история по story_drafts (optional-vs-required противоречие эпика, schema drift) — в [epic-ids-05-scope-validation-2026-06-03.md](epic-ids-05-scope-validation-2026-06-03.md). Здесь — итог под решение D2.

## 2. API

| ID | Severity | Факт | Файл:строка | Класс |
|----|----------|------|-------------|-------|
| API-1 | MEDIUM | Нет `/oauth/introspect` (или рабочего `/me`) для introspection-модели D3 — gateway нечем спросить «active/sub/eid_verified» | [`asgi_app.py`](../../src/core/api/asgi_app.py) (нет роута); `/me` 🟡 501 [`handlers.py:40-51`](../../src/core/api/handlers.py) | косяк (D3): нужен endpoint (будущий эпик) |
| API-2 | LOW | 12 из 14 роутов — заглушки 501 (`/me`, `/auth/eid/*`, `/oauth/*`, story-*) | [`handlers.py:29-97`](../../src/core/api/handlers.py) | ожидаемо: будущие эпики (кроме SB-2) |
| API-3 | LOW | Опубликованного API-контракта (OpenAPI-файла) нет; только рантайм `/docs` | — | ожидаемо; покрыто [runtime-docs/01-api](../runtime-docs/01-api.md) |

## 3. Конфигурация

| ID | Severity | Факт | Файл:строка | Класс |
|----|----------|------|-------------|-------|
| CFG-1 | MEDIUM | В identity-конфиге нет `SERVICE_API_TOKEN` — нечем валидировать входящий сервисный токен (слой доверия D3) | [`config/schema.py`](../../src/core/config/schema.py) | косяк (D3): добавить (будущий эпик) |
| CFG-2 | — (НЕ gap) | Нет `COMPLAINTS_GATEWAY_URL`/`SERVICE_API_TOKEN`-для-форварда | [`schema.py`](../../src/core/config/schema.py) | **корректно** по D1: identity не форвардит. (Ранее считалось gap — снято решением.) |
| CFG-3 | LOW | `.env.example` `AUTHENTIGATE_REDIRECT_URI=http://localhost:8100/auth/eid/callback` — такого роута нет (есть `/auth/authentigate/callback`) | [`.env.example:51`](../../.env.example) vs [`asgi_app.py:195`](../../src/core/api/asgi_app.py) | косяк: drift, поправить URL |

## 4. Модель данных

| ID | Severity | Факт | Класс |
|----|----------|------|-------|
| DM-1 | HIGH | = SB-1/SB-3 (`story_drafts`) | косяк (D2): убрать |
| DM-2 | — | wallet-колонки `profiles.wallet_*` без кода | заготовка → раздел 10 |
| DM-3 | LOW | `eid_verification_sessions.provider` DEFAULT `'eideasy'` ([миграция](../../supabase/migrations/20260526000001_eid_sessions_provider_abstraction.sql)), но активный провайдер в коде — только `mock` | косяк-мелочь: дефолт не совпадает с реальностью |

## 5. Security

| ID | Severity | Факт | Файл:строка | Класс |
|----|----------|------|-------------|-------|
| SEC-1 | MEDIUM | `InMemoryOAuthTokenService.issue_access_token` намеренно НЕ проверяет `client_secret` | [`repositories.py:274-275`](../../src/core/infrastructure/repositories.py) | косяк для прод-impl: enforce в Supabase-варианте |
| SEC-2 | LOW | OAuth-токен HS256 (симметричный `OAUTH_ACCESS_TOKEN_SECRET`) | [`repositories.py:316-329`](../../src/core/infrastructure/repositories.py) | ожидаемо при D3: gateway валидирует через introspection, не подпись. (Если перейдут на локальную валидацию — понадобится RS256.) |
| SEC-3 | LOW | `StubBearerTokenAuth` присутствует, в проде не используется | [`security.py:22-31`](../../src/core/api/security.py) | заготовка/legacy → раздел 10 |
| SEC-4 | LOW | `CODE_VERIFIER_ENCRYPTION_KEY` (AES-256) в конфиге, но шифрование code_verifier в коде не используется | [`schema.py:149`](../../src/core/config/schema.py) | заготовка → раздел 10 |

## 6. eID-модульность

| ID | Severity | Факт | Файл:строка | Класс |
|----|----------|------|-------------|-------|
| EID-1 | MEDIUM | Registry содержит только `mock`; при `EID_PROVIDER=eideasy`/`authentigate` → `get_active()` бросит `KeyError` | [`providers.py:99`](../../src/core/infrastructure/providers.py), [`registry.py:11-14`](../../src/core/providers/registry.py) | латентный баг: либо guard, либо провайдеры (будущий эпик) |
| EID-2 | LOW | Конфиг `eideasy_*`/`authentigate_*` есть, кода провайдеров нет | [`schema.py`](../../src/core/config/schema.py) | заготовка → раздел 10 |

> Архитектура eID-порта/registry/mock — корректна и модульна (см. [runtime-docs/06](../runtime-docs/06-eid-providers.md)). Gap — только в наборе провайдеров.

## 7. Тесты

| ID | Severity | Факт | Класс |
|----|----------|------|-------|
| TEST-1 | LOW | story-роуты покрыты только как 501 (`test_http_transport_smoke`/asgi) — нет контракта реальной логики (её и нет) | ожидаемо |
| TEST-2 | LOW | Нет тестов на не-mock провайдеры (eideasy/authentigate) и на `EID-1` KeyError | ожидаемо/риск |
| TEST-3 | LOW | Нет теста на introspection-контракт (D3) — endpoint отсутствует | следствие API-1 |

## 8. Doc-drift

| ID | Severity | Факт | Класс |
|----|----------|------|-------|
| DOC-1 | MEDIUM | [req-15](../requirements/15-story-authorization.md) описывает форвард identity→gateway — **отменено** D1/D2 | косяк: req-15 устарел |
| DOC-2 | MEDIUM | Противоречие [req-02:52,60](../requirements/02-scope-and-boundaries.md) ↔ [req-03:113](../requirements/03-architecture-formula.md)/req-15 о направлении | разрешено D1 (gateway→identity + GPT→gateway direct) |
| DOC-3 | LOW | [req-08](../requirements/08-supabase-migrations.md) и [req-02:20](../requirements/02-scope-and-boundaries.md) говорят «3 миграции», фактически 5 | косяк: обновить |
| DOC-4 | LOW | [req-15](../requirements/15-story-authorization.md) §story_drafts-table схема ≠ отгруженной | косяк (но таблица идёт на вынос — D2) |

## 9. Сводка по severity

- **HIGH (1):** SB-1/DM-1 — `story_drafts` в required healthcheck ломает `/ready` (центральный, действие оператора уже его триггерит).
- **MEDIUM (8):** SB-2, SB-3, API-1, CFG-1, SEC-1, EID-1, DOC-1, DOC-2.
- **LOW (11):** API-2/3, CFG-3, DM-3, SEC-2/3/4, EID-2, TEST-1/2/3, DOC-3/4.
- **Снято решением:** CFG-2 (форвард-конфиг не нужен).

## 10. Реестр заготовок «без кода» (D4 — разобрать по одному)

Каждую строку оператор помечает «ожидаемо (оставить)» или «убрать/отложить». Сейчас все — ⚪ заготовка, статус решения: **ожидает**.

| # | Заготовка | Где | Риск, если оставить молча | Решение |
|---|-----------|-----|---------------------------|---------|
| P1 | wallet-колонки `profiles.wallet_*` | [миграция:22-27](../../supabase/migrations/20260525000001_create_profiles.sql), [`models.py:34-38`](../../src/core/domain/models.py) | «мёртвые» поля до web3-эпика; создают иллюзию готовности | ⬜ ожидает |
| P2 | `ALLOWED_RETURN_URLS` — читается, нигде не валидируется | [`schema.py:169`](../../src/core/config/schema.py) | open-redirect-риск, если позже забудут провалидировать | ⬜ ожидает |
| P3 | `StubBearerTokenAuth` (не используется) | [`security.py:22-31`](../../src/core/api/security.py) | legacy-путь auth | ⬜ ожидает |
| P4 | `eideasy_*` / `authentigate_*` конфиг без кода провайдеров | [`schema.py`](../../src/core/config/schema.py) | EID-1 (KeyError при переключении) | ⬜ ожидает |
| P5 | `CODE_VERIFIER_ENCRYPTION_KEY` (AES) не используется | [`schema.py:149`](../../src/core/config/schema.py) | секрет требуется в pilot, но не применяется | ⬜ ожидает |
| P6 | `idempotency-key` резолвер без потребителей | [`idempotency.py`](../../src/core/api/idempotency.py) | заготовка под бизнес-роуты | ⬜ ожидает |

## 11. Что НЕ является gap (подтверждённо корректно)

- Слоёная/SOA-архитектура, DI-singleton, фабрика, eID-порт/registry — реализованы чисто.
- Supabase JWT-валидация, RLS, HMAC-хэш — на месте.
- `/health`, `/ready`, 5-уровневый healthcheck — работают (кроме эффекта SB-1).
- Отдельный Supabase-проект для identity — обоснован ([separation-audit](supabase-project-separation-audit-2026-06-03.md)).
- Отсутствие форвард-конфига в identity — корректно по D1.

## Quality gate (analysis.mdc)
- [x] Все findings с `file:line` и severity.
- [x] Покрыты 9 разделов плана + тесты + конфиги + реестр заготовок.
- [x] Классификация «ожидаемо/косяк» — по зафиксированным решениям оператора (раздел 0), не по догадке.
- [x] Реализация не навязана (объём = доки); только findings + класс.
- [x] Не дублирует прежние отчёты — кросс-ссылки.
