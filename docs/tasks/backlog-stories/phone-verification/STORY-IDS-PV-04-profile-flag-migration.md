# STORY-IDS-PV-04 — Флаг профиля + модель данных + миграция + дедуп

## Meta
- **Key:** `STORY-IDS-PV-04-profile-flag-migration`
- **Epic:** `EPIC-IDS-PHONE`
- **Status:** 🟢 Done (pkg-000025; migration [`20260611000001_profiles_phone_verification.sql`](../../../../supabase/migrations/20260611000001_profiles_phone_verification.sql))
- **Источник:** [`phone-verification-architecture-2026-06-10.md`](../../../analysis/phone-verification-architecture-2026-06-10.md) §4, §10.1 (P1)
- **Зависит от:** [PV-01](STORY-IDS-PV-01-phone-provider-backbone.md) (для `PhoneVerificationResult`); параллельно PV-03

## Зачем простыми словами
Куда записать результат: ставим в профиле флаг `phone_verified=true` и сохраняем хэш номера — ровно как сделано для eID (`eid_verified`). Плюс реализуем правило **«один номер = один аккаунт»**: если этот номер уже подтверждён на другом профиле — отклоняем (конфликт 409), как при eID.

## Scope
- **Колонки профиля** (миграция Supabase, по образцу [`20260525000001_create_profiles.sql`](../../../../supabase/migrations/)): `phone_verified bool`, `verified_phone_hash text`, `phone_provider text`, `phone_dial_prefix text`, `phone_verified_at timestamptz`; индекс на `verified_phone_hash` (для дедупа).
- **`ProfileRecord`** + репозиторий: добавить поля (зеркало eID-полей [`models.py:23-40`](../../../../src/core/domain/models.py)) и метод `attach_phone_verification(user_id, *, provider, dial_prefix, verified_phone_hash, verified_at)` — по образцу `attach_eid_verification` ([`contracts.py:30-39`](../../../../src/core/domain/contracts.py), [`repositories.py:84-96`](../../../../src/core/infrastructure/repositories.py)).
- **Дедуп (P1):** при `PHONE_ONE_ACCOUNT_PER_NUMBER=true` — если `verified_phone_hash` уже на другом `supabase_user_id` → `ProfileConflictError` (переиспользуем [`models.py:11`](../../../../src/core/domain/models.py)); поиск — методом `get_by_verified_phone_hash` (зеркало `get_by_verified_person_hash`, [`repositories.py:64`](../../../../src/core/infrastructure/repositories.py)).
- **`/me`:** отдавать `phone_verified` и связанные поля (по образцу [`me_response.py`](../../../../src/core/api/me_response.py)).

## Вне scope
- Сама оркестрация записи (когда вызывать `attach`) — [PV-05](STORY-IDS-PV-05-verification-flow-api.md).
- Telnyx — PV-06/07.

## Точки в коде (образец eID)
- Профиль-флаги eID: [`models.py:23-40`](../../../../src/core/domain/models.py) (`eid_verified`/`verified_person_hash`/`eid_verified_at`).
- Конфликт/дедуп: [`models.py:11`](../../../../src/core/domain/models.py) (`ProfileConflictError`), [`contracts.py:26,30`](../../../../src/core/domain/contracts.py), [`repositories.py:64,84-96`](../../../../src/core/infrastructure/repositories.py).
- `/me`: [`me_response.py`](../../../../src/core/api/me_response.py).
- Миграции: [`supabase/migrations/`](../../../../supabase/migrations/).

## Acceptance Criteria
- [ ] Миграция добавляет phone-колонки + индекс на `verified_phone_hash`.
- [ ] `attach_phone_verification` ставит `phone_verified=true` + хэш/префикс/время.
- [ ] При `PHONE_ONE_ACCOUNT_PER_NUMBER=true` повтор номера на другом аккаунте → `ProfileConflictError`/409 (тест на дедуп).
- [ ] `/me` отдаёт `phone_verified` и поля.
- [ ] Offline-набор зелёный (in-memory + миграционный тест если применимо).

## Парадигма-якорь
[05-data-model](../../../runtime-docs/05-data-model.md) (profiles), [04-security](../../../runtime-docs/04-security.md) (anti-Sybil, PII).
