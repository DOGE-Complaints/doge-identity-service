## Task workspace — `task-ids-10-10-t05-dev-hygiene-gitignore-env-example`

- Story: [`../STORY-IDS-PV-10-file-sms-sink-dev.md`](../STORY-IDS-PV-10-file-sms-sink-dev.md)
- Prerequisite: none (parallel with t01–t04; lands before t06)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000041`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md) Scope §«Гигиена секретов»; Story AC #7  
---

## Task: implement — `.gitignore` outbox + `.env.example` file provider docs

### Цель
Dev hygiene: ignore outbox dir; document `SMS_PROVIDER=file` and `FILE_SMS_OUTBOX_DIR` with dev-only warning.

### Почему это важно
Plaintext OTP files must not be committed; operators need discoverable env docs.

### Факты из кода
1. `.env.example:63` — `SMS_PROVIDER=mock # mock | telnyx` (**`file` not listed**).
2. `.gitignore` — **no** `var/sms-outbox` / sms-outbox entry.
3. Default outbox: `var/sms-outbox` (story scope).

### Gap / Проблема
Outbox OTP files could be committed; `file` provider undocumented in `.env.example`.

### AC/DoD
- [x] (P0) `.gitignore` — outbox dir (e.g. `var/sms-outbox/`).
- [x] (P0) `.env.example` — comment `SMS_PROVIDER=… # mock | file | telnyx`.
- [x] (P0) `.env.example` — `FILE_SMS_OUTBOX_DIR` + dev-only warning (plaintext OTP; never prod/pilot).
- [x] (P1) Story AC #7.

### Где менять код
- `doge-identity-service/.gitignore`
- `doge-identity-service/.env.example`

### Out of scope
- Runtime code (t01–t04)
- Tests (t06)

### Проверка
```bash
cd doge-identity-service
grep -n "sms-outbox\|FILE_SMS_OUTBOX\|file | telnyx" .gitignore .env.example
```
