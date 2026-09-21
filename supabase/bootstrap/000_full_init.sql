-- =============================================================================
-- doge-identity-service — full database bootstrap (create from scratch)
-- =============================================================================
-- Назначение: один скрипт, поднимающий identity-схему с нуля на чистом
-- Supabase-проекте. Эквивалентен последовательному применению миграций
-- из supabase/migrations/ в порядке имён.
--
-- Источник (склейка строго из существующих миграций, без новых DDL):
--   1) 20260525000001_create_profiles.sql
--   2) 20260525000002_create_eid_verification_sessions.sql
--   3) 20260525000003_create_eid_audit_events.sql
--   4) 20260526000001_eid_sessions_provider_abstraction.sql   (ALTER к #2)
--   5) 20260611000001_profiles_phone_verification.sql
--   6) 20260624000001_oauth_authorization_tables.sql
--   7) 20260624000002_oauth_authorization_request_context.sql
--   8) 20260626000001_phone_persistence_tables.sql
--
-- НАМЕРЕННО ИСКЛЮЧЕНО: 20260527000001_create_story_drafts.sql
--   Причина: контент историй — домен doge-complaints-gateway, не identity.
--   Решение оператора (2026-06-04). Подробности и последствия (healthcheck
--   `_REQUIRED_TABLES` всё ещё ждёт story_drafts → /ready=503) описаны в
--   docs/analysis/epic-ids-05-scope-validation-2026-06-03.md и
--   docs/analysis/gap-analysis-full-2026-06-04.md.
--
-- Предусловие: расширение для gen_random_uuid() (в Supabase доступно из коробки;
-- на чистом Postgres — CREATE EXTENSION IF NOT EXISTS pgcrypto;).
-- auth.users управляется Supabase Auth — здесь не создаётся, только FK.
-- =============================================================================


-- =============================================================================
-- [1/4] public.profiles
-- источник: supabase/migrations/20260525000001_create_profiles.sql
-- DOGEstonia user profile: eid status, wallet placeholder, display info
-- =============================================================================

CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    supabase_user_id UUID NOT NULL UNIQUE
        REFERENCES auth.users(id) ON DELETE CASCADE,

    display_name TEXT,
    avatar_url TEXT,

    -- eID verification status
    eid_verified BOOLEAN NOT NULL DEFAULT FALSE,
    verified_person_hash TEXT,
    eid_provider TEXT,
    eid_method TEXT,
    eid_country TEXT,
    eid_verified_at TIMESTAMPTZ,

    -- Wallet placeholder (Post-MVP)
    wallet_address TEXT UNIQUE,
    wallet_linked_at TIMESTAMPTZ,
    wallet_signature_verified_at TIMESTAMPTZ,
    wallet_signature_scheme TEXT,
    wallet_chain_id TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT eid_consistency CHECK (
        (eid_verified = FALSE)
        OR (
            eid_verified = TRUE
            AND verified_person_hash IS NOT NULL
            AND eid_verified_at IS NOT NULL
        )
    )
);

CREATE UNIQUE INDEX IF NOT EXISTS unique_verified_person_hash
    ON public.profiles (verified_person_hash)
    WHERE verified_person_hash IS NOT NULL;

CREATE OR REPLACE FUNCTION update_profiles_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS profiles_updated_at ON public.profiles;
CREATE TRIGGER profiles_updated_at
    BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION update_profiles_updated_at();

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS profiles_select_own ON public.profiles;
CREATE POLICY profiles_select_own
    ON public.profiles FOR SELECT
    USING (auth.uid() = supabase_user_id);

DROP POLICY IF EXISTS profiles_update_own_display ON public.profiles;
CREATE POLICY profiles_update_own_display
    ON public.profiles FOR UPDATE
    USING (auth.uid() = supabase_user_id)
    WITH CHECK (auth.uid() = supabase_user_id);

DROP POLICY IF EXISTS profiles_service_role_all ON public.profiles;
CREATE POLICY profiles_service_role_all
    ON public.profiles FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);


-- =============================================================================
-- [2/4] public.eid_verification_sessions (base)
-- источник: supabase/migrations/20260525000002_create_eid_verification_sessions.sql
-- Tracks in-flight eID verification flows.
-- ПРИМЕЧАНИЕ: колонки nonce/code_verifier_* создаются NOT NULL здесь и
-- ослабляются блоком [4/4] (provider abstraction). Порядок сохранён намеренно.
-- =============================================================================

