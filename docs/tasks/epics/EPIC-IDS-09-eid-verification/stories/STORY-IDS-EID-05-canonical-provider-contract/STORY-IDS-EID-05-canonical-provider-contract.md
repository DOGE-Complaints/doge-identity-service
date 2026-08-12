# STORY-IDS-EID-05 — Канон контракта provider→core: таксономия ошибок и идентичность субъекта

## Meta
- **Key:** `STORY-IDS-EID-05-canonical-provider-contract`
- **Parent Epic:** [`../../../../EPIC-IDS-09-eid-verification.md`](../../../../EPIC-IDS-09-eid-verification.md)
- **Epic alias (код/backlog):** `EPIC-IDS-EID`
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-EID-05-canonical-provider-contract.md`](../../../../backlog-stories/eid/STORY-IDS-EID-05-canonical-provider-contract.md)
- **Decision Ref:** [`../../../../backlog-stories/STORY-IDS-EID-05-canonical-provider-contract.md`](../../../../backlog-stories/eid/STORY-IDS-EID-05-canonical-provider-contract.md); [`authentigate-compatibility-audit-2026-06-07`](../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F2, F12)
- **Источник:** аудит [`authentigate-compatibility-audit-2026-06-07`](../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F2, F12)
- **Зависит от:** [STORY-IDS-EID-03-provider-plugin-backbone](../STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md)

## Зачем простыми словами
Граница «провайдер → ядро» должна говорить на **одном языке для всех провайдеров**. Сегодня две дыры: (1) коды ошибок провайдера теряются — оркестратор схлопывает любую ошибку в `provider_error`, и «пользователь отменил» неотличимо от «всё сломалось»; (2) если завтра добавим второй провайдер, один и тот же человек посчитается разными личностями (в хэш личности зашито имя провайдера) — анти-Sybil сломается. Чиним обе через канонический контракт: вендор-специфика мапится в канон **в адаптере**, ядро знает только канон.

## Scope
- **`EidErrorCode` (StrEnum, новый в `providers/base.py`):** `USER_CANCELLED`, `STATE_MISMATCH`, `TOKEN_EXCHANGE_FAILED`, `IDENTITY_VALIDATION_FAILED`, `MISSING_REQUIRED_CLAIM`, `COUNTRY_NOT_ALLOWED`, `METHOD_NOT_ALLOWED`, `PROVIDER_UNAVAILABLE`, `UNKNOWN`. Провайдер мапит свои вендор-коды в этот канон и бросает `EIDProviderError(code=EidErrorCode.X)`.
- **Оркестратор различает ошибки:** заменить `except Exception` ([`handlers.py:263-281`](../../../../../../src/core/api/handlers.py)) на `except EIDProviderError as e` → `mark_failed(session.id, e.code)`, audit `failure_reason=e.code`, исход несёт `e.code`; отдельный `except Exception` → `UNKNOWN`/internal без утечки деталей.
- **Каноническая идентичность (F12):** контракт `EIDVerificationResult.subject_hash` = нормализованный стабильный идентификатор **без префикса провайдера**; `verified_person_hash = hash_secret(f"{country}:{subject_hash}", eid_secret)` остаётся ([`handlers.py:283-286`](../../../../../../src/core/api/handlers.py)). Имя провайдера — provenance (уже хранится в `provider` профиля/сессии/аудита), в identity-хэш **не входит**. Зафиксировать правило в доке контракта и в [06-eid-providers](../../../../../runtime-docs/06-eid-providers.md).
- Обновить mock при необходимости (его `subject_hash` уже без провайдер-префикса — проверить).

## Вне scope
- Проброс кода в HTTP-ответ/redirect-маркер — [EID-06](../../../../backlog-stories/eid/STORY-IDS-EID-06-browser-callback-redirect.md) (потребляет `EidErrorCode`).
- Реализация маппинга вендор→канон для Authentigate — [EID-02](../../../../backlog-stories/STORY-IDS-EID-02-real-eid-providers.md).

## Точки в коде (текущее состояние)
- `EIDProviderError` определён, но нигде не обрабатывается специально: [`base.py:24-29`](../../../../../../src/core/providers/base.py); широкий `except`: [`handlers.py:263-281`](../../../../../../src/core/api/handlers.py).
- Формула `verified_person_hash`: [`handlers.py:283-286`](../../../../../../src/core/api/handlers.py).
- `EIDVerificationResult`: [`base.py:8-14`](../../../../../../src/core/providers/base.py); mock subject_hash: [`mock_provider.py:65-71`](../../../../../../src/core/providers/mock/mock_provider.py).
- Аудит: `_log_eid_audit` ([`handlers.py:83-111`](../../../../../../src/core/api/handlers.py)).

## Acceptance Criteria
- [x] Есть `EidErrorCode`; `EIDProviderError` несёт канонический код.
- [x] Оркестратор различает `EIDProviderError` (сохраняет код в `failure_reason`/исход) и неожиданный `Exception` (`UNKNOWN`); `user_cancel` отличим в audit.
- [x] `subject_hash` в контракте не содержит имени провайдера; правило задокументировано; один человек через разные провайдеры даёт одинаковый `verified_person_hash` (юнит-тест на дедупликацию).
- [x] Добавление провайдера не добавляет новых кодов ошибок в ядро.
- [x] Offline-набор зелёный; тесты на маппинг ошибок и кросс-провайдерную дедупликацию.

## Парадигма-якорь
[06-eid-providers](../../../../../runtime-docs/06-eid-providers.md) (контракт), [04-security](../../../../../runtime-docs/04-security.md) (anti-Sybil, PII), [05-data-model](../../../../../runtime-docs/05-data-model.md) (profiles/verified_person_hash).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-09-05-t01-eid-error-code-enum`](./task-ids-09-05-t01-eid-error-code-enum/README.md) | pkg-000018 |
| 2 | [`task-ids-09-05-t02-orchestrator-provider-error-handling`](./task-ids-09-05-t02-orchestrator-provider-error-handling/README.md) | pkg-000018 |
| 3 | [`task-ids-09-05-t03-canonical-subject-hash-contract`](./task-ids-09-05-t03-canonical-subject-hash-contract/README.md) | pkg-000018 |
| 4 | [`task-ids-09-05-t04-offline-contract-tests`](./task-ids-09-05-t04-offline-contract-tests/README.md) | pkg-000018 |
| 5 | [`task-ids-09-05-t05-story-acceptance-verification`](./task-ids-09-05-t05-story-acceptance-verification/README.md) | pkg-000018 |
| 6 | [`task-ids-09-05-t06-audit-f1-backlog-story-status-sync`](./task-ids-09-05-t06-audit-f1-backlog-story-status-sync/README.md) | override epic_ids_09_eid_05_audit_2026_06_08 |
| 7 | [`task-ids-09-05-t07-audit-f2-06-eid-providers-registry-section-reconcile`](./task-ids-09-05-t07-audit-f2-06-eid-providers-registry-section-reconcile/README.md) | override epic_ids_09_eid_05_audit_2026_06_08 |
