## Task workspace — `task-ids-08-02-t02-allowed-return-urls-e17`

- Story: [`../STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../STORY-IDS-CLEANUP-02-placeholders-hardening.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-02-placeholders-hardening.md) Scope E17; [`../task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/owner-decisions-e17-e22.md`](../task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/owner-decisions-e17-e22.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000013`  
**Skill declared:** python-pro  
---

## Task: implement — ALLOWED_RETURN_URLS (E17)

### Цель
Выполнить owner decision по E17: либо реализовать валидацию `return_url` по белому списку (закрыть open-redirect), либо убрать настройку `ALLOWED_RETURN_URLS` из конфига.

### Почему это важно
Gap P2 / open-redirect риск: поле читается, но не проверяется ([`08-ui-expectations`](../../../../../../../runtime-docs/08-ui-expectations.md):18,30). Story AC #1, условно AC #2.

### Факты из кода
1. [`schema.py:57,169`](../../../../../../../src/core/config/schema.py) — `AppConfig.allowed_return_urls` из env `ALLOWED_RETURN_URLS`.
2. [`handlers.py:73`](../../../../../../../src/core/api/handlers.py) — `POST /auth/eid/start` stub («implemented in EPIC-IDS-EID»).
3. [`models.py:52`](../../../../../../../src/core/domain/models.py) — `return_url` на сессии eID.
4. Требования: [`11-eid-verification-flow.md`](../../../../../../../docs/requirements/11-eid-verification-flow.md) — validate return_url against allowlist (P-006).

### Gap / Проблема
`ALLOWED_RETURN_URLS` читается, validation enforcement в runtime отсутствует.

### AC/DoD
- [ ] (P0) Story AC #1: решение E17 из t01 выполнено в коде.
- [ ] (P0) Если decision = «довести»: Story AC #2 — `return_url` валидируется; тест отклоняет чужой домен.
- [ ] (P0) Если decision = «убрать»: `allowed_return_urls` / `ALLOWED_RETURN_URLS` grep = 0 в `src/` (tests/docs exempt по decision).
- [ ] (P1) Offline pytest green для затронутых модулей.

### Где менять код
- [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py) — поле / pilot refs (если убрать)
- Новый или существующий validator helper (если довести)
- [`src/core/api/handlers.py`](../../../../../../../src/core/api/handlers.py) или helper, вызываемый из eID start (если довести)
- `tests/test_*` — validation test (если довести)

### Out of scope
- Полная реализация eID start flow — functional EID epic
- web3 wallet — backlog «Вне scope»

### Проверка
```bash
cd doge-identity-service
rg "allowed_return_urls|ALLOWED_RETURN_URLS" src/
.venv/bin/python -m pytest tests/ -k "return_url" -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
