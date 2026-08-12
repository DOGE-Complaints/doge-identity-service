## Task workspace — `task-ids-06-02-t05-story2-acceptance-verification`

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000008`  
**Decision Ref:** [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 2  
**Story:** [`../STORY-IDS-06-02-http-bootstrap-di-smoke-tests.md`](../STORY-IDS-06-02-http-bootstrap-di-smoke-tests.md)  
---

## Task: tests — Story 2 acceptance verification

### Цель
Верифицировать verbatim AC Story 2 (epic L192–195) после t01–t04.

### Почему это важно
Story 2 — основной offline smoke слой перед live integration и CI (epic §2 L28–32).

### Факты из кода
1. Story 2 AC — [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) L192–195.
2. Epic §5 L54–59 — пять целевых test modules.
3. [`profiles.yaml`](../../../../../../../../docs/methodology/builder-queue/profiles.yaml) identity `test_command` — `-m "not live_integration"`.

### Gap
Нет зафиксированной проверки AC L192–195 на полном offline наборе Story 2.

### AC/DoD
- [x] (P0) Все 5 файлов smoke + DI + provider + validator проходят PASSED.
- [x] (P0) Тесты не делают сетевых вызовов (ASGITransport + in-memory только).
- [x] (P0) Общее время offline-сюиты < 30 секунд.

### Где менять код
- N/A (verification); при FAIL — исправления в t01–t04 targets

### Out of scope
- Live integration — Story 3
- CI workflows — Story 4

### Проверка
```bash
cd doge-identity-service && time .venv/bin/python -m pytest tests/test_bootstrap_smoke.py tests/test_http_transport_smoke.py tests/test_di_singleton.py tests/test_di_service_factory.py tests/test_eid_provider_registry.py tests/test_supabase_jwt_validator.py -q
```
