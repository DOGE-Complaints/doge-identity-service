# STORY-IDS-AUTHCORE-02 — Расширить `GET /me` полями аккаунта (created_at / account_status)

## Meta
- **Key:** `STORY-IDS-AUTHCORE-02-me-account-fields`
- **Parent Epic:** [`../../EPIC-IDS-07-auth-core.md`](../../EPIC-IDS-07-auth-core.md)
- **Epic alias (код):** `EPIC-IDS-AUTH-CORE`
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md`](../../../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md)
- **Decision Ref:** [`../../../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md`](../../../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md); [`identity-cabinet-me-fields-interview-2026-07-13.md`](../../../../../analysis/identity-cabinet-me-fields-interview-2026-07-13.md) (D-CAB-1/2); spa [`STORY-SPA-CAB-api-requirements`](../../../../../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-api-requirements.md)
- **Scope:** MVP · **Тип:** implement (extend endpoint + DTO + docs + tests)
- **Зависит от:** [AUTHCORE-01](../STORY-IDS-AUTHCORE-01-profile-and-me/STORY-IDS-AUTHCORE-01-profile-and-me.md) (`GET /me` + `ProfileRecord` уже есть)
- **Разграничение (no-duplication):** поле **`email` в `/me` — за [STORY-IDS-ONB-01](../../../../backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md)** (🟢 Done pkg-000045, 2026-07-24). Эта стори покрывает **только `created_at` + `account_status`**. Контракт CAB-02 (§0) для identity = **ONB-01 (email) + AUTHCORE-02 (created_at, account_status)** → теперь **3/3 live**.
- **Потребитель:** spa CAB-02 (Account Summary Block) — Email / Account Created / Account Status.
- **Координация:** пара к [ONB-01](../../../../backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md) — **обе правят [`me_response.py`](../../../../../../src/core/api/me_response.py)** + `api-reference` + `test_me_profile.py`; делать одной волной или явной очередью (иначе конфликт в билдере `/me`).

## Зачем простыми словами
Кабинет пользователя (SPA CAB-02) показывает карточку аккаунта: **Email**, **Account Created**, **Account Status**. Сейчас `GET /me` этих полей **не отдаёт** ([`me_response.py:19-46`](../../../../../../src/core/api/me_response.py) — есть `display_name/role/phone_*/eid_*`, но нет `email/created_at/account_status`). Фронт написан contract-first (как «готово»), чтобы не блокироваться — identity должен догнать контракт. CAB-02 выбрал **расширение `/me`**, а не отдельный endpoint.

## Контракт (из CAB-api-requirements §0)
`GET /me` `data` дополнить к существующим полями (этой стори — **выделенные**):
```jsonc
{
  "email": "user@example.com | null",                // ← STORY-IDS-ONB-01 (не здесь)
  "created_at": "2026-06-04T10:00:00Z",              // ISO-8601  ← ЭТА стори
  "account_status": "active | pending | suspended | archived"  // ← ЭТА стори
}
```
Остальной контракт `/me` (supabase_user_id, role, display_name, phone_*, eid_*) — без изменений.

## Источники полей (verified по коду)
| Поле | Источник | Готовность |
|------|----------|------------|
| ~~`email`~~ | → **[STORY-IDS-ONB-01](../../../../backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md)** (не в этой стори) | — вне scope здесь |
| `created_at` | `ProfileRecord.created_at` ([`models.py:44`](../../../../../../src/core/domain/models.py)); в БД `profiles.created_at` ([`000_full_init.sql:61`](../../../../../../supabase/bootstrap/000_full_init.sql)) | ✅ есть |
| `account_status` | **синтетическая константа `"active"`** (D-CAB-1) — колонки/миграции нет; enum остаётся в контракте на будущее | ✅ решено (тривиально) |

## Scope (что должно стать истинным)
- `GET /me` возвращает `created_at` и `account_status` (в дополнение, без ломки существующих полей). **`email` — не здесь** (ONB-01).
- **`account_status`** = **константа `"active"`** для всех (включая no-profile) — D-CAB-1. Без колонки/миграции.
- **`created_at`** = `profiles.created_at` через `_format_datetime`, когда профиль есть; **`null`**, когда профиля нет — D-CAB-2. Без обращения к Supabase Auth.
- Политика **no-auto-provision** сохранена: `/me` ничего не пишет; при отсутствии профиля `created_at=null`, `account_status="active"`.
- Синхронизировать API-доки: [`api-reference/openapi.yaml`](../../../../../runtime-docs/api-reference/openapi.yaml) (`MeData`) + [`API_REFERENCE.md §6`](../../../../../runtime-docs/api-reference/API_REFERENCE.md) — `created_at` nullable, `account_status` enum с пометкой «MVP эмитит только `active`».

## Подзадачи
- **T01 — `me_response.py`.** В базовый dict `build_me_data` добавить `data["account_status"] = "active"` и `data["created_at"] = None`; в блок `if profile is not None:` — `data["created_at"] = _format_datetime(profile.created_at)`. (`email`/`email_verified` не трогать — ONB-01.)
- **T02 — API-доки.** `openapi.yaml` `MeData`: `created_at` (`[string,"null"]`, date-time), `account_status` (enum, описание «MVP: всегда `active`»). `API_REFERENCE.md §6` — те же поля в примере `/me`.
- **T03 — Тесты (`test_me_profile.py`).** С профилем → `created_at` = ISO из `profile.created_at`; без профиля → `created_at=null`; `account_status=="active"` в обоих случаях. Полная offline-сюита зелёная.
- **T04 — (опц., spa-сторона; вне identity pkg).** §0-пометка в [`CAB-api-requirements §0`](../../../../../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-api-requirements.md) — MVP эмитит `account_status="active"` и `created_at` может быть `null` (new-user placeholder). Согласовать отдельно в spa.

## Вне scope
- **role-маппинг** (`authenticated` vs `authenticated_user`) — это **FE** ([CAB-02 §Нюанс](../../../../../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-02-account-summary-block.md)), не identity.
- Отдельный account/aggregate-endpoint — CAB-02 решил extend `/me`, не новый роут.
- Gateway-контракты (`GET /story-activity`, `/story-drafts/current`, `/contribution/*`) — **не identity** (не трогаем).
- **Wallet** (`wallet_*`) и **Reputation** — 🚫 POST-MVP.
- Backlog T04 (spa CAB-api note) — вне identity pkg-000044.

## Acceptance Criteria
- [x] `GET /me` `data.account_status == "active"` (всегда, включая no-profile). (`email` — приёмка в [ONB-01](../../../../backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md).)
- [x] `data.created_at` = ISO-8601 из `profiles.created_at` при наличии профиля; `null` — без профиля. **Никаких обращений к Supabase Auth** и **никакой записи в БД** (no-auto-provision сохранён).
- [x] Нет новой миграции/колонки (D-CAB-1): `grep account_status supabase/bootstrap/` → пусто.
- [x] `openapi.yaml` `MeData` + `API_REFERENCE.md §6` обновлены (created_at nullable, account_status enum + пометка «MVP: active»).
- [x] `test_me_profile.py` покрывает оба кейса (профиль/без); полная offline-сюита зелёная.

## Швы
[`me_response.py`](../../../../../../src/core/api/me_response.py) (билдер `data` — единственная точка правки кода), [`models.py`](../../../../../../src/core/domain/models.py) (`ProfileRecord.created_at` — уже есть); доки — [`api-reference/`](../../../../../runtime-docs/api-reference/); тесты — `tests/test_me_profile.py`. **Миграции нет** (D-CAB-1).

## Парадигма-якорь
[`AUTHCORE-01`](../STORY-IDS-AUTHCORE-01-profile-and-me/STORY-IDS-AUTHCORE-01-profile-and-me.md) (тот же `/me`), [`api-reference/API_REFERENCE.md`](../../../../../runtime-docs/api-reference/API_REFERENCE.md), контракт [`CAB-api-requirements`](../../../../../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-api-requirements.md).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-07-02-t01-me-response-created-at-account-status`](./task-ids-07-02-t01-me-response-created-at-account-status/README.md) | pkg-000044 |
| 2 | [`task-ids-07-02-t02-me-api-docs-created-at-account-status`](./task-ids-07-02-t02-me-api-docs-created-at-account-status/README.md) | pkg-000044 |
| 3 | [`task-ids-07-02-t03-me-profile-offline-tests-account-fields`](./task-ids-07-02-t03-me-profile-offline-tests-account-fields/README.md) | pkg-000044 |
| 4 | [`task-ids-07-02-t04-story-acceptance-verification`](./task-ids-07-02-t04-story-acceptance-verification/README.md) | pkg-000044 |
| 5 | [`task-ids-07-02-t05-audit-g3-created-at-semantics-docs`](./task-ids-07-02-t05-audit-g3-created-at-semantics-docs/README.md) | override `epic_ids_07_authcore_02_audit_2026_07_24` |
