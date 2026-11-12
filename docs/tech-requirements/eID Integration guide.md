# DOGEstonia × eID Easy Integration Guide

## Provider: eID Easy OAuth2 IDaaS

## Target: `src/core/providers/eideasy/`

---

# 1. Цель интеграции

Цель интеграции — добавить реального eID-провайдера `eideasy`, который реализует текущий DOGEstonia provider-agnostic контракт:

```python
class EIDProviderPort(Protocol):
    @property
    def provider_name(self) -> str: ...

    @property
    def callback_path(self) -> str: ...

    def start_flow(
        self,
        *,
        supabase_user_id: str,
        return_url: str,
        return_context: str | None = None,
        requested_action: str | None = None,
    ) -> EIDStartResult: ...

    def handle_callback(
        self,
        *,
        raw_params: dict[str, str],
    ) -> EIDVerificationResult: ...
```

Фактический контракт в нашем коде синхронный: `handle_callback` возвращает только `EIDVerificationResult`, а `return_url` берётся оркестратором из `VerificationSession`, поэтому новый провайдер должен ориентироваться именно на фактический контракт, а не на старые async requirements. 

---

# 2. Архитектурное решение

## 2.1 Что интегрируем

Интегрируем:

```text
eID Easy Authentication / IDaaS OAuth2 flow
```

Документация eID Easy описывает IDaaS как OAuth2-based authentication: пользователь редиректится на eID Easy login page, проходит выбранный метод, возвращается на сайт с token/code, а сервер получает данные пользователя с сервера eID Easy. ([eID Easy Docs][2])

## 2.2 Что НЕ интегрируем в MVP

Не интегрируем в MVP:

```text
eID Easy OIDC / eID and Wallet Hub
```

Причина: OIDC Hub у eID Easy сейчас обозначен как beta, доступен только в `https://test.eideasy.com`, и документация прямо говорит не использовать этот flow в production applications до general availability. ([eID Easy Docs][3])

## 2.3 Почему OAuth2 IDaaS подходит лучше

eID Easy OAuth2 IDaaS даёт ровно нужные DOGEstonia поля для EE методов:

```text
idcode
country
status
current_login_method
```

Примеры eID Easy для Smart-ID, Mobile-ID и ID-card показывают, что после успешной authentication API возвращает `idcode`, `country=EE`, `status=OK` и `current_login_method`. ([eID Easy Docs][4])

---

# 3. Как eID Easy ложится на DOGEstonia flow

## 3.1 Общий runtime flow

```text
POST /auth/eid/start
  ↓
FastAPI validates DOGEstonia Supabase session
  ↓
registry.get_active(config) → eideasy provider
  ↓
eideasy.start_flow(...)
  ↓
provider creates VerificationSession with state
  ↓
provider returns redirect_url to SPA
  ↓
React Native opens redirect_url in system browser/AuthSession
  ↓
User verifies via eID Easy
  ↓
eID Easy redirects to /auth/eideasy/callback?code=...&state=...
  ↓
orchestrator resolves session by state
  ↓
eideasy.handle_callback(raw_params)
  ↓
provider exchanges code → access_token
  ↓
provider calls /api/v2/user_data
  ↓
provider maps user_data → EIDVerificationResult
  ↓
orchestrator creates verified_person_hash
  ↓
profile_repo.attach_eid_verification(...)
```

Это совпадает с текущим оркестратором: `start` вызывает `provider.start_flow`, а callback резолвит session по `state`, затем вызывает `provider.handle_callback(raw_params)` и ожидает `EIDVerificationResult`. 

---

# 4. eID Easy endpoints

## 4.1 Production endpoints

Для OAuth2 IDaaS eID Easy указывает:

```text
Authorize URL:
https://id.eideasy.com/oauth/authorize

Access token URL:
https://id.eideasy.com/oauth/access_token

User data URL:
https://id.eideasy.com/api/v2/user_data
```

Эти параметры перечислены в eID Easy Turnkey Solution docs. ([eID Easy Docs][5])

## 4.2 Test environment endpoints

Для тестовой среды eID Easy говорит: заменить URLs, которые начинаются с `https://id.eideasy.com/`, на `https://test.eideasy.com/`; в test environment все действия бесплатны. ([eID Easy Docs][6])

Значит для DOGEstonia:

```env
# Test
EIDEASY_BASE_URL=https://test.eideasy.com

# Production
EIDEASY_BASE_URL=https://id.eideasy.com
```

И provider должен строить endpoints от `base_url`:

```python
authorize_url = f"{base_url}/oauth/authorize"
token_url = f"{base_url}/oauth/access_token"
user_data_url = f"{base_url}/api/v2/user_data"
```

---

# 5. Как создать sandbox/test credentials в eID Easy

## 5.1 Создать test account

По eID Easy Test Environment docs нужно зайти в test environment sign-up page на `https://test.eideasy.com/`, выбрать email/password signup и получить test API credentials. Документация объясняет, что API credentials — это `client_id` и `secret`, которые нужны для запросов к eID Easy API. ([eID Easy Docs][6])

## 5.2 Зарегистрировать webpage/app

В eID Easy self-service portal нужно создать/зарегистрировать webpage/application и указать redirect URI. В eID Easy setup docs для похожих интеграций указано, что в self-service portal нужно открыть **My Webpages**, нажать “Register new webpage”, указать website home page address и `redirect_uri`, а затем сохранить `client_id` и `secret`. ([eID Easy Docs][7])

