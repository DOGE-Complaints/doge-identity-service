## Task workspace — `task-ids-11-02-t07-audit-f2-epic-oauth-backlog-index-sync`

- Story: [`../STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../STORY-IDS-OAUTH-02-introspection-and-service-token.md)
- Audit source: [`../../../../../../analysis/epic-ids-11-oauth-02-audit-2026-06-24.md`](../../../../../../analysis/epic-ids-11-oauth-02-audit-2026-06-24.md) (F2)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_11_oauth_02_audit_2026_06_24`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-11-oauth-02-audit-2026-06-24.md`](../../../../../../analysis/epic-ids-11-oauth-02-audit-2026-06-24.md) §F2  
---

## Task: fix — EPIC-IDS-OAUTH backlog index sync (F2)

### Цель
Привести backlog alias-эпик [`EPIC-IDS-OAUTH.md`](../../../../../../backlog-stories/oauth/EPIC-IDS-OAUTH.md) в соответствие с фактом: OAUTH-02 🟢 Done (introspection + service token, pkg-000030).

### Почему это важно
`EPIC-IDS-OAUTH.md` — пакетный индекс backlog-стори; устаревший `⚪ Todo` для OAUTH-02 и статус-строка «introspection не построены» блокируют корректный intake OAUTH-03/04.

### Факты из кода
1. [`EPIC-IDS-OAUTH.md:18`](../../../../../../backlog-stories/oauth/EPIC-IDS-OAUTH.md) — OAUTH-02 row `⚪ Todo`.
2. [`...:22`](../../../../../../backlog-stories/oauth/EPIC-IDS-OAUTH.md) — статус-строка «OAUTH-02..04 — ⚪ Todo (introspection … не построены)».
3. [`...:8`](../../../../../../backlog-stories/oauth/EPIC-IDS-OAUTH.md) — «introspection и durable store — OAUTH-02/03» (OAUTH-02 уже построен).
4. [`...:28-29`](../../../../../../backlog-stories/oauth/EPIC-IDS-OAUTH.md) — порядок «OAUTH-02 (introspection)» без отметки ✅.
5. Pipeline: [`EPIC-IDS-11-oauth-server.md`](../../../../EPIC-IDS-11-oauth-server.md) Story 2 🟢 Done; код: [`asgi_app.py:407-416`](../../../../../../../src/core/api/asgi_app.py), [`introspection.py`](../../../../../../../src/core/oauth/introspection.py).

### Gap / Проблема
Doc-stale в backlog alias epic после OAUTH-02 Done; расхождение с pipeline EPIC-IDS-11 (audit F2 MEDIUM).

### AC/DoD
- [x] (P0) Таблица состава: OAUTH-02 → 🟢 Done (+ ссылка на pipeline story / pkg-000030).
- [x] (P0) Статус-строка: OAUTH-01+02 построены; OAUTH-03..04 — ⚪ Todo (не «introspection не построен»).
- [x] (P0) «Назначение»: снять «introspection — OAUTH-02» как непостроенное; отразить OAUTH-02 ✅.
- [x] (P1) Порядок реализации: OAUTH-01 ✅ → OAUTH-02 ✅ → OAUTH-03 → OAUTH-04.
- [x] (P1) Опц.: backlog OAUTH-02 «Зачем» — убрать «обоих механизмов нет» (narrative drift, не AC).

### Где менять код
- `doge-identity-service/docs/tasks/backlog-stories/oauth/EPIC-IDS-OAUTH.md`

### Out of scope
- runtime-docs (t08), код pilot fail-fast (t09).
- Изменение AC/Scope соседних backlog-стори OAUTH-03..04 (verbatim).
- `identity-active-package.current.yaml`, pkg-000030 yaml.

### Проверка
```bash
grep -n "OAUTH-02\|introspection\|Todo\|Done" \
  doge-identity-service/docs/tasks/backlog-stories/oauth/EPIC-IDS-OAUTH.md
```
