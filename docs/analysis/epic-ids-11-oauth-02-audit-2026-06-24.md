# Жёсткий аудит исполнения STORY-IDS-OAUTH-02 (introspection + сервисный токен)

> **Дата:** 2026-06-24
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-OAUTH-02-introspection-and-service-token`](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md) vs фактический код. Исполнена под **EPIC-IDS-11-oauth-server** (pkg-000030), 6 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): Текущая волна pkg-000030, OAUTH-02 🟢 (стр.11,57,594-599).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Introspection-endpoint | `POST /oauth/introspect` ([asgi_app.py:407-416](../../src/core/api/asgi_app.py)), gated `Depends(require_service_token)` |
| Handler | `handle_oauth_introspect` ([`core/oauth/introspection.py`](../../src/core/oauth/introspection.py)) — RFC 7662-style (always 200) |
| Ответ active | `{active:true, sub, phone_verified}` ([introspection.py:28-32](../../src/core/oauth/introspection.py)) |
| Ответ inactive | пустой/просрочен/битый → `{active:false}` ([introspection.py:17-22](../../src/core/oauth/introspection.py)) |
| `phone_verified` из профиля | `profile_repository.get_by_supabase_user_id(claims.sub).phone_verified` ([introspection.py:23-27](../../src/core/oauth/introspection.py)) — **не из токена** |
| Сервисный токен (конфиг) | `service_api_token` в `AppConfig` ([schema.py:70,238](../../src/core/config/schema.py)) из `SERVICE_API_TOKEN` |
| Сервисный гейт | `require_service_token` → `ServiceTokenAuth.require` ([security.py:108-116,144](../../src/core/api/security.py)); поддержка `Authorization: Bearer` и `X-Service-Token` |
| Тесты | [test_oauth_introspection.py](../../tests/test_oauth_introspection.py) — 7 |
| **Offline-сюита** | **350 passed, 11 deselected** ✅ (совпадает с индексом) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-11, pkg-000030) | Факт | Статус |
|--------------------------------|------|--------|
| t01 service api token config | `service_api_token` в `AppConfig` ([schema.py:70,238](../../src/core/config/schema.py)) | 🟢 |
| t02 service token auth dependency | `ServiceTokenAuth` + `require_service_token` ([security.py:89-116,144](../../src/core/api/security.py)), DI `ServiceTokenAuth.from_secret` ([providers.py:103](../../src/core/infrastructure/providers.py)) | 🟢 |
| t03 oauth introspection handler | `handle_oauth_introspect` (active/inactive, phone_verified из профиля) | 🟢 |
| t04 oauth introspect route | `POST /oauth/introspect` + service-gate | 🟢 |
| t05 offline introspection tests | 7 тестов | 🟢 |
| t06 story acceptance verification | AC 4/4 (см. §2) | 🟢 |
| **STORY-IDS-OAUTH-02** | introspection + сервисный токен | **🟢 Done** |

Индекс держит эпик корректно: `EPIC-IDS-11 … 🟡 In Progress — OAUTH-01 🟢; OAUTH-02 🟢` ([bullrun-launch-index.md:106](../tasks/bullrun-launch-index.md)); pkg-000030 Done, 350 offline (стр.11).

---

## 2. Сверка Acceptance Criteria story (по коду + тестам)

| AC | Факт (код + тест) | Вердикт |
|----|-------------------|---------|
| introspection валид → `{active:true, sub, phone_verified}`; просрочен/битый → `{active:false}` | [introspection.py:17-32](../../src/core/oauth/introspection.py); тесты `..._valid_token_returns_active...`, `..._invalid_user_token_returns_inactive`, `..._expired_user_token_returns_inactive` | ✅ |
| Без валидного сервисного токена → 401/403 (даже с валидным пользовательским) | `require_service_token`→`ServiceTokenAuth.require`→`UnauthorizedError`→**401** ([security.py:114-116](../../src/core/api/security.py), exception_handler [asgi_app.py:216-226](../../src/core/api/asgi_app.py)); тесты `..._missing_service_token_returns_401`, `..._invalid_service_token_returns_401` | ✅ |
| `phone_verified` из профиля, не из тела токена | `get_by_supabase_user_id(claims.sub).phone_verified` ([introspection.py:24-27](../../src/core/oauth/introspection.py)); тест `test_introspect_phone_verified_from_profile_not_jwt` | ✅ |
| Тесты offline + зафиксирован контракт для gateway | 7 тестов; контракт `{active, sub, phone_verified}` совпадает с [`09-gateway-expectations`](../runtime-docs/09-gateway-expectations.md) | ✅ |

**Вывод:** все 4 AC выполнены и покрыты тестами (7). Контракт introspection (`{active, sub, phone_verified}`) точно соответствует целевой модели 04-security/09 (phone, не eID). Поддержка `X-Service-Token` — бонус (тест `..._accepts_x_service_token_header`).

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F4** | **MEDIUM** | Security (info-disclosure) | `SERVICE_API_TOKEN` **не** в pilot-fail-fast ([schema.py pilot_required](../../src/core/config/schema.py) — отсутствует), а `ServiceTokenAuth.from_secret("")` → `disabled()` → `require()` = **no-op** ([security.py:108-110](../../src/core/api/security.py)). Значит при незаданном `SERVICE_API_TOKEN` (вкл. **pilot**) `/oauth/introspect` **открыт** — любой может узнать `{active, sub, phone_verified}` по токену без сервисного гейта (раскрытие `sub`+статуса верификации). AC2 выполнен только **когда токен задан**. **Как закрыть:** добавить `SERVICE_API_TOKEN` в pilot fail-fast (как `OAUTH_ACCESS_TOKEN_SECRET`/`GPT_OAUTH_CLIENT_SECRET`) либо default-deny для `/oauth/introspect`. | [schema.py](../../src/core/config/schema.py), [security.py:108-116](../../src/core/api/security.py) |
| **F1** | MEDIUM | Doc-stale | Backlog-story `Status: ⚪ Todo` (стр.6) + AC `[ ]` (стр.31-34) + «Точки в коде»: «`/oauth/introspect` — **отсутствует**» (стр.25), «`SERVICE_API_TOKEN` — **нет** в `AppConfig`» (стр.27) — реально 🟢 Done под pkg-000030, оба построены. **Как закрыть:** Status ⚪→🟢, AC `[ ]`→`[x]`, обновить «Точки в коде» (`introspection.py`, `require_service_token`, `service_api_token` в schema). Рекуррентный паттерн. | [`STORY-IDS-OAUTH-02...md:6,25-34`](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md) |
| **F2** | MEDIUM | Doc-stale (пакет-индекс) | [`EPIC-IDS-OAUTH.md`](../tasks/backlog-stories/oauth/EPIC-IDS-OAUTH.md): состав OAUTH-02 = ⚪ Todo (стр.18); статус-строка «OAUTH-02..04 — ⚪ Todo (introspection … не построены)» (стр.22). Реально OAUTH-02 🟢. **Как закрыть:** OAUTH-02 → 🟢 в составе/статус-строке. | [`oauth/EPIC-IDS-OAUTH.md`](../tasks/backlog-stories/oauth/EPIC-IDS-OAUTH.md) |
| **F3** | MEDIUM | Cross-doc consistency (свежий drift) | После билда OAUTH-02 устарели: [`09-gateway-expectations`](../runtime-docs/09-gateway-expectations.md) таблица «`/oauth/introspect` — отсутствует (OAUTH-02)» + «Проверка сервисного токена … нет `SERVICE_API_TOKEN` ❌» (стр.32,34) + Итог «нет introspection-endpoint, нет проверки сервисного токена» (стр.47); [`04-security §A`](../runtime-docs/04-security.md) таблица «introspection-endpoint ❌ отсутствует (OAUTH-02)» + «Проверка сервисного токена ❌» + as-is врезка «introspection-endpoint отсутствует». **Как закрыть:** заменить на «✅ построен (OAUTH-02)»; снять «нет проверки сервисного токена». | runtime-docs 04/09 |

Иных материальных findings нет. Наблюдения (severity none, по scope, **не gap**):
- Introspection отдаёт **только `phone_verified`** (без `eid_verified`) — соответствует phone-pivot и scope story (eID DEFERRED).
- RFC 7662-семантика (всегда 200, inactive→`{active:false}`) — корректно, не утечка (не отличает «не существует» от «истёк»).
- `claims.sub` = `supabase_user_id` (из `issue_authorization_code`), профиль резолвится по нему — консистентно.

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **350 passed, 11 deselected** (было 341 → +9; introspection-тесты), совпадает с индексом |
| Новый модуль `core/oauth/introspection.py` | аддитивный; OAUTH-01-флоу не затронут |
| `security.py` | +`ServiceTokenAuth`/`require_service_token`; `get_current_user` (Supabase/OAuth) без изменений |
| `AppConfig` | +`service_api_token` (дефолт `""`) — существующие config-тесты зелёные |
| OAuth-01/phone/eID | не затронуты — сюита зелёная |

Регрессий не выявлено.

---

## 5. Итог

- **STORY-IDS-OAUTH-02 — 🟢 исполнена полно:** `POST /oauth/introspect` (RFC 7662-style, `{active, sub, phone_verified}`, `phone_verified` из профиля), сервисный гейт `require_service_token` (`SERVICE_API_TOKEN`, Bearer/X-Service-Token), `{active:false}` на битый/просроченный. AC 4/4, 7 тестов.
- **Findings:** **F4 (MEDIUM, security)** — `SERVICE_API_TOKEN` не в pilot-fail-fast → introspect открыт в проде при незаданном токене (утечка `sub`+статуса); **F1 (MEDIUM)** — backlog-story doc-stale (⚪→🟢); **F2 (MEDIUM)** — пакет-индекс OAUTH-02 ⚪; **F3 (MEDIUM)** — `04-security`/`09` ещё пишут «introspection/service-token отсутствует» (свежий drift после билда).
- Наблюдения (только phone_verified; RFC7662 always-200; sub-резолв) — по scope, не gaps.

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; 6 тасков + story сверены по коду (pipeline t01–t06 🟢, индекс корректен).
- [x] AC 4/4 сверены по коду **и** тестам (active/inactive/expired/phone-from-profile/missing-service-token/invalid-service-token).
- [x] **Security-проверка** (analysis.mdc §middleware/auth flows): `SERVICE_API_TOKEN` не enforced в pilot → F4 (info-disclosure), подтверждено `ServiceTokenAuth.disabled` no-op + отсутствие в pilot_required.
- [x] Регрессий нет; 341→350 (+9) объяснён; индекс 350 = факт.
- [x] Свежий doc-drift «introspection отсутствует» (F3) пойман по 04/09 после билда.
