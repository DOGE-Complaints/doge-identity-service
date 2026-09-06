# DOGEstonia Identity Service

**Identity, verification and authorization infrastructure for DOGEstonia**

DOGEstonia Identity Service provides the identity boundary shared by DOGEstonia applications and backend services.

It resolves authenticated sessions into a consistent user identity, maintains verification state, supports phone and electronic-ID verification, and provides OAuth-based authorization for trusted external clients.

The service is designed so that civic and application services do not have to implement identity, verification or authentication-provider logic independently.

---

## What this service does

The current runtime provides:

* authenticated user identity resolution;
* a canonical `/me` identity profile;
* Supabase access-token validation;
* email, phone and eID verification state;
* phone OTP verification;
* configurable SMS delivery providers;
* configurable electronic-ID providers;
* OAuth 2.0 authorization flows;
* signed OAuth access tokens;
* OAuth token introspection;
* service-to-service authentication;
* identity persistence through Supabase/PostgreSQL;
* in-memory persistence for local development and tests;
* rate limiting for sensitive authentication operations;
* audit-safe request identifiers and hashing;
* safe return-URL handling;
* health, readiness and runtime diagnostics.

---

## Role in DOGEstonia

Identity is intentionally separated from civic application logic.

```text
                   ┌────────────────────┐
                   │      User / SPA    │
                   └─────────┬──────────┘
                             │
                    authenticated session
                             │
                             ▼
                ┌───────────────────────────┐
                │  DOGEstonia Identity     │
                │          Service          │
                │                           │
                │ identity                  │
                │ verification              │
                │ authorization             │
                └─────────────┬─────────────┘
                              │
              ┌───────────────┼────────────────┐
              │               │                │
              ▼               ▼                ▼
      Phone verification     eID          OAuth clients
              │           providers            │
              │                                │
              └───────────────┬────────────────┘
                              │
                              ▼
                Canonical DOGEstonia identity
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
          Civic services            Other trusted
          / gateways                  services
```

Instead of every DOGEstonia component independently deciding whether a user is verified or who a Bearer token belongs to, those decisions are centralized behind this service.

---

## Identity profile

Authenticated applications can resolve the current user through:

```http
GET /me
```

The current identity response includes fields such as:

```json
{
  "supabase_user_id": "...",
  "email": "...",
  "email_verified": true,

  "role": "...",
  "display_name": null,
  "avatar_url": null,

  "eid_verified": false,
  "eid_provider": null,
  "eid_method": null,
  "eid_country": null,
  "eid_verified_at": null,

  "phone_verified": false,
  "phone_provider": null,
  "phone_dial_prefix": null,
  "phone_verified_at": null,

  "created_at": null,
  "account_status": "active"
}
```

This gives downstream services a stable identity contract without requiring them to understand individual authentication or verification providers.

---

## Authentication boundary

User-facing protected routes consume Bearer access tokens.

The current runtime validates Supabase-authenticated users and converts the authenticated session into internal `UserClaims` used by the application.

This separates:

```text
authentication provider
        │
        ▼
token validation
        │
        ▼
DOGEstonia UserClaims
        │
        ▼
identity profile / verification state
```

from the business logic of downstream services.

---

# Phone verification

The service implements provider-independent phone verification using one-time passwords.

## Flow

```text
Authenticated user
       │
       ▼
POST /auth/phone/request
       │
       ▼
Phone validation
       │
       ▼
OTP generation
       │
       ▼
Configured SMS provider
       │
       ▼
User receives code
       │
       ▼
POST /auth/phone/confirm
       │
       ▼
Verification state updated
```

The runtime supports configuration for:

* allowed E.164 dial prefixes;
* OTP length;
* OTP lifetime;
* maximum confirmation attempts;
* resend cooldown;
* one-account-per-phone-number enforcement.

Example:

