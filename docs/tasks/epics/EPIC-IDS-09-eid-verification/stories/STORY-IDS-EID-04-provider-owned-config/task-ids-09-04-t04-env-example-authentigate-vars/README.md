## Task workspace — `task-ids-09-04-t04-env-example-authentigate-vars`

- Story: [`../STORY-IDS-EID-04-provider-owned-config.md`](../STORY-IDS-EID-04-provider-owned-config.md)
- Prerequisite: t02 AuthentigateSettings defaults (scopes, acr, discovery)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000017`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §F3, F10  
---

## Task: update — `.env.example` Authentigate section

### Цель
Привести `.env.example` в соответствие с `AuthentigateSettings`: demo issuer, full scope URLs, acr, ui_locales, country, optional discovery_url.

### Почему это важно
Story AC #5 (partial): `.env.example` отражает актуальные Authentigate-настройки. Операторы и CI читают example как SSOT для env shape.

### Факты из кода
1. Stale example: [`.env.example:46-52`](../../../../../../../.env.example) — localhost issuer, short scopes.
2. Audit F10: full claim-URLs required — [`authentigate-compatibility-audit-2026-06-07.md:160-163`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md).
3. Story Scope: issuer demo `https://oidc.demo.sk.ee`, scopes-URL, acr, ui_locales, country.

### Gap / Проблема
`.env.example` не отражает F3/F10 target shape.

### AC/DoD
- [x] (P0) `AUTHENTIGATE_ISSUER=https://oidc.demo.sk.ee` (demo default documented).
- [x] (P0) `AUTHENTIGATE_SCOPES` = full claim-URLs (match t02 default).
- [x] (P0) Add/document `AUTHENTIGATE_ACR_VALUES`, `AUTHENTIGATE_UI_LOCALES`, `AUTHENTIGATE_COUNTRY`, optional `AUTHENTIGATE_DISCOVERY_URL`.
- [x] (P1) Comments align with [`Authentigate Integration guide.md`](../../../../../../tech-requirements/Authentigate%20Integration%20guide.md) where applicable.

### Где менять код
- `doge-identity-service/.env.example` only

### Out of scope
- Local `.env` (operator machine)
- SPIKE-09 live demo confirmation
- Runtime code changes

### Проверка
```bash
grep -n "AUTHENTIGATE" doge-identity-service/.env.example
grep "oidc.demo.sk.ee\|id.authentigate.eu/claims" doge-identity-service/.env.example
```
