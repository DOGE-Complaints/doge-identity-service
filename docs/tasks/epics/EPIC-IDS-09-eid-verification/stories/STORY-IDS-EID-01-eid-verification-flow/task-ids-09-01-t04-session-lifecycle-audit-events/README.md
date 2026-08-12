## Task workspace — `task-ids-09-01-t04-session-lifecycle-audit-events`

- Story: [`../STORY-IDS-EID-01-eid-verification-flow.md`](../STORY-IDS-EID-01-eid-verification-flow.md)
- Prerequisite: [`../task-ids-09-01-t03-mock-callback-orchestration/README.md`](../task-ids-09-01-t03-mock-callback-orchestration/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000015`  
**Skill declared:** python-pro  
---

## Task: implement — session lifecycle + audit events (no PII)

### Цель
Довести lifecycle сессии: `mark_consumed` / `mark_failed` / expired handling; idempotent replay повторного callback; `eid_audit_log_repository.log_event` на success/failure/conflict без PII.

### Почему это важно
Story Scope: callback + audit; AC #3, #5.

### Факты из кода
1. [`repositories.py:145-185`](../../../../../../../src/core/infrastructure/repositories.py) — `VerificationSessionStore` lifecycle methods.
2. [`contracts.py:56-65`](../../../../../../../src/core/domain/contracts.py) — `EIDAuditLogRepository.log_event`.
3. [`dependencies.py:45-46,96`](../../../../../../../src/core/api/dependencies.py) — audit repo в `ApiDependencies`.
4. [`models.py:44-59`](../../../../../../../src/core/domain/models.py) — session status fields.

### Gap / Проблема
t03 реализует happy path; нет terminal-state guard и полного audit trail.

### AC/DoD
- [x] (P0) Успешный callback → session `consumed`.
- [x] (P0) Повторный callback на consumed session — idempotent, не перезаписывает профиль (AC #3).
- [x] (P0) Expired session → корректная ошибка, профиль не меняется (AC #3).
- [x] (P0) Failure paths → `mark_failed` где применимо.
- [x] (P0) Audit events: started, success, failure, conflict — без PII в payload (AC #5).

### Где менять код
- `doge-identity-service/src/core/api/handlers.py`

### Out of scope
- eideasy/authentigate callbacks — EID-02
- Offline e2e tests — t05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q tests/test_inmemory_repositories.py -k session
```
