# Интервью CPO × CTO — Спорные моменты параграфа 4 эпиков doge-identity-service

> **Дата:** 2026-05-27
> **Участники:** CPO (пользователь), CTO (AI-ассистент)
> **Предмет:** Параграф 4 («Где может быть слабое место») из `[epic-audit-fixes-explained-2026-05-26.md](./epic-audit-fixes-explained-2026-05-26.md)`
> **Методология:** `[analysis.mdc](../../.cursor/rules/analysis.mdc)` — каждое решение привязано к конкретному документу или эпику
> **Цель:** Зафиксировать архитектурные решения по 6 спорным точкам и сформировать точные инструкции по доработке эпиков

---

## Результаты в одну строку (TL;DR)


| #   | Точка                          | Решение                                                                                   |
| --- | ------------------------------ | ----------------------------------------------------------------------------------------- |
| 4.1 | CORS + lifespan                | Вариант B: `create_app(config)` фабричная функция                                         |
| 4.2 | Два имени для одного секрета   | Единое имя `DOGESTONIA_EID_SECRET`, убрать `EID_HASH_SECRET` и fallback                   |
| 4.3 | `hash_secret()` не определён   | Вынести в отдельный модуль `core/security/hashing.py`                                     |
| 4.4 | AC для «пустой секрет в pilot» | Добавить явный AC с тестом                                                                |
| 4.5 | Порядок проверок в конфиге     | Одна фраза: «`db_backend` проверяется первым»                                             |
| 4.6 | Один таймаут vs два            | Два отдельных: `REQUEST_TIMEOUT_S` (Supabase, 15s) + `OIDC_REQUEST_TIMEOUT_S` (OIDC, 10s) |


---

## Полная запись интервью

---

### Вопрос 4.1 — CORS и FastAPI lifespan

**CTO поставил вопрос:**

Сейчас в EPIC-IDS-02 Story 4 зафиксирован паттерн: `app.add_middleware(CORSMiddleware, ...)` вызывается внутри `_lifespan`. FastAPI официально не поддерживает регистрацию middleware после старта — `middleware_stack` собирается при первом запросе. На практике работает, но при мажорных обновлениях FastAPI/Starlette может сломаться. Было предложено три варианта:

- **A** — оставить как есть (lifespan, рискованно)
- **B** — `create_app(config: AppConfig) -> FastAPI`, конфиг загружается на module-level до создания `app`
- **C** — читать `CORS_ALLOWED_ORIGINS` из `os.environ` напрямую, минуя AppConfig (нарушает SOA)

**Ответ CPO:** Вариант B — фабричная функция.

---

### Вопрос 4.2 — Два имени для одного HMAC-секрета

**CTO поставил вопрос:**

Существуют два имени для одного секрета (ключа хеширования `personal_code` → `verified_person_hash`): `EID_HASH_SECRET` (новое) и `DOGESTONIA_EID_SECRET_PEPPER` (старое deprecated). Текущий ADR-IDS-008 оставил оба с fallback-логикой. Строка в req-07 двусмысленна — агент может неправильно реализовать проверку.

**Ответ CPO:** Унифицировать полностью. Оставить одно имя `DOGESTONIA_EID_SECRET`. Убрать `EID_HASH_SECRET`. Убрать fallback-логику. Нигде не должно быть двусмысленности.

> **Примечание:** Это ревизия ADR-IDS-008. `DOGESTONIA_EID_SECRET` — новое чистое имя (без суффикса `_PEPPER`). ADR-IDS-008 нужно обновить, отразив это решение.

---

### Вопрос 4.3 — `hash_secret()` не определён нигде в эпиках

**CTO поставил вопрос:**

В EPIC-IDS-04 Story 2 используется `client_secret_hash=hash_secret(config.gpt_oauth_client_secret)` — но функция `hash_secret` нигде не описана. Если агент-реализатор не создаст её сам, будет `NameError` в рантайме. Варианты: (A) описать прямо в Story 2, (B) вынести в отдельный модуль `core.security.hashing`, (C) отложить до req-14.

