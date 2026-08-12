## Task workspace — `task-ids-10-09-t03-supabase-phone-audit-log-repository`

- Story: [`../STORY-IDS-PV-09-durable-phone-persistence.md`](../STORY-IDS-PV-09-durable-phone-persistence.md)
- Prerequisite: [`task-ids-10-09-t01-phone-persistence-migration-sql`](../task-ids-10-09-t01-phone-persistence-migration-sql/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000039`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md) Scope §«Durable phone-audit repo»; Story AC #2, #3, #7  
---

## Task: implement — SupabasePhoneAuditLogRepository

### Цель
Реализовать `SupabasePhoneAuditLogRepository` в `db_supabase.py` — drop-in замена `InMemoryPhoneAuditLogRepository` по протоколу `PhoneAuditLogRepository`.

### Почему это важно
Phone audit теряется на редеплое (G-2a); durable repo закрывает security journal gap.

### Факты из кода
1. In-memory impl: [`repositories.py:362+`](../../../../../../../src/core/infrastructure/repositories.py) — `InMemoryPhoneAuditLogRepository`.
2. Контракт: [`contracts.py:97-106`](../../../../../../../src/core/domain/contracts.py) — `log_event` / `list_events`.
3. Модель: [`models.py:93-103`](../../../../../../../src/core/domain/models.py) — `PhoneAuditEvent` incl. `ip_hash`/`user_agent_hash` (SEC-02 fields — **storage only**, no new hashing).
4. eID audit precedent: [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) — `SupabaseEIDAuditLogRepository` pattern.
5. Schema from t01 migration.

### Gap / Проблема
Нет Supabase-реализации phone audit repo; только in-memory.

### AC/DoD
- [x] (P0) `SupabasePhoneAuditLogRepository` implements `log_event` and `list_events`.
- [x] (P0) Maps `PhoneAuditEvent` fields incl. optional `ip_hash`/`user_agent_hash` columns (persist values as-is; **no new IP/UA hashing logic**).
- [x] (P0) Protocol parity with `InMemoryPhoneAuditLogRepository`.
- [x] (P1) Traceability: Story AC #2 (audit survives repo rebuild), #3 (protocol parity), #7 (no IP/UA logic added).

### Где менять код
- `doge-identity-service/src/core/infrastructure/db_supabase.py` (new class)

### Out of scope
- IP/UA hashing implementation (SEC-02)
- DI backend switch (t04)
- Migration SQL (t01)
- Session store (t02)

### Проверка
```bash
cd doge-identity-service
grep -n 'SupabasePhoneAuditLogRepository' src/core/infrastructure/db_supabase.py
python3 -m pytest -m "not live_integration" -q
```
