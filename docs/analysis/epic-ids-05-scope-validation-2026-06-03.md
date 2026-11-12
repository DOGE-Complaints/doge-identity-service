# Валидация EPIC-IDS-05 — scope `story_drafts` и сопутствующий бардак

> **Дата:** 2026-06-03
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями
> **Триггер:** оператор поднял отдельный Supabase-проект identity, загрузил 4 из 5 миграций, **намеренно пропустив** [`20260527000001_create_story_drafts.sql`](../../supabase/migrations/20260527000001_create_story_drafts.sql) — «зачем истории в identity, если они в doge-complaints-gateway?»
> **Связанный анализ:** [`supabase-project-separation-audit-2026-06-03.md`](./supabase-project-separation-audit-2026-06-03.md)

---

## TL;DR

Вопрос оператора обоснован. `story_drafts` — это **буфер контента историй внутри identity**, втянутый в EPIC-IDS-05 (persistence) раньше своей функциональной фичи (`EPIC-IDS-STORIES`, ещё не существует), при этом:
- эпик сам помечает его **«опционально»**, но healthcheck делает его **обязательным** → пропуск миграции ломает `/ready` (HTTP 503);
- фича, ради которой он создан (форвард историй в gateway), **не реализована и не конфигурируема** (нет `COMPLAINTS_GATEWAY_URL`/`SERVICE_API_TOKEN`);
- схема таблицы в спеке req-15 **расходится** с тем, что реально отгружено.

Найдено **6 несоответствий** (3 HIGH, 2 MEDIUM, 1 LOW).

---

## G1 [HIGH] — `story_drafts`: «опционально» в Story 4, «обязательно» в Story 3 → ломает `/ready`

**Противоречие внутри одного эпика:**
- Story 4 ([`EPIC-IDS-05-...md:160`](../tasks/epics/EPIC-IDS-05-supabase-persistence/EPIC-IDS-05-supabase-persistence.md)): *«Добавляются миграции из req-17 … и **опционально** req-15 (`story_drafts`)»*.
- Story 3 healthcheck ([`db_supabase.py:315-320`](../../src/core/infrastructure/db_supabase.py)): `story_drafts` входит в `_REQUIRED_TABLES`:
  ```python
  _REQUIRED_TABLES = ("profiles", "eid_verification_sessions", "eid_audit_events", "story_drafts")
  ```
  `required_tables_ready()` итерирует все 4 и при первом 404 → `False`.

**Прямое следствие для оператора:** проект, где `story_drafts` не создан, на старте даст:
```
db_checks={'connectivity': True, 'schema': False, ...}  → db_ready=False
GET /ready → HTTP 503 "degraded"
```
То есть «опциональная» таблица фактически блокирует readiness всего сервиса. Это и есть бардак, на который наткнулся оператор.

**Как закрыть (направление):** убрать `story_drafts` из `_REQUIRED_TABLES` (она нужна только будущему `EPIC-IDS-STORIES`), ИЛИ принять решение по G2/G3 и удалить таблицу из identity целиком. До этого `/ready` на корректно поднятом identity-проекте без story-фичи будет 503.

---

## G2 [HIGH] — Scope leak: identity хранит контент историй (PII жалоб)

**Факт:** [`story_drafts`](../../supabase/migrations/20260527000001_create_story_drafts.sql) хранит `payload JSONB` — по req-15 это `title`/`body`/`context` жалобы. Domain-модель [`StoryDraft` (models.py:96-103)](../../src/core/domain/models.py): `draft_id`, `supabase_user_id`, `payload`, `status`, `created_at`, `submitted_at`.

req-15 сам признаёт ([`15-story-authorization.md:5`](../requirements/15-story-authorization.md)): *«реальная pipeline историй — doge-complaints-gateway»*, а identity лишь **форвардит** черновик в gateway `/intake/stories` после eID ([`15-...md:86,156,226-233`](../requirements/15-story-authorization.md)).

