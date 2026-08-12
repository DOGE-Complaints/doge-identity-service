## Task workspace — `task-ids-04-05-t05-audit-s5-2-redundant-iss-check`

- Story: [`../STORY-IDS-04-05-supabase-jwt-bearer-auth.md`](../STORY-IDS-04-05-supabase-jwt-bearer-auth.md)
- Audit source: [`../../../../epic-ids-04-audit-2026-05-30.md`](../../../../epic-ids-04-audit-2026-05-30.md) (S5-2)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** ready  
**Wave:** `override epic_ids_04_audit_2026_05_30`  
---

## Task: refactor — remove redundant iss validation (S5-2)

### Цель
Убрать dead code: явная проверка `iss` после `JWTClaimsRegistry` с `iss={"essential": True, "value": self._expected_iss}`.

### Почему это важно (риск)
Redundant check создаёт шум при чтении security-critical кода; двойная логика может расходиться при рефакторинге.

### Факты из кода
1. [`epic-ids-04-audit-2026-05-30.md`](../../../../epic-ids-04-audit-2026-05-30.md) S5-2 (L207–217).
2. [`src/core/auth/supabase_validator.py:18-21`](../../../../../../../src/core/auth/supabase_validator.py): registry уже проверяет `iss`.
3. [`src/core/auth/supabase_validator.py:34-35`](../../../../../../../src/core/auth/supabase_validator.py): явный `if claims.get("iss") != self._expected_iss` — unreachable после registry pass.
4. [`tests/test_supabase_jwt_auth.py:97-100`](../../../../../../../tests/test_supabase_jwt_auth.py): iss_mismatch test — должен остаться green.

### Gap / Проблема
Дублирующая iss-валидация — dead code, не баг.

### AC/DoD
- [ ] (P0) Удалены строки явной iss-проверки L34-35 (или iss убран из registry — один путь, не оба).
- [ ] (P0) `test_validator_rejects_iss_mismatch` по-прежнему raises `JwtValidationError`.
- [ ] (P0) `pytest tests/test_supabase_jwt_auth.py -q -k iss_mismatch` проходит.

### Где менять код
- `doge-identity-service/src/core/auth/supabase_validator.py`

### Out of scope
- Изменения role/sub/exp validation
- Bearer auth error mapping

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_supabase_jwt_auth.py -q -k iss_mismatch
```
