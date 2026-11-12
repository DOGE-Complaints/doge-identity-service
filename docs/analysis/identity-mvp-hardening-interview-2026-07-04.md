# Продукт-арх интервью: доводка identity-задач MVP (2026-07-04)

> **Контекст:** [`mvp-integration-plan-2026-07-02.md` §3](../../../docs/analysis/mvp-integration-plan-2026-07-02.md) — фокусные задачи doge-identity: **SEC-06** (M-1), **IDS-DOC-DRAFT-05** (M-3), **IDS-DEPLOY-01** (M-2/M-6).
> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc); решения приняты оператором в интервью, обоснованы кодом (`file:line`).
> **Назначение:** SSOT решений D-1…D-6 — референс для стори, которые обновляются после этого отчёта.
> **Update 2026-07-09:** `IDS-DEPLOY-01` retired — deployability superseded by [`run-and-healthcheck.md`](../runbook/run-and-healthcheck.md); **D-4** (`DEV_OTP_ECHO`) dropped (OTP на Railway — Telnyx или local+file).

---

## Сводка решений

| # | Тема | Решение | Затронутые стори |
|---|------|---------|------------------|
| **D-1** | Стратегия JWT-алгоритмов | **JWKS-only** — убрать HS256 полностью | SEC-06 |
| **D-2** | Включение JWKS | По наличию **реального `SUPABASE_URL`** (убрать sentinel `demo.local`) | SEC-06, DEPLOY-01 |
| **D-3** | Профиль railway | **`APP_PROFILE=pilot`** | DEPLOY-01 |
| **D-4** | OTP в облаке | **Лог-строка за отдельным флагом** (не привязан к профилю) | DEPLOY-01 |
| **D-5** | `SUPABASE_JWT_SECRET` | **Удалить** из конфига и pilot-required (мёртв после D-1) | SEC-06, DEPLOY-01 |
| **D-6** | GPT↔identity OAuth | **Остаётся каноном**; docs фиксируют submit=браузер | DOC-DRAFT-05 |

---

## D-1 · JWKS-only (убрать HS256)

**Решение:** валидатор проверяет только асимметричные Cloud-токены (ES256/RS256/ES384/ES512) через JWKS. HS256-путь удаляется целиком.

**Почему.** Supabase Cloud подписывает токены ES256 ([supabase_validator.py:103](../../src/core/auth/supabase_validator.py) диспетч по `alg`); HS256 ([:73](../../src/core/auth/supabase_validator.py)) нужен был лишь для локального demo/оффлайн-тестов и нёс дыру подделки (fallback-секрет, см. D-5). Продукт живёт на Cloud → HS256 не нужен, а его удаление закрывает класс уязвимости в корне.

**Аналитика последствий (что это ломает/чинит):**
- ✅ **Дыра W5 исчезает полностью** — нет HS256 → нет общего секрета → нечего подделывать.
- ⚠️ **Тесты валидатора переписываются, а не дополняются.** Все 9 тестов [`test_supabase_jwt_validator.py`](../../tests/test_supabase_jwt_validator.py) минтят HS256-токены — они **сломаются**. Нужно перевести сюиту на ES256 + **мок-JWKS** (инъекция фейкового `JwksCache`). Это делает **W2 (DI) обязательным**, а не «желательным» — без инъекции кэша оффлайн-тест ES256 невозможен.
- ⚠️ **Локальный полностью-оффлайн dev** (без реального `SUPABASE_URL`) не сможет валидировать реальные токены — валидатор честно отклонит (fail-closed). Приемлемо: логика покрыта мок-JWKS тестами; `make serve` против Cloud работает (JWKS on по D-2).
- ✅ Сохраняются: `aud=authenticated` (закрыт SEC-03), `iss`/`sub`/`exp`/`role`, reject `alg` вне whitelist, refresh-on-unknown-kid. Клеймы валидируются общим `_claims_from_token` — от удаления HS256 не страдают.
- ✅ Валидатор **упрощается**: убираются `_validate_hs256`, `OctKey.import_key`, ветка HS256; остаётся один путь.

**Изменяемый код:** [`supabase_validator.py`](../../src/core/auth/supabase_validator.py) (удалить HS256-ветку/ключ), [`providers.py:109`](../../src/core/infrastructure/providers.py) (убрать `jwt_secret=`).

---

## D-2 · JWKS включается по реальному `SUPABASE_URL`

**Решение:** JWKS-кэш активен, когда задан непустой реальный `SUPABASE_URL`. Убрать эвристику `not endswith("demo.local")` ([:51](../../src/core/auth/supabase_validator.py)) и sentinel `"https://demo.local"` ([providers.py:110](../../src/core/infrastructure/providers.py)).

**Почему.** Текущая эвристика — неявный контракт между двумя файлами через строку-маркер (magic-string, W3): легко сломать на деплое (если URL уедет в фолбэк — ES256 Cloud отвалится 401). Гейт «есть реальный URL → есть JWKS» совпадает с фактом: наличие Supabase-URL и означает, что мы против Cloud.

**Аналитика:**
- Связка с **D-1**: раз HS256 убран, при пустом URL валидировать нечем → это осознанный fail-closed (нет тихого fallback на слабый HS256).
- Связка с **DEPLOY-01**: на pilot `SUPABASE_URL` обязателен (уже в pilot-required) → JWKS всегда on в проде. Тесты подают URL + мок-кэш.
- Реализация: JWKS-кэш **инъектируется** (W2) на основе конфига; решение «включать ли» переносится в `providers.py` (явно), а не прячется в валидаторе.

---

