# Сравнительный аудит: общий vs отдельный Supabase-проект (identity vs business)

> **Дата:** 2026-06-03
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только верифицированные факты с путями
> **Вопрос:** identity-сервису заводить таблицы в существующем бизнес-проекте Supabase (`doge-complaints-gateway`) или держать отдельный проект (как в [`supabase-project-setup.md`](../runbook/supabase-project-setup.md))? Несёт ли разделение важный смысл?
> **Метод:** прочитаны миграции, config-схемы и auth-слои обоих сервисов + spa-app.

---

## 1. Верифицированное состояние (как есть)

### doge-identity-service — построен НА Supabase Auth

| Факт | Доказательство |
|------|----------------|
| `profiles.supabase_user_id` → FK `auth.users(id)` | [`20260525000001_create_profiles.sql:9`](../../supabase/migrations/20260525000001_create_profiles.sql) |
| `eid_verification_sessions` → FK `auth.users` | [`20260525000002_...sql:8`](../../supabase/migrations/20260525000002_create_eid_verification_sessions.sql) |
| `story_drafts` → FK `auth.users` | [`20260527000001_...sql:7`](../../supabase/migrations/20260527000001_create_story_drafts.sql) |
| RLS через `auth.uid()` (end-user policies) | `20260525000001_create_profiles.sql:64,69-70` |
| Валидация Supabase JWT: `iss={SUPABASE_URL}/auth/v1`, `role=authenticated`, HS256 c `SUPABASE_JWT_SECRET` | [`supabase_validator.py:16-45`](../../src/core/auth/supabase_validator.py), [`09-supabase-jwt-validation.md:41,99`](../requirements/09-supabase-jwt-validation.md) |
| Логин людей: email/password + magic link (Supabase Auth) | [[project-identity-kickoff]] |

**Вывод:** identity — это identity-backbone платформы. `auth.users` для него — ядро (FK + RLS + issuer JWT). 5 миграций.

### doge-complaints-gateway — работает ТОЛЬКО через service_role Postgres

| Факт | Доказательство |
|------|----------------|
| Таблицы: `stories`, `doge_issues`, `*_embeddings`, `issue_candidates`, `review_audit_log`, `issue_story_links`, `story_signals`, `cluster_memberships`, `idempotency_keys` | `supabase/bootstrap/000_full_init.sql:7-153` |
| RLS = **только** `to service_role using (true)`; **нет** `auth.uid()` / end-user policies | [`20260423_1510_rls_db_wave.sql:9-42`](../../../doge-complaints-gateway/supabase/migrations/20260423_1510_rls_db_wave.sql) |
| `auth.users` / `auth.uid` / `gotrue` — **0 упоминаний** | grep по `doge-complaints-gateway/supabase/` → пусто |
| Входящая аутентификация — `SERVICE_API_TOKEN` / Bearer service-token (S2S), не Supabase user JWT | [`src/core/api/security.py:17-20,69`](../../../doge-complaints-gateway/src/core/api/security.py) |
| Связь с identity — **строковый** `submitter_identity_issuer` (eID-gate на уровне БД), без FK | [`20260515_1200_submitter_identity_issuer_not_null.sql`](../../../doge-complaints-gateway/supabase/migrations/20260515_1200_submitter_identity_issuer_not_null.sql) |
| Env: `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE` + `DATABASE_URL` | `src/core/config/schema.py:138,144,132` |

**Вывод:** gateway — service-role consumer Postgres. `auth.users` не использует вообще. Идентичность сабмиттера хранит как **непрозрачную строку issuer**, не как ссылку на пользователя.

### spa-app (основной UI) — Supabase не использует

| Факт | Доказательство |
|------|----------------|
| Нет зависимости `@supabase/*` | `spa-app/package.json` → нет supabase |
| Нет `createClient` / `signInWith` | grep по `spa-app/src` → пусто |

---

## 2. Ключевой факт для решения

**Во всём бизнес-стеке сейчас НЕТ ни одного хранилища человеческих Auth-юзеров.** Gateway не трогает `auth.users`; spa-app не подключён к Supabase. Identity-сервис вводит Supabase Auth (`auth.users`) **впервые** на платформе.

Это снимает главный аргумент за слияние: «расширить уже существующих общих юзеров» — расширять **нечего**. `auth.users` создаётся с нуля независимо от выбора проекта. Платформа уже спроектирована с identity как **отдельным issuer**, на который gateway ссылается строкой (`submitter_identity_issuer`), без FK — то есть развязка уже заложена в архитектуру.

---

## 3. Сравнительная матрица (3 варианта)

| Критерий | A. Отдельный проект (текущий runbook) | B. Общий проект, отдельная schema (`identity.*`) | C. Общий проект, общий `public` |
|----------|----------------------------------------|--------------------------------------------------|----------------------------------|
| **service_role blast radius** | ✅ изолирован: ключ gateway не видит PII identity и наоборот | ❌ service_role обходит RLS **на весь проект** — gateway-ключ читает `profiles`/`eid_audit_events` | ❌ то же + случайные коллизии имён |
| **Миграции (SSOT)** | ✅ каждый репо — своя история (identity 5, gateway 15) | ⚠️ два репо пишут в одну БД; нужна координация порядка | ❌ конфликт владения, нет единой истории |
| **JWT secret** | ✅ identity владеет своим issuer | ❌ общий `SUPABASE_JWT_SECRET` — gateway может минтить/валидировать identity-токены | ❌ то же |
| **PII / whistleblower-данные** | ✅ две независимые зоны утечки | ❌ один скомпрометированный ключ = и истории, и verified_person_hash | ❌ то же |
| **Backup / PITR / upgrade / rate-limit** | ✅ независимый жизненный цикл | ❌ общий: апгрейд/лимиты影响 оба | ❌ то же |
| **Единый `auth.users` для всей платформы** | ⚠️ два «вселенных» auth.users (но gateway его не использует → не больно сейчас) | ✅ один auth.users (полезно ТОЛЬКО если gateway начнёт auth.uid()-RLS) | ✅ то же |
| **Кросс-FK identity↔business** | ❌ невозможен (разные БД) | ✅ возможен (но сейчас не нужен — issuer строкой) | ✅ возможен |
| **Стоимость / число проектов** | ❌ +1 проект (Supabase платит за проект) | ✅ один проект | ✅ один проект |
| **Соответствие текущей архитектуре** | ✅ совпадает с opaque-issuer развязкой | ⚠️ вводит связанность, которой в коде нет | ❌ противоречит развязке |

