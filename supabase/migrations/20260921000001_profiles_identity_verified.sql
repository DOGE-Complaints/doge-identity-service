-- 20260921000001_profiles_identity_verified.sql
-- Method-opaque identity_verified on profiles (TECH-ARCH §2.2; STORY-IDS-VB-01)

ALTER TABLE public.profiles
    ADD COLUMN IF NOT EXISTS identity_verified BOOLEAN NOT NULL DEFAULT FALSE;
