# STORY-IDS-CLEANUP-02 — Чистка заготовок и хардненинг

## Meta
- **Key:** `STORY-IDS-CLEANUP-02-placeholders-hardening`
- **Epic:** `EPIC-IDS-CLEANUP` (новый, см. [EPIC-IDS-CLEANUP.md](EPIC-IDS-CLEANUP.md))
- **Status:** 🟢 Done
- **Источник:** backlog [`identity-todo-backlog-2026-06-04`](../../../analysis/identity-todo-backlog-2026-06-04.md) — E17, E18, E20, E21, E22; gap §10 (P2/P3/P5/P6), SEC-3/SEC-4
- **Зависит от:** — (после CLEANUP-01 желательно, но не обязательно)
- **Примечание:** часть пунктов в gap §10 помечена «разобрать по одному» — перед удалением свериться с владельцем (оставить/убрать).

## Зачем простыми словами
В коде накопились «заготовки без поведения» — поля и хелперы, которые либо нужно довести до дела, либо честно убрать, чтобы не вводить в заблуждение и не оставлять дыр (например, `ALLOWED_RETURN_URLS` читается, но не проверяется — это потенциальный open-redirect).

## Scope (по пунктам, каждый — решение оставить/довести/убрать)
- **E17 `ALLOWED_RETURN_URLS`** — либо реализовать валидацию `return_url` по белому списку (закрыть open-redirect), либо убрать настройку. Точка: [`schema.py:169`](../../../../src/core/config/schema.py).
- **E18 `StubBearerTokenAuth`** — удалить неиспользуемый класс ([`security.py:22-31`](../../../../src/core/api/security.py)).
- **E20 `CODE_VERIFIER_ENCRYPTION_KEY`** — либо реально шифровать `code_verifier`, либо убрать секрет/требование ([`schema.py:149`](../../../../src/core/config/schema.py)).
- **E21 idempotency-резолвер** — подключить к POST-операциям или убрать ([`idempotency.py`](../../../../src/core/api/idempotency.py)).
- **E22 пустые пакеты** `core.audit`, `core.oauth`, `core.profiles` — наполнить по мере эпиков или убрать.

## Вне scope
- web3 wallet-колонки (P1) — отдельное post-MVP-решение, не входит сюда.
- Функциональные реализации (audit/oauth наполняются своими эпиками).

## Acceptance Criteria
- [x] По каждому пункту зафиксировано решение владельца (оставить/довести/убрать) и оно выполнено.
- [x] Если `ALLOWED_RETURN_URLS` остаётся — `return_url` валидируется, есть тест на отклонение чужого домена.
- [x] Удалённые заготовки: grep по их идентификаторам = 0.
- [x] Offline-набор зелёный.

## Парадигма-якорь
[08-ui-expectations](../../../runtime-docs/08-ui-expectations.md) (return_url), [04-security](../../../runtime-docs/04-security.md), gap §10.
