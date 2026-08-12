## Task workspace — `task-ids-09-05-t06-audit-f1-backlog-story-status-sync`

- Story: [`../STORY-IDS-EID-05-canonical-provider-contract.md`](../STORY-IDS-EID-05-canonical-provider-contract.md)
- Audit source: [`../../../../../../analysis/epic-ids-09-eid-05-audit-2026-06-08.md`](../../../../../../analysis/epic-ids-09-eid-05-audit-2026-06-08.md) (F1)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_09_eid_05_audit_2026_06_08`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-09-eid-05-audit-2026-06-08.md`](../../../../../../analysis/epic-ids-09-eid-05-audit-2026-06-08.md) §F1  
---

## Task: fix — backlog story status and code refs sync (F1)

### Цель
Привести backlog SSOT [`STORY-IDS-EID-05-canonical-provider-contract.md`](../../../../../../backlog-stories/STORY-IDS-EID-05-canonical-provider-contract.md) в соответствие с фактом: story 🟢 Done под **EPIC-IDS-09**, канон контракта provider→core реализован (не широкий `provider_error` / pre-EID-05 refs).

### Почему это важно
Backlog INDEX и операторы читают backlog как SSOT; устаревший `⚪ Todo`, устаревшие «Точки в коде» и AC `[ ]` вводят в заблуждение при следующем intake (EID-06+).

### Факты из кода
1. [`backlog-stories/STORY-IDS-EID-05-canonical-provider-contract.md:6`](../../../../../../backlog-stories/STORY-IDS-EID-05-canonical-provider-contract.md) — `Status: ⚪ Todo`.
2. [`backlog-stories/...:23-27`](../../../../../../backlog-stories/STORY-IDS-EID-05-canonical-provider-contract.md) — «Точки в коде» — устаревший широкий `except` ([`handlers.py:263-281`](../../../../../../../src/core/api/handlers.py)), `EIDProviderError` без enum ([`base.py:24-29`](../../../../../../../src/core/providers/base.py)).
3. [`backlog-stories/...:30-34`](../../../../../../backlog-stories/STORY-IDS-EID-05-canonical-provider-contract.md) — AC checkboxes `[ ]`.
4. Pipeline story: [`../STORY-IDS-EID-05-canonical-provider-contract.md`](../STORY-IDS-EID-05-canonical-provider-contract.md) — 🟢 Done, AC [x].
5. `EidErrorCode`: [`base.py:9-18`](../../../../../../../src/core/providers/base.py); typed `EIDProviderError`: [`base.py:39-44`](../../../../../../../src/core/providers/base.py).
6. Orchestrator split: [`handlers.py:266-302`](../../../../../../../src/core/api/handlers.py); hash formula: [`handlers.py:304-307`](../../../../../../../src/core/api/handlers.py).
7. Mock subject_hash: [`mock_provider.py:65-71`](../../../../../../../src/core/providers/mock/mock_provider.py) — `secrets.token_hex(16)` без префикса `mock-`.
8. Contract tests: [`tests/test_canonical_provider_contract.py`](../../../../../../../tests/test_canonical_provider_contract.py) — 3 offline tests.

### Gap / Проблема
Doc-stale в backlog; расхождение backlog ↔ pipeline ↔ код (audit F1 MEDIUM).

### AC/DoD
- [x] (P0) Backlog Meta: `Status: 🟢 Done`.
- [x] (P0) Секция «Точки в коде» отражает `EidErrorCode`, split `EIDProviderError`/`Exception` в orchestrator, формулу `verified_person_hash`, mock `subject_hash` (не pre-EID-05 line refs).
- [x] (P0) AC checkboxes в backlog [x] — **verbatim** формулировки AC не менять.
- [x] (P1) Ссылка на pipeline story / pkg-000018 как источник исполнения.

### Где менять код
- `doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-EID-05-canonical-provider-contract.md` only

### Out of scope
- Изменение AC текста story (verbatim).
- Код, pytest, runtime-docs.
- F2 из audit (отдельный task t07).
- Pipeline story «Точки в коде» (audit F1 scope = backlog only).

### Проверка
```bash
grep -n "Status\|EidErrorCode\|handlers.py:266\|provider_error\|263-281" \
  doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-EID-05-canonical-provider-contract.md
```
