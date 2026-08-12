## Task workspace — `task-ids-09-07-t05-offline-oidc-toolkit-mocked-http-tests`

- Story: [`../STORY-IDS-EID-07-oidc-toolkit.md`](../STORY-IDS-EID-07-oidc-toolkit.md)
- Prerequisite: t01–t04 implementation complete

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000020`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/STORY-IDS-EID-07-oidc-toolkit.md`](../../../../../../backlog-stories/STORY-IDS-EID-07-oidc-toolkit.md) AC #5; [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F8)  
---

## Task: tests — offline OIDC toolkit with mocked discovery/JWKS/signature

### Цель
Добавить offline pytest coverage: mocked `.well-known`, JWKS, RS256 id_token; verify cache, unknown-kid refresh, validation failures → `IDENTITY_VALIDATION_FAILED` path — Story AC #5.

### Почему это важно
OIDC toolkit touches network boundaries; offline suite must stay green without live IdP (EID-03/EID-06 regression guard).

### Факты из кода
1. [`tests/conftest.py`](../../../../../../../tests/conftest.py) — offline markers / dotenv isolation (EPIC-IDS-06).
2. Pattern: [`tests/test_eid_callback_redirect.py`](../../../../../../../tests/test_eid_callback_redirect.py) — httpx/ASGI offline tests.
3. [`base.py:13`](../../../../../../../src/core/providers/base.py) — `IDENTITY_VALIDATION_FAILED`.
4. t04 wires `runtime.oidc` when non-mock.

### Gap / Проблема
No tests for `core/security/oidc/`; Story AC #5 open.

### AC/DoD
- [x] (P0) New test module e.g. `tests/test_oidc_toolkit.py` — no live network (`pytest.mark` offline only).
- [x] (P0) Discovery cache: second call does not repeat HTTP (mock transport call count).
- [x] (P0) JWKS unknown `kid` triggers refresh and succeeds on rotated key.
- [x] (P0) Valid RS256 id_token passes; bad signature/wrong `iss`/`aud`/`nonce`/expired → validation error (IDENTITY_VALIDATION_FAILED mappable).
- [x] (P0) `ProviderRuntime.oidc` non-None when `http_client` wired (integration-style unit test).
- [x] (P1) Full offline suite green: `pytest -m "not live_integration" -q`.

### Где менять код
- `doge-identity-service/tests/test_oidc_toolkit.py` (new)
- Fixtures/helpers under `tests/` if needed (minimal)

### Out of scope
- Live Authentigate integration — EID-02 / SPIKE-09
- Runtime-docs updates (not in story Scope)
- Story acceptance doc — t06

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_oidc_toolkit.py -m "not live_integration" -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
