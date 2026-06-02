-- 20260525000003_create_eid_audit_events.sql
-- Immutable audit log for eID verification events.

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
