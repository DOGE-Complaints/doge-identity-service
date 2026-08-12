## Task workspace — `task-ids-08-03-t04-req02-req03-gateway-direction-sync`

- Story: [`../STORY-IDS-CLEANUP-03-doc-drift.md`](../STORY-IDS-CLEANUP-03-doc-drift.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-03-doc-drift.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-03-doc-drift.md) Scope req-02/03; [`../../../../../../runtime-docs/09-gateway-expectations.md`](../../../../../../runtime-docs/09-gateway-expectations.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000014`  
**Skill declared:** python-pro  
---

## Task: fix/docs — req-02/03 gateway direction sync

### Цель
Сверить упоминание направления identity↔gateway в req-02/req-03 с решённой моделью **gateway→identity** (stories owned by gateway; identity не форвардит).

### Почему это важно
Story AC #3 (partial); устаревшая модель «identity принимает story / форвардит в gateway» блокирует корректное планирование функциональных эпиков.

### Факты из кода
1. [`req-02:18-19`](../../../../../../../docs/requirements/02-scope-and-boundaries.md) — Story authorization gate + Story drafts rows in MVP scope table.
2. [`req-03:39`](../../../../../../../docs/requirements/03-architecture-formula.md) — `/stories`, `/story-drafts`, `/gpt/actions/submit-story` listed under identity Layer 3.
3. [`req-03:78-115`](../../../../../../../docs/requirements/03-architecture-formula.md) — Flow B describes identity story submission → POST gateway `/intake/stories`.
4. [`09-gateway-expectations.md:37-38`](../../../../../../../docs/runtime-docs/09-gateway-expectations.md) — gateway-direct model; identity story routes misplaced/removed.
5. `grep story-drafts src/core/api/asgi_app.py` = **0** (post CLEANUP-01).

### Gap / Проблема
Requirements still describe identity as story pipeline owner / forwarder; resolved model is gateway→identity for auth only.

### AC/DoD
- [x] (P0) Story AC #3: req-02 MVP scope rows adjusted — story creation/drafts **не** в identity MVP scope (gateway domain).
- [x] (P0) Story AC #3: req-03 Layer 3 + Flow B aligned — gateway-direct intake; identity provides OAuth/eID, not story HTTP pipeline.
- [x] (P1) Cross-ref [`09-gateway-expectations.md`](../../../../../../../docs/runtime-docs/09-gateway-expectations.md) where appropriate.
- [x] (P1) BULLRUN-PHASE-LOG + acceptance-verification в этой папке (P3).

### Где менять код
- [`docs/requirements/02-scope-and-boundaries.md`](../../../../../../../docs/requirements/02-scope-and-boundaries.md) — MVP scope table (story rows)
- [`docs/requirements/03-architecture-formula.md`](../../../../../../../docs/requirements/03-architecture-formula.md) — Layer 3 bullet list, Flow B

### Out of scope
- Functional gateway/identity code changes
- req-15 body rewrite (t03)
- runtime-docs full sync (t05)

### Проверка
```bash
cd doge-identity-service
grep -n "story-drafts\|submit-story\|/stories" docs/requirements/02-scope-and-boundaries.md docs/requirements/03-architecture-formula.md
grep -n "gateway" docs/requirements/03-architecture-formula.md | head -20
```
