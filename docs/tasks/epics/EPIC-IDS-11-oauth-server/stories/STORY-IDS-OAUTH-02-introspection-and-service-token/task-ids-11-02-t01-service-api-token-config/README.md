## Task workspace — `task-ids-11-02-t01-service-api-token-config`

- Story: [`../STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../STORY-IDS-OAUTH-02-introspection-and-service-token.md)
- Prerequisite: STORY-IDS-OAUTH-01 🟢 Done (pkg-000029)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000030`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md) Scope §SERVICE_API_TOKEN; gap CFG-1  
---

## Task: implement — SERVICE_API_TOKEN in AppConfig

### Цель
Добавить `SERVICE_API_TOKEN` в конфигурацию identity (`AppConfig` + env parsing), по образцу gateway (`SERVICE_API_TOKEN` optional/disabled when empty).

### Почему это важно
Introspection endpoint должен принимать только доверенные сервисы (gateway); без конфига нельзя включить сервисный gate (Story AC #2).

### Факты из кода
1. [`schema.py:24-69`](../../../../../../../src/core/config/schema.py) — `AppConfig` без `service_api_token`.
2. [`doge-complaints-gateway/.../security.py:65-72`](../../../../../../../../doge-complaints-gateway/src/core/api/security.py) — `build_service_auth_from_env` / `SERVICE_API_TOKEN`.
3. [`providers.py`](../../../../../../../src/core/config/providers.py) — `provide_app_config` wiring.

### Gap / Проблема
CFG-1: identity не знает `SERVICE_API_TOKEN` из env.

### AC/DoD
- [x] (P0) `AppConfig` поле `service_api_token: str` (empty = disabled gate at runtime).
- [x] (P0) Env key `SERVICE_API_TOKEN` парсится в `load_app_config` / schema builder.
- [x] (P1) Config test: missing/empty → empty string; set value → round-trip.
- [x] (P1) Traceability: Story AC #2 (prerequisite for service gate).

### Где менять код
- `doge-identity-service/src/core/config/schema.py`
- `doge-identity-service/src/core/config/providers.py` (if needed)
- `doge-identity-service/tests/test_config_schema.py` (or equivalent)

### Out of scope
- FastAPI dependency / route (t02, t04)
- Gateway repo changes
- Pilot fail-fast policy (match gateway: disabled when unset)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_config_schema.py -q
```