Для DOGEstonia test:

```text
Webpage / App name:
DOGEstonia Test

Home page:
https://dogestonia.ee
или текущий staging URL

Redirect URI:
https://<public-api-host>/auth/eideasy/callback
```

Для локального тестирования callback должен быть публично доступен. Практический вариант:

```text
ngrok / cloudflared tunnel
https://<tunnel-domain>/auth/eideasy/callback
```

Тогда этот exact redirect URI надо зарегистрировать в eID Easy test portal.

## 5.3 Настроить env

Минимальный env для test:

```env
EID_PROVIDER=eideasy
DOGESTONIA_EID_SECRET=<long-random-secret>

EIDEASY_ENV=test
EIDEASY_BASE_URL=https://test.eideasy.com
EIDEASY_CLIENT_ID=<from eID Easy test portal>
EIDEASY_CLIENT_SECRET=<from eID Easy test portal>
EIDEASY_REDIRECT_URI=https://<public-api-host>/auth/eideasy/callback

EIDEASY_DEFAULT_COUNTRY=EE
EIDEASY_ALLOWED_COUNTRIES=EE
EIDEASY_ALLOWED_METHODS=smartid,mid-login,ee-id-login

ALLOWED_RETURN_URLS=dogestonia://story/continue,https://dogestonia.ee/verify,https://dogestonia.ee/dashboard/verify
```

Основание: eID Easy OAuth2 flow требует `client_id`, `client_secret`, `redirect_uri`, authorize/token/user_data endpoints; DOGEstonia code requirements уже ожидают provider-specific env fields for eideasy. ([eID Easy Docs][5]) 

---

# 6. Методологическое условие: только EE methods для MVP

## 6.1 Разрешённые методы

Для DOGEstonia MVP нужно разрешить только методы, которые подтверждены документацией eID Easy как возвращающие EE identity payload с `idcode`, `country`, `status`, `current_login_method`.

Разрешить:

```text
smartid
mid-login
ee-id-login
```

eID Easy Smart-ID test response содержит `idcode`, `country=EE`, `status=OK`, `current_login_method=smartid`. ([eID Easy Docs][4])

eID Easy Mobile-ID test response содержит `idcode`, `country=EE`, `status=OK`, `current_login_method=mid-login`. ([eID Easy Docs][8])

eID Easy ID-card test response показывает `idcode`, `country=EE`, `status=OK`, `current_login_method=ee-id-login`. ([eID Easy Docs][8])

## 6.2 Почему нужно ограничение

eID Easy предупреждает, что разные authentication methods могут возвращать разные поля, и некоторые могут не возвращать `idcode` или `birth_date`. ([eID Easy Docs][9])

Для DOGEstonia это критично, потому что anti-Sybil слой требует стабильный уникальный идентификатор личности, который provider adapter мапит в `subject_hash`. 

---

# 7. Provider package structure

Создать:

```text
src/core/providers/eideasy/
  __init__.py
  provider.py
  client.py
  mapper.py
  errors.py
```

Роли:

```text
provider.py
  EIDEasyProvider implements EIDProviderPort.

client.py
  Thin HTTP client for eID Easy:
  - exchange_code_for_token()
  - fetch_user_data()

mapper.py
  Validate and map eID Easy user_data payload to EIDVerificationResult.

errors.py
  Provider-specific error code constants.
```

---

# 8. Provider constructor dependencies

`handle_callback` получает только `raw_params`, не объект session. Если provider нужны `state`, `nonce`, `code_verifier`, vendor data, он должен сам перечитать session из store по `state`. Поэтому `EIDEasyProvider` должен получить `VerificationSessionStore` в конструктор. 

Пример:

```python
class EIDEasyProvider:
    def __init__(
        self,
        *,
        config: AppConfig,
        session_store: VerificationSessionStore,
        http_client: httpx.Client,
        clock: Callable[[], datetime],
    ) -> None:
        self.config = config
        self.session_store = session_store
        self.http_client = http_client
        self.clock = clock
```

---

# 9. `provider_name` and callback path

```python
@property
def provider_name(self) -> str:
    return "eideasy"

@property
def callback_path(self) -> str:
    return "/auth/eideasy/callback"
```

`provider_name` должен совпадать с `EID_PROVIDER=eideasy` и сегментом callback route `/auth/<provider>/callback`, потому что callback handler берёт provider name из route и делает `registry.get(provider_name)`. 

---

# 10. `start_flow()` implementation

## 10.1 Input

```python
def start_flow(
    self,
    *,
    supabase_user_id: str,
    return_url: str,
    return_context: str | None = None,
    requested_action: str | None = None,
) -> EIDStartResult:
    ...
```

Оркестратор уже валидирует `return_url` по allowlist до вызова provider, но provider всё равно должен считать `return_url` opaque value и не модифицировать его. 

## 10.2 Generate session state

Для eID Easy OAuth2 IDaaS PKCE не обязателен по их docs. Поэтому можно оставить:

```python
code_verifier_encrypted=None
code_verifier_hash=None
nonce=<random optional or None>
```

Но `state` обязателен, потому что DOGEstonia callback resolution завязан на `state`. eID Easy docs рекомендуют использовать `state` for CSRF protection and return it in callback. ([eID Easy Docs][9])

Пример:

```python
state = secrets.token_urlsafe(32)
expires_at = now_utc() + timedelta(minutes=10)
```