---

## 4. Анализ «несёт ли разделение смысл»

**Да, несёт — три реальных, проверяемых смысла:**

1. **Изоляция авторитета service_role (severity: HIGH).** Supabase `service_role` обходит RLS **на уровне всего проекта**, а не схемы. Подтверждено: gateway RLS — `to service_role using (true)` на всех таблицах. В общем проекте service_role-ключ gateway технически читает/пишет `profiles`, `eid_audit_events`, `eid_verification_sessions` (PII + verified_person_hash). Вариант B (отдельная schema) это **не** чинит — schema не граница для service_role. Только отдельный проект даёт настоящую изоляцию ключей.

2. **SSOT миграций (severity: MEDIUM).** Два независимых репозитория с собственными `supabase/migrations/` (identity: 5 файлов формата `2026MMDD...`, gateway: 15 файлов формата `YYYYMMDD_HHMM_...` — даже конвенции имён разные). Общая БД = два источника DDL без единой истории → anti-pattern «Integration Gaps» + «Single Source of Truth».

3. **Раздельный issuer JWT (severity: MEDIUM).** identity — OAuth/Supabase-Auth issuer; gateway — S2S по `SERVICE_API_TOKEN`. Общий `SUPABASE_JWT_SECRET` стирает границу: сервис обработки историй получил бы способность валидировать/минтить пользовательские Auth-токены.

**Аргументы ЗА общий проект — сейчас не срабатывают:**
- «Единый `auth.users`» — нет существующих юзеров для объединения (раздел 2); gateway не использует auth.uid().
- «Кросс-FK» — не нужен: связь уже сделана строкой `submitter_identity_issuer` намеренно (eID-gate).
- Остаётся только **стоимость/удобство** (один проект дешевле/проще в управлении) — это операционный, не архитектурный довод.

---

## 5. Рекомендация

**Держать отдельный Supabase-проект для identity (текущий runbook — верный).**

Обоснование: единственные содержательные плюсы общего проекта (общий `auth.users`, кросс-FK) на текущей архитектуре **не реализуемы как выгода** — общего стора юзеров нет, а связь identity↔gateway намеренно развязана через строковый issuer. При этом общий проект вносит реальные риски: project-wide bypass RLS у service_role (HIGH), смешение миграционных историй (MEDIUM), общий JWT-секрет (MEDIUM). Разделение **уже отражено** в коде (opaque `submitter_identity_issuer`, отсутствие FK) — отдельный проект это closure, а не новая сущность.

### Единственное условие, которое перевернуло бы решение

Если бизнес примет стратегическое решение, что **бизнес-проект становится единым Auth-авторитетом всей платформы** (один человек = один `auth.users` на весь стек, и gateway/SPA начнут использовать `auth.uid()`-RLS и FK на `auth.users`), тогда identity-таблицы логично разместить **в том же проекте** (вариант B, отдельная schema `identity.*`), приняв риск общего service_role. Но это требует:
- gateway/SPA реально перейти на Supabase Auth (сейчас — нет: `SERVICE_API_TOKEN` + нет supabase-зависимости в SPA);
- замены строкового `submitter_identity_issuer` на FK к `auth.users`/`profiles`;
- единого владельца миграций общей БД.

До этого решения — **отдельный проект**.

---

## 6. Несоответствие в документации (зафиксировать)

[[project-identity-kickoff]] фиксирует: *«Supabase: проект есть, URL/ключи рабочие, таблицы identity не созданы — нужны миграции»* — формулировка неоднозначна (тот же бизнес-проект или выделенный?). Runbook [`supabase-project-setup.md:3`](../runbook/supabase-project-setup.md) явно требует **«новый» проект**. Рекомендация раздела 5 согласуется с runbook; kickoff-заметку стоит уточнить, чтобы убрать двусмысленность (это и есть исходная причина текущего вопроса).

---

## 7. Интеграционный шов (для справки, не меняется)

Контракт identity ↔ gateway уже определён и не зависит от выбора проекта: gateway хранит `stories.submitter_identity_issuer` (строка, NOT NULL с бэкфиллом `legacy-unknown`), identity выдаёт verified-person/OAuth. Это слабая связанность по значению, не по БД — корректна при отдельных проектах.

---

## Quality gate (analysis.mdc)
- [x] Все claims привязаны к путям/строкам (identity-миграции, gateway RLS/bootstrap/config/security, spa-app package).
- [x] Проверены оба сервиса + spa-app; ключевой факт (нет общего auth.users) подтверждён grep'ом.
- [x] Severity проставлена; варианты B/C рассмотрены, не только бинарный выбор.
- [x] Зафиксировано документ-несоответствие (kickoff vs runbook), не скрыто.
- [x] Рекомендация и условие её разворота — явные и проверяемые.
