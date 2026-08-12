## Task workspace — `task-ids-10-06-t07-audit-f3-sms-runtime-merged-env-source`

- Story: [`../STORY-IDS-PV-06-telnyx-sms-sender.md`](../STORY-IDS-PV-06-telnyx-sms-sender.md)
- Audit source: [`../../../../../../analysis/epic-ids-10-pv-06-audit-2026-06-11.md`](../../../../../../analysis/epic-ids-10-pv-06-audit-2026-06-11.md) (F3)
- Related pattern: [`task-ids-07-01-t07-audit-f1-dotenv-cwd-test-isolation`](../../../../EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t07-audit-f1-dotenv-cwd-test-isolation/README.md) (AUTHCORE dotenv merge)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `override epic_ids_10_pv_06_audit_2026_06_11`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-10-pv-06-audit-2026-06-11.md`](../../../../../../analysis/epic-ids-10-pv-06-audit-2026-06-11.md) §F3  
---

## Task: fix — SMS runtime env source alignment (F3)

### Цель
Загружать Telnyx provider settings из того же merged env-источника, что и `AppConfig` (`environ` + cwd `.env` merge), а не из сырого `os.environ`.

### Почему это важно
При `SMS_PROVIDER=telnyx` и creds только в cwd `.env` (как в [`.env.example:72-77`](../../../../../../../.env.example)) `load_config_from_env` проходит, но `build_sms_provider_runtime` падает `ConfigError: TELNYX_API_KEY missing` — латентный сбой dev/staging деплоя.

### Факты из кода
1. [`providers.py:10-15`](../../../../../../../src/core/config/providers.py) — `provide_app_config`: `merge_dotenv_from_cwd(source, priority=priority)` без мутации `os.environ`.
2. [`runtime_factory.py:24-25`](../../../../../../../src/core/phone/runtime_factory.py) — `descriptor.config_spec.load(os.environ)` для активного SMS-провайдера.
3. [`infrastructure/providers.py:104`](../../../../../../../src/core/infrastructure/providers.py) — `build_sms_registry(build_sms_provider_runtime(config=resolved_config))` без проброса merged env.
4. [`test_telnyx_sms_sender.py`](../../../../../../../tests/test_telnyx_sms_sender.py) — `test_build_sms_registry_active_telnyx` маскирует через `patch.dict(os.environ, _minimal_env())`.
5. eID runtime: [`providers/runtime_factory.py`](../../../../../../../src/core/providers/runtime_factory.py) — не грузит provider-owned settings из `os.environ` на этом пути.

### Gap / Проблема
Config-source inconsistency: `AppConfig` и Telnyx `TelnyxSettings` читают разные источники env (audit F3 MEDIUM).

### AC/DoD
- [x] (P0) `build_sms_provider_runtime` принимает/использует merged env (тот же источник, что `provide_app_config`), не `os.environ` напрямую.
- [x] (P0) `config_spec.load(merged)` для активного SMS-провайдера в production wiring ([`providers.py`](../../../../../../../src/core/infrastructure/providers.py)).
- [x] (P0) Тест: `.env`-only `TELNYX_*` creds (без `patch.dict(os.environ)`) — `build_sms_registry` + `get_active()` → `TelnyxSmsSender`.
- [x] (P1) `pytest -m "not live_integration" -q` — 0 failed.
- [x] (P1) Не ломать mock-ветку (`SMS_PROVIDER=mock`).

### Где менять код
- `doge-identity-service/src/core/phone/runtime_factory.py`
- `doge-identity-service/src/core/infrastructure/providers.py`
- `doge-identity-service/tests/test_telnyx_sms_sender.py`
- опционально: `doge-identity-service/src/core/config/providers.py` (shared `resolve_config_env()` helper)

### Out of scope
- eID provider runtime / `build_provider_runtime`
- PV-07 delivery webhook
- Изменение логики `merge_dotenv_from_cwd` (только consumer alignment)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_telnyx_sms_sender.py -m "not live_integration" -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