```env
PHONE_ALLOWED_DIAL_PREFIXES=+372
PHONE_CODE_LENGTH=6
PHONE_CODE_TTL_S=300
PHONE_MAX_ATTEMPTS=5
PHONE_RESEND_COOLDOWN_S=60
PHONE_ONE_ACCOUNT_PER_NUMBER=true
```

---

## SMS providers

Phone delivery is implemented behind a provider abstraction.

The current codebase includes support for:

* `mock`
* `file`
* `telnyx`
* `smspm`

Select the active provider through:

```env
SMS_PROVIDER=mock
```

### Mock provider

Useful for automated tests and isolated development.

### File sink

```env
SMS_PROVIDER=file
FILE_SMS_OUTBOX_DIR=var/sms-outbox
```

Writes development SMS output to disk.

This mode is intended for development only because OTP values may be visible in plaintext.

### Telnyx

```env
SMS_PROVIDER=telnyx

TELNYX_API_KEY=
TELNYX_FROM=DOGEstonia
TELNYX_MESSAGING_PROFILE_ID=
```

Delivery status can be received through:

```http
POST /webhooks/telnyx/messaging
```

### SMSPM

```env
SMS_PROVIDER=smspm

SMSPM_HASH=
SMSPM_TOKEN=
SMSPM_FROM=
```

Delivery reports are supported through:

```http
GET /webhooks/smspm/delivery/{shared_secret}
```

Provider-specific details remain outside the core OTP domain logic.

---

# Electronic identity verification

The identity service also contains an extensible eID verification layer.

The active provider is configured with:

```env
EID_PROVIDER=...
```

Current provider implementations include:

* mock eID;
* Authentigate;
* eID Easy.

The provider registry keeps provider-specific protocols outside the core identity lifecycle.

---

## eID verification flow

An authenticated user begins verification through:

```http
POST /auth/eid/start
```

The service creates the verification context and delegates authentication to the configured provider.

The provider later returns through:

```http
GET /auth/{provider}/callback
```

The callback is validated and translated back into DOGEstonia verification state.

Conceptually:

```text
DOGEstonia user
      │
      ▼
 /auth/eid/start
      │
      ▼
eID provider adapter
      │
      ▼
external identity flow
      │
      ▼
provider callback
      │
      ▼
validated identity result
      │
      ▼
DOGEstonia identity profile
```

---

## Authentigate

The current runtime contains an OIDC-based Authentigate integration.

Configuration includes:

```env
AUTHENTIGATE_ISSUER=
AUTHENTIGATE_DISCOVERY_URL=
AUTHENTIGATE_CLIENT_ID=
AUTHENTIGATE_CLIENT_SECRET=
AUTHENTIGATE_REDIRECT_URI=
AUTHENTIGATE_SCOPES=
AUTHENTIGATE_ACR_VALUES=
AUTHENTIGATE_UI_LOCALES=
AUTHENTIGATE_COUNTRY=
```

The service includes OIDC/JWT security infrastructure rather than delegating provider responses directly to application code.

---

## eID Easy

An eID Easy provider adapter is also present.

Example configuration:

```env
EID_PROVIDER=eideasy

EIDEASY_ENV=test
EIDEASY_BASE_URL=https://test.eideasy.com
EIDEASY_CLIENT_ID=
EIDEASY_CLIENT_SECRET=
EIDEASY_REDIRECT_URI=http://localhost:8100/auth/eideasy/callback
EIDEASY_ALLOWED_METHODS=smartid,mid-login,ee-id-login
EIDEASY_DEFAULT_COUNTRY=EE
EIDEASY_ALLOWED_COUNTRIES=EE
```

Provider selection is therefore a runtime concern rather than a hard-coded dependency of the identity domain.

---

# OAuth authorization server

The service implements an OAuth authorization boundary for trusted external clients.

The current API includes:

```http
GET  /oauth/authorize
POST /oauth/authorize/complete
POST /oauth/token
POST /oauth/introspect
```

