## Task workspace — `task-ids-12-05-t02-no-expose-service-role-guard-tests`

- Story: [`../STORY-IDS-SEC-04-service-role-isolation.md`](../STORY-IDS-SEC-04-service-role-isolation.md)
- Prerequisite: [`task-ids-12-05-t01-service-role-boundary-docs-sync`](../task-ids-12-05-t01-service-role-boundary-docs-sync/README.md) (docs invariant; tests independent but same story)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000043`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md) Scope §No-expose guard; Story AC #2  
---

## Task: tests — prove service_role not exposed in logs/responses/trace/errors

### Цель
Подтвердить no-expose guard: `service_role` не попадает в логи, HTTP-ответы, trace и сообщения об ошибках — Story AC #2.

### Почему это важно
Утечка привилегированного ключа через observability или error envelope — критический security incident.

### Факты из кода
1. Backlog grep `log|print|debug` + `service_role` → пусто (baseline correct).
2. Error envelope — [`envelope.py`](../../../../../../../src/core/api/envelope.py).
3. Handlers — [`handlers.py`](../../../../../../../src/core/api/handlers.py).

### Gap / Проблема
Нет автоматизированного теста/линта, подтверждающего no-expose при регрессиях.

### AC/DoD
- [x] (P0) New `tests/test_service_role_no_expose.py` (or extend existing security test module).
- [x] (P0) Static grep gate in DoD: src без log/print/debug of service_role value.
- [x] (P0) Offline test: simulated error paths не содержат `SUPABASE_SERVICE_ROLE` / raw key in response body.
- [x] (P1) Story AC #2.

### Где менять код
- `doge-identity-service/tests/test_service_role_no_expose.py` (new at P3)

### Out of scope
- Boundary docs (t01)
- Rotation runbook (t03)
- Changing auth/login model (SEC-05)

### Проверка
```bash
cd doge-identity-service
grep -rn 'log\|print\|debug' src/ | grep -i service_role && exit 1 || true
.venv/bin/python -m pytest tests/test_service_role_no_expose.py -q
```
