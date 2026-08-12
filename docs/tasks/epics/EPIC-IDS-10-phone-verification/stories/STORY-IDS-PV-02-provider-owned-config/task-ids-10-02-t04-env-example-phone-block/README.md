## Task workspace — `task-ids-10-02-t04-env-example-phone-block`

- Story: [`../STORY-IDS-PV-02-provider-owned-config.md`](../STORY-IDS-PV-02-provider-owned-config.md)
- Prerequisite: t02 (env var names stable)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000023`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §7  
---

## Task: docs — `.env.example` phone verification block

### Цель
Дополнить [`.env.example`](../../../../../../../.env.example) phone-блоком verbatim из architecture §7 — Story AC #5 (partial).

### Почему это важно
Оператору нужен образец env рядом с EID-блоком; PV-06 добавит `TELNYX_*` позже.

### Факты из кода
1. [`.env.example`](../../../../../../../.env.example) has `EID_PROVIDER=mock` block; **no** `PHONE_*` / `SMS_PROVIDER`.
2. Architecture §7 lists exact keys and demo defaults.
3. Story «Вне scope»: `TELNYX_*` validation — PV-06; placeholder comments OK in `.env.example`.

### Gap / Проблема
Missing phone env documentation for operators.

### AC/DoD
- [ ] (P0) Section `# --- Phone verification (ядро, provider-agnostic) ---` with `SMS_PROVIDER`, `PHONE_ALLOWED_DIAL_PREFIXES`, OTP/rate-limit vars from story Scope.
- [ ] (P1) Commented `# --- Telnyx ---` placeholder block (keys only, no validation logic).
- [ ] (P1) Story AC #5 traceability (env example part).

### Где менять код
- `doge-identity-service/.env.example`

### Out of scope
- `.env` (local secrets)
- `TELNYX_*` config_spec — PV-06
- Runtime docs — separate wave

### Проверка
```bash
grep -E 'SMS_PROVIDER|PHONE_' doge-identity-service/.env.example
```
