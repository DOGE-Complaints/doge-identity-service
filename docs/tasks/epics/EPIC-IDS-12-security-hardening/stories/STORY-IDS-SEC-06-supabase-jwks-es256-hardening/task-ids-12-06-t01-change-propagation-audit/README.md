## Task workspace — `task-ids-12-06-t01-change-propagation-audit`

- Story: [`../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md)
- Prerequisite: —

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000042`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md) §Подзадачи T01; Story AC prep  
---

## Task: analyze — change-propagation audit for JWKS-only migration

### Цель
Зафиксировать полный список потребителей удаляемого HS256/`SUPABASE_JWT_SECRET`/sentinel-кода и утвердить план миграции тестового харнеса (T05) и доков (T07) — backlog §Подзадачи T01.

### Почему это важно
JWKS-only (D-1) ломает ~14 test-файлов; без полного grep-inventory P3 рискует пропустить минтер или doc assert.

### Факты из кода
1. HS256-путь в валидаторе — [`supabase_validator.py:72-73,101-102`](../../../../../../../src/core/auth/supabase_validator.py) `_validate_hs256`, `alg=="HS256"`.
2. `jwt_secret` / `OctKey` — [`supabase_validator.py:35,40,43`](../../../../../../../src/core/auth/supabase_validator.py).
3. `demo.local` гейт — [`supabase_validator.py:51`](../../../../../../../src/core/auth/supabase_validator.py); sentinel — [`providers.py:109-110`](../../../../../../../src/core/infrastructure/providers.py).
4. `SUPABASE_JWT_SECRET` — [`schema.py:34,160,190,215`](../../../../../../../src/core/config/schema.py).
5. OAuth HS256 **вне scope** — [`oauth/access_token_jwt.py:26`](../../../../../../../src/core/oauth/access_token_jwt.py).
6. Backlog change-propagation list — pipeline story §Scope Change-propagation.

### Gap / Проблема
Нет зафиксированного machine-readable списка файлов/символов для grep-gates AC и порядка миграции T02–T07.

### AC/DoD
- [ ] (P0) Grep inventory `_validate_hs256` / `supabase_jwt_secret` / `test-secret-for-demo` / `demo.local` / Supabase `"alg":"HS256"` по `src/` и `tests/` с явным **exclude** `oauth/access_token_jwt.py`.
- [ ] (P0) Список 14+ test minters + `conftest.py` + `test_config_schema.py` + `test_supabase_runbook_docs.py` + live sanity — сопоставлен с backlog §Change-propagation.
- [ ] (P0) План миграции: порядок T02→T03→T04→T05→T06→T07 задокументирован в task notes или `docs/analysis/` (analysis-only, без runtime).
- [ ] (P1) Story AC traceability для downstream tasks t02–t08.

### Где менять код
- `doge-identity-service/docs/analysis/` (optional audit note)
- Этот README (inventory table в комментарии оператора или linked analysis file)

### Out of scope
- Runtime правки валидатора/тестов (t02+)
- OAuth `access_token_jwt.py`

### Проверка
```bash
cd doge-identity-service
grep -rn '_validate_hs256\|supabase_jwt_secret\|test-secret-for-demo\|demo\.local' src/ tests/ || true
grep -rn 'alg": "HS256"' tests/ | grep -v oauth || true
grep -rn 'SUPABASE_JWT_SECRET' src/ tests/ .env.example || true
```
