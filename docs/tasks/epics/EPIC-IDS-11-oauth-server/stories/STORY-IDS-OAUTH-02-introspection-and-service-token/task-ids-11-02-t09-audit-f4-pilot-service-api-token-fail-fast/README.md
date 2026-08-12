## Task workspace — `task-ids-11-02-t09-audit-f4-pilot-service-api-token-fail-fast`

- Story: [`../STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../STORY-IDS-OAUTH-02-introspection-and-service-token.md)
- Audit source: [`../../../../../../analysis/epic-ids-11-oauth-02-audit-2026-06-24.md`](../../../../../../analysis/epic-ids-11-oauth-02-audit-2026-06-24.md) (F4)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_11_oauth_02_audit_2026_06_24`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-11-oauth-02-audit-2026-06-24.md`](../../../../../../analysis/epic-ids-11-oauth-02-audit-2026-06-24.md) §F4  
---

## Task: fix — pilot fail-fast for SERVICE_API_TOKEN (F4)

### Цель
Закрыть info-disclosure gap: при `APP_PROFILE=pilot` без `SERVICE_API_TOKEN` сервер не должен стартовать — иначе `/oauth/introspect` открыт (`ServiceTokenAuth.disabled()` → `require()` no-op).

### Почему это важно
В pilot без обязательного service token любой клиент может вызвать introspection с пользовательским OAuth-токеном и получить `{sub, phone_verified}` (audit F4 MEDIUM, security).

### Факты из кода
1. [`schema.py:174-184`](../../../../../../../src/core/config/schema.py) — `pilot_required` без `SERVICE_API_TOKEN` (есть `OAUTH_ACCESS_TOKEN_SECRET`, `GPT_OAUTH_CLIENT_SECRET`).
2. [`security.py:108-110`](../../../../../../../src/core/api/security.py) — `from_secret("")` → `disabled()`; `require()` no-op when disabled.
3. [`asgi_app.py:407-416`](../../../../../../../src/core/api/asgi_app.py) — `POST /oauth/introspect` gated `Depends(require_service_token)`.
4. Gateway pattern: [`doge-complaints-gateway/.../security.py:65-72`](../../../../../../../../doge-complaints-gateway/src/core/api/security.py) — optional in demo, required in prod paths.

### Gap / Проблема
AC2 story выполнен только когда `SERVICE_API_TOKEN` задан; pilot не enforce'ит секрет → introspect открыт в production profile (audit F4).

### AC/DoD
- [x] (P0) `pilot_required` включает `("SERVICE_API_TOKEN", _value(env, "SERVICE_API_TOKEN", ""))`.
- [x] (P0) `APP_PROFILE=pilot` без `SERVICE_API_TOKEN` → `ConfigError` (mirror `OAUTH_ACCESS_TOKEN_SECRET` test pattern).
- [x] (P1) `APP_PROFILE=demo` без `SERVICE_API_TOKEN` — по-прежнему allowed (disabled gate).
- [x] (P1) Offline suite green: `pytest -m "not live_integration"` (351 passed).

### Где менять код
- `doge-identity-service/src/core/config/schema.py`
- `doge-identity-service/tests/test_config_schema.py`

### Out of scope
- Default-deny на route-уровне (альтернатива из audit — только если pilot fail-fast недостаточен).
- runtime-docs bulk sync (t08), `EPIC-IDS-OAUTH.md` (t07).
- pkg yaml, `identity-active-package.current.yaml`.

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_config_schema.py -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
