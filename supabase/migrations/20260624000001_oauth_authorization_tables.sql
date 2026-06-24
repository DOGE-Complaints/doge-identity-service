-- 20260624000001_oauth_authorization_tables.sql
-- Durable OAuth handshake + authorization codes (EPIC-IDS-11 OAUTH-03).

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
