-- 20260624000002_oauth_authorization_request_context.sql
-- Relay requested_action + return_context on OAuth handshake (EPIC-IDS-11 OAUTH-04).

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
