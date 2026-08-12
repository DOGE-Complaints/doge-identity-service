## Task workspace — `task-ids-06-04-t02-integration-live-workflow-and-secrets-doc`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000008`  
**Decision Ref:** [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 4  
**Story:** [`../STORY-IDS-06-04-ci-workflows-offline-live.md`](../STORY-IDS-06-04-ci-workflows-offline-live.md)  
---

## Task: implement — integration-live workflow and secrets documentation

### Цель
Создать `.github/workflows/integration-live.yml` (L236–239) и задокументировать GitHub Secrets (L240–243) в runbook.

### Почему это важно
Live integration только на `main` / `workflow_dispatch` с `SUPABASE_TEST_*` secrets (epic Story 4).

### Факты из кода
1. Epic L236–239 — env mapping `secrets.SUPABASE_TEST_URL` → `SUPABASE_URL`, etc.; `EID_PROVIDER=mock`.
2. [`docs/runbook/supabase-project-setup.md`](../../../../../../../docs/runbook/supabase-project-setup.md) — IDS-05 t02 уже описывает CI secrets layout; **расширить**, не противоречить.
3. [`.github/workflows/integration-live.yml`](../../../../../../../.github/workflows/integration-live.yml) — **отсутствует**.

### Gap
Live CI workflow и cross-link secrets doc не реализованы.

### AC/DoD
- [x] (P0) `integration-live.yml`: triggers `push: branches: [main]`, `workflow_dispatch`.
- [x] (P0) Env: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE`, `SUPABASE_JWT_SECRET` from `SUPABASE_TEST_*` secrets; `DB_BACKEND=supabase`, `APP_PROFILE=demo`, `API_BASE_URL=https://test.local`, `EID_PROVIDER=mock`, `DOGESTONIA_EID_SECRET=ci-test-hash-secret`.
- [x] (P0) `python -m pytest -q -m live_integration -v`.
- [x] (P0) Runbook documents: `SUPABASE_TEST_URL`, `SUPABASE_TEST_SERVICE_ROLE_KEY`, `SUPABASE_TEST_JWT_SECRET`.

### Где менять код
- `doge-identity-service/.github/workflows/integration-live.yml` (новый)
- `doge-identity-service/docs/runbook/supabase-project-setup.md` (дополнение)

### Out of scope
- `test-offline.yml` — t01
- Story 4 acceptance — t03

### Проверка
```bash
# yaml lint / act optional; primary: manual workflow_dispatch after secrets set
```
