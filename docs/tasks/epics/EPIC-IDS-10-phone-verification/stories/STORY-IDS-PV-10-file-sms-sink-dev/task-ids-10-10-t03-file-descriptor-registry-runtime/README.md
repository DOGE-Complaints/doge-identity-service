## Task workspace — `task-ids-10-10-t03-file-descriptor-registry-runtime`

- Story: [`../STORY-IDS-PV-10-file-sms-sink-dev.md`](../STORY-IDS-PV-10-file-sms-sink-dev.md)
- Prerequisite: [`task-ids-10-10-t01-file-sms-sender-core`](../task-ids-10-10-t01-file-sms-sender-core/README.md); [`task-ids-10-10-t02-file-sms-config-spec`](../task-ids-10-10-t02-file-sms-config-spec/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000041`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md) Scope §«Дескриптор file» + «Без сети»; Story AC #1, #6  
---

## Task: implement — file descriptor, registry, runtime (no httpx)

### Цель
Зарегистрировать `file` в `ALL_SMS_PROVIDER_DESCRIPTORS`; `SMS_PROVIDER=file` → `get_active()` returns `FileSmsSender`; exclude `file` from httpx client path.

### Почему это важно
Без registry `SMS_PROVIDER=file` rejected by schema; без runtime fix `file` erroneously gets telnyx httpx path.

### Факты из кода
1. Registry: [`registry_builder.py:9-12`](../../../../../../../src/core/phone/registry_builder.py) — only `mock` + `telnyx`.
2. Runtime factory: [`runtime_factory.py:14-15`](../../../../../../../src/core/phone/runtime_factory.py) — `_needs_sms_http_client`: `!= "mock"` → httpx (**file currently hits telnyx path**).
3. Mock descriptor template: [`mock/descriptor.py:9-24`](../../../../../../../src/core/phone/mock/descriptor.py).
4. Telnyx descriptor/registry precedent: PV-06 t04.

### Gap / Проблема
`file` provider not registered; runtime treats non-mock as network provider.

### AC/DoD
- [x] (P0) `file/descriptor.py` — `SmsProviderDescriptor` wiring config + sender factory.
- [x] (P0) Register in `ALL_SMS_PROVIDER_DESCRIPTORS`.
- [x] (P0) Extend `_needs_sms_http_client` — `file` like `mock`, **no** `httpx.Client`.
- [x] (P1) Story AC #1 — `get_active()` returns `FileSmsSender` when `SMS_PROVIDER=file`.
- [x] (P1) Story AC #6 — no http client for file provider.

### Где менять код
- `doge-identity-service/src/core/phone/file/descriptor.py` (new)
- `doge-identity-service/src/core/phone/registry_builder.py`
- `doge-identity-service/src/core/phone/runtime_factory.py`

### Out of scope
- Pilot fail-fast (t04)
- `.gitignore` / `.env.example` (t05)
- Offline e2e tests (t06)

### Проверка
```bash
cd doge-identity-service
grep -n "file" src/core/phone/registry_builder.py src/core/phone/runtime_factory.py
python3 -c "from core.phone.registry_builder import ALL_SMS_PROVIDER_DESCRIPTORS; print([d.name for d in ALL_SMS_PROVIDER_DESCRIPTORS])"
```
