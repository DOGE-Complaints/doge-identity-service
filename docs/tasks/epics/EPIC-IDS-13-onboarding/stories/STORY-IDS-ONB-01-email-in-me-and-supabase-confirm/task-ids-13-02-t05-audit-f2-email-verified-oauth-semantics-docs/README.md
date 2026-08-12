## Task workspace — `task-ids-13-02-t05-audit-f2-email-verified-oauth-semantics-docs`

- Story: [`../STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md`](../STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md)
- Prerequisite: [`task-ids-13-02-t04-story-acceptance-verification`](../task-ids-13-02-t04-story-acceptance-verification/README.md)
- Audit source: [`../../../../../../analysis/identity-onb-01-code-audit-2026-07-24.md`](../../../../../../analysis/identity-onb-01-code-audit-2026-07-24.md) (F2)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_13_onb_01_audit_2026_07_24`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/identity-onb-01-code-audit-2026-07-24.md`](../../../../../../analysis/identity-onb-01-code-audit-2026-07-24.md) §Gaps F2; [`identity-cabinet-me-fields-interview-2026-07-13.md`](../../../../../../../analysis/identity-cabinet-me-fields-interview-2026-07-13.md) D-CAB-3  
---

## Task: docs — `email_verified` OAuth/`email=null` caveat in api-reference (F2)

### Цель
В consumer-facing описании `MeData.email_verified` (и при необходимости `email`) явно указать: для OAuth/GPT-токенов `email` может быть структурно `null` при `email_verified: true`; потребителю **не** трактовать `email_verified` как «есть подтверждённый адрес» без проверки `email != null`.

### Почему это важно
Audit F2 LOW: политика D-CAB-3 задокументирована (Confirm email), но OAuth-путь [`security.py:62-66`](../../../../../../../src/core/api/security.py) отдаёт `UserClaims(email=None)` → `/me` эмитит `email:null, email_verified:true`. Текущие [`openapi.yaml:76-80`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) / [`API_REFERENCE.md:84`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) не предупреждают потребителя.

### Факты из кода
1. [`me_response.py:21-22`](../../../../../../../src/core/api/me_response.py) — `email=current_user.email`, `email_verified=True` в базовом dict.
2. [`security.py:62-66`](../../../../../../../src/core/api/security.py) — OAuth fallback: `UserClaims(..., email=None, ...)`.
3. [`openapi.yaml:76-80`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) — `email_verified` desc: policy D-CAB-3 / Confirm email; без OAuth/`email=null` caveat.
4. [`API_REFERENCE.md:84`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) — Email fields: «всегда true» + Confirm email; без OAuth caveat.
5. Runtime emit — принятый дизайн (не дефект); в этом таске **не** менять код.

### Gap / Проблема
Потребитель может считать `email_verified:true` доказательством наличия подтверждённого email при `email:null` (OAuth/GPT).

### AC/DoD
- [x] (P0) `openapi.yaml` `MeData.email_verified` (и/или `email`) description включает оговорку: OAuth/GPT → `email` может быть `null` при `email_verified:true`; не трактовать флаг без `email != null`.
- [x] (P0) `API_REFERENCE.md` §6 Email fields — та же оговорка.
- [x] (P1) `rg` по обоим файлам: hits на OAuth / `email_verified` / `null` (по фактическому тексту caveat).
- [x] (P1) Не менять `me_response.py`, `security.py`, тесты, миграции.

### Где менять код
- `doge-identity-service/docs/runtime-docs/api-reference/openapi.yaml`
- `doge-identity-service/docs/runtime-docs/api-reference/API_REFERENCE.md`

### Out of scope
- Runtime change `me_response.py` / `security.py`
- Spa CAB-api-requirements (F1 → spa)
- Backlog T01–T03 vs pipeline t04 numbering (F3 ignored)
- Новый `pkg-*.yaml`, смена `identity-active-package.current.yaml`

### Проверка
```bash
cd doge-identity-service
rg -n 'email_verified|OAuth|email.*null|null.*email' \
  docs/runtime-docs/api-reference/openapi.yaml \
  docs/runtime-docs/api-reference/API_REFERENCE.md
```
