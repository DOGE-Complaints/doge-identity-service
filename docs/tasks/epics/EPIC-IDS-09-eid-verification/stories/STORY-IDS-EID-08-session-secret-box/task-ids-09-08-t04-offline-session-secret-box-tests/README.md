## Task workspace — `task-ids-09-08-t04-offline-session-secret-box-tests`

- Story: [`../STORY-IDS-EID-08-session-secret-box.md`](../STORY-IDS-EID-08-session-secret-box.md)
- Prerequisite: t01–t03 implementation complete

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000021`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/STORY-IDS-EID-08-session-secret-box.md`](../../../../../../backlog-stories/STORY-IDS-EID-08-session-secret-box.md) AC #1, #2, #3, #4, #5; [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F7)  
---

## Task: tests — offline SessionSecretBox, config, and runtime wire

### Цель
Добавить offline pytest coverage: Fernet round-trip, pilot missing key, demo default, runtime `secret_box` wire, encryption key separation from `eid_secret` — Story AC #1–#5.

### Почему это важно
Session crypto touches config and DI boundaries; offline suite must stay green without live deps (EID-07 regression guard).

### Факты из кода
1. [`tests/conftest.py`](../../../../../../../tests/conftest.py) — offline markers / dotenv isolation.
2. Pattern: [`tests/test_oidc_toolkit.py`](../../../../../../../tests/test_oidc_toolkit.py) — unit tests for security primitive + runtime wire.
3. [`tests/test_config_schema.py`](../../../../../../../tests/test_config_schema.py) — pilot fail-fast tests for secrets.
4. t03 wires `runtime.secret_box` when config allows.

### Gap / Проблема
No tests for `core/security/session_secret/` or `EID_SESSION_ENC_KEY`.

### AC/DoD
- [x] (P0) New module `tests/test_session_secret_box.py` — no live network.
- [x] (P0) Round-trip: `seal` then `open` returns original plaintext (Story AC #1).
- [x] (P0) Pilot profile + empty `EID_SESSION_ENC_KEY` → `ConfigError` (Story AC #2).
- [x] (P0) Demo profile accepts default/ephemeral key when unset (Story AC #2).
- [x] (P0) `build_provider_runtime` → `secret_box is not None` (Story AC #3).
- [x] (P0) Assert box built from `eid_session_enc_key`, not `eid_secret` (Story AC #4).
- [x] (P1) Full offline suite green: `pytest -m "not live_integration" -q` (Story AC #5).

### Где менять код
- `doge-identity-service/tests/test_session_secret_box.py` (new)
- Extend `tests/test_config_schema.py` if pilot test lives there instead

### Out of scope
- Live Authentigate PKCE flow — EID-02
- Story acceptance doc — t05
- Runtime-docs updates (not in story Scope)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_session_secret_box.py -m "not live_integration" -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
