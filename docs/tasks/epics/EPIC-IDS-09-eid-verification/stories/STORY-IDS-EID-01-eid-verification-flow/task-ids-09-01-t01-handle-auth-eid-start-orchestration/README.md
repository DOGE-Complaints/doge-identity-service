## Task workspace — `task-ids-09-01-t01-handle-auth-eid-start-orchestration`

- Story: [`../STORY-IDS-EID-01-eid-verification-flow.md`](../STORY-IDS-EID-01-eid-verification-flow.md)
- Prerequisite: STORY-IDS-AUTHCORE-01 Done ([`EPIC-IDS-07`](../../../../EPIC-IDS-07-auth-core/EPIC-IDS-07-auth-core.md))

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000015`  
**Skill declared:** python-pro  
---

## Task: implement — `POST /auth/eid/start` orchestration

### Цель
Заменить `handle_auth_eid_start_stub` в [`handlers.py`](../../../../../../../src/core/api/handlers.py): по JWT user, `validate_return_url`, активный провайдер из `deps.eid_provider_registry.get_active`, `start_flow` с `return_context`/`requested_action`; audit event «started».

### Почему это важно
Story Scope: `POST /auth/eid/start`; AC #1 — сессия `started` + redirect к провайдеру.

### Факты из кода
1. [`handlers.py:70-92`](../../../../../../../src/core/api/handlers.py) — stub: `validate_return_url` OK, затем 501 `next_epic="EPIC-IDS-EID"`.
2. [`providers/registry.py:16-17`](../../../../../../../src/core/providers/registry.py) — `EIDProviderRegistry.get_active(config)`.
3. [`providers/mock/mock_provider.py`](../../../../../../../src/core/providers/mock/mock_provider.py) — `MockEIDProvider.start_flow` создаёт сессию + redirect URL.
4. [`models.py:44-59`](../../../../../../../src/core/domain/models.py) — `return_context`, `requested_action` на `VerificationSession`.
5. [`dependencies.py:45-46`](../../../../../../../src/core/api/dependencies.py) — `eid_audit_log_repository` доступен через `ApiDependencies`.
6. [`providers.py:92-104`](../../../../../../../src/core/infrastructure/providers.py) — registry wired в service factory.

### Gap / Проблема
Нет runtime orchestration start: stub возвращает 501 после validation.

### AC/DoD
- [x] (P0) `handle_auth_eid_start` принимает JWT user, `return_url`, опционально `return_context`/`requested_action`.
- [x] (P0) `validate_return_url` — сохранить текущее поведение 400 при invalid URL (story Scope).
- [x] (P0) Активный провайдер через `deps.eid_provider_registry.get_active(deps.config)` → `start_flow` → сессия status `started`, redirect в ответе (AC #1).
- [x] (P0) Audit: `eid_audit_log_repository.log_event` для «started» без PII (AC #5, partial — t04 расширит lifecycle).
- [x] (P1) Stub удалён; `handle_auth_eid_start` — единственный entry point.

### Где менять код
- `doge-identity-service/src/core/api/handlers.py`

### Out of scope
- JSON body parsing / ASGI route — t02
- Callback mock — t03/t04
- Реальные провайдеры eideasy/authentigate — [STORY-IDS-EID-02](../../../../../../backlog-stories/STORY-IDS-EID-02-real-eid-providers.md)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.api.handlers import handle_auth_eid_start; print(handle_auth_eid_start.__name__)"
```
