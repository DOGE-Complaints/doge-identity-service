## Task workspace — `task-ids-08-02-t08-audit-f1-return-url-validator-enforcement`

- Story: [`../STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../STORY-IDS-CLEANUP-02-placeholders-hardening.md)
- Audit source: [`../../../../../../analysis/epic-ids-08-cleanup-02-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-08-cleanup-02-audit-2026-06-05.md) (F1)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `override epic_ids_08_cleanup_02_audit_2026_06_05`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-08-cleanup-02-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-08-cleanup-02-audit-2026-06-05.md) §F1 · [`../task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/owner-decisions-e17-e22.md`](../task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/owner-decisions-e17-e22.md) E17  
---

## Task: implement — return_url validator enforcement (F1)

### Цель
Закрыть audit F1: `validate_return_url` реализован, но не вызывается в runtime — open-redirect защита E17 не enforced.

### Почему это важно
Gap P2 / AC #2 частично: unit-тесты есть, но `grep validate_return_url src/` (кроме модуля) = 0. Единственный потребитель — `POST /auth/eid/start` (501 stub).

### Факты из кода
1. [`return_url.py:26`](../../../../../../../src/core/security/return_url.py) — `validate_return_url`, `parse_allowed_return_urls`, `InvalidReturnUrlError`.
2. Grep `validate_return_url` в `src/` — только определение в `return_url.py` (0 callers).
3. [`handlers.py:65-76`](../../../../../../../src/core/api/handlers.py) — `handle_auth_eid_start_stub` → 501 без validation.
4. [`schema.py:56,166`](../../../../../../../src/core/config/schema.py) — `AppConfig.allowed_return_urls`.
5. [`tests/test_return_url_validation.py:25-28`](../../../../../../../tests/test_return_url_validation.py) — `test_validate_return_url_rejects_foreign_domain` PASS (unit only).

### Gap / Проблема
Open-redirect ради E17 «подготовлен», но в рантайме `return_url` не проверяется.

### AC/DoD
- [ ] (P0) **Branch A (enforce):** `validate_return_url` вызывается при приёме `return_url` (stub/pre-501 path в `handlers.py` или `asgi_app.py`) с `parse_allowed_return_urls(deps.config.allowed_return_urls)`; invalid → 400 `invalid_return_url`.
- [ ] (P0) **Branch A:** integration/route test: foreign domain rejected at handler boundary.
- [ ] (P0) **Branch B (defer):** явная запись в `owner-decisions-e17-e22.md` + pipeline story note: enforcement → EPIC-IDS-EID; audit F1 closed as documented defer (operator choice on P3).
- [ ] (P1) BULLRUN-PHASE-LOG + acceptance-verification в этой папке (P3).

### Где менять код
- [`src/core/api/handlers.py`](../../../../../../../src/core/api/handlers.py) — `handle_auth_eid_start_stub` или новый pre-stub helper
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) — POST `/auth/eid/start` wiring (если body parse здесь)
- [`tests/`](../../../../../../../tests/) — integration test (Branch A)
- [`owner-decisions-e17-e22.md`](../task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/owner-decisions-e17-e22.md) — Branch B only

### Out of scope
- Полная реализация eID flow (EPIC-IDS-EID)
- Удаление `ALLOWED_RETURN_URLS` (противоречит t01 decision «довести»)

### Проверка
```bash
cd doge-identity-service
rg "validate_return_url" src/ --glob '!**/return_url.py'
.venv/bin/python -m pytest -m "not live_integration" -q
```
