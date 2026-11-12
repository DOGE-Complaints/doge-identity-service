## Task workspace — `task-ids-14-01-t03-smspm-config-tests`

- Story: [`../STORY-IDS-SMSPM-01-provider-config-registry.md`](../STORY-IDS-SMSPM-01-provider-config-registry.md)
- Prerequisite: [`task-ids-14-01-t01-smspm-settings-config`](../task-ids-14-01-t01-smspm-settings-config/README.md), [`task-ids-14-01-t02-smspm-descriptor-registry`](../task-ids-14-01-t02-smspm-descriptor-registry/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000046`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md) (T03, AC #1–#3)  
---

## Task: tests — SMSPM config accept / fail-fast / no-regression

### Цель
Accept `smspm` + full env; fail missing required when active=`smspm`; `mock|file|telnyx` без SMSPM env — ok.

### Почему это важно
Story AC #1–#3; зеркало telnyx config tests.

### Факты из кода
1. [`tests/test_phone_config_schema.py:21-67`](../../../../../../../tests/test_phone_config_schema.py) — telnyx require API key; unknown `SMS_PROVIDER` → `ConfigError` match `mock`.
2. [`tests/test_telnyx_sms_sender.py:75-81`](../../../../../../../tests/test_telnyx_sms_sender.py) — `telnyx` in `registered_sms_provider_names()`; `validate_telnyx_config` fail without key.
3. [`tests/test_sms_provider_registry.py:21-22`](../../../../../../../tests/test_sms_provider_registry.py) — `mock` registered.
4. [`tests/test_phone_file_sms_sender.py:66-67`](../../../../../../../tests/test_phone_file_sms_sender.py) — `file` registered.

### Gap / Проблема
Нет тестов на `SMS_PROVIDER=smspm` accept/fail-fast и на то, что mock/file/telnyx не требуют `SMSPM_*`.

### AC/DoD
- [x] (P0) `SMS_PROVIDER=smspm` + HASH/TOKEN/FROM → `load_config_from_env` ok; `cfg.sms_provider == "smspm"`.
- [x] (P0) `SMS_PROVIDER=smspm` без каждого из HASH/TOKEN/FROM → `ConfigError` с ясной env-ошибкой.
- [x] (P0) `SMS_PROVIDER=mock|file|telnyx` без SMSPM env не регрессирует (telnyx — свои TELNYX_* как сейчас).
- [x] (P0) `"smspm" in registered_sms_provider_names()`; unknown name по-прежнему отклоняется.
- [x] (P0) Нет live HTTP / SMSPM API тестов (SMSPM-02).
- [x] (P1) Существующие `test_phone_config_schema.py` / telnyx / file / mock registry тесты зелёные.

### Где менять код
- `doge-identity-service/tests/test_smspm_config.py` (**new**, предпочтительно; не смешивать telnyx-кейсы)

### Out of scope
- `.env.example` (t04)
- Story gate Date / pytest full suite sign-off (t05 / P3)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -q tests/test_smspm_config.py tests/test_phone_config_schema.py tests/test_telnyx_sms_sender.py tests/test_phone_file_sms_sender.py tests/test_sms_provider_registry.py -m "not live_integration"
```
