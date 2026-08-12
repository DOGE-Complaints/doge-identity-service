# Story Acceptance Gate — STORY-IDS-01-03

- Story: `STORY-IDS-01-03-custom-dotenv-parser`
- Epic: `EPIC-IDS-01`
- Status: PASS

## Checks

- `python3.11 -c "from core.config.env_file import merge_dotenv_from_path; print('OK')"` → `OK`
- `python3.11 -c "from core.config import provide_app_config; ...; print(c.port)"` → `8100`
- `python3.11 -m pytest tests/test_env_file.py -q` → `2 passed`

## Covered AC

- shell priority over `.env` keys
- comments/empty lines and quote stripping
- `provide_app_config({...})` works without local `.env`
