# DOGEstonia × Authentigate Integration Guide

## Provider: Authentigate OIDC Gateway

## Target: `src/core/providers/authentigate/`

---

## 1. Цель интеграции

Цель — реализовать боевой eID provider `authentigate`, который подключается к существующему DOGEstonia eID abstraction layer и реализует наш фактический provider contract:

```python
@property
def provider_name(self) -> str

@property
def callback_path(self) -> str

def start_flow(
    *,
    supabase_user_id: str,
    return_url: str,
    return_context: str | None = None,
    requested_action: str | None = None,
) -> EIDStartResult

def handle_callback(
    *,
    raw_params: dict[str, str],
) -> EIDVerificationResult
```

По нашему текущему коду провайдер должен быть синхронным, `handle_callback()` возвращает только `EIDVerificationResult`, а `return_url` берётся оркестратором из сохранённой verification session; всё, что понадобится провайдеру на callback, он должен положить в session на `start_flow()` или уметь перечитать session по `state`. 

---

## 2. Почему Authentigate подходит DOGEstonia MVP

Authentigate — это gateway от SK ID Solutions, который позволяет e-services запрашивать verified personal data на основе strong identity verification methods. В документации прямо указано, что он предназначен для e-services, которым нужно получать verified personal data о пользователях. ([Sk Eid][1])

Для Эстонии Authentigate поддерживает все три нужных метода:

```text
Smart-ID
Mobile-ID
ID-card
```

Это указано в таблице supported identity verification methods: Estonia имеет ✅ для Smart-ID, Mobile-ID и ID-Card. ([Sk Eid][1])

Для DOGEstonia это сильное совпадение:

```text
один provider adapter
один OIDC flow
один callback
одна логика hash/deduplication
три эстонских eID метода
```

---

## 3. Ключевое отличие от eID Easy

Для eID Easy MVP-кандидатом был OAuth2 IDaaS flow с `user_data`.

Для Authentigate правильная модель другая:

```text
Authentigate = OIDC provider / OIDC gateway
```

Authentigate возвращает `id_token`, а документация прямо требует, чтобы relying party валидировал подпись и claims ID token по OIDC Core. ([Sk Eid][2])

Значит adapter должен быть не “OAuth user_data adapter”, а полноценный **OIDC adapter**:

```text
authorize request
↓
callback code + state
↓
token exchange
↓
id_token validation
↓
extract attributes.*
↓
map to EIDVerificationResult
```

---

# 4. Матрица соответствия DOGEstonia requirements ↔ Authentigate docs

| DOGEstonia requirement                                             | Authentigate documentation                                                                                                                                                                                      | Вывод                                                                           |
| ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Provider должен поддерживать Authorization Code callback с `state` | Authentigate требует `response_type=code`; `state` — required для standard flow, используется для состояния между request и callback и mitigation replay/CSRF. ([Sk Eid][2])                                    | Полностью совместимо. `state` — mandatory.                                      |
| Callback должен возвращать `code` и `state`                        | После authentication token can be requested; token request uses authorization `code`, а error tracing/standard flow ожидает state; token request docs описывают code, полученный от OIDC service. ([Sk Eid][2]) | `/auth/authentigate/callback?code=...&state=...` подходит.                      |
| Provider должен уметь получить stable identity identifier          | Authentigate позволяет запросить `personal_code` и `personal_code_country`. ([Sk Eid][1])                                                                                                                       | Adapter строит `subject_hash` из `country + personal_code`.                     |
| Нельзя хранить raw personal code                                   | Authentigate может вернуть `personal_code`, но наш contract требует вернуть в core уже `subject_hash`, не raw idcode.                                                                                           | Adapter обязан сразу HMAC-ить `personal_code` и не логировать его.              |
| Нужно ограничить MVP на Эстонию                                    | Authentigate поддерживает EE Smart-ID, Mobile-ID, ID-card. ([Sk Eid][1])                                                                                                                                        | Использовать `acr_values` для EE методов: `sid_ee mid_ee idcard_ee`.            |
| Нужно запросить минимальные claims                                 | Authentigate scopes include `personal_code`, `personal_code_country`, а также имя, фамилию, birthdate, age и др. ([Sk Eid][1])                                                                                  | DOGEstonia запрашивает только `openid + personal_code + personal_code_country`. |
| Нужно валидировать ID token                                        | Документация говорит: RP must validate `id_token` signature and claims according to OIDC Core. ([Sk Eid][2])                                                                                                    | Обязательна JWKS/discovery validation.                                          |
| Нужен demo/sandbox                                                 | Authentigate demo environment supports UX exploration and technical integration; Demo Plan free of charge. ([Sk Eid][3])                                                                                        | Можно делать integration до production contract.                                |
| Нужны environment endpoints                                        | LIVE discovery: `https://id.authentigate.eu/.well-known/openid-configuration`; DEMO discovery: `https://oidc.demo.sk.ee/.well-known/openid-configuration`. ([Sk Eid][4])                                        | Config должен переключать demo/prod issuer.                                     |
| Нужны test accounts                                                | Demo docs дают Smart-ID Test Accounts / Mobile-ID Test Accounts; Smart-ID Basic/NQ accounts do not function, нужны Qualified/Q accounts. ([Sk Eid][3])                                                          | В тест-плане использовать Smart-ID Qualified demo accounts.                     |
| Нужна бюджетность                                                  | Public pricing: Starter from €29/month, 100 minimum transactions, €0.2900 additional transaction. ([Authentigate][5])                                                                                           | Подходит для пилота, но setup fee/min term надо подтвердить у SK.               |