## 10.3 Create `VerificationSession`

```python
session = VerificationSession(
    id=uuid4(),
    supabase_user_id=supabase_user_id,
    state=state,
    nonce=None,
    code_verifier_encrypted=None,
    code_verifier_hash=None,
    return_context=return_context,
    return_url=return_url,
    requested_action=requested_action,
    status="started",
    created_at=now,
    expires_at=expires_at,
    provider="eideasy",
    provider_session_data={
        "country": self.config.eideasy_default_country,
        "allowed_methods": self.config.eideasy_allowed_methods,
        "allowed_countries": self.config.eideasy_allowed_countries,
    },
)
self.session_store.create(session)
```

Важное условие: session store допускает создание, но не update, поэтому всё, что понадобится на callback, нужно положить в session сразу в `start_flow`. 

## 10.4 Build authorize URL

Базовый OAuth2 authorize endpoint:

```text
{EIDEASY_BASE_URL}/oauth/authorize
```

eID Easy требует `client_id`, `redirect_uri`, `response_type=code`; `state` optional but recommended. ([eID Easy Docs][9])

Для DOGEstonia:

```python
params = {
    "client_id": config.eideasy_client_id,
    "redirect_uri": config.eideasy_redirect_uri,
    "response_type": "code",
    "state": state,
    "country": "EE",
    "allow_country_change": "false",
}
```

Опционально можно добавить method selection:

```python
params["start"] = "smartid"
params["allow_method_change"] = "false"
```

Но для MVP лучше начать без принудительного `start`, чтобы пользователь мог выбрать Smart-ID / Mobile-ID / ID-card внутри разрешённой страны, а adapter потом проверит `current_login_method`. Если позже нужно жёстко ограничивать UX, можно включить `start` и `allow_method_change=false`; eID Easy docs поддерживают `start`, `country`, `allow_method_change`, `allow_country_change`. ([eID Easy Docs][9])

## 10.5 Return

```python
return EIDStartResult(
    redirect_url=authorize_url,
    session_id=str(session.id),
    expires_at=expires_at,
)
```

---

# 11. Frontend launch condition

React Native должен открыть `redirect_url` через system browser/AuthSession, не WebView. Это не только наше требование: eID Easy прямо говорит, что на mobile eID/signing flows должны открываться в default browser, in-app browsers не поддерживаются, и flows нельзя отображать внутри iframe. ([eID Easy Docs][9])

Frontend requirement:

```text
Use:
- Expo AuthSession / WebBrowser
- ASWebAuthenticationSession on iOS
- Chrome Custom Tabs on Android

Do not use:
- embedded WebView
- iframe
- in-app browser
```

---

# 12. `handle_callback()` implementation

## 12.1 Input

```python
def handle_callback(self, *, raw_params: dict[str, str]) -> EIDVerificationResult:
    ...
```

Expected callback:

```text
/auth/eideasy/callback?code=<authorization_code>&state=<state>
```

eID Easy docs confirm that callback includes `code`, and includes `state` if it was set in authorize request. ([eID Easy Docs][9])

## 12.2 Validate required callback params

```python
state = raw_params.get("state")
if not state:
    raise EIDProviderError("Missing state", code="EIDEASY_MISSING_STATE")

code = raw_params.get("code")
if not code:
    raise EIDProviderError("Missing code", code="EIDEASY_MISSING_CODE")
```

## 12.3 Load session by state

Even though orchestrator already loads session, provider must reload it if it needs provider data, because `handle_callback` only receives `raw_params`. 

```python
session = self.session_store.get_by_state(state)
if not session:
    raise EIDProviderError("Verification session not found", code="EIDEASY_SESSION_NOT_FOUND")

if session.provider != "eideasy":
    raise EIDProviderError("Provider mismatch", code="EIDEASY_PROVIDER_MISMATCH")
```

Do not duplicate full status/expiry machine if orchestrator already handles it; provider can rely on orchestrator for lifecycle enforcement. 

## 12.4 Exchange code → access token

Token endpoint:

```text
POST {base_url}/oauth/access_token
Content-Type: application/x-www-form-urlencoded
```

Required body:

```text
client_id
client_secret
redirect_uri
code
grant_type=authorization_code
```

eID Easy docs define this exact access token request and show access token response with `access_token`, `token_type`, `expires_in`. ([eID Easy Docs][9])

Implementation:

```python
response = http_client.post(
    f"{base_url}/oauth/access_token",
    data={
        "client_id": config.eideasy_client_id,
        "client_secret": config.eideasy_client_secret,
        "redirect_uri": config.eideasy_redirect_uri,
        "code": code,
        "grant_type": "authorization_code",
    },
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    timeout=config.request_timeout_s,
)
```

Validate:

```python
if response.status_code != 200:
    raise EIDProviderError("Token exchange failed", code="EIDEASY_TOKEN_EXCHANGE_FAILED")

payload = response.json()
access_token = payload.get("access_token")
if not access_token:
    raise EIDProviderError("Missing access token", code="EIDEASY_MISSING_ACCESS_TOKEN")
```

## 12.5 Fetch user data

User data endpoint:

```text
GET {base_url}/api/v2/user_data
Authorization: Bearer <access_token>
```

This endpoint is listed by eID Easy as the resource owner / user data endpoint for OAuth2 authentication. ([eID Easy Docs][5])

Implementation:

