# Жёсткий аудит исполнения STORY-IDS-SEC-04 (service_role isolation)

> **Дата:** 2026-07-09T19:49:56Z  
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity. Не предлагаю реализацию — только findings.  
> **Предмет:** [`STORY-IDS-SEC-04-service-role-isolation`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md) vs фактический код и docs. Исполнена под **EPIC-IDS-12** (pkg-000043), 5 tasks.  
> **Доп. вход:** pipeline story [`STORY-IDS-SEC-04`](../tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/STORY-IDS-SEC-04-service-role-isolation.md); парная spa [`STORY-SPA-SEC-01`](../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-01-remove-service-role-from-frontend.md).  
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): Текущая волна pkg-000043 SEC-04 P3 Done (стр.11,762-766,792).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Config: `supabase_service_role` из env | [`schema.py:33,158-159,163-164,187,211`](../../src/core/config/schema.py) |
| Pilot fail-fast | [`schema.py:183-197`](../../src/core/config/schema.py) — `SUPABASE_SERVICE_ROLE` в `pilot_required` |
| Server-side PostgREST | [`db_supabase.py:231-259`](../../src/core/infrastructure/db_supabase.py) — `apikey` + `Authorization: Bearer` |
| DI / health probe | [`dependencies.py:92-102`](../../src/core/api/dependencies.py), [`providers.py:83-89`](../../src/core/infrastructure/providers.py) |
| No login routes | grep `/auth/login\|/auth/signup` по `src/` → пусто |
| Static grep gate (log/print/debug + service_role) | `src/` — offenders нет (исключение: `ValueError("service_role_key is required")` — имя поля, не значение) |
| Docs invariant | [`04-security.md:145-151`](../../docs/runtime-docs/04-security.md) §5.1; [`07-env-configuration-spec.md:29`](../../docs/requirements/07-env-configuration-spec.md); [`env-secrets-handbook.md:205`](../../docs/runbook/env-secrets-handbook.md) |
| Rotation runbook | [`supabase-service-role-rotation.md`](../../docs/runbook/supabase-service-role-rotation.md); index [`runbook/README.md:13`](../../docs/runbook/README.md) |
| Spa coordination § | [`supabase-service-role-rotation.md:46-66`](../../docs/runbook/supabase-service-role-rotation.md) |
| No-expose tests | `tests/test_service_role_no_expose.py` — **4 passed** |
| **Offline-сюита** | **402 passed, 12 deselected** ✅ (совпадает с индексом) |
| spa `.env` SERVICE_ROLE | grep `spa-app/.env` → пусто (2026-07-09) |
| Gateway `SUPABASE_SERVICE_ROLE` | [`doge-complaints-gateway/src/core/config/schema.py:498,523-525`](../../../doge-complaints-gateway/src/core/config/schema.py) — отдельный server env (свой Supabase-проект, см. separation-audit) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 Partial · ⚪ Todo. Сверено по коду и docs.

| Таск (EPIC-IDS-12, pkg-000043) | Факт | Статус |
|--------------------------------|------|--------|
| t01 service role boundary docs sync | §5.1 в 04-security, 07-env, env-secrets-handbook — инвариант есть; **overclaim «в платформе»** (F1) | 🟢 |
| t02 no expose service role guard tests | 4 теста + static grep; **нет runtime-log / 500 / supabase-error paths** (F2) | 🟡 Partial |
| t03 service role rotation runbook | runbook + README link; Dashboard/triggers/rollback | 🟢 |
| t04 spa sec 01 coordination checklist | §Spa coordination в runbook; **нет evidence ротации** (F3) | 🟡 Partial |
| t05 story acceptance verification | acceptance doc PASS 2026-07-09; pytest 402 green | 🟢 |
| **STORY-IDS-SEC-04** | волна pkg-000043: docs + runbook + guard tests доставлены; AC #4 coordination — doc-only | **🟢 Done (волна); AC #4 ops — 🟡 Partial** |

---

## 2. Сверка Acceptance Criteria SEC-04 (по коду + тестам)

| AC (из backlog-story) | Факт | Вердикт |
|-----------------------|------|---------|
| Зафиксировано требование «identity — единственный держатель `service_role`; не в браузере» (04-security / 07-env / runbook) | Текст в целевых docs ✅; формулировка «единственный в платформе» расходится с gateway `SUPABASE_SERVICE_ROLE` (другой проект/ключ) — F1 | ✅ для identity↔spa границы; ⚠️ wording |
| No-expose подтверждён (нет в логах/ответах/trace) — проверяемо | `/health`, `/ready`, `/me` 401, envelope builders — sentinel не утекает; static grep `src/` чист; **runtime logs и supabase error logger не покрыты** — F2 | ✅ as-built; 🟡 guard depth |
| Rotation runbook (Dashboard → identity env; триггеры) | [`supabase-service-role-rotation.md`](../../docs/runbook/supabase-service-role-rotation.md) — steps, triggers, rollback | ✅ |
| Ротация скоординирована с spa SEC-01 (если был фронт-bundle) | Runbook checklist + spa pipeline Done (pkg-000014); spa backlog AC `[ ]`; **нет run-summary/ticket о факте ротации identity key** — F3 | 🟡 doc ✅ / ops evidence ⚪ |

