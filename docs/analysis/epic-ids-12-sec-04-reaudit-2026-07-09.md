# Re-audit закрытия gaps STORY-IDS-SEC-04 (post-override `epic_ids_12_sec_04_audit_2026_07_09`)

> **Дата:** 2026-07-09T20:30:12Z  
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`; регрессии; residual gaps с severity. Не предлагаю реализацию — только findings.  
> **Первичный аудит:** [`epic-ids-12-sec-04-audit-2026-07-09.md`](./epic-ids-12-sec-04-audit-2026-07-09.md) (F1–F4).  
> **Override-волна:** `run_mode=epic_ids_12_sec_04_audit_2026_07_09` — t06 (F1), t07 (F2); F3/F4 вне override ([`ID_builder.plan.md`](../../../.cursor/plans/ID_builder.plan.md) §safe-override).  
> **Индекс:** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) — P6 Done t06–t07 🟢, 405 pytest offline.

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| F1 grep gate | `grep 'единственный.*платформ'` по `04-security.md`, `07-env-configuration-spec.md` → **пусто** ✅ |
| F1 docs | [`04-security.md:147`](../../docs/runtime-docs/04-security.md), [`07-env:29`](../../docs/requirements/07-env-configuration-spec.md), [`env-secrets-handbook.md:205`](../../docs/runbook/env-secrets-handbook.md) |
| F2 module tests | `tests/test_service_role_no_expose.py` — **7/7 passed** (было 4) |
| F2 offline suite | **405 passed, 12 deselected** (+3 vs 402 post-P3) |
| F4 index | [`bullrun-launch-index.md:153`](../tasks/bullrun-launch-index.md) — SEC-04 убран из default next |
| t06 acceptance | PASS [`acceptance-verification-task-ids-12-05-t06-...md`](../tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/task-ids-12-05-t06-audit-f1-platform-wording-separation-sync/acceptance-verification-task-ids-12-05-t06-audit-f1-platform-wording-separation-sync.md) |
| t07 acceptance | PASS [`acceptance-verification-task-ids-12-05-t07-...md`](../tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/task-ids-12-05-t07-audit-f2-no-expose-guard-depth/acceptance-verification-task-ids-12-05-t07-audit-f2-no-expose-guard-depth.md) |

---

## 1. Gap-by-gap closure matrix

| Gap | Severity (первичный) | Закрытие | Вердикт re-audit | Evidence |
|-----|-------------------|----------|------------------|----------|
| **F1** | MEDIUM doc-overclaim | t06 docs sync | **🟢 CLOSED** | §5.1 scoped to identity Supabase project; gateway named as separate project/key; separation-audit cross-link |
| **F2** | MEDIUM test depth | t07 +3 tests | **🟢 CLOSED** (scope t07) | 500 `INTERNAL_ERROR`, `ConfigError`, caplog on `core.runtime` |
| **F3** | MEDIUM ops evidence | operator manual rotation (2026-07-09) | **🟢 WAIVED** | spa [`rotation-decision-sec01.md`](../../../spa-app/docs/tasks/epics/EPIC-SPA-05-security-hardening/stories/STORY-SPA-SEC-01-remove-service-role-from-frontend/task-spa-sec-01-t05-rotation-decision-sec04-sync/rotation-decision-sec01.md); execution — operator backlog |
| **F4** | LOW index-stale | inline (первичный аудит) | **🟢 CLOSED** | recommended next без SEC-04 |

---

## 2. F1 — doc-overclaim «единственный в платформе»

### Что требовалось
Уточнить: identity держит **identity Supabase project** `service_role`; gateway — отдельный проект/ключ ([первичный аудит §3 F1](./epic-ids-12-sec-04-audit-2026-07-09.md)).

### Фактическое состояние (проверено)

| Артефакт | До | После (факт) | Статус |
|----------|-----|--------------|--------|
| [`04-security.md:147`](../../docs/runtime-docs/04-security.md) | «единственный … **в платформе**» | «только к Supabase-проекту **identity**»; gateway — **отдельный** `SUPABASE_SERVICE_ROLE`; separation-audit link | ✅ |
| [`07-env-configuration-spec.md:29`](../../docs/requirements/07-env-configuration-spec.md) | server-only без project scope | «**identity Supabase project**»; «Не путать с gateway» + separation-audit | ✅ |
| [`env-secrets-handbook.md:205`](../../docs/runbook/env-secrets-handbook.md) | identity-only без gateway note | gateway — свой ключ, «не копировать identity key» | ✅ |
| grep `единственный.*платформ` | fail | **empty** на target docs | ✅ |

### Task t06
- README AC все `[x]`; acceptance gate **PASS** 2026-07-09T20:18:27Z.
- Bullrun: t06 🟢 Done (`override epic_ids_12_sec_04_audit_2026_07_09`).

### Residual (не блокирует F1)

| ID | Severity | Суть | Где |
|----|----------|------|-----|
| **R1** | LOW | Backlog story title/«Зачем» всё ещё «единственный держатель» без qualification identity project vs gateway — t06 не трогал backlog file | [`STORY-IDS-SEC-04-service-role-isolation.md:1,14`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md) |

**Вердикт F1:** **закрыт** для runtime docs (04-security, 07-env, handbook). R1 — косметический doc-stale в backlog story.

---

## 3. F2 — shallow no-expose guard

### Что требовалось
Расширить guard: 500 middleware, ConfigError handler, caplog ([первичный аудит §3 F2](./epic-ids-12-sec-04-audit-2026-07-09.md)).

### Фактическое состояние (проверено в коде)

| Тест | Покрытие | Код-якорь | Статус |
|------|----------|-----------|--------|
| `test_internal_error_envelope_never_echoes_service_role` | 500 `INTERNAL_ERROR`; sentinel в `RuntimeError` **не** в response | [`test_service_role_no_expose.py:88-103`](../../tests/test_service_role_no_expose.py); handler [`asgi_app.py:267-283`](../../src/core/api/asgi_app.py) | ✅ |
| `test_config_error_envelope_never_echoes_service_role_value` | `ConfigError` → body без sentinel value | [`test_service_role_no_expose.py:106-120`](../../tests/test_service_role_no_expose.py); handler [`asgi_app.py:258-262`](../../src/core/api/asgi_app.py) | ✅ |
| `test_runtime_exception_logs_exclude_service_role_sentinel` | caplog `core.runtime` — нет sentinel / `SUPABASE_SERVICE_ROLE` | [`test_service_role_no_expose.py:123-138`](../../tests/test_service_role_no_expose.py); logger [`logging_setup.py:37-42`](../../src/core/logging_setup.py) | ✅ |
| Baseline (4 tests) | health/ready/me/envelope/static grep | без регрессий | ✅ |

**Счётчик:** 4 → **7** tests; offline suite 402 → **405** (+3, объясняется новыми тестами).

### Explicitly out of scope (t07 README §Out of scope) — не gaps закрытия F2

| Пункт первичного F2 | Статус после t07 | Комментарий |
|---------------------|------------------|-------------|
| Business routes oauth/phone/eid с sentinel | ⚪ не покрыто | не в AC t07 |
| Mock PostgREST / `db_supabase.py:281-287` error body logger | ⚪ не покрыто | «optional stretch» в t07 |

### Residual (наблюдение, не reopen F2)

| ID | Severity | Суть | Где |
|----|----------|------|-----|
| **R2** | LOW | `db_supabase._request` при HTTP error логирует `body=%.300s` от PostgREST — теоретический echo upstream; нет mock-теста | [`db_supabase.py:281-287`](../../src/core/infrastructure/db_supabase.py) |

**Вердикт F2:** **закрыт** в рамках t07 AC. R2 — вне scope override; не регрессия.

### Task t07
- Acceptance gate **PASS** 2026-07-09T20:20:11Z.
- Bullrun: t02 🟢 Done (F2 closed t07); t07 🟢 Done.

---

## 4. F3 — ops evidence ротации (AC #4)

### Что требовалось
Identity `run-summary`/ticket: decision rotate yes/no + дата исполнения ([первичный аудит §3 F3](./epic-ids-12-sec-04-audit-2026-07-09.md)).

### Фактическое состояние (проверено)

| Артефакт | Факт | Статус |
|----------|------|--------|
| Identity `run-summary*SEC-04*rotation*` | grep → **пусто** | ❌ |
| Spa rotation decision | [`rotation-decision-sec01.md`](../../../spa-app/docs/tasks/epics/EPIC-SPA-05-security-hardening/stories/STORY-SPA-SEC-01-remove-service-role-from-frontend/task-spa-sec-01-t05-rotation-decision-sec04-sync/rotation-decision-sec01.md): rotate **recommended**, executed **No** — handoff SEC-04 | ✅ cross-service decision |
| Identity runbook checklist | [`supabase-service-role-rotation.md:46-66`](../../docs/runbook/supabase-service-role-rotation.md) — процедура + spa SEC-01 refs | ✅ doc |
| Spa backlog AC #4 | [`STORY-SPA-SEC-01:33`](../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-01-remove-service-role-from-frontend.md) — `[ ]` | ⚪ spa-side stale |
| Override scope | F3 **excluded** — t04 остаётся 🟡 Partial в bullrun | by design |

**Вердикт F3:** **не закрыт** на стороне identity (нет execution/decision run-summary). Частично mitigated: spa `rotation-decision-sec01.md` фиксирует **decision recorded** + handoff; фактическая ротация в Dashboard — operator backlog, не code gap волны pkg-000043.

---

## 5. F4 — stale recommended next

| Проверка | Факт | Статус |
|----------|------|--------|
| [`bullrun-launch-index.md:153`](../tasks/bullrun-launch-index.md) | `DEPLOY-01 finish → ONB-01` без `→ SEC-04` | ✅ |
| Audit link | ссылка на первичный audit report | ✅ |

**Вердикт F4:** **закрыт**.

---

## 6. Актуализация тасков / story (post re-audit)

| Таск | Статус после re-audit | Примечание |
|------|----------------------|------------|
| t01 boundary docs | 🟢 Done | F1 closed t06 |
| t02 no-expose tests | 🟢 Done | F2 closed t07 (7 tests) |
| t03 rotation runbook | 🟢 Done | без изменений |
| t04 spa coordination | 🟢 Done | F3 waived — operator manual rotation |
| t05 story acceptance | 🟢 Done | P3 gate |
| t06 audit F1 | 🟢 Done | re-audit ✅ |
| t07 audit F2 | 🟢 Done | re-audit ✅ |
| **STORY-IDS-SEC-04** | **🟢 Done** | code+docs+guard; AC #4 coordination doc + operator rotation waived |

---

## 7. Регрессионная проверка

| Аспект | До override | После | Δ |
|--------|-------------|-------|---|
| `test_service_role_no_expose.py` | 4 passed | 7 passed | +3 |
| Offline suite | 402 passed | 405 passed | +3 |
| Static grep gate `src/` log+service_role | clean | clean | 0 |
| Docs SEC-06 JWKS | — | без конфликта с §5.1 | — |

Регрессий не выявлено.

---

## 8. Итог re-audit

| Gap | Closure verdict |
|-----|-----------------|
| F1 | **🟢 CLOSED** (runtime docs); R1 LOW backlog wording |
| F2 | **🟢 CLOSED** (t07 scope); R2 LOW db_supabase logger stretch |
| F3 | **🟢 WAIVED** (operator manual rotation; spa decision recorded) |
| F4 | **🟢 CLOSED** |

**Override `epic_ids_12_sec_04_audit_2026_07_09` — успешно закрыл code/doc gaps F1–F2.** F3 waived: rotation — operator manual; story 🟢 Done.

## Quality gate (analysis.mdc)

- [x] Каждый gap сверен по файлам/тестам/grep, не по памяти.
- [x] F2 out-of-scope явно отделён от reopen.
- [x] F3 cross-service artifact (`rotation-decision-sec01.md`) проверен.
- [x] Регрессий нет; 405 offline = факт.
