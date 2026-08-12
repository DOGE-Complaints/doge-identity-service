# STORY-IDS-EID-04 — Provider-owned configuration: конфиг и валидация на стороне провайдера

## Meta
- **Key:** `STORY-IDS-EID-04-provider-owned-config`
- **Parent Epic:** [`../../../../EPIC-IDS-09-eid-verification.md`](../../../../EPIC-IDS-09-eid-verification.md)
- **Epic alias (код/backlog):** `EPIC-IDS-EID`
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-EID-04-provider-owned-config.md`](../../../../backlog-stories/eid/STORY-IDS-EID-04-provider-owned-config.md)
- **Decision Ref:** [`../../../../backlog-stories/STORY-IDS-EID-04-provider-owned-config.md`](../../../../backlog-stories/eid/STORY-IDS-EID-04-provider-owned-config.md); [`authentigate-compatibility-audit-2026-06-07`](../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F3, F4, F10)
- **Источник:** аудит [`authentigate-compatibility-audit-2026-06-07`](../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F3, F4, F10)
- **Зависит от:** [STORY-IDS-EID-03-provider-plugin-backbone](../STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md) (`config_spec` живёт в дескрипторе)

## Зачем простыми словами
Сейчас `AppConfig` — это один плоский список полей **всех** провайдеров, а валидация обязательных полей зашита `if`-ами прямо в ядре (для eideasy есть, для authentigate нет). Чем больше провайдеров — тем сильнее раздувается ядро. Делаем так, чтобы **каждый провайдер сам объявлял свои настройки и сам себя валидировал**, а ядро только спрашивало активного «всё ли у тебя есть».

## Scope
- **`ProviderConfigSpec`** (часть дескриптора из [EID-03](../../../../backlog-stories/eid/STORY-IDS-EID-03-provider-plugin-backbone.md)): провайдер декларирует `required: tuple[str,...]`, `optional_defaults: dict[str,str]`, `load(env) -> <ProviderSettings>`.
- **`AuthentigateSettings`** (новый, `providers/authentigate/config.py`): `issuer`, `discovery_url` (вывод из issuer по умолчанию), `client_id`, `client_secret`, `redirect_uri`, `scopes` (**полные claim-URL по умолчанию**, фикс F10), `acr_values` (`sid_ee mid_ee idcard_ee`), `ui_locales`, `country`.
- **Делегированная валидация:** на старте активный `descriptor.config_spec.validate(env)` → fail-fast `ConfigError` с понятным текстом (закрывает F4 + AC EID-02 про понятную ошибку конфигурации).
- **Убрать провайдер-`if` из ядра:** вынести блок `if eid_provider == "eideasy"` ([`schema.py:109-112`](../../../../../../src/core/config/schema.py)) в спецификацию eideasy-дескриптора (или пометить legacy, см. «Решение владельца»); `load_config_from_env` оставляет только generic + членство `eid_provider`.
- Обновить `.env.example`/`.env`: актуальные `AUTHENTIGATE_*` (issuer demo `https://oidc.demo.sk.ee`, scopes-URL, acr, ui_locales, country).

## Вне scope
- Сетевое использование конфига (discovery/token) — [EID-07](../../../../backlog-stories/eid/STORY-IDS-EID-07-oidc-toolkit.md).
- Сборка самого провайдера — [EID-02](../../../../backlog-stories/STORY-IDS-EID-02-real-eid-providers.md).

## Решение владельца (зафиксировать в реализации)
- Плоские `authentigate_*`/`eideasy_*` поля в `AppConfig` ([`schema.py:31-52`](../../../../../../src/core/config/schema.py)): **оставить** для обратной совместимости и читать из них в `AuthentigateSettings.load`, **или** мигрировать в nested. Рекомендация: ввести nested `AuthentigateSettings`, eideasy-поля не трогать (провайдер не активен).

## Точки в коде (текущее состояние)
- Плоский `AppConfig` + провайдер-поля: [`schema.py:18-56`](../../../../../../src/core/config/schema.py).
- Провайдер-`if` валидации: [`schema.py:96-112`](../../../../../../src/core/config/schema.py) (`eid_provider` membership + eideasy required).
- Парсинг полей: [`schema.py:141-162`](../../../../../../src/core/config/schema.py).
- Дефолты конфига: [`config/providers.py`](../../../../../../src/core/config/providers.py); `.env.example` (секция Authentigate).

## Acceptance Criteria
- [x] Authentigate-поля объявлены в `AuthentigateSettings`/`config_spec`, не в теле `load_config_from_env`.
- [x] `EID_PROVIDER=authentigate` без обязательных `AUTHENTIGATE_*` → понятная `ConfigError` (имя недостающего поля), fail-fast на старте.
- [x] Добавление нового провайдера не требует правок провайдер-логики в `schema.py`.
- [x] `scopes` по умолчанию — полные claim-URL; значение подтверждается в demo ([SPIKE-IDS-EID-09](../../../../backlog-stories/SPIKE-IDS-EID-09-authentigate-demo-access.md)).
- [x] `.env.example` отражает актуальные Authentigate-настройки; offline-набор зелёный, тест на отсутствующее required-поле.

## Парадигма-якорь
[06-eid-providers](../../../../../runtime-docs/06-eid-providers.md), [04-security](../../../../../runtime-docs/04-security.md) (минимизация claims/scope).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-09-04-t01-provider-config-spec-types`](./task-ids-09-04-t01-provider-config-spec-types/README.md) | pkg-000017 |
| 2 | [`task-ids-09-04-t02-authentigate-settings-config-spec`](./task-ids-09-04-t02-authentigate-settings-config-spec/README.md) | pkg-000017 |
| 3 | [`task-ids-09-04-t03-delegated-validation-schema-cleanup`](./task-ids-09-04-t03-delegated-validation-schema-cleanup/README.md) | pkg-000017 |
| 4 | [`task-ids-09-04-t04-env-example-authentigate-vars`](./task-ids-09-04-t04-env-example-authentigate-vars/README.md) | pkg-000017 |
| 5 | [`task-ids-09-04-t05-offline-provider-config-tests`](./task-ids-09-04-t05-offline-provider-config-tests/README.md) | pkg-000017 |
| 6 | [`task-ids-09-04-t06-story-acceptance-verification`](./task-ids-09-04-t06-story-acceptance-verification/README.md) | pkg-000017 |
| 7 | [`task-ids-09-04-t07-audit-f1-backlog-story-status-sync`](./task-ids-09-04-t07-audit-f1-backlog-story-status-sync/README.md) | override epic_ids_09_eid_04_audit_2026_06_08 |
| 8 | [`task-ids-09-04-t08-audit-f2-eid-provider-membership-from-descriptors`](./task-ids-09-04-t08-audit-f2-eid-provider-membership-from-descriptors/README.md) | override epic_ids_09_eid_04_audit_2026_06_08 |
