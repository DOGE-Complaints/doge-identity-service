## Task workspace — `task-ids-10-07-t02-telnyx-webhook-signature-verifier`

- Story: [`../STORY-IDS-PV-07-telnyx-delivery-webhook.md`](../STORY-IDS-PV-07-telnyx-delivery-webhook.md)
- Prerequisite: t01 (optional parallel with t01 if no session coupling)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000028`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md) Scope bullet 2; Story AC #2; [`../../../../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md`](../../../../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md) §2.7  
---

## Task: implement — Telnyx webhook Ed25519 signature verifier

### Цель
Верифицировать подлинность входящего Telnyx webhook по Ed25519 signature header до обработки payload.

### Почему это важно
Story AC #2: без валидной подписи → 401/403, тело не обрабатываем.

### Факты из кода
1. [`telnyx/config.py`](../../../../../../../src/core/phone/telnyx/config.py) — `TelnyxSettings` **нет** webhook public key.
2. Webhook verifier module **отсутствует** (`grep webhook_signature src/core/phone/telnyx` → 0).
3. Backlog: Ed25519 signature header; уточнить имена header/алгоритм по [SPIKE-PV-08](../../../../../../backlog-stories/phone-verification/SPIKE-IDS-PV-08-telnyx-account-setup.md) / Telnyx docs.
4. [`.env.example`](../../../../../../../.env.example) — TELNYX block без webhook key.

### Gap / Проблема
Нет config + verifier для webhook signature — нельзя безопасно принимать публичный endpoint.

### AC/DoD
- [x] (P0) `TelnyxSettings` + env: `TELNYX_WEBHOOK_PUBLIC_KEY` (или каноническое имя по Telnyx docs).
- [x] (P0) `verify_telnyx_webhook_signature(*, raw_body: bytes, headers: Mapping[str, str], public_key: str) -> bool` в `src/core/phone/telnyx/`.
- [x] (P0) Unit test: valid signature passes; tampered body / wrong key fails.
- [x] (P1) `.env.example` — комментарий + placeholder для webhook public key.
- [x] (P1) README/docstring: ссылка на SPIKE-PV-08 для live header names.

### Где менять код
- `doge-identity-service/src/core/phone/telnyx/config.py`
- `doge-identity-service/src/core/phone/telnyx/webhook_signature.py` (new)
- `doge-identity-service/.env.example`
- `doge-identity-service/tests/test_telnyx_webhook_signature.py` (new)

### Out of scope
- HTTP route / handler (t04)
- Delivery status parsing (t03)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_telnyx_webhook_signature.py -q
```
