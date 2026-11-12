# Жёсткий аудит исполнения STORY-IDS-SEC-01b (HTTP rate-limit на `POST /auth/phone/request`)

> **Дата:** 2026-06-26
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity. Не предлагаю реализацию — только findings.
> **Предмет:** [`STORY-IDS-SEC-01b-phone-request-http-rate-limit`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md) vs фактический код. Исполнена под **EPIC-IDS-12** (pkg-000036), 6 tasks.
> **Контекст:** остаток G-1 после SEC-01 (eid/start+callback). Источник: [`sec-01-g1-rate-limit-split-2026-06-26.md`](./sec-01-g1-rate-limit-split-2026-06-26.md).
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): Текущая волна pkg-000036, SEC-01b 🟢 (стр.11,69,123,671-676).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Route key | `ROUTE_AUTH_PHONE_REQUEST = "POST /auth/phone/request"` + правило ([rate_limit_config.py:23,38-40](../../src/core/security/rate_limit_config.py)) |
| Конфиг (2 env) | `rate_limit_phone_request_requests/window_s` ([schema.py:75-76,251-252](../../src/core/config/schema.py)), env `RATE_LIMIT_PHONE_REQUEST_*` default 5/600 |
| Dependency (per-user) | `require_phone_request_rate_limit` → key `user:{supabase_user_id}` ([rate_limit_dependency.py:61-68](../../src/core/api/rate_limit_dependency.py)) |
| Wiring | `Depends(require_phone_request_rate_limit)` на `POST /auth/phone/request` ([asgi_app.py:346-349](../../src/core/api/asgi_app.py)) — **до** `handle_phone_request` |
| Порядок vs cooldown | dependency (429) → handler → cooldown (400) — FastAPI резолвит Depends до тела |
| 429-конверт | переиспользует `RateLimitExceeded`→429+`Retry-After`+`build_rate_limit_envelope` (SEC-01 инфраструктура) |
| Тесты | [test_rate_limiting.py:105](../../tests/test_rate_limiting.py) (429 window) + [test_phone_verification_flow.py:120](../../tests/test_phone_verification_flow.py) (cooldown-сценарий) |
| **Offline-сюита** | **371 passed, 11 deselected** ✅ (совпадает с индексом) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-12, pkg-000036) | Факт | Статус |
|--------------------------------|------|--------|
| t01 phone request rate limit config schema | 2 env-поля + дефолты ([schema.py:75-76,251-252](../../src/core/config/schema.py)) | 🟢 |
| t02 phone request rate limit dependency | `require_phone_request_rate_limit` per-user ([rate_limit_dependency.py:61-68](../../src/core/api/rate_limit_dependency.py)) | 🟢 |
| t03 phone request route wiring | `Depends(...)` на роуте ([asgi_app.py:349](../../src/core/api/asgi_app.py)) | 🟢 |
| t04 cooldown http window coexistence policy | задокументировано (spec19:225, 04-security §8) | 🟢 |
| t05 offline phone request rate limit tests | 429-тест + cooldown-тест | 🟢 |
| t06 story acceptance verification | AC 4/4 (см. §2) | 🟢 |
| **STORY-IDS-SEC-01b** | HTTP rate-limit phone/request | **🟢 Done** |

**Индекс корректен:** `EPIC-IDS-12 … SEC-01 🟢; SEC-01b 🟢; SEC-02/03 ⚪ backlog` ([bullrun-launch-index.md:123](../tasks/bullrun-launch-index.md)); pkg-000036 Done, 371 offline (стр.11).

> **G-1 — теперь полностью закрыт:** три чувствительных роута под HTTP rate-limit — `/auth/eid/start` (user), `/auth/{provider}/callback` (ip), `/auth/phone/request` (user). Остаток G-1 из [full-audit §3](./identity-backend-full-audit-2026-06-24.md) исчерпан (SEC-01 + SEC-01b).

---

## 2. Сверка Acceptance Criteria (по коду + тестам)

| AC | Факт | Вердикт |
|----|------|---------|
| `phone/request` wired на HTTP rate-limit (per-user); лимит/окно в конфиге | `require_phone_request_rate_limit` key `user:{sub}` ([rate_limit_dependency.py:61-68](../../src/core/api/rate_limit_dependency.py)); `RATE_LIMIT_PHONE_REQUEST_*` 5/600 | ✅ |
| Превышение окна → 429 + `retry_after`; cooldown по-прежнему 400 | тест `..._returns_429_with_retry_after` ([test_rate_limiting.py:105-126](../../tests/test_rate_limiting.py)): 3-й запрос (лимит=2) → 429, `retry_after≥1`, `code=rate_limit_exceeded`; cooldown→400 не затронут | ✅ |
| Политика сосуществования задокументирована (analysis + runtime-docs/spec 19) | [spec 19:225](../requirements/19-phone-verification-flow.md) + [04-security §8:128](../runtime-docs/04-security.md) «Два слоя на phone/request: 429 dependency vs 400 cooldown; порядок Depends→handler→cooldown» | ✅ |
| Offline-тест демонстрирует оба сценария (429 vs 400) | 429 — `test_phone_request_rate_limit_returns_429_with_retry_after`; cooldown-400 — `test_phone_request_rate_limited_before_cooldown` ([test_phone_verification_flow.py:120](../../tests/test_phone_verification_flow.py)) | ✅ |