```python
response = http_client.get(
    f"{base_url}/api/v2/user_data",
    headers={"Authorization": f"Bearer {access_token}"},
    timeout=config.request_timeout_s,
)
```

Validate HTTP:

```python
if response.status_code != 200:
    raise EIDProviderError("User data request failed", code="EIDEASY_USER_DATA_FAILED")
```

---

# 13. Map user_data → `EIDVerificationResult`

## 13.1 Expected user_data

For target EE methods, expected shape:

```json
{
  "idcode": "30303039914",
  "lastname": "Testnumber",
  "firstname": "Ok",
  "birth_date": "1903-03-03",
  "country": "EE",
  "status": "OK",
  "current_login_method": "smartid"
}
```

eID Easy Smart-ID docs show this exact structure for a successful EE Smart-ID authentication. ([eID Easy Docs][4])

Mobile-ID docs show `current_login_method=mid-login` and `country=EE`; ID-card docs show `current_login_method=ee-id-login`. ([eID Easy Docs][8])

## 13.2 Required validations

```python
status = data.get("status")
if status != "OK":
    raise EIDProviderError("Identity status is not OK", code="EIDEASY_IDENTITY_NOT_OK")

country = data.get("country")
if country not in config.eideasy_allowed_countries:
    raise EIDProviderError("Country not allowed", code="EIDEASY_COUNTRY_NOT_ALLOWED")

idcode = data.get("idcode")
if not idcode:
    raise EIDProviderError("Missing idcode", code="EIDEASY_MISSING_IDCODE")

login_method = data.get("current_login_method")
if login_method not in config.eideasy_allowed_methods:
    raise EIDProviderError("Method not allowed", code="EIDEASY_METHOD_NOT_ALLOWED")
```

Reason: eID Easy warns that different authentication methods can return different fields, and DOGEstonia needs `idcode`/stable identity for anti-Sybil. ([eID Easy Docs][9])

## 13.3 Privacy transformation: raw `idcode` must not leave adapter

DOGEstonia provider contract says `subject_hash` must be a stable unique identity identifier, not raw idcode; then orchestrator performs another HMAC into `verified_person_hash`. 

Therefore:

```python
subject_hash = hash_secret(
    f"eideasy:{country}:{idcode}",
    key=config.eid_secret,
)
```

Then return:

```python
return EIDVerificationResult(
    provider="eideasy",
    country=country,
    subject_hash=subject_hash,
    login_method=login_method,
    verified_at=now_utc(),
)
```

Never return:

```python
idcode
firstname
lastname
birth_date
raw user_data
access_token
```

---

# 14. Why double-HMAC is acceptable

The eID Easy adapter creates:

```text
subject_hash = HMAC(eid_secret, "eideasy:EE:<idcode>")
```

Then orchestrator creates:

```text
verified_person_hash = HMAC(eid_secret, "EE:<subject_hash>")
```

This is slightly redundant, but safe and compatible with the current contract: provider never leaks raw national idcode, while core keeps a provider-agnostic deduplication key. The uploaded integration requirements explicitly say the provider returns `subject_hash`, and orchestrator hashes `country:subject_hash` again for profile deduplication. 

If later you want cleaner separation, use two secrets:

```env
DOGESTONIA_EID_PROVIDER_SUBJECT_SECRET=...
DOGESTONIA_EID_SECRET=...
```

But for MVP, using the existing `eid_secret` is acceptable if it is long, random, and server-only.

---

# 15. Config updates

## 15.1 Current config expectations

The integration document says `AppConfig` already contains fields:

```text
eideasy_env
eideasy_base_url
eideasy_client_id
eideasy_client_secret
eideasy_redirect_uri
eideasy_allowed_methods
eideasy_default_country
eideasy_allowed_countries
```

and validator requires `EIDEASY_CLIENT_ID`, `EIDEASY_CLIENT_SECRET`, `EIDEASY_REDIRECT_URI` when `EID_PROVIDER=eideasy`. 

## 15.2 Required env values

Test:

```env
EID_PROVIDER=eideasy
DOGESTONIA_EID_SECRET=<strong-random-secret>

EIDEASY_ENV=test
EIDEASY_BASE_URL=https://test.eideasy.com
EIDEASY_CLIENT_ID=<test-client-id>
EIDEASY_CLIENT_SECRET=<test-client-secret>
EIDEASY_REDIRECT_URI=https://<public-api-host>/auth/eideasy/callback

EIDEASY_DEFAULT_COUNTRY=EE
EIDEASY_ALLOWED_COUNTRIES=EE
EIDEASY_ALLOWED_METHODS=smartid,mid-login,ee-id-login
```

Production:

```env
EID_PROVIDER=eideasy
DOGESTONIA_EID_SECRET=<production-strong-random-secret>

EIDEASY_ENV=production
EIDEASY_BASE_URL=https://id.eideasy.com
EIDEASY_CLIENT_ID=<prod-client-id>
EIDEASY_CLIENT_SECRET=<prod-client-secret>
EIDEASY_REDIRECT_URI=https://api.dogestonia.ee/auth/eideasy/callback

EIDEASY_DEFAULT_COUNTRY=EE
EIDEASY_ALLOWED_COUNTRIES=EE
EIDEASY_ALLOWED_METHODS=smartid,mid-login,ee-id-login
```

eID Easy test environment docs say all `https://id.eideasy.com/` URLs can be replaced with `https://test.eideasy.com/` for test server requests. ([eID Easy Docs][6])

---

# 16. Registry / DI changes

