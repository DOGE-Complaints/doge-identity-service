# Story Acceptance Gate — STORY-IDS-01-02

- Story: `STORY-IDS-01-02-appconfig`
- Epic: `EPIC-IDS-01`
- Status: PASS

## Checks

- `python3.11 -m pytest tests/test_config_schema.py -q` → `8 passed`
- `python3.11 -c "from core.config import AppConfig, ConfigError, load_config_from_env"` → `OK`
- `load_config_from_env` matrix covered:
  - demo defaults (`request_timeout_s=15`, `oidc_request_timeout_s=10`, `port=8100`)
  - supabase missing vars -> `ConfigError`
  - sqlite forbidden -> `ConfigError`
  - unknown `EID_PROVIDER` -> `ConfigError`
  - eideasy missing credentials -> `ConfigError`
  - pilot missing required secrets -> `ConfigError`
  - pilot empty `DOGESTONIA_EID_SECRET` -> `ConfigError`
  - dataclass immutability (`FrozenInstanceError`)
