# Аудит EPIC-IDS-01 — Scaffold, Config и Launch

> **Дата:** 2026-05-28
> **Методология:** [`analysis.mdc`](../../../../.cursor/rules/analysis.mdc) — только верифицированные факты с путями и строками
> **Предмет:** Acceptance Criteria каждой Story vs фактический код + referenced requirements
> **Статус эпика:** Implemented (Waiting Acceptance)

---

## Сводная таблица findings

| ID   | Story | Severity | Суть |
|------|-------|----------|------|
| F1-1 | 1     | HIGH     | `src/core/security/__init__.py` отсутствует |
| F2-1 | 2     | HIGH     | `API_BASE_URL` не включён в `pilot_required` |
| F1-2 | 1     | MEDIUM   | AC "no tests ran" — неверно, тесты уже существуют |
| F1-3 | 1     | MEDIUM   | `hashing.py` описан как "placeholder", реализован полностью |
| F2-2 | 2     | MEDIUM   | `db_enabled` не покрыт тестами |
| F2-3 | 2     | MEDIUM   | Нет теста для `pilot + missing OAUTH_ACCESS_TOKEN_SECRET` |
| F3-1 | 3     | MEDIUM   | `_parse_dotenv_file()` не тестируется |
| F1-5 | 1     | LOW      | `pyrightconfig.json` конфликтует с `[tool.pyright]` в `pyproject.toml` |
| F4-1 | 4     | LOW      | Makefile `test-live`: флаги `-q -v` конфликтуют |
| F2-4 | 2     | LOW      | `EIDEASY_ALLOWED_METHODS` default: порядок расходится в коде и `.env.example` |
| F1-4 | 1     | LOW      | `httpx` в dev-deps не указан в Story 1 Outputs |
| F4-2 | 4     | LOW      | `DOGESTONIA_EID_SECRET=` в неверной секции `.env.example` |

---

## Story 1 — Инициализация пакета и зависимостей

### F1-1 [HIGH] `src/core/security/__init__.py` отсутствует

`src/core/security/` содержит `hashing.py`, но `__init__.py` не создан. `core` — обычный пакет (имеет `__init__.py`), поэтому `core.security` без `__init__.py` является namespace package, что непоследовательно с остальной структурой.

`from core.security.hashing import hash_secret` может давать разное поведение в зависимости от порядка `sys.path` и версии Python. EPIC-IDS-04 Story 2 вызывает этот импорт — без `__init__.py` риск `ModuleNotFoundError`.

**Как закрыть:** создать пустой `src/core/security/__init__.py`. Добавить AC в Story 1:
```
python3.11 -c "from core.security.hashing import hash_secret; print(hash_secret('x', key='k'))" → exit 0
```

---

### F1-2 [MEDIUM] Story 1 AC "no tests ran" — неверно

Story 1 AC: `python3.11 -m pytest --collect-only -q` → "no tests ran".

Факт: `tests/test_config_schema.py` (8 тестов) и `tests/test_env_file.py` (2 теста) уже существуют и будут собраны. AC должен гласить "коллекция без `ModuleNotFoundError`", а не "no tests ran".

**Как закрыть:** заменить AC на: `python3.11 -m pytest --collect-only -q` — завершается без `ModuleNotFoundError`, количество тестов ≥ 0.

---

### F1-3 [MEDIUM] `hashing.py` описан как "placeholder" — реализован полностью

Story 1 Output: `src/core/security/hashing.py — placeholder (контракт в EPIC-IDS-04 Story 2)`.

Фактическое содержимое файла:
```python
def hash_secret(plaintext: str, *, key: str) -> str:
    """Create deterministic HMAC hash for secret values."""
    return hmac.new(key.encode("utf-8"), plaintext.encode("utf-8"), hashlib.sha256).hexdigest()
```

Функция полностью реализована с правильной сигнатурой (`plaintext`, `*, key`). Слово "placeholder" неверно. Агент EPIC-IDS-04, прочитав эпик, может попытаться перезаписать файл с другой сигнатурой — регрессионный риск.

**Как закрыть:** заменить формулировку на: "Реализован: `hash_secret(plaintext: str, *, key: str) -> str` (HMAC-SHA256). EPIC-IDS-04 Story 2 только импортирует из `core.security.hashing`, не переопределяет."

---

### F1-4 [LOW] Dev-зависимость `httpx` отсутствует в описании Story 1

Story 1 Output перечисляет dev deps: `pytest>=8.0.0`, `pytest-asyncio>=0.24.0`.

Фактический `pyproject.toml` строка 25:
```toml
dev = [
  "pytest>=8.0.0",
  "pytest-asyncio>=0.24.0",
  "httpx>=0.27.0",     ← не упомянут в эпике
]
```

