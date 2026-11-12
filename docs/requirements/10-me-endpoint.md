# 10. GET /me Endpoint

> **Актуализировано 2026-06-24 под фактический код (решение Q3: код — истина).** См. `docs/analysis/identity-backend-full-audit-2026-06-24.md`.
> **Статус:** Реализовано.
> **Предусловие:** Файл 08 (миграции) + Файл 09 (JWT validation) реализованы.
> **Назначение:** Основной endpoint для spa-app: загрузка профиля пользователя после логина.

---

## Endpoint

```
GET /me
Authorization: Bearer <supabase_access_token>
```

---

## Auth

Required: **да**.
Метод: Supabase JWT Bearer (файл 09 — `get_current_user` dependency).

Если токен отсутствует или невалиден — error envelope с кодом `AUTHENTICATION_REQUIRED` (uppercase, вложен под `error`):
```json
HTTP 401
{
  "error": {
    "code": "AUTHENTICATION_REQUIRED",
    "message": "Valid DOGEstonia session required."
  }
}
```

---

## Алгоритм обработки

```
1. Validate Supabase JWT → extract supabase_user_id, role
2. SELECT profile FROM public.profiles WHERE supabase_user_id = $1
3. If profile не найден:
   a. Вернуть синтетический профиль-view (eid_verified=false, поля профиля null)
   b. БЕЗ записи в БД
4. Build me data (build_me_data) и обернуть в success envelope
5. Return 200
```
(см. `src/core/api/handlers.py:85-87`, `src/core/api/me_response.py:17-46`)

**Нет auto-provision профиля (решение t01):**
`/me` НЕ создаёт запись в `public.profiles`. Для аутентифицированного пользователя без строки в таблице возвращается синтетический 200-ответ (profile-view) с `eid_verified=false` и null-полями профиля — без записи в БД. Профиль создаётся flow'ами верификации (eID / телефон), а НЕ вызовом `GET /me`. Проверяется тестом `tests/test_me_profile.py::test_me_missing_profile_returns_200_not_verified_no_db_write` («t01 decision: synthetic 200, ..., no upsert on GET /me»).

---

## Response (успех)

Ответ обёрнут в success envelope: `{ "data": { ... } }`. Поля `data` (РОВНО этот набор, `src/core/api/me_response.py:19-46`):

```json
HTTP 200
{
  "data": {
    "supabase_user_id": "a1b2c3d4-...",
    "eid_verified": true,
    "role": "authenticated",
    "display_name": "Zeya",
    "avatar_url": null,
    "eid_provider": "mock",
    "eid_method": "smart_id",
    "eid_country": "EE",
    "eid_verified_at": "2026-05-25T14:30:00Z",
    "phone_verified": false,
    "phone_provider": null,
    "phone_dial_prefix": null,
    "phone_verified_at": null
  }
}
```

**Поля которые НИКОГДА не возвращаются в /me:**
```
verified_person_hash    — никогда не передаётся на frontend (подтверждено кодом)
verified_phone_hash     — никогда не передаётся на frontend (подтверждено кодом)
```

> **Внимание:** `supabase_user_id` ВОЗВРАЩАЕТСЯ в `/me` (это первое поле `data`). Прежнее утверждение «используется только внутренне» — неверно; считать его не секретом в контексте этого ответа.

**Поля старого дизайна, которых НЕТ в коде (NOT IMPLEMENTED):**
```
user_id          — НЕ существует; фактическое имя поля = supabase_user_id
permissions      — НЕ ИМПЛЕМЕНТИРОВАНО; массива permissions нет нигде в коде
wallet_linked    — НЕ ИМПЛЕМЕНТИРОВАНО; не выставляется в /me
created_at       — НЕ ИМПЛЕМЕНТИРОВАНО; не выставляется в /me
```

---

## Permissions derivation logic — NOT IMPLEMENTED

> Массив `permissions` НЕ существует в коде, и `/me` его не возвращает. Раздел ниже — это исходный (нереализованный) дизайн, оставлен только для истории. Не является текущим контрактом.

| Условие | Разрешения (НЕ ИМПЛЕМЕНТИРОВАНО) |
|---------|-----------|
| Авторизован, `eid_verified=false` | `["stories:draft", "profile:read"]` |
| Авторизован, `eid_verified=true` | `["stories:create", "stories:draft", "profile:read"]` |
| Авторизован, `eid_verified=true`, `wallet_address` set | `["stories:create", "stories:draft", "profile:read", "wallet:linked"]` |

**stories:draft** — создание черновика без eID.  
**stories:create** — финальная подача story (требует eID).  

---

## Схема полного ответа

Фактический payload собирается `build_me_data` (`src/core/api/me_response.py`) как `dict` в составе `data` envelope. Точный набор ключей:

```python
# build_me_data(profile, current_user) -> dict, обёрнут в {"data": ...}
{
    "supabase_user_id": str,        # current_user.supabase_user_id
    "eid_verified": bool,           # False если профиля нет
    "role": str,                    # из JWT (например "authenticated")
    "display_name": str | None,
    "avatar_url": str | None,
    "eid_provider": str | None,     # например "mock"
    "eid_method": str | None,       # "smart_id" | "mobile_id" | "id_card"
    "eid_country": str | None,      # "EE" | "LV" | "LT"
    "eid_verified_at": str | None,  # ISO 8601 (isoformat)
    "phone_verified": bool,         # False если профиля нет
    "phone_provider": str | None,
    "phone_dial_prefix": str | None,
    "phone_verified_at": str | None,  # ISO 8601 (isoformat)
}
```

---

## Использование в spa-app

spa-app вызывает `/me` при:
- загрузке dashboard (чтобы знать надо ли показывать "Verify eID" CTA);
- после завершения eID flow (чтобы обновить статус);
- после OAuth login (чтобы показать profile.

**Кэширование на frontend:** spa-app может кэшировать response с коротким TTL (30-60 секунд) для снижения нагрузки.

---

## Acceptance Criteria

- [x] `GET /me` с валидным Supabase JWT → 200, `data` с корректным профилем
- [x] `GET /me` без токена → 401, `error.code == "AUTHENTICATION_REQUIRED"`
- [x] `GET /me` для пользователя без профиля → 200 (синтетический view), `eid_verified=false`, БЕЗ записи в БД
- [x] Response НЕ содержит `verified_person_hash` и `verified_phone_hash` ни в каком виде
- [x] Response содержит `supabase_user_id` как первое поле `data`
- [x] `eid_verified=true` → `eid_verified_at` присутствует и корректный ISO 8601
- [x] `phone_verified=true` → `phone_provider` / `phone_dial_prefix` / `phone_verified_at` присутствуют
- [ ] ~~`permissions`~~ — NOT IMPLEMENTED, не проверяется
