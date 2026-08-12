## Task workspace — `task-ids-10-03-t02-phone-verification-session-store-inmemory`

- Story: [`../STORY-IDS-PV-03-otp-engine-session.md`](../STORY-IDS-PV-03-otp-engine-session.md)
- Prerequisite: t01 (`PhoneVerificationSession`)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000024`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md) Scope bullet 1; AC #1  
---

## Task: implement — `PhoneVerificationSessionStore` protocol and in-memory store

### Цель
Формализовать `PhoneVerificationSessionStore` (supabase-совместимый Protocol) + `InMemoryPhoneVerificationSessionStore` — Story Scope store methods; AC #1.

### Почему это важно
OTP engine (t03–t04) и PV-05 flow нуждаются в persistence между request/confirm; образец [`VerificationSessionStore`](../../../../../../../src/core/domain/contracts.py:43-54) + [`InMemoryVerificationSessionStore`](../../../../../../../src/core/infrastructure/repositories.py:141-191).

### Факты из кода
1. eID store Protocol: [`contracts.py:43-54`](../../../../../../../src/core/domain/contracts.py).
2. In-memory impl pattern: [`repositories.py:141-191`](../../../../../../../src/core/infrastructure/repositories.py) (`create`, `get_by_id`, `mark_consumed`, `mark_failed`, `expire_pending`).
3. Supabase eID store exists ([`db_supabase.py:462+`](../../../../../../../src/core/infrastructure/db_supabase.py)) — phone store **not** implemented (defer).
4. Story requires `get_active_by_user` (phone-specific, not on eID store).

### Gap / Проблема
No `PhoneVerificationSessionStore`; no in-memory phone session persistence.

### AC/DoD
- [ ] (P0) `PhoneVerificationSessionStore` Protocol: `create`, `get_by_id`, `get_active_by_user`, `mark_consumed`, `mark_failed`, `expire_pending`.
- [ ] (P0) `InMemoryPhoneVerificationSessionStore` implements all methods; tracks `attempts` on session updates.
- [ ] (P0) `get_active_by_user(supabase_user_id)` returns latest `started` non-expired session or `None`.
- [ ] (P1) `expire_pending(now)` marks `started` sessions past `expires_at` as `expired`.

### Где менять код
- `doge-identity-service/src/core/domain/contracts.py`
- `doge-identity-service/src/core/infrastructure/repositories.py`

### Out of scope
- Supabase `PhoneVerificationSessionStore` — defer
- OTP engine — t03, t04
- Tests — t05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.infrastructure.repositories import InMemoryPhoneVerificationSessionStore; print(InMemoryPhoneVerificationSessionStore)"
```
