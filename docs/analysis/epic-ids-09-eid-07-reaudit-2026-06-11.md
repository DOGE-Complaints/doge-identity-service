# Жёсткий аудит (re-audit) исполнения STORY-IDS-EID-07 (provider-agnostic OIDC-тулкит)

> **Дата:** 2026-06-11
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-EID-07-oidc-toolkit`](../tasks/backlog-stories/eid/STORY-IDS-EID-07-oidc-toolkit.md) vs фактический код. Исполнена под **EPIC-IDS-09-eid-verification** (alias `EPIC-IDS-EID`), pkg-000020, 6 tasks.
> **Контекст:** повторный аудит (первый — [`epic-ids-09-eid-07-audit-2026-06-08.md`](./epic-ids-09-eid-07-audit-2026-06-08.md)); проверка состояния по текущему коду + статус F1.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): EPIC-IDS-09, EID-07 🟢 (стр.95, task-queue стр.499-504).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Модуль | `src/core/security/oidc/`: `discovery.py`, `jwks_cache.py`, `id_token.py`, `toolkit.py`, `__init__.py` |
| Классы | `OidcDiscoveryClient`+`OidcDiscoveryDocument`, `JwksCache`, `IdTokenValidator`+`OidcIdTokenValidationError`, `OidcToolkit`+`build_oidc_toolkit` |
| Provider-agnostic | в `oidc/` нет импортов authentigate/eideasy (grep чисто) ✅ |
| Проводка | `ProviderRuntime.oidc: OidcToolkit | None` ([runtime.py:21](../../src/core/providers/runtime.py)); `build_oidc_toolkit` только non-mock ([runtime_factory.py:22-25,34](../../src/core/providers/runtime_factory.py)) |
| Якорь-паттерн | `supabase_validator.py` (HS256/`JWTClaimsRegistry`) — путь story `src/core/auth/supabase_validator.py` **подтверждён** (файл существует) |
| Тесты | [test_oidc_toolkit.py](../../tests/test_oidc_toolkit.py) — 8 (`httpx.MockTransport`, без сети) |
| **Offline-сюита** | **329 passed, 11 deselected** ✅ (канонический `pytest -m "not live_integration"`) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-09, pkg-000020) | Факт | Статус |
|--------------------------------|------|--------|
| t01 oidc discovery client | `OidcDiscoveryClient.get_discovery` — fetch `.well-known/openid-configuration` + per-issuer кэш ([discovery.py:25-45](../../src/core/security/oidc/discovery.py)) | 🟢 |
| t02 jwks cache refresh on unknown kid | `JwksCache`: TTL (3600с дефолт) + `resolve_key_set_for_kid` → `force_refresh` при `InvalidKeyIdError` ([jwks_cache.py:32-58](../../src/core/security/oidc/jwks_cache.py)) | 🟢 |
| t03 id token validator rs256 claims | `IdTokenValidator.validate`: RS256 + `iss/aud/exp/iat/nonce` через `JWTClaimsRegistry`; невалид → `OidcIdTokenValidationError(IDENTITY_VALIDATION_FAILED)` ([id_token.py:33-74](../../src/core/security/oidc/id_token.py)) | 🟢 |
| t04 oidc toolkit provider runtime wire | `OidcToolkit` (lazy per-jwks_uri кэш) + слот `ProviderRuntime.oidc`; `build_oidc_toolkit` для non-mock ([toolkit.py](../../src/core/security/oidc/toolkit.py), [runtime_factory.py:25](../../src/core/providers/runtime_factory.py)) | 🟢 |
| t05 offline oidc toolkit mocked http tests | 8 тестов на `httpx.MockTransport` (discovery cache / unknown-kid refresh / RS256 valid / failure→IDENTITY_VALIDATION_FAILED / runtime-wire / mock-omit) | 🟢 |
| t06 story acceptance verification | AC 5/5 (см. §2); pipeline-story `Status: 🟢 Done` (стр.7), индекс t01–t06 🟢 ([bullrun-launch-index.md:499-504](../tasks/bullrun-launch-index.md)) | 🟢 |
| **STORY-IDS-EID-07** | OIDC-тулкит (discovery/JWKS/id_token) | **🟢 Done** |

Индекс держит эпик корректно: `EPIC-IDS-09 … EID-07 🟢` ([bullrun-launch-index.md:95](../tasks/bullrun-launch-index.md)).

---

## 2. Сверка Acceptance Criteria story (по коду + тестам)

| AC | Факт (код + тест) | Вердикт |
|----|-------------------|---------|
| Модуль `core/security/oidc/` с `OidcDiscoveryClient`/`JwksCache`/`IdTokenValidator`, provider-agnostic | три класса + `OidcToolkit`; нет провайдер-импортов | ✅ |
| Discovery и JWKS кэшируются; неизвестный `kid` → обновление JWKS | discovery per-issuer cache ([discovery.py:27-31](../../src/core/security/oidc/discovery.py)); `JwksCache.resolve_key_set_for_kid` force_refresh ([jwks_cache.py:50-58](../../src/core/security/oidc/jwks_cache.py)); тесты `..._caches_openid_configuration`, `..._resolves_unknown_kid_after_refresh` | ✅ |
| `IdTokenValidator`: RS256 + `iss/aud/exp/iat/nonce`; невалид → `IDENTITY_VALIDATION_FAILED` | id_token.py:45 (RS256), 60-66 (claims вкл. exp/iat); `OidcIdTokenValidationError(code=IDENTITY_VALIDATION_FAILED)`; тесты `..._accepts_valid_rs256_token`, `..._maps_failures_to_identity_validation_failed` | ✅ |
| Тулкит доступен провайдерам через `ProviderRuntime` | runtime.py:21 + runtime_factory.py:34; тесты `..._wires_oidc_for_non_mock`, `..._omits_oidc_in_mock_mode` | ✅ |
| Тесты с замоканными discovery/JWKS/подписью; offline без сети | `httpx.MockTransport`; **329 passed** | ✅ |

**Вывод:** все 5 AC выполнены и покрыты тестами (8). F8 Authentigate-аудита (нет OIDC id_token-валидации) закрыт **общим** тулкитом, не привязанным к провайдеру.

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F1** | MEDIUM | Doc-stale / SSOT-contradiction | Backlog-story `Status: ⚪ Todo` (стр.6) + AC `[ ]` (стр.32-36) + секция «Точки в коде (текущее состояние)» описывает пред-состояние («`joserfc` только HS256/симметрично», стр.26) — реально 🟢 Done под pkg-000020. **Самопротиворечие:** соседний epic-индекс [`EPIC-IDS-EID.md:24`](../tasks/backlog-stories/eid/EPIC-IDS-EID.md) уже держит EID-07 = `🟢 Done`, а сам story-файл — `⚪ Todo`. Тот же F1, что отмечен в аудите 2026-06-08 — **до сих пор не закрыт**. **Как закрыть:** Status ⚪→🟢, AC `[ ]`→`[x]`, обновить «Точки в коде» (добавить `src/core/security/oidc/` модуль, RS256-валидацию). | [`STORY-IDS-EID-07...md:6,26,32-36`](../tasks/backlog-stories/eid/STORY-IDS-EID-07-oidc-toolkit.md) |

Иных материальных findings нет. Наблюдения (severity none, по scope, **не gap**):
- **Discovery кэшируется без TTL** (per-issuer навсегда, [discovery.py:23,44](../../src/core/security/oidc/discovery.py)); scope требовал TTL только для JWKS. JWKS-кэш с TTL+refresh-on-unknown-kid реализован. Не gap.
- **`oidc=None` в mock/in-memory** ([runtime_factory.py:22-25](../../src/core/providers/runtime_factory.py)) — строится только non-mock (как `http_client`). Консистентно с EID-03, без сети в dev. Не gap.
- **`OidcToolkit` — lazy per-`jwks_uri` кэш** валидаторов/JWKS ([toolkit.py:20-29](../../src/core/security/oidc/toolkit.py)); сверх минимума AC, поддерживает несколько IdP одним тулкитом. Усиление, не gap.
- **Claims-маппинг id_token → `EIDVerificationResult`, PKCE, scope/acr** — **вне scope EID-07** (адаптер Authentigate [EID-02](../tasks/backlog-stories/eid-deferred/STORY-IDS-EID-02-real-eid-providers.md), [EID-08](../tasks/backlog-stories/eid/STORY-IDS-EID-08-session-secret-box.md), [EID-04](../tasks/backlog-stories/eid/STORY-IDS-EID-04-provider-owned-config.md)). EID-02 отложен (eid-deferred). Не gap.

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **329 passed, 11 deselected** (на 2026-06-08 было 244; рост за счёт PV-01..06 / EID-08 — OIDC-тесты стабильны) |
| Модуль `core/security/oidc/` | без изменений с 2026-06-09 (даты файлов); аддитивен; `supabase_validator` (HS256) не затронут |
| `ProviderRuntime` слот `oidc` | типизирован `OidcToolkit | None`; non-mock получает тулкит, mock — None |
| Сеть в offline | нет (всё на `httpx.MockTransport`) |
| eID/phone/OAuth | не затронуты — сюита зелёная |

Регрессий не выявлено. Код EID-07 не менялся со времени первого аудита; интеграция с последующими волнами (EID-08, PV) не сломала OIDC-тесты.

---

## 5. Итог

- **STORY-IDS-EID-07 — 🟢 исполнена полно (подтверждено re-audit):** provider-agnostic OIDC-тулкит (discovery+cache, JWKS TTL+refresh-on-unknown-kid, RS256 id_token validation с `iss/aud/exp/iat/nonce` → канон `IDENTITY_VALIDATION_FAILED`), доступен через `ProviderRuntime` для non-mock. AC 5/5, 8 тестов на моках. F8 Authentigate-аудита закрыт переиспользуемым тулкитом.
- **Единственный finding — F1 (MEDIUM, doc-stale)**, рекуррентный и **открыт с 2026-06-08**: story-файл `⚪ Todo` противоречит собственному epic-индексу (`EPIC-IDS-EID.md` = 🟢) и pipeline-story/индексу.
- Наблюдения (discovery без TTL; oidc=None в mock; lazy per-jwks_uri кэш; claims/PKCE → EID-02/04/08) — по scope, не gaps.

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; статусы 6 тасков сверены по коду (pipeline-story 🟢, индекс t01–t06 🟢).
- [x] AC 5/5 сверены по коду **и** тестам; полный claim-set (`exp/iat` в id_token.py:63-64), provider-agnostic проверен grep'ом.
- [x] Якорь-путь story (`src/core/auth/supabase_validator.py`) подтверждён существующим.
- [x] Регрессий нет; код не менялся с 2026-06-09; OIDC-тесты зелёные в текущей сюите (329).
- [x] F1 классифицирован как SSOT-contradiction (story-файл vs `EPIC-IDS-EID.md`), отмечен как открытый с прошлого аудита.
