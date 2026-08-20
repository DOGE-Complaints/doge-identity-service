# Аудит: STORY-IDS-SMSPM-03 (operator runbook + live smoke) — 2026-08-20

> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями; регрессии; gaps с severity + как закрыть. Findings-only.
> **Объект:** pipeline [`STORY-IDS-SMSPM-03-operator-runbook-smoke`](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-03-operator-runbook-smoke/STORY-IDS-SMSPM-03-operator-runbook-smoke.md) · backlog [`STORY-IDS-SMSPM-03-operator-runbook-smoke`](../tasks/backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md) (pkg-000048).
> **Fence:** t01–t03 claimed PASS (режим C); t04/t05 claimed BLOCKED (SPIKE-01 Todo, `SMSPM_*` unset); нет `src/` в этой story. AC #4 live EE может быть OPEN. **Story Done ≠ BLOCKED live** — ниже раздельно.
> **Bullrun:** touchpoints в этом файле. Индекс VAL не правил. P5 не стартовать.

---

## Вердикт

**Product Story SMSPM-03 = ⚪ Todo — не Done.** Docs-часть (режим C) исполнена; live EE smoke **не** выполнен.

| Срез | Результат |
|------|-----------|
| **Story Done** | **нет** (Meta ⚪; INDEX Todo; dashboard Remaining) |
| **vs AC** | **1 OPEN / 4** — AC #1–#3 PASS; **AC #4 OPEN** |
| **P3 tasks** | t01–t03 🟢 Done; **t04/t05 ⚪ BLOCKED** |
| **`src/`** | pkg-000048 paths = только 5× task README под `docs/tasks/` ([`pkg-000048:11-16`](../tasks/identity-active-packages/pkg-000048-20260820-epic-ids-14-smspm-03-operator-runbook-smoke.yaml)); story «Вне scope» запрещает `src/` |

Не invent PASS live. BLOCKED-артефакт [run-summary](../tasks/run-reports/identity-build-windows/run-summary-20260820-1048-epic-ids-14-smspm-03-live-ee-smoke.md) `result: BLOCKED` — evidence отсутствия smoke, не замена AC #4.

---

## Bullrun status touchpoints (без правок индекса)

| Якорь | Строки | Заявлено | Факт | Вердикт |
|-------|--------|----------|------|---------|
| §Актуальная точка | [bullrun:11-13](../tasks/bullrun-launch-index.md) | SMSPM-03 ⚪ pkg-000048; t01–t03 🟢; t04/t05 BLOCKED | runbook C есть; live не run; SPIKE ⚪ | ✅ |
| input_mode / story | [bullrun:112](../tasks/bullrun-launch-index.md) | ⚪ Todo; t04/t05 BLOCKED | pipeline/backlog Meta ⚪; AC #4 `[ ]` | ✅ |
| Active pkg | [bullrun:114](../tasks/bullrun-launch-index.md) | pkg-000048 ⚪ 5 paths | yaml 5 README, без `src/` | ✅ |
| Epic EPIC-IDS-14 | [bullrun:179](../tasks/bullrun-launch-index.md) | 🟡; SMSPM-03 ⚪ | SMSPM-04 ещё backlog | ✅ |
| Task queue t01–t05 | [bullrun:825-829](../tasks/bullrun-launch-index.md) | t01–t03 🟢; t04/t05 ⚪ BLOCKED | gates PASS / BLOCKED ниже | ✅ |
| Stories SMSPM-03 | [bullrun:900](../tasks/bullrun-launch-index.md) | ⚪ Todo (t04 BLOCKED) | Meta ⚪ | ✅ нет drift 🟢 |

**Актуализация в отчёте:** статусы индекса **факт-верны**. Менять ⚪→🟢 нельзя, пока AC #4 OPEN.

---

## Пер-таск верификация

