# 17. eID Provider Abstraction — SOA Layer

> **Статус:** НЕ реализовано. Spec для `src/core/providers/` — провайдер-агностичного слоя верификации.
> **Контекст:** Замена жёсткой Authentigate-зависимости в файлах 11/12 на подключаемые провайдеры.
> **Предусловие:** Файл 06 (scaffold), файл 09 (JWT validation), файл 08 (migrations — будет поправлена схема).
> **Связь:** Файл 18 (eideasy provider) реализует этот интерфейс. Файл 12 (Authentigate) будет рефакторен как второй провайдер при появлении credentials.

---

## Проблема

Файлы 11 и 12 описывают flow, жёстко привязанный к Authentigate OIDC:
- `code_verifier_encrypted`, `nonce` в DB — артефакты PKCE, не нужны для OAuth2-провайдеров.
- `authentigate_client.py` — OIDC discovery, JWKS, ID token validation — всё специфично для Authentigate.
- Callback URL `/auth/eid/callback` жёстко зарегистрирован у Authentigate.

При смене провайдера на eideasy нужна другая схема сессии, другой callback URL, другой HTTP клиент. Без абстракции получится спагетти из `if provider == "authentigate"` по всему коду.

---

## Решение — Plugin архитектура

```
src/core/providers/
├── __init__.py
├── base.py              ← EIDProviderPort (Protocol), EIDVerificationResult, EIDSessionData
├── registry.py          ← get_active_provider() — читает EID_PROVIDER из env
├── mock/
│   └── mock_provider.py ← dev mock (всегда доступен)
├── eideasy/             ← OAuth2 provider (файл 18)
│   ├── config.py
│   ├── client.py
│   └── provider.py
└── authentigate/        ← OIDC provider (файл 12, рефакторинг при получении credentials)
    ├── config.py
    ├── client.py
    └── provider.py
```

**Публичные HTTP endpoints** (`/auth/eid/start`, `/auth/{provider}/callback`) становятся тонкими оркестраторами — они не знают про PKCE или OAuth2. Вся логика в провайдере.

---

## `src/core/providers/base.py`

```python
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class EIDVerificationResult:
    """Результат успешной верификации — провайдер-агностичный контракт."""
    provider: str           # "eideasy" | "authentigate" | "mock"
    country: str            # "EE"
    subject_hash: str       # HMAC-SHA256 идентификатор (never raw idcode)
    login_method: str       # "smartid" | "mid-login" | "ee-id-login"
    verified_at: datetime


@dataclass
class EIDStartResult:
    """Ответ на /auth/eid/start — что вернуть SPA."""
    redirect_url: str       # URL куда SPA делает window.location.href
    session_id: str         # ID созданной сессии (для audit)
    expires_at: datetime


@runtime_checkable
class EIDProviderPort(Protocol):
    """
    Интерфейс, который ОБЯЗАН реализовать каждый eID провайдер.
    Два метода: запустить flow + обработать callback.
    """

    @property
    def provider_name(self) -> str:
        """Уникальный машинный идентификатор провайдера: "eideasy", "authentigate", "mock"."""
        ...

    @property
    def callback_path(self) -> str:
        """
        Путь callback URL, зарегистрированный у провайдера.
        eideasy: "/auth/eideasy/callback"
        authentigate: "/auth/authentigate/callback"
        mock: "/auth/mock/callback"
        """
        ...

    async def start_flow(
        self,
        *,
        supabase_user_id: str,
        return_url: str,
        return_context: str,
        requested_action: str,
    ) -> EIDStartResult:
        """
        Инициирует eID flow.
        - Создаёт сессию в DB (provider-специфичные данные в provider_session_data JSONB).
        - Строит authorize URL.
        - Возвращает redirect_url для SPA.
        """
        ...

    async def handle_callback(
        self,
        *,
        raw_params: dict[str, str],  # все query params из GET callback
    ) -> tuple[EIDVerificationResult, str]:
        """
        Обрабатывает callback от провайдера.
        - Валидирует state.
        - Обменивает code на токен.
        - Получает и валидирует user data.
        - Возвращает (EIDVerificationResult, return_url).
        - Не записывает в DB — это делает вызывающий слой (file 11 бизнес-логика).
        """
        ...
```

---

## `src/core/providers/registry.py`

```python
from __future__ import annotations
from functools import lru_cache

from src.core.providers.base import EIDProviderPort


def get_active_provider() -> EIDProviderPort:
    """
    Возвращает активный eID провайдер на основе EID_PROVIDER env var.
    Вызывать через FastAPI Depends() или напрямую.
    """
    from src.core.config.schema import app_config
    provider_name = app_config().eid_provider  # читает EID_PROVIDER env var

    if provider_name == "eideasy":
        from src.core.providers.eideasy.provider import EIDEasyProvider
        return EIDEasyProvider()
    elif provider_name == "authentigate":
        from src.core.providers.authentigate.provider import AuthenticateProvider
        return AuthenticateProvider()
    elif provider_name == "mock":
        from src.core.providers.mock.mock_provider import MockEIDProvider
        return MockEIDProvider()
    else:
        raise ValueError(f"Unknown EID_PROVIDER: {provider_name!r}. Valid: eideasy, authentigate, mock")
```

