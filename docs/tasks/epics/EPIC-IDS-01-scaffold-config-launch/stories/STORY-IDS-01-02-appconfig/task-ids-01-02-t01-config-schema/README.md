## Task workspace — `task-ids-01-02-t01-config-schema`

- Story: [`../STORY-IDS-01-02-appconfig.md`](../STORY-IDS-01-02-appconfig.md)
- Epic: [`../../../../EPIC-IDS-01-scaffold-config-launch.md`](../../../../EPIC-IDS-01-scaffold-config-launch.md) §Story 2
- Decision Ref: [`../../../../../../requirements/07-env-configuration-spec.md`](../../../../../../requirements/07-env-configuration-spec.md); [`../../../../../../requirements/17-eid-provider-abstraction.md`](../../../../../../requirements/17-eid-provider-abstraction.md); [`../../../../../../requirements/18-eideasy-provider.md`](../../../../../../requirements/18-eideasy-provider.md); [`../../../../../../analysis/interview-cpo-cto-epics-2026-05-27.md`](../../../../../../analysis/interview-cpo-cto-epics-2026-05-27.md)

---
**Приоритет:** P0  
**Сложность:** L  
**Статус:** done  
**Wave:** `pkg-000001`  
**Зависимости:** STORY-IDS-01-01  
---

## Task: implement — AppConfig schema and load_config_from_env

### Цель
Реализовать `ConfigError`, `DeploymentProfile`, frozen `AppConfig`, `load_config_from_env` с identity field-set и fail-fast правилами.

### Факты из кода
1. `src/core/config/schema.py` — отсутствует.
2. Паттерн: [`doge-complaints-gateway/src/core/config/schema.py`](../../../../../../../doge-complaints-gateway/src/core/config/schema.py) — `_require`, `_get_value`, `_parse_*` (заменить gateway `cluster_*` поля на identity blocks).
3. Эпик §Story 2 Outputs — полный список полей и валидаций.
4. Interview 4.5: **первая** проверка — `db_backend`; `sqlite` → `ConfigError` (audit H-3).
5. Interview 4.4: `profile=pilot` + пустой `DOGESTONIA_EID_SECRET` → `ConfigError`.
6. `eid_secret = source.get("DOGESTONIA_EID_SECRET", "")` — **без** `or` fallback.

### Gap / Проблема
Нет единого immutable config — EPIC-IDS-02..06 не могут стартовать.

### AC/DoD
- [x] (P0) `@dataclass(frozen=True) class AppConfig` с полями из эпика §Story 2 (deployment, supabase, authentigate, identity secrets, oauth, eid_provider, eideasy_*, db_backend, cors).
- [x] (P0) `port` default `8100`; `request_timeout_s=15`, `oidc_request_timeout_s=10`.
- [x] (P0) `load_config_from_env`: `db_backend` проверяется первым; `in_memory|supabase` only.
- [x] (P0) `db_backend=supabase` без `SUPABASE_URL` / `SUPABASE_SERVICE_ROLE` → `ConfigError`.
- [x] (P0) `eid_provider` ∈ `{mock, eideasy, authentigate}`; `eideasy` без credentials → `ConfigError`.
- [x] (P0) `profile=pilot` — pilot-required table из [`07-env-configuration-spec.md`](../../../../../../requirements/07-env-configuration-spec.md) §«Валидация».
- [x] (P0) Нет полей `cluster_*`.

### Где менять код
- `doge-identity-service/src/core/config/schema.py`

### Out of scope
- `config/__init__.py` exports (T02)
- `env_file.py` / `providers.py` (STORY-IDS-01-03)
- ADR-IDS-005 решение psycopg vs supabase-py (парковка эпик §9)

### Команды проверки
```bash
cd doge-identity-service && . .venv/bin/activate
python3.11 -c "
from core.config.schema import load_config_from_env, ConfigError
cfg = load_config_from_env({'APP_PROFILE':'demo','API_BASE_URL':'http://localhost:8100','DB_BACKEND':'in_memory','EID_PROVIDER':'mock'})
assert cfg.port == 8100 and cfg.request_timeout_s == 15
"
```
