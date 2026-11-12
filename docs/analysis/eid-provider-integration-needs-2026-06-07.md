# eID Provider Integration — потребности кода (provider-agnostic)

> **Назначение.** Контекст-документ для подготовки в отдельном диалоге анализа, склеивающего нашу
> архитектуру с документацией конкретного eID-провайдера (eID Easy / Authentigate / др.) в рамках
> [STORY-IDS-EID-02](../tasks/backlog-stories/eid-deferred/STORY-IDS-EID-02-real-eid-providers.md).
> **Принцип.** Здесь зафиксированы требования **нашего кода** к любому провайдеру — без привязки к
> конкретному вендору. Всё ниже проверено по реальному коду (методология [`analysis.mdc`](../../../.cursor/rules/analysis.mdc)).
> **Статус кода на 2026-06-07:** реально зарегистрирован только `mock`; боевые провайдеры не написаны.

---

## 1. Карта компонентов eID-слоя (как есть)

| Слой | Файл | Роль |
|------|------|------|
| Контракт провайдера | [`src/core/providers/base.py`](../../src/core/providers/base.py) | `EIDProviderPort` (Protocol) + DTO + `EIDProviderError` |
| Реестр | [`src/core/providers/registry.py`](../../src/core/providers/registry.py) | `get(name)` / `get_active(config)` |
| Эталон реализации | [`src/core/providers/mock/mock_provider.py`](../../src/core/providers/mock/mock_provider.py) | mock-провайдер — рабочий пример контракта |
| Сборка/DI | [`src/core/infrastructure/providers.py`](../../src/core/infrastructure/providers.py) | наполнение реестра, инъекция зависимостей |
| Оркестрация HTTP | [`src/core/api/handlers.py`](../../src/core/api/handlers.py) (`handle_auth_eid_start`, `handle_auth_eid_callback`) | бизнес-логика флоу, провайдер-агностичная |
| Маршруты | [`src/core/api/asgi_app.py`](../../src/core/api/asgi_app.py) | `/auth/eid/start`, `/auth/<provider>/callback` |
| Сессия | [`src/core/domain/models.py`](../../src/core/domain/models.py) (`VerificationSession`) + [`contracts.py`](../../src/core/domain/contracts.py) (`VerificationSessionStore`) | состояние флоу между start и callback |
| Конфиг | [`src/core/config/schema.py`](../../src/core/config/schema.py) (`AppConfig`) | env-параметры провайдеров |
| Крипто | [`src/core/security/hashing.py`](../../src/core/security/hashing.py) (`hash_secret`) | HMAC-SHA256 для `subject_hash` |

> ⚠️ **Расхождение с requirements.** Доки [req-17](../requirements/17-eid-provider-abstraction.md) и
> [req-18](../requirements/18-eideasy-provider.md) описывают **async** методы и `handle_callback`,
> возвращающий кортеж `(result, return_url)`, а также `registry.get_active_provider()` через import-switch.
> **Реальный код — синхронный**, `handle_callback` возвращает только `EIDVerificationResult`, а
> `return_url` берётся оркестратором из сессии. Ниже описан **фактический** контракт; на него и нужно
> опираться при реализации. Requirements-доки в этой части устарели.

---

## 2. Контракт, который обязан реализовать провайдер