---

# 5. Demo access и условия тестирования

## 5.1 Что подтверждено документацией

Authentigate предлагает два варианта demo testing:

```text
1. Explore UX/UI in browser without registration.
2. Integrate your own system for technical testing.
```

Для технического тестирования документация говорит:

```text
1. Request demo access via e-Service Portal.
2. Select Demo Plan, free of charge.
3. Include test environment details in the order form.
4. Wait for confirmation.
5. Set up integration with demo environment.
6. Start testing with API specifications.
```

([Sk Eid][3])

## 5.2 Demo endpoints

Для demo:

```text
Base URL:
https://oidc.demo.sk.ee/

Discovery:
https://oidc.demo.sk.ee/.well-known/openid-configuration
```

Для production:

```text
Base URL:
https://id.authentigate.eu

Discovery:
https://id.authentigate.eu/.well-known/openid-configuration
```

([Sk Eid][4])

## 5.3 Что нужно подготовить для demo request

Client Registration docs говорят, что каждый client должен быть зарегистрирован с такими обязательными данными:

```text
Client ID — generated by OIDC Provider
Client Secret — generated by OIDC Provider
Redirect URI — one or many allowed callback URIs
Allowed IPs — list of IPs allowed for this client
Service Name
```

Allowed Countries необязательны, но поддерживают значения вроде `EE`, `LV`, `LT`. ([Sk Eid][6])

Для DOGEstonia demo request:

```text
Service Name:
DOGEstonia

Environment:
Development / pilot

Redirect URI:
https://<public-api-host>/auth/authentigate/callback

Allowed IPs:
<server public IP or tunnel IP if accepted>

Allowed Countries:
EE

Authentication methods:
Smart-ID, Mobile-ID, ID-card

Use case:
One-time human verification for civic story submission.
Not financial KYC, not AML, not signing.
```

---

# 6. Registration / contract conditions

## 6.1 Demo

Demo integration is supported without needing a signed contract; documentation says demo integrations are supported for technical testing and Demo Plan is free of charge. ([Sk Eid][3])

## 6.2 Production

For production access, the general path is to request access, select pricing plan, provide live environment details, and sign agreement; the docs point to sales/contact for registration and production access. Client registration docs say you need to contact the sales team to initiate registration. ([Sk Eid][6])

Public pricing page says Starter starts from €29/month with 100 minimum transactions and €0.2900 per additional transaction, but it does not clearly state whether there is setup fee, minimum term, or entity requirements. ([Authentigate][5])

## 6.3 Что не подтверждено документацией

Нужно отдельно спросить у SK:

```text
Can an early civic-tech pilot use Starter plan?
Is there a setup fee?
Is there a minimum contract term?
Can a small pilot company/team get demo access?
Is company registration required for Demo Plan?
Is client_secret_basic available for our client?
Are EE-only methods configurable?
Can we request only personal_code + personal_code_country?
```

---

# 7. Authentigate OIDC request design

## 7.1 Required request parameters

Authentigate authentication request requires:

```text
scope
response_type=code
client_id
redirect_uri
state
```

`scope` must contain `openid`. `state` is required in standard flow and is used for maintaining state between request and callback and for replay/CSRF mitigation. ([Sk Eid][2])

## 7.2 Optional but recommended for DOGEstonia

Authentigate supports `nonce`; if provided, it is returned as a nonce claim in `id_token` and can mitigate replay attacks. ([Sk Eid][2])

For DOGEstonia we should include:

```text
nonce
code_challenge
code_challenge_method=S256
ui_locales=et en
acr_values=sid_ee mid_ee idcard_ee
sid_confirmation_message=DOGEstonia verification
mid_confirmation_message=DOGEstonia verification
mid_confirmation_message_format=GSM-7
```

Why include PKCE? Authentigate docs say `code_challenge` and `code_challenge_method` must be present if the client is `code-challenge-required` or if not using JWT authentication; token request also requires `code_verifier` in that case. ([Sk Eid][2])

---

# 8. `scope` design for DOGEstonia

## 8.1 Minimal scope

Use only:

```text
openid
https://id.authentigate.eu/claims/personal_code
https://id.authentigate.eu/claims/personal_code_country
```

Authentigate lists these claim scope values as personal identification code and country code that issued the personal identification code. ([Sk Eid][2])

## 8.2 Do not request unnecessary claims

Do not request:

```text
given_name
family_name
name
birthdate
age
age_over
age_under
```

Authentigate supports them, but DOGEstonia does not need them for anti-Sybil verification. The overview docs list these additional attributes, but our privacy model says to minimize identity data. ([Sk Eid][1])

---

# 9. `acr_values` design

Authentigate supports `acr_values` such as:

```text
mid_ee
mid_lt
sid
idcard
```

The docs include an example with `acr_values: "mid_ee mid_lt sid idcard"` and also error handling for invalid `acr_values`. ([Sk Eid][2])

For DOGEstonia MVP:

```text
acr_values = "sid_ee mid_ee idcard_ee"
```

Rationale:

```text
sid_ee     → Estonia Smart-ID
mid_ee     → Estonia Mobile-ID
idcard_ee  → Estonia ID-card
```

Order matters for UX if Authentigate uses the order in request; previously docs examples and Authentigate behavior indicate `acr_values` control allowed/presented methods, while invalid/unallowed values produce errors. ([Sk Eid][2])

**Implementation note:** exact allowed values for our client must be confirmed in demo, because Authentigate can reject ACR values not allowed for the registered client. The error table explicitly includes “client is not allowed to use acr”. ([Sk Eid][2])

---

# 10. Token exchange

## 10.1 Token endpoint

The token endpoint comes from discovery:

```text
Demo discovery:
https://oidc.demo.sk.ee/.well-known/openid-configuration

Live discovery:
https://id.authentigate.eu/.well-known/openid-configuration
```

([Sk Eid][4])

## 10.2 Required token request parameters

Authentigate token request requires:

```text
grant_type=authorization_code
code
redirect_uri
```

`redirect_uri` must be identical to the value included in initial Authorization Request. ([Sk Eid][2])

## 10.3 Client authentication options

Authentigate supports:

```text
client_secret_basic
private_key_jwt
```

For `client_secret_basic`, request uses HTTP Basic Authorization header. For `private_key_jwt`, request includes `client_assertion_type` and `client_assertion`, and the Authorization header must not be present. ([Sk Eid][2])

For DOGEstonia MVP:

```text
Prefer client_secret_basic if SK enables it.
```

Reason:

```text
- simpler implementation
- matches current AppConfig authentigate_client_secret
- avoids private_key_jwt/JWKS key management in MVP
```

## 10.4 PKCE / code verifier

