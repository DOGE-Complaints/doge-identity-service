## Task workspace — `task-ids-11-01-t09-audit-f2-epic-oauth-backlog-index-sync`

- Story: [`../STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../STORY-IDS-OAUTH-01-oauth-server-endpoints.md)
- Audit source: [`../../../../../../analysis/epic-ids-11-oauth-01-audit-2026-06-24.md`](../../../../../../analysis/epic-ids-11-oauth-01-audit-2026-06-24.md) (F2)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_11_oauth_01_audit_2026_06_24`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-11-oauth-01-audit-2026-06-24.md`](../../../../../../analysis/epic-ids-11-oauth-01-audit-2026-06-24.md) §F2  
---

## Task: fix — EPIC-IDS-OAUTH backlog index sync (F2)

### Цель
Привести backlog alias-эпик [`EPIC-IDS-OAUTH.md`](../../../../../../backlog-stories/oauth/EPIC-IDS-OAUTH.md) в соответствие с фактом: OAUTH-01 🟢 Done (роуты подключены, не 501).

### Почему это важно
`EPIC-IDS-OAUTH.md` — пакетный индекс backlog-стори; устаревшие «501» и `⚪ Todo` для OAUTH-01 блокируют корректный intake OAUTH-02/03/04.

### Факты из кода
1. [`EPIC-IDS-OAUTH.md:8`](../../../../../../backlog-stories/oauth/EPIC-IDS-OAUTH.md) — «роуты `/oauth/*` — заглушки 501».
2. [`...:17`](../../../../../../backlog-stories/oauth/EPIC-IDS-OAUTH.md) — OAUTH-01 row `⚪ Todo`.
3. [`...:22`](../../../../../../backlog-stories/oauth/EPIC-IDS-OAUTH.md) — статус-строка «OAUTH-01..04 = 501 / не построено».
4. [`...:29`](../../../../../../backlog-stories/oauth/EPIC-IDS-OAUTH.md) — порядок «OAUTH-01 (снять 501)» устарел.
5. Pipeline: [`EPIC-IDS-11-oauth-server.md`](../../../../EPIC-IDS-11-oauth-server.md) Story 1 🟢 Done.

### Gap / Проблема
Doc-stale в backlog alias epic; расхождение с pipeline EPIC-IDS-11 (audit F2 MEDIUM).

### AC/DoD
- [x] (P0) Таблица состава: OAUTH-01 → 🟢 Done (+ ссылка на pipeline story).
- [x] (P0) Снять «501» из «Назначение» для факта OAUTH-01 (OAUTH-02..04 остаются ⚪ Todo).
- [x] (P0) Статус-строка: OAUTH-01 построен; OAUTH-02..04 — ⚪ Todo (не «все 501»).
- [x] (P1) Порядок реализации: OAUTH-01 ✅ → OAUTH-03 → OAUTH-02 → OAUTH-04 (без «снять 501» для OAUTH-01).

### Где менять код
- `doge-identity-service/docs/tasks/backlog-stories/oauth/EPIC-IDS-OAUTH.md`

### Out of scope
- Код, pytest, runtime-docs (t10).
- Изменение AC/Scope соседних backlog-стори OAUTH-02..04.
- `identity-active-package.current.yaml`, pkg-000029 yaml.

### Проверка
```bash
grep -n "OAUTH-01\|501\|Todo\|Done" \
  doge-identity-service/docs/tasks/backlog-stories/oauth/EPIC-IDS-OAUTH.md
```
