# EPIC-IDS-05 Re-audit Scaffold — mapping и артефакты (Plan only)

> **Дата:** 2026-06-02  
> **Режим:** P5 scaffold only — без runtime-кода и без `pytest` execution  
> **Методология:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc)

---

## Source files (SSOT)

| Роль | Путь |
|------|------|
| Re-audit findings | [`doge-identity-service/docs/tasks/epics/EPIC-IDS-05-supabase-persistence/re-audit-report-2026-06-02.md`](../tasks/epics/EPIC-IDS-05-supabase-persistence/re-audit-report-2026-06-02.md) |
| Epic | [`doge-identity-service/docs/tasks/epics/EPIC-IDS-05-supabase-persistence/EPIC-IDS-05-supabase-persistence.md`](../tasks/epics/EPIC-IDS-05-supabase-persistence/EPIC-IDS-05-supabase-persistence.md) |
| Bullrun index | [`doge-identity-service/docs/tasks/bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) |
| Default active pkg | [`doge-identity-service/docs/tasks/identity-active-packages/pkg-000006-20260530-epic-ids-05-supabase-persistence.yaml`](../tasks/identity-active-packages/pkg-000006-20260530-epic-ids-05-supabase-persistence.yaml) |
| Re-audit pkg (archival) | [`doge-identity-service/docs/tasks/identity-active-packages/pkg-000007-20260602-epic-ids-05-reaudit-gaps.yaml`](../tasks/identity-active-packages/pkg-000007-20260602-epic-ids-05-reaudit-gaps.yaml) |
| Active pointer (unchanged) | [`doge-identity-service/docs/tasks/identity-active-package.current.yaml`](../tasks/identity-active-package.current.yaml) → pkg-000006 |
| Override activation | [`.cursor/plans/ID_builder.plan.md`](../../../.cursor/plans/ID_builder.plan.md) §`run_mode=epic_ids_05_reaudit_2026_06_02` |

---

## Gap matrix (re-audit → story → task)

| Gap ID | Severity | Story | Task README | Status |
|--------|----------|-------|-------------|--------|
| RG-1 | HIGH | — (superseded STORY-IDS-05-06 t02) | — | superseded |
| S2-1 | MEDIUM | STORY-IDS-05-02 | [`task-ids-05-02-t04-audit-s2-1-oauth-store-env-doc/README.md`](../tasks/epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-02-supabase-repositories-identity-set/task-ids-05-02-t04-audit-s2-1-oauth-store-env-doc/README.md) | ⚪ Todo |
| S3-1 | MEDIUM | STORY-IDS-05-03 | [`task-ids-05-03-t04-audit-s3-1-dual-health-db-comment/README.md`](../tasks/epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-03-five-level-healthcheck/task-ids-05-03-t04-audit-s3-1-dual-health-db-comment/README.md) | ⚪ Todo |
| S1-1 | LOW | STORY-IDS-05-01 | [`task-ids-05-01-t03-audit-s1-1-empty-service-role-key-test/README.md`](../tasks/epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-01-supabase-database-http-client/task-ids-05-01-t03-audit-s1-1-empty-service-role-key-test/README.md) | ⚪ Todo |
| S2-2 | LOW | STORY-IDS-05-02 | [`task-ids-05-02-t05-audit-s2-2-mark-consumed-started-guard/README.md`](../tasks/epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-02-supabase-repositories-identity-set/task-ids-05-02-t05-audit-s2-2-mark-consumed-started-guard/README.md) | ⚪ Todo |
| S3-2 | LOW | STORY-IDS-05-03 | [`task-ids-05-03-t05-audit-s3-2-health-db-request-timeout/README.md`](../tasks/epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-03-five-level-healthcheck/task-ids-05-03-t05-audit-s3-2-health-db-request-timeout/README.md) | ⚪ Todo |

Все 5 task README существуют на диске (проверка `test -f`, 2026-06-02).

---

## Mapping: requirement → epic → story → tasks

Re-audit волна привязана к **эпику** (не отдельному requirement-doc). Требования эпика — из Inputs EPIC-IDS-05:

| Requirement (epic Inputs) | Epic | Story | Gap tasks |
|---------------------------|------|-------|-----------|
| [`docs/requirements/08-supabase-migrations.md`](../requirements/08-supabase-migrations.md) (schema, RLS context) | EPIC-IDS-05 | STORY-IDS-05-02 | S2-1 (OAuth store doc), S2-2 (`mark_consumed` guard) |
| [`docs/requirements/08-supabase-migrations.md`](../requirements/08-supabase-migrations.md) | EPIC-IDS-05 | STORY-IDS-05-03 | S3-1 (dual `health_db` comment), S3-2 (`request_timeout_s`) |
| EPIC-IDS-05 §6 Story 1 (`SupabaseDatabase` client) | EPIC-IDS-05 | STORY-IDS-05-01 | S1-1 (empty `service_role_key` test) |
| Re-audit report (closure verification) | EPIC-IDS-05 | STORY-IDS-05-06 | RG-1 — **superseded** (не в override-очереди) |

Источник привязки requirement→epic: [`EPIC-IDS-05-supabase-persistence.md`](../tasks/epics/EPIC-IDS-05-supabase-persistence/EPIC-IDS-05-supabase-persistence.md) §1, §3, §4.

---

## Activation

| Режим | Значение |
|-------|----------|
| **Default YAML SSOT** | `pkg-000006` via [`identity-active-package.current.yaml`](../tasks/identity-active-package.current.yaml) |
| **Gap execution (P6)** | `run_mode=epic_ids_05_reaudit_2026_06_02` — список в `ID_builder.plan.md` (5 README, порядок 1–5) |
| **Archival pkg mirror** | `pkg-000007` (`input_kind: epic_story_tree`, 5 paths, `decision_ref` = re-audit report) |

`builder_resolve_queue.py --project identity --verify` → `ok 17 paths` (active pkg-000006). pkg-000007 не переключает pointer — по контракту P5/P6 override.

---

## Что сделано в этой итерации (Plan only)

### Создано
- [`doge-identity-service/docs/tasks/identity-active-packages/pkg-000007-20260602-epic-ids-05-reaudit-gaps.yaml`](../tasks/identity-active-packages/pkg-000007-20260602-epic-ids-05-reaudit-gaps.yaml)
- [`doge-identity-service/docs/analysis/ids-05-reaudit-scaffold-mapping-2026-06-02.md`](./ids-05-reaudit-scaffold-mapping-2026-06-02.md) (этот файл)

### Обновлено
- [`doge-identity-service/docs/tasks/bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) — ссылка на pkg-000007 в re-audit gap queue и «Актуальная точка»
- [`doge-identity-service/docs/tasks/epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-01-supabase-database-http-client/STORY-IDS-05-01-supabase-database-http-client.md`](../tasks/epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-01-supabase-database-http-client/STORY-IDS-05-01-supabase-database-http-client.md) — §Re-audit gap overlay
- [`doge-identity-service/docs/tasks/epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-02-supabase-repositories-identity-set/STORY-IDS-05-02-supabase-repositories-identity-set.md`](../tasks/epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-02-supabase-repositories-identity-set/STORY-IDS-05-02-supabase-repositories-identity-set.md) — §Re-audit gap overlay
- [`doge-identity-service/docs/tasks/epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-03-five-level-healthcheck/STORY-IDS-05-03-five-level-healthcheck.md`](../tasks/epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-03-five-level-healthcheck/STORY-IDS-05-03-five-level-healthcheck.md) — §Re-audit gap overlay
- 5× task `README.md` — добавлен §Out of scope (остальные 8 секций task-standard уже были)

### Без изменений (намеренно)
- `doge-identity-service/src/**` — runtime не трогался
- `identity-active-package.current.yaml` — остаётся на pkg-000006 (default SSOT)
- `.cursor/plans/ids-05_re-audit_scaffold_ab2cfdd5.plan.md` — по инструкции оператора

### Уже было корректно (предыдущий scaffold)
- 5× gap task README с `Decision Ref` на re-audit report
- [`ID_builder.plan.md`](../../../.cursor/plans/ID_builder.plan.md) §`run_mode=epic_ids_05_reaudit_2026_06_02`
- Gap queue в `bullrun-launch-index.md`

---

## Следующий шаг (P6, вне этого плана)

Оператор: `run_mode=epic_ids_05_reaudit_2026_06_02` + `@ID_builder.plan.md` — исполнить 5 task README по порядку override, затем P7 re-audit по коду.
