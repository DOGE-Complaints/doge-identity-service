## Task workspace — `task-ids-05-05-t01-supabase-setup-runbook`

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000006`  
**Decision Ref:** [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 5  
**Story:** [`../STORY-IDS-05-05-supabase-project-setup-live-credentials.md`](../STORY-IDS-05-05-supabase-project-setup-live-credentials.md)  
---

## Task: add — Supabase project setup runbook

### Цель
Создать `docs/runbook/supabase-project-setup.md` с 6 шагами epic L188–194 (create project → API keys → migrations → `.env` → `make serve`).

### Почему это важно
Любой агент/оператор должен поднять identity на новом Supabase за фиксированный runbook без ad-hoc инструкций.

### Факты из кода
1. Epic L187–194 — runbook steps verbatim in Outputs.
2. [`docs/tech-requirements/impl-epic-05-supabase-persistence.md`](../../../../../../../docs/tech-requirements/impl-epic-05-supabase-persistence.md) §Story 5 — pattern source.
3. [`Makefile`](../../../../../../../Makefile) — `check-env`, `serve` targets (EPIC-IDS-01).
4. `docs/runbook/supabase-project-setup.md` — **отсутствует**.

### Gap
Нет документированного runbook для Supabase project bootstrap.

### AC/DoD
- [x] (P0) Runbook содержит шаги 1–6 из epic L188–194.
- [x] (P0) Ссылка на 5 migration files из Story 4 (ordered list).
- [x] (P1) Optional: `supabase db push` as optional step (epic L291).

### Где менять код
- `doge-identity-service/docs/runbook/supabase-project-setup.md` (новый)

### Out of scope
- GitHub Secrets layout — [`task-ids-05-05-t02-ci-test-secrets-layout`](../task-ids-05-05-t02-ci-test-secrets-layout/README.md)
- `make test-live` — EPIC-IDS-06

### Проверка
```bash
test -f doge-identity-service/docs/runbook/supabase-project-setup.md
grep -c 'SUPABASE_URL\|SUPABASE_SERVICE_ROLE\|SUPABASE_JWT_SECRET\|make serve' \
  doge-identity-service/docs/runbook/supabase-project-setup.md
```
