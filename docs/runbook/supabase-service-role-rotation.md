# Runbook: Supabase `service_role` rotation (identity)

**Story:** [STORY-IDS-SEC-04-service-role-isolation](../tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/STORY-IDS-SEC-04-service-role-isolation.md)  
**Scope:** identity-backend — единственный легитимный держатель `SUPABASE_SERVICE_ROLE`.

## Когда ротировать (триггеры)

| Триггер | Действие |
|---------|----------|
| Подозрение на утечку ключа (commit, лог, скриншот) | **Немедленная** ротация |
| `service_role` был в spa `.env` / Vite bundle ([spa SEC-01](../../../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-01-remove-service-role-from-frontend.md)) | Ротация **после** удаления ключа с фронта и redeploy spa (см. §Spa coordination) |
| Плановая ротация (policy) | По календарю оператора; зафиксировать в change log |
| Новый участник команды с доступом к старому `.env` | Рекомендуется ротация |

## Предусловия

- Доступ к Supabase Dashboard проекта identity (prod / staging / dev — **отдельные** ключи).
- Доступ к Railway Variables (или локальному `.env`) **только** identity-backend.
- Окно обслуживания: краткий restart identity после смены env (PostgREST вызовы используют новый ключ сразу после reload).

## Процедура (Dashboard → identity env)

1. **Зафиксировать инцидент/причину** (ticket, run-summary, или строка в ops log).
2. **Supabase Dashboard** → Project → Settings → API → **service_role** (secret) → **Rotate** (или Regenerate — по UI Supabase).
3. Скопировать **новый** `service_role` key (secret). **Не** сохранять в chat/email/ticket в открытом виде.
4. **Identity env** (Railway Variables или local `.env`):
   - Обновить `SUPABASE_SERVICE_ROLE=<new_key>`.
   - Убедиться, что ключ **не** попал в spa, gateway или другие сервисы.
5. **Redeploy / restart** identity-backend.
6. **Smoke:**
   ```bash
   curl -sS "$API_BASE_URL/health" | jq .
   curl -sS "$API_BASE_URL/ready" | jq .
   ```
   При `DB_BACKEND=supabase` — `ready` должен показывать `db_ready: true`.
7. **Optional:** offline regression `pytest -q -m "not live_integration"` на staging перед prod.

## Rollback

Если после ротации identity не стартует или `ready` падает:

1. В Supabase **нельзя** «откатить» старый ключ после rotate — только **ещё одна** ротация на новый валидный ключ.
2. Если новый ключ ошибочен — повторить шаг 2–5 с корректным ключом из Dashboard.
3. Если проблема не в ключе (URL, сеть) — не ротировать повторно; диагностировать [`run-and-healthcheck.md`](./run-and-healthcheck.md).

## Spa coordination (STORY-SPA-SEC-01)

Парная spa-стори: [STORY-SPA-SEC-01 — remove service_role from frontend](../../../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-01-remove-service-role-from-frontend.md).

**Единая точка решения — когда ротировать после spa SEC-01:**

| Сценарий | Ротация |
|----------|---------|
| Ключ был **только** в локальном `spa-app/.env`, prod bundle **не** собирался с `VITE_SUPABASE_SERVICE_ROLE` | По решению оператора; **рекомендуется** ротация |
| Prod/staging spa **деплоился** с `VITE_SUPABASE_SERVICE_ROLE` в bundle | **Обязательная** ротация после merge/deploy spa SEC-01 |
| Spa SEC-01 Done, ключ удалён с фронта, bundle чист | Ротация по триггеру выше; синхронизировать identity env **до** или **сразу после** spa deploy |

**Checklist (координированная ротация):**

- [ ] Spa: `grep SERVICE_ROLE` по `spa-app/.env*` → пусто; CI guard на `VITE_*SERVICE_ROLE*` активен (spa SEC-01 AC).
- [ ] Spa prod redeploy без service_role в bundle (если применимо).
- [ ] Identity: rotate в Supabase Dashboard → update `SUPABASE_SERVICE_ROLE` → restart identity.
- [ ] Smoke `/health` + `/ready` на identity.
- [ ] Зафиксировать в run-summary / ticket: дата ротации, среда, ссылка на spa SEC-01 + identity SEC-04.

**Не делать:** копировать новый `service_role` в spa, gateway или клиентские `.env`.

## Связанные документы

- [`04-security.md` §5.1](../runtime-docs/04-security.md) — инвариант границы
- [`07-env-configuration-spec.md`](../requirements/07-env-configuration-spec.md) — `SUPABASE_SERVICE_ROLE`
- [`env-secrets-handbook.md`](./env-secrets-handbook.md) — типы секретов
- [`supabase-project-setup.md`](./supabase-project-setup.md) — первичная настройка ключа
