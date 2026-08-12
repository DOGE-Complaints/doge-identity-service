## Task workspace — `task-ids-08-02-t01-owner-decisions-placeholders-e17-e22`

- Story: [`../STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../STORY-IDS-CLEANUP-02-placeholders-hardening.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-02-placeholders-hardening.md) Meta «разобрать по одному»; Scope E17–E22

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000013`  
**Skill declared:** python-pro  
---

## Task: analyze — owner decisions for E17–E22 placeholders

### Цель
Зафиксировать решение владельца по каждому Scope-пункту (оставить / довести / убрать) до начала реализации в t02–t06.

### Почему это важно
Story AC #1 и Meta backlog: «разобрать по одному» — без явных решений t02–t06 могут принять противоречивые трактовки (особенно E17 «довести vs убрать», E22 «наполнить vs убрать» при «Вне scope: функциональные реализации»).

### Факты из кода
1. E17 — [`schema.py:57,169`](../../../../../../../src/core/config/schema.py): `allowed_return_urls` в `AppConfig`; validation call sites в `src/` отсутствуют.
2. E18 — [`security.py:22-31`](../../../../../../../src/core/api/security.py): `StubBearerTokenAuth`; prod DI → `SupabaseJwtBearerTokenAuth`; тесты: `tests/test_security_primitives.py`, `tests/test_api_dependencies.py`, `tests/test_service_factory.py`.
3. E20 — [`schema.py:37,123,149`](../../../../../../../src/core/config/schema.py): `code_verifier_encryption_key` pilot-required; encryption usage в `src/` отсутствует.
4. E21 — [`idempotency.py:6`](../../../../../../../src/core/api/idempotency.py): `resolve_idempotency_key`; wiring в routes отсутствует; tests в `tests/test_api_envelope.py`.
5. E22 — [`core/audit/__init__.py`](../../../../../../../src/core/audit/__init__.py), [`core/oauth/__init__.py`](../../../../../../../src/core/oauth/__init__.py), [`core/profiles/__init__.py`](../../../../../../../src/core/profiles/__init__.py): docstring-only; import sites в `src/` отсутствуют.

### Gap / Проблема
Пять независимых placeholder-решений без зафиксированного owner choice блокируют атомарную реализацию t02–t06.

### AC/DoD
- [ ] (P0) Story AC #1 (partial): артефакт `owner-decisions-e17-e22.md` в этой папке с 5 строками (E17–E22 → decision + rationale).
- [ ] (P0) Каждое решение — одно из: **оставить** (placeholder), **довести** (implement), **убрать** (remove).
- [ ] (P1) t02–t06 README ссылаются на соответствующую строку decision-артефакта.

### Где менять код
- Task-артефакт в этой папке (P3):
  - `owner-decisions-e17-e22.md`

### Out of scope
- Изменения в `src/` или `tests/` — t02–t06
- Runtime-docs sync — CLEANUP-03

### Проверка
```bash
test -f doge-identity-service/docs/tasks/epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/owner-decisions-e17-e22.md
wc -l doge-identity-service/docs/tasks/epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/owner-decisions-e17-e22.md
```
