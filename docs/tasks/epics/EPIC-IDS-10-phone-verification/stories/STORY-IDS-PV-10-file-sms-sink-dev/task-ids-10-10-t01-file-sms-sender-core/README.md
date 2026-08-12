## Task workspace — `task-ids-10-10-t01-file-sms-sender-core`

- Story: [`../STORY-IDS-PV-10-file-sms-sink-dev.md`](../STORY-IDS-PV-10-file-sms-sink-dev.md)
- Prerequisite: STORY-IDS-PV-01 🟢 Done (pkg-000022); STORY-IDS-PV-02 🟢 Done (pkg-000023)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000041`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md) Scope §«FileSmsSender»; Story AC #1 (partial), #2, #4  
---

## Task: implement — `FileSmsSender` core

### Цель
Реализовать `FileSmsSender` в `src/core/phone/file/file_sender.py` — append SMS-текста в outbox-файл по номеру.

### Почему это важно
Mock держит OTP только в памяти; для ручного фронт-теста нужен dev-sink на диск (G-SMS-1 файловый вариант).

### Факты из кода
1. Контракт порта: [`base.py:20-42`](../../../../../../../src/core/phone/base.py) — `SmsSenderPort`, `SmsSendResult`, `SmsSenderError`, `SmsErrorCode.SEND_FAILED`.
2. Шаблон отправителя: [`mock_sender.py:9-25`](../../../../../../../src/core/phone/mock/mock_sender.py).
3. Текст SMS: [`sms_text.py:4-5`](../../../../../../../src/core/phone/sms_text.py).
4. `grep file src/core/phone` → модуль **отсутствует**.

### Gap / Проблема
Нет `FileSmsSender`; OTP при ручном тесте через UI недоступен вне mock/in-process tests.

### AC/DoD
- [x] (P0) `FileSmsSender` с `provider_name="file"`.
- [x] (P0) `send(*, to_e164, text)` — append `{utc_iso}\t{text}\n` в `<outbox>/<sanitized>.log` (UTF-8, create-if-missing).
- [x] (P0) Санитайз имени файла: только `[+0-9]` из `to_e164` (path-traversal защита).
- [x] (P0) Успех → `SmsSendResult(provider_message_id=f"file-{uuid4()}", accepted=True)`.
- [x] (P0) IO error → `SmsSenderError(code=SmsErrorCode.SEND_FAILED)`.
- [x] (P1) Story AC #1 (partial), #2, #4 — sender behaviour без registry/config.

### Где менять код
- `doge-identity-service/src/core/phone/file/file_sender.py` (new)
- `doge-identity-service/src/core/phone/file/__init__.py` (new, optional)

### Out of scope
- Registry / descriptor (t03)
- Provider-owned config spec (t02)
- Pilot fail-fast (t04)
- `.gitignore` / `.env.example` (t05)

### Проверка
```bash
cd doge-identity-service
grep -n "FileSmsSender\|provider_name.*file" src/core/phone/file/file_sender.py
python3 -c "from core.phone.file.file_sender import FileSmsSender; print(FileSmsSender)"
```
