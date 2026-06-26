# Жёсткий аудит исполнения STORY-IDS-SEC-01 (rate-limiting, G-1)

> **Дата:** 2026-06-26
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity. Не предлагаю реализацию — только findings.
> **Предмет:** [`STORY-IDS-SEC-01-rate-limiting`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md) vs фактический код. Исполнена под **EPIC-IDS-12** (pkg-000035), 7 tasks.
> **Доп. вход:** [`sec-01-g1-rate-limit-split-2026-06-26.md`](./sec-01-g1-rate-limit-split-2026-06-26.md) (операторский split G-1).
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): Текущая волна pkg-000035, SEC-01 🟢 (стр.11,64,117,645-651).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Лимитер | [`InMemoryRateLimiter`](../../src/core/security/rate_limit.py) — sliding-window, `check(key, rule)`; `RateLimitExceeded(retry_after_s)` |
| Правила/скоупы | [`rate_limit_config.py:21-37`](../../src/core/security/rate_limit_config.py) — `ROUTE_AUTH_EID_START` (per `user`), `ROUTE_AUTH_CALLBACK` (per `ip`) |
| Конфиг (4 env) | [`schema.py:70-73,243-246`](../../src/core/config/schema.py) — `RATE_LIMIT_EID_START_*`, `RATE_LIMIT_CALLBACK_*` (default 5/600) |
| Dependency-слой | [`rate_limit_dependency.py`](../../src/core/api/rate_limit_dependency.py) — `require_eid_start_rate_limit` (key `user:{sub}`), `require_callback_rate_limit` (key `ip:{addr}`) |
| Wiring роутов | `/auth/eid/start` `Depends(require_eid_start_rate_limit)` ([asgi_app.py:304](../../src/core/api/asgi_app.py)); `/auth/{provider}/callback` `Depends(require_callback_rate_limit)` ([asgi_app.py:323](../../src/core/api/asgi_app.py)) |
| 429-контракт | exception_handler `RateLimitExceeded` → 429 + `Retry-After` header + `build_rate_limit_envelope` ([asgi_app.py:221-230](../../src/core/api/asgi_app.py)); конверт `{code:"rate_limit_exceeded", retry_after}` ([envelope.py:23-31](../../src/core/api/envelope.py)) |
| OTP-cooldown отделён | доменный `SmsErrorCode.RATE_LIMITED`→400, **не** 429; коммент-инвариант [handlers.py:458-459](../../src/core/api/handlers.py) |
| Тесты | [test_rate_limiting.py](../../tests/test_rate_limiting.py) — 3 |
| **Offline-сюита** | **369 passed, 11 deselected** ✅ (совпадает с индексом) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 Partial · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-12, pkg-000035) | Факт | Статус |
|--------------------------------|------|--------|
| t01 rate limit config schema | 4 env-поля + дефолты ([schema.py:70-73,243-246](../../src/core/config/schema.py)) | 🟢 |
| t02 in-memory rate limiter store | `InMemoryRateLimiter` sliding-window ([rate_limit.py:22-40](../../src/core/security/rate_limit.py)) | 🟢 |
| t03 rate limit dependency 429 envelope | `RateLimitExceeded`→429+`Retry-After`+envelope ([asgi_app.py:221-230](../../src/core/api/asgi_app.py)) | 🟢 |
| t04 sensitive routes wiring | eid/start (user) + callback (ip) подключены | 🟢 |
| t05 otp cooldown coexistence policy | cooldown=400 vs HTTP=429 разведены ([handlers.py:458-459](../../src/core/api/handlers.py)) | 🟢 |
| t06 offline rate limit tests | 3 теста (429 eid/start, 429 callback-ip, 400 cooldown) | 🟢 |
| t07 story acceptance verification | AC делив. волны 🟢 (см. §2) | 🟢 |
| **STORY-IDS-SEC-01** | rate-limiting волна pkg-000035 (eid/start + callback) | **🟢 Done (волна); G-1 — 🟡 Partial** |

