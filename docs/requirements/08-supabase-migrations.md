# 08. Supabase Migrations — Data Model

> **Статус:** НЕ реализовано. SQL для выполнения в Supabase SQL editor или через migration runner.
> **Предусловие:** Supabase проект существует (URL и ключи есть в .env). Таблицы НЕ созданы.
> **Связь:** Файл 09 (JWT validation) и файл 11 (eID flow) зависят от этих таблиц.

---

## Структура миграций

```
supabase/migrations/
├── 20260525000001_create_profiles.sql
├── 20260525000002_create_eid_verification_sessions.sql
├── 20260525000003_create_eid_audit_events.sql
└── 20260526000001_eid_sessions_provider_abstraction.sql
```

Каждая миграция — отдельный файл. Применяются последовательно. **Operational set:** 4 миграции (3 таблицы + provider abstraction для `eid_verification_sessions`). Историческая `20260527000001_create_story_drafts.sql` — вне identity scope (DEPRECATED, см. EPIC-IDS-08 CLEANUP-01).

---

## Migration 1: `public.profiles`

```sql
-- 20260525000001_create_profiles.sql
-- DOGEstonia user profile: eid status, wallet placeholder, display info
-- auth.users is managed by Supabase Auth — never modify directly

CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    supabase_user_id UUID NOT NULL UNIQUE
        REFERENCES auth.users(id) ON DELETE CASCADE,

    display_name TEXT,
    avatar_url TEXT,

    -- eID verification status
    eid_verified BOOLEAN NOT NULL DEFAULT FALSE,
    verified_person_hash TEXT,       -- HMAC_SHA256 output; NEVER expose in API responses
    eid_provider TEXT,               -- "authentigate"
    eid_method TEXT,                 -- "smart_id" | "mobile_id" | "id_card"
    eid_country TEXT,                -- "EE" | "LV" | "LT"
    eid_verified_at TIMESTAMPTZ,

    -- Wallet placeholder (Post-MVP)
    wallet_address TEXT UNIQUE,
    wallet_linked_at TIMESTAMPTZ,
    wallet_signature_verified_at TIMESTAMPTZ,
    wallet_signature_scheme TEXT,    -- "eth_personal_sign" | future
    wallet_chain_id TEXT,            -- "1" (mainnet) | "137" (polygon) | future

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Invariant: when eid_verified=true, hash and timestamp MUST be present
    CONSTRAINT eid_consistency CHECK (
        (eid_verified = FALSE)
        OR (
            eid_verified = TRUE
            AND verified_person_hash IS NOT NULL
            AND eid_verified_at IS NOT NULL
        )
    )
);

-- Partial unique index: allows multiple NULL (unverified users),
-- enforces uniqueness when verified_person_hash is set.
-- This is the final enforcement layer for 1 eID = 1 account invariant.
CREATE UNIQUE INDEX IF NOT EXISTS unique_verified_person_hash
    ON public.profiles (verified_person_hash)
    WHERE verified_person_hash IS NOT NULL;

-- Auto-update updated_at on any row change
CREATE OR REPLACE FUNCTION update_profiles_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER profiles_updated_at
    BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION update_profiles_updated_at();

-- RLS: enable but service role bypasses all policies
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Policy: users can read their own profile
CREATE POLICY "profiles_select_own"
    ON public.profiles FOR SELECT
    USING (auth.uid() = supabase_user_id);

-- Policy: users can update their own non-sensitive fields (display_name, avatar_url)
-- eid_verified и verified_person_hash обновляет только server через service role
CREATE POLICY "profiles_update_own_display"
    ON public.profiles FOR UPDATE
    USING (auth.uid() = supabase_user_id)
    WITH CHECK (auth.uid() = supabase_user_id);

-- Service role bypasses RLS (default Supabase behaviour).
-- Identity-service always uses service role key for eID operations.
```

---

## Migration 2: `public.eid_verification_sessions`

```sql
-- 20260525000002_create_eid_verification_sessions.sql
-- Tracks in-flight eID verification flows.
-- Single-use: state is consumed or expired after first use.

CREATE TABLE IF NOT EXISTS public.eid_verification_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    supabase_user_id UUID NOT NULL
        REFERENCES auth.users(id) ON DELETE CASCADE,

    -- OIDC security parameters
    state TEXT NOT NULL UNIQUE,         -- CSRF token; binds /start to /callback
    nonce TEXT NOT NULL,                -- OIDC nonce; plaintext OK (short-lived, not identity)
    code_verifier_encrypted TEXT NOT NULL,
    -- AES-256-GCM encrypted code_verifier; key from CODE_VERIFIER_ENCRYPTION_KEY env
    -- MUST be deleted/unusable after session reaches consumed/failed/expired
    -- MUST NOT be logged
    code_verifier_hash TEXT NOT NULL,   -- SHA-256 of code_verifier; for debug/audit only

    -- Context for post-verification redirect
    return_context TEXT CHECK (
        return_context IN ('dashboard_verification', 'story_submission', 'custom_gpt_submit')
    ),
    return_url TEXT,                    -- Must be from approved allowlist (validated in /start)
    requested_action TEXT CHECK (
        requested_action IN ('eid:verify', 'stories:submit')
        -- stories:create / stories:draft do NOT require eID
    ),

    -- Session lifecycle
    status TEXT NOT NULL DEFAULT 'started'
        CHECK (status IN ('started', 'consumed', 'failed', 'expired')),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL     -- Computed as NOW() + interval '10 minutes' in /start
);

-- Index for callback lookup by state
CREATE INDEX IF NOT EXISTS eid_sessions_state_idx
    ON public.eid_verification_sessions (state)
    WHERE status = 'started';

-- Index for cleanup job
CREATE INDEX IF NOT EXISTS eid_sessions_expires_idx
    ON public.eid_verification_sessions (expires_at)
    WHERE status = 'started';

-- RLS: no direct user access; only service role
ALTER TABLE public.eid_verification_sessions ENABLE ROW LEVEL SECURITY;
-- No user-facing policies; service role bypasses RLS.
```

