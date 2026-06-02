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