The codebase contains dedicated components for:

* authorization requests;
* authorization completion;
* authorization-code exchange;
* client-secret validation;
* OAuth scopes;
* signed access-token JWTs;
* token introspection;
* verification requirements;
* SPA login context.

---

## OAuth flow

```text
External client
      │
      ▼
GET /oauth/authorize
      │
      ▼
DOGEstonia authentication
      │
      ▼
POST /oauth/authorize/complete
      │
      ▼
authorization code
      │
      ▼
POST /oauth/token
      │
      ▼
signed access token
      │
      ▼
DOGEstonia APIs
```

A trusted backend can validate an OAuth access token through:

```http
POST /oauth/introspect
```

The introspection endpoint itself is protected by service-to-service authentication.

---

## Current OAuth deployment profile

The current environment template includes an OAuth client profile intended for DOGEstonia integrations with a Custom GPT / external assistant client.

Example configuration:

```env
GPT_OAUTH_CLIENT_ID=openai-custom-gpt
GPT_OAUTH_CLIENT_SECRET=
GPT_OAUTH_REDIRECT_URI=https://oauth.pstmn.io/v1/callback
```

This is a deployment configuration of the existing OAuth infrastructure rather than the complete purpose of the identity service.

---

# Service-to-service trust

Some operations are not user-authenticated browser operations.

For trusted backend calls, the service exposes a separate service credential boundary.

Example:

```env
SERVICE_API_TOKEN=
```

This credential is used for server-to-server trust, including OAuth token introspection.

User Bearer tokens and service credentials are deliberately separate security concepts.

---

# Security model

Identity infrastructure is security-sensitive, so the runtime contains several controls outside the normal application flow.

Current mechanisms include:

* JWT validation;
* OIDC validation support;
* service-token authentication;
* configurable CORS;
* authentication-specific rate limiting;
* safe redirect / return-URL validation;
* HMAC-based identity hashing utilities;
* encrypted eID session material;
* audit-safe request context;
* trace IDs;
* generic internal-error envelopes;
* provider webhook validation infrastructure.

---

## Rate limiting

Sensitive authentication entry points are protected by dedicated rate-limit dependencies.

These currently include:

* phone OTP requests;
* eID start requests;
* eID provider callbacks.

A rate-limit violation returns:

```http
HTTP 429 Too Many Requests
Retry-After: ...
```

This provides a common abuse-control boundary before provider-specific work occurs.

---

## Audit-safe request context

Security-sensitive operations can derive hashed audit identifiers from incoming requests rather than propagating raw request metadata throughout the application.

This helps keep security observability separate from business-domain identity data.

---

## Return URL safety

Authentication flows frequently redirect users back to another application.

Return destinations therefore pass through explicit validation rather than being blindly trusted from request input.

Allowed destinations are deployment-configurable.

```env
ALLOWED_RETURN_URLS=
```

---

# API overview

## Runtime

| Method | Endpoint  | Purpose                            |
| ------ | --------- | ---------------------------------- |
| `GET`  | `/health` | Service health                     |
| `GET`  | `/ready`  | Dependency / persistence readiness |

## Identity

| Method | Endpoint | Purpose                             |
| ------ | -------- | ----------------------------------- |
| `GET`  | `/me`    | Resolve current DOGEstonia identity |

## Electronic identity

| Method | Endpoint                    | Purpose                     |
| ------ | --------------------------- | --------------------------- |
| `POST` | `/auth/eid/start`           | Begin eID verification      |
| `GET`  | `/auth/{provider}/callback` | Receive eID provider result |

## Phone verification

| Method | Endpoint              | Purpose     |
| ------ | --------------------- | ----------- |
| `POST` | `/auth/phone/request` | Request OTP |
| `POST` | `/auth/phone/confirm` | Confirm OTP |

## Provider webhooks

