# EPIC-IDS-AUTH-CORE — Профиль, `/me`, базовые права

> **ID:** `EPIC-IDS-AUTH-CORE` (назван в коде через `next_epic` в [`handlers.py`](../../../../src/core/api/handlers.py)) · **Статус:** 🟢 Done (AUTHCORE-01) · **Тип:** Функциональный
> **Не декомпозирован** в pipeline-эпик — backlog-стори (реализована под pipeline [`EPIC-IDS-07-auth-core`](../../epics/EPIC-IDS-07-auth-core/EPIC-IDS-07-auth-core.md)).
> **Тематический индекс** (стори остаются в руте backlog-stories — на них ссылаются 28+ файлов; физически не перемещаются).

## Назначение
Базовый защищённый маршрут идентичности: `GET /me` — профиль пользователя по Supabase JWT, источник `eid_verified`/`phone_verified`/`role`, на которых держатся OAuth-валидация (OAUTH-02 introspection) и потребительские гейты.

## Состав
| Story | Тема | Слой | Статус |
|-------|------|------|--------|
| [STORY-IDS-AUTHCORE-01](STORY-IDS-AUTHCORE-01-profile-and-me.md) | профиль и `/me` (Bearer Supabase JWT) | API/данные | 🟢 Done (pkg-000009) |

## Связь
Фундамент для [`EPIC-IDS-OAUTH`](../oauth/EPIC-IDS-OAUTH.md) (даёт `eid_verified`) и [`EPIC-IDS-ONBOARDING`](../identity-onboarding/EPIC-IDS-ONBOARDING.md) (`/me` для гейтов). Парадигма: [`04-security`](../../../runtime-docs/04-security.md), [`08-ui-expectations`](../../../runtime-docs/08-ui-expectations.md).
