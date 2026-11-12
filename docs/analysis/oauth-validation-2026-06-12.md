# Валидация OAuth: реализация vs требование-14 vs backlog (2026-06-12)

> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`; gaps с severity.
> **Вопрос:** реализован ли OAuth полноценно? достаточно ли качественно прописан backlog [`oauth/`](../tasks/backlog-stories/oauth/EPIC-IDS-OAUTH.md)? стыкуется ли с функциональным требованием [`14-oauth-server-custom-gpt.md`](../requirements/14-oauth-server-custom-gpt.md)?

## Вердикт
**OAuth реализован НЕ полноценно — частично (движок есть, HTTP-слой 501).** Backlog directionally верен, но **под-специфицирован** vs требование-14 — есть material-пробелы.

## 1. Что реализовано (по коду)
| Компонент | Факт | Статус |
|-----------|------|--------|
| Движок токенов | `InMemoryOAuthTokenService` ([repositories.py:430](../../src/core/infrastructure/repositories.py)) | ✅ |
| Выдача authorization code | `issue_authorization_code` (token_urlsafe, TTL `oauth_authorization_code_ttl_s`, PKCE-поля) | ✅ |
| Обмен code→token | `issue_access_token`: invalid_grant на consumed/expired/client-mismatch/redirect-mismatch | ✅ |
| **PKCE S256** | sha256(verifier)→b64url→сравнение с challenge ([repositories.py](../../src/core/infrastructure/repositories.py)) | ✅ соответствует §POST/token п.4 |
| Формат access-token JWT | HS256, claims `iss/sub/aud/exp/iat/jti/scope/token_type/client_id` | ✅ соответствует §Access Token Format |
| Валидация токена | `validate_access_token` → `OAuthTokenClaims` | ✅ |
| Конфиг | `OAUTH_ACCESS_TOKEN_SECRET`, `OAUTH_*_TTL_S`, `GPT_OAUTH_CLIENT_*` ([schema.py:44-48,211-216](../../src/core/config/schema.py)) | ✅ |
| Supabase client-store | `SupabaseOAuthClientStore` хэширует `client_secret` ([db_supabase.py:672-693](../../src/core/infrastructure/db_supabase.py)) | ✅ (частично) |

## 2. Что НЕ реализовано (по коду)
| Пробел | Где | Severity |
|--------|-----|----------|
| **HTTP-роуты 501** — `/oauth/authorize`, `/oauth/authorize/complete`, `/oauth/token` → `handle_bearer_stub` (движок не подключён) | [asgi_app.py:334-372](../../src/core/api/asgi_app.py), [handlers.py:732](../../src/core/api/handlers.py) | **HIGH** |
| **`client_secret` не проверяется** (in-memory `del client_secret`) | [repositories.py](../../src/core/infrastructure/repositories.py) (SEC-1) | **HIGH** |
| **Нет `authorization_request`-стора** — промежуточный `oauth_request_id` (authorize → spa login → complete) из §GET/authorize п.5-6 и §complete; в движке только `_codes` | repositories.py | **HIGH** |
| **Durability:** `OAuthTokenService` только in-memory ([providers.py:88](../../src/core/infrastructure/providers.py)) — codes/handshake теряются на редеплое/при нескольких инстансах. Access-токены stateless (ок). | repositories.py | MEDIUM → закрыто [OAUTH-03](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) |
| **`/oauth/authorize` валидации** — `invalid_client` / `invalid_redirect_uri` (direct, не redirect) / `invalid_scope` / `state` | требование §GET/authorize п.1-4 | MEDIUM |
| **Кто принимает OAuth-access-token на эндпоинтах** — `get_current_user` валидирует только **Supabase** JWT ([security.py](../../src/core/api/security.py)); путь приёма OAuth-токена (от ChatGPT) не реализован | требование §15 / §валидация | **HIGH** |
| Формат ошибок RFC 6749 `{error, error_description}` | требование §Ошибки | MEDIUM |
| Scope-модель (`profile:read`/`stories:draft`/`stories:create`) | требование §Scope Model | MEDIUM |

## 3. Стыковка backlog `oauth/` с требованием-14
[`STORY-IDS-OAUTH-01`](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) покрывает: подключить роуты к движку, включить `client_secret`, PKCE. [`OAUTH-02`](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md) — introspection + сервисный токен.

**Под-специфицировано (backlog молчит, требование-14 детализирует):**
1. `authorization_request`-store + `oauth_request_id`-handshake (authorize↔spa-login↔complete) — **ключевой кусок флоу, не упомянут**.
2. Валидации на `/oauth/authorize` (`invalid_client`/`invalid_redirect_uri`/`invalid_scope`/`state`).
3. Какой токен принимают защищённые эндпоинты (Supabase vs OAuth-access) — модель приёма OAuth-токена.
4. Формат ошибок RFC 6749 + scope-модель.

> Эти пункты добавлены в Scope OAUTH-01 (правка 2026-06-12) со ссылкой на требование-14 — закрывает качественный gap бэклога.

## 4. Реконсиляция с фронт-требованием
Фронт-дока ([identity-frontend.md](../../../docs/Identify/identity-frontend.md)) AC-16/17 (старая нумерация) и новый AC-17 ожидают рабочий `/oauth/authorize`. Сейчас невозможно (501). **Вход #2 (GPT) — заблокирован OAUTH-01.** Зафиксировано в gap G1 ([identity-onboarding-ux-2026-06-12.md](./identity-onboarding-ux-2026-06-12.md)) как HIGH.

## 5. Итог
- OAuth **частичен**: движок (выдача/обмен/PKCE/валидация) готов и матчит требование; **HTTP, client_secret-enforcement, authorize-handshake, приём OAuth-токена — отсутствуют**.
- Backlog был **directionally ок, но не покрывал** authorize-handshake / валидации / token-acceptance / RFC6749 / scope — **дополнен** в OAUTH-01.
- **Блокер входа #2 (GPT): OAUTH-01 (HIGH).**

## Quality gate
- [x] Все claims с `file:line`; сверка движка с требованием §POST/token — совпадает.
- [x] Пробелы классифицированы по severity; HIGH = роуты/secret/handshake/token-acceptance.
- [x] Backlog-стыковка проверена против требования-14; недостающее перечислено и внесено в OAUTH-01.