| Method | Endpoint                                   | Purpose                   |
| ------ | ------------------------------------------ | ------------------------- |
| `POST` | `/webhooks/telnyx/messaging`               | Telnyx messaging callback |
| `GET`  | `/webhooks/smspm/delivery/{shared_secret}` | SMSPM delivery callback   |

## OAuth

| Method | Endpoint                    | Purpose                               |
| ------ | --------------------------- | ------------------------------------- |
| `GET`  | `/oauth/authorize`          | Start OAuth authorization             |
| `POST` | `/oauth/authorize/complete` | Complete authorization                |
| `POST` | `/oauth/token`              | Exchange authorization code for token |
| `POST` | `/oauth/introspect`         | Introspect an access token            |

FastAPI also exposes generated OpenAPI documentation when the server is running.

---

# Persistence

The current service supports two persistence modes.

## In-memory

```env
DB_BACKEND=in_memory
```

Used for:

* local development;
* unit/integration tests;
* isolated identity flows.

Data is not durable.

---

## Supabase / PostgreSQL

```env
DB_BACKEND=supabase

SUPABASE_URL=
SUPABASE_SERVICE_ROLE=
```

The Supabase implementation persists identity-domain state and repositories behind infrastructure abstractions.

A direct PostgreSQL connection can also be configured for operational tooling:

```env
DATABASE_URL=postgresql://...
```

Server-side Supabase service credentials must never be exposed to browser applications.

---

# Architecture

The service separates HTTP, identity-domain logic, provider integrations and persistence.

```text
┌─────────────────────────────────────────┐
│                API Layer                │
│                                         │
│ FastAPI                                 │
│ auth dependencies                       │
│ rate limits                             │
│ request / response envelopes            │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│          Identity Application           │
│                                         │
│ profile resolution                      │
│ verification orchestration              │
│ service construction                    │
└──────────────┬──────────────┬───────────┘
               │              │
       ┌───────▼───────┐ ┌────▼──────────┐
       │ Phone / OTP   │ │ eID Providers │
       │               │ │               │
       │ mock          │ │ mock          │
       │ file          │ │ Authentigate  │
       │ Telnyx        │ │ eID Easy      │
       │ SMSPM         │ │               │
       └───────┬───────┘ └────┬──────────┘
               │              │
               └───────┬──────┘
                       │
             ┌─────────▼──────────┐
             │   Identity Domain  │
             └─────────┬──────────┘
                       │
             ┌─────────▼──────────┐
             │   Infrastructure   │
             │                    │
             │ in-memory stores   │
             │ Supabase           │
             │ external providers │
             └────────────────────┘
```

OAuth forms another authorization boundary over the same identity foundation:

```text
Identity
   │
   ▼
OAuth authorization
   │
   ▼
authorization code
   │
   ▼
signed access token
   │
   ▼
trusted external client
```

---

# Source structure

```text
src/core/
├── api/              # FastAPI routes, handlers, request security
├── application/      # dependency and service construction
├── auth/             # authenticated-session/JWT validation
├── config/           # application configuration
├── domain/           # identity domain models and contracts
├── infrastructure/   # repositories and Supabase persistence
├── oauth/            # OAuth authorization server
├── phone/            # OTP engine and SMS provider abstraction
├── providers/        # electronic-ID providers
├── security/         # rate limits, hashing, OIDC, redirect safety
└── logging_setup.py
```

Provider implementations are intentionally isolated below their corresponding abstractions.

---

# Tech stack

The current service uses:

* **Python 3.11+**
* **FastAPI**
* **Uvicorn**
* **Supabase / PostgreSQL**
* **psycopg**
* **HTTPX**
* **JOSE RFC**
* **Cryptography**
* **pytest**

---

# Local development

## 1. Clone

```bash
git clone https://github.com/DOGE-Complaints/doge-identity-service.git
cd doge-identity-service
git checkout dev
```

## 2. Create a Python environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

