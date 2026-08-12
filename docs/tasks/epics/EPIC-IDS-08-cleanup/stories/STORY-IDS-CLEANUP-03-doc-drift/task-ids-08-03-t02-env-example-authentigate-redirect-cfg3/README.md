## Task workspace — `task-ids-08-03-t02-env-example-authentigate-redirect-cfg3`

- Story: [`../STORY-IDS-CLEANUP-03-doc-drift.md`](../STORY-IDS-CLEANUP-03-doc-drift.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-03-doc-drift.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-03-doc-drift.md) Scope CFG-3; [`../../../../../../analysis/gap-analysis-full-2026-06-04.md`](../../../../../../analysis/gap-analysis-full-2026-06-04.md) CFG-3

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000014`  
**Skill declared:** python-pro  
---

## Task: fix — `.env.example` AUTHENTIGATE_REDIRECT_URI (CFG-3)

### Цель
Исправить `AUTHENTIGATE_REDIRECT_URI` в `.env.example` на существующий callback route.

### Почему это важно
Story AC #2; неверный redirect URI в примере env вводит в заблуждение при локальной настройке OIDC.

### Факты из кода
1. [`.env.example:51`](../../../../../../../.env.example) — `AUTHENTIGATE_REDIRECT_URI=http://localhost:8100/auth/eid/callback`.
2. [`asgi_app.py:209`](../../../../../../../src/core/api/asgi_app.py) — `@app.get("/auth/authentigate/callback")` (exists).
3. [`conftest.py:42-44`](../../../../../../../tests/conftest.py) — `AUTHENTIGATE_REDIRECT_URI=http://localhost:8100/auth/authentigate/callback` (correct pattern).
4. `grep "/auth/eid/callback" src/` — route **не** объявлен в `asgi_app.py`.

### Gap / Проблема
`.env.example` указывает на несуществующий роут `/auth/eid/callback`; фактический callback — `/auth/authentigate/callback`.

### AC/DoD
- [x] (P0) Story AC #2: `.env.example` `AUTHENTIGATE_REDIRECT_URI` → `http://localhost:8100/auth/authentigate/callback` (или эквivalent matching deployed route).
- [x] (P0) Value cross-ref with [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) route table.
- [x] (P1) BULLRUN-PHASE-LOG + acceptance-verification в этой папке (P3).

### Где менять код
- [`.env.example`](../../../../../../../.env.example) — line ~51 `AUTHENTIGATE_REDIRECT_URI`

### Out of scope
- [`07-env-configuration-spec.md`](../../../../../../../docs/requirements/07-env-configuration-spec.md) (not in backlog Scope; t05 may address if AC#4 finds contradiction)
- Runtime code / route renames
- Production URL changes beyond local example consistency

### Проверка
```bash
cd doge-identity-service
grep -n "AUTHENTIGATE_REDIRECT_URI" .env.example
grep -n "authentigate/callback" src/core/api/asgi_app.py
```
