# 15. Story Authorization Endpoints

> **DEPRECATED (2026-06):** Story scope removed from identity-service. Stories are owned by doge-complaints-gateway; identity does not expose story routes or store `story_drafts`. This document is retained for historical reference only.
>
> **Статус:** DEPRECATED — historical spec only (см. banner выше). Не реализовано и не будет в identity-service.
> **Предусловие:** Файл 09 (Supabase JWT), файл 13 (conflict logic), файл 14 (OAuth token).
> **Связь:** Identity-service авторизует story actions; реальная pipeline историй — doge-complaints-gateway.

---

## Canonical Story Lifecycle в контексте identity-service

```
POST /story-drafts           — создать черновик (eID НЕ требуется)
      ↓
POST /story-drafts/{id}/submit — финальная подача (eID ТРЕБУЕТСЯ)

Shortcut для already-verified users:
POST /stories                — создать + подать атомически (eID ТРЕБУЕТСЯ)

Для Custom GPT:
POST /gpt/actions/submit-story — submit через ChatGPT (eID ТРЕБУЕТСЯ)
```

---

## POST /story-drafts

**Назначение:** Сохранить черновик до прохождения eID. Позволяет пользователю набрать историю → пройти eID → вернуться к черновику.

**Auth:** Supabase JWT Bearer (обязательно).  
**eID:** НЕ требуется.

### Request

```json
{
  "title": "Разбитые фонари на улице Таллинн 12",
  "body": "Уже третий месяц как...",
  "locale": "ru",
  "context": {
    "location": "Tallinn",
    "category": "infrastructure"
  }
}
```

### Алгоритм

```
1. Validate Supabase JWT → supabase_user_id
2. Check account active (not blocked)
3. INSERT story_drafts: { id: UUID, owner_user_id, content, created_at, status: 'draft' }
4. Log audit: story_draft_created
5. Return { draft_id, created_at, status: "draft" }
```

### Response

```json
HTTP 201
{
  "draft_id": "abc123",
  "status": "draft",
  "created_at": "2026-05-25T15:00:00Z"
}
```

---

## POST /story-drafts/{draft_id}/submit

**Назначение:** Финальная подача существующего черновика. Требует eID.

**Auth:** Supabase JWT Bearer (обязательно).  
**eID:** ОБЯЗАТЕЛЬНО (`profiles.eid_verified = true`).

### Алгоритм

```
1. Validate Supabase JWT → supabase_user_id
2. SELECT draft WHERE id = $draft_id
   → Если не найден: 404
3. Check draft.owner_user_id == supabase_user_id
   → Если нет: 403 { error: "forbidden" }
4. Check profiles.eid_verified == true
   → Если нет: 403 verification_required response
5. Forward to doge-complaints-gateway POST /intake/stories
   (добавить Authorization: Bearer <service_token>)
6. Log audit: story_draft_submitted
7. Return complaints-gateway response
```

### Response если не верифицирован

```json
HTTP 403
{
  "error": "verification_required",
  "reason": "Story submission requires eID verification.",
  "verification_start_url": "https://dogestonia.ee/verify",
  "draft_id": "abc123"
}
```

`draft_id` возвращается чтобы spa-app мог восстановить контекст после eID.

---

## POST /stories

**Назначение:** Shortcut для уже верифицированных пользователей. Атомически создаёт и подаёт историю.

**Auth:** Supabase JWT Bearer (обязательно).  
**eID:** ОБЯЗАТЕЛЬНО.

### Алгоритм

```
1. Validate Supabase JWT → supabase_user_id
2. Check profiles.eid_verified == true
   → Если нет: 403 verification_required
3. Validate story payload (basic schema check)
4. Forward to doge-complaints-gateway POST /intake/stories
5. Log audit: story_submit_success
6. Return { story_id, status: "accepted" }
```

### Response если не верифицирован

```json
HTTP 403
{
  "error": "verification_required",
  "reason": "Story submission requires eID verification.",
  "verification_start_url": "/auth/eid/start"
}
```

---

## POST /gpt/actions/submit-story

**Назначение:** Custom GPT endpoint. ChatGPT подаёт историю от имени пользователя.

**Auth:** OAuth access_token Bearer (файл 14 — `validate_oauth_access_token`).  
**Required scope:** `stories:create`.  
**eID:** ОБЯЗАТЕЛЬНО.

### Алгоритм

```
1. Validate OAuth access_token → OAuthClaims { supabase_user_id, scope }
2. Check scope contains "stories:create"
   → Если нет: 403 { error: "insufficient_scope" }
3. Check profiles.eid_verified == true
   → Если нет: 403 gpt_verification_required response
4. Forward to doge-complaints-gateway POST /intake/stories
   Body: { ...story_payload, submitter_external_user_id: supabase_user_id }
5. Log audit: gpt_submit_success
6. Return { story_id, status: "accepted" }
```

### Response если не верифицирован (human-friendly для ChatGPT)

```json
HTTP 403
{
  "error": "verification_required",
  "message": "Please open DOGEstonia and verify your account with Estonian eID before submitting stories.",
  "verification_url": "https://dogestonia.ee/verify"
}
```

ChatGPT показывает `message` пользователю и предлагает перейти по `verification_url`.

### GPT Story Payload

```json
{
  "title": "Story title",
  "body": "Full story text",
  "locale": "ru",
  "location": {
    "city": "Tallinn",
    "district": "Põhja-Tallinn"
  }
}
```

Identity-service добавляет к payload:
```json
{
  "submitter_external_user_id": "<supabase_user_id>",
  "submitter_identity_issuer": "doge-identity-service"
}
```

---

## story_drafts table (дополнительная таблица)

Требует отдельной миграции (добавить в файл 08 или создать `000004`):

```sql
CREATE TABLE IF NOT EXISTS public.story_drafts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT,
    body TEXT,
    locale TEXT,
    context JSONB,
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'submitted', 'expired')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS story_drafts_owner_idx
    ON public.story_drafts (owner_user_id, created_at DESC);
```

---

## Проброс запроса в doge-complaints-gateway

Identity-service выступает прокси/gateway для story submission. Прямое подключение:

```python
async with httpx.AsyncClient() as client:
    response = await client.post(
        f"{COMPLAINTS_GATEWAY_URL}/intake/stories",
        json={**story_payload, "submitter_external_user_id": supabase_user_id},
        headers={"Authorization": f"Bearer {SERVICE_API_TOKEN}"},
        timeout=10.0,
    )
```

`COMPLAINTS_GATEWAY_URL` и `SERVICE_API_TOKEN` — добавить в env vars (файл 07).

---

## Acceptance Criteria

- [ ] `POST /story-drafts` без JWT → 401
- [ ] `POST /story-drafts` с JWT, не верифицирован → 201 (черновик создаётся без eID)
- [ ] `POST /story-drafts/{id}/submit` без eID → 403 `verification_required` с `draft_id`
- [ ] `POST /story-drafts/{id}/submit` с чужим `draft_id` → 403 `forbidden`
- [ ] `POST /stories` без eID → 403 `verification_required`
- [ ] `POST /stories` с eID → 200 с `story_id`
- [ ] `POST /gpt/actions/submit-story` с OAuth token, без eID → 403 с `verification_url`
- [ ] `POST /gpt/actions/submit-story` с OAuth token без scope `stories:create` → 403 `insufficient_scope`
- [ ] `POST /gpt/actions/submit-story` с eID → проксируется в complaints-gateway
- [ ] `submitter_external_user_id` добавляется к payload автоматически (не от ChatGPT)
