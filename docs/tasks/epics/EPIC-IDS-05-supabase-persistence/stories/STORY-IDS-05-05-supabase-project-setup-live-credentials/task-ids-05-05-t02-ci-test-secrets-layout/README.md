## Task workspace — `task-ids-05-05-t02-ci-test-secrets-layout`

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000006`  
**Decision Ref:** [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 5  
**Story:** [`../STORY-IDS-05-05-supabase-project-setup-live-credentials.md`](../STORY-IDS-05-05-supabase-project-setup-live-credentials.md)  
---

## Task: add — CI test secrets layout and .env.example alignment

### Цель
Документировать GitHub Secrets `SUPABASE_TEST_*` (epic L195–198) и обновить [`.env.example`](../../../../../../../.env.example) для supabase backend vars.

### Почему это важно
EPIC-IDS-06 live integration tests требуют отдельный тестовый Supabase project; prod/test isolation обязательна.

### Факты из кода
1. Epic L195–198 — `SUPABASE_TEST_URL`, `SUPABASE_TEST_SERVICE_ROLE_KEY`, `SUPABASE_TEST_JWT_SECRET`.
2. [`.env.example`](../../../../../../../.env.example) — exists (EPIC-IDS-01); verify supabase section completeness.
3. [`docs/tasks/epics/EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) — will consume test secrets.
4. Epic L202 — prod vs test URLs must differ.

### Gap
CI secrets layout not documented; `.env.example` may lack test-project guidance.

### AC/DoD
- [x] (P0) Runbook or README block documents 3 GitHub Secrets from epic L195–198.
- [x] (P0) `.env.example` includes `DB_BACKEND=supabase`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE`, `SUPABASE_JWT_SECRET` with comments.
- [x] (P1) Explicit note: test project URL ≠ production URL.

### Где менять код
- `doge-identity-service/.env.example`
- `doge-identity-service/docs/runbook/supabase-project-setup.md` (CI secrets section) or task README appendix

### Out of scope
- GitHub Actions workflow wiring — EPIC-IDS-06
- Story 5 live AC — [`task-ids-05-05-t03-story5-acceptance-verification`](../task-ids-05-05-t03-story5-acceptance-verification/README.md)

### Проверка
```bash
grep -E 'SUPABASE_URL|SUPABASE_SERVICE_ROLE|SUPABASE_JWT_SECRET|DB_BACKEND' doge-identity-service/.env.example
grep 'SUPABASE_TEST' doge-identity-service/docs/runbook/supabase-project-setup.md
```