If `code_challenge` was sent in authorize request, token request must send matching `code_verifier`. Authentigate says `code_verifier` must be present if client is code-challenge-required or if not using JWT authentication. ([Sk Eid][2])

Therefore our `AuthentigateProvider.start_flow()` must create and store:

```text
code_verifier
code_verifier_encrypted
code_verifier_hash
code_challenge = BASE64URL(SHA256(code_verifier))
code_challenge_method = S256
```

This matches our code requirements: anything provider needs on callback must be saved when creating the verification session, because session store has no generic update method. 

---

# 11. Token response and ID token

If token request validation succeeds, Authentigate returns JSON with:

```text
access_token
scope
expires_in
id_token
token_type=Bearer
```

The `id_token` is a serialized and signed JWT including requested end-user claims. ([Sk Eid][2])

The RP must validate `id_token` signature and claims according to OIDC Core. ([Sk Eid][2])

Decoded ID token claims include:

```text
sub
amr
iss
client_id
aud
acr
scope
acr_values
attributes.*
redirect_uri
state
exp
iat
jti
```

`attributes.*` is described as a key-value map of end-user info claims requested by RP in scope. ([Sk Eid][2])

---

# 12. Mapping ID token → `EIDVerificationResult`

## 12.1 Required values

DOGEstonia provider contract requires:

```text
provider
country
subject_hash
login_method
verified_at
```



## 12.2 Authentigate source fields

Use:

```text
country:
attributes["https://id.authentigate.eu/claims/personal_code_country"]

raw personal code:
attributes["https://id.authentigate.eu/claims/personal_code"]

login_method:
acr or amr
```

Claims are available only if requested in scope. Authentigate documents these scope values for personal code and country. ([Sk Eid][2])

## 12.3 Privacy rule

Do not return raw `personal_code`.

Adapter should compute:

```python
subject_hash = hash_secret(
    f"authentigate:{country}:{personal_code}",
    key=config.eid_secret,
)
```

Then return:

```python
EIDVerificationResult(
    provider="authentigate",
    country=country,
    subject_hash=subject_hash,
    login_method=login_method,
    verified_at=now_utc,
)
```

Core will then compute:

```python
verified_person_hash = hash_secret(
    f"{country}:{subject_hash}",
    key=config.eid_secret,
)
```

This double-HMAC pattern is aligned with our provider-agnostic contract: provider returns a stable pseudonymous `subject_hash`, and orchestrator hashes it again into the internal deduplication key. 

---

# 13. Provider package structure

Create:

```text
src/core/providers/authentigate/
  __init__.py
  provider.py
  client.py
  oidc.py
  mapper.py
  errors.py
```

Suggested roles:

```text
provider.py
  AuthentigateProvider implements EIDProviderPort.

client.py
  HTTP client for OIDC discovery, token request, JWKS retrieval.

oidc.py
  PKCE generation, id_token validation, JWKS cache.

mapper.py
  Map ID token claims → EIDVerificationResult.

errors.py
  Provider-specific error code constants.
```

---

# 14. Provider constructor dependencies

Because `handle_callback(raw_params)` receives only query params, the provider must be able to reload session by `state` if it needs `nonce`, `code_verifier_encrypted`, or vendor data. Our integration requirements explicitly state this pattern. 

Suggested constructor:

```python
class AuthentigateProvider:
    def __init__(
        self,
        *,
        config: AppConfig,
        session_store: VerificationSessionStore,
        http_client: httpx.Client,
        clock: Callable[[], datetime],
        crypto: CodeVerifierCrypto,
        jwks_cache: JWKSCache,
    ) -> None:
        ...
```

---

# 15. `provider_name` and callback path

```python
@property
def provider_name(self) -> str:
    return "authentigate"

@property
def callback_path(self) -> str:
    return "/auth/authentigate/callback"
```

This must match:

```text
EID_PROVIDER=authentigate
/auth/authentigate/callback
registry.get("authentigate")
```

The callback handler uses the provider segment from URL and calls `registry.get(provider_name)`, so registration and route naming must match. 

---

# 16. Config requirements

Current `AppConfig` already has Authentigate fields:

```text
authentigate_issuer
authentigate_client_id
authentigate_client_secret
authentigate_redirect_uri
authentigate_scopes
```

