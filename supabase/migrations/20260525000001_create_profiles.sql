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
