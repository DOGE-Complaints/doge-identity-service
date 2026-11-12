# Audit: совместимость Authentigate Integration Guide ↔ архитектура DOGEstonia

> **Что это.** Аудит совместимости предложенного решения из
> [`Authentigate Integration guide.md`](../tech-requirements/Authentigate%20Integration%20guide.md)
> с фактической архитектурой `doge-identity-service` под
> [STORY-IDS-EID-02](../tasks/backlog-stories/eid-deferred/STORY-IDS-EID-02-real-eid-providers.md).
> **Решение по продукту:** Authentigate выбран как primary MVP eID-провайдер (eID Easy дорогой).
> **База контекста:** [eid-provider-integration-needs-2026-06-07.md](eid-provider-integration-needs-2026-06-07.md).
> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — каждое утверждение гайда о «нашем коде» сверено с реальным кодом.
> **Дата:** 2026-06-07. **Статус кода:** боевые провайдеры не написаны, зарегистрирован только `mock`.

---

## 0. Вердикт (кратко)

Гайд **архитектурно совместим** с нашим provider-контрактом: он корректно учитывает синхронность,
`handle_callback(raw_params)→EIDVerificationResult`, отсутствие update в session store, double-HMAC `subject_hash`,
переиспользование существующих `authentigate_*` полей. Это сильная сторона — автор сверялся с фактическим кодом.

Но есть **один блокер браузерного флоу** (callback возвращает JSON, а не 302-redirect) и **набор gap'ов**,
без которых решение не заработает end-to-end. Сводка:

| # | Находка | Severity | Тип |
|---|---------|----------|-----|
| F1 | Callback возвращает JSON-конверт, а не HTTP-redirect в SPA | 🔴 HIGH | Архитектурный разрыв браузерного флоу |
| F2 | Таксономия ошибок (§20) не доходит до API: оркестратор схлопывает `Exception`→`provider_error` | 🔴 HIGH | Контракт ошибок |
| F3 | Новые env-поля (`DISCOVERY_URL`, `ACR_VALUES`, `UI_LOCALES`, `COUNTRY`) отсутствуют в `AppConfig` | 🟠 HIGH | Конфиг |
| F4 | Нет валидации обязательных `AUTHENTIGATE_*` при `EID_PROVIDER=authentigate` | 🟠 HIGH | Конфиг / AC story |
| F5 | EID-1 не закрыт: реестр без authentigate + голый `KeyError` | 🟠 HIGH | Реестр / AC story |
| F6 | Callback-роут `/auth/authentigate/callback` — заглушка | 🟠 HIGH | Проводка |
| F7 | Нет helper'а шифрования `code_verifier` и не определён источник ключа | 🟡 MEDIUM | Крипто |
| F8 | Нет инфраструктуры OIDC discovery + JWKS (RS256) | 🟡 MEDIUM | OIDC валидация |
| F9 | Фабрика инжектит провайдеру только store — нужен http_client/crypto/jwks | 🟡 MEDIUM | DI / фабрика |
| F10 | Расхождение формата `scope` (короткие имена vs полные claim-URL) | 🟡 MEDIUM | Конфиг / вендор |
| F11 | Frontend-предпосылка гайда — React Native, а у нас SPA-first | 🟡 MEDIUM | Док-рассинхрон |
| F12 | Кросс-провайдерная дедупликация: `subject_hash` с префиксом провайдера | 🟢 LOW | Дизайн |
| F13 | jti replay-cache и «active provider» guard не поддержаны | 🟢 LOW | Безопасность (defer) |
| F14 | Открытые вопросы к SK (attributes-ключ, client_secret_basic, ACR, цена) | ⚪ INFO | Вендор-блокеры |

---

## 1. Что совместимо (verified ✅)

Подтверждено реальным кодом — гайд НЕ требует переделки этих мест:

| Утверждение гайда | Подтверждение в коде |
|-------------------|----------------------|
| Провайдер синхронный, `handle_callback`→только `EIDVerificationResult` (§1, §34) | [`base.py:40-53`](../../src/core/providers/base.py#L40-L53) |
| Перечитать сессию по `state` внутри callback (§14, §19.2) | `store.get_by_state` есть: [`contracts.py:46`](../../src/core/domain/contracts.py#L46) |
| Всё для callback сохранить при `start_flow` (нет update) (§10.4, §17.2) | store без update: [`contracts.py:43-54`](../../src/core/domain/contracts.py#L43-L54) |
| `registry.get(provider_name)` по сегменту URL в callback (§15) | [`handlers.py:262`](../../src/core/api/handlers.py#L262) |
| `subject_hash = hash_secret(f"...:{code}", key=eid_secret)`, double-HMAC (§12.3) | сигнатура [`hashing.py:9`](../../src/core/security/hashing.py#L9); внешний HMAC [`handlers.py:283-286`](../../src/core/api/handlers.py#L283-L286) |
| Оркестратор валидирует `return_url` до провайдера (§17.1) | [`handlers.py:123-140`](../../src/core/api/handlers.py#L123-L140) |
| Существующие поля `authentigate_issuer/client_id/client_secret/redirect_uri/scopes` (§16) | [`schema.py:31-35`](../../src/core/config/schema.py#L31-L35) |
| `EIDStartResult(redirect_url, session_id, expires_at)` (§17) | [`base.py:17-21`](../../src/core/providers/base.py#L17-L21) |
| Зависимости `httpx`, `joserfc`, `cryptography` доступны | [`pyproject.toml`](../../pyproject.toml) |
| Поля сессии `state/nonce/code_verifier_encrypted/code_verifier_hash/provider_session_data` существуют (§17.2) | [`models.py:44-59`](../../src/core/domain/models.py#L44-L59) |

---

## 2. Находки (gaps / рассинхроны)

### 🔴 F1 — Callback отдаёт JSON, а браузерный OIDC требует redirect в SPA
**Гайд** (§19, §23.2): после аутентификации Authentigate делает **браузерный GET-redirect** на
`/auth/authentigate/callback?code=...&state=...`, далее «`/me` returns `eid_verified=true`, story submit succeeds».

**Реальность кода:** `handle_auth_eid_callback` возвращает JSON-конверт `{"status":"verified","return_url":...}`
([`handlers.py:327-330`](../../src/core/api/handlers.py#L327-L330)), а роут оборачивает его в `JSONResponse`
([`asgi_app.py:238-248`](../../src/core/api/asgi_app.py#L238-L248), `_json_envelope`). **HTTP 302 нет.**

**Impact:** для mock это ок (вызывается программно из тестов). Но при реальном Authentigate браузер пользователя
после логина попадёт на endpoint, который **показывает JSON**, а не возвращает человека в SPA на `return_url`.
Флоу end-to-end в браузере не замкнётся. Это **архитектурный разрыв уровня оркестратора** (EID-01), а не провайдера —
гайд его не покрывает, т.к. сфокусирован на adapter.

**Рекомендация:** решить контракт callback для браузерных провайдеров — `handle_auth_eid_callback` (или тонкая
обёртка в роуте) должен на успехе/ошибке отдавать `RedirectResponse(303)` на `session.return_url` с маркером
статуса (`?eid=verified` / `?eid_error=<code>`), сохранив JSON-вариант для mock/тестов. Зафиксировать в STORY-IDS-EID-02
или отдельной стори на оркестратор. **Без этого live-тест §23.2 не пройдёт.**

### 🔴 F2 — Таксономия ошибок (§20) не доходит до API
**Гайд** (§20, §22.4): провайдер бросает `EIDProviderError` с кодами (`AUTHENTIGATE_USER_CANCEL`,
`AUTHENTIGATE_INVALID_GRANT`, …), и негативные тесты ожидают эти коды.

**Реальность:** `EIDProviderError` определён ([`base.py:24-29`](../../src/core/providers/base.py#L24-L29)), но
**нигде не обрабатывается специально** (grep: только определение и реэкспорт). Оркестратор ловит широкий
`except Exception` и схлопывает всё в `failure_reason="provider_error"` + API-ошибку `eid_verification_failed`
([`handlers.py:263-281`](../../src/core/api/handlers.py#L263-L281)). Код ошибки и `user_cancel` теряются.

**Impact:** богатая таксономия §20 не видна ни в API-ответе, ни в audit. `user_cancel` неотличим от реального сбоя.
Негативные тесты §22.4, если писать их на уровне API, провалятся.

**Рекомендация:** (а) оркестратор должен `except EIDProviderError` отдельно — пробрасывать `exc.code` в
`build_error_envelope` и в audit `failure_reason`; (б) тесты §22.4 формулировать на уровне провайдера
(`pytest.raises(EIDProviderError, code=...)`), пока оркестратор не доработан. Выбрать (а) или (б) — решение для стори.

### 🟠 F3 — Новые env-поля отсутствуют в `AppConfig`
**Гайд** (§16) вводит `AUTHENTIGATE_DISCOVERY_URL`, `AUTHENTIGATE_ACR_VALUES`, `AUTHENTIGATE_UI_LOCALES`,
`AUTHENTIGATE_COUNTRY`. В [`schema.py:31-35`](../../src/core/config/schema.py#L31-L35) их **нет** (есть только
issuer/client_id/client_secret/redirect_uri/scopes).

**Рекомендация:** добавить поля в `AppConfig` + парсинг в `load_config_from_env`
([`schema.py:141-145`](../../src/core/config/schema.py#L141-L145)). Примечание: `DISCOVERY_URL` избыточен — его
можно детерминированно вывести как `{issuer}/.well-known/openid-configuration`; решить, держать ли отдельным полем.

### 🟠 F4 — Нет валидации обязательных `AUTHENTIGATE_*`
**Реальность:** валидатор требует `EIDEASY_CLIENT_ID/SECRET/REDIRECT_URI` при `eid_provider=eideasy`
([`schema.py:109-112`](../../src/core/config/schema.py#L109-L112)), но **аналога для authentigate нет**.

**Impact:** при `EID_PROVIDER=authentigate` без credentials провайдер упадёт уже в рантайме невнятно. AC story
требует **понятную** ошибку конфигурации.

**Рекомендация:** добавить блок: при `eid_provider=authentigate` требовать
`AUTHENTIGATE_CLIENT_ID/CLIENT_SECRET/REDIRECT_URI/ISSUER` (и/или `DISCOVERY_URL`).

### 🟠 F5 — EID-1 не закрыт (реестр + KeyError)
**Реальность:** фабрика регистрирует только `{"mock": ...}` ([`providers.py:92`](../../src/core/infrastructure/providers.py#L92)),
`registry.get` бросает голый `KeyError` ([`registry.py:11-14`](../../src/core/providers/registry.py#L11-L14)).
Гайд §15 предполагает регистрацию, но фикс EID-1 (понятная ошибка) — отдельный пункт AC.

**Рекомендация:** зарегистрировать `AuthentigateProvider`; заменить `KeyError` на доменную ошибку конфигурации
с понятным текстом (перечислить зарегистрированные провайдеры).

### 🟠 F6 — Callback-роут authentigate всё ещё заглушка
**Реальность:** `/auth/authentigate/callback` → `handle_public_stub(next_epic="EPIC-IDS-EID")`
([`asgi_app.py:214-236`](../../src/core/api/asgi_app.py#L214-L236)). Образец боевой проводки — mock-роут
([`asgi_app.py:238-248`](../../src/core/api/asgi_app.py#L238-L248)).

**Рекомендация:** переключить на `handle_auth_eid_callback(provider_name="authentigate", raw_params=..., trace_id=...)`
(с учётом F1 про redirect).

### 🟡 F7 — Нет helper'а шифрования `code_verifier`, источник ключа не определён
**Гайд** (§10.4, §14, §17.2) инжектит `crypto: CodeVerifierCrypto` и сохраняет `code_verifier_encrypted`/`code_verifier_hash`.
**Реальность:** в [`hashing.py`](../../src/core/security/hashing.py) только односторонний HMAC; symmetric encrypt/decrypt
helper'а нет. `cryptography>=42` доступна, но **ключ шифрования не определён** (`eid_secret` — это HMAC-ключ для `subject_hash`).

**Открытое решение (для следующего диалога/стори):**
- (a) отдельный Fernet-ключ через новый env (`DOGESTONIA_SESSION_ENC_KEY`), или
- (b) детерминированно вывести симметричный ключ из отдельного секрета, или
- (c) **MVP-упрощение:** хранить `code_verifier` в `provider_session_data` открытым (сессия серверная, БД-only,
  одноразовая, TTL≈10 мин) и отложить шифрование. `code_verifier_hash` определить как `SHA256(code_verifier)`.

### 🟡 F8 — Нет инфраструктуры OIDC discovery + JWKS (RS256)
**Реальность:** `joserfc` используется только для **HS256/симметричного** Supabase-JWT (`OctKey`,
[`supabase_validator.py:5,17,26`](../../src/core/auth/supabase_validator.py#L5)). ID-token Authentigate подписан
**RS256** и валидируется по JWKS из discovery (§11, §19.5). Кода discovery-fetch, JWKS KeySet и кэша **нет** —
всё greenfield (гайд §13: `oidc.py`, `JWKSCache`). `joserfc` это поддерживает (`KeySet`/`jwt.decode` с RSA), но
реализацию + кэш нужно написать; HTTP — через `httpx` с таймаутом `oidc_request_timeout_s`
([`schema.py:136`](../../src/core/config/schema.py#L136), уже есть).

### 🟡 F9 — Фабрика инжектит провайдеру только store
**Гайд** (§14) constructor: `config, session_store, http_client, clock, crypto, jwks_cache`.
**Реальность:** фабрика умеет только `MockEIDProvider(verification_session_store)`
([`providers.py:92`](../../src/core/infrastructure/providers.py#L92)).

**Рекомендация:** в `provide_service_factory` собрать `httpx.Client(timeout=oidc_request_timeout_s)` (синглтон на
приложение), crypto и jwks-cache, и инжектить в `AuthentigateProvider` **только когда `eid_provider=authentigate`**
(ленивая регистрация), чтобы mock-режим не тянул сетевые зависимости. Продумать lifecycle/закрытие `httpx.Client`.

### 🟡 F10 — Расхождение формата `scope`
**Реальность:** дефолт в [`schema.py:145`](../../src/core/config/schema.py#L145) и `.env.example` —
`"openid personal_code personal_code_country"` (короткие имена). **Гайд** §8/§16 требует полные claim-URL
`"openid https://id.authentigate.eu/claims/personal_code https://id.authentigate.eu/claims/personal_code_country"`.

**Impact:** неверный формат scope → `invalid_scope` от Authentigate. **Рекомендация:** привести дефолт к полным
URL (вероятно правильный вариант по докам SK) и **подтвердить в demo** точные scope/claim-имена.

### 🟡 F11 — Frontend-предпосылка: React Native vs SPA-first
**Гайд** (§18, §24) предписывает внешний user-agent через Expo AuthSession / ASWebAuthenticationSession /
Chrome Custom Tabs и «No embedded WebView». **Но** по решению проекта основной UI — `spa-app` (web),
**не React Native** (memory `project-identity-kickoff`).

**Разбор:** для web-SPA authorize-redirect — это обычная полностраничная навигация `window.location`, что само по себе
и есть «external user agent / no WebView», т.е. требование удовлетворяется естественно. Мобильная формулировка гайда
**не соответствует** SPA-first и вводит в заблуждение.

**Рекомендация:** в реализации/доке зафиксировать web-SPA вариант (full-page redirect → callback → 303 redirect назад,
см. F1); мобильные рекомендации применять только если/когда появится RN-клиент.

### 🟢 F12 — Кросс-провайдерная дедупликация
`subject_hash = hash_secret("authentigate:{country}:{code}")` (§12.3) содержит **префикс провайдера**, затем
оркестратор делает внешний HMAC. Значит один и тот же человек, верифицированный через другой провайдер (eideasy),
даст другой `verified_person_hash` → будет посчитан новой личностью. Для single-provider MVP приемлемо;
**задокументировать** ограничение на случай смены/добавления провайдера.

### 🟢 F13 — jti replay-cache и «active provider» guard
Гайд §19.5/§24 упоминает jti-uniqueness (опционально) — инфраструктуры нет; одноразовость сессии
(`mark_consumed`, [`handlers.py:316`](../../src/core/api/handlers.py#L316)) уже защищает от повторного использования
code в рамках сессии. Также `registry.get(route_segment)` в callback вернёт провайдера, даже если он не активен
(если зарегистрирован) — оркестратор частично страхует проверкой `session.provider==provider_name`
([`handlers.py:216`](../../src/core/api/handlers.py#L216)). Обе — LOW, можно отложить.

### ⚪ F14 — Открытые вопросы к SK (вендор-блокеры)
Из гайда §6.3, §19.6, §26 — подтвердить в demo **до хардкода**:
точный JSON-ключ `attributes.*` в id_token (возможная опечатка `attribues` в доках);
доступность `client_secret_basic` (иначе `private_key_jwt` + управление ключами);
разрешённые `acr_values` для нашего клиента; коммерческие условия Starter.

---

## 3. Перечень изменений в коде (change propagation)

Для реализации Authentigate по гайду затрагиваются (минимум):

| Файл | Изменение | Находка |
|------|-----------|---------|
| `src/core/providers/authentigate/` (новый пакет) | `provider.py`, `client.py`, `oidc.py`, `mapper.py`, `errors.py` | F7,F8 |
| [`src/core/config/schema.py`](../../src/core/config/schema.py) | +поля `AppConfig` (acr/ui_locales/country[/discovery]); +валидация required при `authentigate`; формат scope | F3,F4,F10 |
| [`src/core/infrastructure/providers.py`](../../src/core/infrastructure/providers.py) | регистрация провайдера + DI (httpx/crypto/jwks), ленивая | F5,F9 |
| [`src/core/providers/registry.py`](../../src/core/providers/registry.py) | guard: понятная ошибка вместо `KeyError` | F5 |
| [`src/core/api/asgi_app.py`](../../src/core/api/asgi_app.py) | роут callback: stub → боевой хендлер; redirect-обёртка | F6,F1 |
| [`src/core/api/handlers.py`](../../src/core/api/handlers.py) | `except EIDProviderError` (коды); 303-redirect для браузерного callback | F1,F2 |
| `src/core/security/` (новый helper) | шифрование/хеш `code_verifier` (если выбран путь a/b) | F7 |
| `.env.example`, `.env` | актуальные `AUTHENTIGATE_*` (issuer demo, scope-URL, acr) | F3,F10 |
| `tests/` | unit (start/callback/mapping/negative) + live-skip-тесты | §22-23 гайда, F2 |

---

## 4. Что нужно подтвердить до старта реализации

**Продуктовые/архитектурные решения (наши):**
1. Контракт браузерного callback: 303-redirect vs JSON (F1) — нужен для рабочего флоу.
2. Доводить ли коды ошибок до API сейчас или позже (F2).
3. Путь шифрования `code_verifier`: Fernet-ключ / derive / plaintext-MVP (F7).
4. `DISCOVERY_URL` отдельным полем или вывод из issuer (F3).

**Вендорные (к SK, demo):** F14 — attributes-ключ, client_secret_basic, allowed ACR, цена.

**Операционные:** публичный host для `redirect_uri` + Allowed IPs (локально — туннель); Smart-ID **Qualified** demo-аккаунты (Basic/NQ не работают, §21.3).

---

## 5. Итоговая оценка

Предложенное решение **пригодно как основа реализации**: автор гайда корректно лёг на наш provider-контракт и
не требует ломать абстракцию. Гайд закрывает уровень **adapter** (OIDC request/token/validation/mapping) — здесь
совместимость высокая.

**Главные риски — на уровне оркестратора и инфраструктуры, которые гайд не покрывает:**
F1 (callback должен редиректить, а не отдавать JSON) — **блокер браузерного флоу**; F2 (коды ошибок не доходят);
F7/F8 (крипто `code_verifier` и JWKS/discovery — greenfield). Плюс конфиг-гэпы F3-F5 и проводка F6 — обязательны
для AC story. F11 — поправить док под SPA-first.

Рекомендуемый порядок: сначала закрыть конфиг+реестр+роут (F3-F6), затем adapter (F7-F10), затем решить
оркестраторные F1/F2, в конце — live-тест на demo (F14, операционные).

---

---

# 6. Архитектурные решения по гэпам (design, не костыли)

> **Установка.** Все находки исправимы. Но устранять их надо **доработкой на уровне абстракции**, а не
> точечными `if`-заплатками, потому что провайдеров eID будет много и важна гибкость под разные стандарты
> (OAuth2, OIDC, завтра — eIDAS-node/SAML). Ниже по каждому гэпу: проблема (с код-ссылкой) → принцип →
> решение (новые абстракции) → почему масштабируемо (SOLID) → затронутые файлы → стори.
> **Сквозная идея:** превратить «один захардкоженный mock» в **plugin-платформу провайдеров** с тремя
> канонами на границе `provider ↔ core`: канонический **результат**, каноническая **таксономия ошибок**,
> каноническая **идентичность субъекта**. Всё провайдер-специфичное живёт в адаптере провайдера; ядро и SPA
> говорят на провайдер-агностичном языке.

## Сквозной целевой дизайн (карта абстракций)

```
core (провайдер-агностично)                     provider adapter (specifics)
─────────────────────────────                  ──────────────────────────────
EIDProviderPort (контракт)            ◄── implements ── AuthentigateProvider / EideasyProvider / Mock
EIDProviderDescriptor (name, config-spec, build) ◄── declares ── каждый провайдер
EIDProviderRegistry (resolve active, guard)
ProviderRuntime (DI-контекст: http, secret_box, oidc-toolkit, store, clock)
EidErrorCode (канон. таксономия)      ◄── maps to ── вендор-ошибки провайдера
EidCallbackOutcome (канон. результат) ◄── returns ── orchestrator
canonical subject identity (country, national_id) ◄── normalizes ── провайдер
─────────────────────────────
shared toolkits (reusable любым OIDC-провайдером):
  OidcDiscoveryClient · JwksCache · IdTokenValidator · SessionSecretBox
```

---

## F5 + F9 — Plugin-регистрация провайдеров и DI-контекст (backbone)

**Проблема.** Фабрика хардкодит `EIDProviderRegistry({"mock": MockEIDProvider(store)})`
([`providers.py:92`](../../src/core/infrastructure/providers.py#L92)); реестр бросает голый `KeyError`
([`registry.py:11-14`](../../src/core/providers/registry.py#L11-L14)). Каждый новый провайдер = правка тела
фабрики + ручная проводка зависимостей; невалидный `EID_PROVIDER` падает невнятно. Это нарушает **OCP**:
ядро меняется при каждом добавлении провайдера.

**Принцип.** Open-Closed + Dependency Inversion: добавление провайдера = добавление модуля, а не правка ядра.

**Решение.**
1. **`EIDProviderDescriptor`** (новый, в `providers/base.py` или `providers/descriptor.py`): декларативное
   описание провайдера — `name: str`, `config_spec` (см. F3/F4), `build(runtime: ProviderRuntime) -> EIDProviderPort`.
   Провайдер сам объявляет, как он собирается.
2. **`ProviderRuntime`** (новый, DI-bundle): общие синглтоны — `config`, `session_store`, `http_client: httpx.Client`,
   `secret_box: SessionSecretBox` (F7), `oidc: OidcToolkit` (F8), `clock`. Фабрика собирает их **один раз**.
3. **Реестр строит только активный провайдер + `mock`** (lazy): `build_registry(runtime)` берёт дескриптор
   активного `config.eid_provider`, вызывает его `build(runtime)`. Сетевые клиенты не создаются в mock/in-memory
   режиме (закрывает побочный риск F9).
4. **Guard вместо `KeyError`:** `registry.get(name)` при отсутствии бросает `ProviderNotRegisteredError`
   (подкласс `ConfigError` из [`schema.py:9`](../../src/core/config/schema.py#L9)) с текстом
   «EID_PROVIDER=x не зарегистрирован; доступны: …». Глобальный `ConfigError`-handler
   ([`asgi_app.py:141-145`](../../src/core/api/asgi_app.py#L141-L145)) уже отдаёт чистый ответ — переиспользуем.

**Почему масштабируемо.** Реестр строится из набора дескрипторов (`PROVIDER_DESCRIPTORS: tuple[...]`); новый
провайдер = +1 дескриптор, ядро (`providers.py`, `registry.py`) не трогается. SRP: дескриптор знает «как
собрать», runtime — «из чего», реестр — «какой активен». DIP: провайдер зависит от абстракций в `ProviderRuntime`.

**Затронутые файлы.** `providers/base.py` (+`EIDProviderDescriptor`), `providers/registry.py` (guard +
`build_registry`), `providers/runtime.py` (новый `ProviderRuntime`), `infrastructure/providers.py` (сборка
runtime + дескрипторов), `mock_provider.py` (обернуть в дескриптор). → **STORY-IDS-EID-03**.

---

## F3 + F4 + F10 — Provider-owned configuration

**Проблема.** `AppConfig` — плоский dataclass со всеми полями всех провайдеров
([`schema.py:31-52`](../../src/core/config/schema.py#L31-L52)); `load_config_from_env` содержит
провайдер-специфичные блоки валидации (`if eid_provider == "eideasy": ...`,
[`schema.py:109-112`](../../src/core/config/schema.py#L109-L112)), а для authentigate валидации нет.
Новых полей (`ACR_VALUES`/`UI_LOCALES`/`COUNTRY`) нет; формат `scope` зашит коротким
([`schema.py:145`](../../src/core/config/schema.py#L145)). Каждый провайдер раздувает центральную схему и
плодит `if`-цепочки — анти-паттерн «provider conditionals scattered in core».

**Принцип.** Single Responsibility + OCP: каждый провайдер владеет своим конфиг-контрактом.

**Решение.**
1. **`ProviderConfigSpec`** (часть дескриптора): провайдер декларирует свои env-поля — `required: tuple[str,...]`,
   `optional_defaults: dict[str,str]`, и `load(env) -> <ProviderSettings dataclass>`. Напр. `AuthentigateSettings`
   (issuer, client_id, client_secret, redirect_uri, scopes=полные claim-URL по умолчанию, acr_values, ui_locales,
   country) живёт в `providers/authentigate/config.py`.
2. **Центральная схема — только generic.** `load_config_from_env` оставляет `eid_provider` (+ членство) и общие
   поля; провайдер-специфичные блоки **удаляются** из schema.py. Валидацию required-полей делегируем активному
   дескриптору: на старте `descriptor.config_spec.validate(env)` → fail-fast `ConfigError` с понятным текстом
   (закрывает F4 и AC story про «понятную ошибку конфигурации»).
3. **Формат scope (F10)** становится умолчанием в `AuthentigateSettings` (полные claim-URL), а не в ядре;
   подтверждается в demo (F14).

**Почему масштабируемо.** Добавление провайдера не трогает `schema.py`. Удаляются `if provider==...` из ядра
(устранение анти-паттерна). Тесты конфигурации провайдера живут рядом с провайдером.

**Совместимость.** Существующие плоские `authentigate_*`/`eideasy_*` поля в `AppConfig` можно (а) оставить как
есть для обратной совместимости и читать из них, либо (б) мигрировать в nested settings. Рекомендация: ввести
nested `AuthentigateSettings`, а плоские eideasy-поля не трогать в этой стори (они не активны). Зафиксировать как
явное решение.

**Затронутые файлы.** `config/schema.py` (убрать провайдер-блоки, добавить delegation hook), новый
`providers/authentigate/config.py`, дескриптор (F5), `.env.example`/`.env`. → **STORY-IDS-EID-04**.

---

## F2 + F12 — Канон контракта provider→core (ошибки и идентичность)

**Проблема (F2).** `EIDProviderError` определён ([`base.py:24-29`](../../src/core/providers/base.py#L24-L29)), но
оркестратор ловит широкий `except Exception` и схлопывает всё в `provider_error`
([`handlers.py:263-281`](../../src/core/api/handlers.py#L263-L281)) — код ошибки и `user_cancel` теряются.
**Проблема (F12).** Гайд кладёт имя провайдера в `subject_hash` (`"authentigate:{country}:{code}"`, §12.3) →
один человек через разных провайдеров = разные `verified_person_hash` ([`handlers.py:283-286`](../../src/core/api/handlers.py#L283-L286)),
анти-Sybil ломается при смене/добавлении провайдера.

**Принцип.** Контракт на границе должен быть **каноническим и провайдер-агностичным** (Liskov: любой провайдер
взаимозаменяем); вендор-специфика мапится в канон в адаптере.

**Решение.**
1. **`EidErrorCode` (StrEnum, новый)** — каноническая таксономия: `USER_CANCELLED`, `STATE_MISMATCH`,
   `TOKEN_EXCHANGE_FAILED`, `IDENTITY_VALIDATION_FAILED`, `MISSING_REQUIRED_CLAIM`, `COUNTRY_NOT_ALLOWED`,
   `METHOD_NOT_ALLOWED`, `PROVIDER_UNAVAILABLE`, `UNKNOWN`. Провайдер мапит **свои** вендор-коды (§20 гайда —
   `AUTHENTIGATE_*`) в этот канон и бросает `EIDProviderError(code=EidErrorCode.X)`. Ядро и SPA знают только канон.
2. **Оркестратор различает ошибки:** `except EIDProviderError as e:` → `mark_failed(session.id, e.code)`, audit
   `failure_reason=e.code`, и прокидывает `e.code` в исход (F1). Отдельно `except Exception:` → `UNKNOWN`/
   internal (без утечки деталей). Это снимает «плоский provider_error».
3. **Каноническая идентичность (F12):** провайдер возвращает в `EIDVerificationResult` **нормализованный**
   стабильный идентификатор **без префикса провайдера**; `subject_hash = hash_secret(f"{country}:{national_id}", key=eid_secret)`.
   Имя провайдера фиксируется отдельно (`provider` уже хранится в профиле/сессии/аудите) как provenance, но **не
   входит в identity-хэш**. Тогда анти-Sybil работает кросс-провайдерно. Внешний HMAC оркестратора остаётся.

**Почему масштабируемо.** Новый провайдер не добавляет новых кодов ошибок в ядро и не ломает дедупликацию.
Контракт `provider→core` стабилен (OCP). Тесты §22.4 формулируются в канон-кодах, едины для всех провайдеров.

**Затронутые файлы.** `providers/base.py` (+`EidErrorCode`, доке контракта про нормализацию identity),
`api/handlers.py` (разбор `EIDProviderError`, формула subject_hash — уже агностична, меняется только вклад
провайдера), доке `runtime-docs/06`. → **STORY-IDS-EID-05**.

---

## F1 + F6(route) + F11 — Браузерный callback: redirect-рендеринг + динамический роут

**Проблема (F1).** `handle_auth_eid_callback` возвращает JSON-конверт
([`handlers.py:327-330`](../../src/core/api/handlers.py#L327-L330)), роут оборачивает в `JSONResponse`
([`asgi_app.py:238-248`](../../src/core/api/asgi_app.py#L238-L248)) — браузер после реального eID увидит JSON,
а не вернётся в SPA. **Проблема (F6).** Callback-роуты захардкожены по одному
([`asgi_app.py:214-248`](../../src/core/api/asgi_app.py#L214-L248)) — каждый провайдер = новый роут.
**Проблема (F11).** Доки навязывают React Native, хотя UI — SPA (web).

**Принцип.** Separation of Concerns: бизнес-исход (домен) ≠ его HTTP-представление (транспорт).

**Решение.**
1. **`EidCallbackOutcome` (новый dataclass)** — результат оркестрации: `outcome: Literal["verified",
   "already_verified","failed"]`, `return_url: str | None`, `error_code: EidErrorCode | None`,
   `json_status: int`. `handle_auth_eid_callback` возвращает его вместо `(dict,int)`.
2. **Рендер на уровне роута:** callback (браузерный endpoint OIDC по стандарту) **всегда** завершается
   `RedirectResponse(303)` на `session.return_url` с маркером: `?eid_status=verified` или
   `?eid_status=error&eid_error=<canonical-code>`. `return_url` уже прошёл allowlist на старте
   ([`validate_return_url`](../../src/core/security/return_url.py)) и хранится в сессии → редирект безопасен.
   Если сессия/return_url неизвестны (нельзя безопасно редиректить — риск open-redirect) → JSON/HTML 400.
   JSON-вариант сохраняется для mock/тестов (контролируемо, напр. `Accept: application/json`).
3. **Динамический роут (F6):** заменить три захардкоженных callback-роута на один параметризованный
   `GET /auth/{provider}/callback`; хендлер резолвит `provider` из пути, проверяет регистрацию в реестре
   (иначе `ConfigError`), делегирует в оркестратор. Новый провайдер — без правок роутинга (OCP).
4. **Док (F11):** зафиксировать web-SPA модель (full-page redirect → callback → 303 back). Мобильные
   рекомендации (AuthSession/Custom Tabs) — только при появлении RN-клиента (см. [[project-identity-kickoff]]).

**Почему масштабируемо.** Любой будущий провайдер переиспользует один redirect-рендер и один роут. Контракт
callback'а единый и стандарт-корректный (redirect_uri обязан редиректить).

**Затронутые файлы.** `api/handlers.py` (`EidCallbackOutcome`), `api/asgi_app.py` (параметризованный роут +
`RedirectResponse`), доке `runtime-docs/06`+`08-ui-expectations`. Зависит от F2 (коды для маркера).
→ **STORY-IDS-EID-06**.

---

## F8 — Provider-agnostic OIDC toolkit (discovery, JWKS, ID-token)

**Проблема.** `joserfc` используется только для симметричного HS256 (Supabase, `OctKey`,
[`supabase_validator.py:5,17,26`](../../src/core/auth/supabase_validator.py#L5)). Для RS256-подписанного
ID-token Authentigate нужны OIDC discovery + JWKS + валидация claims — кода нет.

**Принцип.** DIP + переиспользуемость: строить не «Authentigate-валидатор», а **общий OIDC-тулкит**, которым
воспользуется любой OIDC-провайдер (завтра — eIDAS-node, другой IdP).

**Решение.** Новый модуль `core/security/oidc/` (или `core/oidc/`):
- **`OidcDiscoveryClient`** — тянет и кэширует `.well-known/openid-configuration` (authorization/token endpoint,
  jwks_uri, issuer). HTTP через общий `httpx.Client` с таймаутом `oidc_request_timeout_s`
  ([`schema.py:136`](../../src/core/config/schema.py#L136), уже есть).
- **`JwksCache`** — кэш JWKS с TTL и refresh-on-unknown-kid (стандартная ротация ключей), отдаёт joserfc `KeySet`.
- **`IdTokenValidator`** — RS256-подпись через `KeySet` + `iss/aud/exp/iat/nonce` через `jwt.JWTClaimsRegistry`
  (паттерн уже применён в `supabase_validator.py:18-22` — переиспользуем подход).
- Собирается в `OidcToolkit` и кладётся в `ProviderRuntime` (F5/F9).

**Почему масштабируемо.** Любой OIDC-провайдер инжектит тулкит и не дублирует discovery/JWKS. SRP: три класса —
три ответственности. joserfc уже в зависимостях — поддерживает RSA/`KeySet`.

**Затронутые файлы.** новый `core/security/oidc/*`, `providers/runtime.py` (экспозиция), тесты с замоканным
discovery/JWKS. → **STORY-IDS-EID-07**.

---

## F7 — Защита session-секретов (SessionSecretBox) для PKCE code_verifier

**Проблема.** Helper'а симметричного шифрования нет (`CODE_VERIFIER_ENCRYPTION_KEY` удалён в CLEANUP-02,
[STORY-IDS-CLEANUP-02 E20](../tasks/backlog-stories/cleanup/STORY-IDS-CLEANUP-02-placeholders-hardening.md)).
Модель имеет `code_verifier_encrypted`/`code_verifier_hash` (nullable,
[`models.py:49-50`](../../src/core/domain/models.py#L49-L50)). `hash_secret` — односторонний
([`hashing.py:9`](../../src/core/security/hashing.py#L9)). `cryptography>=42` доступна.

**Принцип.** Инверсия зависимости от крипты + разделение ключей (encryption-key ≠ HMAC `eid_secret`).

**Решение.**
- **`SessionSecretBox` (порт, новый):** `seal(plaintext) -> str` / `open(token) -> str`. Реализация на Fernet
  (`cryptography`) с **выделенным** ключом `EID_SESSION_ENC_KEY` (новое env; fail-fast required в pilot —
  по образцу pilot-валидации [`schema.py:114-127`](../../src/core/config/schema.py#L114-L127)).
- Провайдер на `start_flow` пишет `code_verifier_encrypted = secret_box.seal(code_verifier)` и
  `code_verifier_hash = sha256(code_verifier)`; на callback — `secret_box.open(...)`.
- В demo/in-memory допускается дефолтный/эфемерный ключ; в pilot — обязателен.

**Альтернатива (зафиксировать решение владельца).** PKCE verifier — одноразовый серверный секрет (TTL≈10 мин,
БД-only). Для MVP допустимо хранить его открытым в `provider_session_data` и отложить шифрование. **Рекомендация:**
всё же ввести `SessionSecretBox` — это provider-agnostic примитив (пригодится для nonce и др.), abstracts крипту
для будущей ротации/KMS без правки провайдеров. Не переиспользовать `eid_secret` (разные назначения ключей).

**Почему масштабируемо.** Любой провайдер/секрет переиспользует box; смена реализации (KMS) не трогает провайдеров.

**Затронутые файлы.** новый `core/security/session_secret.py`, `config/schema.py` (+`EID_SESSION_ENC_KEY`),
`providers/runtime.py`. → **STORY-IDS-EID-08**.

---

## F13 — jti replay-cache и active-provider guard (LOW, осознанно отложить)

Сессия уже одноразовая (`mark_consumed`, [`handlers.py:316`](../../src/core/api/handlers.py#L316)) — повторное
использование `code` в рамках сессии исключено. `registry.get(route_segment)` после backbone (F5: регистрируется
только активный + mock) естественно ограничен; оркестратор дополнительно сверяет `session.provider==provider_name`
([`handlers.py:216`](../../src/core/api/handlers.py#L216)). **Решение:** jti-replay-cache **отложить** (вынести
в backlog как hardening), мелкий guard покрывается F5. В стори-группу не выношу отдельно — упомянуть в EID-05/EID-03
как «вне scope, defer».

---

## F14 — Демо-доступ Authentigate и подтверждение рантайма (SPIKE)

Не код — внешняя зависимость. Подтвердить в demo (до хардкода): точный JSON-ключ `attributes.*` (возможная
опечатка `attribues` в доках, §19.6), доступность `client_secret_basic`, разрешённые `acr_values` для клиента,
коммерческие условия. Операционка: публичный host для `redirect_uri` + Allowed IPs (локально — туннель),
Smart-ID **Qualified** demo-аккаунты (§21.3). → **SPIKE-IDS-EID-09** (prereq для capstone).

---

## Карта «гэп → стори»

| Гэп | Стори | Суть доработки |
|-----|-------|----------------|
| F5, F9, F13(guard) | **EID-03** Plugin-backbone | Descriptor + ProviderRuntime + lazy registry + ConfigError-guard |
| F3, F4, F10 | **EID-04** Provider-owned config | ProviderConfigSpec, delegated validation, nested AuthentigateSettings |
| F2, F12 | **EID-05** Канон контракта | EidErrorCode taxonomy + orchestrator error-mapping + canonical subject identity |
| F1, F6, F11 | **EID-06** Browser callback | EidCallbackOutcome + 303 redirect + параметризованный роут + doc SPA |
| F8 | **EID-07** OIDC toolkit | OidcDiscoveryClient + JwksCache + IdTokenValidator |
| F7 | **EID-08** SessionSecretBox | Порт + Fernet + EID_SESSION_ENC_KEY |
| F14 | **SPIKE-IDS-EID-09** | Demo-доступ + подтверждение рантайм-деталей |
| (capstone) | **EID-02** Authentigate provider | Сборка всего в `AuthentigateProvider` (рефреш scope) |

**Порядок:** EID-03 → (EID-04, EID-05, EID-07, EID-08 — независимы между собой) → EID-06 → EID-02 (capstone);
SPIKE-09 параллельно, но обязателен до live-теста EID-02.

---

## Anchors
- Гайд: [`Authentigate Integration guide.md`](../tech-requirements/Authentigate%20Integration%20guide.md)
- Контекст потребностей кода: [eid-provider-integration-needs-2026-06-07.md](eid-provider-integration-needs-2026-06-07.md)
- Story: [STORY-IDS-EID-02](../tasks/backlog-stories/eid-deferred/STORY-IDS-EID-02-real-eid-providers.md) + группа EID-03…09
- Парадигма: [runtime-docs/06-eid-providers.md](../runtime-docs/06-eid-providers.md)
- Requirements (частично устарели): [req-12](../requirements/12-authentigate-oidc-client.md), [req-17](../requirements/17-eid-provider-abstraction.md)
