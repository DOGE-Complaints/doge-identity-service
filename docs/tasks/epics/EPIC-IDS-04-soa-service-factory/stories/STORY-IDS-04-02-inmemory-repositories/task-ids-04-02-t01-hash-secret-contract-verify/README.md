## Task workspace — `task-ids-04-02-t01-hash-secret-contract-verify`

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000005`  
**Decision Ref:** [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) §6 Story 2 (зависимость hashing L141–150)  
**Story:** [`../STORY-IDS-04-02-inmemory-repositories.md`](../STORY-IDS-04-02-inmemory-repositories.md)  
---

## Task: verify — hash_secret contract vs epic

### Цель
Верифицировать, что [`src/core/security/hashing.py`](../../../../../../../src/core/security/hashing.py) соответствует контракту epic L145–148 (`HMAC-SHA256 hex digest`, явный `key`, без global state). При необходимости — минимальная правка; опционально — unit-тест на детерминизм (одна строка).

### Почему это важно
`InMemoryOAuthClientStore.from_config` и eID-провайдеры (req-13/14) зависят от единого `hash_secret`; расхождение контракта ломает OAuth client secret hashing и тесты Story 2.

### Факты из кода
1. [`src/core/security/hashing.py:9-11`](../../../../../../../src/core/security/hashing.py) — `hash_secret(plaintext, *, key)` → `hmac.new(..., hashlib.sha256).hexdigest()`.
2. [`src/core/domain/`](../../../../../../../src/core/domain/) — **отсутствует** (Story 1).
3. [`src/core/infrastructure/repositories.py`](../../../../../../../src/core/infrastructure/repositories.py) — **отсутствует**.
4. Epic L145–148 требует: `def hash_secret(plaintext: str, *, key: str) -> str` с docstring про HMAC-SHA256.

### Gap
Нет формальной верификации контракта и опционального теста детерминизма из AC Story 2 L205.

### AC/DoD
- [ ] (P0) `from core.security.hashing import hash_secret` — импортируется без ошибок.
- [ ] (P0) Сигнатура и поведение соответствуют epic L145–148 (HMAC-SHA256 hex, key явный).
- [ ] (P1) Опционально: unit-тест — одинаковый `(plaintext, key)` даёт одинаковый digest (детерминизм).

### Где менять код
- `doge-identity-service/src/core/security/hashing.py` (только если контракт не совпадает)
- `doge-identity-service/tests/test_security_hashing.py` (новый, опционально)

### Out of scope
- InMemory repositories — [`task-ids-04-02-t02-inmemory-repositories`](../task-ids-04-02-t02-inmemory-repositories/README.md)
- Story 2 full AC pytest — t03
- Supabase hashing — EPIC-IDS-05

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "
from core.security.hashing import hash_secret
a = hash_secret('demo', key='demo-key')
b = hash_secret('demo', key='demo-key')
assert a == b and len(a) == 64
print('hash_secret OK:', a[:16], '...')
"
# опционально:
# .venv/bin/python -m pytest tests/test_security_hashing.py -q
```
