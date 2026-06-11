-- 20260611000001_profiles_phone_verification.sql
-- Phone verification status on profiles (mirror eID columns)

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