The provider-agnostic integration document confirms these fields exist as OIDC-style config for Authentigate. 

Recommended env for demo:

```env
EID_PROVIDER=authentigate
DOGESTONIA_EID_SECRET=<strong-random-secret>

AUTHENTIGATE_ISSUER=https://oidc.demo.sk.ee
AUTHENTIGATE_DISCOVERY_URL=https://oidc.demo.sk.ee/.well-known/openid-configuration
AUTHENTIGATE_CLIENT_ID=<from SK demo>
AUTHENTIGATE_CLIENT_SECRET=<from SK demo>
AUTHENTIGATE_REDIRECT_URI=https://<public-api-host>/auth/authentigate/callback

AUTHENTIGATE_SCOPES=openid https://id.authentigate.eu/claims/personal_code https://id.authentigate.eu/claims/personal_code_country
AUTHENTIGATE_ACR_VALUES=sid_ee mid_ee idcard_ee
AUTHENTIGATE_UI_LOCALES=et en
AUTHENTIGATE_COUNTRY=EE
```

Recommended env for production:

```env
EID_PROVIDER=authentigate
DOGESTONIA_EID_SECRET=<prod-strong-random-secret>

AUTHENTIGATE_ISSUER=https://id.authentigate.eu
AUTHENTIGATE_DISCOVERY_URL=https://id.authentigate.eu/.well-known/openid-configuration
AUTHENTIGATE_CLIENT_ID=<prod-client-id>
AUTHENTIGATE_CLIENT_SECRET=<prod-client-secret>
AUTHENTIGATE_REDIRECT_URI=https://api.dogestonia.ee/auth/authentigate/callback

AUTHENTIGATE_SCOPES=openid https://id.authentigate.eu/claims/personal_code https://id.authentigate.eu/claims/personal_code_country
AUTHENTIGATE_ACR_VALUES=sid_ee mid_ee idcard_ee
AUTHENTIGATE_UI_LOCALES=et en
AUTHENTIGATE_COUNTRY=EE
```

---

# 17. `start_flow()` design

## 17.1 Inputs

```python
def start_flow(
    *,
    supabase_user_id: str,
    return_url: str,
    return_context: str | None = None,
    requested_action: str | None = None,
) -> EIDStartResult:
    ...
```

Orchestrator already validates return URL before calling provider. Provider should preserve it in session, not trust it for redirect construction.

## 17.2 Generate OIDC session material

Generate:

```text
state
nonce
code_verifier
code_challenge
expires_at
```

Store in `VerificationSession`:

```text
state
nonce
code_verifier_encrypted
code_verifier_hash
return_url
return_context
requested_action
provider="authentigate"
provider_session_data:
  scopes
  acr_values
  issuer
```

This is necessary because session store supports creation/lookup/marking, not generic updates, so all callback-needed data must be stored at start. 

## 17.3 Build authorize URL

Use discovery authorization endpoint or:

```text
{issuer}/authorize
```

Request params:

```text
response_type=code
client_id=<client_id>
redirect_uri=<registered redirect_uri>
scope=openid + personal_code + personal_code_country
state=<state>
nonce=<nonce>
acr_values=sid_ee mid_ee idcard_ee
code_challenge=<S256 challenge>
code_challenge_method=S256
ui_locales=et en
sid_confirmation_message=DOGEstonia verification
mid_confirmation_message=DOGEstonia verification
mid_confirmation_message_format=GSM-7
```

Authentigate docs confirm these parameters: required `scope`, `response_type=code`, `client_id`, `redirect_uri`, `state`; optional `nonce`; `code_challenge`/`code_challenge_method` required when not using JWT auth or if code challenge is required; `sid_confirmation_message` and `mid_confirmation_message` are supported. ([Sk Eid][2])

---

# 18. Frontend launch requirement

Authentigate docs say the app should open the authorization link with an external user agent as recommended by OAuth2 native client best practices. ([Sk Eid][2])

This matches our React Native requirement:

```text
Use:
- Expo AuthSession / WebBrowser
- ASWebAuthenticationSession
- Chrome Custom Tabs

Do not use:
- embedded WebView
```

