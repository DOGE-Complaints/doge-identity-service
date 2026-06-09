# Жёсткий аудит исполнения STORY-IDS-EID-07 (provider-agnostic OIDC-тулкит)

> **Дата:** 2026-06-08
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-EID-07-oidc-toolkit`](../tasks/backlog-stories/STORY-IDS-EID-07-oidc-toolkit.md) vs фактический код. Исполнена под **EPIC-IDS-09-eid-verification** (pkg-000020), 6 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): EPIC-IDS-09, task queue t01–t06 (pkg-000020).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Модуль | `src/core/security/oidc/`: `discovery.py`, `jwks_cache.py`, `id_token.py`, `toolkit.py` |
| Классы | `OidcDiscoveryClient`, `JwksCache`, `IdTokenValidator`, `OidcToolkit` |
| Provider-agnostic | в `oidc/` нет импортов authentigate/eideasy ✅ |
| Проводка | `ProviderRuntime.oidc: OidcToolkit | None` ([runtime.py:21](../../src/core/providers/runtime.py)); `build_oidc_toolkit(http_client)` только для non-mock ([runtime_factory.py:22-24](../../src/core/providers/runtime_factory.py)) |
| Тесты | [test_oidc_toolkit.py](../../tests/test_oidc_toolkit.py) — 8 (`httpx.MockTransport`, без сети) |
| **Offline-сюита** | **244 passed, 10 deselected** ✅ (было 232 → +12) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-09, pkg-000020) | Факт | Статус |
|--------------------------------|------|--------|
| t01 oidc discovery client | `OidcDiscoveryClient.get_discovery` — fetch `.well-known/openid-configuration` + per-issuer кэш ([discovery.py:19-43](../../src/core/security/oidc/discovery.py)) | 🟢 |
| t02 jwks cache refresh on unknown kid | `JwksCache`: TTL + `resolve_key_set_for_kid` → refresh при неизвестном kid ([jwks_cache.py:13-55](../../src/core/security/oidc/jwks_cache.py)) | 🟢 |
| t03 id token validator rs256 claims | `IdTokenValidator.validate`: RS256 + `iss/aud/exp/iat/nonce` через `JWTClaimsRegistry`; невалид → `OidcIdTokenValidationError(IDENTITY_VALIDATION_FAILED)` ([id_token.py:27-74](../../src/core/security/oidc/id_token.py)) | 🟢 |
| t04 oidc toolkit provider runtime wire | `OidcToolkit` + слот `ProviderRuntime.oidc`; `build_oidc_toolkit` для non-mock | 🟢 |
| t05 offline oidc toolkit mocked http tests | 8 тестов на `httpx.MockTransport` (discovery cache / unknown-kid refresh / RS256 valid / failure→IDENTITY_VALIDATION_FAILED / runtime-wire / mock-omit) | 🟢 |
| t06 story acceptance verification | AC 5/5 (см. §2) | 🟢 |
| **STORY-IDS-EID-07** | OIDC-тулкит (discovery/JWKS/id_token) | **🟢 Done** |

Индекс ([`bullrun-launch-index.md:68`](../tasks/bullrun-launch-index.md)) держит эпик `🟡 In Progress — EID-01/03/04/05/06/07 🟢` — корректно.

---

## 2. Сверка Acceptance Criteria story

| AC | Факт (код + тест) | Вердикт |
|----|-------------------|---------|
| Модуль `core/security/oidc/` с 3 компонентами, provider-agnostic | discovery/jwks_cache/id_token + toolkit; нет провайдер-импортов | ✅ |
| Discovery и JWKS кэшируются; неизвестный `kid` → обновление JWKS | discovery per-issuer cache; `JwksCache.resolve_key_set_for_kid` refresh ([jwks_cache.py:47-55](../../src/core/security/oidc/jwks_cache.py)); тесты `..._caches_openid_configuration`, `..._resolves_unknown_kid_after_refresh` | ✅ |
| `IdTokenValidator`: RS256 + `iss/aud/exp/iat/nonce`; невалид → доменная ошибка (→ `IDENTITY_VALIDATION_FAILED`) | id_token.py:45,60-66; `OidcIdTokenValidationError(code=IDENTITY_VALIDATION_FAILED)`; тесты `..._accepts_valid_rs256_token`, `..._maps_failures_to_identity_validation_failed`, `..._refreshes_jwks_on_unknown_kid` | ✅ |
| Тулкит доступен провайдерам через `ProviderRuntime` | runtime.py:21 + runtime_factory.py:24; тесты `..._wires_oidc_for_non_mock`, `..._omits_oidc_in_mock_mode` | ✅ |
| Тесты с замоканными discovery/JWKS/подписью; offline без сети | `httpx.MockTransport`; 244 passed | ✅ |

**Вывод:** все 5 AC выполнены и покрыты тестами (8). F8 Authentigate-аудита (нет OIDC-валидации) закрыт **общим** тулкитом, не привязанным к провайдеру.

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| F1 | MEDIUM | Doc-stale | backlog-story помечена `⚪ Todo` (стр.6), реально 🟢 Done под `EPIC-IDS-09` (pkg-000020); «Точки в коде (текущее состояние)» описывают пред-состояние («`joserfc` только HS256/симметрично») — теперь есть RS256 OIDC-тулкит | [`STORY-IDS-EID-07...md:6,25-29`](../tasks/backlog-stories/STORY-IDS-EID-07-oidc-toolkit.md) |

Иных материальных findings нет. Наблюдения (severity none, по scope):
- `OidcDiscoveryClient` кэширует discovery **без TTL** (per-issuer навсегда). Для стабильных endpoint'ов приемлемо; scope требовал TTL только для JWKS. Не gap.
- `oidc` строится только для non-mock (как `http_client`) — в mock/in-memory `oidc=None`. Консистентно с EID-03, без сетевых клиентов в dev. Не gap.

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **244 passed** (было 232 → +12 OIDC-тестов), **ожидаемо** |
| Новый модуль `core/security/oidc/` | аддитивный; существующий `supabase_validator` (HS256) не затронут |
| `ProviderRuntime` слот `oidc` | был `Any | None` (EID-03) → теперь типизирован `OidcToolkit | None`; non-mock получает тулкит, mock — None |
| Сеть в offline | нет (всё на `httpx.MockTransport`) |
| eID-флоу (EID-01/05/06) | не затронут — сюита зелёная |

Регрессий не выявлено.

---

## 5. Итог

- **STORY-IDS-EID-07 — 🟢 исполнена полно:** provider-agnostic OIDC-тулкит (discovery+cache, JWKS TTL+refresh-on-unknown-kid, RS256 id_token validation с `iss/aud/exp/iat/nonce` → канон `IDENTITY_VALIDATION_FAILED`), доступен через `ProviderRuntime` для non-mock. AC 5/5, 8 тестов на моках. F8 Authentigate-аудита закрыт переиспользуемым тулкитом.
- **Единственный finding — F1 (doc-stale backlog-story)**, рекуррентный паттерн (Status ⚪→🟢 + «точки в коде»).

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; статусы тасков сверены по коду.
- [x] AC сверены по коду **и** тестам; полный набор claims (`exp/iat` подтверждён в id_token.py:63-64), provider-agnostic проверен grep'ом.
- [x] Регрессий нет; 232→244 объяснён; offline без сети (MockTransport).
- [x] Наблюдения (discovery без TTL; oidc=None в mock) отделены от material findings (по scope, не gap).
