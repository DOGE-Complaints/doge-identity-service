## Task workspace — `task-ids-10-06-t01-telnyx-settings-config-spec`

- Story: [`../STORY-IDS-PV-06-telnyx-sms-sender.md`](../STORY-IDS-PV-06-telnyx-sms-sender.md)
- Prerequisite: STORY-IDS-PV-01, PV-02 Done

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000027`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md) Scope bullet 1; [`../../../../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md`](../../../../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md) §2  
---

## Task: implement — `TelnyxSettings` + `config_spec`

### Цель
Provider-owned config для Telnyx SMS: env vars + условная валидация alphanumeric `TELNYX_FROM`.

### Почему это важно
Story AC #1: `SMS_PROVIDER=telnyx` без creds / буквенный from без profile_id → понятная `ConfigError`.

### Факты из кода
1. Образец provider-owned config: [`authentigate/config.py`](../../../../../../../src/core/providers/authentigate/config.py) — `Settings` + `config_spec` hook.
2. SMS descriptor pattern: [`SmsProviderDescriptor`](../../../../../../../src/core/phone/descriptor.py), mock [`mock/descriptor.py`](../../../../../../../src/core/phone/mock/descriptor.py).
3. `AppConfig` boundary (PV-02): Telnyx vars **не** в `AppConfig`; только `TelnyxSettings` + delegated validate.
4. `grep telnyx src/core/phone` → **0** (модуль отсутствует).
5. `.env.example` TELNYX block exists (lines 71–75) but **нет** `TELNYX_MESSAGE_TYPE` / `TELNYX_ENCODING` (t05).

### Gap / Проблема
Нет `TelnyxSettings`; `SMS_PROVIDER=telnyx` отклоняется на load ([`test_phone_config_schema.py:21-23`](../../../../../../../tests/test_phone_config_schema.py)).

### AC/DoD
- [ ] (P0) `TelnyxSettings` dataclass: `api_key`, `api_base_url`, `from_sender`, `messaging_profile_id`, optional `message_type`, `encoding`.
- [ ] (P0) `config_spec`: `TELNYX_API_KEY` required when active; defaults `TELNYX_API_BASE_URL=https://api.telnyx.com`, `TELNYX_FROM=DOGEstonia`.
- [ ] (P0) Условная валидация: буквенный `TELNYX_FROM` (не E.164: не `+` + digits only) → `TELNYX_MESSAGING_PROFILE_ID` обязателен → `ConfigError`.
- [ ] (P1) Story AC #1 (config half): missing api_key / invalid from+profile → `ConfigError` with clear message.
- [ ] (P1) Path: `doge-identity-service/src/core/phone/telnyx/config.py`.

### Где менять код
- `doge-identity-service/src/core/phone/telnyx/config.py` (new)
- `doge-identity-service/src/core/phone/telnyx/__init__.py` (new, optional)

### Out of scope
- `TelnyxSmsSender.send` HTTP — t02
- Descriptor/registry — t04
- `.env.example` optional vars — t05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.phone.telnyx.config import TelnyxSettings; print(TelnyxSettings)"
```
