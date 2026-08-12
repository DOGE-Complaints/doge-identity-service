# STORY-IDS-EID-04 — Provider-owned configuration: конфиг и валидация на стороне провайдера

## Meta
- **Key:** `STORY-IDS-EID-04-provider-owned-config`
- **Epic:** `EPIC-IDS-09` (alias `EPIC-IDS-EID`)
- **Status:** 🟢 Done
- **Источник:** аудит [`authentigate-compatibility-audit-2026-06-07`](../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F3, F4, F10)
- **Исполнение:** [pipeline story](../../epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-04-provider-owned-config/STORY-IDS-EID-04-provider-owned-config.md) + pkg-000017 (2026-06-08)
- **Зависит от:** [STORY-IDS-EID-03](STORY-IDS-EID-03-provider-plugin-backbone.md) (`config_spec` живёт в дескрипторе)

## Зачем простыми словами
Сейчас `AppConfig` — это один плоский список полей **всех** провайдеров, а валидация обязательных полей зашита `if`-ами прямо в ядре (для eideasy есть, для authentigate нет). Чем больше провайдеров — тем сильнее раздувается ядро. Делаем так, чтобы **каждый провайдер сам объявлял свои настройки и сам себя валидировал**, а ядро только спрашивало активного «всё ли у тебя есть».

## Scope
- **`ProviderConfigSpec`** (часть дескриптора из [EID-03](STORY-IDS-EID-03-provider-plugin-backbone.md)): провайдер декларирует `required: tuple[str,...]`, `optional_defaults: dict[str,str]`, `load(env) -> <ProviderSettings>`.
- **`AuthentigateSettings`** (новый, `providers/authentigate/config.py`): `issuer`, `discovery_url` (вывод из issuer по умолчанию), `client_id`, `client_secret`, `redirect_uri`, `scopes` (**полные claim-URL по умолчанию**, фикс F10), `acr_values` (`sid_ee mid_ee idcard_ee`), `ui_locales`, `country`.
- **Делегированная валидация:** на старте активный `descriptor.config_spec.validate(env)` → fail-fast `ConfigError` с понятным текстом (закрывает F4 + AC EID-02 про понятную ошибку конфигурации).
- **Убрать провайдер-`if` из ядра:** вынести блок `if eid_provider == "eideasy"` ([`schema.py:109-112`](../../../../src/core/config/schema.py)) в спецификацию eideasy-дескриптора (или пометить legacy, см. «Решение владельца»); `load_config_from_env` оставляет только generic + членство `eid_provider`.
- Обновить `.env.example`/`.env`: актуальные `AUTHENTIGATE_*` (issuer demo `https://oidc.demo.sk.ee`, scopes-URL, acr, ui_locales, country).

## Вне scope
- Сетевое использование конфига (discovery/token) — [EID-07](STORY-IDS-EID-07-oidc-toolkit.md).
- Сборка самого провайдера — [EID-02](../eid-deferred/STORY-IDS-EID-02-real-eid-providers.md).

## Решение владельца (зафиксировать в реализации)
- Плоские `authentigate_*`/`eideasy_*` поля в `AppConfig` ([`schema.py:31-52`](../../../../src/core/config/schema.py)): **оставить** для обратной совместимости и читать из них в `AuthentigateSettings.load`, **или** мигрировать в nested. Рекомендация: ввести nested `AuthentigateSettings`, eideasy-поля не трогать (провайдер не активен).

## Точки в коде (текущее состояние)
- `ProviderConfigSpec`: [`config_spec.py:16-29`](../../../../src/core/providers/config_spec.py).
- Делегированная валидация: [`schema.py:88-93,118`](../../../../src/core/config/schema.py) — `_validate_active_eid_provider_config` → `descriptor.config_spec.validate` (без eideasy-`if` в `load_config_from_env`).
- `AuthentigateSettings` / `AUTHENTIGATE_CONFIG_SPEC`: [`authentigate/config.py`](../../../../src/core/providers/authentigate/config.py), [`authentigate/descriptor.py`](../../../../src/core/providers/authentigate/descriptor.py).
- Eideasy config_spec: [`eideasy/config.py`](../../../../src/core/providers/eideasy/config.py), [`eideasy/descriptor.py`](../../../../src/core/providers/eideasy/descriptor.py).
- Плоский `AppConfig` + провайдер-поля (owner: keep): [`schema.py:18-56`](../../../../src/core/config/schema.py).
- Каталог дескрипторов / членство `EID_PROVIDER`: [`registry_builder.py`](../../../../src/core/providers/registry_builder.py), [`schema.py`](../../../../src/core/config/schema.py) `load_config_from_env`.
- `.env.example` (секция Authentigate).

## Acceptance Criteria
- [x] Authentigate-поля объявлены в `AuthentigateSettings`/`config_spec`, не в теле `load_config_from_env`.
- [x] `EID_PROVIDER=authentigate` без обязательных `AUTHENTIGATE_*` → понятная `ConfigError` (имя недостающего поля), fail-fast на старте.
- [x] Добавление нового провайдера не требует правок провайдер-логики в `schema.py`.
- [x] `scopes` по умолчанию — полные claim-URL; значение подтверждается в demo ([SPIKE-IDS-EID-09](../eid-deferred/SPIKE-IDS-EID-09-authentigate-demo-access.md)).
- [x] `.env.example` отражает актуальные Authentigate-настройки; offline-набор зелёный, тест на отсутствующее required-поле.

## Парадигма-якорь
[06-eid-providers](../../../runtime-docs/06-eid-providers.md), [04-security](../../../runtime-docs/04-security.md) (минимизация claims/scope).