Current gap: validator allows `eideasy`, but registry contains only `mock`, so `registry.get()` / `get_active()` can raise `KeyError`. 

## 16.1 Register provider

In `src/core/infrastructure/providers.py`:

```python
from src.core.providers.eideasy.provider import EIDEasyProvider

def build_provider_registry(...):
    registry = EIDProviderRegistry()

    registry.register(mock_provider)

    eideasy_provider = EIDEasyProvider(
        config=config,
        session_store=verification_session_store,
        http_client=httpx.Client(timeout=config.request_timeout_s),
        clock=clock,
    )
    registry.register(eideasy_provider)

    return registry
```

## 16.2 Guard against missing provider

Update `registry.get()` and `get_active()` to return a clear config error instead of raw `KeyError`:

```python
class EIDProviderNotRegisteredError(Exception):
    ...

def get(self, name: str) -> EIDProviderPort:
    try:
        return self._providers[name]
    except KeyError:
        raise EIDProviderNotRegisteredError(
            f"EID provider '{name}' is not registered"
        )
```

This is explicitly listed as a gap/acceptance-condition area in the integration requirements. 

---

# 17. Routes

The integration document says `/auth/mock/callback` is already connected to the real handler and serves as wiring example. For the new provider, route `/auth/eideasy/callback` must be connected to `handle_auth_eid_callback`, not to a public stub. 

Add or ensure:

```python
GET /auth/eideasy/callback
  → handle_auth_eid_callback(provider_name="eideasy", raw_params=query_params)
```

---

# 18. Error mapping

## 18.1 Provider-specific errors

Create `errors.py`:

```python
EIDEASY_MISSING_STATE = "EIDEASY_MISSING_STATE"
EIDEASY_MISSING_CODE = "EIDEASY_MISSING_CODE"
EIDEASY_SESSION_NOT_FOUND = "EIDEASY_SESSION_NOT_FOUND"
EIDEASY_PROVIDER_MISMATCH = "EIDEASY_PROVIDER_MISMATCH"
EIDEASY_TOKEN_EXCHANGE_FAILED = "EIDEASY_TOKEN_EXCHANGE_FAILED"
EIDEASY_MISSING_ACCESS_TOKEN = "EIDEASY_MISSING_ACCESS_TOKEN"
EIDEASY_USER_DATA_FAILED = "EIDEASY_USER_DATA_FAILED"
EIDEASY_IDENTITY_NOT_OK = "EIDEASY_IDENTITY_NOT_OK"
EIDEASY_MISSING_IDCODE = "EIDEASY_MISSING_IDCODE"
EIDEASY_COUNTRY_NOT_ALLOWED = "EIDEASY_COUNTRY_NOT_ALLOWED"
EIDEASY_METHOD_NOT_ALLOWED = "EIDEASY_METHOD_NOT_ALLOWED"
```

OIDC eID Easy docs list standard OAuth/OIDC error categories like `invalid_client`, `invalid_grant`, `unauthorized_client`, `invalid_request`; for IDaaS OAuth2 adapter, map equivalent token/user_data failures into provider error codes above. ([eID Easy Docs][1])

## 18.2 Do not leak vendor payload

Logs may include:

```text
provider=eideasy
error_code
http_status
request_id if available
```

Logs must not include:

```text
idcode
firstname
lastname
birth_date
access_token
raw user_data
```

This follows DOGEstonia’s provider contract and privacy constraints: raw national ID must not leave provider adapter, and core stores only derived hashes. 

---

# 19. Sandbox testing guide

## 19.1 Prepare eID Easy test credentials

Steps:

1. Open eID Easy test environment.
2. Sign up using email/password.
3. Open self-service / My Webpages.
4. Register new webpage/app.
5. Set redirect URI:

   ```text
   https://<public-api-host>/auth/eideasy/callback
   ```
6. Copy:

   ```text
   client_id
   client_secret
   ```
7. Set:

   ```env
   EIDEASY_BASE_URL=https://test.eideasy.com
   ```

eID Easy test environment guide says to use `https://test.eideasy.com` for the test server and explains that client_id/secret are required API credentials. ([eID Easy Docs][6])

## 19.2 Use public callback URL

If developing locally:

```bash
ngrok http 8000
```

Then set:

```env
EIDEASY_REDIRECT_URI=https://<ngrok-id>.ngrok-free.app/auth/eideasy/callback
```

and register the exact same URL in eID Easy test portal. Redirect URI mismatch will normally break OAuth2 token exchange.

## 19.3 Test Smart-ID

eID Easy Smart-ID test docs provide an EE happy-path ID code:

```text
EE: 30303039914
```

The expected response includes:

```json
{
  "idcode": "30303039914",
  "country": "EE",
  "status": "OK",
  "current_login_method": "smartid"
}
```

([eID Easy Docs][4])

Manual test:

1. Open DOGEstonia app.
2. Login/signup.
3. Create draft story.
4. Start eID verification.
5. Choose Estonia.
6. Choose Smart-ID.
7. Enter test idcode.
8. Wait for automatic confirmation.
9. Confirm DOGEstonia returns to `dogestonia://story/continue?draft_id=...`.
10. Check `/me.eid_verified=true`.
11. Submit draft.

## 19.4 Test Mobile-ID

eID Easy Mobile-ID test docs show expected response:

```json
{
  "idcode": "60001019906",
  "country": "EE",
  "status": "OK",
  "current_login_method": "mid-login"
}
```