**Как закрыть:** добавить `httpx>=0.27.0` в список dev deps в Story 1 Output.

---

### F1-5 [LOW] `pyrightconfig.json` конфликтует с `[tool.pyright]` в pyproject.toml

`pyrightconfig.json` (корень репозитория):
```json
{"include": ["src", "tests"], "extraPaths": ["src"], "pythonVersion": "3.11"}
```

`pyproject.toml` `[tool.pyright]`:
```toml
extraPaths = ["src", "tests"]
```

При наличии обоих файлов **`pyrightconfig.json` имеет приоритет**. Эффективный `extraPaths = ["src"]` — без `tests`. Тестовые модули (`from core.config import ...` в `test_*.py`) не будут type-checked в IDE.

**Как закрыть:** добавить `"tests"` в `extraPaths` в `pyrightconfig.json`, либо удалить `pyrightconfig.json` и оставить только `[tool.pyright]` в `pyproject.toml`.

---

## Story 2 — AppConfig

### F2-1 [HIGH] `API_BASE_URL` не в `pilot_required` — нарушение fail-fast порядка

`schema.py` строки 116–128: кортеж `pilot_required` содержит 8 проверок. `API_BASE_URL` отсутствует.

`_required(env, "API_BASE_URL")` вызывается в строке 133 — в `return AppConfig(...)`, после пилот-блока. Поведение: `APP_PROFILE=pilot` + отсутствующий `API_BASE_URL` даёт `ConfigError("Required env var 'API_BASE_URL' is missing")` — корректное сообщение, но не из pilot-секции.

Нарушение принципа "pilot_required = всё обязательное в одном месте". Нет теста, покрывающего этот кейс.

**Как закрыть:** добавить в `pilot_required`:
```python
("API_BASE_URL", _value(env, "API_BASE_URL", "")),
```
Либо добавить явный AC + тест: `load_config_from_env({"APP_PROFILE": "pilot", ...все_секреты..., API_BASE_URL отсутствует}) → ConfigError`.

---

### F2-2 [MEDIUM] `db_enabled` не покрыт тестами

`schema.py` строка 166: `db_enabled=(db_backend == "supabase")`. Поле присутствует в `AppConfig` (строка 55).

Ни один тест в `test_config_schema.py` не делает `assert cfg.db_enabled`. Epic Section 8 (верификационный скрипт) проверяет `assert cfg.db_enabled is False`, но это shell-команда, не pytest-тест.

**Как закрыть:**
- В `test_demo_minimal_defaults` добавить `assert cfg.db_enabled is False`.
- Добавить отдельный тест с `DB_BACKEND=supabase` (+ необходимые `SUPABASE_*`) → `assert cfg.db_enabled is True`.

---

### F2-3 [MEDIUM] Нет теста, изолирующего `OAUTH_ACCESS_TOKEN_SECRET` в pilot

Epic Story 2 AC: `load_config_from_env({"APP_PROFILE": "pilot", ...})` без `OAUTH_ACCESS_TOKEN_SECRET` → `ConfigError`.

Существующий тест `test_pilot_requires_secrets` (`test_config_schema.py:72`) не передаёт supabase-credentials, поэтому падает на проверке `SUPABASE_URL` — до `OAUTH_ACCESS_TOKEN_SECRET`. Сам путь кода (`schema.py:123`) для `OAUTH_ACCESS_TOKEN_SECRET` не проходит через тест.

**Как закрыть:** добавить тест, передающий все pilot-required (`SUPABASE_URL`, `SUPABASE_SERVICE_ROLE`, `SUPABASE_JWT_SECRET`, `DATABASE_URL`, `DOGESTONIA_EID_SECRET`, `CODE_VERIFIER_ENCRYPTION_KEY`, `GPT_OAUTH_CLIENT_SECRET`) и намеренно опускающий `OAUTH_ACCESS_TOKEN_SECRET`, проверяя что `ConfigError` сообщение называет это поле.

---

### F2-4 [LOW] `EIDEASY_ALLOWED_METHODS` default различается в коде и `.env.example`

`schema.py` строка 162: default `"smartid,mid-login,ee-id-login"`.
`.env.example`: `EIDEASY_ALLOWED_METHODS=ee-id-login,mid-login,smartid`.

Порядок элементов различается. Функционально эквивалентно при split+set-проверке, но создаёт путаницу при сравнении кода и конфига.

**Как закрыть:** привести порядок к одному виду — рекомендуется `smartid,mid-login,ee-id-login` как в коде.

---

## Story 3 — Кастомный dotenv-парсер

### F3-1 [MEDIUM] `_parse_dotenv_file()` не тестируется