---

# 19. `handle_callback()` design

Expected callback:

```text
/auth/authentigate/callback?code=<code>&state=<state>
```

## 19.1 Validate callback params

```python
state = raw_params.get("state")
if not state:
    raise EIDProviderError("Missing state", code="AUTHENTIGATE_MISSING_STATE")

code = raw_params.get("code")
if not code:
    # Also handle raw_params["error"] if present
    raise EIDProviderError("Missing code", code="AUTHENTIGATE_MISSING_CODE")
```

## 19.2 Reload session

```python
session = session_store.get_by_state(state)
if not session:
    raise EIDProviderError("Session not found", code="AUTHENTIGATE_SESSION_NOT_FOUND")
```

Provider should use session to retrieve:

```text
nonce
code_verifier_encrypted
code_verifier_hash
provider_session_data
```

The orchestrator does status/expiry/provider checks, but provider needs session data for OIDC validation. 

## 19.3 Token exchange

Decrypt `code_verifier`.

POST to token endpoint:

```text
grant_type=authorization_code
code=<code>
code_verifier=<decrypted code_verifier>
redirect_uri=<same redirect_uri>
```

For `client_secret_basic`, add HTTP Basic `Authorization` header with `client_id:client_secret`. Authentigate token request examples show this pattern. ([Sk Eid][2])

## 19.4 Validate token response

Require:

```text
id_token present
token_type=Bearer
```

Token response includes `access_token`, `scope`, `expires_in`, `id_token`, and `token_type`. ([Sk Eid][2])

## 19.5 Validate ID token

Validate:

```text
signature via JWKS
iss == expected issuer
aud contains client_id
exp not expired
iat reasonable
nonce matches session.nonce if nonce was sent
state matches session.state if state claim present
jti unique if you implement replay cache
```

Authentigate explicitly says RP must validate ID token signature and claims as specified in OIDC Core, and its decoded claim list includes `iss`, `aud`, `exp`, `iat`, `nonce`, `state`, `jti`, and `attributes.*`. ([Sk Eid][2])

## 19.6 Extract attributes

From decoded ID token:

```python
attributes = claims.get("attributes") or claims.get("attribues")?
```

Important: the docs table appears to spell it as `attribues.*` in one line, likely a typo, while the textual meaning is “attributes.* key-value map”. We must verify the exact JSON key in demo before hardcoding. ([Sk Eid][2])

Expected attribute keys:

```python
PERSONAL_CODE = "https://id.authentigate.eu/claims/personal_code"
PERSONAL_CODE_COUNTRY = "https://id.authentigate.eu/claims/personal_code_country"
```

These scope/claim names are documented. ([Sk Eid][2])

## 19.7 Map to EIDVerificationResult

```python
country = attributes[PERSONAL_CODE_COUNTRY]
personal_code = attributes[PERSONAL_CODE]

subject_hash = hash_secret(
    f"authentigate:{country}:{personal_code}",
    key=config.eid_secret,
)

login_method = claims.get("acr") or ",".join(claims.get("amr", []))

return EIDVerificationResult(
    provider="authentigate",
    country=country,
    subject_hash=subject_hash,
    login_method=login_method,
    verified_at=now_utc(),
)
```

Do not return or log raw `personal_code`.

---

# 20. Error mapping

Authentigate docs list several relevant errors:

```text
user_cancel
invalid_scope
unsupported_response_type
invalid_request
invalid redirect_uri
missing state
missing code_challenge
missing code_challenge_method
invalid acr_values
invalid_client
too_many_requests
invalid_grant
```

These appear in `/authorize`, `/par`, and `/token` error tracing. ([Sk Eid][2])

Recommended adapter error codes:

