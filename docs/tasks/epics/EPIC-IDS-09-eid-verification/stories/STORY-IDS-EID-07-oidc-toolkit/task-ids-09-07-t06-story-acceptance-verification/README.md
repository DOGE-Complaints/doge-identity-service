## Task workspace — `task-ids-09-07-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-EID-07-oidc-toolkit.md`](../STORY-IDS-EID-07-oidc-toolkit.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000020`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/STORY-IDS-EID-07-oidc-toolkit.md`](../../../../../../backlog-stories/STORY-IDS-EID-07-oidc-toolkit.md); [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F8)  
---

## Task: verify — STORY-IDS-EID-07 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim: provider-agnostic `core/security/oidc/` module, discovery/JWKS cache + kid refresh, RS256+claims validator with `IDENTITY_VALIDATION_FAILED`, toolkit via `ProviderRuntime`, offline mocked tests green.

### Почему это важно
EID-07 разблокирует EID-02 (Authentigate OIDC capstone) per [`EPIC-IDS-EID.md`](../../../../../../backlog-stories/EPIC-IDS-EID.md) dependency graph.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-EID-07-oidc-toolkit.md`](../STORY-IDS-EID-07-oidc-toolkit.md) (5 checkboxes verbatim).
2. Tasks t01–t05 — implementation + offline tests.
3. Backlog SSOT — [`STORY-IDS-EID-07-oidc-toolkit.md`](../../../../../../backlog-stories/STORY-IDS-EID-07-oidc-toolkit.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [x] (P0) Story AC #1: `OidcDiscoveryClient`, `JwksCache`, `IdTokenValidator` in `core/security/oidc/` — evidence t01–t03.
- [x] (P0) Story AC #2: discovery/JWKS cached; unknown `kid` refresh — evidence t01/t02/t05.
- [x] (P0) Story AC #3: RS256 + `iss/aud/exp/iat/nonce`; invalid → `IDENTITY_VALIDATION_FAILED` — evidence t03/t05.
- [x] (P0) Story AC #4: toolkit via `ProviderRuntime` — evidence t04/t05.
- [x] (P0) Story AC #5: mocked tests, offline green — evidence t05.
- [x] (P1) `acceptance-verification-task-ids-09-07-t06-story-acceptance-verification.md` создан.
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; bullrun sync (same iteration).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-07-oidc-toolkit/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/bullrun-launch-index.md` (story/task statuses)

### Out of scope
- Backlog file status sync (optional post-audit)
- Epic AC gate EPIC-IDS-09 (отдельная операция)
- EID-02 Authentigate adapter
- EID-08 SessionSecretBox

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
```
