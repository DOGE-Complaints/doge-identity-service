## Task workspace — `task-ids-07-01-t01-missing-profile-behavior-decision`

- Story: [`../STORY-IDS-AUTHCORE-01-profile-and-me.md`](../STORY-IDS-AUTHCORE-01-profile-and-me.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-AUTHCORE-01-profile-and-me.md`](../../../../../../backlog-stories/STORY-IDS-AUTHCORE-01-profile-and-me.md) Scope п.4

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000009`  
**Skill declared:** python-pro  
---

## Task: fix — missing profile behavior decision

### Цель
Зафиксировать детерминированное поведение `GET /me`, когда `ProfileRepository.get_by_supabase_user_id` возвращает `None` (один из вариантов Scope: «создать пустой» / «вернуть не верифицирован»).

### Почему это важно
Story AC #3 требует детерминизм и тест; без явного решения t02–t05 разойдутся в ожиданиях. Gateway позже читает `eid_verified` ([`09-gateway-expectations.md`](../../../../../../../runtime-docs/09-gateway-expectations.md)).

### Факты из кода
1. [`repositories.py:61-62`](../../../../../../../src/core/infrastructure/repositories.py) — InMemory `get_by_supabase_user_id` → `None`, если записи нет.
2. [`db_supabase.py:386-394`](../../../../../../../src/core/infrastructure/db_supabase.py) — Supabase repo аналогично.
3. [`attach_eid_verification`](../../../../../../../src/core/infrastructure/repositories.py) создаёт профиль при eID — **вне scope** этой story.
4. Story Scope п.4 — два допустимых варианта; выбор за исполнителем в P3.

### Gap / Проблема
Поведение при отсутствии профиля не задокументировано в runtime; AC #3 не закрыт.

### Решение

**Вариант B:** `GET /me` при отсутствии профиля → **200**, синтетический payload (`eid_verified=false`, поля профиля `null`), **без** upsert. См. [`BULLRUN-PHASE-LOG.md`](./BULLRUN-PHASE-LOG.md).

### AC/DoD
- [x] (P0) В BULLRUN-PHASE-LOG и в этом README (секция «Решение») зафиксирован **один** выбранный вариант с обоснованием (детерминизм, без лишних side-effect, совместимость с `eid_verified` для gateway).
- [x] (P0) Решение не меняет формулировки AC story; prerequisite для t02–t05.
- [x] (P1) Ссылка на [`09-gateway-expectations.md`](../../../../../../../runtime-docs/09-gateway-expectations.md) в обосновании.

### Где менять код
- Task-артефакты: `BULLRUN-PHASE-LOG.md` в этой папке; опционально однострочный комментарий в t02 handler (после выбора).
- **Без** изменения backlog story.

### Out of scope
- Реализация `handle_me` — t02+
- eID attach / upsert в eID-флоу — STORY-IDS-EID-01

### План выполнения
1. Сравнить варианты Scope п.4 с фактами repos (read-only vs upsert).
2. Записать решение в BULLRUN + README «Решение».
3. Передать выбор в t02/t05.

### Проверка
```bash
# Артефакт: grep решения в task folder
grep -n "Решение\|Decision" doge-identity-service/docs/tasks/epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t01-missing-profile-behavior-decision/README.md
```