## D-3 · railway = `APP_PROFILE=pilot`

**Решение:** деплой identity на railway идёт в строгом профиле `pilot`.

**Почему.** Pilot fail-fast ([schema.py:185+](../../src/core/config/schema.py)) не даёт сервису стартовать без критичных секретов — ловит забытый секрет **на старте**, а не в рантайме 401-ами. Ближе к боевому; безопаснее для реального Cloud.

**Аналитика:**
- Pilot запрещает `SMS_PROVIDER=file` ([schema.py:182](../../src/core/config/schema.py)) → на railway SMS через **`mock`** (ФС всё равно эфемерна). Чтение OTP — по **D-4**.
- Pilot требует секреты; список **сокращается** на `SUPABASE_JWT_SECRET` (D-5).
- Отдельный флаг OTP-эха (D-4) намеренно **не** завязан на профиль → работает и под pilot для окна ручного теста.

---

## D-4 · OTP в облаке — лог-строка за отдельным флагом

**Решение:** при поднятом отдельном флаге (напр. `DEV_OTP_ECHO=true`, **не** привязан к `APP_PROFILE`) сервис печатает OTP в stdout → виден в `railway logs`.

**Почему.** На railway ФС эфемерна и недоступна снаружи (file-sink не прочитать), mock прячет код в память. Лог-строка — самый дешёвый способ получить код для ручного онбординга до подключения Telnyx. Независимый флаг (а не `APP_PROFILE=demo`) нужен, потому что деплой идёт в **pilot** (D-3).

**Аналитика / ограничения:**
- 🔒 **OTP в логах — осознанный анти-паттерн**: строго за флагом, **выключено по умолчанию**, убрать после Telnyx. Задокументировать как временную dev-меру.
- Место: хендлер phone-request / mock-sender; флаг читается из конфига. Укладывается в **DEPLOY-01 §D** (не новая стори).
- После Telnyx флаг гасится — реальные SMS приходят на телефон.

---

## D-5 · Удалить `SUPABASE_JWT_SECRET`

**Решение:** убрать переменную из конфига (`AppConfig` поле, загрузку, pilot-required) и из wiring.

**Почему (по коду).** Единственный потребитель — HS256-валидатор ([providers.py:109](../../src/core/infrastructure/providers.py) `jwt_secret=...`); больше **нигде** (OAuth-самоподпись использует `OAUTH_ACCESS_TOKEN_SECRET`, не этот). После D-1 переменная мертва. Сейчас она в pilot-required ([schema.py:190](../../src/core/config/schema.py)) — это ложное требование секрета, который ничего не валидирует.

**Аналитика:**
- Убирает дыру **W5** «в корне» (нет секрета — нет fallback `test-secret-for-demo`).
- **DEPLOY-01 §C:** список обязательных env на railway **сокращается** (минус `SUPABASE_JWT_SECRET`).
- Изменяемый код: [`schema.py:34,160,190,215`](../../src/core/config/schema.py), [`providers.py:109`](../../src/core/infrastructure/providers.py). Проверить, что pilot-тесты и `.env.example` синхронизированы.

---

## D-6 · GPT↔identity OAuth остаётся каноном

**Решение:** OAuth-сервер identity (`/oauth/authorize`, `/oauth/token`, `/oauth/introspect` + редирект на spa login/verify) остаётся штатным способом GPT авторизовать юзера. **DOC-DRAFT-05** только фиксирует, что **подача истории** идёт браузером (browser-submit), не трогая статус OAuth в коде.

**Почему.** Хендшейк — единственный механизм user-scoped авторизации GPT-Actions на будущее; удалять его при переходе на browser-submit преждевременно. Gateway удалил лишь **свой** introspection-клиент (продуктовый submit-путь), но identity-OAuth как способность остаётся.

**Аналитика:**
- DOC-DRAFT-05 сужается до чистого docs-sync: [`04-security.md`](../../docs/runtime-docs/04-security.md) §A и [`09-gateway-expectations.md`](../../docs/runtime-docs/09-gateway-expectations.md) — заменить «GPT сам шлёт историю» на browser-submit, **сохранив** OAuth/introspection/`/me`/`phone_verified`/`verification_required` как валидные.
- ⚠️ Наблюдение (вне scope DRAFT-05): у `/oauth/introspect` в identity после удаления gateway-клиента может не остаться продуктового потребителя. Не блокер MVP; зафиксировать как отдельный вопрос позже (не в этой волне).

---

## Влияние на стори (что обновляется после отчёта)

| Стори | Ключевые правки от решений |
|-------|----------------------------|
| **SEC-06** | Разворот на **JWKS-only** (D-1): убрать HS256; W5 «растворяется» (resolved-by-design); W3 → гейт по реальному URL (D-2); **W2 DI обязателен** (мок-JWKS для тестов); **W4 тесты переписать** на ES256; удалить `SUPABASE_JWT_SECRET` (D-5); docs → «JWKS/ES256-only» (не «HS256+JWKS»). |
| **IDS-DEPLOY-01** | Профиль **pilot** (D-3); secret-list **минус** `SUPABASE_JWT_SECRET` (D-5); реальный `SUPABASE_URL` обязателен для JWKS (D-2); SMS `mock` + **флаг OTP-эха** в лог (D-4). |
| **IDS-DOC-DRAFT-05** | Подтверждён docs-only; **OAuth остаётся** (D-6); привести к общему стандарту (Зачем/Контекст-verified/Scope/AC/Швы). |

**Следующий шаг:** обновить три стори до общего стандарта, вшив решения D-1…D-6 со ссылкой на этот отчёт.
