# Epic acceptance gate — EPIC-IDS-03

- Epic: `EPIC-IDS-03-dependency-injection`
- Gate status: **PASS** (2026-05-29)
- Package: `pkg-000004`
- Verified: automated AC + pytest

## Story gates

| Story | Gate |
|-------|------|
| STORY-IDS-03-01 | [PASS](./stories/STORY-IDS-03-01-api-dependencies-dataclass-handler-alias/story-acceptance-gate-STORY-IDS-03-01.md) |
| STORY-IDS-03-02 | [PASS](./stories/STORY-IDS-03-02-build-api-dependencies-singleton-lifespan/story-acceptance-gate-STORY-IDS-03-02.md) |
| STORY-IDS-03-03 | [PASS](./stories/STORY-IDS-03-03-epic-ids-04-extension-hook-contract/story-acceptance-gate-STORY-IDS-03-03.md) |

## Epic Goal (§2) evidence

| Check | Result | Evidence |
|-------|--------|----------|
| Singleton `get_api_dependencies()` | PASS | `test_get_api_dependencies_is_singleton` |
| `config.port` from EPIC-IDS-01 | PASS | `build_api_dependencies()` + `provide_app_config()` |
| `bearer_token_auth` present | PASS | factory returns `StubBearerTokenAuth` |
| `db_backend` in allowed set | PASS | schema + factory |
| `isinstance(db_checks, dict)` | PASS | dataclass field |
| Identity slots `None` in IDS-03 | PASS | `test_api_dependencies_identity_slots_default_none` |
| `_clear_api_dependencies_cache()` works | PASS | `test_clear_cache_creates_new_singleton` |
| EPIC-IDS-04 hooks documented | PASS | TODO + commented block in `dependencies.py` |

## Automated evidence

- `pytest tests/ -q -m "not live_integration"` → **56 passed**
- Epic §8 steps 1–4 covered by `tests/test_api_dependencies.py` (step 5 `test_di_singleton.py` — EPIC-IDS-06, not in scope)

## Operator smoke (§8 epic — optional)

```bash
cd doge-identity-service && .venv/bin/python -c "
from core.api.asgi_app import get_api_dependencies, _clear_api_dependencies_cache
from core.api.dependencies import HandlerDependencies
_clear_api_dependencies_cache()
d = get_api_dependencies()
assert HandlerDependencies is type(d)
assert d is get_api_dependencies()
print('EPIC-IDS-03 smoke OK')
"
```