```text
AUTHENTIGATE_MISSING_STATE
AUTHENTIGATE_MISSING_CODE
AUTHENTIGATE_USER_CANCEL
AUTHENTIGATE_INVALID_SCOPE
AUTHENTIGATE_INVALID_ACR_VALUES
AUTHENTIGATE_INVALID_REDIRECT_URI
AUTHENTIGATE_TOKEN_EXCHANGE_FAILED
AUTHENTIGATE_INVALID_GRANT
AUTHENTIGATE_MISSING_ID_TOKEN
AUTHENTIGATE_ID_TOKEN_VALIDATION_FAILED
AUTHENTIGATE_MISSING_ATTRIBUTES
AUTHENTIGATE_MISSING_PERSONAL_CODE
AUTHENTIGATE_MISSING_PERSONAL_CODE_COUNTRY
AUTHENTIGATE_COUNTRY_NOT_ALLOWED
AUTHENTIGATE_METHOD_NOT_ALLOWED
```

---

# 21. Demo testing guide

## 21.1 Get demo access

Steps from docs:

```text
1. Request demo access via e-Service Portal.
2. Select Demo Plan, free of charge.
3. Include test environment details.
4. Wait for confirmation.
5. Connect test system to demo environment.
6. Start testing with API Specifications.
```

([Sk Eid][3])

## 21.2 Test UX without registration first

Docs say UX/UI can be explored directly in browser without registration via demo client page. ([Sk Eid][3])

Use this before implementing adapter to inspect:

```text
which methods appear
what attributes are requestable
what Smart-ID/Mobile-ID flow looks like
```

## 21.3 Use correct test accounts

Docs state:

```text
Smart-ID Basic (NQ) accounts do not function with Authentigate.
Use Smart-ID Qualified (Q) accounts for testing.
```

([Sk Eid][3])

This must be in test plan.

---

# 22. Unit test plan

## 22.1 `start_flow()`

Assert:

```text
session.provider == "authentigate"
session.state is non-empty
session.nonce is non-empty
session.code_verifier_encrypted is present
session.code_verifier_hash is present
redirect_url contains:
  response_type=code
  client_id
  redirect_uri
  state
  nonce
  scope including openid + personal_code + personal_code_country
  acr_values
  code_challenge
  code_challenge_method=S256
```

## 22.2 `handle_callback()` with mocked token response

Mock token response:

```json
{
  "access_token": "opaque",
  "token_type": "Bearer",
  "scope": "openid https://id.authentigate.eu/claims/personal_code https://id.authentigate.eu/claims/personal_code_country",
  "expires_in": 3600,
  "id_token": "<signed jwt>"
}
```

Validate:

```text
ID token signature checked
issuer checked
audience checked
exp checked
nonce checked
attributes extracted
personal_code hashed
raw personal_code not returned
```

## 22.3 Mapping tests

Input claims:

```json
{
  "iss": "https://oidc.demo.sk.ee",
  "aud": "dogestonia-client",
  "exp": 9999999999,
  "iat": 9999999000,
  "nonce": "session-nonce",
  "state": "session-state",
  "acr": "sid_ee",
  "amr": ["sid"],
  "attributes": {
    "https://id.authentigate.eu/claims/personal_code": "49101010000",
    "https://id.authentigate.eu/claims/personal_code_country": "EE"
  }
}
```

Expected:

```text
provider=authentigate
country=EE
login_method=sid_ee
subject_hash present
subject_hash != personal_code
```

## 22.4 Negative tests

```text
missing state → AUTHENTIGATE_MISSING_STATE
missing code → AUTHENTIGATE_MISSING_CODE
token 400 invalid_grant → AUTHENTIGATE_INVALID_GRANT
missing id_token → AUTHENTIGATE_MISSING_ID_TOKEN
invalid signature → AUTHENTIGATE_ID_TOKEN_VALIDATION_FAILED
missing personal_code → AUTHENTIGATE_MISSING_PERSONAL_CODE
missing country → AUTHENTIGATE_MISSING_PERSONAL_CODE_COUNTRY
country != EE → AUTHENTIGATE_COUNTRY_NOT_ALLOWED
acr not allowed → AUTHENTIGATE_METHOD_NOT_ALLOWED
```

---

# 23. Integration test plan

## 23.1 CI-safe tests

```text
test_authentigate_start_flow_builds_oidc_authorize_url
test_authentigate_pkce_generated_and_stored
test_authentigate_maps_id_token_claims
test_authentigate_rejects_missing_personal_code
test_authentigate_never_returns_raw_personal_code
test_registry_registers_authentigate
```

