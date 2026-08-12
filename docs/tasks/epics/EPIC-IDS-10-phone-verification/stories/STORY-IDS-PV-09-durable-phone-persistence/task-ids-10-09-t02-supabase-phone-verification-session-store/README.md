## Task workspace — `task-ids-10-09-t02-supabase-phone-verification-session-store`

- Story: [`../STORY-IDS-PV-09-durable-phone-persistence.md`](../STORY-IDS-PV-09-durable-phone-persistence.md)
- Prerequisite: [`task-ids-10-09-t01-phone-persistence-migration-sql`](../task-ids-10-09-t01-phone-persistence-migration-sql/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000039`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md) Scope §«Durable phone-session store»; Story AC #1, #3, #4  
---

## Task: implement — SupabasePhoneVerificationSessionStore

### Цель
Реализовать `SupabasePhoneVerificationSessionStore` в `db_supabase.py` — drop-in замена `InMemoryPhoneVerificationSessionStore` по протоколу `PhoneVerificationSessionStore`.

### Почему это важно
Pending OTP-сессии теряются на редеплое (G-3); durable store закрывает gap по образцу OAUTH-03.

### Факты из кода
1. In-memory semantics: [`repositories.py:284+`](../../../../../../../src/core/infrastructure/repositories.py) — `InMemoryPhoneVerificationSessionStore` (10 ops).
2. Контракт: [`contracts.py:74-93`](../../../../../../../src/core/domain/contracts.py) — `create` / `get_by_id` / `get_active_by_user` / `get_latest_for_confirm` / `get_by_provider_message_id` / `replace` / `mark_consumed` / `mark_failed` / `mark_expired` / `expire_pending`.
3. OAuth precedent: [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) — `SupabaseAuthorizationRequestStore` pattern.
4. **Нет** phone-session store в `db_supabase.py` сегодня.
5. Schema from t01 migration.

### Gap / Проблема
Нет Supabase-реализации phone session store; только in-memory.

### AC/DoD
- [x] (P0) `SupabasePhoneVerificationSessionStore` implements all `PhoneVerificationSessionStore` methods.
- [x] (P0) TTL/expiry semantics (`expires_at`, `started→expired`) enforced in store (mirror in-memory).
- [x] (P0) Protocol parity with `InMemoryPhoneVerificationSessionStore` — no contract change.
- [x] (P1) Traceability: Story AC #1 (session survives store rebuild), #3 (protocol parity), #4 (supabase path only — wiring in t04).

### Где менять код
- `doge-identity-service/src/core/infrastructure/db_supabase.py` (new class)

### Out of scope
- DI backend switch (t04)
- Migration SQL (t01)
- Audit repo (t03)
- IP/UA hashing (SEC-02)

### Проверка
```bash
cd doge-identity-service
grep -n 'SupabasePhoneVerificationSessionStore' src/core/infrastructure/db_supabase.py
python3 -m pytest -m "not live_integration" -q
```
