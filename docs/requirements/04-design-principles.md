# 04. Принципы проектирования

> **Статус:** НЕ реализовано. Requirements document.
> **Сервис:** `doge-identity-service`

---

## P-001: Account-First Architecture

**Правило:** Пользователь всегда сначала авторизуется в DOGEstonia. eID — это upgrade существующего аккаунта, а не метод входа.

```
DOGEstonia session → eID verification → privileged action
```

**Следствие для кода:**
- `/auth/eid/start` требует валидного Supabase JWT. Без него — 401.
- Authentigate flow никогда не запускается для анонимного пользователя.
- eID callback привязывает верификацию к уже существующему `supabase_user_id`.

---

## P-002: One-Time Verification

**Правило:** После однократной привязки eID аккаунт считается верифицированным навсегда (до явного отзыва).

Backend НЕ требует повторную eID верификацию при каждой подаче story.

**Проверка при каждом запросе:**
```
profiles.eid_verified == true
```

Это быстрая DB-проверка, не новый OIDC flow.

**Повторная верификация требуется только при:**
- удалении аккаунта;
- отзыве администратором;
- security incident;
- явной policy re-verification (post-MVP).

---

## P-003: Session-Binding Rule (eID callback)

**Правило:** Единственный источник истины для привязки верификации к пользователю — `eid_verification_sessions.supabase_user_id`.

**Callback НИКОГДА не использует:**
- текущую браузерную сессию;
- cookies;
- любой контекст кроме валидированного `state` параметра из сессионной записи.

**Обоснование:** Пользователь может открыть eID в другом браузере или переключить аккаунт пока шла верификация. Привязка через сессионную запись гарантирует детерминизм.

---

## P-004: Privacy-by-Design / Minimal PII

**Запрещено персистировать:**
```
personal_code
legal_name
birthdate
document_number
raw_id_token
raw_access_token
```

**Разрешено хранить:**
```
eid_verified (boolean)
verified_person_hash (HMAC, не обратим к personal_code)
eid_provider
eid_method
eid_country
eid_verified_at
```

**`verified_person_hash` НИКОГДА не передаётся:**
- на frontend;
- в Custom GPT;
- в любой API response;
- on-chain.

**Назначение eID данных (purpose limitation):**
Только anti-bot protection, duplicate account prevention, verified civic participation.
НЕ для маркетинга, профилирования, продажи данных.

---

## P-005: Authentigate Encapsulation

**Правило:** Authentigate — внутренняя деталь реализации identity-service. Ни один внешний клиент не должен знать об Authentigate.

- Custom GPT → видит только OAuth 2.0 endpoints identity-service.
- spa-app → получает `redirect_url` от identity-service и редиректит пользователя. spa-app не знает OIDC параметры.
- doge-complaints-gateway → видит только Bearer token, не eID claims.

---

## P-006: Return URL Allowlist

**Правило:** `return_url` в `/auth/eid/start` MUST валидироваться против жёсткого allowlist на backend.

Backend MUST проверять: scheme + host + path. Query params не являются частью allowlist matching, но допустимые ключи query params тоже ограничены.

**Обоснование:** Открытый редирект (open redirect) — критическая уязвимость в OAuth/OIDC flows.

Разрешённые `return_url` values:
```
https://dogestonia.ee/verify
https://dogestonia.ee/dashboard/verify
```

Допустимые query param keys на разрешённых URL: `context`, `error`, `draft_id`.
Любой другой query key MUST быть удалён перед редиректом.

---

## P-007: Supabase Service Role Key — только server-side

**Правило:** `SUPABASE_SERVICE_ROLE` key НИКОГДА не попадает в браузер, в response headers, в logs.

Используется только в серверном коде identity-service для записи в protected таблицы и обхода RLS.

---

## P-008: No On-Chain PII

**Правило:** Следующие данные НИКОГДА не записываются on-chain:
```
personal_code
verified_person_hash
supabase_user_id
email
legal identity data
```

Это ограничение актуально когда появится wallet-signature layer.

---

## P-009: Wallet-Readiness (Post-MVP preparation)

**Правило:** Data model и story submission flow MUST быть проектированы так, чтобы wallet signatures могли быть добавлены позднее без breaking changes.

В MVP:
- `profiles.wallet_address` поле существует (NULL).
- Story submission принимает `payload_hash` (опционально).

Post-MVP:
- Wallet signature заменяет или дополняет eID verification как authorship proof.
- Суть: eID = временный anti-Sybil до появления wallet identity.

---

## P-010: Explicit Error Codes

**Правило:** Все ошибки identity-service возвращают структурированный JSON с machine-readable кодом.

```json
{
  "error": "<snake_case_code>",
  "message": "<human readable>",
  "next_action": "<optional: what user should do>"
}
```

Список обязательных error codes:
```
authentication_required       — нет сессии
verification_required         — нет eID
already_verified              — eID уже привязан к этому аккаунту
identity_already_linked       — eID уже привязан к другому аккаунту
invalid_or_consumed_state     — state replay или не найден
eid_session_expired           — сессия истекла
invalid_return_url            — return_url не в allowlist
```
