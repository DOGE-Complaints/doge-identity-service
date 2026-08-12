## Task workspace — `task-ids-04-02-t04-audit-s2-1-client-secret-doc`

- Story: [`../STORY-IDS-04-02-inmemory-repositories.md`](../STORY-IDS-04-02-inmemory-repositories.md)
- Audit source: [`../../../../epic-ids-04-audit-2026-05-30.md`](../../../../epic-ids-04-audit-2026-05-30.md) (S2-1)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** ready  
**Wave:** `override epic_ids_04_audit_2026_05_30`  
---

## Task: fix — document InMemory OAuth client_secret skip (S2-1)

### Цель
Задокументировать намеренное отсутствие проверки `client_secret` в `InMemoryOAuthTokenService.issue_access_token` и закрепить тестом InMemory-поведение.

### Почему это важно (риск)
Без doc/test неясно — упрощение для demo или пропущенная логика; при EPIC-IDS-05 Supabase impl может не добавить real validation.

### Факты из кода
1. [`epic-ids-04-audit-2026-05-30.md`](../../../../epic-ids-04-audit-2026-05-30.md) S2-1 (L100–119).
2. [`src/core/infrastructure/repositories.py:274`](../../../../../../../src/core/infrastructure/repositories.py): `del client_secret` — параметр Protocol принят, но не проверяется.
3. [`src/core/domain/contracts.py:89-97`](../../../../../../../src/core/domain/contracts.py): `OAuthTokenService.issue_access_token` требует `client_secret` в сигнатуре.

### Gap / Проблема
InMemory принимает любой `client_secret`, включая пустой/wrong — без комментария и теста.

### AC/DoD
- [ ] (P0) Комментарий у `del client_secret` объясняет InMemory skip + ссылку на EPIC-IDS-05 для Supabase impl.
- [ ] (P0) Тест: `issue_access_token(..., client_secret="wrong", ...)` успешно при валидном code (InMemory policy задокументирован).
- [ ] (P1) `pytest tests/test_inmemory_repositories.py -q` проходит.

### Где менять код
- `doge-identity-service/src/core/infrastructure/repositories.py` — `InMemoryOAuthTokenService.issue_access_token`
- `doge-identity-service/tests/test_inmemory_repositories.py` — новый test case

### Out of scope
- Реальная проверка `client_secret_hash` в InMemory (намеренно out of scope)
- Supabase OAuth token service — EPIC-IDS-05

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_inmemory_repositories.py -q -k client_secret
```
