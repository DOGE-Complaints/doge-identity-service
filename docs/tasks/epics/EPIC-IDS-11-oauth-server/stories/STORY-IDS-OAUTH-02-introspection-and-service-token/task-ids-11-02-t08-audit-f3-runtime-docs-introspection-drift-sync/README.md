## Task workspace — `task-ids-11-02-t08-audit-f3-runtime-docs-introspection-drift-sync`

- Story: [`../STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../STORY-IDS-OAUTH-02-introspection-and-service-token.md)
- Audit source: [`../../../../../../analysis/epic-ids-11-oauth-02-audit-2026-06-24.md`](../../../../../../analysis/epic-ids-11-oauth-02-audit-2026-06-24.md) (F3)

---
**Приоритет:** P1  
**Сложность:** M  
**Статус:** done  
**Wave:** `override epic_ids_11_oauth_02_audit_2026_06_24`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-11-oauth-02-audit-2026-06-24.md`](../../../../../../analysis/epic-ids-11-oauth-02-audit-2026-06-24.md) §F3  
---

## Task: fix — runtime-docs introspection + service-token drift (F3)

### Цель
Синхронизировать persistent runtime-docs после OAUTH-02 build: `/oauth/introspect` ✅, `SERVICE_API_TOKEN` / service gate ✅; снять устаревшие «introspection отсутствует» / «нет проверки сервисного токена».

### Почему это важно
`04-security` и `09-gateway-expectations` — intake для gateway; свежий drift после OAUTH-02 Done вводит в заблуждение при планировании стыка identity↔gateway.

### Факты из кода
1. [`04-security.md:68,92-93,95`](../../../../../../runtime-docs/04-security.md) — as-is «introspection-endpoint ❌ отсутствует», «нет SERVICE_API_TOKEN».
2. [`09-gateway-expectations.md:32,34,47`](../../../../../../runtime-docs/09-gateway-expectations.md) — «`/oauth/introspect` отсутствует», «нет SERVICE_API_TOKEN», итог «нет introspection-endpoint».
3. [`01-api.md:36`](../../../../../../runtime-docs/01-api.md) — «нет `/oauth/introspect`».
4. Код: [`asgi_app.py:407-416`](../../../../../../../src/core/api/asgi_app.py) — `POST /oauth/introspect`; [`schema.py:70,238`](../../../../../../../src/core/config/schema.py) — `service_api_token`; [`security.py:89-116`](../../../../../../../src/core/api/security.py) — `ServiceTokenAuth`.

### Gap / Проблема
Свежий cross-doc drift «introspection/service-token отсутствует» после OAUTH-02 Done (audit F3 MEDIUM).

### AC/DoD
- [x] (P0) `04-security §A`: as-is таблица/врезка — introspection-endpoint ✅ (OAUTH-02); service-token gate ✅.
- [x] (P0) `09-gateway-expectations`: таблица + итог — introspect ✅, service token check ✅ (не ❌).
- [x] (P1) `01-api.md`: убрать «нет `/oauth/introspect`» (или отметить ✅ построен).
- [x] (P1) OAUTH-03/04 в тексте runtime-docs: handshake in-memory остаётся наблюдением (OAUTH-03); не менять AC соседних backlog-стори.
- [x] (P1) **Не** переписывать target-диаграммы целиком — только as-is/factual sync.

### Где менять код
- `doge-identity-service/docs/runtime-docs/04-security.md`
- `doge-identity-service/docs/runtime-docs/09-gateway-expectations.md`
- `doge-identity-service/docs/runtime-docs/01-api.md` (опц. P1)

### Out of scope
- [`PLAN-IDS-OAUTH-docs-actualization.md`](../../../../../../backlog-stories/oauth/PLAN-IDS-OAUTH-docs-actualization.md) (временный рабочий план).
- Код, pytest, `EPIC-IDS-OAUTH.md` (t07), pilot fail-fast (t09).
- pkg yaml, active package pointer.

### Проверка
```bash
grep -n "introspect\|SERVICE_API_TOKEN\|отсутствует\|OAUTH-02" \
  doge-identity-service/docs/runtime-docs/04-security.md \
  doge-identity-service/docs/runtime-docs/09-gateway-expectations.md \
  doge-identity-service/docs/runtime-docs/01-api.md
```
