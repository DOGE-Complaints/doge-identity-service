## Task workspace — `task-ids-04-05-t06-audit-s6-1-me-integration-test-hardening`

- Story: [`../STORY-IDS-04-05-supabase-jwt-bearer-auth.md`](../STORY-IDS-04-05-supabase-jwt-bearer-auth.md)
- Audit source: [`../../../../epic-ids-04-audit-2026-05-30.md`](../../../../epic-ids-04-audit-2026-05-30.md) (S6-1)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** ready  
**Wave:** `override epic_ids_04_audit_2026_05_30`  
---

## Task: tests — harden /me integration test setup (S6-1)

### Цель
Упростить или задокументировать `test_get_me_with_valid_supabase_token_not_401`: убрать хрупкий порядок `create_app` → monkeypatch → второй `create_app` в TestClient.

### Почему это важно (риск)
Тест проходит, но зависит от нестандартного lifecycle; изменения в `_lifespan` или `create_app` могут сломать сценарий без явной причины.

### Факты из кода
1. [`epic-ids-04-audit-2026-05-30.md`](../../../../epic-ids-04-audit-2026-05-30.md) S6-1 (L219–227).
2. [`tests/test_supabase_jwt_auth.py:127-153`](../../../../../../../tests/test_supabase_jwt_auth.py): двойной `create_app`, monkeypatch `get_api_dependencies` после первого вызова.
3. [`tests/conftest.py:20-28`](../../../../../../../tests/conftest.py): стандартный `test_client` fixture с env + `_clear_api_dependencies_cache`.
4. [`tests/test_asgi_transport.py`](../../../../../../../tests/test_asgi_transport.py): `_make_demo_bearer_token()` pattern для `/me` с demo JWT.

### Gap / Проблема
Нестандартный порядок setup; audit рекомендует conftest/env pattern или doc comment.

### AC/DoD
- [ ] (P0) Тест использует предсказуемый setup (conftest env **или** один `create_app` + TestClient **или** явный docstring с обоснованием порядка).
- [ ] (P0) AC сохранён: valid token → `/me` status != 401.
- [ ] (P1) `pytest tests/test_supabase_jwt_auth.py -q -k get_me` проходит.

### Где менять код
- `doge-identity-service/tests/test_supabase_jwt_auth.py` — `test_get_me_with_valid_supabase_token_not_401`

### Out of scope
- Functional `/me` handler (остаётся 501 stub)
- Изменения `asgi_app.py` singleton hook

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_supabase_jwt_auth.py -q -k get_me
```
