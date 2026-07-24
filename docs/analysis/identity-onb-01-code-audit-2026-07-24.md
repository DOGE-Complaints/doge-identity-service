# Аудит по коду: STORY-IDS-ONB-01 (`email` в `/me` + Supabase «Confirm email») — 2026-07-24

> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — verified-state, только проверяемые claims с путями; регрессии; gaps с severity + как закрыть. Findings-only (реализацию не предлагаю).
> **Объект:** [`STORY-IDS-ONB-01-email-in-me-and-supabase-confirm`](../tasks/backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md) (pkg-000045).
> **Синхронизирован отчёт:** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) — статусы task/story подтверждены аудитом (drift не найден); findings ниже вынесены в gap-queue индекса.
> **Решения-основа:** [`identity-cabinet-me-fields-interview-2026-07-13`](identity-cabinet-me-fields-interview-2026-07-13.md) (D-CAB-3: `email_verified: true` по политике «токен ⇒ подтверждён»).
> **Пара:** [AUTHCORE-02 audit](identity-authcore-02-code-audit-2026-07-24.md) — ONB-01 закрывает бывший **G1** того аудита (`email` в `/me`).

---

## Вердикт

**STORY-IDS-ONB-01 = 🟢 Done — подтверждено фактическим кодом.** Все 3 таска стори (T01–T03) реализованы; pipeline отработал 4 таска (+синтетический t04 acceptance-verification). Scope-контракт (`email` + `email_verified=true` + runbook «Confirm email») исполнен точно по D-CAB-3; регрессий нет; offline-сюита независимо перепрогнана зелёной (**406 passed, 12 deselected** — совпадает с [run-summary](../tasks/run-reports/identity-build-windows/run-summary-20260724-1857-epic-ids-13-onb-01-pkg-000045.md); +1 тест против 405 у AUTHCORE-02). Индекс `bullrun-launch-index.md` уже отражает статусы корректно (pipeline актуализировал) — правок статусов не требуется.

**Следствие:** umbrella-контракт CAB-02 для identity теперь **3/3** (`email` + `created_at` + `account_status` — все live). Бывший **G1 (MEDIUM)** аудита AUTHCORE-02 — 🟢 закрыт.

Найдено **3 gap'а** (0×HIGH, 0×MEDIUM, 3×LOW) — cross-repo drift доков (в т.ч. обратный дрейф SPA после закрытия ONB-01), семантический нюанс `email_verified` и трассируемость нумерации тасков. Ни один не является дефектом реализации.

---

## Пер-таск верификация (по коду)

| Task | Требование стори | Факт в коде | Вердикт |
|------|------------------|-------------|---------|
| **T01** me_response | базовый dict `build_me_data`: `email = current_user.email`, `email_verified = True` (верно и для no-profile) | [`me_response.py:21-22`](../../src/core/api/me_response.py) — оба в **базовом** dict (до `if profile is not None`), значит отдаются даже без профиля; `email` из [`UserClaims.email: str \| None`](../../src/core/domain/models.py) (models.py:18) | ✅ Done |
| **T02** runbook + api-docs | runbook: обязательный «Confirm email»; `openapi.yaml MeData` + `API_REFERENCE.md §6`: `email [string,null]` + `email_verified` bool «политика» | [`supabase-project-setup.md:50-58`](../runbook/supabase-project-setup.md) §2a «Confirm email (**mandatory**)»; [`openapi.yaml:73-80`](../runtime-docs/api-reference/openapi.yaml) (`email` nullable + `email_verified` desc «policy D-CAB-3/ONB-01, correct only when Confirm email enabled»); [`API_REFERENCE.md:84`](../runtime-docs/api-reference/API_REFERENCE.md) §6 email-fields + ссылка на runbook | ✅ Done |
| **T03** tests | `email` из токена (`null` без claim); `email_verified == true`; сюита зелёная | [`test_me_profile.py:87-88`](../../tests/test_me_profile.py) (с профилем) + [`:91-98`](../../tests/test_me_profile.py) (`test_me_email_null_when_jwt_has_no_email_claim` → `email=null`, `email_verified=true`) + [`:165-166`](../../tests/test_me_profile.py) (no-profile → `email` из токена, `email_verified=true`) | ✅ Done |
| **t04** (pipeline) | story acceptance verification | run-summary t04 🟢; синтетический pipeline-таск (не нумеруется в backlog-стори — см. F3) | ✅ Done (иной scope) |

**Guard-проверки (независимо перепрогнаны):**
- `.venv/bin/python -m pytest -m "not live_integration"` → **406 passed, 12 deselected** (2026-07-24). ✅
- `pytest tests/test_me_profile.py` → **6 passed** (было 5 до ONB-01: +`test_me_email_null_when_jwt_has_no_email_claim`). ✅
- `grep email src/core/api/` → только `me_response.py:21-22` (payload) + `security.py:64` (OAuth-путь `email=None`, см. F2). ✅

**AC стори:** все 5 пунктов `[x]` ([story:38-42](../tasks/backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md)) — каждый подтверждён кодом выше. Status 🟢 Done в обеих копиях (backlog + epic-materialized), в [INDEX onboarding](../tasks/backlog-stories/identity-onboarding/INDEX.md) (1/1, 100%) и в bullrun (task-table [769-772], story-registry [835]).