**Ответ CPO:** Вариант B — отдельный модуль `core/security/hashing.py`. Единая точка для всех хеш-операций сервиса.

---

### Вопрос 4.4 — AC для случая «оба секрета пустые в pilot»

**CTO поставил вопрос:**

Правило есть: если `eid_hash_secret` пустой в pilot — `ConfigError`. Но нет конкретного проверяемого Acceptance Criteria в EPIC-IDS-01 Story 2. Агент может пропустить это условие. Теперь, с учётом ответа 4.2 (одна переменная, без fallback), вопрос упрощается: одна переменная, пустая — ошибка.

**Ответ CPO:** Да, добавить явный AC с конкретным тестовым кейсом.

---

### Вопрос 4.5 — Порядок проверок в `load_config_from_env()`

**CTO поставил вопрос:**

Сейчас в EPIC-IDS-01 Story 2 порядок проверок конфига не описан. Риск: оператор задаёт `DB_BACKEND=sqlite` → сервер падает с ошибкой `Отсутствует SUPABASE_URL` (непонятная причина), хотя правильная ошибка — `Недопустимое значение DB_BACKEND: sqlite`. Варианты: (A) одна фраза «`db_backend` проверяется первым», (B) полный пронумерованный порядок.

**Ответ CPO:** Вариант A — достаточно одной фразы в эпике.

---

### Вопрос 4.6 — Область применения `REQUEST_TIMEOUT_S`

**CTO поставил вопрос:**

`REQUEST_TIMEOUT_S` сейчас описан как «таймаут к Supabase PostgREST», но identity-сервис делает исходящие HTTP-запросы и к Authentigate (OIDC discovery, JWKS), и к eID Easy (`/token`). Если таймаут только для Supabase — другие запросы уходят без таймаута (потенциальное зависание). req-12 уже упоминает `OIDC_REQUEST_TIMEOUT_S = 10.0` хардкодом.

**Ответ CPO:** Два отдельных таймаута: `REQUEST_TIMEOUT_S` (Supabase, default 15s) и `OIDC_REQUEST_TIMEOUT_S` (Authentigate/eID Easy, default 10s, уже есть в req-12 — вынести из хардкода в AppConfig).

---

## Комментарии к параграфу 4 — как именно доработать эпики

---

### 4.1 → EPIC-IDS-02 Story 4

**Что изменить:**

Текущий паттерн с `app.add_middleware(...)` внутри `_lifespan` заменить на фабричную функцию.

**Конкретная правка в Story 4:**

```python
# asgi_app.py — module-level
def create_app(config: AppConfig) -> FastAPI:
    """Создаёт и конфигурирует FastAPI-приложение."""
    app = FastAPI(lifespan=_lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_allowed_origins.split(","),
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["authorization", "content-type", "x-trace-id"],
    )
    _register_routes(app)
    return app

# module-level — выполняется один раз при импорте модуля
_config = provide_app_config()
app = create_app(_config)
```

`_lifespan` остаётся, но только для: `get_api_dependencies()` (warmup DI) + `configure_logging(...)`.

**Acceptance Criteria добавить:** `CORSMiddleware` зарегистрирован до первого запроса; `allow_origins` читается из `config.cors_allowed_origins`, не из `os.environ`.

**Файл:** `EPIC-IDS-02-fastapi-transport.md` → Story 4.

---

### 4.2 → EPIC-IDS-01, EPIC-IDS-06, req-07, ADR-IDS-008

**Что изменить:**

Единое имя переменной: `DOGESTONIA_EID_SECRET`. Убрать `EID_HASH_SECRET` везде. Убрать fallback-логику в loader'е.

**Конкретные правки:**

**EPIC-IDS-01 Story 2 — AppConfig:**