**Вывод:** волна pkg-000043 закрывает основной scope (identity server-only key, no spa/browser, runbook, automated guard baseline). Остатки: doc precision (F1), deeper no-expose coverage (F2), operational rotation evidence (F3).

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F1** | MEDIUM | Doc-overclaim | [`04-security.md:147`](../../docs/runtime-docs/04-security.md): «**Identity — единственный держатель** … **в платформе**» — при этом `doge-complaints-gateway` тоже конфигурирует `SUPABASE_SERVICE_ROLE` для **своего** Supabase-проекта ([`gateway/schema.py:523-525`](../../../doge-complaints-gateway/src/core/config/schema.py)). По [`supabase-project-separation-audit-2026-06-03.md`](./supabase-project-separation-audit-2026-06-03.md) — разные проекты/ключи; риск не в утечке identity-ключа в gateway, а в **неверной семантике инварианта**. Story AC #1 про «не в браузере» выполнен; claim «единственный в платформе» — завышен. **Как закрыть:** уточнить wording: «единственный держатель **identity Supabase project key**; gateway — отдельный проект/ключ»; не смешивать с spa `VITE_*`. | `04-security.md:147`, `07-env:29`, backlog story Scope |
| **F2** | MEDIUM | Test-coverage gap | [`test_service_role_no_expose.py`](../../tests/test_service_role_no_expose.py) покрывает `/health`, `/ready`, `/me` 401, envelope builders + static grep. **Не покрыто:** (a) middleware 500 `INTERNAL_ERROR` ([`asgi_app.py:267-283`](../../src/core/api/asgi_app.py)); (b) `ConfigError` handler ([`asgi_app.py:258-262`](../../src/core/api/asgi_app.py)); (c) бизнес-роуты oauth/phone/eid с sentinel env; (d) runtime log capture — только static line-grep, не pytest caplog; (e) `db_supabase` error logger `body=%.300s` ([`db_supabase.py:281-287`](../../src/core/infrastructure/db_supabase.py)) при гипотетическом echo ключа upstream. **Как закрыть:** расширить guard-тесты на 500/ConfigError paths + caplog assertion; опционально contract-test что PostgREST error body не содержит `apikey`. | `tests/test_service_role_no_expose.py`, `db_supabase.py:281-287` |
| **F3** | MEDIUM | Ops-evidence gap (AC #4) | Runbook §Spa coordination описывает порядок и checklist ([`supabase-service-role-rotation.md:46-66`](../../docs/runbook/supabase-service-role-rotation.md)). Spa pipeline SEC-01 🟢 ([`STORY-SPA-SEC-01` pipeline](../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-01-remove-service-role-from-frontend.md):6), guards в spa CI есть. **Нет** identity `run-summary`/ticket с датой ротации identity `SUPABASE_SERVICE_ROLE` после инцидента spa `.env` (grep `run-summary*rotation|SEC-04` → пусто). Spa backlog AC #4 «решение по ротации» — `[ ]` (стр.33). **Как закрыть:** операторский run-summary с decision (rotate yes/no + rationale) + ссылка spa SEC-01; при rotate — зафиксировать дату в runbook checklist. | runbook §Spa coordination; spa backlog AC |
| **F4** | LOW | Index-stale | [`bullrun-launch-index.md:150`](../tasks/bullrun-launch-index.md) — recommended next всё ещё содержит `SEC-04`, хотя SEC-04 🟢 Done (стр.11,792). **Как закрыть:** убрать SEC-04 из default next; оставить DEPLOY-01 → ONB-01. | `bullrun-launch-index.md:150` |

Наблюдения (severity none/LOW, **не gaps волны**):

- **O1 (none):** `service_role` читается только server-side; в HTTP `/ready` отдаётся `db_checks` как booleans ([`handlers.py:46-51`](../../src/core/api/handlers.py)) — ключ не сериализуется.
- **O2 (none):** `ConfigError` / `providers.py` сообщения содержат **имена** env vars, не значения ([`schema.py:164`](../../src/core/config/schema.py), [`providers.py:85`](../../src/core/infrastructure/providers.py)).
- **O3 (LOW, hygiene):** локальный `doge-identity-service/.env` содержит реальный JWT `service_role` (untracked; известно с EPIC-IDS-07 audit) — вне SEC-04 AC, но операторский риск утечки cwd `.env`.
- **O4 (none):** spa `grep SERVICE_ROLE` по `.env` пуст (2026-07-09) — согласуется с spa SEC-01 intent.

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **402 passed, 12 deselected** (совпадает с индексом и acceptance-verification) |
| SEC-04 guard module | 4/4 passed; аддитивный модуль, не ломает conftest |
| Существующие security тесты | `test_config_schema.py`, `test_asgi_transport.py` — без регрессий |
| Доки SEC-04 | аддитивные § в 04-security, 07-env, runbook — не конфликтуют с SEC-06 JWKS |

Регрессий не выявлено.

---

## 5. Итог

- **SEC-04 — 🟢 исполнена (волна pkg-000043):** identity server-only `SUPABASE_SERVICE_ROLE`, docs invariant, rotation runbook, spa coordination checklist, baseline no-expose tests (4) + static grep. AC #1–#3 ✅; AC #4 — doc ✅, ops evidence 🟡.
- **Findings:** **F1 (MEDIUM)** doc-overclaim «единственный в платформе»; **F2 (MEDIUM)** shallow no-expose test depth; **F3 (MEDIUM)** нет evidence фактической ротации; **F4 (LOW)** stale recommended next в индексе.
- **Регрессий нет** (402 passed).

## Quality gate (analysis.mdc)

- [x] Все claims с `file:line`; 5 тасков + story + 4 AC сверены по коду, docs и тестам.
- [x] Cross-service: spa SEC-01 + gateway separation проверены grep/read_file.
- [x] Findings отделены от наблюдений (O1–O4).
- [x] Регрессий нет; 402 offline = факт.
