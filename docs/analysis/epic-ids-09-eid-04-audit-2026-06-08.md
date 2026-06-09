# Жёсткий аудит исполнения STORY-IDS-EID-04 (provider-owned configuration)

> **Дата:** 2026-06-08
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-EID-04-provider-owned-config`](../tasks/backlog-stories/STORY-IDS-EID-04-provider-owned-config.md) vs фактический код. Исполнена под **EPIC-IDS-09-eid-verification** (pkg-000017), 6 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): EPIC-IDS-09, task queue t01–t06 (pkg-000017).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| `ProviderConfigSpec` | `required`, `optional_defaults`, `loader`, `validate`, `load` ([config_spec.py:16-29](../../src/core/providers/config_spec.py)) |
| Authentigate config | `AuthentigateSettings` + `AUTHENTIGATE_CONFIG_SPEC` ([authentigate/config.py](../../src/core/providers/authentigate/config.py)); eideasy тоже вынесен ([eideasy/config.py](../../src/core/providers/eideasy/config.py)) |
| Делегированная валидация **на старте** | `load_config_from_env:118` → `_validate_active_eid_provider_config` → `descriptor.config_spec.validate(env)` ([schema.py:88-93,118](../../src/core/config/schema.py)) |
| Каталог дескрипторов | mock + eideasy + authentigate ([registry_builder.py:10-13](../../src/core/providers/registry_builder.py)) |
| `.env.example` | issuer `oidc.demo.sk.ee`, scopes-URL, acr/ui_locales/country ([.env.example:48-56](../../.env.example)) |
| **Offline-сюита** | **222 passed, 10 deselected** ✅ (было 218 → +4) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-09, pkg-000017) | Факт | Статус |
|--------------------------------|------|--------|
| t01 provider config spec types | `ProviderConfigSpec` (required/optional_defaults/loader/validate/load) ([config_spec.py](../../src/core/providers/config_spec.py)) | 🟢 |
| t02 authentigate settings config spec | `AuthentigateSettings` (9 полей, defaults для scopes/acr/ui_locales/country, discovery из issuer) + `AUTHENTIGATE_CONFIG_SPEC`; eideasy аналогично | 🟢 |
| t03 delegated validation + schema cleanup | старт-валидация активного провайдера; eideasy-`if` убран (grep `eid_provider == "eideasy"` → 0); **но** membership-литерал остался (F2) | 🟢 c оговоркой |
| t04 env example authentigate vars | `.env.example:48-56` обновлён (полный набор `AUTHENTIGATE_*`) | 🟢 |
| t05 offline provider config tests | [test_provider_owned_config.py](../../tests/test_provider_owned_config.py): missing-required / default-scopes / discovery / no-provider-ifs | 🟢 |
| t06 story acceptance verification | AC 4/5 полностью, AC3 частично (F2) | 🟢 c оговоркой |
| **STORY-IDS-EID-04** | provider-owned config + делегированная валидация | **🟢 Done** |

Индекс ([`bullrun-launch-index.md:57`](../tasks/bullrun-launch-index.md)) держит эпик `🟡 In Progress — EID-01 🟢; EID-03 🟢; EID-04 🟢` — корректно.

---

## 2. Сверка Acceptance Criteria story

| AC | Факт (код + тест) | Вердикт |
|----|-------------------|---------|
| Authentigate-поля в `AuthentigateSettings`/`config_spec`, не в теле `load_config_from_env` | `AUTHENTIGATE_CONFIG_SPEC` + `AuthentigateSettings.load`; ядро лишь делегирует ([schema.py:88-93](../../src/core/config/schema.py)) | ✅ |
| `EID_PROVIDER=authentigate` без обязательных → понятная `ConfigError` (имя поля), fail-fast на старте | `validate` raise `f"Required env var {key!r} ..."` ([config_spec.py:22-25](../../src/core/providers/config_spec.py)); вызов на load; тест `test_authentigate_provider_requires_client_id` (`match="AUTHENTIGATE_CLIENT_ID"`) | ✅ |
| Добавление провайдера не требует правок провайдер-логики в `schema.py` | провайдер-специфичные `if`-валидации **убраны** (тест `test_schema_has_no_provider_specific_ifs`); ⚠️ **НО** membership-литерал `{"mock","eideasy","authentigate"}` остался ([schema.py:106](../../src/core/config/schema.py)) | ⚠️ частично (F2) |
| `scopes` по умолчанию — полные claim-URL | `DEFAULT_AUTHENTIGATE_SCOPES` (claim-URL); тест `..._default_scopes_use_full_claim_urls` (assert `https://id.authentigate.eu/claims/`) | ✅ (demo-подтверждение — SPIKE-09) |
| `.env.example` отражает Authentigate; offline зелёный, тест на missing-required | `.env.example:48-56`; 222 passed; тест missing-required есть | ✅ |

