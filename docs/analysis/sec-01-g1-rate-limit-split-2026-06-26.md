# SEC-01 / G-1: разделение rate-limit — что закрыто, что вынесено в follow-up

> **Дата:** 2026-06-26  
> **Методология:** [analysis.mdc](../../../.cursor/rules/analysis.mdc) — claims только с `file:line` или проверенным grep.  
> **Источник решения:** P1 materialize + P3 Execute `pkg-000035` ([`run-summary-20260626-epic-ids-12-sec-01-pkg-000035.md`](../tasks/run-reports/run-summary-20260626-epic-ids-12-sec-01-pkg-000035.md)).  
> **Аудит-якорь:** [identity-backend-full-audit-2026-06-24.md](./identity-backend-full-audit-2026-06-24.md) **G-1** (HIGH).

---

## 1. Зачем этот документ

В плане materialize/execute **STORY-IDS-SEC-01** оператор явно разделил волну:

- **В pkg-000035 (сделано):** HTTP rate-limit на `POST /auth/eid/start` и `GET /auth/{provider}/callback`.
- **В отдельную follow-up стори (не сделано):** HTTP rate-limit на `POST /auth/phone/request`.

Backlog [STORY-IDS-SEC-01](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md) по-прежнему перечисляет `phone/request` в Scope — это **исходное требование аудита**, но **не весь Scope закрыт одной волной**. Этот файл фиксирует остаток G-1 и требования к отдельной стори, чтобы при P1 materialize follow-up не было двусмысленности.

---

## 2. Для какого сервиса

| Зона | Сервис | Роль |
|------|--------|------|
| **Реализация** | `doge-identity-service` | Единственный владелец `/auth/*`, envelope 429, OTP-cooldown |
| **Потребители** | `spa-app` (UI verify), Custom GPT → OAuth | Вызывают `POST /auth/phone/request` с Bearer JWT; должны различать 400 cooldown vs 429 window-limit |
| **Вне scope** | `doge-complaints-gateway` | Роуты `/stories`, `/gpt/...` из spec 16 — gateway-only ([SEC-01 backlog «Вне scope»](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md)) |

---

## 3. As-is после pkg-000035 (проверено в коде)

### 3.1 Закрыто — сквозной HTTP rate-limit

| Роут | Лимит (default) | Scope | Код |
|------|-----------------|-------|-----|
| `POST /auth/eid/start` | 5 req / 600 s | per `user:{sub}` | [`rate_limit_config.py:21-30`](../../src/core/security/rate_limit_config.py), [`asgi_app.py:283-299`](../../src/core/api/asgi_app.py) `Depends(require_eid_start_rate_limit)` |
| `GET /auth/{provider}/callback` | 5 req / 600 s | per `ip:{addr}` | [`rate_limit_config.py:32-36`](../../src/core/security/rate_limit_config.py), [`asgi_app.py:301-342`](../../src/core/api/asgi_app.py) `Depends(require_callback_rate_limit)` |

Превышение → HTTP **429**, `error.code=rate_limit_exceeded`, `error.retry_after` (сек), опционально заголовок `Retry-After` — [`envelope.py`](../../src/core/api/envelope.py), [`asgi_app.py`](../../src/core/api/asgi_app.py) handler `RateLimitExceeded`.

Конфиг env: `RATE_LIMIT_EID_START_*`, `RATE_LIMIT_CALLBACK_*` — [`schema.py`](../../src/core/config/schema.py).

Тесты: [`tests/test_rate_limiting.py`](../../tests/test_rate_limiting.py) (369 offline suite green после волны).

### 3.2 Не закрыто — `POST /auth/phone/request`

Роут **без** `Depends(require_*_rate_limit)` — [`asgi_app.py:344-358`](../../src/core/api/asgi_app.py).

Единственная защита от повтора SMS:

- OTP **resend-cooldown** в handler — [`handlers.py:456-473`](../../src/core/api/handlers.py)
- Доменный код `SmsErrorCode.RATE_LIMITED` → HTTP **400** (не 429) — [`handlers.py:96-99`](../../src/core/api/handlers.py) `_sms_error_http_status`
- Default окно cooldown: `PHONE_RESEND_COOLDOWN_S=60` — [`schema.py:237`](../../src/core/config/schema.py)

Это уже задокументировано в as-built spec 19 §G-3 residual — [`19-phone-verification-flow.md:225`](../../requirements/19-phone-verification-flow.md).

---

## 4. Операторское решение: почему phone/request — отдельная стори

**Проблема:** два разных анти-абьюз-механизма на одном роуте нельзя смешивать без явной политики.

