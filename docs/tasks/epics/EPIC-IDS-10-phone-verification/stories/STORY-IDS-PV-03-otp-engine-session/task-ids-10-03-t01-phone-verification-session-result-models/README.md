## Task workspace — `task-ids-10-03-t01-phone-verification-session-result-models`

- Story: [`../STORY-IDS-PV-03-otp-engine-session.md`](../STORY-IDS-PV-03-otp-engine-session.md)
- Prerequisite: STORY-IDS-PV-02 Done ([`../STORY-IDS-PV-02-provider-owned-config/STORY-IDS-PV-02-provider-owned-config.md`](../STORY-IDS-PV-02-provider-owned-config/STORY-IDS-PV-02-provider-owned-config.md))

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000024`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md) Scope bullet 1; [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §3, §5  
---

## Task: implement — `PhoneVerificationSession` and `PhoneVerificationResult` domain models

### Цель
Добавить frozen dataclass `PhoneVerificationSession` и `PhoneVerificationResult` в domain layer — Story Scope bullets 1, 5 (result shape).

### Почему это важно
Store (t02) и OTP engine (t03–t04) требуют typed session/result; зеркало eID [`VerificationSession`](../../../../../../../src/core/domain/models.py:43-59) и [`EIDVerificationResult`](../../../../../../../src/core/providers/base.py:21-29).

### Факты из кода
1. eID session model: [`models.py:43-59`](../../../../../../../src/core/domain/models.py).
2. `PhoneVerificationSession` **отсутствует** (grep `PhoneVerification` в `src/` — 0).
3. `SmsErrorCode` OTP codes ready ([`base.py:14-16`](../../../../../../../src/core/phone/base.py)).
4. PV-02 `AppConfig` phone params exist ([`schema.py:63-69`](../../../../../../../src/core/config/schema.py)).

### Gap / Проблема
No phone verification domain models; OTP engine has no session DTO.

### AC/DoD
- [ ] (P0) `PhoneVerificationSession` frozen dataclass with fields verbatim from story Scope (`id`, `supabase_user_id`, `phone_hash`, `dial_prefix`, `code_hash`, `status`, `attempts`, `created_at`, `expires_at`, `provider`, `provider_message_id`).
- [ ] (P0) `status` values: `started|consumed|failed|expired`.
- [ ] (P0) `PhoneVerificationResult(provider, dial_prefix, subject_hash, verified_at)` frozen dataclass (Story Scope).
- [ ] (P1) Export from `core.domain` package if convention requires.

### Где менять код
- `doge-identity-service/src/core/domain/models.py`
- `doge-identity-service/src/core/domain/__init__.py` (optional exports)

### Out of scope
- Store protocol — t02
- OTP generate/verify — t03, t04
- Supabase persistence — defer PV-04/PV-05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.domain.models import PhoneVerificationSession, PhoneVerificationResult; print(PhoneVerificationSession, PhoneVerificationResult)"
```