**Индекс корректен:** `EPIC-IDS-12 … 🟡 In Progress — SEC-01 🟢; SEC-02/03 ⚪ backlog` ([bullrun-launch-index.md:117](../tasks/bullrun-launch-index.md)); pkg-000035 Done, 369 offline (стр.11). **EPIC-IDS-SEC** (backlog-индекс) тоже корректен: SEC-01 «🟢 Done (pkg-000035; phone/request → SEC-01b)» ([EPIC-IDS-SEC.md:23](../tasks/backlog-stories/security-hardening/EPIC-IDS-SEC.md)).

---

## 2. Сверка Acceptance Criteria SEC-01 (по коду + тестам)

| AC (из backlog-story) | Факт | Вердикт |
|-----------------------|------|---------|
| Перечень sensitive-роутов + лимит (eid/start = 5/10мин/user) | `ROUTE_AUTH_EID_START` per user, default 5/600 ([rate_limit_config.py:27-31](../../src/core/security/rate_limit_config.py)) | ✅ для eid/start+callback; ⚠️ **phone/request — не в этой волне** (→ SEC-01b) |
| 429 + `retry_after` в конверте | `{code:"rate_limit_exceeded", retry_after}` 429 ([envelope.py:23-31](../../src/core/api/envelope.py)); тест `..._returns_429_with_retry_after` | ✅ |
| Лимит до бизнес-логики (сквозной слой) | `Depends(require_*_rate_limit)` до хендлера ([asgi_app.py:304,323](../../src/core/api/asgi_app.py)) | ✅ |
| Непротиворечивое сосуществование с OTP-cooldown | cooldown→400 доменный, HTTP→429; коммент + тест `..._cooldown_still_domain_400_not_http_429` | ✅ |
| Конфиг + тест 429+retry_after | 4 env-поля; 3 теста | ✅ |
| (Альт. DEFERRED) | n/a — построено, не deferred | — |

**Вывод:** волна pkg-000035 — все доставленные AC ✅ (eid/start per-user, callback per-ip, 429-конверт, cooldown-разведение, тесты). **G-1 закрыт частично:** `POST /auth/phone/request` сознательно вынесен в **SEC-01b** (см. split-analysis §4). Backlog-story SEC-01 в Scope всё ещё перечисляет phone/request как свой пункт — это исходное требование, но не доставлено этой волной (F1).

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F1** | MEDIUM | Doc-stale (backlog-story) | SEC-01 story `Status: ⚪ Todo` (стр.6) + AC все `[ ]` (стр.34-39) + «Точки в коде: **Rate-limiter отсутствует во всём `src/core/`**» (стр.29) — по факту построено (pkg-000035 🟢, 7 tasks). Scope (стр.16) перечисляет `phone/request` без пометки о выносе в SEC-01b. EPIC-индекс уже 🟢 — расходится **только** story-файл. **Как закрыть:** Status → 🟢 Done (волна) + остаток G-1 → SEC-01b; AC `[x]` для доставленного (eid/start+callback), пункт phone/request пометить «вынесен в SEC-01b»; «Точки в коде» → as-built (`rate_limit*.py`, dependency, wiring). Рекуррентный паттерн. | [`STORY-IDS-SEC-01...md:6,16,29,34-39`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md) |
| **F2** | **MEDIUM** | Security (anti-abuse evasion) | Per-IP лимит на `/auth/{provider}/callback` берёт IP из **`X-Forwarded-For` (первое значение)** ([rate_limit_dependency.py:14-20](../../src/core/api/rate_limit_dependency.py)) без allowlist доверенных прокси. `XFF` задаётся клиентом → атакующий ротацией `X-Forwarded-For` **обходит** per-IP окно (ключ `ip:{spoofable}`). Для стори, чья суть — анти-абьюз, это ослабляет именно callback-защиту. **Как закрыть:** доверять `XFF` только от сконфигурированных прокси (брать правый-недоверенный hop) ИЛИ зафиксировать deployment-допущение «единственный доверенный reverse-proxy выставляет XFF» в 04-security/спеке + тест на spoof. | [rate_limit_dependency.py:14-20](../../src/core/api/rate_limit_dependency.py) |

