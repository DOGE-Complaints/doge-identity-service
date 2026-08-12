## Task workspace — `task-ids-10-06-t05-offline-telnyx-sender-tests`

- Story: [`../STORY-IDS-PV-06-telnyx-sms-sender.md`](../STORY-IDS-PV-06-telnyx-sms-sender.md)
- Prerequisite: t01–t04 (full Telnyx adapter wired)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000027`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md) Scope bullets 5–6; [`../../../../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md`](../../../../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md) §2, §3  
---

## Task: implement — offline Telnyx tests + `.env.example`

### Цель
`tests/test_telnyx_sms_sender.py` with mocked httpx; live test skip without creds; complete `.env.example` TELNYX block.

### Почему это важно
Story AC #4 (offline + live skip) and AC #5 (`.env.example` TELNYX_*).

### Факты из кода
1. Registry test pattern: [`test_sms_provider_registry.py`](../../../../../../../tests/test_sms_provider_registry.py).
2. eID httpx mock patterns in provider tests (grep `httpx` in `tests/`).
3. `.env.example` lines 71–75: core TELNYX vars present; **missing** `TELNYX_MESSAGE_TYPE=SMS`, `TELNYX_ENCODING=auto` per backlog Scope.
4. SPIKE-PV-08: live trial creds external — live test must **skip** without `TELNYX_API_KEY` (+ profile/from).
5. pytest marker: `@pytest.mark.live_integration` (project convention from PV-05 acceptance).

### Gap / Проблема
No `test_telnyx_sms_sender.py`; no offline coverage for success/errors/PII; incomplete env example.

### AC/DoD
- [ ] (P0) Mocked httpx: success `queued` → `accepted=True` + `provider_message_id`.
- [ ] (P0) Error codes: country not allowed, rate limit, 5xx, missing `data.id`→`UNKNOWN`.
- [ ] (P0) Parse `errors[].code/title/detail` from Telnyx JSON body.
- [ ] (P0) Assert no OTP/phone in log captures (`caplog` or mock logger).
- [ ] (P0) Live test: `@pytest.mark.live_integration` or explicit skip without `TELNYX_API_KEY`.
- [ ] (P1) UPDATE [`.env.example`](../../../../../../../.env.example): add optional `TELNYX_MESSAGE_TYPE=SMS`, `TELNYX_ENCODING=auto`.
- [ ] (P1) Story AC #4, #5 evidence.

### Где менять код
- `doge-identity-service/tests/test_telnyx_sms_sender.py` (new)
- `doge-identity-service/.env.example`

### Out of scope
- SPIKE-PV-08 account setup (external)
- PV-07 delivery webhook
- Full e2e phone flow with telnyx (optional; mock flow sufficient per PV-05)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_telnyx_sms_sender.py -m "not live_integration" -q
```
