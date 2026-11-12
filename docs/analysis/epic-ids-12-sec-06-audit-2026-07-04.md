# Жёсткий аудит STORY-IDS-SEC-06 (JWKS-only) по фактическому коду

> **Дата:** 2026-07-04
> **Объект:** [`STORY-IDS-SEC-06-supabase-jwks-es256-hardening`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md) (backlog 🟢 Done, pkg-000042) vs реальный код `src/`, `tests/`, конфиг, доки.
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`; регрессии; gaps с severity + как закрыть. Findings, не реализация.
> **Сюита:** **398 passed, 12 deselected** (offline, `pytest -m "not live_integration"`) — регрессий нет (база до SEC-06 — 394).

---

## 0. Вердикт

**Стори реализована добросовестно и полностью.** Все 8 подзадач (T01–T08) + W2 (DI) + W6 (сужение `except`) подтверждены кодом; ключевое решение интервью **D-1 (JWKS-only)** доведено до конца: HS256-путь и `SUPABASE_JWT_SECRET` удалены, тест-харнес мигрирован на ES256+мок-JWKS, доки синхронизированы, границы соблюдены (OAuth-HS256 сохранён). Найдено **2 LOW-наблюдения** (не блокеры). Индекс [`bullrun-launch-index`](../tasks/bullrun-launch-index.md) для SEC-06 фактически корректен; одна косметическая актуализация (pytest-счётчик).

---

## 1. Подзадачи T01–T08 → код: построчная сверка (всё ✅)

| Задача | Требование | Факт в коде | Статус |
|--------|------------|-------------|--------|
| **T01** | change-propagation аудит | инвентарь отражён в стори; удаляемое подтверждено grep'ом (ниже) | ✅ |
| **T02** | валидатор JWKS-only | [`supabase_validator.py`](../../src/core/auth/supabase_validator.py): нет `_validate_hs256`/`OctKey`/`jwt_secret`; только `_validate_jwks` (`:71-100`), диспетч `alg in _JWKS_ALGORITHMS` (`:105`); `demo.local`-эвристики нет, гейт `if self._supabase_url` (`:38,72`) | ✅ |
| **T03** | DI кэша ключей (W2) | конструктор принимает `jwks_cache: JwksCache | None` ([`:30-37`](../../src/core/auth/supabase_validator.py)); собственный `httpx.Client` не создаётся; wiring в [`providers.py:111-119`](../../src/core/infrastructure/providers.py) (кэш строится снаружи от реального `supabase_url`) | ✅ |
| **T04** | удалить `SUPABASE_JWT_SECRET` (D-5) | `grep -rn "supabase_jwt_secret\|SUPABASE_JWT_SECRET" src/` → **пусто**; pilot-required без него ([`schema.py:184-187`](../../src/core/config/schema.py)); `.env.example` очищен | ✅ |
| **T05** | тест-харнес HS256→ES256 (крит) | новый [`tests/supabase_jwt_harness.py`](../../tests/supabase_jwt_harness.py); `conftest.py:82-85` мокает JWKS-http; минтеров HS256 Supabase-токенов не осталось | ✅ |
| **T06** | ES256-тесты валидатора | [`test_supabase_jwt_validator.py`](../../tests/test_supabase_jwt_validator.py): ES256 happy (`:113`), kid-refresh (`:149`), HS256-reject (`:95`), jwks-unavailable (`:101`), RS256 (`:113`) | ✅ |
| **T07** | доки → JWKS-only | [`09:23-47`](../requirements/09-supabase-jwt-validation.md) «HS256 удалён (D-1)»; [`04-security.md:104,136`](../runtime-docs/04-security.md) JWKS-only; [`07:34`](../requirements/07-env-configuration-spec.md) `SUPABASE_JWT_SECRET удалён`; runbooks очищены | ✅ |
| **T08** | story acceptance | offline-сюита **398 passed** | ✅ |

### Прицельные grep-гейты (из AC) — пройдены
- `grep -rn "_validate_hs256|OctKey|test-secret-for-demo|demo.local|supabase_jwt_secret|SUPABASE_JWT_SECRET" src/` → **пусто**. ✅
- **KEEP-граница соблюдена:** HS256 OAuth-самоподписи **сохранён** — [`access_token_jwt.py:1,26`](../../src/core/oauth/access_token_jwt.py) (на `OAUTH_ACCESS_TOKEN_SECRET`, iss identity; это НЕ Supabase-валидатор). Единственный оставшийся HS256-минт в тестах — [`test_oauth_introspection.py:135-137`](../../tests/test_oauth_introspection.py) — это OAuth-access-токен, миграции не подлежит. ✅ (не пропуск)

### Клеймы и алгоритм-безопасность (KEEP из SEC-03)
`_claims_from_token` сохранил `iss`/`sub`/`exp`/`aud=authenticated`/`role` ([`supabase_validator.py:40-59`](../../src/core/auth/supabase_validator.py)); `alg` вне `_JWKS_ALGORITHMS` (в т.ч. `HS256`/`none`) → `JwtValidationError("Unsupported JWT algorithm")` ([`:105-107`](../../src/core/auth/supabase_validator.py)). refresh-on-unknown-kid — один retry ([`:78-94`](../../src/core/auth/supabase_validator.py)).

---

## 2. Findings (оба LOW — не блокеры)

> ✅ **ЗАКРЫТО (re-audit 2026-07-04, override t09).** Клиент назван `jwks_http_client`, прокинут в фабрику ([`providers.py:113-117,154`](../../src/core/infrastructure/providers.py)), доступен через [`service_factory.py:43,87-88`](../../src/core/infrastructure/service_factory.py) и **закрывается в lifespan-shutdown**: [`asgi_app.py:229-230`](../../src/core/api/asgi_app.py) `if deps.jwks_http_client is not None: deps.jwks_http_client.close()`. AC W2 «клиент закрывается» теперь выполнен полностью. Регрессий нет (398 passed).

### F1 · LOW · `httpx.Client` для JWKS не закрывается явно
[`providers.py:115`](../../src/core/infrastructure/providers.py) создаёт `httpx.Client` под JWKS-кэш и **не закрывает** его; это не переиспользование общего клиента (другого http-клиента в этой сборке нет — reuse нечего). AC W2 «клиент переиспользуется/**закрывается**» выполнен частично: инъекция ✅ (тестируемо), close ✗.
- **Оценка:** это **процесс-синглтон** (строится один раз при сборке фабрики, живёт весь процесс), не per-request — реальной утечки дескрипторов нет; клиент умирает с процессом. По факту приемлемо для FastAPI-приложения.
- **Как закрыть (если нужно строго):** привязать `http_client.close()` к lifespan-shutdown приложения, либо переиспользовать общий клиент, когда появится shared-http-слой.

> ✅ **ЗАКРЫТО (re-audit 2026-07-04, override t10).** `SUPABASE_TEST_JWT_SECRET` снят из **всех живых потребителей** — `grep` по `.env.example`, `tests/integration/supabase/conftest.py`, `test_supabase_jwt_live_sanity.py`, `test_supabase_runbook_docs.py`, `docs/runbook/*.md`, `.github/workflows/integration-live.yml` → **пусто**. Live-sanity переведён на новый API валидатора: [`test_supabase_jwt_live_sanity.py:41-43`](../../tests/integration/supabase/test_supabase_jwt_live_sanity.py) `SupabaseJwtValidatorImpl(supabase_url=…, jwks_cache=JwksCache(…))` (без `jwt_secret`). Остаточные упоминания — только в истории (пакеты SEC-06/t10, старые EPIC-IDS-05/06 аудиты), что корректно (историю не трогаем).

### F2 · LOW · ⚠️verify · `SUPABASE_TEST_JWT_SECRET` — актуальность под JWKS-only
После JWKS-only live-sanity ([`test_supabase_jwt_live_sanity.py:24-37`](../../tests/integration/supabase/test_supabase_jwt_live_sanity.py)) валидирует **реальный** ES256-токен из dotenv (`validator.validate(token)`), не минтит HS256. При этом `SUPABASE_TEST_JWT_SECRET` всё ещё требуется live-conftest'ом ([`integration/supabase/conftest.py:46,52`](../../tests/integration/supabase/conftest.py)) и проверяется doc-тестом ([`test_supabase_runbook_docs.py:65`](../../tests/test_supabase_runbook_docs.py)).
- **Оценка:** возможно **рудимент** для live-ветки (offline-deselected, MVP не гейтит). Не дефект offline-приёмки.
- **Как закрыть:** проверить, минтит ли какой-либо live-тест токен этим секретом; если нет — снять `SUPABASE_TEST_JWT_SECRET` из `.env.example`/runbook/live-conftest как мёртвый (в отдельной мелкой задаче live-integration, вне SEC-06).

---

## 3. Регрессии
**Не обнаружено.** Offline-сюита **398 passed, 12 deselected** (рост с 394 → +4: тесты валидатора расширены ES256-кейсами; ~14 файлов, минтивших HS256, мигрированы на общий ES256-харнес и остаются зелёными — «переписали, не удалили»). Существующий OAuth-HS256 путь не тронут.

---

## 4. Актуализация `bullrun-launch-index.md`

Индекс для SEC-06 **уже корректен** (актуализирован пайплайном pkg-000042). Сверка по факту:

| Место | Запись | Факт | Вердикт |
|-------|--------|------|---------|
| [`:11`](../tasks/bullrun-launch-index.md) | P3 done SEC-06, pkg-000042, 8/8 tasks | подтверждено | ✅ (добавлен pytest-счётчик — §5) |
| [`:139`](../tasks/bullrun-launch-index.md) | EPIC-IDS-12 … SEC-06 🟢 | реализовано | ✅ |
| [`:743-750`](../tasks/bullrun-launch-index.md) | 8 задач t01–t08 🟢 Done | каждая ↔ реальный код-артефакт (см. §1) | ✅ |
| [`:766`](../tasks/bullrun-launch-index.md) | story SEC-06 🟢 Done | — | ✅ |

Маппинг задач → код (все подтверждены): t01→инвентарь; t02→[`supabase_validator.py`](../../src/core/auth/supabase_validator.py); t03→[`providers.py`](../../src/core/infrastructure/providers.py); t04→[`schema.py`](../../src/core/config/schema.py)/`.env.example`; t05→[`supabase_jwt_harness.py`](../../tests/supabase_jwt_harness.py); t06→[`test_supabase_jwt_validator.py`](../../tests/test_supabase_jwt_validator.py); t07→[`09`](../requirements/09-supabase-jwt-validation.md)/[`04-security`](../runtime-docs/04-security.md)/[`07`](../requirements/07-env-configuration-spec.md); t08→398 passed.

---

## 5. Применённые правки (актуализация)
- **Индекс `:11`:** добавлен `398 pytest offline` в строку текущей волны SEC-06 (для консистентности с остальными P3-записями).

Код и стори **не менялись** (правок не требовали — исполнение верное). Findings F1/F2 — LOW, вне обязательной доработки SEC-06; F2 при желании закрывается отдельной live-integration-мелочью.
