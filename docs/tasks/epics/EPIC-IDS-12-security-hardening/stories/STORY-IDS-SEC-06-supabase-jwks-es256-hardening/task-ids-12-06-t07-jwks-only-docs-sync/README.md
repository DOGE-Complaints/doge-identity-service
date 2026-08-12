## Task workspace — `task-ids-12-06-t07-jwks-only-docs-sync`

- Story: [`../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md)
- Prerequisite: [`task-ids-12-06-t02-jwks-only-validator`](../task-ids-12-06-t02-jwks-only-validator/README.md), [`task-ids-12-06-t04-remove-supabase-jwt-secret`](../task-ids-12-06-t04-remove-supabase-jwt-secret/README.md)

---
**Приоритет:** P1  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000042`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md) §Подзадачи T07; Story AC #8  
---

## Task: docs — sync specs/runbooks to JWKS/ES256-only as-built

### Цель
Привести [`09`](../../../../../../../docs/requirements/09-supabase-jwt-validation.md), [`04-security.md`](../../../../../../../docs/runtime-docs/04-security.md), [`07-env-configuration-spec.md`](../../../../../../../docs/requirements/07-env-configuration-spec.md), runbooks к JWKS-only; синхронизировать [`test_supabase_runbook_docs.py`](../../../../../../../tests/test_supabase_runbook_docs.py).

### Почему это важно
Spec drift («MVP HS256» vs JWKS-only code) блокирует операторов; deploy validated via [`run-and-healthcheck.md`](../../../../../../runbook/run-and-healthcheck.md) (DEPLOY-01 retired 2026-07-09).

### Факты из кода
1. Req 09 — dual-path wording post-`09e1145` commit still mentions HS256+JWKS.
2. Runtime security — [`04-security.md`](../../../../../../../docs/runtime-docs/04-security.md) ~L104 dual path.
3. Env spec — [`07-env-configuration-spec.md`](../../../../../../../docs/requirements/07-env-configuration-spec.md) `SUPABASE_JWT_SECRET`.
4. Runbooks — [`supabase-project-setup.md`](../../../../../../../docs/runbook/supabase-project-setup.md), [`run-and-healthcheck.md`](../../../../../../../docs/runbook/run-and-healthcheck.md).
5. Doc tests — [`test_supabase_runbook_docs.py`](../../../../../../../tests/test_supabase_runbook_docs.py).

### Gap / Проблема
Documentation describes HS256 secret path; code target is JWKS-only (D-1/D-5).

### AC/DoD
- [ ] (P0) [`09-supabase-jwt-validation.md`](../../../../../../../docs/requirements/09-supabase-jwt-validation.md) — JWKS/ES256-only as-built; no «MVP выбор HS256» for Supabase validator.
- [ ] (P0) [`04-security.md`](../../../../../../../docs/runtime-docs/04-security.md) — single JWKS path for Supabase JWT (verify line range ~104).
- [ ] (P0) [`07-env-configuration-spec.md`](../../../../../../../docs/requirements/07-env-configuration-spec.md) — `SUPABASE_JWT_SECRET` removed.
- [ ] (P0) Runbooks — no required `SUPABASE_JWT_SECRET` for Cloud auth.
- [ ] (P0) `test_supabase_runbook_docs.py` green.
- [ ] (P1) Story AC #8 traceability.

### Где менять код
- `doge-identity-service/docs/requirements/09-supabase-jwt-validation.md`
- `doge-identity-service/docs/requirements/07-env-configuration-spec.md`
- `doge-identity-service/docs/runtime-docs/04-security.md`
- `doge-identity-service/docs/runbook/supabase-project-setup.md`
- `doge-identity-service/docs/runbook/run-and-healthcheck.md`
- `doge-identity-service/tests/test_supabase_runbook_docs.py`

### Out of scope
- OAuth server doc HS256 (14-oauth-server)
- Runtime code changes

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_supabase_runbook_docs.py -q
grep -n 'SUPABASE_JWT_SECRET\|MVP выбор.*HS256' docs/requirements/09-supabase-jwt-validation.md docs/requirements/07-env-configuration-spec.md || true
```
