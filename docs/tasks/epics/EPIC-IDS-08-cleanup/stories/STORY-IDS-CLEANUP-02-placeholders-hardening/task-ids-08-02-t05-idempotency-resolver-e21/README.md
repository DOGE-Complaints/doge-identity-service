## Task workspace — `task-ids-08-02-t05-idempotency-resolver-e21`

- Story: [`../STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../STORY-IDS-CLEANUP-02-placeholders-hardening.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-02-placeholders-hardening.md) Scope E21; [`../task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/owner-decisions-e17-e22.md`](../task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/owner-decisions-e17-e22.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000013`  
**Skill declared:** python-pro  
---

## Task: refactor — idempotency resolver (E21)

### Цель
Выполнить owner decision по E21: подключить `resolve_idempotency_key` к POST-операциям или убрать модуль/резолвер.

### Почему это важно
Helper создан в EPIC-IDS-02 ([`01-api`](../../../../../../../runtime-docs/01-api.md):50), но потребителей в prod routes нет (gap P6). Story AC #1, AC #3.

### Факты из кода
1. [`idempotency.py:6-11`](../../../../../../../src/core/api/idempotency.py) — `resolve_idempotency_key(headers)` case-insensitive.
2. Tests: [`tests/test_api_envelope.py:45-55`](../../../../../../../tests/test_api_envelope.py) — единственный runtime consumer.
3. Wiring: `asgi_app.py`, `handlers.py` — вызовов `resolve_idempotency_key` нет.
4. EPIC-IDS-02 Story 1 — resolver intentionally created; business routes deferred.

### Gap / Проблема
Idempotency-key резолвер без потребителей — placeholder под будущие POST.

### AC/DoD
- [ ] (P0) Story AC #1: решение E21 из t01 выполнено.
- [ ] (P0) Если «убрать»: Story AC #3 — `resolve_idempotency_key` / `idempotency.py` grep = 0 в `src/`; tests переписаны или удалены.
- [ ] (P0) Если «довести»: wiring к конкретному POST route (имя route — из t01 decision) + test.
- [ ] (P1) Offline pytest green.

### Где менять код
- [`src/core/api/idempotency.py`](../../../../../../../src/core/api/idempotency.py) — remove или keep + wire
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) / [`handlers.py`](../../../../../../../src/core/api/handlers.py) — если wire
- [`tests/test_api_envelope.py`](../../../../../../../tests/test_api_envelope.py)

### Out of scope
- Supabase `idempotency_keys` table persistence — EPIC-IDS-05 scope (already has repo infra in tech-requirements)
- Gateway intake idempotency

### Проверка
```bash
cd doge-identity-service
rg "resolve_idempotency_key|idempotency" src/
.venv/bin/python -m pytest tests/test_api_envelope.py -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