Наблюдения (severity none/LOW, **не gaps волны** — вне AC):
- **O1 (LOW, deployment):** `InMemoryRateLimiter` — per-process ([rate_limit.py:23](../../src/core/security/rate_limit.py) docstring «in-process; demo path»). При нескольких репликах окно считается на каждый инстанс отдельно → суммарный лимит слабее. Выбор стора (Redis) — вне scope SEC-01 (как и in-memory у OAuth). Зафиксировать как pilot-допущение.
- **O2 (none):** eid/start per-`user` (есть JWT), callback per-`ip` (юзера ещё нет) — корректный выбор скоупа.
- **O3 (none):** OTP-cooldown остаётся 400 (доменная ошибка PV-флоу) — намеренно, чтобы не смешивать с 429; задокументировано в split-analysis §4 и spec 19.

---

## 4. SEC-01b (follow-up G-1) — статус задачи «создать стори»

**Стори УЖЕ существует и соответствует общему стандарту — дубликат не создаю** (analysis.mdc: «NO duplication»):
- Файл [`STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md) — есть; формат полный (Meta/Зачем/Scope/Вне scope/Точки в коде/AC/Якорь), code-grounded (`asgi_app.py:344-358`, `handlers.py:456-473`, `rate_limit_dependency.py`), Источник = split-analysis. ⚪ Todo.
- Зарегистрирована в индексе пакета: [`EPIC-IDS-SEC.md:24`](../tasks/backlog-stories/security-hardening/EPIC-IDS-SEC.md) (⚪ Todo, зависит от SEC-01) и в мини-индексе [`GAP-CLOSURE-INDEX.md`](../tasks/backlog-stories/GAP-CLOSURE-INDEX.md).
- Содержание совпадает с требованиями split-analysis §5 (wire phone/request на готовый слой; политика cooldown-400 vs 429; env-конфиг; тесты N+1).

**Вердикт:** задача «сделать стори на основе analysis» уже выполнена ранее; SEC-01b готова к P1 materialize. Действий по созданию не требуется. Мелкое наблюдение: в split-analysis ключ предложен `RATE_LIMIT_PHONE_REQUEST_*` — финальное значение лимита там сознательно не зафиксировано (spec 16 цифры для phone/request не даёт) → это решается на materialize, не дефект стори.

---

## 5. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **369 passed, 11 deselected** (совпадает с индексом; было 366 до SEC-01 → +3 rate-limit теста) |
| Новые модули `security/rate_limit*.py`, `api/rate_limit_dependency.py` | аддитивны; eid/phone/oauth-флоу не сломаны |
| `asgi_app` | +exception_handler + 2 Depends; happy-path роутов сохранён |
| OTP-cooldown (PV-05) | без изменений поведения (400) — тест зелёный |

Регрессий не выявлено.

---

## 6. Итог

- **SEC-01 — 🟢 исполнена (волна pkg-000035):** сквозной HTTP rate-limit (eid/start per-user 5/600, callback per-ip 5/600), 429+`Retry-After`+envelope `rate_limit_exceeded`/`retry_after`, OTP-cooldown отделён (400). AC доставленной волны 5/5, 3 теста. Таски t01–t07 🟢; индекс корректен.
- **G-1 — 🟡 Partial:** `phone/request` вынесен в **SEC-01b** (уже заведена, стандарт-конформна, в индексе — дубликат не требуется).
- **Findings:** **F1 (MEDIUM)** — backlog-story SEC-01 стейл (⚪/AC `[ ]`/«rate-limiter отсутствует» + Scope без split-пометки); **F2 (MEDIUM, security)** — per-IP callback-лимит доверяет спуфабельному `X-Forwarded-For` → обход. Наблюдения O1 (per-process стор), O3 (cooldown 400) — вне AC.
- **Регрессий нет** (369 passed).

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; 7 тасков + story + AC сверены по коду и тестам.
- [x] Проверена middleware/auth-цепочка (dependency до хендлера; IP/user-ключи) — выявлен F2 (XFF-spoof).
- [x] G-1 split распознан: волна 🟢 vs остаток (phone/request) 🟡 → SEC-01b; дубликат не создан (стори уже есть и в индексе).
- [x] Регрессий нет; 366→369 (+3) объяснён; индекс 369 = факт.
- [x] Doc-stale (F1) отделён от security-gap (F2) и от deployment-наблюдений (O1).
