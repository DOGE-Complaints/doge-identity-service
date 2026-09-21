-- 20260921000002_profiles_identity_verified_backfill.sql
-- One-shot backfill: phone_verified OR eid_verified → identity_verified=true (TECH-ARCH §2.4)

UPDATE public.profiles
SET identity_verified = TRUE
WHERE phone_verified = TRUE
   OR eid_verified = TRUE;
