## Task workspace — `task-ids-09-08-t02-eid-session-enc-key-config-pilot-failfast`

- Story: [`../STORY-IDS-EID-08-session-secret-box.md`](../STORY-IDS-EID-08-session-secret-box.md)
- Prerequisite: t01 `SessionSecretBox` ([`../task-ids-09-08-t01-session-secret-box-fernet-port/README.md`](../task-ids-09-08-t01-session-secret-box-fernet-port/README.md))

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000021`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/STORY-IDS-EID-08-session-secret-box.md`](../../../../../../backlog-stories/STORY-IDS-EID-08-session-secret-box.md) Scope #2; [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F7)  
---

## Task: implement — `EID_SESSION_ENC_KEY` in AppConfig with pilot fail-fast

### Цель
Добавить env `EID_SESSION_ENC_KEY` → `AppConfig.eid_session_enc_key`; обязателен в `pilot` (понятная `ConfigError`), допустим дефолт/эфемерный ключ в `demo` — Story Scope #2, AC #2 и AC #4.

### Почему это важно
Encryption key must be separate from HMAC `DOGESTONIA_EID_SECRET` ([`schema.py:117,131`](../../../../../../../src/core/config/schema.py)); pilot deployments need fail-fast before serving traffic.

### Факты из кода
1. [`schema.py:19-45`](../../../../../../../src/core/config/schema.py) — `AppConfig` frozen dataclass; `eid_secret: str` exists, no `eid_session_enc_key`.
2. [`schema.py:124-137`](../../../../../../../src/core/config/schema.py) — `pilot_required` tuple pattern + `ConfigError` on empty value.
3. [`tests/test_config_schema.py:135`](../../../../../../../tests/test_config_schema.py) — existing pilot empty-secret rejection test pattern.
4. grep `EID_SESSION_ENC_KEY` in `src/` → 0 matches (today).

### Gap / Проблема
No config field or validation for session encryption key.

### AC/DoD
- [x] (P0) `AppConfig.eid_session_enc_key: str` loaded from env `EID_SESSION_ENC_KEY`.
- [x] (P0) `APP_PROFILE=pilot` + empty `EID_SESSION_ENC_KEY` → `ConfigError` with key name in message (Story AC #2).
- [x] (P0) `demo`/in-memory profile may use documented ephemeral default when env unset (Story Scope #2).
- [x] (P1) Field distinct from `eid_secret` / `DOGESTONIA_EID_SECRET` (Story AC #4).
- [x] (P1) Do not add `EID_SESSION_ENC_KEY` to pilot_required conflation with `DOGESTONIA_EID_SECRET`.

### Где менять код
- `doge-identity-service/src/core/config/schema.py`
- `doge-identity-service/tests/test_config_schema.py` (pilot fail-fast test — or defer full coverage to t04 if minimal)

### Out of scope
- Fernet port implementation — t01
- Runtime wire — t03
- Full offline regression suite — t04

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.config.schema import AppConfig; print('eid_session_enc_key' in AppConfig.__dataclass_fields__)"
.venv/bin/python -m pytest tests/test_config_schema.py -m "not live_integration" -q -k session_enc || true
```