[`base.py:32-53`](../../src/core/providers/base.py#L32-L53) — `EIDProviderPort` (Protocol, `@runtime_checkable`, **синхронный**):

```python
@property
def provider_name(self) -> str            # машинное имя: должно совпадать с EID_PROVIDER и сегментом callback-роута
@property
def callback_path(self) -> str            # путь callback: "/auth/<name>/callback"

def start_flow(self, *, supabase_user_id: str, return_url: str,
               return_context: str | None = None,
               requested_action: str | None = None) -> EIDStartResult

def handle_callback(self, *, raw_params: dict[str, str]) -> EIDVerificationResult
```

DTO ([`base.py:8-29`](../../src/core/providers/base.py#L8-L29)):

- `EIDStartResult(redirect_url: str, session_id: str, expires_at: datetime)` — `redirect_url` уходит SPA как `window.location`.
- `EIDVerificationResult(provider, country, subject_hash, login_method, verified_at)` (frozen) — провайдер-агностичный результат верификации.
- `EIDProviderError(message, *, code="EID_PROVIDER_ERROR")` — для ошибок с машинным кодом.

### Что должен вернуть `EIDVerificationResult` (минимальный набор данных от вендора)
| Поле | Тип | Семантика / что мапить из ответа провайдера |
|------|-----|---------------------------------------------|
| `provider` | str | собственное `provider_name` |
| `country` | str | ISO-страна личности (MVP — `EE`) |
| `subject_hash` | str | **стабильный уникальный идентификатор личности**, НЕ сырой idcode (см. §6) |
| `login_method` | str | метод аутентификации (`smartid` / `mid-login` / `ee-id-login` / …) |
| `verified_at` | datetime | момент успешной верификации (UTC) |

---

## 3. Жизненный цикл сессии — жёсткие ограничения архитектуры

Сессия — единственный мост между `start_flow` и `handle_callback` (разные HTTP-запросы).

### 3.1. Хранилище допускает только создание, не обновление
`VerificationSessionStore` ([`contracts.py:43-54`](../../src/core/domain/contracts.py#L43-L54)):
`create`, `get_by_state`, `get_by_id`, `mark_consumed`, `mark_failed`, `expire_pending`.
**Метода update нет.**

➡️ **Следствие:** всё, что провайдеру понадобится на callback (`state`, PKCE `code_verifier`, `nonce`,
любые vendor-данные), он обязан положить в сессию **в момент `create()` внутри `start_flow`** — в поля
`state`, `nonce`, `code_verifier_encrypted`, `code_verifier_hash` или в JSONB `provider_session_data`.
Дописать в сессию после редиректа нельзя.

Поля `VerificationSession` ([`models.py:44-59`](../../src/core/domain/models.py#L44-L59)):
`id, supabase_user_id, state, nonce, code_verifier_encrypted, code_verifier_hash, return_context,
return_url, requested_action, status, created_at, expires_at, provider, provider_session_data: dict`.
PKCE-поля nullable — OAuth2-провайдеры оставляют их `None` и кладут `state` в `provider_session_data`/`state`.

### 3.2. Резолв callback завязан на `state`
Оркестратор ([`handlers.py:176-186`](../../src/core/api/handlers.py#L176-L186)) ищет сессию так:
сначала по `raw_params["state"]` (`get_by_state`), иначе по `raw_params["session_id"]` (`get_by_id`).

➡️ **Следствие:** authorize-URL провайдера **обязан** прокидывать `state`, и провайдер возвращает его в
callback как query-параметр `state`. Значение `state` = поле `session.state`, заданное при `create()`.

### 3.3. `handle_callback` НЕ получает объект сессии
Оркестратор ([`handlers.py:262-264`](../../src/core/api/handlers.py#L262-L264)) загружает сессию для своих
проверок, но в провайдер передаёт **только `raw_params`**.

➡️ **Следствие:** если провайдеру для обмена кода нужны сохранённые секреты (PKCE `code_verifier`, `nonce`),
он должен **сам** перечитать сессию из store по `state` внутри `handle_callback`. Значит провайдеру нужна
инъекция `VerificationSessionStore` в конструктор (как у mock — [`mock_provider.py:13`](../../src/core/providers/mock/mock_provider.py#L13)).

### 3.4. Машина состояний и истечение — на стороне оркестратора
[`handlers.py:207-260`](../../src/core/api/handlers.py#L207-L260): проверка `provider`-совпадения,
статусов (`consumed`→идемпотентный 200, `failed`/`expired`→400, не-`started`→400), и срок жизни
(`expires_at < now` → `mark_failed("session_expired")`). Провайдеру **не нужно** дублировать эти проверки —
он отвечает только за криптографию протокола (state/code/token/identity). Срок: mock ставит 10 минут;
провайдер задаёт собственный разумный TTL в `start_flow`.

---

## 4. Поток управления (как оркестратор зовёт провайдера)

```
POST /auth/eid/start  (Bearer JWT → current_user)
  └─ handle_auth_eid_start (handlers.py:114)
       ├─ validate_return_url(return_url) по allowlist  → 400 при нарушении
       ├─ provider = registry.get_active(config)         # config.eid_provider
       ├─ result = provider.start_flow(supabase_user_id, return_url, return_context, requested_action)
       │     └─ провайдер: store.create(session{state, status="started", expires_at, provider, ...})
       │                    + строит authorize-URL вендора (с redirect_uri и state)
       ├─ audit "eid_verification_started"
       └─ 200 {redirect_url, expires_at, session_id}

GET /auth/<provider>/callback?code=...&state=...
  └─ handle_auth_eid_callback (handlers.py:189, provider_name из роута)
       ├─ session = resolve(raw_params by state|session_id)        → 400 если нет
       ├─ проверки: provider-match / status / expiry               → 400/200
       ├─ provider = registry.get(provider_name)                   # ВАЖНО: get, не get_active
       ├─ verification = provider.handle_callback(raw_params)
       │     └─ провайдер: (при необходимости перечитать сессию по state)
       │                    validate state → exchange code→token → fetch+validate identity
       │                    → EIDVerificationResult(country, subject_hash, login_method, ...)
       │        любое исключение → оркестратор: mark_failed("provider_error"), audit, 400
       ├─ verified_person_hash = hash_secret(f"{country}:{subject_hash}", key=config.eid_secret)
       ├─ profile_repo.attach_eid_verification(...)                → ProfileConflictError → 409
       ├─ store.mark_consumed(session.id) + audit "eid_verification_success"
       └─ 200 {status:"verified", return_url?}
```

> Нюанс §4: callback вызывает `registry.get(provider_name)` (по сегменту URL), а start — `get_active(config)`.
> Это **второй симптом gap EID-1** (см. §7): если активный провайдер не зарегистрирован, оба падают `KeyError`.

---

## 5. Конфигурация (env), доступная провайдеру

`AppConfig` ([`schema.py:18-56`](../../src/core/config/schema.py#L18-L56)) уже содержит поля для двух
провайдеров (значения — пример из `.env.example`, не догма):

**Общие:** `eid_provider`, `eid_secret` (`DOGESTONIA_EID_SECRET`), `node_id`, `api_base_url`,
`request_timeout_s`, `oidc_request_timeout_s`, `allowed_return_urls`.

**OAuth2-стиль (eideasy):** `eideasy_env`, `eideasy_base_url`, `eideasy_client_id`,
`eideasy_client_secret`, `eideasy_redirect_uri`, `eideasy_allowed_methods`, `eideasy_default_country`,
`eideasy_allowed_countries`. Валидатор требует `EIDEASY_CLIENT_ID/SECRET/REDIRECT_URI` при
`EID_PROVIDER=eideasy` ([`schema.py:109-112`](../../src/core/config/schema.py#L109-L112)).

**OIDC-стиль (authentigate):** `authentigate_issuer`, `authentigate_client_id`,
`authentigate_client_secret`, `authentigate_redirect_uri`, `authentigate_scopes`.

➡️ **Provider-agnostic вывод:** для нового провайдера нужен аналогичный блок env (base_url/issuer,
client_id, client_secret, redirect_uri, scopes/methods, country-allowlist) + строка валидации
обязательных полей при его активации.

---

## 6. Контракт `subject_hash` (защита PII)

- Провайдер **никогда** не возвращает сырой национальный idcode. Поле `subject_hash` —
  уже хэш/псевдоним стабильного идентификатора личности.
- Оркестратор **повторно** хэширует его: `verified_person_hash = hash_secret(f"{country}:{subject_hash}", key=eid_secret)`
  ([`handlers.py:283-286`](../../src/core/api/handlers.py#L283-L286)) — это значение и есть ключ дедупликации
  личности (`profile_repo.get_by_verified_person_hash`, конфликт → 409).
- `hash_secret` ([`hashing.py:9`](../../src/core/security/hashing.py#L9)) — HMAC-SHA256, **односторонний**.
- ⚠️ Symmetric-encrypt/decrypt helper'а для `code_verifier_encrypted` в коде **нет**. Но в зависимостях есть
  `cryptography>=42`, `httpx` (HTTP-клиент) и `joserfc` (JOSE/JWT — для валидации OIDC ID-токена) —
  [`pyproject.toml`](../../pyproject.toml). OIDC-провайдеру helper шифрования `code_verifier` придётся добавить.

---

## 7. Gaps и точки изменения для STORY-IDS-EID-02

| ID | Что | Где |
|----|-----|-----|
| **EID-1** | Валидатор пускает `eideasy`/`authentigate`, реестр содержит только `mock` → `KeyError` в `get()`/`get_active()` | [`schema.py:97-99`](../../src/core/config/schema.py#L97-L99) ↔ [`registry.py:11-14`](../../src/core/providers/registry.py#L11-L14) ↔ [`providers.py:92`](../../src/core/infrastructure/providers.py#L92) |
| **EID-2** | Боевой провайдер по `EIDProviderPort` не написан | `src/core/providers/<name>/` (новый) |
| Реестр | Зарегистрировать новый провайдер (+ его DI: store, config, HTTP-клиент) | [`providers.py:92`](../../src/core/infrastructure/providers.py#L92) |
| Guard | Понятная ошибка конфигурации вместо голого `KeyError` (AC story) | `registry.get` |
| Роут | Подключить `/auth/<name>/callback` к `handle_auth_eid_callback` вместо `handle_public_stub` | [`asgi_app.py:214-236`](../../src/core/api/asgi_app.py#L214-L236) |
| Крипто | Helper шифрования `code_verifier` (если провайдер OIDC/PKCE) | новый, на базе `cryptography` |

Маршрут `/auth/mock/callback` уже подключён к боевому хендлеру ([`asgi_app.py:238-248`](../../src/core/api/asgi_app.py#L238-L248)) — образец проводки для нового провайдера.

---

## 8. Тестовые ожидания (из AC story)

- Юнит на разбор callback'а провайдера (мапинг ответа вендора → `EIDVerificationResult`).
- Полный eID-флоу против тестового окружения вендора (live-тест, **скип без credentials**).
- Существующая база тестов: [`tests/test_eid_providers.py`](../../tests/test_eid_providers.py),
  [`tests/test_eid_provider_registry.py`](../../tests/test_eid_provider_registry.py),
  [`tests/test_eid_verification_flow.py`](../../tests/test_eid_verification_flow.py), [`tests/integration/`](../../tests/integration/).

---

## 9. Что должна дать документация выбранного провайдера (вход для следующего анализа)

Чтобы склеить нашу архитектуру с вендором, из его документации нужно извлечь:

1. **Протокол.** OAuth2 Authorization Code (как eID Easy — без PKCE/nonce/ID-token) или OIDC
   (как Authentigate — discovery, JWKS, ID-token, PKCE/nonce). От этого зависит, какие поля сессии нужны.
2. **Endpoints.** authorize-URL, token-endpoint, userinfo/identity-endpoint (или OIDC discovery URL).
3. **Параметры authorize.** обязательные query (client_id, redirect_uri, scope/method, `state`,
   при OIDC — `nonce`, `code_challenge`/`method`). Подтвердить, что `state` round-trip'ится в callback.
4. **Обмен code→token.** формат запроса (auth-метод клиента: basic/post), формат ответа, тайминги.
5. **Identity payload.** где взять страну, стабильный идентификатор личности, метод логина; как из них
   построить `subject_hash` (формат message; единый ключ — `DOGESTONIA_EID_SECRET`).
6. **Валидация.** для OIDC — issuer/aud/exp/nonce/подпись (JWKS); для OAuth2 — серверная проверка `state`.
7. **Тестовое окружение.** sandbox base URL, как получить test-credentials, регистрация redirect_uri,
   тестовые личности.
8. **Коды ошибок** вендора → маппинг в `EIDProviderError.code` / `failure_reason` аудита.

Результат следующего анализа: документ, мапящий пункты 1–8 на §2–§6 этого файла, + конкретный план
реализации `src/core/providers/<name>/` под AC story.

---

## Anchors
- Story: [STORY-IDS-EID-02](../tasks/backlog-stories/eid-deferred/STORY-IDS-EID-02-real-eid-providers.md)
- Парадигма: [runtime-docs/06-eid-providers.md](../runtime-docs/06-eid-providers.md)
- Requirements (частично устарели, см. §2): [req-17](../requirements/17-eid-provider-abstraction.md), [req-18](../requirements/18-eideasy-provider.md), [req-12](../requirements/12-authentigate-oidc-client.md)
- Backlog/gaps: [identity-todo-backlog-2026-06-04](identity-todo-backlog-2026-06-04.md)
