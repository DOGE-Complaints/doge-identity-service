## Task workspace — `task-ids-10-01-t05-offline-sms-registry-tests`

- Story: [`../STORY-IDS-PV-01-phone-provider-backbone.md`](../STORY-IDS-PV-01-phone-provider-backbone.md)
- Prerequisite: t04 (`MockSmsSender` + registry wiring)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000022`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md) AC #3, #5  
---

## Task: test — offline SMS registry guard, build, and mock.send

### Цель
Покрыть offline-тестами guard реестра, сборку active+mock, и `mock.send` round-trip — Story AC #3, #5.

### Почему это важно
Без тестов guard может регрессировать в `KeyError`; mock.send — smoke для будущего OTP flow (PV-05).

### Факты из кода
1. eID registry test образец: [`test_eid_provider_registry.py`](../../../../../../../tests/test_eid_provider_registry.py).
2. t03 guard: `SmsProviderNotRegisteredError` extends `ConfigError`.
3. **PV-01 boundary:** tests use `SimpleNamespace(sms_provider="unknown")` for unregistered active name until PV-02 adds `AppConfig.sms_provider`.
4. Baseline offline suite: 253 pytest (post EID-08).

### Gap / Проблема
Нет `tests/test_sms_provider_registry.py`; Story AC #5 open.

### AC/DoD
- [x] (P0) Test: `build_sms_registry` registers `mock` (and active when != mock).
- [x] (P0) Test: `registry.get("unknown")` raises `SmsProviderNotRegisteredError` with available names in message (Story AC #3).
- [x] (P0) Test: `get_active(SimpleNamespace(sms_provider="unknown"))` raises guard error, not `KeyError`.
- [x] (P0) Test: `mock.send(...)` returns `accepted=True`; message captured in mock store.
- [x] (P1) Full offline suite green: `pytest -m "not live_integration" -q`.

### Где менять код
- `doge-identity-service/tests/test_sms_provider_registry.py` (new)

### Out of scope
- `AppConfig` / `SMS_PROVIDER` env integration tests — PV-02
- Telnyx HTTP mocks — PV-06
- Story acceptance doc — t06

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_sms_provider_registry.py -m "not live_integration" -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
