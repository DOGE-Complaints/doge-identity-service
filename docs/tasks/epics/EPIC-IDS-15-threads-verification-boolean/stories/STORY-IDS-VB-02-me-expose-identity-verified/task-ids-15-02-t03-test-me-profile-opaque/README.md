## Task workspace — `task-ids-15-02-t03-test-me-profile-opaque`

- Story: [`../STORY-IDS-VB-02-me-expose-identity-verified.md`](../STORY-IDS-VB-02-me-expose-identity-verified.md)
- Prerequisite: [`t01`](../task-ids-15-02-t01-me-response-identity-verified/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000051`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md`](../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md) (Scope #5, AC tests)  
---

## Task: test — `/me` opaque key offline coverage

### Цель
Extend `tests/test_me_profile.py`: key present; no-profile → false; with profile reflects persisted `identity_verified`; method fields still present.

### Почему это важно
Offline proof of AC-ID-THR-01/03/04 wire without live_integration.

### Факты из кода
1. [`test_me_profile.py`](../../../../../../../tests/test_me_profile.py) — seeds `identity_verified` on ProfileRecord; asserts `phone_verified` only (no opaque assertions yet).
2. Builder under test: `me_response.build_me_data` (t01).

### Gap / Проблема
No offline assertions for opaque `/me` key.

### AC/DoD
- [x] (P0) Assert `identity_verified` key present on `/me` data.
- [x] (P0) No-profile (or default path) → `false`.
- [x] (P0) Profile with `identity_verified=True` → response `true` (and False reflects persist).
- [x] (P0) Method fields `phone_verified` / `eid_verified` still present.
- [x] (P1) `pytest -m "not live_integration"` green for touched tests.

### Где менять код
- `doge-identity-service/tests/test_me_profile.py`

### Out of scope
- Docs (t02); story gate (t04); live_integration

### Проверка
```bash
cd doge-identity-service && python3 -m pytest -q tests/test_me_profile.py -m "not live_integration"
```
