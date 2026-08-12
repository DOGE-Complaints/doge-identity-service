## Task workspace — `task-ids-09-06-t05-spa-first-runtime-docs`

- Story: [`../STORY-IDS-EID-06-browser-callback-redirect.md`](../STORY-IDS-EID-06-browser-callback-redirect.md)
- Prerequisite: t01–t04 (implemented behavior to document)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000019`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md`](../../../../../../backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md) Scope #6; [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F11)  
---

## Task: implement — SPA-first redirect model in runtime docs

### Цель
Зафиксировать в runtime-docs web-SPA модель callback: full-page redirect → `GET /auth/{provider}/callback` → `303` back to SPA с query-маркерами; обновить устаревшие секции про `return_url` и callback routing.

### Почему это важно
Audit F11: операторы и UI-команда должны видеть контракт redirect, не JSON callback. Устаревший текст в `08-ui-expectations` вводит в заблуждение (allowlist уже enforced).

### Факты из кода
1. [`06-eid-providers.md`](../../../../../../../runtime-docs/06-eid-providers.md) — provider/callback sections (post EID-05 reconcile).
2. [`08-ui-expectations.md`](../../../../../../../runtime-docs/08-ui-expectations.md) — §3 помечает allowlist как «не валидируется» — противоречит [`handlers.py:123-140`](../../../../../../../src/core/api/handlers.py).
3. [`01-api.md`](../../../../../../../runtime-docs/01-api.md) — endpoint contracts (may reference hardcoded callback paths).
4. Story Scope #6: SPA-first; RN recommendations deferred until RN client exists.

### Gap / Проблема
Доки не описывают redirect-модель и динамический `/auth/{provider}/callback`; `08-ui-expectations` stale про allowlist.

### AC/DoD
- [x] (P0) `06-eid-providers.md`: callback flow = browser redirect to dynamic route → 303 to `return_url` with `eid_status` / `eid_error` markers; `Accept: application/json` for tests noted.
- [x] (P0) `08-ui-expectations.md`: SPA-first model (start → provider → callback → 303 back); §3 allowlist status corrected to ✅ (enforced on `/auth/eid/start`).
- [x] (P1) `01-api.md` callback path references aligned to `/auth/{provider}/callback` if present.
- [x] (P1) Story AC #6 (docs part) traceability.
- [x] (P1) No RN/mobile UA guidance unless explicitly deferred per backlog Scope.

### Где менять код
- `doge-identity-service/docs/runtime-docs/06-eid-providers.md`
- `doge-identity-service/docs/runtime-docs/08-ui-expectations.md`
- `doge-identity-service/docs/runtime-docs/01-api.md` (if callback paths mentioned)

### Out of scope
- spa-app UI implementation (other repo)
- Backlog file sync — t06 optional at story close
- EID-02 provider-specific callback docs

### Проверка
```bash
cd doge-identity-service
rg -n "eid_status|/auth/\\{provider\\}/callback|303" docs/runtime-docs/06-eid-providers.md docs/runtime-docs/08-ui-expectations.md
rg -n "ALLOWED_RETURN_URLS|validate_return_url" docs/runtime-docs/08-ui-expectations.md
```