and refer to SK Mobile-ID demo test number/personal identity code. ([eID Easy Docs][8])

Manual test:

1. Use eID Easy demo/test instructions for Mobile-ID.
2. Enter test phone number and personal identity code.
3. Wait for automatic confirmation.
4. Validate `login_method=mid-login`.

## 19.5 Test ID-card

eID Easy ID-card test docs show the target response shape with `idcode`, `country=EE`, `status=OK`, `current_login_method=ee-id-login`; ID-card testing may require Estonian test ID-card setup. ([eID Easy Docs][8])

For automated CI, ID-card full browser/certificate flow is likely not practical. Mark it as manual integration test unless you have a dedicated test environment.

---

# 20. Unit test plan

## 20.1 `mapper.py` unit tests

Test payloads:

### Smart-ID success

Input:

```json
{
  "idcode": "30303039914",
  "country": "EE",
  "status": "OK",
  "current_login_method": "smartid"
}
```

Expected:

```text
provider=eideasy
country=EE
login_method=smartid
subject_hash present
subject_hash != raw idcode
```

### Mobile-ID success

```json
{
  "idcode": "60001019906",
  "country": "EE",
  "status": "OK",
  "current_login_method": "mid-login"
}
```

Expected:

```text
login_method=mid-login
```

### ID-card success

```json
{
  "idcode": "39111123456",
  "country": "EE",
  "status": "OK",
  "current_login_method": "ee-id-login"
}
```

Expected:

```text
login_method=ee-id-login
```

## 20.2 Negative tests

```text
missing idcode → EIDEASY_MISSING_IDCODE
country=LV with allowed EE only → EIDEASY_COUNTRY_NOT_ALLOWED
status != OK → EIDEASY_IDENTITY_NOT_OK
method not in allowed list → EIDEASY_METHOD_NOT_ALLOWED
raw idcode never appears in result/logs
```

## 20.3 `start_flow()` tests

Expected:

```text
creates VerificationSession
session.provider == eideasy
session.state is non-empty
session.status == started
session.supabase_user_id is correct
session.return_url is preserved
redirect_url contains:
  client_id
  redirect_uri
  response_type=code
  state=session.state
  country=EE
```

## 20.4 `handle_callback()` tests with mocked HTTP

Mock token response:

```json
{
  "access_token": "test-access-token",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

Mock user data response:

```json
{
  "idcode": "30303039914",
  "country": "EE",
  "status": "OK",
  "current_login_method": "smartid"
}
```

Expected:

```text
EIDVerificationResult(provider="eideasy", country="EE", login_method="smartid")
```

## 20.5 Registry tests

```text
EID_PROVIDER=eideasy → registry.get_active(config).provider_name == eideasy
/auth/eideasy/callback → registry.get("eideasy")
unregistered provider → clear config error, not raw KeyError
```

The current provider integration document explicitly lists missing production providers, registry KeyError risk, and new route wiring as STORY-IDS-EID-02 gaps. 

---

# 21. Integration test plan

## 21.1 CI-safe tests

These do not call eID Easy live:

```text
test_eideasy_start_flow_builds_authorize_url
test_eideasy_maps_smartid_user_data
test_eideasy_maps_mobileid_user_data
test_eideasy_maps_idcard_user_data
test_eideasy_rejects_missing_idcode
test_eideasy_rejects_disallowed_country
test_eideasy_rejects_disallowed_method
test_eideasy_never_returns_raw_idcode
test_registry_registers_eideasy
```

## 21.2 Live tests, skipped without credentials

Use pytest markers:

```python
pytestmark = pytest.mark.integration
```

Skip unless:

```env
EIDEASY_CLIENT_ID
EIDEASY_CLIENT_SECRET
EIDEASY_REDIRECT_URI
EIDEASY_BASE_URL=https://test.eideasy.com
```

Test:

```text
start_flow returns redirect_url pointing to https://test.eideasy.com/oauth/authorize
```

Full callback live-test requires browser interaction and should be manual or semi-automated because user must complete Smart-ID/Mobile-ID/ID-card flow.

---

# 22. Manual end-to-end test checklist

## 22.1 Smart-ID happy path

```text
[ ] User logged in through DOGEstonia/Supabase
[ ] POST /story-drafts returns draft_id
[ ] POST /auth/eid/start returns eID Easy redirect_url
[ ] redirect_url opens system browser/AuthSession
[ ] User chooses Estonia + Smart-ID
[ ] User enters test idcode
[ ] eID Easy redirects to /auth/eideasy/callback?code&state
[ ] Orchestrator resolves session by state
[ ] Provider exchanges code for access token
[ ] Provider fetches user_data
[ ] Provider maps idcode → subject_hash
[ ] Orchestrator stores verified_person_hash
[ ] /me returns eid_verified=true
[ ] App resumes draft_id
[ ] POST /story-drafts/{draft_id}/submit succeeds
```

## 22.2 Conflict path

```text
[ ] Account A verifies with test idcode
[ ] Account B tries same idcode
[ ] attach_eid_verification detects same verified_person_hash
[ ] Backend returns identity_already_linked / 409
[ ] No account merge
[ ] Frontend shows identity conflict screen
```

## 22.3 Replay path

```text
[ ] Complete callback once
[ ] Repeat same callback URL
[ ] Orchestrator rejects invalid_or_consumed_state
[ ] No second profile update
```

## 22.4 Expired session

```text
[ ] Start flow
[ ] Force expires_at < now
[ ] Callback arrives
[ ] Orchestrator marks session expired
[ ] Returns error
```

---

# 23. Security requirements for implementation

## 23.1 `state` is mandatory

Even though eID Easy marks `state` optional, for DOGEstonia it is mandatory because session resolution depends on `state`. eID Easy docs recommend state as CSRF protection and return it in callback when provided. ([eID Easy Docs][9])

## 23.2 Never log raw identity

Do not log:

```text
idcode
firstname
lastname
birth_date
raw user_data
access_token
client_secret
```

## 23.3 Never expose raw identity to core

`EIDVerificationResult.subject_hash` must not be raw `idcode`.

Correct:

```python
subject_hash = HMAC("eideasy:EE:<idcode>")
```

Incorrect:

```python
subject_hash = idcode
```

The DOGEstonia integration contract says provider returns `subject_hash`, while core hashes it again into `verified_person_hash`; raw national ID must not be returned from provider. 

## 23.4 Only default browser/AuthSession

No WebView, no iframe. eID Easy explicitly disallows mobile in-app browsers and iframes for eID/signing flows. ([eID Easy Docs][9])

## 23.5 Restrict country and methods

For MVP:

```text
country == EE
method in smartid, mid-login, ee-id-login
```

Reason: our anti-Sybil mechanism needs stable identity identifier and we validated eID Easy examples for those EE methods. ([eID Easy Docs][4])

---

# 24. Production readiness conditions

Before switching production:

```text
[ ] eID Easy production account is approved
[ ] Production My Webpages app registered
[ ] Production redirect URI configured:
    https://api.dogestonia.ee/auth/eideasy/callback
