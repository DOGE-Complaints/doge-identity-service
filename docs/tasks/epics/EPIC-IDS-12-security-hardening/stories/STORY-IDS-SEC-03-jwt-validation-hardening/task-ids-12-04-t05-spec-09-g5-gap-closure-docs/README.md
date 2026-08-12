## Task workspace — `task-ids-12-04-t05-spec-09-g5-gap-closure-docs`

- Story: [`../STORY-IDS-SEC-03-jwt-validation-hardening.md`](../STORY-IDS-SEC-03-jwt-validation-hardening.md)
- Prerequisite: [`task-ids-12-04-t02-confirm-octkey-import-form-live-token`](../task-ids-12-04-t02-confirm-octkey-import-form-live-token/README.md), [`task-ids-12-04-t03-aud-claim-registry-or-spec-waiver`](../task-ids-12-04-t03-aud-claim-registry-or-spec-waiver/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000038`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md) Scope §Согласование спеки и кода; Story AC #4  
---

## Task: fix — close G-5 spec/code gap in docs (spec 09 + runtime 04-security)

### Цель
Устранить открытые G-5 «честные note» в spec 09; обновить runtime as-built для `aud` и key import — Story Scope §Согласование, AC #4.

### Почему это важно
Story AC #4: нет открытых notes о несоответствии между `supabase_validator.py` и spec 09.

### Факты из кода
1. G-5 notes in spec — [`09-supabase-jwt-validation.md:48,99,126`](../../../../../../../docs/requirements/09-supabase-jwt-validation.md).
2. Runtime JWT section без `aud` — [`04-security.md:102-104`](../../../../../../../docs/runtime-docs/04-security.md).
3. Validator as-built — [`supabase_validator.py`](../../../../../../../src/core/auth/supabase_validator.py).

### Gap / Проблема
Spec и runtime docs всё ещё описывают G-5 как открытый gap после t02/t03.

### AC/DoD
- [ ] (P0) Remove/replace G-5 «честный note» blocks in spec 09; claims table matches code (aud + key import).
- [ ] (P0) Update [`04-security.md`](../../../../../../../docs/runtime-docs/04-security.md) §1 JWT checks — `aud` behavior and key import form as implemented.
- [ ] (P1) Story AC #4.
- [ ] (P1) No contradictory NB blocks left referencing open G-5.

### Где менять код
- `doge-identity-service/docs/requirements/09-supabase-jwt-validation.md`
- `doge-identity-service/docs/runtime-docs/04-security.md`

### Out of scope
- Validator code changes (t02–t03)
- RS256/JWKS
- Commits including `docs/tasks/**` (operator P8 policy)

### Проверка
```bash
cd doge-identity-service
grep -n "G-5\|честн" docs/requirements/09-supabase-jwt-validation.md || true
grep -n "aud\|OctKey" docs/runtime-docs/04-security.md docs/requirements/09-supabase-jwt-validation.md
```
