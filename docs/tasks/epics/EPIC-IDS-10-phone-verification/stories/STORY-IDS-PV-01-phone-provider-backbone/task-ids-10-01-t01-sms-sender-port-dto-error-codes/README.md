## Task workspace — `task-ids-10-01-t01-sms-sender-port-dto-error-codes`

- Story: [`../STORY-IDS-PV-01-phone-provider-backbone.md`](../STORY-IDS-PV-01-phone-provider-backbone.md)
- Prerequisite: eID plugin platform Done ([`../../../../EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md`](../../../../EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md))

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000022`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md) Scope; [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §3, §6  
---

## Task: implement — `SmsSenderPort`, DTO, and `SmsErrorCode` canon

### Цель
Создать пакет `core/phone` с контрактом SMS-провайдера: `SmsSenderPort` (Protocol), `SmsSendResult`, `SmsSenderError`, `SmsErrorCode` (StrEnum) — Story Scope bullets 1–3, AC #1 (partial).

### Почему это важно
Без канонического порта и кодов ошибок нельзя подключить Telnyx (PV-06) и OTP-ядро (PV-03); зеркало [`base.py`](../../../../../../../src/core/providers/base.py) для eID.

### Факты из кода
1. Пакета `src/core/phone/` **нет** (glob 0 files under `src/core/phone`).
2. Образец порта/DTO/ошибок: [`base.py:9-48`](../../../../../../../src/core/providers/base.py) — `EidErrorCode`, `EIDProviderError`, `EIDProviderPort`.
3. Story Scope перечисляет 9 значений `SmsErrorCode` verbatim (delivery + OTP layers).
4. `httpx` уже в зависимостях (eID OIDC); SMS transport reuse в runtime t02.

### Gap / Проблема
Нет SMS provider contract; phone verification architecture §3/§6 не отражены в коде.

### AC/DoD
- [x] (P0) `SmsSenderPort` Protocol: `provider_name: str`, `send(*, to_e164: str, text: str) -> SmsSendResult`.
- [x] (P0) `SmsSendResult(provider_message_id: str | None, accepted: bool)` frozen dataclass.
- [x] (P0) `SmsErrorCode` StrEnum с членами verbatim из Story Scope.
- [x] (P0) `SmsSenderError(message, code: SmsErrorCode)` exception type.
- [x] (P1) Публичный реэкспорт из `core.phone` package (`__init__.py`).
- [x] (P1) Story AC #1 traceability (port + DTO + errors).

### Где менять код
- `doge-identity-service/src/core/phone/base.py` (new)
- `doge-identity-service/src/core/phone/__init__.py` (new)

### Out of scope
- `SmsProviderDescriptor` / `SmsProviderRuntime` — t02
- Registry / guard — t03
- `MockSmsSender` — t04
- `AppConfig` / `SMS_PROVIDER` env — PV-02

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.phone.base import SmsSenderPort, SmsSendResult, SmsSenderError, SmsErrorCode; print(list(SmsErrorCode))"
```
