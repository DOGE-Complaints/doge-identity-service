## Task workspace — `task-ids-11-01-t10-audit-f3-runtime-docs-oauth-501-drift-sync`

- Story: [`../STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../STORY-IDS-OAUTH-01-oauth-server-endpoints.md)
- Audit source: [`../../../../../../analysis/epic-ids-11-oauth-01-audit-2026-06-24.md`](../../../../../../analysis/epic-ids-11-oauth-01-audit-2026-06-24.md) (F3)

---
**Приоритет:** P1  
**Сложность:** M  
**Статус:** done  
**Wave:** `override epic_ids_11_oauth_01_audit_2026_06_24`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-11-oauth-01-audit-2026-06-24.md`](../../../../../../analysis/epic-ids-11-oauth-01-audit-2026-06-24.md) §F3  
---

## Task: fix — runtime-docs + neighbor stories OAuth 501 drift (F3)

### Цель
Синхронизировать флоу-доки и prerequisites соседних backlog-стори после OAUTH-01 build: убрать устаревшие «OAuth = 501», отразить ✅ построенные роуты и закрытый SEC-1.

### Почему это важно
Доки обновлялись 2026-06-24 под phone-pivot, но as-is врезки ещё описывают OAuth как 501 — вводит в заблуждение gateway/intake и OAUTH-02/03/04 planning.

### Факты из кода
1. [`04-security.md:68,89,95,109-111`](../../../../../../runtime-docs/04-security.md) — as-is «OAuth = 501», устаревшие refs SEC-1.
2. [`09-gateway-expectations.md:33,47`](../../../../../../runtime-docs/09-gateway-expectations.md) — «роуты `/oauth/*` — 501».
3. [`STORY-IDS-OAUTH-02`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md) — prerequisites устарели.
4. [`STORY-IDS-OAUTH-03`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) — «`/oauth/*` = 501».
5. [`STORY-IDS-OAUTH-04`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md) — «`/oauth/*` = 501».
6. Код: роуты live [`asgi_app.py:369-403`](../../../../../../../src/core/api/asgi_app.py); `verify_client_secret` [`client_secret.py`](../../../../../../../src/core/oauth/client_secret.py).

### Gap / Проблема
Свежий cross-doc drift «OAuth 501» после OAUTH-01 Done (audit F3 MEDIUM).

### AC/DoD
- [x] (P0) `04-security §A`: as-is таблица — OAuth-маршруты ✅ (OAUTH-01); introspection ⚪ (OAUTH-02).
- [x] (P0) `04-security §3`: SEC-1 закрыт; наружу подключён (`core/oauth/`).
- [x] (P0) `09-gateway-expectations`: выдача OAuth-токена ✅ (роуты); introspection ❌.
- [x] (P0) OAUTH-02/03/04 backlog: prerequisites — OAUTH-01 ✅ построен; убрать «роуты 501».
- [x] (P1) **Не** менять AC/Scope соседних стори (verbatim).
- [x] (P1) In-memory handshake → OAUTH-03 остаётся наблюдением (не gap).

### Где менять код
- `doge-identity-service/docs/runtime-docs/04-security.md`
- `doge-identity-service/docs/runtime-docs/09-gateway-expectations.md`
- `doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md`
- `doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`
- `doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`

### Out of scope
- [`PLAN-IDS-OAUTH-docs-actualization.md`](../../../../../../backlog-stories/oauth/PLAN-IDS-OAUTH-docs-actualization.md) (временный рабочий план).
- Код, pytest, pkg yaml, active package pointer.
- Полная перепись target-диаграмм (только as-is/factual sync).

### Проверка
```bash
grep -n "501\|OAUTH-01\|построен\|SEC-1" \
  doge-identity-service/docs/runtime-docs/04-security.md \
  doge-identity-service/docs/runtime-docs/09-gateway-expectations.md \
  doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-0{2,3,4}*.md
```
