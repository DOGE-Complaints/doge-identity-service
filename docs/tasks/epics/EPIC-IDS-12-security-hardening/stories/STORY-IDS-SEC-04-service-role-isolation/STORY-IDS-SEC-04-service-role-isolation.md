# STORY-IDS-SEC-04 — Изоляция Supabase `service_role`: identity — единственный держатель

## Meta
- **Key:** `STORY-IDS-SEC-04-service-role-isolation`
- **Parent Epic:** [`../../EPIC-IDS-12-security-hardening.md`](../../EPIC-IDS-12-security-hardening.md)
- **Epic alias (код/backlog):** `EPIC-IDS-SEC` · [`EPIC-IDS-SEC`](../../../../backlog-stories/security-hardening/EPIC-IDS-SEC.md)
- **Status:** 🟢 Done
- **Severity:** 🔴 (cross-service security boundary)
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md`](../../../../backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md)
- **Decision Ref:** [`../../../../backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md`](../../../../backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md); [`identity-supabase-frontend-split-2026-06-16.md`](../../../../../../../spa-app/docs/analysis/identity-supabase-frontend-split-2026-06-16.md) §6.1; [`STORY-SPA-SEC-01`](../../../../../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-01-remove-service-role-from-frontend.md)
- **Источник:** [`identity-supabase-frontend-split §6.1`](../../../../../../../spa-app/docs/analysis/identity-supabase-frontend-split-2026-06-16.md) — `service_role` нашли в браузерном `spa-app/.env`.
- **Парная spa-стори:** [`STORY-SPA-SEC-01`](../../../../../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-01-remove-service-role-from-frontend.md)

Deprecated, extracted to doge-identity-service/docs/tasks/backlog-stories/auth-bff (post MVP)

## Зачем простыми словами
`service_role` — это привилегированный ключ Supabase, который **обходит RLS** и видит все данные проекта. Правило безопасности: его держит **ровно один** компонент — **identity-backend на сервере**, и он **никогда** не уходит в браузер/клиента. При валидации фронта выяснилось, что копия этого ключа лежала в браузерном `spa-app/.env` (это чинит spa [SEC-01](../../../../../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-01-remove-service-role-from-frontend.md)). Со стороны identity нужно **зафиксировать границу как требование** и дать runbook ротации — чтобы единственным легитимным местом ключа был identity.

## Точки в коде (текущее состояние — уже корректно)
- `service_role` читается из env только на сервере: `supabase_service_role` ([`schema.py:33,159,209`](../../../../../../src/core/config/schema.py)); **обязателен** при `DB_BACKEND=supabase` ([`schema.py:165-166`](../../../../../../src/core/config/schema.py)) и в pilot fail-fast ([`schema.py:184`](../../../../../../src/core/config/schema.py)).
- Используется server-side для Postgres (PostgREST `service_role`) в [`db_supabase.py`](../../../../../../src/core/infrastructure/db_supabase.py).
- **Не** логируется (grep по `log|print|debug` + `service_role` → пусто). ✅
- identity **не** делает user-login (нет `/auth/login|signup` — grep по [`asgi_app.py`](../../../../../../src/core/api/asgi_app.py) пусто) → service_role нужен только для server-side data-доступа.

## Scope (требования)
- **Инвариант границы:** зафиксировать как требование — `SUPABASE_SERVICE_ROLE` существует **только** в `doge-identity-service` (server env), **никогда** в spa/браузере/клиентских артефактах.
- **No-expose guard:** требование «service_role не логируется, не возвращается в ответах, не попадает в trace/ошибки» (подтвердить тестом/линтом).
- **Rotation runbook:** документированная процедура ротации в Supabase Dashboard + обновления `SUPABASE_SERVICE_ROLE` в identity (и триггеры: подозрение на утечку, как с `spa-app/.env`).
- **Координация с spa:** ротация после выноса ключа из фронта ([SEC-01 AC](../../../../../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-01-remove-service-role-from-frontend.md)) — единая точка решения.

## Вне scope
- Вынос ключа из spa-`.env` — это spa [SEC-01](../../../../../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-01-remove-service-role-from-frontend.md).
- Модель login (BFF vs anon) — [SEC-05](../../../../backlog-stories/security-hardening/STORY-IDS-SEC-05-auth-credential-model-adr.md).

## Acceptance Criteria
- [x] Зафиксировано требование «identity — единственный держатель `service_role`; не в браузере» (в 04-security / 07-env / runbook).
- [x] No-expose подтверждён (нет в логах/ответах/trace) — проверяемо.
- [x] Rotation runbook написан (Dashboard → identity env; триггеры).
- [x] Ротация скоординирована с spa [SEC-01](../../../../../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-01-remove-service-role-from-frontend.md) (если был фронт-bundle).

## Парадигма-якорь
[`04-security §5 (RLS/service_role)`](../../../../../runtime-docs/04-security.md), [`split-doc §6.1, §6.5`](../../../../../../../spa-app/docs/analysis/identity-supabase-frontend-split-2026-06-16.md).