## 3. Install

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## 4. Configure

```bash
cp .env.example .env
```

For a minimal local environment:

```env
APP_PROFILE=demo
PORT=8100

DB_BACKEND=in_memory
EID_PROVIDER=mock
SMS_PROVIDER=mock
```

Do not commit real credentials.

---

# Running the service

Using the Makefile:

```bash
make serve
```

Development mode with reload:

```bash
make dev
```

Or directly:

```bash
python -m uvicorn \
  --app-dir src \
  core.api.asgi_app:app \
  --host 127.0.0.1 \
  --port 8100
```

The API is then available at:

```text
http://localhost:8100
```

Health:

```bash
curl http://localhost:8100/health
```

Readiness:

```bash
curl http://localhost:8100/ready
```

---

# Tests

Run the offline suite:

```bash
make test
```

Equivalent command:

```bash
python -m pytest tests/ -q -m "not live_integration"
```

The project defines additional test categories for:

* `live_integration` — live Supabase integration;
* `mock_oidc` — tests against a local mock OIDC provider;
* `smoke` — tests against a running identity service.

Live integration:

```bash
make test-live
```

Smoke testing:

```bash
make smoke
```

Against another deployed environment:

```bash
make smoke IDENTITY_URL=https://<identity-service>
```

---

# CI

GitHub Actions separates:

* offline tests;
* live integration tests.

This keeps ordinary pull-request validation independent of production-like external services while still allowing real Supabase integration to be validated separately.

---

# Deployment

The repository contains Railpack and Railway deployment configuration.

The runtime entry point is:

```bash
python -m uvicorn \
  --app-dir src \
  core.api.asgi_app:app \
  --host 0.0.0.0 \
  --port ${PORT:-8100}
```

Provider credentials, identity secrets and database credentials are supplied through environment variables.

They must not be committed to the repository.

---

# Configuration domains

The environment is intentionally divided by responsibility.

```text
Application
├── deployment / logging
├── persistence
├── Supabase
├── user authentication
│
├── eID
│   ├── provider selection
│   ├── Authentigate
│   └── eID Easy
│
├── phone verification
│   ├── OTP policy
│   ├── Telnyx
│   └── SMSPM
│
├── identity secrets
├── OAuth
├── service trust
├── CORS
└── return URL policy
```

See [`.env.example`](./.env.example) for the complete runtime configuration contract.

---

# What this repository does not own

This service provides DOGEstonia identity and authorization infrastructure.

It does **not** own:

* civic-story intake;
* story clustering;
* issue creation;
* municipal workflows;
* application-specific business rules;
* the complete DOGEstonia frontend;
* blockchain tokenization or voting.

Those responsibilities belong to other DOGEstonia components.

The identity service provides them with a stable answer to a different set of questions:

```text
Who is this user?

Is the session valid?

Which identity attributes are known?

Which verification steps have been completed?

May this external client receive delegated access?

Can this backend trust the supplied token?
```

---

# Development status

This repository is under active development.

The `dev` branch contains the working identity runtime.

The existing implementation is significantly beyond the original scaffold state and currently includes user identity resolution, phone verification, eID provider adapters, OAuth authorization, security controls and persistent storage integrations.

Interfaces and provider support may continue to evolve as DOGEstonia's federated node architecture develops.

---

# Documentation

Operational notes, implementation audits and security analysis are stored under:

```text
docs/
```

The repository contains detailed audit material for identity, eID, phone verification, OAuth and security work.

For current runtime behaviour, source code in `dev` is authoritative.

---

# DOGEstonia

DOGEstonia is building civic infrastructure in which applications can share identity and verification capabilities without embedding those concerns into every civic workflow.

This repository implements that identity boundary.

It is responsible for turning authentication-provider sessions and verification events into a consistent identity contract that other DOGEstonia services can trust.

---

# License

Apache License 2.0.

See [`LICENSE`](./LICENSE).
