# Re-audit закрытия gap-листа STORY-IDS-PV-06 (F1/F2/F3)

> **Дата:** 2026-06-11
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — закрытие каждого gap проверено по фактическому коду (`file:line`), регрессии, остаточные.
> **Источник gap-листа:** [`epic-ids-10-pv-06-audit-2026-06-11.md`](./epic-ids-10-pv-06-audit-2026-06-11.md) §3 (F1 MEDIUM, F2 LOW, F3 MEDIUM).
> **Итог:** **3/3 закрыты** (F3 — c регрессионным тестом + SSOT-рефактором). Остаточное: 1 косметический typo даты (severity none).

## Сводка закрытия

| ID | Severity | Было | Стало | Вердикт |
|----|----------|------|-------|---------|
| F3 | MEDIUM | Telnyx-настройки из `os.environ`, конфиг из `environ`+`.env` merge → `.env`-only creds падают на старте | Настройки грузятся из того же merged-источника (`resolve_config_env`); регрессионный тест на `.env`-only без `patch.dict` | 🟢 Закрыт |
| F1 | MEDIUM | backlog-story `⚪ Todo`, AC `[ ]`, EPIC.md PV-06 `⚪` | Status `🟢 Done`, 5×AC `[x]`, EPIC.md PV-06 `🟢` | 🟢 Закрыт |
| F2 | LOW | индекс «314», аудит насчитал 315 | Канонический offline-счёт зафиксирован как `pytest -m "not live_integration"` = **314**; индекс консистентен | 🟢 Закрыт |

---

## F3 — config-source inconsistency (MEDIUM) → 🟢 ЗАКРЫТ

**Проверка по коду:**

1. **Единый merged-источник.** Введён `resolve_config_env(env)` ([providers.py:10-17](../../src/core/config/providers.py)) — та же логика merge, что раньше была инлайн в `provide_app_config`: `dict(environ)` + `merge_dotenv_from_cwd(source, priority=priority)`.
2. **SSOT-рефактор (analysis.mdc «single source of truth»):** `provide_app_config` теперь **делегирует** в `resolve_config_env` ([providers.py:20](../../src/core/config/providers.py)) — дублирования merge-логики больше нет; конфиг и провайдер-настройки гарантированно из одного источника.
3. **Фабрика рантайма переключена с `os.environ` на merged-env.** `build_sms_provider_runtime` получил параметр `env` и грузит настройки через `resolve_config_env(env)`:
   ```python
   # было: loaded = descriptor.config_spec.load(os.environ)
   config_env = resolve_config_env(env)                 # providers.py merge
   ...
   loaded = descriptor.config_spec.load(config_env)     # runtime_factory.py:31
   ```
   ([runtime_factory.py:18-34](../../src/core/phone/runtime_factory.py))
4. **Caller пробрасывает тот же merged-env.** `merged_env = resolve_config_env()` → `build_sms_provider_runtime(config=resolved_config, env=merged_env)` ([providers.py:104-107](../../src/core/infrastructure/providers.py)) — `config` и `settings` строятся из одного словаря.
5. **Регрессионный тест без маскировки.** `test_build_sms_registry_active_telnyx` переписан: `monkeypatch.chdir(tmp_path)` + `delenv(TELNYX_API_KEY/PROFILE_ID/SMS_PROVIDER)` + запись creds **только** в `tmp_path/.env`, затем `provide_app_config()` → `build_sms_provider_runtime(config=config)` → `get_active()` == `TelnyxSmsSender` ([test:99-116](../../tests/test_telnyx_sms_sender.py)). Прежняя версия требовала `patch.dict(os.environ, ...)` — теперь её нет, тест доказывает именно `.env`-only путь.

**Вывод:** исходный сценарий («creds в cwd `.env`, старт падает `ConfigError`») устранён — теперь `.env`-only Telnyx-конфиг резолвится и проходит. Расхождение «config-source vs settings-source» закрыто на уровне архитектуры (SSOT), а не точечно.

---

## F1 — doc-stale (MEDIUM) → 🟢 ЗАКРЫТ

| Артефакт | Проверка | Состояние |
|----------|----------|-----------|
| [`STORY-IDS-PV-06...md:6`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md) | `Status:` | `🟢 Done` ✅ |
| там же, AC (5 пунктов, стр.33-37) | чекбоксы | все `- [x]` ✅ |
| [`EPIC-IDS-PHONE.md:27`](../tasks/backlog-stories/phone-verification/EPIC-IDS-PHONE.md) | строка PV-06 | `… | провайдер | 🟢 Done |` ✅ |

