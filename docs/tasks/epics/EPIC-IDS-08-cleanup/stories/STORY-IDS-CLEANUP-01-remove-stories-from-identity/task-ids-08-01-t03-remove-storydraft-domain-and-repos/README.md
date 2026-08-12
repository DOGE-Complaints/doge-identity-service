## Task workspace — `task-ids-08-01-t03-remove-storydraft-domain-and-repos`

- Story: [`../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md) Scope п.3

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000011`  
**Skill declared:** python-pro  
---

## Task: refactor — remove StoryDraft domain and repositories

### Цель
Удалить `StoryDraft`-модель, протокол `StoryDraftRepository`, InMemory/Supabase реализации, mappers и слоты в фабрике/DI/providers.

### Почему это важно
Наследие story-домена в identity мешает чистой базе для AUTH-CORE/EID/OAUTH. Story AC #2 (grep clean).

### Факты из кода
1. [`models.py:96`](../../../../../../../src/core/domain/models.py) — класс `StoryDraft`.
2. [`contracts.py:103-106`](../../../../../../../src/core/domain/contracts.py) — `StoryDraftRepository` protocol.
3. [`domain/__init__.py`](../../../../../../../src/core/domain/__init__.py) — экспорт `StoryDraft`, `StoryDraftRepository`.
4. [`repositories.py:349-365`](../../../../../../../src/core/infrastructure/repositories.py) — `InMemoryStoryDraftRepository`.
5. [`db_supabase.py:211-227,622-651`](../../../../../../../src/core/infrastructure/db_supabase.py) — Supabase repo + mappers.
6. [`dependencies.py:51`](../../../../../../../src/core/api/dependencies.py), [`service_factory.py`](../../../../../../../src/core/infrastructure/service_factory.py), [`providers.py`](../../../../../../../src/core/infrastructure/providers.py) — DI wiring.

### Gap / Проблема
StoryDraft и репозитории остаются в кодовой базе identity после решения 2026-06-04 о выносе stories в gateway.

### AC/DoD
- [x] (P0) Удалены `StoryDraft` из `models.py` и экспортов `domain/__init__.py`.
- [x] (P0) Удалён `StoryDraftRepository` из `contracts.py` и экспортов.
- [x] (P0) Удалены InMemory и Supabase реализации + mappers.
- [x] (P0) Удалены слоты story_draft из `dependencies.py`, `service_factory.py`, `providers.py`, `application/factory.py` (если есть).
- [x] (P0) Story AC #2: grep `StoryDraft|story_draft` в `src/` = 0 (кроме migration exempt).

### Где менять код
- [`src/core/domain/models.py`](../../../../../../../src/core/domain/models.py)
- [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py)
- [`src/core/domain/__init__.py`](../../../../../../../src/core/domain/__init__.py)
- [`src/core/infrastructure/repositories.py`](../../../../../../../src/core/infrastructure/repositories.py)
- [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py)
- [`src/core/api/dependencies.py`](../../../../../../../src/core/api/dependencies.py)
- [`src/core/infrastructure/service_factory.py`](../../../../../../../src/core/infrastructure/service_factory.py)
- [`src/core/infrastructure/providers.py`](../../../../../../../src/core/infrastructure/providers.py)

### Out of scope
- Пакет `core.stories` — t04
- Тесты — t06

### Проверка
```bash
cd doge-identity-service
rg "StoryDraft|story_draft" src --glob '!*migrations*'
# ожидание: 0 matches
```