**Проблема:** identity — сервис идентичности/eID/OAuth. Хранение черновикового контента жалоб (whistleblower-данные) в identity-БД:
- нарушает SRP (контент историй — домен gateway, см. `stories` в [gateway bootstrap](../../../doge-complaints-gateway/supabase/bootstrap/000_full_init.sql));
- расширяет зону PII identity без необходимости (drafts — лишь UX-буфер «написать до eID»).

Инстинкт оператора верен: финальные истории в identity не нужны и их там нет — но **черновиковый контент** туда заведён.

**Как закрыть (направление):** продуктовое решение — (а) убрать `story_drafts` из identity, буфер черновиков держать в gateway/SPA; либо (б) если pre-eID-буфер в identity намеренный — формализовать его как **identity-scoped staging**, не как часть mandatory-схемы, и зафиксировать privacy-обоснование в ADR.

---

## G3 [HIGH] — Persistence построен для нереализуемой фичи (нет handler + нет конфига)

EPIC-IDS-05 отгрузил полный persistence для story_drafts: миграция + `SupabaseStoryDraftRepository` ([db_supabase.py:616-648](../../src/core/infrastructure/db_supabase.py)) + `InMemoryStoryDraftRepository`. Но потребляющая фича отсутствует:

| Компонент | Состояние | Доказательство |
|-----------|-----------|----------------|
| Роуты `/story-drafts`, `/story-drafts/{id}/submit`, `/stories`, `/gpt/actions/submit-story` | **501 stub** | [`asgi_app.py:258-310`](../../src/core/api/asgi_app.py) → `next_epic="EPIC-IDS-STORIES"` |
| Форвард в gateway (`COMPLAINTS_GATEWAY_URL`, `SERVICE_API_TOKEN`) — req-15 требует | **нет в `AppConfig`** | grep по `src/` → пусто; [`schema.py`](../../src/core/config/schema.py) не содержит этих полей |
| Те же vars в `.env.example` | **отсутствуют** | grep по `.env.example` → пусто |

Итого: EPIC-IDS-05 (persistence-слой) реализовал хранилище под фичу `EPIC-IDS-STORIES`, которой **ещё нет** (не декомпозирована), и встроил его в mandatory-healthcheck. Anti-pattern «Verified State / Integration-First»: персистентность опередила фичу, конфиг для её ключевого шага (форвард в gateway) не заведён.

**Как закрыть (направление):** отложить story-persistence до `EPIC-IDS-STORIES` (там же добавить `COMPLAINTS_GATEWAY_URL`/`SERVICE_API_TOKEN`), а в IDS-05 не держать таблицу в required-наборе.

---

## G4 [MEDIUM] — Schema drift: req-15 spec ↔ отгруженная таблица

Одна таблица, две несовместимые схемы:

| Поле | req-15 §"story_drafts table" ([`15-...md:204-218`](../requirements/15-story-authorization.md)) | Отгружено (migration + model + epic) |
|------|---------|---------|
| PK | `id` | `draft_id` |
| owner | `owner_user_id` | `supabase_user_id` |
| контент | `title`, `body`, `locale`, `context JSONB` | `payload JSONB` |
| status CHECK | `('draft','submitted','expired')` | `('draft','submitted')` — нет `expired` |
| timestamps | `created_at`, `updated_at` | `created_at`, `submitted_at` — нет `updated_at` |

Отгруженное (миграция + [`models.py:96-103`](../../src/core/domain/models.py) + epic line 98) согласовано между собой; **req-15 — устаревший** источник. Поскольку req-15 — формальная спека endpoint'ов, drift введёт в заблуждение при реализации `EPIC-IDS-STORIES`.

**Как закрыть:** привести req-15 §"story_drafts table" к фактической схеме (или пометить, что финальная схема — в миграции).

---

## G5 [MEDIUM] — req-08 (Migrations SSOT) не отражает 2 из 5 миграций