CREATE TABLE IF NOT EXISTS public.eid_verification_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    supabase_user_id UUID NOT NULL
        REFERENCES auth.users(id) ON DELETE CASCADE,

    state TEXT NOT NULL UNIQUE,
    nonce TEXT NOT NULL,
    code_verifier_encrypted TEXT NOT NULL,
    code_verifier_hash TEXT NOT NULL,

    return_context TEXT CHECK (
        return_context IN ('dashboard_verification', 'story_submission', 'custom_gpt_submit')
    ),
    return_url TEXT,
    requested_action TEXT CHECK (
        requested_action IN ('eid:verify', 'stories:submit')
    ),

    status TEXT NOT NULL DEFAULT 'started'
        CHECK (status IN ('started', 'consumed', 'failed', 'expired')),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS eid_sessions_state_idx
    ON public.eid_verification_sessions (state)
    WHERE status = 'started';

CREATE INDEX IF NOT EXISTS eid_sessions_expires_idx
    ON public.eid_verification_sessions (expires_at)
    WHERE status = 'started';

ALTER TABLE public.eid_verification_sessions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS eid_verification_sessions_service_role_all ON public.eid_verification_sessions;
CREATE POLICY eid_verification_sessions_service_role_all
    ON public.eid_verification_sessions FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);


-- =============================================================================
-- [3/4] public.eid_audit_events
-- источник: supabase/migrations/20260525000003_create_eid_audit_events.sql
-- Immutable audit log for eID verification events.
-- =============================================================================

CREATE TABLE IF NOT EXISTS public.eid_audit_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    supabase_user_id UUID,
    event_type TEXT NOT NULL,
    provider TEXT,
    method TEXT,
    success BOOLEAN NOT NULL,
    failure_reason TEXT,

    request_id TEXT,
    ip_hash TEXT,
    user_agent_hash TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS eid_audit_user_idx
    ON public.eid_audit_events (supabase_user_id, created_at DESC)
    WHERE supabase_user_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS eid_audit_event_type_idx
    ON public.eid_audit_events (event_type, created_at DESC);

ALTER TABLE public.eid_audit_events ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS eid_audit_events_service_role_all ON public.eid_audit_events;
CREATE POLICY eid_audit_events_service_role_all
    ON public.eid_audit_events FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);


-- =============================================================================
-- [4/4] eid_verification_sessions — provider abstraction (req-17)
-- источник: supabase/migrations/20260526000001_eid_sessions_provider_abstraction.sql
-- Добавляет provider/provider_session_data и снимает NOT NULL с PKCE-полей.
-- =============================================================================

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


-- =============================================================================
-- [5/8] public.profiles — phone verification columns
-- источник: supabase/migrations/20260611000001_profiles_phone_verification.sql
-- =============================================================================

ALTER TABLE public.profiles
    ADD COLUMN IF NOT EXISTS phone_verified BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS verified_phone_hash TEXT,
    ADD COLUMN IF NOT EXISTS phone_provider TEXT,
    ADD COLUMN IF NOT EXISTS phone_dial_prefix TEXT,
    ADD COLUMN IF NOT EXISTS phone_verified_at TIMESTAMPTZ;

CREATE UNIQUE INDEX IF NOT EXISTS unique_verified_phone_hash
    ON public.profiles (verified_phone_hash)
    WHERE verified_phone_hash IS NOT NULL;

ALTER TABLE public.profiles
    DROP CONSTRAINT IF EXISTS phone_consistency;

ALTER TABLE public.profiles
    ADD CONSTRAINT phone_consistency CHECK (
        (phone_verified = FALSE)
        OR (
            phone_verified = TRUE
            AND verified_phone_hash IS NOT NULL
            AND phone_verified_at IS NOT NULL
        )
    );


-- =============================================================================
-- [5b] public.profiles — identity_verified (method-opaque)
-- источник: supabase/migrations/20260921000001_profiles_identity_verified.sql
-- backfill: supabase/migrations/20260921000002_profiles_identity_verified_backfill.sql
-- =============================================================================

ALTER TABLE public.profiles
    ADD COLUMN IF NOT EXISTS identity_verified BOOLEAN NOT NULL DEFAULT FALSE;

UPDATE public.profiles
SET identity_verified = TRUE
WHERE phone_verified = TRUE
   OR eid_verified = TRUE;


-- =============================================================================
-- [6/8] OAuth authorization tables
-- источник: supabase/migrations/20260624000001_oauth_authorization_tables.sql
-- =============================================================================

