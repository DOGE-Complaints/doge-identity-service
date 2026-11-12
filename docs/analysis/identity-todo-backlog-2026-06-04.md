# Сборный список доработок identity (черновик, 2026-06-04)

> **Что это.** Один документ, куда вынесено всё недоделанное (заглушки), все расхождения с согласованной парадигмой и всё лишнее (истории / ложные связи с gateway), извлечённое **проходом по каждому** файлу в [`docs/runtime-docs/`](../runtime-docs/). По сути — сырой бэклог задач.
> **Статус.** ⏳ Структура **черновая, ждёт указаний владельца** — пока ничего не приоритизируется, не группируется в эпики и не исправляется. Только сбор.
> **Связь.** Каждый пункт привязан к коду и к строке runtime-дока; технические детали и severity уже есть в [`gap-analysis-full-2026-06-04.md`](gap-analysis-full-2026-06-04.md) (не дублирую — ссылаюсь).
> **Парадигма (контекст).** identity **не создаёт истории** и **не обращается к gateway**; наоборот — gateway вызывает identity (introspection), чтобы проверить пользователя и eID. Всё, что противоречит этому, ниже помечено как «лишнее».

Типы: **STUB** (заглушка 501) · **MISSING** (нужно по парадигме, в коде нет) · **PARADIGM** (расходится с целевой моделью) · **EXCESS** (лишнее: истории/ложные связи) · **PLACEHOLDER** (заготовка без кода) · **BUG** (латентный дефект) · **DOC** (рассинхрон документации).

---

## Часть 1. Проход по каждому документу

### 01-api.md
- **STUB** `/me` — 501 ([`asgi_app.py:159-169`](../../src/core/api/asgi_app.py)).
- **STUB** `/auth/eid/start` — 501 ([`asgi_app.py:171-181`](../../src/core/api/asgi_app.py)).
- **STUB** `/auth/eideasy/callback`, `/auth/authentigate/callback`, `/auth/mock/callback` — 501 ([`asgi_app.py:183-217`](../../src/core/api/asgi_app.py)).
- **STUB** `/oauth/authorize`, `/oauth/authorize/complete`, `/oauth/token` — 501 ([`asgi_app.py:219-256`](../../src/core/api/asgi_app.py)).
- **MISSING** нет `/oauth/introspect` (или рабочего `/me`) для проверки токена gateway'ем (01-api:36).
- **EXCESS** story-роуты `/story-drafts`, `/story-drafts/{id}/submit`, `/stories`, `/gpt/actions/submit-story` — на вынос ([`asgi_app.py:258-310`](../../src/core/api/asgi_app.py), 01-api:38-40).
- **PLACEHOLDER** `idempotency-key`-резолвер без потребителей ([`idempotency.py`](../../src/core/api/idempotency.py), 01-api:50).

### 02-data-bootstrap.md
- **EXCESS/BUG (HIGH-эффект)** `story_drafts` в списке обязательных таблиц healthcheck → на корректно поднятой по bootstrap базе `/ready`=503 ([`db_supabase.py:315-320`](../../src/core/infrastructure/db_supabase.py), 02:49).
- **DOC** req-08 описывает 3 миграции, фактически 4 (02:33).

### 03-soa-roles.md
- **PLACEHOLDER** пустые пакеты (только `__init__.py`): `core.audit`, `core.oauth`, `core.profiles` (03:64).
- **EXCESS** пустой пакет `core.stories` — наследие story-темы, кандидат на удаление (03:64).

### 04-security.md (особое внимание — расхождения с парадигмой)
- **STUB** OAuth-маршруты `/oauth/authorize`, `/oauth/token` — 501 (04:84).
- **STUB** eID-старт и callback'и — 501 (04:85).
- **MISSING** **introspection-endpoint** для gateway — отсутствует совсем; ключевая дыра целевой модели (04:88).
- **MISSING** проверка **сервисного токена** на входе identity — нет `SERVICE_API_TOKEN` в конфиге (04:89).
- **PARADIGM** OAuth-движок есть, но наружу не подключён (логика в [`repositories.py:238-346`](../../src/core/infrastructure/repositories.py), роуты 501) (04:91,107).
- **BUG/PARADIGM** `InMemoryOAuthTokenService` не проверяет `client_secret` — должна прод-реализация ([`repositories.py:274-275`](../../src/core/infrastructure/repositories.py), 04:107).
- **PARADIGM** флаг «нужен eID» — поля `return_context`/`requested_action` есть, но роут старта 501 ([`models.py:43-59`](../../src/core/domain/models.py), 04:87).
- **PLACEHOLDER** `StubBearerTokenAuth` не используется ([`security.py:22-31`](../../src/core/api/security.py), 04:103).
- **PLACEHOLDER** `CODE_VERIFIER_ENCRYPTION_KEY` (AES) заявлен, шифрование verifier в коде не используется ([`schema.py:149`](../../src/core/config/schema.py), 04:123).

### 05-data-model.md
- **EXCESS** таблица `story_drafts` + модель `StoryDraft` + репозитории (in_memory + supabase) — контент историй, на удаление ([миграция `20260527`](../../supabase/migrations/20260527000001_create_story_drafts.sql), [`models.py:95-103`](../../src/core/domain/models.py), [`db_supabase.py:616-648`](../../src/core/infrastructure/db_supabase.py), 05:56-58).

