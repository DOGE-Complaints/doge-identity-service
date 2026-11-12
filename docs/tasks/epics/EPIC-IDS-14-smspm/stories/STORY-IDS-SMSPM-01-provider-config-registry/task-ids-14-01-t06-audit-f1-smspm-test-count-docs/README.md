## Task workspace — `task-ids-14-01-t06-audit-f1-smspm-test-count-docs`

- Story: [`../STORY-IDS-SMSPM-01-provider-config-registry.md`](../STORY-IDS-SMSPM-01-provider-config-registry.md)
- Prerequisite: [`task-ids-14-01-t05-story-acceptance-verification`](../task-ids-14-01-t05-story-acceptance-verification/README.md)
- Audit source: [`../../../../../../analysis/identity-smspm-01-code-audit-2026-08-20.md`](../../../../../../analysis/identity-smspm-01-code-audit-2026-08-20.md) (F1)
- P5 scaffold: `2026-08-20T10:10:04Z` (`--print-utc-now` apply-session). Gate `Date:` — only after P6 live verify.

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_14_smspm_01_audit_2026_08_20`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/identity-smspm-01-code-audit-2026-08-20.md`](../../../../../../analysis/identity-smspm-01-code-audit-2026-08-20.md) §Gaps F1  
---

## Task: docs — SMSPM pytest file counter 12→11 in t05 gate + run-summary (F1)

### Цель
В P3-артефактах SMSPM-01 заменить ложный счётчик `pytest tests/test_smspm_config.py` → «12 passed» на **11 passed**, совпадающий с collect/run файла.

### Почему это важно
Audit F1 LOW: полная сюита «417 passed, 12 deselected» верна; счётчик **файла** SMSPM-тестов завышен на 1. Не дефект продукта; ложный evidence в gate/run-summary.

### Факты из кода
1. t05 gate [`acceptance-verification-task-ids-14-01-t05-story-acceptance-verification.md:25`](../task-ids-14-01-t05-story-acceptance-verification/acceptance-verification-task-ids-14-01-t05-story-acceptance-verification.md) — комментарий `# 12 passed`.
2. run-summary [`run-summary-20260820-0959-epic-ids-14-smspm-01-pkg-000046.md:25`](../../../../../../run-reports/identity-build-windows/run-summary-20260820-0959-epic-ids-14-smspm-01-pkg-000046.md) — `# 12 passed`.
3. [`tests/test_smspm_config.py`](../../../../../../../tests/test_smspm_config.py) — 11 `def test_*` (строки 38, 44, 49, 54, 59, 64, 75, 80, 85, 96, 101). Audit collect-list = 11.

### Gap / Проблема
Off-by-one в двух persistent P3-артефактах. Статусы 🟢 story/t01–t05 не менять.

### AC/DoD
- [x] (P0) t05 gate: `# 12 passed` → `# 11 passed`.
- [x] (P0) run-summary: `# 12 passed` → `# 11 passed`.
- [x] (P1) Не менять `src/`, pytest, 🟢 статусы SMSPM-01 t01–t05 / story Done.
- [x] (P1) Не перештамповывать t05 gate `Date:` без нового live-run.
- [x] (P1) `acceptance-verification-task-ids-14-01-t06-audit-f1-smspm-test-count-docs.md` PASS (`Date:` только P6 + `--print-utc-now`).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-01-provider-config-registry/task-ids-14-01-t05-story-acceptance-verification/acceptance-verification-task-ids-14-01-t05-story-acceptance-verification.md`
- `doge-identity-service/docs/tasks/run-reports/identity-build-windows/run-summary-20260820-0959-epic-ids-14-smspm-01-pkg-000046.md`

### Out of scope
- Runbook `phone-sms-verification.md` (F2 → SMSPM-03)
- HTTP send (SMSPM-02)
- Product `src/` / новые тесты
- Новый `pkg-*.yaml`, смена `identity-active-package.current.yaml`

### План выполнения (P6, не P5)
1. Заменить два комментария `12 passed` → `11 passed`.
2. `rg -n '12 passed'` по двум файлам — 0 hits на SMSPM file-counter; `11 passed` присутствует.
3. Написать acceptance-verification t06 с live `--print-utc-now` для `Date:`.

### Проверка
```bash
rg -n '12 passed|11 passed' \
  doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-01-provider-config-registry/task-ids-14-01-t05-story-acceptance-verification/acceptance-verification-task-ids-14-01-t05-story-acceptance-verification.md \
  doge-identity-service/docs/tasks/run-reports/identity-build-windows/run-summary-20260820-0959-epic-ids-14-smspm-01-pkg-000046.md
```
