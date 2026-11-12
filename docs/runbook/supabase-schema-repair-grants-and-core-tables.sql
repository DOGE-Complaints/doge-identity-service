-- =============================================================================
-- doge-identity-service — schema repair (operator-only, NOT auto-applied)
-- =============================================================================
-- Контекст: docs/analysis/supabase-startup-db-ready-false-2026-06-27.md
-- Симптомы: db_ready=False; 403 on profiles/eid_sessions; 404 on eid_audit_events
--
-- ВАЖНО:
-- 1. Выполнять в Supabase SQL Editor на проблемном проекте.
-- 2. Сначала Шаг 0 (SELECT) — убедиться что именно отсутствует.
-- 3. Если таблиц нет — предпочтительнее полный bootstrap:
--    supabase/bootstrap/000_full_init.sql (вместо cherry-pick).
-- 4. Этот файл — repair addendum; не заменяет migrations/.
-- =============================================================================


-- -----------------------------------------------------------------------------
-- Шаг 0 — диагностика (read-only)
-- -----------------------------------------------------------------------------

SELECT tablename
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename IN (
    'profiles',
    'eid_verification_sessions',
    'eid_audit_events',
    'phone_verification_sessions',
    'phone_audit_events',
    'oauth_authorization_requests',
    'oauth_authorization_codes'
  )
ORDER BY 1;

SELECT table_name, grantee, privilege_type
FROM information_schema.role_table_grants
WHERE table_schema = 'public'
  AND table_name IN ('profiles', 'eid_verification_sessions', 'eid_audit_events')
  AND grantee = 'service_role'
ORDER BY 1, 3;


-- -----------------------------------------------------------------------------
-- Шаг 1 — если eid_audit_events отсутствует: применить миграцию #3 целиком
-- (скопировать содержимое файла, не дублировать здесь — SSOT = migrations/)
--   supabase/migrations/20260525000003_create_eid_audit_events.sql
-- Если нет provider columns на eid_verification_sessions:
--   supabase/migrations/20260526000001_eid_sessions_provider_abstraction.sql
-- -----------------------------------------------------------------------------


-- -----------------------------------------------------------------------------
-- Шаг 2 — GRANT для service_role (fix HTTP 403 / Postgres 42501)
-- RLS policies alone are insufficient; PostgREST needs table privileges.
-- -----------------------------------------------------------------------------

GRANT SELECT, INSERT, UPDATE, DELETE ON public.profiles TO service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.eid_verification_sessions TO service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.eid_audit_events TO service_role;

-- Если phone/oauth таблицы уже созданы — выдать те же права:
GRANT SELECT, INSERT, UPDATE, DELETE ON public.phone_verification_sessions TO service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.phone_audit_events TO service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.oauth_authorization_requests TO service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.oauth_authorization_codes TO service_role;


-- -----------------------------------------------------------------------------
-- Шаг 3 — после repair: перезапустить identity и проверить
--   make serve  →  db_ready=True
--   curl http://localhost:8100/ready
-- -----------------------------------------------------------------------------
