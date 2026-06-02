-- 20260525000002_create_eid_verification_sessions.sql
-- Tracks in-flight eID verification flows.

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
