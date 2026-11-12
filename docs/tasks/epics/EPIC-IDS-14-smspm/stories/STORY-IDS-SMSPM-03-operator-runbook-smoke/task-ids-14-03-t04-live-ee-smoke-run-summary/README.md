## Task workspace — `task-ids-14-03-t04-live-ee-smoke-run-summary`

- Story: [`../STORY-IDS-SMSPM-03-operator-runbook-smoke.md`](../STORY-IDS-SMSPM-03-operator-runbook-smoke.md)
- Prerequisite: t01–t03 runbook text; [SPIKE-01](../../../../../../backlog-stories/smspm/SPIKE-IDS-SMSPM-01-account-sender-setup.md) ops (out of queue)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** blocked  
**Wave:** `pkg-000048`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md) (T04, AC #4, D-03-3, D-03-4)  
---

## Task: execute — live EE smoke + run-summary (PASS or BLOCKED)

### Цель
После SPIKE: live request → SMS на EE → confirm → `/me` `phone_verified` + `phone_provider=smspm`. Краткий summary в `docs/tasks/run-reports/` (дата, env **names** без секретов, pass/fail) — D-03-3. **Не изобретать live PASS.**

### Почему это важно
Story AC #4 — единственный live-гейт. Без creds SPIKE задача остаётся в очереди как **BLOCKED**, не как PASS.

### Факты из кода
1. SPIKE-01 ⚪ Todo [`SPIKE-IDS-SMSPM-01-account-sender-setup.md`](../../../../../../backlog-stories/smspm/SPIKE-IDS-SMSPM-01-account-sender-setup.md) — ops, не в pkg.
2. Обязательные env [`config.py:12`](../../../../../../../src/core/phone/smspm/config.py) — `SMSPM_HASH`, `SMSPM_TOKEN`, `SMSPM_FROM`.
3. Curl-шаблон после t02 — [`phone-sms-verification.md`](../../../../../../runbook/phone-sms-verification.md) режим C.
4. Каталог evidence: `doge-identity-service/docs/tasks/run-reports/` (D-03-3); P3-имя: `identity-build-windows/run-summary-<P3-prefix>-epic-ids-14-smspm-03-live-ee-smoke.md`. Prefix только из `--print-utc-now` на P3.
5. Gate `Date:` — не в P1.

### Gap / Проблема
Live EE smoke и run-summary отсутствуют. Creds могут быть недоступны (SPIKE Todo) — это BLOCKED, не skip-as-PASS.

### AC/DoD
- [ ] (P0) **PASS:** live smoke на тестовом EE (`+372` prefix only in git, не полный MSISDN); `/me` `phone_verified` + `phone_provider=smspm`; summary без секретов/PII (D-03-3, D-03-4).
- [x] (P0) **или BLOCKED:** `SMSPM_HASH`/`TOKEN`/`FROM` unset **или** SPIKE T01–T05 не Done. `acceptance-verification-task-ids-14-03-t04-live-ee-smoke-run-summary.md` Result **BLOCKED** + факты (путь SPIKE status; env names missing). Optional BLOCKED run-summary `result: BLOCKED` — **never** `PASS`.
- [x] (P1) Не стартовать SMSPM-04. Не реализовывать SPIKE. Не править `src/`. Не коммитить `.env` секреты.

### Где менять код
- `doge-identity-service/docs/tasks/run-reports/identity-build-windows/run-summary-<P3-prefix>-epic-ids-14-smspm-03-live-ee-smoke.md` (**new** at P3)
- `acceptance-verification-task-ids-14-03-t04-live-ee-smoke-run-summary.md` (**new** at P3; PASS | BLOCKED)

### Out of scope
- Runbook text (t01–t03)
- SPIKE account setup
- Product `src/`
- Invented live PASS

### Проверка
```bash
# P3 only — Date from --print-utc-now; do not invent PASS
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now
# PASS path: operator curl from runbook C with real EE number; then:
ls doge-identity-service/docs/tasks/run-reports/identity-build-windows/run-summary-*-epic-ids-14-smspm-03-live-ee-smoke.md
rg -n 'PASS|BLOCKED|SMSPM_HASH|phone_provider' doge-identity-service/docs/tasks/run-reports/identity-build-windows/run-summary-*-epic-ids-14-smspm-03-live-ee-smoke.md
# BLOCKED path: if env missing, write BLOCKED acceptance — do not create a PASS summary
```
