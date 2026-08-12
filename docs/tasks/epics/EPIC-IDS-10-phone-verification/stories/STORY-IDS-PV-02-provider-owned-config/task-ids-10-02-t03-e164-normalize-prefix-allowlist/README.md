## Task workspace — `task-ids-10-02-t03-e164-normalize-prefix-allowlist`

- Story: [`../STORY-IDS-PV-02-provider-owned-config.md`](../STORY-IDS-PV-02-provider-owned-config.md)
- Prerequisite: t02 (`phone_allowed_dial_prefixes` on `AppConfig`)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000023`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-02-provider-owned-config.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-02-provider-owned-config.md) Scope; [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §7, §10.2  
---

## Task: implement — E.164 normalization and dial-prefix allowlist gate

### Цель
Реализовать `normalize_to_e164(raw) -> str` и `assert_allowed_dial_prefix(e164, allowed_prefixes)` → `SmsSenderError(COUNTRY_NOT_ALLOWED)` — Story Scope bullet 3; AC #2, #3.

### Почему это важно
Ядро фильтрует страны **до** отправки SMS (architecture §8.3); PV-05 будет вызывать эти функции в flow handler.

### Факты из кода
1. `SmsErrorCode.COUNTRY_NOT_ALLOWED` exists ([`base.py:10`](../../../../../../../src/core/phone/base.py)).
2. `SmsSenderError` with code ([`base.py:26-34`](../../../../../../../src/core/phone/base.py)).
3. E.164 module **отсутствует** under `src/core/phone/`.
4. Story AC: `+372` ok, `+1` rejected when allowlist is `+372`; normalize spaces/parens/missing `+`.

### Gap / Проблема
No phone normalization utility; prefix gate not implemented.

### AC/DoD
- [ ] (P0) `normalize_to_e164(raw: str) -> str` handles spaces, parentheses, leading `+` optional (Story AC #3).
- [ ] (P0) `assert_allowed_dial_prefix(e164, allowed_prefixes)` raises `SmsSenderError(..., code=COUNTRY_NOT_ALLOWED)` when no prefix matches (Story AC #2).
- [ ] (P1) Invalid/unparseable input → `SmsSenderError(..., code=INVALID_PHONE)` or `ConfigError` (document choice in code).
- [ ] (P1) Export from `core.phone`.

### Где менять код
- `doge-identity-service/src/core/phone/e164.py` (new)
- `doge-identity-service/src/core/phone/__init__.py`

### Out of scope
- HTTP handler integration — PV-05
- Telnyx-specific errors — PV-06
- Tests — t05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.phone.e164 import normalize_to_e164; print(normalize_to_e164('372 5555 5555'))"
```