CREATE TABLE IF NOT EXISTS public.oauth_authorization_requests (
    oauth_request_id TEXT PRIMARY KEY,

    client_id TEXT NOT NULL,
    redirect_uri TEXT NOT NULL,
    scopes JSONB NOT NULL DEFAULT '[]'::jsonb,
    code_challenge TEXT,
    code_challenge_method TEXT,
    state TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS oauth_authorization_requests_expires_idx
    ON public.oauth_authorization_requests (expires_at);

CREATE TABLE IF NOT EXISTS public.oauth_authorization_codes (
    code TEXT PRIMARY KEY,

    request_id TEXT
        REFERENCES public.oauth_authorization_requests (oauth_request_id) ON DELETE SET NULL,

    supabase_user_id UUID NOT NULL
        REFERENCES auth.users(id) ON DELETE CASCADE,

    client_id TEXT NOT NULL,
    redirect_uri TEXT NOT NULL,
    scopes JSONB NOT NULL DEFAULT '[]'::jsonb,
    code_challenge TEXT,
    code_challenge_method TEXT,

    expires_at TIMESTAMPTZ NOT NULL,
    consumed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS oauth_authorization_codes_expires_idx
    ON public.oauth_authorization_codes (expires_at)
    WHERE consumed = FALSE;

ALTER TABLE public.oauth_authorization_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.oauth_authorization_codes ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS oauth_authorization_requests_service_role_all ON public.oauth_authorization_requests;
CREATE POLICY oauth_authorization_requests_service_role_all
    ON public.oauth_authorization_requests FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

DROP POLICY IF EXISTS oauth_authorization_codes_service_role_all ON public.oauth_authorization_codes;
CREATE POLICY oauth_authorization_codes_service_role_all
    ON public.oauth_authorization_codes FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);


-- =============================================================================
-- [7/8] OAuth authorization request context
-- источник: supabase/migrations/20260624000002_oauth_authorization_request_context.sql
-- =============================================================================

ALTER TABLE public.oauth_authorization_requests
    ADD COLUMN IF NOT EXISTS requested_action TEXT,
    ADD COLUMN IF NOT EXISTS return_context TEXT;

ALTER TABLE public.oauth_authorization_requests
    DROP CONSTRAINT IF EXISTS oauth_authorization_requests_requested_action_check;

ALTER TABLE public.oauth_authorization_requests
    ADD CONSTRAINT oauth_authorization_requests_requested_action_check
    CHECK (
        requested_action IS NULL
        OR requested_action IN ('eid:verify', 'stories:submit')
    );


-- =============================================================================
-- [8/8] phone persistence tables
-- источник: supabase/migrations/20260626000001_phone_persistence_tables.sql
-- =============================================================================

CREATE TABLE IF NOT EXISTS public.phone_verification_sessions (
    id UUID PRIMARY KEY,

    supabase_user_id UUID NOT NULL
        REFERENCES auth.users(id) ON DELETE CASCADE,

    phone_hash TEXT NOT NULL,
    dial_prefix TEXT NOT NULL,
    code_hash TEXT NOT NULL,

    status TEXT NOT NULL DEFAULT 'started'
        CHECK (status IN ('started', 'consumed', 'failed', 'expired')),

    attempts INTEGER NOT NULL DEFAULT 0,

    provider TEXT NOT NULL,
    provider_message_id TEXT,
    delivery_status TEXT,
    delivery_updated_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS phone_verification_sessions_user_idx
    ON public.phone_verification_sessions (supabase_user_id, created_at DESC);

CREATE INDEX IF NOT EXISTS phone_verification_sessions_expires_idx
    ON public.phone_verification_sessions (expires_at)
    WHERE status = 'started';

CREATE INDEX IF NOT EXISTS phone_verification_sessions_provider_message_idx
    ON public.phone_verification_sessions (provider_message_id)
    WHERE provider_message_id IS NOT NULL;

CREATE TABLE IF NOT EXISTS public.phone_audit_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    supabase_user_id UUID,
    event_type TEXT NOT NULL,
    provider TEXT,
    success BOOLEAN NOT NULL,
    failure_reason TEXT,

    request_id TEXT,
    ip_hash TEXT,
    user_agent_hash TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS phone_audit_user_idx
    ON public.phone_audit_events (supabase_user_id, created_at DESC)
    WHERE supabase_user_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS phone_audit_event_type_idx
    ON public.phone_audit_events (event_type, created_at DESC);

CREATE INDEX IF NOT EXISTS phone_audit_created_at_idx
    ON public.phone_audit_events (created_at DESC);

ALTER TABLE public.phone_verification_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.phone_audit_events ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS phone_verification_sessions_service_role_all ON public.phone_verification_sessions;
CREATE POLICY phone_verification_sessions_service_role_all
    ON public.phone_verification_sessions FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

DROP POLICY IF EXISTS phone_audit_events_service_role_all ON public.phone_audit_events;
CREATE POLICY phone_audit_events_service_role_all
    ON public.phone_audit_events FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);


-- =============================================================================
-- Итог: profiles, eid_verification_sessions, eid_audit_events, oauth_* ,
-- phone_verification_sessions, phone_audit_events (+ phone profile columns).
-- story_drafts намеренно отсутствует (см. шапку). Если фича story-drafts будет
-- признана нужной в identity — добавить отдельным блоком из соответствующей
-- миграции и снять её из gap-листа.
-- =============================================================================