Pipeline-story и task-queue (t01–t06) уже были 🟢 — без изменений.

---

## F2 — индекс pytest-count (LOW) → 🟢 ЗАКРЫТ

**Реконсиляция по фактическому прогону:**

| Команда | Результат |
|---------|-----------|
| `pytest -m "not live_integration"` (канонический offline проекта) | **314 passed, 11 deselected** ✅ |
| `pytest -m "not online"` (команда исходного аудита) | 315 passed, 10 skipped |

Расхождение объяснено: маркер `live_integration` **определён** в [pyproject.toml:33](../../pyproject.toml), а `online` — нет. Под `not live_integration` 11 live-тестов (10 supabase + 1 telnyx-live) корректно **деселектятся** → 314; под несуществующим `not online` они запускаются и само-скипаются → счёт смещается на +1 (315). Канонический счёт — **314** (исключение live по реальному маркеру). Gap-fix-таск это и зафиксировал: «verified factual 314 (`pytest -m "not live_integration"`), audit 315 miscount» ([bullrun-launch-index.md:307](../tasks/bullrun-launch-index.md)).

Индекс ([bullrun-launch-index.md:11,13,14](../tasks/bullrun-launch-index.md)) теперь консистентно держит «314 pytest offline», что соответствует каноническому прогону. F2 закрыт корректно (число привязано к воспроизводимой команде).

**Остаточное (severity none, косметика):** строка 11 содержит typo даты — «314 pytest offline, **2026-06-02**» (override помечен сегодняшним run_mode `…2026_06_11`; ожидалось `2026-06-11`). Не влияет на статус/счёт; при следующей правке индекса заменить `2026-06-02`→`2026-06-11`.

---

## Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| `pytest -m "not live_integration"` | **314 passed, 11 deselected** ✅ (канонический offline) |
| `pytest -m "not online"` | 315 passed, 10 skipped ✅ |
| Сигнатура `build_sms_provider_runtime` (+`env`) | единственный продакшн-caller обновлён ([providers.py:106](../../src/core/infrastructure/providers.py)); тест зовёт с `env=None` (merge из cwd) — оба пути зелёные |
| `provide_app_config` рефактор → `resolve_config_env` | поведение идентично (та же merge-логика); все config/me/flow-тесты зелёные |
| mock-путь (`SMS_PROVIDER=mock`) | `_needs_sms_http_client` False → `settings={}`, `config_spec.load` не вызывается — не затронут |
| eID/OAuth/PV-01..05 | не затронуты |

Регрессий не выявлено. F3-фикс аддитивен (новый параметр с дефолтом + общий хелпер), SSOT-рефактор убрал дублирование без смены поведения.

---

## Итог

- **F3 (MEDIUM) — 🟢 закрыт по существу:** провайдер-настройки и `AppConfig` сведены к единому merged-источнику (`resolve_config_env`, SSOT-рефактор `provide_app_config`), `build_sms_provider_runtime(env=...)` грузит из него, продакшн-caller пробрасывает `merged_env`. Регрессионный тест доказывает `.env`-only сценарий **без** `patch.dict(os.environ)`.
- **F1 (MEDIUM) — 🟢 закрыт:** backlog-story `🟢 Done` + 5×AC `[x]` + строка EPIC.md PV-06 `🟢`.
- **F2 (LOW) — 🟢 закрыт:** канонический offline-счёт = `pytest -m "not live_integration"` = **314**, индекс консистентен; «315» исходного аудита объяснён неопределённым маркером `online`.
- **Остаточное:** косметический typo даты в строке 11 индекса (`2026-06-02`→`2026-06-11`), severity none.

## Quality gate (analysis.mdc)
- [x] Каждый gap перепроверен по фактическому коду с `file:line`; не по заявлению.
- [x] F3 — прослежена вся цепочка (config source → resolve_config_env → runtime_factory → caller → тест); SSOT-рефактор подтверждён; регрессионный тест валидирует именно прежде-падавший путь.
- [x] F2 — расхождение 314/315 воспроизведено обеими командами и объяснено маркерами (`live_integration` определён, `online` — нет); канон зафиксирован.
- [x] Регрессий нет (314 / 315 зелёные); mock-путь и eID не затронуты.
- [x] Остаточный typo даты зафиксирован честно (severity none), не выдаётся за закрытый.
