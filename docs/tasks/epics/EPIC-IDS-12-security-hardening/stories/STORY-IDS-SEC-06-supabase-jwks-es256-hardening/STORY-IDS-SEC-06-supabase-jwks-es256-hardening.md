# STORY-IDS-SEC-06 — Supabase-JWT валидатор: JWKS-only, DI, честные тесты, без мёртвого кода

## Meta
- **Key:** `STORY-IDS-SEC-06-supabase-jwks-es256-hardening`
- **Parent Epic:** [`../../EPIC-IDS-12-security-hardening.md`](../../EPIC-IDS-12-security-hardening.md)
- **Epic alias (код/backlog):** `EPIC-IDS-SEC` · [`EPIC-IDS-SEC`](../../../../backlog-stories/security-hardening/EPIC-IDS-SEC.md)
- **Status:** 🟢 Done (pkg-000042, P3 2026-07-04)
- **Severity:** 🟠 HIGH — hot-path аутентификации; change-propagation через всю тест-суиту
- **Тип:** implement (refactor/removal + tests + docs; анти-паттерны «Legacy Accumulation» / «Contract Violations»)
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md)
- **Decision Ref:** [`../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md); [`identity-mvp-hardening-interview-2026-07-04.md`](../../../../../analysis/identity-mvp-hardening-interview-2026-07-04.md) — **D-1** JWKS-only, **D-2** гейт по реальному URL, **D-5** удалить `SUPABASE_JWT_SECRET`.
- **Зависит от:** [SEC-03](../STORY-IDS-SEC-03-jwt-validation-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md) (🟢 `aud`+клеймы — тот же валидатор; SEC-03 вынес «RS256/JWKS» в отдельную тему — это она)

## Зачем простыми словами
Из браузера логин «не сохранялся»: `GET /me` отдавал **401**, spa показывал «Session Expired». Причина — **Supabase Cloud подписывает JWT алгоритмом ES256** (асимметрично, проверка по публичным ключам JWKS), а наш валидатор знал только **HS256** (симметрично, общий секрет). ES256/JWKS-путь уже добавлен и закоммичен (`4c191ea`), но по-быстрому: остались костыли (magic-string `demo.local`, валидатор сам себе делает HTTP-клиент и кэш и не закрывает, мёртвый секрет), а **новый асимметричный путь не покрыт тестами** — вся суита до сих пор минтит HS256-токены.

**Решение (интервью D-1):** идём в **JWKS-only** — HS256-путь в Supabase-валидаторе **удаляется целиком**. Cloud его не использует, а он нёс дыру подделки (публичный fallback-секрет `test-secret-for-demo`). Это упрощает валидатор, закрывает дыру «в корне» и снимает мёртвый секрет `SUPABASE_JWT_SECRET`. **Цена:** тест-харнес авторизации (14 файлов) переводится с HS256 на ES256+мок-JWKS, а DI (инъекция кэша ключей) становится обязательным.

> ⚠️ **Важная граница (change-propagation):** HS256 в [`oauth/access_token_jwt.py:26`](../../../../../../src/core/oauth/access_token_jwt.py) — **ДРУГОЙ** механизм (самоподпись OAuth-access-токенов на `OAUTH_ACCESS_TOKEN_SECRET`), к Supabase-валидатору отношения не имеет. **НЕ трогать.** Поэтому grep-гейты ниже прицельные (не «HS256 по всему src»).

## Scope (только требования)

### Инвентарь (verified по коду 2026-07-04)
| Компонент | Путь | Действие |
|-----------|------|----------|
| `_validate_hs256`, `self._key = OctKey.import_key`, ветка `alg=="HS256"` | [`supabase_validator.py:43,72-73,101-102`](../../../../../../src/core/auth/supabase_validator.py) | ❌ **REMOVE** (D-1) |
| аргумент `jwt_secret` конструктора + `self._jwt_secret` | [`supabase_validator.py:35,40`](../../../../../../src/core/auth/supabase_validator.py) | ❌ **REMOVE** (D-1/D-5) |
| эвристика `not endswith("demo.local")` + sentinel `"https://demo.local"` | [`supabase_validator.py:51`](../../../../../../src/core/auth/supabase_validator.py); [`providers.py:110`](../../../../../../src/core/infrastructure/providers.py) | ❌ **REMOVE** → гейт по реальному URL (D-2) |
| `JwksCache(client,…)` + `http_client or httpx.Client(...)` внутри `__init__` | [`supabase_validator.py:51-54`](../../../../../../src/core/auth/supabase_validator.py) | ⚠️ **REFACTOR** → инъекция снаружи (W2) |
| ES256/JWKS путь + диспетч по `alg` + `_JWKS_ALGORITHMS` | [`supabase_validator.py:76-105`](../../../../../../src/core/auth/supabase_validator.py) | ✅ **KEEP** (ядро) |
| клеймы `_claims_from_token` (`aud`/`iss`/`sub`/`exp`/`role`) | [`supabase_validator.py`](../../../../../../src/core/auth/supabase_validator.py) | ✅ **KEEP** (SEC-03) |
| `SUPABASE_JWT_SECRET` / `supabase_jwt_secret` (поле, load, pilot-required, AppConfig) | [`schema.py:34,160,190,215`](../../../../../../src/core/config/schema.py) | ❌ **REMOVE** (D-5) |
| fallback `... or "test-secret-for-demo"` | [`providers.py:109`](../../../../../../src/core/infrastructure/providers.py) | ❌ **REMOVE** (D-5) |
| `SUPABASE_JWT_SECRET=` + `SUPABASE_TEST_JWT_SECRET` заметка | [`.env.example:29,37,41`](../../../../../../.env.example) | ⚠️ **EDIT** (снять/пометить) |
| HS256 OAuth-самоподпись (`OAUTH_ACCESS_TOKEN_SECRET`) | [`oauth/access_token_jwt.py:26`](../../../../../../src/core/oauth/access_token_jwt.py) | ✅ **KEEP — не трогать** |
| DI-эталон: `build_oidc_toolkit(http_client)` + `OidcToolkit.jwks_cache(uri)` | [`toolkit.py:20-35`](../../../../../../src/core/security/oidc/toolkit.py) | ✅ **REUSE** (образец для W2) |

### Change-propagation (analysis.mdc §2) — ВСЕ затронутые
**Тест-харнес авторизации (крит):** суита минтит Supabase-Bearer **через HS256** (`jwt.encode({"alg":"HS256"}, claims, OctKey)`), подписывая fallback-секретом. При JWKS-only это перестаёт валидироваться → **ломается ~14 файлов**, не только валидатор-тесты:
- Прямые минтеры HS256: [`test_supabase_jwt_validator.py`](../../../../../../tests/test_supabase_jwt_validator.py), [`test_supabase_jwt_auth.py`](../../../../../../tests/test_supabase_jwt_auth.py), `test_me_profile.py`, `test_phone_verification_flow.py`, `test_audit_ip_ua_hashing.py`, `test_eid_callback_redirect.py`, `test_eid_verification_flow.py`, `test_oauth_introspection.py`, `test_oauth_server_flow.py`, `test_epic_ids_04_integration.py`, `test_asgi_transport.py`, `test_http_transport_smoke.py`, `test_canonical_provider_contract.py`, `test_security_primitives.py`.
- [`conftest.py:35`](../../../../../../tests/conftest.py) выставляет `SUPABASE_JWT_SECRET=""` (autouse) — точка, где сейчас держится тестовый секрет.
- [`test_config_schema.py`](../../../../../../tests/test_config_schema.py) — проверяет pilot-required (там `SUPABASE_JWT_SECRET`) → обновить.
- [`test_supabase_runbook_docs.py`](../../../../../../tests/test_supabase_runbook_docs.py) — assert по содержимому runbook → синхронизировать.
- [`integration/supabase/test_supabase_jwt_live_sanity.py`](../../../../../../tests/integration/supabase/test_supabase_jwt_live_sanity.py) (`live_integration`, offline-deselected) — согласовать с JWKS-only.

**Конфиг/доки:** [`.env.example`](../../../../../../.env.example); [`07-env-configuration-spec.md`](../../../../../requirements/07-env-configuration-spec.md), [`09-supabase-jwt-validation.md`](../../../../../requirements/09-supabase-jwt-validation.md), [`04-security.md`](../../../../../runtime-docs/04-security.md); runbooks [`supabase-project-setup.md`](../../../../../runbook/supabase-project-setup.md), [`run-and-healthcheck.md`](../../../../../runbook/run-and-healthcheck.md). *(14-oauth-server и `access_token_jwt` HS256 — OAuth, НЕ трогать.)*

### Подзадачи
- **T01 — Change-propagation аудит.** Зафиксировать полный список потребителей удаляемого (grep `_validate_hs256`/`supabase_jwt_secret`/`test-secret-for-demo`/`demo.local`/`alg":"HS256"` по `src/` и `tests/`), явно исключив OAuth `access_token_jwt`. Утвердить план миграции тестового харнеса (T05) и список доков (T07).
- **T02 — Валидатор → JWKS-only (D-1/D-2).** Удалить `_validate_hs256`, `OctKey`-импорт, `self._key`, параметр `jwt_secret`, ветку `alg=="HS256"`; оставить только асимметричный путь (`_JWKS_ALGORITHMS`). Гейт JWKS — по факту непустого реального `supabase_url`; убрать `demo.local`-эвристику и sentinel.
- **T03 — DI кэша ключей (W2).** Вынести создание `JwksCache`/`http_client` в `providers.py` по образцу [`build_oidc_toolkit`](../../../../../../src/core/security/oidc/toolkit.py); валидатор **принимает** `JwksCache` (или `None`) снаружи, сам `httpx.Client` не создаёт → устранить утечку незакрытого клиента. Сузить `except Exception` (W6) до ожидаемых ошибок.
- **T04 — Удалить `SUPABASE_JWT_SECRET` (D-5).** Снять из [`schema.py:34,160,190,215`](../../../../../../src/core/config/schema.py) (поле, load, **pilot-required**, AppConfig), `providers.py:109` (fallback), `.env.example`. Обновить `test_config_schema.py` (pilot-required без него).
- **T05 — Тестовый харнес: HS256 → ES256+мок-JWKS (крит).** Общий хелпер: ES256-keypair, мок-`JwksCache` с публичным ключом (инъекция через DI из T03), функция подписи токена приватным ключом; реальный тест-`SUPABASE_URL` (JWKS on). Мигрировать **все 14 файлов** + `conftest.py` с HS256-минта на общий ES256-хелпер. Убрать хардкод `test-secret-for-demo`.
- **T06 — Тесты валидатора (ES256/JWKS).** happy ES256; unknown-`kid` → refresh → успех; `kid` не найден после refresh → ошибка; `alg` вне whitelist / `alg=none` / `alg=HS256` → reject; `_jwks_cache is None` при asymmetric → понятная ошибка; клеймы `aud`/`iss`/`sub`/`exp`/`role` — перенести прежние кейсы на ES256.
- **T07 — Документация → as-built JWKS-only.** [`09`](../../../../../requirements/09-supabase-jwt-validation.md) («MVP выбор HS256»→JWKS/ES256-only), [`04-security.md:104`](../../../../../runtime-docs/04-security.md) (двойной путь → JWKS-only, сверить устаревший диапазон строк), [`07-env-configuration-spec.md`](../../../../../requirements/07-env-configuration-spec.md) + runbooks — снять `SUPABASE_JWT_SECRET`; синхронизировать `test_supabase_runbook_docs.py`.
- **T08 — Story gate.** Прицельные grep = 0 (см. AC); вся offline-сюита зелёная **после** миграции (не за счёт удаления живых тестов); live-sanity согласован; мёртвого/осиротевшего/сломанного кода нет.

## Вне scope
- **НЕ трогать** HS256 в OAuth-самоподписи ([`access_token_jwt.py`](../../../../../../src/core/oauth/access_token_jwt.py), другой секрет).
- **НЕ трогать** уже-верное: JWKS-путь, клеймы `aud`/`iss`/`sub`/`exp`/`role`, refresh-on-unknown-kid.
- OIDC `id_token.py`/`toolkit.py` — эталон, только reuse, не рефакторить.
- Live-интеграция Supabase — согласовать, но не гейтит offline-приёмку.

## Точки в коде (текущее состояние)
- Валидатор: [`supabase_validator.py`](../../../../../../src/core/auth/supabase_validator.py); wiring/DI: [`providers.py:108-110`](../../../../../../src/core/infrastructure/providers.py); DI-эталон [`toolkit.py`](../../../../../../src/core/security/oidc/toolkit.py), кэш [`jwks_cache.py`](../../../../../../src/core/security/oidc/jwks_cache.py).
- Config: [`schema.py:34,160,190,215`](../../../../../../src/core/config/schema.py), [`.env.example`](../../../../../../.env.example).
- Тесты: `test_supabase_jwt_validator.py`, `test_supabase_jwt_auth.py`, `conftest.py`, `test_config_schema.py`, `test_supabase_runbook_docs.py` + 12 минтеров (см. change-propagation).
- Доки: [`09`](../../../../../requirements/09-supabase-jwt-validation.md), [`04-security.md`](../../../../../runtime-docs/04-security.md), [`07`](../../../../../requirements/07-env-configuration-spec.md), runbooks.

## Acceptance Criteria
- [x] Debug-инструментация отсутствует (W1, verified `4c191ea`): `grep -n "_debug_log\|3c4b9a\|post-fix" src/` = пусто.
- [x] `grep -rn "_validate_hs256\|OctKey\|test-secret-for-demo\|demo\.local\|supabase_jwt_secret\|SUPABASE_JWT_SECRET" src/` → **пусто** (HS256/секрет Supabase-валидатора и sentinel удалены). *(HS256 в `oauth/access_token_jwt.py` сохранён — вне этого grep.)*
- [x] Валидатор принимает `JwksCache` снаружи (DI из `providers.py`), собственный `httpx.Client` не создаёт; клиент переиспользуется/закрывается (W2). `except` сужен (W6).
- [x] JWKS-гейт по реальному `supabase_url`; при пустом URL — fail-closed (нет HS256-фолбэка).
- [x] `SUPABASE_JWT_SECRET` удалён из `schema.py`, `providers.py`, `.env.example`; pilot-required без него; `test_config_schema.py` обновлён.
- [x] Тест-харнес переведён на ES256+мок-JWKS: Supabase `"alg": "HS256"` в tests/ отсутствует (OAuth access-token — отдельно); 14+ файлов зелёные.
- [x] Тесты валидатора ES256 (happy, unknown-kid→refresh, kid-not-found, alg-not-allowed, `alg=none`/`HS256` reject, jwks-unavailable, клеймы).
- [x] Доки [`09`](../../../../../requirements/09-supabase-jwt-validation.md)/[`04-security.md`](../../../../../runtime-docs/04-security.md)/[`07`](../../../../../requirements/07-env-configuration-spec.md)/runbooks приведены к **JWKS/ES256-only**; `test_supabase_runbook_docs.py` синхронизирован.
- [x] Полная offline-сюита зелёная: `.venv/bin/python -m pytest -q -m "not live_integration"` — **398 passed**, 12 deselected (2026-07-04).
- [ ] (Опц., live) реальный Supabase ES256-токен проходит `/me` (не 401) — `make smoke IDENTITY_URL=…`.

## Парадигма-якорь
[`09-supabase-jwt-validation.md`](../../../../../requirements/09-supabase-jwt-validation.md) (валидация Supabase-JWT, JWKS/ES256), [`runtime-docs/04-security.md`](../../../../../runtime-docs/04-security.md), DI-эталон OIDC [`security/oidc/`](../../../../../../src/core/security/oidc/).
