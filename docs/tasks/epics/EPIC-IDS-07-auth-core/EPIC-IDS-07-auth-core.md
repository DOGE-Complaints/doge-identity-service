# EPIC-IDS-07 — Auth Core (профиль и `/me`)

> **ID:** `EPIC-IDS-07` · **Alias (код):** `EPIC-IDS-AUTH-CORE` · **Статус:** 🟡 In Progress (Story 1+2 Done; epic gate pending — post-audit gaps pkg-000010 closed)
> **Layer:** Functional — identity / user profile
> **Зависит от:** EPIC-IDS-04 (SOA Service Factory, `ProfileRepository`, JWT bearer) — Done
> **Блокирует:** STORY-IDS-OAUTH-02 (introspection), gateway eID checks ([`09-gateway-expectations`](../../../runtime-docs/09-gateway-expectations.md))

---

## 1. Назначение

Первый функциональный защищённый маршрут identity: **`GET /me`** возвращает профиль пользователя, `eid_verified` и базовые права (`role` из JWT) по Supabase JWT. Реализован в STORY-IDS-AUTHCORE-01 ([`handle_me`](../../../src/core/api/handlers.py), [`asgi_app.py`](../../../src/core/api/asgi_app.py)).

Парадигма: [`04-security §Часть A`](../../../runtime-docs/04-security.md) — `/me` как точка, где gateway узнаёт `eid_verified`.

## 2. Источники

- Backlog intake: [`STORY-IDS-AUTHCORE-01-profile-and-me`](../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-01-profile-and-me.md), [`STORY-IDS-AUTHCORE-02-me-account-fields`](../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md)
- Runtime: [`01-api`](../../../runtime-docs/01-api.md), [`05-data-model`](../../../runtime-docs/05-data-model.md), [`04-security`](../../../runtime-docs/04-security.md)
- Post-audit: [`epic-ids-07-authcore-01-audit-2026-06-05`](../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md)
- CAB-02 interview: [`identity-cabinet-me-fields-interview-2026-07-13`](../../../analysis/identity-cabinet-me-fields-interview-2026-07-13.md) (D-CAB-1/2)

## 3. Вне scope эпика

- eID-флоу — отдельный эпик `EPIC-IDS-EID` (backlog).
- OAuth-сервер — отдельный эпик `EPIC-IDS-OAUTH` (backlog).

## 4. Предусловия

- EPIC-IDS-04: `ProfileRepository` (InMemory + Supabase), `get_current_user`, `ApiDependencies.profile_repository` ([`dependencies.py:97`](../../../src/core/api/dependencies.py)).
- EPIC-IDS-06: offline pytest + `_block_dotenv_leakage` ([`tests/conftest.py`](../../../tests/conftest.py)).

## 5. Целевые файлы (Story 1)

```
src/core/api/handlers.py
src/core/api/me_response.py
src/core/api/asgi_app.py
tests/test_me_profile.py
tests/test_http_transport_smoke.py
tests/test_asgi_transport.py
```

## 6. Stories

### Story 1: STORY-IDS-AUTHCORE-01 — Профиль пользователя и `GET /me` — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-AUTHCORE-01-profile-and-me/STORY-IDS-AUTHCORE-01-profile-and-me.md`](./stories/STORY-IDS-AUTHCORE-01-profile-and-me/STORY-IDS-AUTHCORE-01-profile-and-me.md)
- **Source (backlog):** [`backlog-stories/STORY-IDS-AUTHCORE-01-profile-and-me.md`](../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-01-profile-and-me.md)

**Acceptance Criteria:**
- [x] `GET /me` без токена → 401 `AUTHENTICATION_REQUIRED`.
- [x] `GET /me` с валидным Supabase JWT → 200, `data` содержит как минимум `supabase_user_id`, `eid_verified`, и (если есть) поля профиля.
- [x] Если профиля нет — поведение детерминировано и покрыто тестом.
- [x] Ответ в envelope-формате `{"data": {...}}`.
- [x] Покрыто тестами (offline, без сети) на оба backend'а (`in_memory`).

### Story 2: STORY-IDS-AUTHCORE-02 — `created_at` + `account_status` в `GET /me` — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-AUTHCORE-02-me-account-fields/STORY-IDS-AUTHCORE-02-me-account-fields.md`](./stories/STORY-IDS-AUTHCORE-02-me-account-fields/STORY-IDS-AUTHCORE-02-me-account-fields.md)
- **Source (backlog):** [`backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md`](../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md)
- **Wave:** `pkg-000044` (P3 Done 2026-07-24)

**Acceptance Criteria:**
- [x] `GET /me` `data.account_status == "active"` (всегда, включая no-profile). (`email` — приёмка в [ONB-01](../../backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md).)
- [x] `data.created_at` = ISO-8601 из `profiles.created_at` при наличии профиля; `null` — без профиля. **Никаких обращений к Supabase Auth** и **никакой записи в БД** (no-auto-provision сохранён).
- [x] Нет новой миграции/колонки (D-CAB-1): `grep account_status supabase/bootstrap/` → пусто.
- [x] `openapi.yaml` `MeData` + `API_REFERENCE.md §6` обновлены (created_at nullable, account_status enum + пометка «MVP: active»).
- [x] `test_me_profile.py` покрывает оба кейса (профиль/без); полная offline-сюита зелёная.

## 7. Верификация эпика (Story 1)

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
```
