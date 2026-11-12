## Task workspace — `task-ids-15-02-t02-api-docs-medata`

- Story: [`../STORY-IDS-VB-02-me-expose-identity-verified.md`](../STORY-IDS-VB-02-me-expose-identity-verified.md)
- Prerequisite: [`t01`](../task-ids-15-02-t01-me-response-identity-verified/README.md) (wire key locked)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000051`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md`](../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md) (Scope #4, AC docs, AUTHCORE-02 etalon)  
---

## Task: docs — MeData `identity_verified` in openapi + API_REFERENCE

### Цель
Document `identity_verified` on `MeData` in `openapi.yaml` and `API_REFERENCE.md`, with coexistence note for legacy method flags (etalon AUTHCORE-02 extend `/me`).

### Почему это важно
Story Scope #4 / AC docs: runtime consumer contract must match wire.

### Факты из кода
1. [`openapi.yaml`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) `MeData` — `phone_verified` present; **no** `identity_verified`.
2. [`API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) Me sample — phone fields; no opaque.
3. Etalon: AUTHCORE-02 / ONB-01 MeData extend patterns (story Verified).

### Gap / Проблема
API docs lag wire after t01.

### AC/DoD
- [x] (P0) `openapi.yaml` `MeData.identity_verified` boolean documented.
- [x] (P0) `API_REFERENCE.md` Me example/description includes `identity_verified` + coexistence with `phone_verified` / `eid_verified`.
- [x] (P1) No new HTTP path documented.

### Где менять код
- `doge-identity-service/docs/runtime-docs/api-reference/openapi.yaml`
- `doge-identity-service/docs/runtime-docs/api-reference/API_REFERENCE.md`

### Out of scope
- `me_response.py` impl (t01); tests (t03); gate (t04)

### Проверка
```bash
rg -n 'identity_verified' doge-identity-service/docs/runtime-docs/api-reference/openapi.yaml doge-identity-service/docs/runtime-docs/api-reference/API_REFERENCE.md
```
