## Task workspace — `task-ids-09-04-t02-authentigate-settings-config-spec`

- Story: [`../STORY-IDS-EID-04-provider-owned-config.md`](../STORY-IDS-EID-04-provider-owned-config.md)
- Prerequisite: t01 `ProviderConfigSpec` types

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000017`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §F3, F10  
---

## Task: implement — `AuthentigateSettings` and authentigate config_spec

### Цель
Ввести `AuthentigateSettings` + authentigate `config_spec` на дескрипторе; зарегистрировать дескриптор в `ALL_EID_PROVIDER_DESCRIPTORS` для lookup валидации (build stub — EID-02 Out of scope).

### Почему это важно
Story AC #1: Authentigate-поля в `AuthentigateSettings`/`config_spec`, не в `load_config_from_env`. AC #4: default `scopes` = full claim-URLs (F10).

### Факты из кода
1. Flat fields без валидации: [`schema.py:31-35,141-145`](../../../../../../../src/core/config/schema.py).
2. Wrong default scopes (short names): [`schema.py:145`](../../../../../../../src/core/config/schema.py) — `"openid personal_code personal_code_country"`.
3. Audit F3 missing env fields: [`authentigate-compatibility-audit-2026-06-07.md:97-100`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md).
4. No `providers/authentigate/` — only [`providers/mock/`](../../../../../../../src/core/providers/mock/).
5. Owner decision (story): flat `AppConfig` fields **keep**; `AuthentigateSettings.load(env)` reads from env/flat fields.

### Gap / Проблема
Authentigate config не объявлен provider-side; F3/F10 gaps открыты.

### AC/DoD
- [x] (P0) `AuthentigateSettings` in `providers/authentigate/config.py`: issuer, discovery_url (derive from issuer default), client_id, client_secret, redirect_uri, scopes, acr_values (`sid_ee mid_ee idcard_ee`), ui_locales, country.
- [x] (P0) Default `scopes` = full claim-URLs (not short names); SPIKE-09 live demo confirm — Out of scope (offline default only).
- [x] (P0) Authentigate `config_spec` on descriptor with `validate`/`load`; **build stub** (provider body = EID-02).
- [x] (P0) Register authentigate descriptor in [`registry_builder.py:8-10`](../../../../../../../src/core/providers/registry_builder.py) `ALL_EID_PROVIDER_DESCRIPTORS`.
- [x] (P1) Owner decision documented in code: nested `AuthentigateSettings`; flat `AppConfig.authentigate_*` unchanged; eideasy fields untouched.

### Где менять код
- `doge-identity-service/src/core/providers/authentigate/config.py` (new)
- `doge-identity-service/src/core/providers/authentigate/descriptor.py` (new)
- `doge-identity-service/src/core/providers/registry_builder.py`

### Out of scope
- OIDC network / discovery HTTP — EID-07
- Provider `start_flow`/`handle_callback` — EID-02
- Delegated hook in `schema.py` — t03

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.providers.authentigate.config import AuthentigateSettings; print(AuthentigateSettings)"
grep -n "authentigate" src/core/providers/registry_builder.py
```
