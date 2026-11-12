## Task workspace — `task-ids-15-02-t01-me-response-identity-verified`

- Story: [`../STORY-IDS-VB-02-me-expose-identity-verified.md`](../STORY-IDS-VB-02-me-expose-identity-verified.md)
- Prerequisite: VB-01 Done (`identity_verified` on `ProfileRecord`)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000051`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md`](../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md) (Scope #1–#3, AC-ID-THR-01/03/04, TECH-ARCH §2.1/§2.5)  
---

## Task: implement — expose `identity_verified` in `build_me_data`

### Цель
Extend `build_me_data` only: default `identity_verified=False`; if profile → `profile.identity_verified`. Keep emitting `phone_verified` / `eid_verified`. No new HTTP path.

### Почему это важно
AC-ID-THR-01/03/04: consumers read method-opaque wire key on existing `/me`.

### Факты из кода
1. [`me_response.py:17-51`](../../../../../../../src/core/api/me_response.py) — method flags present; **no** `identity_verified` key.
2. Route [`asgi_app.py:302`](../../../../../../../src/core/api/asgi_app.py) `@app.get("/me")` — do not add routes.
3. Persist field exists: [`models.py`](../../../../../../../src/core/domain/models.py) `identity_verified: bool` (VB-01).

### Gap / Проблема
`/me` `data` does not include opaque boolean.

### AC/DoD
- [x] (P0) `build_me_data` always includes `identity_verified` bool (default false when no profile).
- [x] (P0) With profile: value from `profile.identity_verified` (not derived from method flags at read time).
- [x] (P0) Legacy `phone_verified` / `eid_verified` still present (coexistence).
- [x] (P1) No new route in `asgi_app.py`; `account_status` not used as verified boolean.

### Где менять код
- `doge-identity-service/src/core/api/me_response.py`

### Out of scope
- openapi/API_REFERENCE (t02); tests (t03); story gate (t04); VB-03 write hooks

### Проверка
```bash
rg -n 'identity_verified' doge-identity-service/src/core/api/me_response.py
rg -n '@app\.(get|post).*me' doge-identity-service/src/core/api/asgi_app.py
```