[ ] EIDEASY_BASE_URL=https://id.eideasy.com
[ ] EIDEASY_CLIENT_ID set from production portal
[ ] EIDEASY_CLIENT_SECRET set from production portal
[ ] DOGESTONIA_EID_SECRET strong and not reused from test
[ ] allowed countries = EE
[ ] allowed methods = smartid,mid-login,ee-id-login
[ ] logs verified not to contain idcode/access_token
[ ] frontend uses AuthSession/system browser
[ ] full Smart-ID and Mobile-ID happy path tested
[ ] conflict test completed
[ ] replay test completed
[ ] expired session test completed
```

eID Easy production OAuth2 endpoints are under `https://id.eideasy.com`, while test environment uses `https://test.eideasy.com`. ([eID Easy Docs][6])

---

# 25. Minimal implementation skeleton

```python
# src/core/providers/eideasy/provider.py

class EIDEasyProvider:
    provider_name = "eideasy"
    callback_path = "/auth/eideasy/callback"

    def __init__(self, *, config, session_store, http_client, clock):
        self.config = config
        self.session_store = session_store
        self.http = http_client
        self.clock = clock

    def start_flow(
        self,
        *,
        supabase_user_id: str,
        return_url: str,
        return_context: str | None = None,
        requested_action: str | None = None,
    ) -> EIDStartResult:
        now = self.clock()
        state = secrets.token_urlsafe(32)
        expires_at = now + timedelta(minutes=10)

        session = VerificationSession(
            id=str(uuid.uuid4()),
            supabase_user_id=supabase_user_id,
            state=state,
            nonce=None,
            code_verifier_encrypted=None,
            code_verifier_hash=None,
            return_context=return_context,
            return_url=return_url,
            requested_action=requested_action,
            status="started",
            created_at=now,
            expires_at=expires_at,
            provider="eideasy",
            provider_session_data={
                "allowed_countries": self.config.eideasy_allowed_countries,
                "allowed_methods": self.config.eideasy_allowed_methods,
            },
        )
        self.session_store.create(session)

        redirect_url = build_url(
            f"{self.config.eideasy_base_url}/oauth/authorize",
            {
                "client_id": self.config.eideasy_client_id,
                "redirect_uri": self.config.eideasy_redirect_uri,
                "response_type": "code",
                "state": state,
                "country": self.config.eideasy_default_country,
                "allow_country_change": "false",
            },
        )

        return EIDStartResult(
            redirect_url=redirect_url,
            session_id=session.id,
            expires_at=expires_at,
        )

    def handle_callback(self, *, raw_params: dict[str, str]) -> EIDVerificationResult:
        state = raw_params.get("state")
        if not state:
            raise EIDProviderError("Missing state", code="EIDEASY_MISSING_STATE")

        code = raw_params.get("code")
        if not code:
            raise EIDProviderError("Missing code", code="EIDEASY_MISSING_CODE")

        session = self.session_store.get_by_state(state)
        if not session:
            raise EIDProviderError("Session not found", code="EIDEASY_SESSION_NOT_FOUND")

        token = self._exchange_code(code)
        data = self._fetch_user_data(token)
        return self._map_user_data(data)

    def _exchange_code(self, code: str) -> str:
        response = self.http.post(
            f"{self.config.eideasy_base_url}/oauth/access_token",
            data={
                "client_id": self.config.eideasy_client_id,
                "client_secret": self.config.eideasy_client_secret,
                "redirect_uri": self.config.eideasy_redirect_uri,
                "code": code,
                "grant_type": "authorization_code",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=self.config.request_timeout_s,
        )
        if response.status_code != 200:
            raise EIDProviderError(
                "Token exchange failed",
                code="EIDEASY_TOKEN_EXCHANGE_FAILED",
            )

        access_token = response.json().get("access_token")
        if not access_token:
            raise EIDProviderError(
                "Missing access token",
                code="EIDEASY_MISSING_ACCESS_TOKEN",
            )
        return access_token

    def _fetch_user_data(self, access_token: str) -> dict:
        response = self.http.get(
            f"{self.config.eideasy_base_url}/api/v2/user_data",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=self.config.request_timeout_s,
        )
        if response.status_code != 200:
            raise EIDProviderError(
                "User data failed",
                code="EIDEASY_USER_DATA_FAILED",
            )
        return response.json()

    def _map_user_data(self, data: dict) -> EIDVerificationResult:
        if data.get("status") != "OK":
            raise EIDProviderError(
                "Identity status is not OK",
                code="EIDEASY_IDENTITY_NOT_OK",
            )

        country = data.get("country")
        if country not in self.config.eideasy_allowed_countries:
            raise EIDProviderError(
                "Country not allowed",
                code="EIDEASY_COUNTRY_NOT_ALLOWED",
            )

        idcode = data.get("idcode")
        if not idcode:
            raise EIDProviderError(
                "Missing idcode",
                code="EIDEASY_MISSING_IDCODE",
            )

        login_method = data.get("current_login_method")
        if login_method not in self.config.eideasy_allowed_methods:
            raise EIDProviderError(
                "Method not allowed",
                code="EIDEASY_METHOD_NOT_ALLOWED",
            )

        subject_hash = hash_secret(
            f"eideasy:{country}:{idcode}",
            key=self.config.eid_secret,
        )

        return EIDVerificationResult(
            provider="eideasy",
            country=country,
            subject_hash=subject_hash,
            login_method=login_method,
            verified_at=self.clock(),
        )
```