```python
# Было (после предыдущего фикса):
eid_hash_secret: str = ""  # primary: EID_HASH_SECRET, fallback: DOGESTONIA_EID_SECRET_PEPPER

# Стало:
eid_secret: str = ""  # читается из DOGESTONIA_EID_SECRET
```

**EPIC-IDS-01 Story 2 — loader:**

```python
# Было (fallback-цепочка):
eid_hash_secret = env.get("EID_HASH_SECRET") or env.get("DOGESTONIA_EID_SECRET_PEPPER") or ""

# Стало (одна строка):
eid_secret = env.get("DOGESTONIA_EID_SECRET", "")
```

**EPIC-IDS-06 conftest:**

```python
# Было (оба env var):
monkeypatch.setenv("EID_HASH_SECRET", "test-secret")
monkeypatch.setenv("DOGESTONIA_EID_SECRET_PEPPER", "test-secret")

# Стало (один):
monkeypatch.setenv("DOGESTONIA_EID_SECRET", "test-secret")
```

**req-07:** удалить строки `EID_HASH_SECRET` и `DOGESTONIA_EID_SECRET_PEPPER`, добавить `DOGESTONIA_EID_SECRET | Yes (pilot) | — | HMAC-SHA256 ключ для генерации verified_person_hash`.

**ADR-IDS-008:** обновить — зафиксировать что решение пересмотрено: вместо дуализма с fallback выбрано одно имя `DOGESTONIA_EID_SECRET`. Указать причину: простота, нет fallback-кода, нет двусмысленности.

**Файлы:** `EPIC-IDS-01`, `EPIC-IDS-06`, `docs/requirements/07-env-configuration-spec.md`, `docs/requirements/05-adr-log.md`.

---

### 4.3 → EPIC-IDS-04 Story 2 + новый модуль

**Что изменить:**

Добавить в EPIC-IDS-04 Story 2 явное описание нового модуля.

**Конкретная правка:**

В EPIC-IDS-04 Story 2 добавить секцию «Зависимость: `core/security/hashing.py`»:

```python
# src/core/security/hashing.py
import hashlib
import hmac

def hash_secret(plaintext: str, *, key: str) -> str:
    """HMAC-SHA256 хеш для хранения секретов (client_secret и т.п.)."""
    return hmac.new(
        key.encode("utf-8"),
        plaintext.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
```

В `InMemoryOAuthClientStore.from_config()` заменить:

```python
# Было:
client_secret_hash=hash_secret(config.gpt_oauth_client_secret or "demo")

# Стало (явный ключ):
from core.security.hashing import hash_secret
client_secret_hash=hash_secret(
    config.gpt_oauth_client_secret or "demo",
    key=config.oauth_access_token_secret or "demo-key",
)
```

Добавить в структуру `src/`:

```
src/
  core/
    security/
      __init__.py
      hashing.py     ← новый файл
```

**Файл:** `EPIC-IDS-04-soa-service-factory.md` → Story 2.

---

### 4.4 → EPIC-IDS-01 Story 2

**Что изменить:**

В Acceptance Criteria Story 2 добавить явный кейс с проверяемым поведением.

**Конкретный AC добавить:**

```
✓ load_config_from_env({"APP_PROFILE": "pilot", ..., "DOGESTONIA_EID_SECRET": ""})
  → raises ConfigError("DOGESTONIA_EID_SECRET обязателен в pilot-профиле")
```

Этот кейс дополняет уже существующие AC и гарантирует, что агент напишет тест, а не пропустит проверку.

**Файл:** `EPIC-IDS-01-scaffold-config-launch.md` → Story 2, раздел Acceptance Criteria.

---

### 4.5 → EPIC-IDS-01 Story 2

**Что изменить:**

В описании `load_config_from_env()` добавить одно предложение о порядке проверок.

**Конкретный текст добавить** (в начало блока описания функции):

> Порядок валидации: сначала проверяется `db_backend ∈ {"in_memory", "supabase"}` — до всех остальных полей. Это гарантирует что при неверном backend оператор видит конкретную ошибку, а не сбивающую с толку «не задан SUPABASE_URL».

