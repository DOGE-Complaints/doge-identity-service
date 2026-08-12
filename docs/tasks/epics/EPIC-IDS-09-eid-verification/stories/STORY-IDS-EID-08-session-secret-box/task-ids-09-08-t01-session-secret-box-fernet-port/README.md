## Task workspace — `task-ids-09-08-t01-session-secret-box-fernet-port`

- Story: [`../STORY-IDS-EID-08-session-secret-box.md`](../STORY-IDS-EID-08-session-secret-box.md)
- Prerequisite: STORY-IDS-EID-03 Done ([`../STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md`](../STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md))

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000021`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/STORY-IDS-EID-08-session-secret-box.md`](../../../../../../backlog-stories/STORY-IDS-EID-08-session-secret-box.md) Scope #1; [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F7)  
---

## Task: implement — `SessionSecretBox` port and Fernet implementation

### Цель
Реализовать provider-agnostic `SessionSecretBox`: `seal(plaintext) -> str` / `open(token) -> str` на Fernet (`cryptography>=42`) — Story Scope #1, AC #1 и AC #4 (отдельный encryption key, не `eid_secret`).

### Почему это важно
PKCE `code_verifier` пишется в сессию при `create` ([`models.py:49`](../../../../../../../src/core/domain/models.py)); без reversible seal/open провайдер не сможет достать секрет на callback (EID-02).

### Факты из кода
1. Модуля `src/core/security/session_secret.py` **нет** (glob 0 files).
2. [`pyproject.toml:17`](../../../../../../../pyproject.toml) — `cryptography>=42.0.0` dependency present.
3. [`hashing.py:9-11`](../../../../../../../src/core/security/hashing.py) — HMAC-only; не подходит для reversible encryption.
4. [`schema.py:37,117`](../../../../../../../src/core/config/schema.py) — `eid_secret` from `DOGESTONIA_EID_SECRET` (HMAC purpose only).
5. EID-03 reserved slot: [`runtime.py:20`](../../../../../../../src/core/providers/runtime.py) — `secret_box: Any | None = None`.

### Gap / Проблема
Encryption helper removed in CLEANUP-02; no `SessionSecretBox` port or Fernet impl.

### AC/DoD
- [x] (P0) `SessionSecretBox` protocol/port in `core/security/session_secret.py` with `seal` / `open`.
- [x] (P0) `FernetSessionSecretBox` (or equivalent) using `cryptography.fernet.Fernet`.
- [x] (P0) Factory/build helper accepts **encryption key material**, not `AppConfig.eid_secret` (Story AC #4 partial).
- [x] (P1) Provider-agnostic: no Authentigate/eideasy imports.
- [x] (P1) Story AC #1 traceability (port + Fernet impl).

### Где менять код
- `doge-identity-service/src/core/security/session_secret.py` (new)

### Out of scope
- `EID_SESSION_ENC_KEY` env / pilot fail-fast — t02
- `ProviderRuntime.secret_box` wire — t03
- Round-trip tests — t04
- Provider `start_flow`/`callback` PKCE usage — EID-02

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.security.session_secret import SessionSecretBox, FernetSessionSecretBox; print(SessionSecretBox)"
```