## 23.2 Live demo tests

Skip unless:

```env
AUTHENTIGATE_CLIENT_ID
AUTHENTIGATE_CLIENT_SECRET
AUTHENTIGATE_REDIRECT_URI
AUTHENTIGATE_ISSUER=https://oidc.demo.sk.ee
```

Manual/live test:

```text
start_flow returns redirect_url
redirect_url opens external browser/AuthSession
user authenticates with Smart-ID Q demo account
callback returns code + state
token exchange succeeds
id_token validates
/me returns eid_verified=true
story draft submit succeeds
```

---

# 24. Security constraints

## Mandatory

```text
state mandatory
nonce generated and validated
PKCE S256 generated and verified through code_verifier
ID token signature validation mandatory
issuer/audience/exp/iat validation mandatory
raw personal_code never logged
raw personal_code never returned from provider
verified_person_hash never exposed to frontend/GPT/blockchain
external browser/AuthSession only
```

## Not allowed

```text
No embedded WebView
No iframe
No raw personal_code persistence
No legal name/birthdate request in MVP
No direct Custom GPT → Authentigate
No using ID token without verification
```

---

# 25. Production readiness checklist

```text
[ ] Demo access received.
[ ] Demo client registered.
[ ] Redirect URI configured.
[ ] Allowed IPs configured.
[ ] Allowed countries includes EE.
[ ] Demo Smart-ID Q account tested.
[ ] Mobile-ID demo account tested if available.
[ ] ID-card tested if feasible.
[ ] Exact attributes JSON key confirmed in real ID token.
[ ] client_secret_basic confirmed or private_key_jwt implemented.
[ ] Starter plan confirmed.
[ ] Setup fee confirmed absent or acceptable.
[ ] Minimum contract term confirmed.
[ ] Production client registered.
[ ] Production redirect URI configured.
[ ] DOGESTONIA_EID_SECRET rotated for production.
[ ] Logs checked for no personal_code leakage.
```

---

# 26. Engineering decision record

```text
Decision:
Use Authentigate as the primary MVP eID provider for DOGEstonia.

Reason:
It supports Estonia Smart-ID, Mobile-ID, and ID-card through one OIDC gateway, provides demo environment, supports requesting personal_code and personal_code_country, returns signed ID token, and has public Starter pricing from €29/month.

Provider type:
OIDC adapter.

MVP scopes:
openid
https://id.authentigate.eu/claims/personal_code
https://id.authentigate.eu/claims/personal_code_country

MVP ACR values:
sid_ee mid_ee idcard_ee

MVP client auth preference:
client_secret_basic, if enabled by SK.

Privacy rule:
Adapter must immediately hash personal_code into subject_hash and must never return/log/store raw personal_code.

Testing:
Use Authentigate Demo Plan and Smart-ID Qualified demo accounts.
```

---

## Финальный вывод

**Authentigate лучше всего стыкуется с текущей DOGEstonia architecture как primary MVP provider.** В отличие от eID Easy, он не требует обходных решений через `user_data`: он даёт нормальный OIDC flow, EE eID methods, `personal_code`/`personal_code_country` claims, demo environment, and one-gateway integration.

Главная осторожность: до реализации нужно получить demo access и подтвердить exact runtime details:

```text
1. exact attributes JSON key in id_token;
2. client_secret_basic availability;
3. allowed ACR values for our demo client;
4. Starter plan commercial conditions.
```

[1]: https://sk-eid.github.io/authentigate-documentation/api/overview.html "Overview :: Authentigate documentation"
[2]: https://sk-eid.github.io/authentigate-documentation/api/index.html "Specifications :: Authentigate documentation"
[3]: https://sk-eid.github.io/authentigate-documentation/demo.html "Testing :: Authentigate documentation"
[4]: https://sk-eid.github.io/authentigate-documentation/environments.html "Environments :: Authentigate documentation"
[5]: https://authentigate.eu/ "One integration. Most popular Baltic eIDs. Full compliance. - Authentigate"
[6]: https://sk-eid.github.io/authentigate-documentation/api/registration.html "Client Registration :: Authentigate documentation"