---

# 26. Final acceptance checklist for STORY-IDS-EID-02

```text
[ ] EIDEasyProvider implements EIDProviderPort.
[ ] Provider registered in registry.
[ ] /auth/eideasy/callback wired to real callback handler.
[ ] EID_PROVIDER=eideasy does not crash with KeyError.
[ ] start_flow creates VerificationSession with state.
[ ] redirect_url points to eID Easy authorize endpoint.
[ ] state round-trips from authorize to callback.
[ ] handle_callback exchanges code for access_token.
[ ] handle_callback fetches user_data.
[ ] Smart-ID user_data maps to EIDVerificationResult.
[ ] Mobile-ID user_data maps to EIDVerificationResult.
[ ] ID-card user_data maps to EIDVerificationResult.
[ ] Raw idcode is never returned from provider.
[ ] subject_hash is deterministic and not equal to idcode.
[ ] Orchestrator creates verified_person_hash.
[ ] Duplicate same idcode causes identity conflict.
[ ] Unverified user cannot submit final story.
[ ] Verified user can submit final story.
[ ] Frontend opens eID Easy only via system browser/AuthSession.
[ ] Sandbox credentials documented.
[ ] Live test skipped unless credentials are present.
```

---

# 27. Short engineering decision record

```text
Decision:
Use eID Easy OAuth2 IDaaS as the MVP eID provider adapter.

Reason:
It fits the current DOGEstonia EIDProviderPort, uses client_id/client_secret already present in AppConfig, supports OAuth2 authorization code flow, returns EE idcode/country/current_login_method for Smart-ID, Mobile-ID, and ID-card test flows, and does not require OIDC private_key_jwt infrastructure.

Rejected for MVP:
eID Easy OIDC / eID Wallet Hub.

Reason:
Currently documented as beta and sandbox/test-only. Production support is not available yet.

Privacy rule:
eID Easy may return raw idcode in user_data, but DOGEstonia provider adapter must immediately convert it into subject_hash and never return/log/store raw idcode.

Security rule:
state is mandatory; callback is resolved through VerificationSession; no WebView or iframe; only EE methods allowed for MVP.
```

This guide should be enough to hand to the backend developer as implementation context for `src/core/providers/eideasy/`, while keeping it aligned with the account-first DOGEstonia identity architecture and the provider-agnostic code contract.

[1]: https://docs.eideasy.com/oidc/oidc-guide?utm_source=chatgpt.com "OIDC Integration Guide | eID Easy Docs"
[2]: https://docs.eideasy.com/authentication/?utm_source=chatgpt.com "Authentication (IDaaS) | eID Easy Docs"
[3]: https://docs.eideasy.com/oidc/?utm_source=chatgpt.com "eID and Wallet Hub | eID Easy Docs"
[4]: https://docs.eideasy.com/guide/test-user/smartid?utm_source=chatgpt.com "Smart ID | eID Easy Docs"
[5]: https://docs.eideasy.com/authentication/turnkey-solution.html?utm_source=chatgpt.com "Turnkey Solution | eID Easy Docs"
[6]: https://docs.eideasy.com/guide/test-environment?utm_source=chatgpt.com "Test Environment | eID Easy Docs"
[7]: https://docs.eideasy.com/nextcloud/nextcloud-app-setup.html?utm_source=chatgpt.com "2. Set up | eID Easy Docs"
[8]: https://docs.eideasy.com/guide/test-user/mobileid?utm_source=chatgpt.com "Mobile ID | eID Easy Docs"
[9]: https://docs.eideasy.com/authentication/eideasy-authentication-page-flow.html?utm_source=chatgpt.com "eID Easy authentication page flow | eID Easy Docs"
