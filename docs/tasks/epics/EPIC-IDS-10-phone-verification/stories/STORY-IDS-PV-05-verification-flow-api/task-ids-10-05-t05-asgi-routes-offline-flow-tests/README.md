## Task workspace — `task-ids-10-05-t05-asgi-routes-offline-flow-tests`

- Story: [`../STORY-IDS-PV-05-verification-flow-api.md`](../STORY-IDS-PV-05-verification-flow-api.md)
- Prerequisite: t03 `handle_phone_request`; t04 `handle_phone_confirm`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** todo  
**Wave:** `pkg-000026`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md) Scope bullets 1–2, 5; AC #1–#5  
---

## Task: implement — ASGI routes + offline e2e phone verification flow tests

### Цель
Зарегистрировать `POST /auth/phone/request` и `POST /auth/phone/confirm`; покрыть полный MockSmsSender flow — Story Scope §роуты + AC #5.

### Почему это важно
AC #1–#5 require HTTP-level verification; образец [`test_eid_verification_flow.py`](../../../../../../../tests/test_eid_verification_flow.py).

### Факты из кода
1. eID routes: [`asgi_app.py:224-240`](../../../../../../../src/core/api/asgi_app.py) — Bearer `Depends(get_current_user)`.
2. `MockSmsSender.sent_messages` for asserting SMS without PII leak in tests.
3. Phone routes **отсутствуют** in `asgi_app.py`.
4. `test_phone_verification_flow.py` **отсутствует**.

### Gap / Проблема
Handlers exist only after t03/t04; no HTTP surface or e2e tests for phone flow.

### AC/DoD
- [ ] (P0) `POST /auth/phone/request` — JSON `{"phone": "<e164 or local>"}`, Bearer JWT, calls `handle_phone_request`.
- [ ] (P0) `POST /auth/phone/confirm` — JSON `{"phone": "...", "code": "..."}`, Bearer JWT, calls `handle_phone_confirm`.
- [ ] (P0) Story AC #1: valid JWT + `+372...` → 200, `expires_at`, session `started`, MockSmsSender received message.
- [ ] (P0) Story AC #2: `+1...` (if not in allowlist) → `COUNTRY_NOT_ALLOWED`; resend within cooldown → `RATE_LIMITED`; after cooldown new request invalidates old code.
- [ ] (P0) Story AC #3: wrong code → `CODE_MISMATCH`; duplicate number other user → 409; success → `phone_verified` via `/me`.
- [ ] (P0) Story AC #4: audit events logged without raw phone/code (inspect `InMemoryPhoneAuditLogRepository` or mock).
- [ ] (P1) Story AC #5: full offline e2e green in `tests/test_phone_verification_flow.py`.

### Где менять код
- `doge-identity-service/src/core/api/asgi_app.py`
- `doge-identity-service/tests/test_phone_verification_flow.py` (new)

### Out of scope
- OpenAPI doc update
- Live Telnyx — PV-06

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_phone_verification_flow.py -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
