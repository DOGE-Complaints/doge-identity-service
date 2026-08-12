# EPIC-IDS-09 — eID Verification Flow

> **ID:** `EPIC-IDS-09` · **Alias (код/backlog):** `EPIC-IDS-EID` · **Статус:** 🟡 In Progress (EID-01/03/04/05 Done)
> **Layer:** Functional — identity / eID orchestration
> **Зависит от:** EPIC-IDS-04 (SOA Service Factory) · EPIC-IDS-05 (Supabase repos) · EPIC-IDS-07 STORY-IDS-AUTHCORE-01 (`ProfileRepository`, `/me`) — Done
> **Блокирует:** STORY-IDS-EID-02 (real providers, backlog) · STORY-IDS-OAUTH-02 (gateway introspection needs `eid_verified`)

---

## 1. Назначение

Рабочий eID-флоу на mock-провайдере: **`POST /auth/eid/start`** создаёт сессию и redirect; **`/auth/mock/callback`** завершает верификацию, пишет профиль (`eid_verified`, `verified_person_hash`) и аудит. Инфраструктура (порт, registry, сессии, HMAC) готова — story STORY-IDS-EID-01 собирает оркестрацию.

Парадигма: [`04-security §Часть A`](../../../runtime-docs/04-security.md), [`06-eid-providers`](../../../runtime-docs/06-eid-providers.md), [`05-data-model`](../../../runtime-docs/05-data-model.md).

## 2. Источники

- Backlog intake: [`STORY-IDS-EID-01-eid-verification-flow`](../../backlog-stories/eid/STORY-IDS-EID-01-eid-verification-flow.md)
- Analysis: [`identity-todo-backlog-2026-06-04`](../../../analysis/identity-todo-backlog-2026-06-04.md) — A2, A3, C9, C10
- Runtime: [`01-api`](../../../runtime-docs/01-api.md), [`04-security`](../../../runtime-docs/04-security.md), [`06-eid-providers`](../../../runtime-docs/06-eid-providers.md)

## 3. Вне scope эпика (Story 1 wave)

- Реальные провайдеры eideasy/authentigate — STORY-IDS-EID-02 (backlog).
- OAuth-сервер — отдельный эпик `EPIC-IDS-OAUTH` (backlog).

## 4. Предусловия

- EPIC-IDS-04: `ProfileRepository`, `get_current_user`, `ApiDependencies` ([`dependencies.py`](../../../src/core/api/dependencies.py)).
- EPIC-IDS-05: Supabase persistence для profiles/sessions/audit.
- EPIC-IDS-07 AUTHCORE-01: `/me` отдаёт `eid_verified` — Done.
- EPIC-IDS-06: offline pytest + `_block_dotenv_leakage` ([`tests/conftest.py`](../../../tests/conftest.py)).

## 5. Целевые файлы (Story 1)

```
src/core/api/handlers.py
src/core/api/asgi_app.py
tests/test_eid_verification_flow.py
tests/test_asgi_transport.py
```

## 6. Stories

### Story 1: STORY-IDS-EID-01 — eID-флоу: старт, callback, orchestration — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-EID-01-eid-verification-flow/STORY-IDS-EID-01-eid-verification-flow.md`](./stories/STORY-IDS-EID-01-eid-verification-flow/STORY-IDS-EID-01-eid-verification-flow.md)
- **Source (backlog):** [`backlog-stories/STORY-IDS-EID-01-eid-verification-flow.md`](../../backlog-stories/eid/STORY-IDS-EID-01-eid-verification-flow.md)

**Acceptance Criteria:**
- [x] `POST /auth/eid/start` (валидный JWT) → создаёт сессию `started`, отдаёт redirect к провайдеру.
- [x] callback с валидным `state` → профиль становится `eid_verified=true`, заполнены `verified_person_hash`/`eid_verified_at`.
- [x] Повторный callback / просроченная сессия → корректная обработка (не перезаписывает терминальный статус).
- [x] Конфликт `verified_person_hash` (тот же человек, другой аккаунт) → ошибка `ProfileConflictError`/409.
- [x] Каждое событие пишется в `eid_audit_events` без PII.
- [x] Полный флоу проходит на `mock` офлайн-тестом.

### Story 3: STORY-IDS-EID-03 — Plugin-платформа провайдеров: дескрипторы, DI-контекст, реестр-guard — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md`](./stories/STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md)
- **Source (backlog):** [`backlog-stories/STORY-IDS-EID-03-provider-plugin-backbone.md`](../../backlog-stories/eid/STORY-IDS-EID-03-provider-plugin-backbone.md)
- **Decision Ref:** [`authentigate-compatibility-audit-2026-06-07`](../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F5, F9, F13-guard)

**Acceptance Criteria:**
- [x] Есть `EIDProviderDescriptor` и `ProviderRuntime`; `mock` собирается через дескриптор.
- [x] Реестр строится из набора дескрипторов; добавление провайдера не требует правок тела `providers.py`/`registry.py` (только +дескриптор).
- [x] `EID_PROVIDER=<незарегистрированный>` → `ProviderNotRegisteredError`/`ConfigError` с перечислением доступных, **не** голый `KeyError`; глобальный handler отдаёт чистый ответ.
- [x] В mock/in-memory режиме сетевые клиенты провайдеров не создаются.
- [x] Offline-набор зелёный; тест на guard и на сборку реестра.