| Task | Требование | Факт | Вердикт |
|------|------------|------|---------|
| **t01** Env checklist режим C | `SMS_PROVIDER=smspm` + HASH/TOKEN/FROM + optional base URL, без секретов; не новый файл | [`phone-sms-verification.md:4`](../runbook/phone-sms-verification.md) три режима A/B/**C**; [`:54-62`](../runbook/phone-sms-verification.md) env-блок, значения пустые; Telnyx §B [`:44-51`](../runbook/phone-sms-verification.md) сохранён; второй SMSPM-runbook не создан (SSOT тот же файл); `SMSPM_REPORT_URL` в runbook нет | 🟢 Done (gate PASS) |
| **t02** Curl smoke | request → confirm → `/me`; mock+Telnyx остаются | §6C [`:145-163`](../runbook/phone-sms-verification.md); mock §5 [`:85-105`](../runbook/phone-sms-verification.md); Telnyx §6 [`:117-136`](../runbook/phone-sms-verification.md); `/me` ожидает `phone_verified` + `phone_provider: smspm` — поле есть в [`me_response.py:31-32,46-47`](../../src/core/api/me_response.py) (код SMSPM-02, не правка этой story) | 🟢 Done |
| **t03** Troubleshooting | missing creds, country/prefix, rate limit, SEND_FAILED | §7 [`:168-178`](../runbook/phone-sms-verification.md): CONFIG_ERROR для пустых `SMSPM_*`; COUNTRY_NOT_ALLOWED; RATE_LIMITED; SEND_FAILED (HTTP 503) — совпадает с [`handlers.py:97-99`](../../src/core/api/handlers.py) | 🟢 Done |
| **t04** Live EE + run-summary | после SPIKE: request→SMS→confirm→`phone_verified` / `phone_provider=smspm` | [run-summary](../tasks/run-reports/identity-build-windows/run-summary-20260820-1048-epic-ids-14-smspm-03-live-ee-smoke.md) **BLOCKED**; curl §6C **not run**; SPIKE-01 ⚪ [`:6`](../tasks/backlog-stories/smspm/SPIKE-IDS-SMSPM-01-account-sender-setup.md); process `SMSPM_HASH`/`TOKEN`/`FROM` unset-or-empty; dotenv keys **absent** (values not logged) | ⚪ **BLOCKED** |
| **t05** Story gate | все parent AC | [t05](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-03-operator-runbook-smoke/task-ids-14-03-t05-story-acceptance-verification/acceptance-verification-task-ids-14-03-t05-story-acceptance-verification.md) Result **BLOCKED**; AC #4 BLOCKED | ⚪ **BLOCKED** |

---

## Сверка Acceptance Criteria (verbatim backlog = pipeline)

Источник: backlog [`:55-59`](../tasks/backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md) = pipeline [`:58-62`](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-03-operator-runbook-smoke/STORY-IDS-SMSPM-03-operator-runbook-smoke.md).

| AC | Факт | Вердикт |
|----|------|---------|
| Режим C + env-чеклист (T01) | intro C + §2 режим C [`runbook:4,54-62`](../runbook/phone-sms-verification.md) | ✅ |
| Curl-путь (T02); Telnyx и mock описаны (D-03-2) | §6C + §5 A + §6 B | ✅ |
| Troubleshooting (T03) | §7 rows missing creds / prefix / cooldown / SEND_FAILED | ✅ |
| Live-smoke EE выполнен; summary без секретов/PII (T04, D-03-3) | summary **есть**, но `result: BLOCKED`; live **не** выполнен; полных MSISDN/секретов в summary нет | ❌ **OPEN** (F1) |

D-03-1: один файл runbook — ✅. D-03-2: Telnyx B на месте — ✅. D-03-4 критерий live не измерен (нет прогона).

---

## Регрессии

**Не найдено в docs этой волны** относительно mock/Telnyx: §5 и §6 сохранены. Webhook Telnyx строка в таблице эндпоинтов осталась. Sender/OTP (`src/`) вне pkg-000048.

---

## Gaps (findings)

| ID | Severity | Суть | Файл:строка | Как закрыть |
|----|----------|------|-------------|-------------|
| **F1** | **MEDIUM** | **AC #4 OPEN: live EE smoke не выполнен.** T04/T05 корректно BLOCKED: SPIKE-01 ⚪ Todo; `SMSPM_*` нет в process и нет nonempty в dotenv; curl §6C не гонялся. BLOCKED-summary **не** PASS (сам файл это фиксирует). Story Done запрещён. Не дефект runbook C. | [AC `[ ]` pipeline:62](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-03-operator-runbook-smoke/STORY-IDS-SMSPM-03-operator-runbook-smoke.md); [t04 gate](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-03-operator-runbook-smoke/task-ids-14-03-t04-live-ee-smoke-run-summary/acceptance-verification-task-ids-14-03-t04-live-ee-smoke-run-summary.md); [run-summary](../tasks/run-reports/identity-build-windows/run-summary-20260820-1048-epic-ids-14-smspm-03-live-ee-smoke.md); [SPIKE-01:6](../tasks/backlog-stories/smspm/SPIKE-IDS-SMSPM-01-account-sender-setup.md) | После SPIKE-01 Done + nonempty `SMSPM_HASH`/`TOKEN`/`FROM`: выполнить §6C (request → SMS EE → confirm → `/me` `phone_verified` + `phone_provider=smspm`); записать PASS summary без секретов/PII; тогда t04/t05 PASS и Meta 🟢. **Не invent PASS сейчас.** |

Наблюдения (не gap): env-чеклист — fenced `env`-блок, не markdown-таблица; AC говорит «чеклист». §6C вложен после Telnyx §6 — режим C находится.

---

## Итог / P5

- **Story Done: нет.** **vs AC: 1 OPEN (AC #4).** Docs AC 3/3 закрыты.
- **BLOCKED:** t04, t05. **Done:** t01–t03.
- Bullrun ⚪ / BLOCKED **совпадает** с диском; F1 = тот же OPEN AC, не index-drift.
- **P5 не стартовать** из VAL. Закрытие F1 = resume t04 после SPIKE (ops), не scaffold `src/`.