`env_file.py` строки 40–54: функция `_parse_dotenv_file(path: Path) -> dict[str, str]`. Несмотря на "одиночное подчёркивание" (условно-приватная), она является Output Story 3 и будет импортироваться в других эпиках.

В `test_env_file.py` нет ни одного теста для этой функции. Epic Story 3 AC её не упоминает.

**Как закрыть:** добавить тест в `test_env_file.py`:
```python
def test_parse_dotenv_file(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text('KEY1=val1\nKEY2="quoted"\n# comment\n\n')
    result = _parse_dotenv_file(env_file)
    assert result == {"KEY1": "val1", "KEY2": "quoted"}
```

---

## Story 4 — Makefile, Railway-конфиг, `.env.example`

### F4-1 [LOW] Makefile `test-live`: конфликт флагов `-q` и `-v`

`Makefile` строка 26:
```makefile
test-live:
	.venv/bin/python -m pytest tests/ -q -m live_integration -v
```

Флаги `-q` (quiet) и `-v` (verbose) противоречат друг другу. Epic Story 4 описывает `test-live` только с `-v`. В pytest при одновременном присутствии обоих побеждает `-v`, но комбинация запутывает.

**Как закрыть:** убрать `-q` из `test-live`: `.venv/bin/python -m pytest tests/ -m live_integration -v`.

---

### F4-2 [LOW] `DOGESTONIA_EID_SECRET=` размещён в неверной секции `.env.example`

`.env.example` структура:
```
# --- Identity Provider ---
EID_PROVIDER=mock
DOGESTONIA_EID_SECRET=    ← здесь
NODE_ID=tallinn

# --- Identity Secrets ---
# HMAC secret for verified_person_hash / subject_hash:
# python3 -c "import secrets,base64; ..."
CODE_VERIFIER_ENCRYPTION_KEY=    ← а здесь нет DOGESTONIA_EID_SECRET
```

Комментарий с командой генерации HMAC-ключа находится в секции "Identity Secrets", а сама переменная `DOGESTONIA_EID_SECRET=` — в секции "Identity Provider". Оператор, читающий сверху вниз, видит инструкцию генерации и не находит под ней нужную переменную.

**Как закрыть:** переместить `DOGESTONIA_EID_SECRET=` в секцию `# --- Identity Secrets ---`, рядом с командой генерации.

---

## Верификация Epic Goal (Section 8)

| Шаг | Ожидание | Статус |
|-----|----------|--------|
| `from core.config import AppConfig, provide_app_config` | ImportError = 0 | ✅ `config/__init__.py` экспортирует оба |
| `provide_app_config({...})` без `cluster_*` полей | Нет gateway-полей | ✅ `schema.py` не содержит `cluster_*` |
| `make check-env` печатает 6 identity-vars | `APP_PROFILE`, `PORT`, `SUPABASE_URL`, `SUPABASE_JWT_SECRET`, `AUTHENTIGATE_ISSUER`, `EID_PROVIDER` | ✅ Makefile совпадает |
| Fail-fast: pilot без секретов → `ConfigError` | — | ✅ код + `test_pilot_requires_secrets` |
| `railpack.json`: JSON-valid, `--app-dir src`, `--host 0.0.0.0`, `${PORT:-8100}` | — | ✅ |
| `AppConfig` immutable | `FrozenInstanceError` | ✅ `test_config_is_frozen` |
| `DB_BACKEND=sqlite` → `ConfigError` | — | ✅ `test_sqlite_backend_is_forbidden` |
| `EID_PROVIDER=unknown` → `ConfigError` | — | ✅ `test_unknown_eid_provider_rejected` |
| `DOGESTONIA_EID_SECRET` — одна переменная, без fallback | — | ✅ `schema.py:105`, нет `or env.get(...)` |
| `db_backend` проверяется первым | — | ✅ `schema.py:92–94` до `_profile()` |
| `oidc_request_timeout_s: int = 10` в AppConfig | — | ✅ `schema.py:26`, default `"10"` в `providers.py:20` |

---

## Приоритет исправлений

1. **F1-1** — создать `src/core/security/__init__.py` (риск `ModuleNotFoundError` при импорте в EPIC-IDS-04)
2. **F2-1** — добавить `API_BASE_URL` в `pilot_required` (нарушение fail-fast семантики)
3. **F2-2** — добавить `assert cfg.db_enabled` в тесты (coverage gap на critical field)
4. **F2-3** — добавить изолирующий тест для `OAUTH_ACCESS_TOKEN_SECRET` в pilot
5. **F1-3** — исправить "placeholder" → "реализован" в описании `hashing.py`
6. **F3-1** — добавить тест для `_parse_dotenv_file`
7. Остальное LOW — по усмотрению
