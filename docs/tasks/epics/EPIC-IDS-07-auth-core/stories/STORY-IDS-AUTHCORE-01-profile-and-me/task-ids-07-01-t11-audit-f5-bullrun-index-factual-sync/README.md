## Task workspace — `task-ids-07-01-t11-audit-f5-bullrun-index-factual-sync`

- Story: [`../STORY-IDS-AUTHCORE-01-profile-and-me.md`](../STORY-IDS-AUTHCORE-01-profile-and-me.md)
- Audit source: [`../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md) (F5)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000010`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md) §F5  
---

## Task: fix — bullrun index and epic doc factual sync (F5)

### Цель
Синхронизировать [`bullrun-launch-index.md`](../../../../../../bullrun-launch-index.md) и [`EPIC-IDS-07-auth-core.md`](../../../../EPIC-IDS-07-auth-core.md) с фактическим состоянием pytest и runtime `/me` (после закрытия F1 — зелёная сюита; до F1 — явная оговорка).

### Почему это важно
Индекс строка 11 заявляет «200 pytest offline, 199 passed» при P3 Done — вводит в заблуждение, если F1 ещё открыт. Epic file §1–§6 всё ещё описывает stub 501.

### Факты из кода
1. [`bullrun-launch-index.md:11`](../../../../../../bullrun-launch-index.md) — «P3 Execute Done» + «199 passed» без явного open gap F1 до scaffold wave.
2. [`EPIC-IDS-07-auth-core.md:3,12`](../../../../EPIC-IDS-07-auth-core.md) — «⚪ Todo», «заглушка 501».
3. [`EPIC-IDS-07-auth-core.md:59-64`](../../../../EPIC-IDS-07-auth-core.md) — AC story [ ] unchecked в epic file.
4. Факт runtime: `handle_me` wired — [`asgi_app.py:166`](../../../../../../../src/core/api/asgi_app.py).

### Gap / Проблема
Index-vs-факт и epic doc-stale после AUTHCORE-01 Done.

### AC/DoD
- [x] (P0) «Актуальная точка» отражает: story Done, gap wave pkg-000010 (F1–F6), pytest count согласован с фактом **после** t07 или с пометкой «1 known fail F1» до t07.
- [x] (P0) Epic file §1/§5/§6: `/me` реализован; story 1 AC [x] или ссылка на pipeline story Done.
- [x] (P0) Epic registry: EPIC-IDS-07 — post-audit gap wave scaffolded / in progress (согласовано с gap queue).
- [x] (P1) Не менять immutable pkg-000009 YAML.

### Где менять код
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-07-auth-core/EPIC-IDS-07-auth-core.md`

### Out of scope
- Переключение `identity-active-package.current.yaml` (P1 отдельно).
- Исправление F1 в коде (t07).

### Проверка
```bash
grep -n "501\|199 passed\|P3 Execute\|AUTHCORE" doge-identity-service/docs/tasks/bullrun-launch-index.md
grep -n "501\|stub\|Acceptance" doge-identity-service/docs/tasks/epics/EPIC-IDS-07-auth-core/EPIC-IDS-07-auth-core.md
```