**Файл:** `EPIC-IDS-01-scaffold-config-launch.md` → Story 2, описание `load_config_from_env`.

---

### 4.6 → EPIC-IDS-01 Story 2, EPIC-IDS-05 Story 6, req-07, req-12

**Что изменить:**

Разделить один таймаут на два; `OIDC_REQUEST_TIMEOUT_S` вынести из хардкода req-12 в AppConfig.

**Конкретные правки:**

**EPIC-IDS-01 Story 2 — AppConfig добавить поле:**

```python
# Было (только Supabase):
request_timeout_s: int = 15

# Стало (два поля):
request_timeout_s: int = 15      # Supabase PostgREST
oidc_request_timeout_s: int = 10 # Authentigate OIDC discovery, eID Easy /token
```

**req-07** — добавить строку:

```
OIDC_REQUEST_TIMEOUT_S | No | 10 | Таймаут запросов к OIDC-провайдерам (Authentigate, eID Easy)
```

**req-12** — заменить хардкод `OIDC_REQUEST_TIMEOUT_S = 10.0` на `config.oidc_request_timeout_s`.

**EPIC-IDS-05 Story 6** — `SupabaseDatabase` уже использует `request_timeout_s`, ничего не меняется.

Места использования `oidc_request_timeout_s`:

- `AuthenticateProvider` при OIDC discovery
- `EIDEasyProvider` при вызове `/token`
- `MockEIDProvider` — игнорирует (заглушка)

**Файлы:** `EPIC-IDS-01`, `EPIC-IDS-05`, `docs/requirements/07-env-configuration-spec.md`, `docs/requirements/12-oidc-authentigate-spec.md`.

---

## Сводная таблица доработок по файлам


| Файл                  | Что добавить/изменить                                                                                                                                                | Откуда             |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| `EPIC-IDS-01` Story 2 | `create_app()` → нет (это Story 4); `eid_secret` вместо `eid_hash_secret`; +`oidc_request_timeout_s: int = 10`; +AC пустой секрет pilot; +фраза про порядок проверок | 4.2, 4.4, 4.5, 4.6 |
| `EPIC-IDS-02` Story 4 | Заменить lifespan-паттерн на `create_app(config)`                                                                                                                    | 4.1                |
| `EPIC-IDS-04` Story 2 | +`core/security/hashing.py` описание + импорт в `from_config`                                                                                                        | 4.3                |
| `EPIC-IDS-05` Story 6 | Без изменений — `request_timeout_s` уже корректен                                                                                                                    | —                  |
| `EPIC-IDS-06` Story 1 | conftest: только `DOGESTONIA_EID_SECRET`, без `EID_HASH_SECRET`                                                                                                      | 4.2                |
| `req-07`              | `DOGESTONIA_EID_SECRET` как единственная; +`OIDC_REQUEST_TIMEOUT_S`; удалить `EID_HASH_SECRET`, `SUPABASE_ANON_KEY`                                                  | 4.2, 4.6           |
| `req-12`              | `OIDC_REQUEST_TIMEOUT_S` → из AppConfig, не хардкод                                                                                                                  | 4.6                |
| `ADR-IDS-008`         | Обновить: решение пересмотрено, выбрано `DOGESTONIA_EID_SECRET`                                                                                                      | 4.2                |


---

## Открытые вопросы после интервью

**Статус (2026-05-27):** пункты 1–3 закрыты; эпики и requirements синхронизированы.

1. ~~**Имя поля в AppConfig для 4.2**~~ — **закрыто:** `DOGESTONIA_EID_SECRET` → `AppConfig.eid_secret`.
2. ~~**Grep `eid_hash_secret` в эпиках**~~ — **закрыто:** обновлены EPIC-IDS-01..06 и requirements.
3. ~~**`hash_secret` ключ**~~ — **закрыто:** `hash_secret(plaintext, *, key: str)` в `core/security/hashing.py` (EPIC-IDS-04).

