## Task workspace — `task-ids-14-01-t02-smspm-descriptor-registry`

- Story: [`../STORY-IDS-SMSPM-01-provider-config-registry.md`](../STORY-IDS-SMSPM-01-provider-config-registry.md)
- Prerequisite: [`task-ids-14-01-t01-smspm-settings-config`](../task-ids-14-01-t01-smspm-settings-config/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000046`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md) (T02, D-01-4, D-01-5)  
---

## Task: implement — `SMSPM_SMS_DESCRIPTOR` + registry append

### Цель
`SMSPM_SMS_DESCRIPTOR` (`name="smspm"`); stub или no-op `build` допустим до SMSPM-02; **обязательно** append в `ALL_SMS_PROVIDER_DESCRIPTORS`.

### Почему это важно
Story AC #1 / #5: `SMS_PROVIDER=smspm` должен быть членом registry; `schema.py` берёт имена из `registered_sms_provider_names()` без отдельного allow-list.

### Факты из кода
1. [`registry_builder.py:10-14`](../../../../../../../src/core/phone/registry_builder.py) — `ALL_SMS_PROVIDER_DESCRIPTORS` = mock, file, telnyx (нет `smspm`).
2. [`telnyx/descriptor.py:19-23`](../../../../../../../src/core/phone/telnyx/descriptor.py) — `TELNYX_SMS_DESCRIPTOR` `name="telnyx"`.
3. [`schema.py:168-176`](../../../../../../../src/core/config/schema.py) — `SMS_PROVIDER` ∈ `registered_sms_provider_names()`.
4. [`runtime_factory.py:14-15`](../../../../../../../src/core/phone/runtime_factory.py) — `_needs_sms_http_client` = `sms_provider not in {"mock", "file"}` (D-01-4: не хардкодить HTTP allow-list).
5. [`base.py:38-42`](../../../../../../../src/core/phone/base.py) — `SmsSenderPort.send`.

### Gap / Проблема
`smspm` не registered; неизвестное имя отклоняется, `smspm` тоже.

### AC/DoD
- [x] (P0) `SMSPM_SMS_DESCRIPTOR` `name="smspm"` + `config_spec` из t01.
- [x] (P0) Append в `ALL_SMS_PROVIDER_DESCRIPTORS`; mock/file/telnyx остаются (D-01-5 / D-G3).
- [x] (P0) Stub/no-op `build` удовлетворяет `SmsSenderPort` если registry собирается с active=`smspm`; **без** HTTP send (SMSPM-02).
- [x] (P0) Не менять `runtime_factory._needs_sms_http_client` на allow-list (D-01-4).
- [x] (P1) `"smspm" in registered_sms_provider_names()`; `schema.py` membership не дублировать вручную.

### Где менять код
- `doge-identity-service/src/core/phone/smspm/descriptor.py` (**new**)
- `doge-identity-service/src/core/phone/smspm/__init__.py` (export descriptor)
- `doge-identity-service/src/core/phone/registry_builder.py` (import + tuple)

### Out of scope
- HTTP SMSPM POST (SMSPM-02)
- Config tests file (t03)
- `.env.example` (t04)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.phone.registry_builder import registered_sms_provider_names; assert 'smspm' in registered_sms_provider_names()"
rg -n 'smspm|SMSPM_SMS_DESCRIPTOR' src/core/phone/registry_builder.py src/core/phone/smspm/
```
