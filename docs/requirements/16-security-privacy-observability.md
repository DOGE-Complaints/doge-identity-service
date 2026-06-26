# 16. Security, Privacy, Observability

> **Статус:** НЕ реализовано. Сводная спецификация требований безопасности.
> **Связь:** Применяется ко всем файлам 09-15. Обязательно при реализации каждого компонента.

---

## Security Requirements (BE-SEC)

| ID | Требование | Применение |
|----|-----------|-----------|
| BE-SEC-001 | OIDC validation: state, nonce, token signature, issuer, audience, expiration, issued_at, acr/amr | Файл 12 (Authentigate client) |
| BE-SEC-002 | Valid DOGEstonia session требуется перед: start eID, check status, submit story, link wallet | Файлы 11, 15 |
| BE-SEC-003 | Rate limits: `/auth/eid/start` — 5 req / 10 min / user; `/stories` — 20 req / hour / user; `/gpt/actions/submit-story` — 10 req / hour / user | Файл 11, 15 |
| BE-SEC-004 | Запрещено персистировать: personal_code, legal_name, birthdate, raw_id_token, raw_access_token, document_number | Файлы 12, 13 |
| BE-SEC-005 | Запрещено on-chain: personal_code, verified_person_hash, supabase_user_id, email, legal identity data | Файл 13 |
| BE-SEC-006 | FastAPI MUST validate Supabase access token: JWT signature (JWKS / JWT secret), iss, aud, exp, sub. Frontend session alone — NOT trusted. | Файл 09 |

---

## Privacy Requirements (BE-PRIV)

| ID | Требование |
|----|-----------|
| BE-PRIV-001 | Purpose limitation: только anti-bot protection, duplicate account prevention, verified civic participation. НЕ для маркетинга, профилирования, продажи данных. |
| BE-PRIV-002 | Data minimization: хранить только `eid_verified`, `verified_person_hash`, `eid_provider`, `eid_method`, `eid_country`, `eid_verified_at`. |
| BE-PRIV-003 | Backend поддерживает frontend messaging: personal code не хранится в читаемом виде; identity data не пишется в blockchain. |

---

## Rate Limiting — реализация

MVP минимум: per-user rate limiting через sliding window в памяти или Redis.

```python
# Паттерн: simple in-memory rate limiter (demo), Redis-backed (pilot)

RATE_LIMITS = {
    "/auth/eid/start":            RateLimit(requests=5,  window_s=600,  per="user"),
    "/stories":                   RateLimit(requests=20, window_s=3600, per="user"),
    "/gpt/actions/submit-story":  RateLimit(requests=10, window_s=3600, per="user"),
    "/auth/eid/callback":         RateLimit(requests=5,  window_s=600,  per="ip"),
}
```

При превышении:
```json
HTTP 429
{
  "error": "rate_limit_exceeded",
  "retry_after": 300
}
```

---

## CORS Configuration

```python
# Для demo: широко открыто
CORSMiddleware(
    allow_origins=config.cors_allowed_origins,  # из CORS_ALLOWED_ORIGINS env
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["authorization", "x-trace-id", "content-type"],
)
```

Production `CORS_ALLOWED_ORIGINS`:
```
https://dogestonia.ee
https://chat.openai.com
```

---

## PII в Logs — запрещённые поля

Никогда не логировать:
```
personal_code
verified_person_hash
supabase_user_id (в сообщениях уровня DEBUG/INFO — только в структурированных полях для трассировки)
raw_id_token
raw_access_token
client_secret
DOGESTONIA_EID_SECRET
CODE_VERIFIER_ENCRYPTION_KEY
OAUTH_ACCESS_TOKEN_SECRET
```

**Разрешено логировать:**
```
trace_id
event_type (eid_verification_started, etc.)
success: true/false
failure_reason (error code, not user data)
eid_method (smart_id, mobile_id)
eid_country (EE, LV)
```

---

## Audit Events — полный список

Записываются в `public.eid_audit_events` через `src/core/audit/audit_logger.py`.