Runbook §Related называет [`08-supabase-migrations.md`](../requirements/08-supabase-migrations.md) «Migrations SSOT». Но req-08 документирует **только 3** миграции ([`08-...md:13-15`](../requirements/08-supabase-migrations.md)): profiles, eid_verification_sessions, eid_audit_events.

Фактически в [`supabase/migrations/`](../../supabase/migrations/) — **5**:
- `20260526000001_eid_sessions_provider_abstraction.sql` (req-17) — **не в req-08**;
- `20260527000001_create_story_drafts.sql` (req-15) — **не в req-08**.

«SSOT» миграций не является SSOT. Оператор, читающий req-08, не узнает о 2 миграциях; читающий runbook §3 — увидит 5. Источники расходятся.

**Как закрыть:** дополнить req-08 миграциями provider_abstraction + story_drafts (или явно делегировать их req-17/req-15 с перечнем в req-08).

---

## G6 [LOW] — Runbook предписывает обязательной таблицу, помеченную «опционально»

Runbook [`supabase-project-setup.md:54-62`](../runbook/supabase-project-setup.md) перечисляет 5 миграций «по порядку (каждый файл целиком → Run)» как обязательный bootstrap, включая story_drafts (#5); §5 ожидает `db_checks={'schema': True}`. Это downstream G1: документация требует таблицу, которую эпик зовёт опциональной и которую оператор обоснованно пропустил.

**Как закрыть:** после решения по G1/G2 — синхронизировать runbook (либо пометить миграцию 5 как часть будущей story-фичи и не входящую в minimal bootstrap).

---

## Сводная таблица

| ID | Severity | Суть | Якорь |
|----|----------|------|-------|
| G1 | HIGH | `story_drafts` optional в Story 4, required в healthcheck → `/ready` 503 при пропуске | `db_supabase.py:315-320` vs epic L160 |
| G2 | HIGH | identity хранит контент историй (PII жалоб) — scope/SRP leak | `models.py:96-103`, req-15 L5 |
| G3 | HIGH | persistence без фичи: роуты 501, нет `COMPLAINTS_GATEWAY_URL`/`SERVICE_API_TOKEN` | `asgi_app.py:258-310`, `schema.py` |
| G4 | MEDIUM | schema drift req-15 ↔ migration/model | req-15 L204-218 |
| G5 | MEDIUM | req-08 SSOT не содержит 2 из 5 миграций | `08-...md:13-15` |
| G6 | LOW | runbook требует «опциональную» таблицу | runbook L54-62 |

---

## Рекомендация (для решения, не реализовано)

**Минимальный безопасный фикс (разблокирует оператора немедленно):** исключить `story_drafts` из `_REQUIRED_TABLES` healthcheck'а — она потребляется только будущим `EPIC-IDS-STORIES`. После этого identity-проект без story_drafts даёт `/ready` 200.

**Стратегически:** перенести всю story-draft персистентность (таблица, репозитории, миграция) из IDS-05 в `EPIC-IDS-STORIES` и принять продуктовое решение по G2 — нужен ли pre-eID буфер контента жалоб именно в identity, или черновики должны жить в gateway/SPA. Сейчас identity несёт story-домен «авансом», и это источник несоответствий G1–G6.

**Открытый вопрос (нужен ответ владельца):** pre-eID draft-буфер — намеренная UX-фича identity или артефакт спеки? От этого зависит, удалять `story_drafts` из identity или формализовать как identity-staging вне mandatory-схемы.

---

## Quality gate (analysis.mdc)
- [x] Все claims привязаны к путям/строкам (миграция, db_supabase, asgi_app, models, schema, req-08/15, runbook, epic).
- [x] Подтверждён конкретный эффект действия оператора (пропуск story_drafts → `/ready` 503) через `_REQUIRED_TABLES`.
- [x] Внутреннее противоречие эпика (optional vs required) зафиксировано цитатами обеих сторон.
- [x] Severity проставлена; реализация не навязана — даны направления + открытый вопрос владельцу.
- [x] Кросс-ссылка на связанный separation-audit.