---

## Регрессии

**Не найдено.** Существующие поля `/me` не тронуты; поля AUTHCORE-02 (`created_at`, `account_status`) сохранены в том же билдере ([`me_response.py:35-36,50`](../../src/core/api/me_response.py)); envelope `{data:{…}}` цел; политика no-auto-provision сохранена (no-profile → 200, `email`+`email_verified` из токена, БД не пишется — [`test_me_profile.py:146-166`](../../tests/test_me_profile.py)); новых миграций нет (`email`/`email_verified` — из JWT-claim, не из БД).

---

## Gaps (findings)

| ID | Severity | Суть | Файл:строка | Как закрыть |
|----|----------|------|-------------|-------------|
| **F1** | **LOW** | **Обратный cross-repo drift: SPA-контракт снова устарел.** После закрытия ONB-01 `email` **live** в `/me`, но SPA cabinet-доки (правились 2026-07-24, когда ONB-01 был ⚪) всё ещё помечают `email` как ❌ «ждёт ONB-01 (⚪ Todo)» → недооценивают готовность. CAB-02 identity-контракт теперь **3/3**, карточка может рендерить complete-состояние (M24). | [`STORY-SPA-CAB-api-requirements.md:7,31,39-41,100`](../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-api-requirements.md); [`STORY-SPA-CAB-02:21`](../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-02-account-summary-block.md) | Обновить SPA §0/§4 + CAB-02 «Текущее состояние»: `email` → ✅ live (ONB-01 pkg-000045); пометить caveat'ы F2 (`email_verified` policy-gated; `email=null` для OAuth-токенов). (spa-сторона, вне identity pkg.) |
| **F2** | **LOW** | **Семантика `email_verified` не полна для потребителя.** `email_verified` захардкожен `True` в базовом dict ([`me_response.py:22`](../../src/core/api/me_response.py)) безусловно — **даже когда `email=null`**. OAuth/GPT-путь конструирует `UserClaims(email=None)` ([`security.py:62-66`](../../src/core/api/security.py)) → `/me` отдаёт `email:null, email_verified:true` (структурно, не «claim absent»). Плюс корректность флага завязана на ops-тумблер Supabase «Confirm email», который код не может проверить. Оба факта задокументированы ([`openapi.yaml:78-80`](../runtime-docs/api-reference/openapi.yaml), [`runbook §2a`](../runbook/supabase-project-setup.md)) — принятый дизайн, не дефект. | [`me_response.py:22`](../../src/core/api/me_response.py), [`security.py:64`](../../src/core/api/security.py) | (Опц.) в api-reference уточнить: для OAuth/GPT-токенов `email` структурно `null` при `email_verified:true`; потребителю не трактовать `email_verified` как «есть подтверждённый адрес» без проверки `email != null`. |
| **F3** | **LOW** | **Traceability: t04 синтетический.** Backlog-стори нумерует 3 подзадачи (T01–T03, [story:22-24](../tasks/backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md)), pipeline исполнил 4 (добавил t04 «story acceptance verification»). «4/4 tasks» в индексе считает t04, которого нет в backlog-нумерации. Не дефект — идентичный доброкачественный паттерн, что G4 аудита AUTHCORE-02. | [`bullrun:772`](../tasks/bullrun-launch-index.md) vs [`story:22-24`](../tasks/backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md) | Системный паттерн pipeline (synthetic acceptance-task); фикса не требует — при желании явно пометить t04 как pipeline-generated в шаблоне run-summary. |

---

## Итог для индекса

- Статусы task/story ONB-01 в `bullrun-launch-index.md` — **факт-верны** (pipeline pkg-000045 актуализировал: [11], [16 G1🟢], [158-160], [769-772], [835]); drift не найден, правок статусов нет.
- **Бывший G1 (MEDIUM) аудита AUTHCORE-02 — 🟢 закрыт:** CAB-02 identity = 3/3 (`email`+`created_at`+`account_status`).
- Findings F1–F3 — все LOW: F1 (обратный SPA-drift, spa-сторона), F2 (семантика `email_verified`, documented/accepted), F3 (нумерация t04, системный паттерн).
- **Состояние доков:** [`identity-mvp-dashboard.md`](../tasks/identity-mvp-dashboard.md) счётчики уже актуальны (pipeline pkg-000045: 34/4 Done, 89%, onboarding 1/1, ONB-01 из Remaining убран) — добавлен лишь pointer на этот аудит. Остаточный drift (⚪ Todo при факте 🟢) исправлен под факт (`analysis.mdc` «fix discrepancies»): [`EPIC-IDS-ONBOARDING.md:30`](../tasks/backlog-stories/identity-onboarding/EPIC-IDS-ONBOARDING.md) (⚪→🟢) + AUTHCORE-02 email-разграничение (обе копии backlog+materialized, ⚪→🟢). Датированные analysis-снимки (`identity-mvp-readiness-2026-06-26`, `backlog-status-audit-2026-07-09`) — point-in-time, не ретро-правятся.
