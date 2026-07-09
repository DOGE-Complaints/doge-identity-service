# Runbooks — doge-identity-service

Операторская документация: запуск, env, интеграции.

## Начни отсюда

| Runbook | Когда читать |
|---------|--------------|
| [**env-secrets-handbook.md**](./env-secrets-handbook.md) | Настройка `.env` / Railway Variables: секреты, OAuth, local vs pilot, команды генерации ключей |
| [**run-and-healthcheck.md**](./run-and-healthcheck.md) | Поднять сервис локально или на Railway, проверить `/health` и smoke |
| [**cors-allowed-origins.md**](./cors-allowed-origins.md) | CORS для spa: что писать в `CORS_ALLOWED_ORIGINS` |
| [**supabase-project-setup.md**](./supabase-project-setup.md) | Новый Supabase-проект, миграции, credentials в `.env` |
| [**supabase-service-role-rotation.md**](./supabase-service-role-rotation.md) | Ротация `SUPABASE_SERVICE_ROLE` (SEC-04): триггеры, Dashboard → identity env, spa coordination |

## Phone / onboarding

| Runbook | Когда читать |
|---------|--------------|
| [**onboarding-phone-verification-api.md**](./onboarding-phone-verification-api.md) | API phone-верификации без фронтенда |
| [**phone-sms-verification.md**](./phone-sms-verification.md) | Архитектура SMS/phone flow |
| [**sms-mock-testing.md**](./sms-mock-testing.md) | `SMS_PROVIDER=mock`, OTP в логах |

## SQL / repair

| Файл | Когда использовать |
|------|-------------------|
| [**supabase-schema-repair-grants-and-core-tables.sql**](./supabase-schema-repair-grants-and-core-tables.sql) | Ручной repair grants/таблиц в Supabase |