### Story 4: STORY-IDS-EID-04 — Provider-owned configuration: конфиг и валидация на стороне провайдера — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-EID-04-provider-owned-config/STORY-IDS-EID-04-provider-owned-config.md`](./stories/STORY-IDS-EID-04-provider-owned-config/STORY-IDS-EID-04-provider-owned-config.md)
- **Source (backlog):** [`backlog-stories/STORY-IDS-EID-04-provider-owned-config.md`](../../backlog-stories/eid/STORY-IDS-EID-04-provider-owned-config.md)
- **Decision Ref:** [`authentigate-compatibility-audit-2026-06-07`](../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F3, F4, F10)

**Acceptance Criteria:**
- [x] Authentigate-поля объявлены в `AuthentigateSettings`/`config_spec`, не в теле `load_config_from_env`.
- [x] `EID_PROVIDER=authentigate` без обязательных `AUTHENTIGATE_*` → понятная `ConfigError` (имя недостающего поля), fail-fast на старте.
- [x] Добавление нового провайдера не требует правок провайдер-логики в `schema.py`.
- [x] `scopes` по умолчанию — полные claim-URL; значение подтверждается в demo ([SPIKE-IDS-EID-09](../../backlog-stories/SPIKE-IDS-EID-09-authentigate-demo-access.md)).
- [x] `.env.example` отражает актуальные Authentigate-настройки; offline-набор зелёный, тест на отсутствующее required-поле.

### Story 5: STORY-IDS-EID-05 — Канон контракта provider→core: таксономия ошибок и идентичность субъекта — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-EID-05-canonical-provider-contract/STORY-IDS-EID-05-canonical-provider-contract.md`](./stories/STORY-IDS-EID-05-canonical-provider-contract/STORY-IDS-EID-05-canonical-provider-contract.md)
- **Source (backlog):** [`backlog-stories/STORY-IDS-EID-05-canonical-provider-contract.md`](../../backlog-stories/eid/STORY-IDS-EID-05-canonical-provider-contract.md)
- **Decision Ref:** [`authentigate-compatibility-audit-2026-06-07`](../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F2, F12)

**Acceptance Criteria:**
- [x] Есть `EidErrorCode`; `EIDProviderError` несёт канонический код.
- [x] Оркестратор различает `EIDProviderError` (сохраняет код в `failure_reason`/исход) и неожиданный `Exception` (`UNKNOWN`); `user_cancel` отличим в audit.
- [x] `subject_hash` в контракте не содержит имени провайдера; правило задокументировано; один человек через разные провайдеры даёт одинаковый `verified_person_hash` (юнит-тест на дедупликацию).
- [x] Добавление провайдера не добавляет новых кодов ошибок в ядро.
- [x] Offline-набор зелёный; тесты на маппинг ошибок и кросс-провайдерную дедупликацию.

### Story 7: STORY-IDS-EID-07 — Provider-agnostic OIDC-тулкит: discovery, JWKS, ID-token validation — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-EID-07-oidc-toolkit/STORY-IDS-EID-07-oidc-toolkit.md`](./stories/STORY-IDS-EID-07-oidc-toolkit/STORY-IDS-EID-07-oidc-toolkit.md)
- **Source (backlog):** [`backlog-stories/STORY-IDS-EID-07-oidc-toolkit.md`](../../backlog-stories/eid/STORY-IDS-EID-07-oidc-toolkit.md)
- **Decision Ref:** [`authentigate-compatibility-audit-2026-06-07`](../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F8)

**Acceptance Criteria:**
- [x] Модуль `core/security/oidc/` содержит `OidcDiscoveryClient`, `JwksCache`, `IdTokenValidator`, не зависящие от конкретного провайдера.
- [x] Discovery и JWKS кэшируются; неизвестный `kid` инициирует обновление JWKS.
- [x] `IdTokenValidator` проверяет подпись RS256 + `iss/aud/exp/iat/nonce`; невалидный токен → доменная ошибка валидации (мапится в `IDENTITY_VALIDATION_FAILED`, см. [EID-05](./stories/STORY-IDS-EID-05-canonical-provider-contract/STORY-IDS-EID-05-canonical-provider-contract.md)).
- [x] Тулкит доступен провайдерам через `ProviderRuntime`.
- [x] Тесты с замоканными discovery/JWKS/подписью; offline-набор зелёный (без сети).

### Story 8: STORY-IDS-EID-08 — Защита session-секретов (SessionSecretBox) для PKCE code_verifier — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-EID-08-session-secret-box/STORY-IDS-EID-08-session-secret-box.md`](./stories/STORY-IDS-EID-08-session-secret-box/STORY-IDS-EID-08-session-secret-box.md)
- **Source (backlog):** [`backlog-stories/STORY-IDS-EID-08-session-secret-box.md`](../../backlog-stories/eid/STORY-IDS-EID-08-session-secret-box.md)
- **Decision Ref:** [`authentigate-compatibility-audit-2026-06-07`](../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F7)

**Acceptance Criteria:**
- [x] Есть `SessionSecretBox` (порт + Fernet-реализация); `seal`/`open` обратимы; round-trip-тест.
- [x] `EID_SESSION_ENC_KEY` обязателен в `pilot` (понятная `ConfigError` при отсутствии), допустим дефолт в `demo`.
- [x] `secret_box` доступен провайдерам через `ProviderRuntime`.
- [x] Ключ шифрования отделён от `eid_secret` (разные назначения).
- [x] Offline-набор зелёный.

## 7. Верификация эпика (Story 1)

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
```

Ожидается новый offline e2e из task t05 (`tests/test_eid_verification_flow.py`).