**Вывод:** все 4 AC выполнены кодом+тестами+доками. Цитируемый в spec19:235 тест `test_phone_request_rate_limited_before_cooldown` **реально существует** (не фантом). Слой переиспользует инфраструктуру SEC-01 (тот же `InMemoryRateLimiter`/envelope/exception-handler) — без дублирования.

---

## 3. Findings (severity + как закрыть; без реализации)

Код SEC-01b — без материальных дефектов. Findings — **doc-staleness** (рекуррентный паттерн: код 🟢, индексы/чекбоксы отстают).

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F1** | MEDIUM | Doc-stale (внутр. противоречие) | Story `Status: 🟢 Done` (стр.6), но **все 4 AC = `[ ]`** (стр.31-34) — при том что все выполнены кодом+тестами. **Как закрыть:** проставить AC `[x]`. | [`STORY-IDS-SEC-01b...md:31-34`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md) |
| **F2** | MEDIUM | Doc-stale (пакет-индекс) | [`EPIC-IDS-SEC.md:24`](../tasks/backlog-stories/security-hardening/EPIC-IDS-SEC.md) состав SEC-01b = **⚪ Todo** — по факту 🟢 (pkg-000036); bullrun-эпик-строка уже 🟢. **Как закрыть:** SEC-01b → 🟢 Done в составе. | [`EPIC-IDS-SEC.md:24`](../tasks/backlog-stories/security-hardening/EPIC-IDS-SEC.md) |
| **F3** | LOW | Doc-stale (мини-индекс) | [`GAP-CLOSURE-INDEX.md`](../tasks/backlog-stories/GAP-CLOSURE-INDEX.md) держит SEC-01b ⚪ Todo и в «приоритете» как next; G-1 помечен Partial. Теперь G-1 **полностью закрыт** (3 роута). **Как закрыть:** SEC-01b → 🟢; G-1 → fully closed; снять из «next». | [`GAP-CLOSURE-INDEX.md`](../tasks/backlog-stories/GAP-CLOSURE-INDEX.md) |

Наблюдения (severity none, по scope, **не gaps**):
- **O1:** `/auth/phone/confirm` — без HTTP rate-limit (намеренно вне волны, [spec19:225](../requirements/19-phone-verification-flow.md)); защищён доменным лимитом попыток OTP (`PHONE_MAX_ATTEMPTS`). Не gap SEC-01b.
- **O2:** per-user скоуп корректен — роут требует Bearer JWT ([asgi_app.py:347](../../src/core/api/asgi_app.py) `Depends(get_current_user)`), анонимно недостижим; ключ `user:{sub}`.
- **O3 (наследие SEC-01):** `InMemoryRateLimiter` per-process (мультиреплика слабее) — pilot-допущение, Redis вне scope.

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **371 passed, 11 deselected** (было 370 → **+1**: `test_phone_request_rate_limit_returns_429_with_retry_after`) |
| Изменения | `ROUTE_AUTH_PHONE_REQUEST` + 2 env-поля + `require_phone_request_rate_limit` + 1 Depends — аддитивно поверх SEC-01 |
| Существующий phone-флоу (PV-05) | cooldown-семантика (400) сохранена — тест `..._rate_limited_before_cooldown` зелёный |
| SEC-01 (eid/start, callback) | не затронуты |

Регрессий не выявлено.

---

## 5. Итог

- **SEC-01b — 🟢 исполнена полно:** `POST /auth/phone/request` под per-user HTTP rate-limit (5/600, `RATE_LIMIT_PHONE_REQUEST_*`), 429+`retry_after`, cooldown остаётся 400; порядок Depends→handler→cooldown; политика задокументирована (spec19+04-security). AC 4/4, 2 теста (429 + cooldown). Таски t01–t06 🟢; bullrun-индекс корректен.
- **G-1 полностью закрыт** (SEC-01 eid/start+callback + SEC-01b phone/request).
- **Findings — только doc-staleness:** **F1** (story AC `[ ]` при Status 🟢), **F2** (EPIC-IDS-SEC состав SEC-01b ⚪), **F3** (GAP-CLOSURE SEC-01b ⚪ + G-1 Partial). Наблюдения O1–O3 — вне AC.
- **Регрессий нет** (371 passed).

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; 6 тасков + story + 4 AC сверены по коду, тестам и докам.
- [x] Проверена цепочка dependency→handler→cooldown (порядок и скоупы user/ip).
- [x] Цитируемый spec19 тест проверен на существование (не фантом) — `test_phone_verification_flow.py:120`.
- [x] Регрессий нет; 370→371 (+1) объяснён; индекс 371 = факт.
- [x] G-1-завершённость зафиксирована; doc-drift (F1/F2/F3) отделён от кода (дефектов нет).
