## Task workspace — `task-ids-08-02-t04-code-verifier-encryption-key-e20`

- Story: [`../STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../STORY-IDS-CLEANUP-02-placeholders-hardening.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-02-placeholders-hardening.md) Scope E20; [`../task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/owner-decisions-e17-e22.md`](../task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/owner-decisions-e17-e22.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000013`  
**Skill declared:** python-pro  
---

## Task: fix — CODE_VERIFIER_ENCRYPTION_KEY (E20)

### Цель
Выполнить owner decision по E20: либо реально шифровать `code_verifier`, либо убрать секрет/требование из конфига и pilot gate.

### Почему это важно
Pilot требует секрет, который не используется ([`04-security`](../../../../../../../runtime-docs/04-security.md):123, gap P5). Ложное требование усложняет deploy. Story AC #1, AC #3.

### Факты из кода
1. Field: [`schema.py:37,149`](../../../../../../../src/core/config/schema.py) — `code_verifier_encryption_key`.
2. Pilot gate: [`schema.py:123`](../../../../../../../src/core/config/schema.py) — `CODE_VERIFIER_ENCRYPTION_KEY` в `pilot_required`.
3. Fixtures: [`tests/conftest.py:56`](../../../../../../../tests/conftest.py), [`tests/test_config_schema.py`](../../../../../../../tests/test_config_schema.py), [`.env.example:74`](../../../../../../../.env.example).
4. Encryption usage в `src/` — отсутствует (grep `code_verifier_encryption` только schema + tests).

### Gap / Проблема
Секрет заявлен (AES-256), но шифрование verifier в коде не применяется.

### AC/DoD
- [ ] (P0) Story AC #1: решение E20 из t01 выполнено.
- [ ] (P0) Если «убрать»: Story AC #3 — `code_verifier_encryption_key` / `CODE_VERIFIER_ENCRYPTION_KEY` grep = 0 в `src/`; pilot gate и conftest обновлены согласованно.
- [ ] (P0) Если «довести»: реальный cipher helper + usage path + tests (out of minimal cleanup — только если t01 = довести).
- [ ] (P1) Offline pytest green.

### Где менять код
- [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py)
- [`tests/conftest.py`](../../../../../../../tests/conftest.py)
- [`tests/test_config_schema.py`](../../../../../../../tests/test_config_schema.py)
- [`.env.example`](../../../../../../../.env.example)
- [`tests/test_bootstrap_smoke.py`](../../../../../../../tests/test_bootstrap_smoke.py) (если задаёт key)

### Out of scope
- Полный Authentigate OIDC client flow — functional epic
- EPIC-IDS-04 `code_verifier_cipher.py` parking — не реализовать без decision «довести»

### Проверка
```bash
cd doge-identity-service
rg "code_verifier_encryption|CODE_VERIFIER_ENCRYPTION" src/
.venv/bin/python -m pytest tests/test_config_schema.py tests/test_bootstrap_smoke.py -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
