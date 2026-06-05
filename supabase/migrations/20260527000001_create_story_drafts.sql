-- DEPRECATED — identity scope removed 2026-06 (stories are gateway domain).
-- Historical migration only; do not apply on new identity deployments.
-- 20260527000001_create_story_drafts.sql
-- Story draft persistence for identity-service (req-15 / EPIC-IDS-05 Story 4).

CREATE TABLE IF NOT EXISTS public.story_drafts (
    draft_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supabase_user_id UUID NOT NULL
        REFERENCES auth.users(id) ON DELETE CASCADE,
    payload JSONB NOT NULL DEFAULT '{}',
    status TEXT NOT NULL DEFAULT 'draft'
        CHECK (status IN ('draft', 'submitted')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    submitted_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS story_drafts_user_idx
    ON public.story_drafts (supabase_user_id, created_at DESC);

ALTER TABLE public.story_drafts ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS story_drafts_service_role_all ON public.story_drafts;
CREATE POLICY story_drafts_service_role_all
    ON public.story_drafts FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);
