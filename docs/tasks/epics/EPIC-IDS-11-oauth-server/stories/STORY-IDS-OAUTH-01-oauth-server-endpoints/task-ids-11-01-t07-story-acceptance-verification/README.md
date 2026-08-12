## Task workspace — `task-ids-11-01-t07-story-acceptance-verification`

- Story: [`../STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../STORY-IDS-OAUTH-01-oauth-server-endpoints.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000029`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md); [`story-acceptance-gate-template.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-OAUTH-01 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim (8 checkboxes): authorize/complete/token flow, PKCE, client_secret, validations, authorization_request handshake, RFC errors, offline tests.

### Почему это важно
Story gate для pkg-000029; разблокирует OAUTH-03/02/04 в backlog.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../STORY-IDS-OAUTH-01-oauth-server-endpoints.md) (8 checkboxes verbatim).
2. Tasks t01–t06 — implementation + tests.
3. Backlog SSOT — [`STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [x] (P0) Story AC #1: authorize → code bound to `supabase_user_id` — evidence t04/t06.
- [x] (P0) Story AC #2: token exchange + `invalid_grant` — evidence t02, t04, t06.
- [x] (P0) Story AC #3: `client_secret` rejection — evidence t02, t06.
- [x] (P0) Story AC #4: PKCE `code_verifier` — evidence t04, t06.
- [x] (P0) Story AC #5: authorize validations + `state` — evidence t03, t06.
- [x] (P0) Story AC #6: authorization_request handshake — evidence t01, t03, t04, t06.
- [x] (P0) Story AC #7: RFC 6749 + scope model — evidence t02, t06.
- [x] (P0) Story AC #8: offline tests green — evidence t06.
- [x] (P1) `acceptance-verification-task-ids-11-01-t07-story-acceptance-verification.md` создан с PASS.
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; epic Story 1; bullrun sync (same iteration).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-01-oauth-server-endpoints/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-11-oauth-server/EPIC-IDS-11-oauth-server.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`

### Out of scope
- Backlog file AC/Scope edits
- OAUTH-02/03/04 implementation
- pkg-000028 mutation (immutable)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
```