**Session state machine:**

```
started
  ├── → consumed  (callback processed successfully)
  ├── → failed    (token exchange failed)
  └── → expired   (callback arrived after expires_at, or background cleanup)

Rules:
- state is single-use: replay of same state → reject with invalid_or_consumed_state
- callback MUST fail if session.status != 'started'
- callback MUST fail if expires_at < now()
- after successful processing: UPDATE status = 'consumed'
- after failed token exchange: UPDATE status = 'failed'
- expired sessions cleaned up by background job (no user impact)
```

---

## Migration 3: `public.eid_audit_events`

```sql
-- 20260525000003_create_eid_audit_events.sql
-- Immutable audit log for eID verification events.
-- Privacy: MUST NOT contain raw personal_code, raw tokens, or legal identity data.

CREATE TABLE IF NOT EXISTS public.eid_audit_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    supabase_user_id UUID,              -- nullable: failure before user resolved
    event_type TEXT NOT NULL,           -- see event type list below
    provider TEXT,                      -- "authentigate" | "mock"
    method TEXT,                        -- "smart_id" | "mobile_id" | "id_card" | null
    success BOOLEAN NOT NULL,
    failure_reason TEXT,                -- error code only; no PII

    -- Request context (hashed for privacy)
    request_id TEXT,                    -- trace_id
    ip_hash TEXT,                       -- SHA-256 of IP; not raw IP
    user_agent_hash TEXT,               -- SHA-256 of User-Agent; not raw UA

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index for user history lookup
CREATE INDEX IF NOT EXISTS eid_audit_user_idx
    ON public.eid_audit_events (supabase_user_id, created_at DESC)
    WHERE supabase_user_id IS NOT NULL;

-- Index for monitoring/analytics
CREATE INDEX IF NOT EXISTS eid_audit_event_type_idx
    ON public.eid_audit_events (event_type, created_at DESC);

-- RLS: no direct user access; only service role and admin queries
ALTER TABLE public.eid_audit_events ENABLE ROW LEVEL SECURITY;
```

**Обязательные event_type значения:**

```
eid_verification_started
eid_verification_success
eid_verification_failed
eid_already_verified
eid_identity_conflict
eid_session_expired
eid_state_replay_rejected
eid_return_url_rejected
story_submit_blocked_unverified
story_submit_success
story_draft_created
story_draft_submitted
gpt_submit_blocked_unverified
gpt_submit_success
oauth_code_issued
oauth_token_issued
oauth_token_invalid
```

---

## Migration 4: provider abstraction (`eid_verification_sessions`)

```sql
-- 20260526000001_eid_sessions_provider_abstraction.sql
-- Provider abstraction columns for eid_verification_sessions (req-17).

ALTER TABLE public.eid_verification_sessions
    ADD COLUMN IF NOT EXISTS provider TEXT NOT NULL DEFAULT 'eideasy';

ALTER TABLE public.eid_verification_sessions
    ADD COLUMN IF NOT EXISTS provider_session_data JSONB NOT NULL DEFAULT '{}';

ALTER TABLE public.eid_verification_sessions
    ALTER COLUMN nonce DROP NOT NULL;

ALTER TABLE public.eid_verification_sessions
    ALTER COLUMN code_verifier_encrypted DROP NOT NULL;

ALTER TABLE public.eid_verification_sessions
    ALTER COLUMN code_verifier_hash DROP NOT NULL;

CREATE INDEX IF NOT EXISTS idx_eid_sessions_provider
    ON public.eid_verification_sessions (provider);
```

Не создаёт новую таблицу; расширяет Migration 2. См. [req-17](17-eid-provider-abstraction.md).

---

## Применение миграций

### Через Supabase SQL editor (ручной способ)

```
Supabase Dashboard → SQL Editor → выполнить каждый файл последовательно
```

### Через supabase CLI (рекомендуется)

```bash
# Установить supabase CLI
brew install supabase/tap/supabase

# Link с проектом
supabase link --project-ref <project-ref>

# Применить миграции
supabase db push
```

### Через psycopg (programmatic)

```python
import psycopg

with psycopg.connect(config.database_url) as conn:
    with open("supabase/migrations/20260525000001_create_profiles.sql") as f:
        conn.execute(f.read())
    conn.commit()
```

---

## Readiness check (паттерн из complaints-gateway)

Identity-service при старте проверяет наличие таблиц:

```python
def required_tables_ready(conn) -> bool:
    result = conn.execute("""
        SELECT COUNT(*) FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name IN ('profiles', 'eid_verification_sessions', 'eid_audit_events')
    """).fetchone()
    return result[0] == 3
```

Если таблицы отсутствуют — `GET /ready` возвращает `{"status": "degraded", "reason": "missing_tables"}`.
