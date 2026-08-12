## Task workspace — `task-ids-12-02-t04-cooldown-http-window-coexistence-policy`

- Story: [`../STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../STORY-IDS-SEC-01b-phone-request-http-rate-limit.md)
- Prerequisite: [`task-ids-12-02-t03-phone-request-route-wiring`](../task-ids-12-02-t03-phone-request-route-wiring/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000036`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md) Scope §политика; Story AC #2, #3  
---

## Task: implement — cooldown vs HTTP window coexistence policy (docs)

### Цель
Задокументировать политику: cooldown = **400** `RATE_LIMITED`; HTTP window = **429** `rate_limit_exceeded` + `retry_after` — Story Scope §политика, AC #2–#3.

### Почему это важно
Два независимых анти-абьюз-слоя на одном роуте; клиенты (spa-app, GPT) должны различать ответы.

### Факты из кода
1. Cooldown: [`handlers.py:456-473`](../../../../../../../src/core/api/handlers.py) → 400 `RATE_LIMITED`.
2. HTTP 429 envelope: [`envelope.py`](../../../../../../../src/core/api/envelope.py) `build_rate_limit_envelope`.
3. SEC-01 §8: [`04-security.md`](../../../../../../../runtime-docs/04-security.md) — phone follow-up note.
4. Split policy table: [`sec-01-g1-rate-limit-split-2026-06-26.md`](../../../../../../analysis/sec-01-g1-rate-limit-split-2026-06-26.md) §4.

### Gap / Проблема
As-built spec 19 / 04-security не описывают dual-layer policy для phone/request после wire.

### AC/DoD
- [ ] (P0) Story AC #2: documented 400 vs 429 semantics in runtime-docs + spec 19.
- [ ] (P0) Story AC #3: policy references analysis + `Depends` → handler → cooldown order.
- [ ] (P1) Handler comment clarifying layer separation (if not already sufficient from SEC-01).
- [ ] (P1) Scope §5: update [`04-security.md`](../../../../../../../runtime-docs/04-security.md) §8 and [`19-phone-verification-flow.md`](../../../../../../../requirements/19-phone-verification-flow.md).

### Где менять код
- `doge-identity-service/docs/runtime-docs/04-security.md`
- `doge-identity-service/docs/requirements/19-phone-verification-flow.md`
- `doge-identity-service/src/core/api/handlers.py` (comment only, optional)

### Out of scope
- Changing cooldown to 429
- Redis / gateway limits

### Проверка
```bash
grep -n "429\|RATE_LIMITED\|phone/request\|cooldown" \
  doge-identity-service/docs/runtime-docs/04-security.md \
  doge-identity-service/docs/requirements/19-phone-verification-flow.md
```
