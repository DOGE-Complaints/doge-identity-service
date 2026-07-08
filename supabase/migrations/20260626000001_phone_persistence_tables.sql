-- 20260626000001_phone_persistence_tables.sql
-- Durable phone verification sessions + audit (EPIC-IDS-10 PV-09).

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