`required` Authentigate = `ISSUER/CLIENT_ID/CLIENT_SECRET/REDIRECT_URI` ([config.py:13-18](../../src/core/providers/authentigate/config.py)) — разумный набор; `scopes/acr/ui_locales/country` опциональны с дефолтами.

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| F1 | MEDIUM | Doc-stale | backlog-story помечена `⚪ Todo` (стр.6), а «Точки в коде (текущее состояние)» описывают **отрефакторенный** провайдер-`if` («[schema.py:96-112] eid_provider membership + eideasy required») — eideasy-валидация уже вынесена | [`STORY-IDS-EID-04...md:6,27-31`](../tasks/backlog-stories/STORY-IDS-EID-04-provider-owned-config.md) |
| F2 | MEDIUM | AC3 partial / SSOT | Список допустимых провайдеров `{"mock","eideasy","authentigate"}` остался **захардкоженным литералом** в [schema.py:106-107](../../src/core/config/schema.py), дублируя имена из каталога дескрипторов ([registry_builder._DESCRIPTOR_BY_NAME](../../src/core/providers/registry_builder.py)). Добавление нового провайдера всё ещё требует правки `schema.py`. Acceptance-тест `test_schema_has_no_provider_specific_ifs` проверяет только `== "authentigate"`-ифы и этот литерал **не ловит** | schema.py:106 |

### F2 — пояснение
EID-04 закрыл провайдер-специфичную **валидацию required** (делегирована в `config_spec`) — это главная цель (F4 аудита). Но «членство» `eid_provider` осталось жёстким перечнем, который дублирует каталог дескрипторов. Следствия:
- AC3 «добавление провайдера не требует правок провайдер-логики в `schema.py`» — **частично**: +дескриптор недостаточно, нужно ещё дописать имя в литерал `schema.py:106`.
- Single-Source-of-Truth: два источника списка провайдеров (литерал в schema vs каталог дескрипторов) могут разойтись.
- Acceptance-тест даёт ложное чувство полноты (ловит `==`-иф, но не `in {...}`-литерал).
**Как закрыть (направление):** вывести допустимые имена из каталога дескрипторов (registered names), а не из литерала. Решение — за владельцем (LOW runtime-impact: сейчас 3 имени совпадают с 3 дескрипторами).

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **222 passed** (было 218 → +4 provider-config теста), **ожидаемо** |
| eideasy-`if` в ядре | удалён; eideasy вынесен в дескриптор+config_spec — не регресс |
| Плоские `authentigate_*`/`eideasy_*` поля в `AppConfig` | **сохранены** (решение владельца, обратная совместимость) — парсинг на месте ([schema.py:141-165](../../src/core/config/schema.py)) |
| Старт-валидация для mock | mock `config_spec` = noop loader, `required=()` — пустая валидация, не ломает demo |
| Pilot-required (eid_secret и пр.) | не затронуто; сюита зелёная |

Регрессий не выявлено.

---

## 5. Итог

- **STORY-IDS-EID-04 — 🟢 исполнена:** provider-owned `ProviderConfigSpec`, `AuthentigateSettings`/`EideasySettings`, **делегированная fail-fast валидация на старте**, дефолтные scopes как полные claim-URL, `.env.example` актуализирован. F4 аудита (нет понятной ошибки для authentigate) закрыт.
- **Два MEDIUM-findings:** F1 (doc-stale backlog-story) и F2 (AC3 частично — захардкоженный membership-литерал дублирует каталог; acceptance-тест его не ловит).
- Регрессий нет; обратная совместимость плоских полей сохранена по решению владельца.

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; статусы тасков сверены по коду.
- [x] Критичная точка (вызов делегированной валидации на старте) проверена — не «метод есть, но не зовётся».
- [x] AC сверены по коду **и** тестам; AC3-частичность вскрыта (acceptance-тест не покрывает membership-литерал).
- [x] Регрессий нет; 218→222 объяснён.