| Event | Триггер | success |
|-------|---------|---------|
| `eid_verification_started` | POST /auth/eid/start успешно | true |
| `eid_verification_success` | Callback обработан, eid_verified=true | true |
| `eid_verification_failed` | Ошибка token exchange / ID token | false |
| `eid_already_verified` | /start вызван для уже верифицированного | true |
| `eid_identity_conflict` | Case C в conflict detection | false |
| `eid_session_expired` | Callback после expires_at | false |
| `eid_state_replay_rejected` | state уже consumed/not found | false |
| `eid_return_url_rejected` | return_url не в allowlist | false |
| `story_draft_created` | POST /story-drafts | true |
| `story_draft_submitted` | POST /story-drafts/{id}/submit успешно | true |
| `story_submit_blocked_unverified` | POST /stories без eID | false |
| `story_submit_success` | POST /stories успешно | true |
| `gpt_submit_blocked_unverified` | GPT submit без eID | false |
| `gpt_submit_success` | GPT submit успешно | true |
| `oauth_code_issued` | POST /oauth/authorize/complete | true |
| `oauth_token_issued` | POST /oauth/token | true |
| `oauth_token_invalid` | Невалидный access_token в любом endpoint | false |

---

## Audit Logger Interface

```python
# src/core/audit/audit_logger.py

async def log_eid_event(
    conn: psycopg.AsyncConnection,
    *,
    event_type: str,
    supabase_user_id: str | None,
    provider: str | None,
    method: str | None,
    success: bool,
    failure_reason: str | None = None,
    request_id: str | None = None,
    ip_address: str | None = None,   # хэшируется внутри функции
    user_agent: str | None = None,   # хэшируется внутри функции
) -> None:
    """
    Insert audit event. Hashes IP and User-Agent before storage (HMAC-SHA256 via
    `hash_secret` and `DOGESTONIA_EID_SECRET` — same key as other identity hashes).
    Never logs personal_code or raw tokens.
    """
    ip_hash = hash_secret(ip_address, key=eid_hmac_key) if ip_address else None
    ua_hash = hash_secret(user_agent, key=eid_hmac_key) if user_agent else None
    await conn.execute("""
        INSERT INTO public.eid_audit_events
            (supabase_user_id, event_type, provider, method, success,
             failure_reason, request_id, ip_hash, user_agent_hash)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
    """, supabase_user_id, event_type, provider, method, success,
         failure_reason, request_id, ip_hash, ua_hash)
```

---

## Trace ID паттерн (из complaints-gateway)

Каждый request получает `trace_id` (UUID). Логируется во все events.

```python
# src/core/api/envelope.py

def ensure_trace_id(incoming: str | None) -> str:
    if incoming and len(incoming) <= 64 and incoming.isprintable():
        return incoming
    return str(uuid.uuid4())
```

Header: `X-Trace-Id: <uuid>` — принимается от клиента (forwarded из spa-app или ChatGPT) или генерируется если отсутствует.

---

## Health и Readiness Endpoints

### GET /health

```json
HTTP 200
{
  "status": "ok",
  "service": "doge-identity-service",
  "version": "0.1.0"
}
```

### GET /ready

Проверяет:
1. DB connectivity (psycopg ping)
2. Required tables exist (profiles, eid_verification_sessions, eid_audit_events)
3. Authentigate issuer reachable (опционально, с timeout 2s)

```json
HTTP 200 (все OK)
{
  "status": "ok",
  "checks": {
    "db_connectivity": "ok",
    "db_tables": "ok",
    "oidc_discovery": "ok"
  }
}

HTTP 200 (деградированный)
{
  "status": "degraded",
  "checks": {
    "db_connectivity": "ok",
    "db_tables": "fail",
    "oidc_discovery": "ok"
  }
}
```

`/ready` возвращает HTTP 200 даже при `status: degraded` (load balancer pattern — не убирать из rotation, но сигнализировать о проблеме).

---

## Acceptance Criteria (Security)

- [ ] `POST /auth/eid/start` — превышение rate limit → 429 с `retry_after`
- [ ] Logs НЕ содержат `personal_code` ни в каком виде
- [ ] Logs НЕ содержат `verified_person_hash` ни в каком виде
- [ ] `GET /me` response НЕ содержит `verified_person_hash`
- [ ] Audit events пишутся в `eid_audit_events` для каждого события из списка
- [ ] IP в audit events хэшируется перед записью (не raw IP)
- [ ] CORS не разрешает wildcard origins в `pilot` профиле
- [ ] `GET /ready` при отсутствующих таблицах → `status: degraded`
- [ ] Все защищённые endpoints возвращают 401 при отсутствии Authorization header
