# STORY-IDS-ONB-01 — `email` в `/me` + требование Supabase «Confirm email»

## Meta
- **Key:** `STORY-IDS-ONB-01-email-in-me-and-supabase-confirm`
- **Epic:** `EPIC-IDS-ONBOARDING`
- **Type:** story
- **Status:** 🟢 Done
- **Источник:** [`identity-onboarding-ux-2026-06-12.md`](../../../analysis/identity-onboarding-ux-2026-06-12.md) §4 G2; решение интервью — «полагаться на Supabase Confirm email»
- **Зависит от:** [STORY-IDS-AUTHCORE-01](../auth-core/STORY-IDS-AUTHCORE-01-profile-and-me.md) (`/me`/профиль)
- **Решения (интервью 2026-07-13):** [`identity-cabinet-me-fields-interview`](../../../analysis/identity-cabinet-me-fields-interview-2026-07-13.md) — **D-CAB-3:** добавить `email_verified: true` (политика «токен ⇒ подтверждён»).
- **Координация:** пара к [AUTHCORE-02](../auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md) (CAB-02) — **обе правят [`me_response.py`](../../../../src/core/api/me_response.py)** + `api-reference` + `test_me_profile.py`; делать одной волной/очередью.

## Зачем простыми словами
Email-верификацию делает Supabase: при включённой настройке «Confirm email» неподтверждённый пользователь **не получает токен**, значит Identity его и не видит — отдельный блок в Identity не нужен. Но это решение нужно (а) зафиксировать как обязательную настройку проекта, иначе гейт не работает; (б) показать `email` в `/me`, чтобы потребитель (web/gateway) видел, кто залогинен.

## Scope
- **`/me` отдаёт `email`:** вынести `email` (уже парсится в [`UserClaims.email`](../../../../src/core/domain/models.py)) в payload `/me` ([`me_response.py`](../../../../src/core/api/me_response.py)). Сырой email — не PII-чувствительный для самого владельца токена (его же адрес).
- **Требование к Supabase (зафиксировать):** в [`supabase-project-setup.md`](../../../runbook/supabase-project-setup.md) добавить обязательный пункт — включить **«Confirm email»** (Auth → Providers → Email). Следствие: токен-холдер ⇒ email подтверждён (политика).
- **`email_verified: true`** в `/me` (D-CAB-3, решено **ДА**) — политика «валидный токен ⇒ Supabase подтвердил email». ⚠️ **Истинно только при включённом «Confirm email»** (см. пункт runbook выше) — это предусловие корректности поля.

## Подзадачи
- **T01 — `me_response.py`.** В базовый dict `build_me_data` добавить `data["email"] = current_user.email` и `data["email_verified"] = True` (верно и для no-profile). Координация с AUTHCORE-02 (тот же билдер `/me`).
- **T02 — Runbook + API-доки.** [`supabase-project-setup.md`](../../../runbook/supabase-project-setup.md) — обязательный пункт «включить Confirm email» (предусловие `email_verified`). `api-reference/openapi.yaml` `MeData` + `API_REFERENCE.md §6`: `email` (`[string,"null"]`), `email_verified` (bool, «политика: токен ⇒ true»).
- **T03 — Тесты (`test_me_profile.py`).** `email` из токена (`null`, если нет claim); `email_verified == true`. Полная offline-сюита зелёная.

## Вне scope
- Жёсткий email-гейт внутри Identity (решено: полагаемся на Supabase).
- Телефонный гейт — [DOC-IDS-ONB-01](DOC-IDS-ONB-01-lazy-phone-gate-contract.md).
- OAuth/GPT — OAUTH-01.

## Точки в коде (текущее состояние)
- `UserClaims.email: str | None` уже парсится из токена: [`models.py:18`](../../../../src/core/domain/models.py).
- `/me` payload **не содержит** `email`: [`me_response.py`](../../../../src/core/api/me_response.py) (поля eid/phone/role/display_name).
- Supabase-валидатор требует `role="authenticated"`: [`supabase_validator.py:34`](../../../../src/core/auth/supabase_validator.py).
- Runbook Supabase **не упоминает** Confirm-email: [`supabase-project-setup.md`](../../../runbook/supabase-project-setup.md).

## Acceptance Criteria
- [x] `GET /me` возвращает `email` (из токена; `null`, если в токене нет).
- [x] `GET /me` возвращает `email_verified: true` (D-CAB-3, политика «токен ⇒ подтверждён»).
- [x] `supabase-project-setup.md` содержит обязательный пункт «включить Confirm email» (предусловие корректности `email_verified`).
- [x] `api-reference` (`openapi.yaml` `MeData` + `API_REFERENCE.md §6`) обновлён на `email` + `email_verified`.
- [x] Offline-тест (`test_me_profile.py`) на `email` и `email_verified`; согласовано с AUTHCORE-02 (один билдер `/me`).

## Парадигма-якорь
[04-security](../../../runtime-docs/04-security.md) (токены/PII), [08-ui-expectations](../../../runtime-docs/08-ui-expectations.md) (контракт `/me` для UI).
