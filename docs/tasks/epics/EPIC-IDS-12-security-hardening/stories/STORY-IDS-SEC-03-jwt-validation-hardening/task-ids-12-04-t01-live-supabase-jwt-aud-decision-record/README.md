## Task workspace — `task-ids-12-04-t01-live-supabase-jwt-aud-decision-record`

- Story: [`../STORY-IDS-SEC-03-jwt-validation-hardening.md`](../STORY-IDS-SEC-03-jwt-validation-hardening.md)
- Prerequisite: —

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000038`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md) Scope §Решение по `aud`; Story AC #1  
---

## Task: analyze — live Supabase JWT `aud` claim and decision record

### Цель
Зафиксировать фактическое значение `aud` в **реальном** Supabase access token и принять решение: валидировать `aud=authenticated` или осознанный waiver в spec 09 — Story Scope §Решение по `aud`, AC #1.

### Почему это важно
G-5: спека требует `aud`, код не проверяет; решение не должно опираться на синтетические тесты без live evidence.

### Факты из кода
1. `JWTClaimsRegistry` без `aud` — [`supabase_validator.py:18-22`](../../../../../../../src/core/auth/supabase_validator.py).
2. Spec целевое `aud=authenticated` + G-5 note — [`09-supabase-jwt-validation.md:43-48`](../../../../../../../docs/requirements/09-supabase-jwt-validation.md).
3. Synthetic tests включают `aud` в claims, но не assert rejection — [`test_supabase_jwt_validator.py:33-37`](../../../../../../../tests/test_supabase_jwt_validator.py).
4. Live creds pattern — [`tests/integration/supabase/conftest.py`](../../../../../../../tests/integration/supabase/conftest.py) `_require_supabase_creds_from_dotenv`.
5. Audit G-5 — [`identity-backend-full-audit-2026-06-24.md:63`](../../../../../../../docs/analysis/identity-backend-full-audit-2026-06-24.md).

### Gap / Проблема
Нет задокументированного решения по `aud`, основанного на live Supabase JWT payload.

### AC/DoD
- [ ] (P0) Получен и разобран **реальный** Supabase access JWT (live_integration test и/или operator-assisted decode); зафиксированы claims `aud`, `role`, `iss` (без публикации секрета/полного токена).
- [ ] (P0) Decision record: **validate** `aud=authenticated` **или** **waiver** с обоснованием в spec 09 / pipeline story decision block.
- [ ] (P1) Story AC #1 traceability.
- [ ] (P1) Блокирует t03 (ветка registry vs waiver).

### Где менять код
- `doge-identity-service/tests/integration/supabase/` (optional live sanity test, `@pytest.mark.live_integration`)
- `doge-identity-service/docs/requirements/09-supabase-jwt-validation.md` (decision paragraph — final wording may complete in t05)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-03-jwt-validation-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md` (optional decision block)

### Out of scope
- RS256/JWKS, ротация ключей, асимметричная проверка
- Изменение `iss`/`sub`/`exp`/`role` enforcement
- Реализация registry (t03)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/integration/supabase/ -m live_integration -k jwt -q
# или operator: decode live JWT header/payload (jq), record aud value in task notes
grep -n "aud" docs/requirements/09-supabase-jwt-validation.md
```
