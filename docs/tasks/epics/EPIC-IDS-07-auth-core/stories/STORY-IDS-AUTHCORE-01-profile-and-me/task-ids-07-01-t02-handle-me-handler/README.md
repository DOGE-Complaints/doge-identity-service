## Task workspace — `task-ids-07-01-t02-handle-me-handler`

- Story: [`../STORY-IDS-AUTHCORE-01-profile-and-me.md`](../STORY-IDS-AUTHCORE-01-profile-and-me.md)
- Prerequisite: [`../task-ids-07-01-t01-missing-profile-behavior-decision/README.md`](../task-ids-07-01-t01-missing-profile-behavior-decision/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000009`  
**Skill declared:** python-pro  
---

## Task: implement — `handle_me` handler with profile lookup

### Цель
Добавить `handle_me` в [`handlers.py`](../../../../../../../src/core/api/handlers.py): по `UserClaims.supabase_user_id` читать профиль через `deps.profile_repository`, применить решение t01 при `None`.

### Почему это важно
Заменяет заглушку 501 — первый рабочий защищённый маршрут identity (story «Зачем простыми словами»).

### Факты из кода
1. [`handlers.py:40-51`](../../../../../../../src/core/api/handlers.py) — `handle_me_stub` → 501, `next_epic="EPIC-IDS-AUTH-CORE"`.
2. [`contracts.py:24-25`](../../../../../../../src/core/domain/contracts.py) — `ProfileRepository.get_by_supabase_user_id`.
3. [`dependencies.py:45,97`](../../../../../../../src/core/api/dependencies.py) — `profile_repository` всегда заполнен при успешном `provide_service_factory` ([`providers.py:59-79`](../../../../../../../src/core/infrastructure/providers.py)).
4. [`models.py:16-19`](../../../../../../../src/core/domain/models.py) — `UserClaims.supabase_user_id`.
5. [`envelope.py:6-7`](../../../../../../../src/core/api/envelope.py) — `build_success_envelope`.

### Gap / Проблема
Нет runtime `handle_me`; только stub.

### AC/DoD
- [x] (P0) Функция `handle_me(deps, *, current_user, trace_id) -> tuple[dict, int]` существует и использует `deps.profile_repository`.
- [x] (P0) При отсутствии профиля — поведение по решению t01.
- [x] (P0) Возвращает 200 + `build_success_envelope` (тело делегирует t03 или inline минимум `supabase_user_id`, `eid_verified`).
- [x] (P1) `handle_me_stub` остаётся до t04 или помечен deprecated — маршрут переключается в t04.

### Где менять код
- `doge-identity-service/src/core/api/handlers.py`

### Out of scope
- Wiring `/me` в asgi — t04
- Полная сериализация payload / права — t03
- Тесты — t05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.api.handlers import handle_me; print(handle_me.__name__)"
```
