## Task workspace — `task-ids-04-01-t04-audit-s1-2-mutable-collection-fields`

- Story: [`../STORY-IDS-04-01-domain-protocols-contracts.md`](../STORY-IDS-04-01-domain-protocols-contracts.md)
- Audit source: [`../../../../epic-ids-04-audit-2026-05-30.md`](../../../../epic-ids-04-audit-2026-05-30.md) (S1-2)

---
**Приоритет:** P2  
**Сложность:** M  
**Статус:** ready  
**Wave:** `override epic_ids_04_audit_2026_05_30`  
---

## Task: fix — frozen dataclass mutable collection fields (S1-2)

### Цель
Закрыть gap S1-2: решить политику для `list`/`dict` полей в `@dataclass(frozen=True)` — immutable types **или** явная doc+test на допустимую shallow-мутацию.

### Почему это важно (риск)
`frozen=True` не защищает содержимое `list`/`dict`; неожиданная мутация scopes или session data может нарушить изоляцию тестов.

### Факты из кода
1. [`epic-ids-04-audit-2026-05-30.md`](../../../../epic-ids-04-audit-2026-05-30.md) S1-2 (L67–77).
2. [`src/core/domain/models.py:54`](../../../../../../../src/core/domain/models.py): `VerificationSession.provider_session_data: dict[str, object]`.
3. [`src/core/domain/models.py:77`](../../../../../../../src/core/domain/models.py): `OAuthClient.scopes: list[str]`.
4. [`src/core/domain/models.py:83`](../../../../../../../src/core/domain/models.py): `OAuthTokenClaims.scopes: list[str]`.

### Gap / Проблема
Shallow mutation (`scopes.append(...)`) возможна без ошибки; нет теста и явного решения.

### AC/DoD
- [ ] (P0) Принято и зафиксировано одно решение: **(A)** `tuple`/`MappingProxyType` **или** **(B)** docstring + test documenting shallow-mutation policy.
- [ ] (P0) Все call sites / tests обновлены под выбранное решение.
- [ ] (P1) `pytest tests/test_domain_contracts.py tests/test_inmemory_repositories.py -q` проходит.

### Где менять код
- `doge-identity-service/src/core/domain/models.py`
- `doge-identity-service/tests/test_domain_contracts.py` (или новый focused test)

### Out of scope
- Deep immutability для nested dict values (unless chosen explicitly)
- Supabase persistence models — EPIC-IDS-05

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_domain_contracts.py -q
```