### 06-eid-providers.md
- **PLACEHOLDER** провайдеры `eideasy`, `authentigate` — конфиг есть, кода нет (06:28-29).
- **BUG** при `EID_PROVIDER=eideasy/authentigate` → `get_active()` бросит `KeyError` (валидатор пропускает, реестр содержит только `mock`) ([`schema.py:97-99`](../../src/core/config/schema.py), [`providers.py:99`](../../src/core/infrastructure/providers.py), [`registry.py:11-14`](../../src/core/providers/registry.py), 06:31).
- **STUB** эндпоинты eID-флоу (`/auth/eid/start`, callback'и) — 501 (06:44,48).

### 07-web3-foundation.md
- **PLACEHOLDER** wallet-колонки `profiles.wallet_*` — поля есть, логики (подпись/сеть/SIWE) нет ([миграция:22-27](../../supabase/migrations/20260525000001_create_profiles.sql), [`models.py:34-38`](../../src/core/domain/models.py), 07:7,33).

### 08-ui-expectations.md
- **PLACEHOLDER/BUG-риск** `ALLOWED_RETURN_URLS` читается, но нигде не валидируется (риск open-redirect) ([`schema.py:169`](../../src/core/config/schema.py), 08:18,30).
- **MISSING (на стороне UI)** экран входа/верификации — URL в коде identity не зашит (08:21,31) — зона UI, отмечено для полноты.

### 09-gateway-expectations.md
- **MISSING** introspection-endpoint / рабочий `/me`, отдающий `active/sub/eid_verified` (09:30).
- **STUB** выдача OAuth-токена наружу — роуты `/oauth/*` 501 (09:31).
- **MISSING** проверка сервисного токена на входе identity — нет `SERVICE_API_TOKEN` (09:32).
- **EXCESS/PARADIGM** story-форвард-роуты в identity — наследие отменённого req-15 (форвард identity→gateway) (09:37,45).
- **EXCESS** хранение контента историй (`story_drafts`) — на удаление (09:38).
- **DOC** req-15 — устаревшая модель (форвард из identity), отменена решением 2026-06-04 (09:37).

---

## Часть 2. Сводный уникальный список (дедупликация)

### A. STUB — реализовать эндпоинты (каркас есть, отвечает 501)
1. `GET /me` — профиль + права; он же кандидат на роль introspection-ответа для gateway.
2. `POST /auth/eid/start` — старт eID-проверки.
3. `GET /auth/eideasy/callback`, `GET /auth/authentigate/callback`, `GET /auth/mock/callback` — возвраты от провайдеров.
4. `GET /oauth/authorize`, `POST /oauth/authorize/complete`, `POST /oauth/token` — OAuth-сервер для GPT.

### B. MISSING — нет в коде, нужно по согласованной парадигме
5. `/oauth/introspect` (или рабочий `/me`), отдающий `{active, sub, eid_verified}` — чтобы gateway проверял пользователя.
6. Проверка **сервисного токена** на входе identity (`SERVICE_API_TOKEN` в конфиге + middleware).

### C. PARADIGM — долги целевой модели авторизации (04)
7. Подключить OAuth-движок наружу (логика готова — `repositories.py:238-346`, маршруты 501).
8. Включить проверку `client_secret` в прод-реализации OAuth (сейчас отключена — `repositories.py:274-275`).
9. Прокинуть флаг «нужен eID» в реальный флоу старта (поля сессии готовы, роут 501).
10. Дописать orchestration eID (start → провайдер → callback → выставить `eid_verified`).

### D. EXCESS — лишнее (истории / ложные связи), на вынос/удаление
11. Story-роуты `/story-drafts`, `/story-drafts/{id}/submit`, `/stories`, `/gpt/actions/submit-story` (`asgi_app.py:258-310`).
12. Таблица `story_drafts` + `StoryDraft` + InMemory/Supabase story-репозитории + контракт `StoryDraftRepository`.
13. `story_drafts` из `_REQUIRED_TABLES` healthcheck (`db_supabase.py:315-320`) — иначе `/ready`=503 (**высокий эффект**).
14. Пустой пакет `core.stories`.
15. Устаревшая модель req-15 (форвард identity→gateway) — привести требования в соответствие.

### E. PLACEHOLDER — заготовки без кода (решение «оставить/убрать» — за владельцем)
16. web3 wallet-колонки `profiles.wallet_*`.
17. `ALLOWED_RETURN_URLS` — без валидации (риск open-redirect).
18. `StubBearerTokenAuth` — не используется.
19. `eideasy`/`authentigate` — конфиг без кода провайдеров.
20. `CODE_VERIFIER_ENCRYPTION_KEY` — секрет без применения.
21. `idempotency-key`-резолвер — без потребителей.
22. Пустые пакеты `core.audit`, `core.oauth`, `core.profiles`.

### F. BUG — латентные дефекты
23. `EID_PROVIDER=eideasy/authentigate` → `KeyError` (валидатор пропускает, реестр пуст для них).
24. (см. также #8 — client_secret) и #13 — healthcheck/ready.

### G. DOC — рассинхрон документации
25. req-08 / req-02: «3 миграции» против фактических 4.
26. req-15: отменённая модель форварда — пометить устаревшей.

---

> ⏳ Дальше: жду, как ты хочешь это структурировать (эпики/приоритеты/волны). Доп. находки, не попавшие в runtime-docs (напр. `.env.example` `AUTHENTIGATE_REDIRECT_URI` указывает на несуществующий роут — gap CFG-3), лежат в [gap-анализе](gap-analysis-full-2026-06-04.md) — подниму по твоему запросу.
