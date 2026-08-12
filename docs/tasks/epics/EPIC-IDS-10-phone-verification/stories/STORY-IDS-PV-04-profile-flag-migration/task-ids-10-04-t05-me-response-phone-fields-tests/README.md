## Task workspace — `task-ids-10-04-t05-me-response-phone-fields-tests`

- Story: [`../STORY-IDS-PV-04-profile-flag-migration.md`](../STORY-IDS-PV-04-profile-flag-migration.md)
- Prerequisite: t02 `ProfileRecord` phone fields; t03 attach for test seeding

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000025`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md) Scope bullet 4; [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §4  
---

## Task: implement — GET `/me` phone fields + offline tests

### Цель
Расширить `build_me_data` phone-полями и покрыть тестами — Story Scope bullet 4 (`/me`).

### Почему это важно
Story AC #4: клиент видит `phone_verified` и связанные поля. Зеркало eID block в [`me_response.py:17-38`](../../../../../../../src/core/api/me_response.py) — **не** отдавать `verified_phone_hash` (PII/anti-enumeration, как `verified_person_hash`).

### Факты из кода
1. Current `/me` data: `eid_verified`, `eid_provider`, `eid_method`, `eid_country`, `eid_verified_at` only ([`me_response.py`](../../../../../../../src/core/api/me_response.py)).
2. Test fixture: [`test_me_profile.py`](../../../../../../../tests/test_me_profile.py) — `_seed_profile` builds `ProfileRecord` without phone fields.
3. Handler uses `build_me_data` — no handler change expected if envelope unchanged.

### Gap / Проблема
`/me` не возвращает phone verification status; consumers cannot distinguish verified phone users.

### AC/DoD
- [ ] (P0) `build_me_data` defaults: `phone_verified=False`, `phone_provider=None`, `phone_dial_prefix=None`, `phone_verified_at=None`.
- [ ] (P0) When profile present: map phone fields from `ProfileRecord`; `phone_verified_at` ISO formatted like `eid_verified_at`.
- [ ] (P0) `verified_phone_hash` **not** exposed in `/me` payload.
- [ ] (P0) Story AC #4: `test_me_profile.py` — verified phone profile returns expected fields.
- [ ] (P1) Story AC #5: full offline suite green after all t01–t05.

### Где менять код
- `doge-identity-service/src/core/api/me_response.py`
- `doge-identity-service/tests/test_me_profile.py`

### Out of scope
- HTTP phone flow endpoints — PV-05
- OpenAPI doc update — optional post-audit
- Telnyx — PV-06/07

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_me_profile.py -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
