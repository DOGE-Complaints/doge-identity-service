## Task workspace — `task-ids-12-04-t03-aud-claim-registry-or-spec-waiver`

- Story: [`../STORY-IDS-SEC-03-jwt-validation-hardening.md`](../STORY-IDS-SEC-03-jwt-validation-hardening.md)
- Prerequisite: [`task-ids-12-04-t01-live-supabase-jwt-aud-decision-record`](../task-ids-12-04-t01-live-supabase-jwt-aud-decision-record/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000038`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md) Scope §Согласование спеки и кода; Story AC #1, #2 (conditional)  
---

## Task: implement — `aud` claim registry or spec waiver per t01 decision

### Цель
Реализовать ветку решения t01: зарегистрировать `aud=authenticated` в `JWTClaimsRegistry` **или** зафиксировать intentional non-validation в spec 09 — Story Scope §Согласование спеки и кода.

### Почему это важно
Закрывает функциональный разрыв G-5 по `aud` (или осознанный waiver) без регрессии остальных claims.

### Факты из кода
1. Registry essential claims — [`supabase_validator.py:18-22`](../../../../../../../src/core/auth/supabase_validator.py).
2. Separate `role` check — [`supabase_validator.py:34-35`](../../../../../../../src/core/auth/supabase_validator.py) (not `aud`).
3. `joserfc` registry pattern for `iss` — same file L19 `iss={"essential": True, "value": ...}`.

### Gap / Проблема
`aud` не валидируется при целевом требовании spec 09 (или waiver не задокументирован).

### AC/DoD
- [ ] (P0) If **validate** (t01): add `aud={"essential": True, "value": "authenticated"}` to `JWTClaimsRegistry`.
- [ ] (P0) If **waiver** (t01): spec 09 claims table states intentional non-validation + rationale; no registry change.
- [ ] (P0) `iss`/`sub`/`exp`/`role` behavior unchanged.
- [ ] (P1) Story AC #1 (implement half); AC #2 conditional on validate branch.

### Где менять код
- `doge-identity-service/src/core/auth/supabase_validator.py`
- `doge-identity-service/docs/requirements/09-supabase-jwt-validation.md` (waiver branch)

### Out of scope
- RS256/JWKS, ротация ключей
- OctKey import form (t02)
- Offline aud tests (t04)
- G-5 note removal (t05)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_supabase_jwt_validator.py -m "not live_integration" -q
grep -n "aud" src/core/auth/supabase_validator.py docs/requirements/09-supabase-jwt-validation.md
```