**Правило:** `get_active_provider()` — НЕ `@lru_cache`. Провайдер создаётся per-request через FastAPI Depends. Это обеспечивает корректную инициализацию при тестах и позволяет менять провайдер без перезапуска (через env).

---

## Изменения в `src/core/config/schema.py`

Добавить в `AppConfig`:

```python
# Новые поля в AppConfig dataclass:
eid_provider: str = "eideasy"    # EID_PROVIDER env var: "eideasy" | "authentigate" | "mock"
eid_secret: str = ""             # DOGESTONIA_EID_SECRET — единый secret для HMAC subject_hash
node_id: str = "tallinn"         # NODE_ID — для multi-node поддержки (будущее)
```

Добавить в `ENV_SCHEMA` tuple:

```python
("EID_PROVIDER", "eid_provider", str, "eideasy"),
("DOGESTONIA_EID_SECRET", "eid_secret", str, ""),
("NODE_ID", "node_id", str, "tallinn"),
```

**Важно:** `DOGESTONIA_EID_SECRET` — единый HMAC secret для всех провайдеров (поле AppConfig: `eid_secret`). Провайдер сам формирует message (`"eideasy:EE:{idcode}"`), но ключ один. См. `ADR-IDS-008` (пересмотр 2026-05-27).

---

## Изменения в DB схеме `eid_verification_sessions`

**Проблема:** Текущая схема (файл 08) содержит PKCE-специфичные поля:
```sql
nonce TEXT NOT NULL,
code_verifier_encrypted TEXT NOT NULL,
code_verifier_hash TEXT NOT NULL,
```

Эти поля нужны только для Authentigate OIDC. eideasy не использует ни nonce, ни code_verifier.

**Решение:** Provider-specific данные в JSONB колонке.

```sql
-- Добавить в миграцию (новая миграция или изменение 08):
-- 20260526000001_eid_sessions_provider_abstraction.sql

ALTER TABLE public.eid_verification_sessions
  ADD COLUMN IF NOT EXISTS provider TEXT NOT NULL DEFAULT 'eideasy',
  ADD COLUMN IF NOT EXISTS provider_session_data JSONB NOT NULL DEFAULT '{}';

-- Старые PKCE поля: сделать nullable (для обратной совместимости при Authentigate)
ALTER TABLE public.eid_verification_sessions
  ALTER COLUMN nonce DROP NOT NULL,
  ALTER COLUMN code_verifier_encrypted DROP NOT NULL,
  ALTER COLUMN code_verifier_hash DROP NOT NULL;

-- Индекс для поиска по provider (для audit/cleanup)
CREATE INDEX IF NOT EXISTS idx_eid_sessions_provider
  ON public.eid_verification_sessions (provider);
```

**Содержимое `provider_session_data` по провайдеру:**

| Provider | JSON содержимое |
|----------|----------------|
| `eideasy` | `{"oauth_state": "<random>", "return_to": "/verify?..."}` |
| `authentigate` | `{"nonce": "...", "code_verifier_encrypted": "...", "code_verifier_hash": "..."}` |
| `mock` | `{}` |

---

## Публичные HTTP endpoints (провайдер-агностичные)

### POST /auth/eid/start (файл 11 — обновить)

Становится тонким оркестратором:

```python
# src/core/api/routes/eid_start.py

@router.post("/auth/eid/start")
async def start_eid_flow(
    body: EidStartRequest,
    user: UserClaims = Depends(get_current_user),
    provider: EIDProviderPort = Depends(get_active_provider),
    db: AsyncConnection = Depends(get_db),
):
    # Валидация return_url (allowlist — логика из файла 11)
    validate_return_url(body.return_url)

    # Делегируем провайдеру — он сам знает про PKCE или state
    result = await provider.start_flow(
        supabase_user_id=user.sub,
        return_url=body.return_url,
        return_context=body.return_context,
        requested_action=body.requested_action,
    )

    return {"redirect_url": result.redirect_url, "expires_at": result.expires_at}
```

### Provider callbacks (провайдер-специфичные маршруты)

Каждый провайдер регистрирует свой callback route через `callback_path`:

```python
# src/core/api/routes/eid_callback.py

from src.core.providers.registry import get_active_provider
# ... импорты

@router.get("/auth/eideasy/callback")
async def eideasy_callback(
    request: Request,
    db: AsyncConnection = Depends(get_db),
):
    return await handle_provider_callback(request, "eideasy", db)

@router.get("/auth/authentigate/callback")
async def authentigate_callback(
    request: Request,
    db: AsyncConnection = Depends(get_db),
):
    return await handle_provider_callback(request, "authentigate", db)

@router.get("/auth/mock/callback")
async def mock_callback(
    request: Request,
    db: AsyncConnection = Depends(get_db),
):
    return await handle_provider_callback(request, "mock", db)


async def handle_provider_callback(request: Request, provider_name: str, db):
    """
    Общая логика для всех callback routes.
    Провайдер-специфичная логика делегируется провайдеру.
    Бизнес-логика (conflict detection, mark eid_verified) — здесь.
    """
    from src.core.providers.registry import get_active_provider
    provider = get_active_provider()

    # Safety check: callback должен соответствовать активному провайдеру
    # (или mock в dev режиме)
    if provider.provider_name != provider_name and provider_name != "mock":
        return RedirectResponse(f"{base_return_url}?error=provider_mismatch")

    try:
        verification, return_url = await provider.handle_callback(
            raw_params=dict(request.query_params),
        )
    except EIDProviderError as e:
        return RedirectResponse(f"{return_url_from_state}?error={e.code}")

    # Бизнес-логика — провайдер-агностичная:
    await attach_eid_to_user(db, verification)    # conflict detection (файл 13)
    await mark_profile_verified(db, verification) # update profiles.eid_verified = true
    await write_audit_event(db, "eid_verified", verification)

    return RedirectResponse(return_url)
```

---

## Mock провайдер (dev без eideasy credentials)

```python
# src/core/providers/mock/mock_provider.py

class MockEIDProvider:
    @property
    def provider_name(self) -> str:
        return "mock"

    @property
    def callback_path(self) -> str:
        return "/auth/mock/callback"

    async def start_flow(self, *, supabase_user_id, return_url, **kwargs) -> EIDStartResult:
        # В dev: немедленно создаём "успешную" сессию и редиректим на mock callback
        session_id = str(uuid4())
        # store session in DB with provider_session_data={}
        mock_callback = f"/auth/mock/callback?session_id={session_id}&mock=1"
        return EIDStartResult(
            redirect_url=mock_callback,
            session_id=session_id,
            expires_at=datetime.now(UTC) + timedelta(minutes=10),
        )

    async def handle_callback(self, *, raw_params) -> tuple[EIDVerificationResult, str]:
        # Возвращает фиктивный успех
        return (
            EIDVerificationResult(
                provider="mock",
                country="EE",
                subject_hash="mock-hash-" + secrets.token_hex(8),
                login_method="mock",
                verified_at=datetime.now(UTC),
            ),
            "/verify?context=dashboard_verification",
        )
```

---

## Конфигурация для `EID_PROVIDER=mock` (dev)

```env
EID_PROVIDER=mock
DOGESTONIA_EID_SECRET=dev-only-not-a-real-secret
NODE_ID=tallinn
```

Без `EIDEASY_*` и без `AUTHENTIGATE_*` — mock работает локально.

---

## Взаимодействие с существующими файлами

| Файл | Статус после внедрения абстракции |
|------|----------------------------------|
| Файл 11 (eid-verification-flow) | POST /auth/eid/start переписывается как тонкий orchestrator. GET /auth/eid/callback → заменяется на provider-specific routes. |
| Файл 12 (authentigate-oidc-client) | Становится `src/core/providers/authentigate/` — один из провайдеров. Реализуется когда получены Authentigate credentials. |
| Файл 07 (env-configuration) | EID_PROVIDER, DOGESTONIA_EID_SECRET, NODE_ID. AUTHENTIGATE_* остаются (для будущего провайдера). |
| Файл 08 (migrations) | Новая миграция: добавить `provider`, `provider_session_data JSONB`; сделать PKCE поля nullable. |
| Файл 13 (hash-and-conflict) | `generate_verified_person_hash()` переименовать в `generate_subject_hash()`; принимает уже готовый message от провайдера. |

---

## Acceptance Criteria

- [ ] `EID_PROVIDER=eideasy` → используется EIDEasyProvider
- [ ] `EID_PROVIDER=mock` → используется MockEIDProvider, верификация проходит без credentials
- [ ] `EID_PROVIDER=unknown_value` → сервис не стартует (ошибка валидации конфига)
- [ ] Добавление нового провайдера = только создать новый `provider.py` + добавить case в registry.py
- [ ] POST /auth/eid/start не содержит if/else по имени провайдера
- [ ] handle_provider_callback содержит бизнес-логику (conflict detection, mark verified) — не в провайдере
- [ ] `eid_verification_sessions.provider_session_data` хранит provider-специфичные данные
- [ ] PKCE поля в DB nullable — обратная совместимость при переключении провайдеров
