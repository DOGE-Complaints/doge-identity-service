# STORY-IDS-CLEANUP-02 — Чистка заготовок и хардненинг

## Meta
- **Key:** `STORY-IDS-CLEANUP-02-placeholders-hardening`
- **Parent Epic:** [`../../../../EPIC-IDS-08-cleanup.md`](../../../../EPIC-IDS-08-cleanup.md)
- **Epic alias (backlog):** `EPIC-IDS-CLEANUP`
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-02-placeholders-hardening.md)
- **Decision Ref:** [`../../../../backlog-stories/STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-02-placeholders-hardening.md); [`identity-todo-backlog-2026-06-04`](../../../../../analysis/identity-todo-backlog-2026-06-04.md) E17–E22; [`gap-analysis-full-2026-06-04`](../../../../../analysis/gap-analysis-full-2026-06-04.md) §10
- **Источник:** backlog [`identity-todo-backlog-2026-06-04`](../../../../../analysis/identity-todo-backlog-2026-06-04.md) — E17, E18, E20, E21, E22; gap §10 (P2/P3/P5/P6), SEC-3/SEC-4
- **Зависит от:** — (после CLEANUP-01 желательно, но не обязательно)
- **Примечание:** часть пунктов в gap §10 помечена «разобрать по одному» — перед удалением свериться с владельцем (оставить/убрать).

## Зачем простыми словами
В коде накопились «заготовки без поведения» — поля и хелперы, которые либо нужно довести до дела, либо честно убрать, чтобы не вводить в заблуждение и не оставлять дыр (например, `ALLOWED_RETURN_URLS` читается, но не проверяется — это потенциальный open-redirect).

## Scope
- **E17 `ALLOWED_RETURN_URLS`** — либо реализовать валидацию `return_url` по белому списку (закрыть open-redirect), либо убрать настройку. Точка: [`schema.py:169`](../../../../../../src/core/config/schema.py).
- **E18 `StubBearerTokenAuth`** — удалить неиспользуемый класс ([`security.py:22-31`](../../../../../../src/core/api/security.py)).
- **E20 `CODE_VERIFIER_ENCRYPTION_KEY`** — либо реально шифровать `code_verifier`, либо убрать секрет/требование ([`schema.py:149`](../../../../../../src/core/config/schema.py)).
- **E21 idempotency-резолвер** — подключить к POST-операциям или убрать ([`idempotency.py`](../../../../../../src/core/api/idempotency.py)).
- **E22 пустые пакеты** `core.audit`, `core.oauth`, `core.profiles` — наполнить по мере эпиков или убрать.

## Вне scope
- web3 wallet-колонки (P1) — отдельное post-MVP-решение, не входит сюда.
- Функциональные реализации (audit/oauth наполняются своими эпиками).

## Точки в коде (текущее состояние)
- E17: [`schema.py:57,169`](../../../../../../src/core/config/schema.py) — `allowed_return_urls` читается; validation call sites в `src/` отсутствуют.
- E18: [`security.py:22-31`](../../../../../../src/core/api/security.py) — класс есть; prod DI → `SupabaseJwtBearerTokenAuth`; остаётся в `tests/test_security_primitives.py`, `tests/test_api_dependencies.py`, `tests/test_service_factory.py`.
- E20: [`schema.py:37,123,149`](../../../../../../src/core/config/schema.py) — pilot-required; encryption usage в `src/` отсутствует.
- E21: [`idempotency.py:6`](../../../../../../src/core/api/idempotency.py) — `resolve_idempotency_key`; consumer в коде — `tests/test_api_envelope.py`; wiring в `asgi_app`/`handlers` отсутствует.
- E22: [`core/audit/__init__.py`](../../../../../../src/core/audit/__init__.py), [`core/oauth/__init__.py`](../../../../../../src/core/oauth/__init__.py), [`core/profiles/__init__.py`](../../../../../../src/core/profiles/__init__.py) — docstring-only; import sites `core.audit|oauth|profiles` в `src/` отсутствуют.

## Acceptance Criteria
- [x] По каждому пункту зафиксировано решение владельца (оставить/довести/убрать) и оно выполнено.
- [x] Если `ALLOWED_RETURN_URLS` остаётся — `return_url` валидируется, есть тест на отклонение чужого домена.
- [x] Удалённые заготовки: grep по их идентификаторам = 0.
- [x] Offline-набор зелёный.

## Парадигма-якорь
[08-ui-expectations](../../../../../runtime-docs/08-ui-expectations.md) (return_url), [04-security](../../../../../runtime-docs/04-security.md), gap §10.

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-08-02-t01-owner-decisions-placeholders-e17-e22`](./task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/README.md) | pkg-000013 |
| 2 | [`task-ids-08-02-t02-allowed-return-urls-e17`](./task-ids-08-02-t02-allowed-return-urls-e17/README.md) | pkg-000013 |
| 3 | [`task-ids-08-02-t03-remove-stub-bearer-token-auth-e18`](./task-ids-08-02-t03-remove-stub-bearer-token-auth-e18/README.md) | pkg-000013 |
| 4 | [`task-ids-08-02-t04-code-verifier-encryption-key-e20`](./task-ids-08-02-t04-code-verifier-encryption-key-e20/README.md) | pkg-000013 |
| 5 | [`task-ids-08-02-t05-idempotency-resolver-e21`](./task-ids-08-02-t05-idempotency-resolver-e21/README.md) | pkg-000013 |
| 6 | [`task-ids-08-02-t06-empty-layer-packages-e22`](./task-ids-08-02-t06-empty-layer-packages-e22/README.md) | pkg-000013 |
| 7 | [`task-ids-08-02-t07-story-acceptance-verification`](./task-ids-08-02-t07-story-acceptance-verification/README.md) | pkg-000013 |
| 8 | [`task-ids-08-02-t08-audit-f1-return-url-validator-enforcement`](./task-ids-08-02-t08-audit-f1-return-url-validator-enforcement/README.md) | override |
| 9 | [`task-ids-08-02-t09-audit-f2-empty-layer-directories-doc-align`](./task-ids-08-02-t09-audit-f2-empty-layer-directories-doc-align/README.md) | override |
| 10 | [`task-ids-08-02-t10-audit-f3-idempotency-runtime-doc-drift`](./task-ids-08-02-t10-audit-f3-idempotency-runtime-doc-drift/README.md) | override |
