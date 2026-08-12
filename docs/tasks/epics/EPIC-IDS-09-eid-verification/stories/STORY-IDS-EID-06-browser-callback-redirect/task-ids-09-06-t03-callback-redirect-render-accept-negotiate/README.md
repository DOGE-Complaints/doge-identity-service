## Task workspace — `task-ids-09-06-t03-callback-redirect-render-accept-negotiate`

- Story: [`../STORY-IDS-EID-06-browser-callback-redirect.md`](../STORY-IDS-EID-06-browser-callback-redirect.md)
- Prerequisite: t01 (`EidCallbackOutcome`), t02 (dynamic route)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000019`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md`](../../../../../../backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md) Scope #2–#4; [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F1)  
---

## Task: implement — callback HTTP presentation: redirect 303, safe fallback, JSON variant

### Цель
На уровне роута преобразовать `EidCallbackOutcome` в HTTP-ответ: браузер по умолчанию → `RedirectResponse(303)` на `return_url` с query-маркерами; безопасный 400 без redirect; `Accept: application/json` → JSON envelope для тестов.

### Почему это важно
F1 🔴: живой eID-флоу требует возврата пользователя в SPA, не JSON-страницы. EID-01 offline-тесты зависят от JSON-варианта.

### Факты из кода
1. [`asgi_app.py:68-69`](../../../../../../../src/core/api/asgi_app.py) — только `_json_envelope`; `RedirectResponse` не импортирован [`asgi_app.py:10`](../../../../../../../src/core/api/asgi_app.py).
2. [`handlers.py:123-140`](../../../../../../../src/core/api/handlers.py) — `return_url` validated на start; хранится в сессии.
3. [`return_url.py`](../../../../../../../src/core/security/return_url.py) — allowlist helpers (redirect target уже trusted).
4. [`test_eid_verification_flow.py:176-206`](../../../../../../../tests/test_eid_verification_flow.py) — callback без `Accept` ожидает JSON 200 (потребует `Accept: application/json` после default=redirect).

### Gap / Проблема
Нет redirect render; нет content negotiation; open-redirect risk если редиректить без `return_url`.

### AC/DoD
- [x] (P0) Успех в браузере → `303` на `return_url` с `?eid_status=verified` (или `&` если URL уже с query).
- [x] (P0) Ошибка provider/session с известным `return_url` → `303` с `?eid_status=error&eid_error=<EidErrorCode.value>` (canonical code из EID-05).
- [x] (P0) Неизвестная сессия / отсутствует безопасный `return_url` → 400 JSON (без redirect на неизвестный origin) — story AC #3.
- [x] (P0) `Accept: application/json` → JSON envelope + `json_status` из outcome (EID-01 regression path).
- [x] (P1) Story AC #2, #3 traceability.

### Где менять код
- `doge-identity-service/src/core/api/asgi_app.py` (render helper + route handler)
- При необходимости: `doge-identity-service/src/core/api/handlers.py` (JSON body builder из outcome для negotiate path)

### Out of scope
- Новые error codes — EID-05
- Offline redirect tests — t04
- Runtime docs — t05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_eid_verification_flow.py -m "not live_integration" -q -k callback --tb=short
# Manual smoke (after implement):
# curl -sI 'http://localhost:8000/auth/mock/callback?session_id=...' | grep -i location
# curl -sH 'Accept: application/json' 'http://localhost:8000/auth/mock/callback?session_id=...' | jq .data.status
```