| Механизм | Семантика | HTTP | Когда срабатывает |
|----------|-----------|------|-------------------|
| **OTP resend-cooldown** (есть) | «Не шли второй SMS, пока не истекла пауза после предыдущей сессии» | **400** `RATE_LIMITED` | Активная phone-сессия моложе `phone_resend_cooldown_s` |
| **HTTP per-user window limit** (follow-up) | «Не больше N запросов `/auth/phone/request` за окно W на пользователя» | **429** `rate_limit_exceeded` + `retry_after` | Счётчик сквозного слоя **до** handler |

**Решение pkg-000035:** не wire HTTP limit на `phone/request` в первой волне, чтобы:

1. Не дублировать cooldown тем же окном (риск двух 429/400 на один сценарий).
2. Сначала стабилизировать инфраструктуру (`InMemoryRateLimiter`, dependency, envelope) на eid/callback.
3. В follow-up **явно** согласовать числа: лимит окна vs `PHONE_RESEND_COOLDOWN_S` (backlog SEC-01 Scope §строка 16).

Pipeline note (verbatim intent): [`STORY-IDS-SEC-01-rate-limiting.md` §«Волна pkg-000035»](../tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01-rate-limiting/STORY-IDS-SEC-01-rate-limiting.md).

---

## 5. Follow-up стори (требования к materialize)

**Предлагаемый ключ:** `STORY-IDS-SEC-01b-phone-request-http-rate-limit`  
**Эпик:** [`EPIC-IDS-SEC`](../tasks/backlog-stories/security-hardening/EPIC-IDS-SEC.md) / pipeline [`EPIC-IDS-12`](../tasks/epics/EPIC-IDS-12-security-hardening/EPIC-IDS-12-security-hardening.md)  
**Зависит от:** SEC-01 🟢 (инфраструктура rate-limit уже в коде)  
**Backlog-файл:** [`STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md)

### Scope (что должно стать истинным)

1. **Wire** `POST /auth/phone/request` на существующий слой [`rate_limit_dependency.py`](../../src/core/api/rate_limit_dependency.py) — новый route key + env defaults (значение **зафиксировать**; spec 16 не задаёт явную цифру для phone/request — только eid/start и callback).
2. **Политика сосуществования** с cooldown (обязательно в AC):
   - Cooldown остаётся доменным **400** `RATE_LIMITED` внутри handler.
   - HTTP **429** только от сквозного слоя (например, попытки **сменить номер** или burst до истечения cooldown другой сессии).
   - Документировать порядок: `Depends(rate_limit)` → `handle_phone_request` → cooldown check.
3. **Конфиг:** `RATE_LIMIT_PHONE_REQUEST_REQUESTS` / `RATE_LIMIT_PHONE_REQUEST_WINDOW_S` (или эквивалент) в [`schema.py`](../../src/core/config/schema.py) + запись в [`19-phone-verification-flow.md`](../../requirements/19-phone-verification-flow.md).
4. **Тесты:** N+1 в окне → 429 + `retry_after`; regression: cooldown по-прежнему 400 без `retry_after` в envelope — расширить [`test_rate_limiting.py`](../../tests/test_rate_limiting.py).

### Вне scope follow-up

- Замена cooldown на 429 (меняет контракт PV-05 / spec 19).
- Redis-backed store (как и в SEC-01 — MVP in-memory).
- Gateway-only лимиты из spec 16.

### Критерий закрытия G-1 полностью

G-1 в аудите считается **частично закрытым** после pkg-000035 (eid + callback). **Полное** закрытие G-1 — после follow-up на `phone/request` **или** явный операторский DEFERRED на этот роут в spec 16/19 (альтернатива SEC-01 AC #6).

---

## 6. Связанные артефакты

| Артефакт | Статус |
|----------|--------|
| Pipeline SEC-01 | 🟢 Done ([`pkg-000035`](../tasks/identity-active-packages/pkg-000035-20260626-epic-ids-12-sec-01-rate-limiting.yaml)) |
| Backlog SEC-01 | Scope шире волны; статус backlog-файла обновить при синхронизации |
| [`GAP-CLOSURE-INDEX.md`](../tasks/backlog-stories/GAP-CLOSURE-INDEX.md) | G-1 → partial + ссылка сюда |
| [`04-security.md`](../runtime-docs/04-security.md) §8 | as-built SEC-01; phone follow-up — одна строка «не wire» |

---

## 7. Рекомендуемый next для оператора

1. **P1 materialize** `STORY-IDS-SEC-01b` (новый pkg, 3–4 tasks: config+wire, policy doc, tests, gate).
2. Либо **DEFERRED** с обоснованием в spec 19 (если cooldown + Telnyx 429 достаточно для pilot).
3. Не смешивать с **SEC-02** (IP/UA hashing) — разные гэпы; SEC-02 может переиспользовать request context из rate-limit слоя.

---

## 8. Регрессии (на дату документа)

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
# 369 passed (post pkg-000035)
```
