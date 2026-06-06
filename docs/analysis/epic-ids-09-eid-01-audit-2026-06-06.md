# Жёсткий аудит исполнения STORY-IDS-EID-01 (eID-флоу: старт, callback, orchestration)

> **Дата:** 2026-06-06
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-EID-01-eid-verification-flow`](../tasks/backlog-stories/STORY-IDS-EID-01-eid-verification-flow.md) vs фактический код. Исполнена под **EPIC-IDS-09-eid-verification** (pkg-000015), 6 tasks (story-файл всё ещё помечен `EPIC-IDS-EID`).
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): EPIC-IDS-09, task queue t01–t06.

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| `/auth/eid/start` → хендлер | `handle_auth_eid_start` (не stub) — [`handlers.py:114-173`](../../src/core/api/handlers.py); роут пробрасывает body — [`asgi_app.py:196-212`](../../src/core/api/asgi_app.py) |
| `/auth/mock/callback` → хендлер | `handle_auth_eid_callback` — [`handlers.py:189-330`](../../src/core/api/handlers.py); роут [`asgi_app.py:238-247`](../../src/core/api/asgi_app.py) |
| `get_by_id` (контракт + обе реализации) | [`contracts.py:48`](../../src/core/domain/contracts.py), [`repositories.py:158`](../../src/core/infrastructure/repositories.py), **[`db_supabase.py:489`](../../src/core/infrastructure/db_supabase.py)** — нет интеграционного разрыва |
| Тесты флоу | [`test_eid_verification_flow.py`](../../tests/test_eid_verification_flow.py) — 5 e2e |
| **Offline-сюита** | **211 passed, 10 deselected** ✅ (было 206 → +5 eID-тестов) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-09, pkg-000015) | Факт | Статус |
|--------------------------------|------|--------|
| t01 handle auth eid start orchestration | `handle_auth_eid_start`: validate return_url → `registry.get_active` → `start_flow` → audit started → 200 {redirect_url, session_id, expires_at} ([`handlers.py:114-173`](../../src/core/api/handlers.py)) | 🟢 |
| t02 asgi eid start wire body | роут извлекает `return_url/return_context/requested_action` из тела (`_eid_start_payload_from_request`) и передаёт ([`asgi_app.py:196-212`](../../src/core/api/asgi_app.py)) | 🟢 |
| t03 mock callback orchestration | `handle_auth_eid_callback` + роут `/auth/mock/callback` (`provider_name="mock"`, raw_params) | 🟢 |
| t04 session lifecycle + audit events | consumed→already_consumed; failed/expired→400; expired→mark_failed; provider_error→mark_failed; conflict→409; success→mark_consumed; аудит на каждом шаге ([`handlers.py:224-325`](../../src/core/api/handlers.py)) | 🟢 |
| t05 mock eid flow offline tests | 5 e2e: start / verify+/me / replay-idempotent / expired / conflict-409 | 🟢 |
| t06 story acceptance verification | AC 6/6 (см. §2) | 🟢 |
| **STORY-IDS-EID-01** | флоу реализован end-to-end на mock | **🟢 Done** |

Индекс ([`bullrun-launch-index.md:51`](../tasks/bullrun-launch-index.md)) держит эпик `🟡 In Progress — EID-01 🟢; EID-02 backlog` — корректно.

---

## 2. Сверка Acceptance Criteria story

| AC | Факт (код + тест) | Вердикт |
|----|-------------------|---------|
| `POST /auth/eid/start` → сессия `started` + redirect | start_flow создаёт сессию (mock), хендлер отдаёт `redirect_url`; тест `test_eid_start_creates_session_and_returns_redirect` ([`:58-87`](../../tests/test_eid_verification_flow.py)) проверяет `status=started`, `session_id`, audit | ✅ |
| callback с валидным state → `eid_verified=true` + `verified_person_hash`/`eid_verified_at` | `attach_eid_verification` + hash; тест `test_mock_callback_verifies_profile_and_me_reflects_status` (через `/me`: `eid_verified=true`, `eid_verified_at`, `eid_provider=mock`) | ✅ |
| Повторный callback / просрочка → не перезаписывает терминальный статус | consumed→`already_consumed`; expired→400 `eid_session_expired`; тесты `..._replay_is_idempotent`, `..._expired_session_does_not_verify_profile` | ✅ |
| Конфликт `verified_person_hash` → `ProfileConflictError`/409 | `except ProfileConflictError → 409`; тест `..._profile_hash_conflict_returns_409` | ✅ |
| Каждое событие в `eid_audit_events` без PII | `_log_eid_audit` на started/failed(expired/provider_error/conflict)/success; `ip_hash=None`, `user_agent_hash=None` ([`handlers.py:107-108`](../../src/core/api/handlers.py)) | ✅ |
| Полный флоу на mock офлайн-тестом | 5 e2e через `TestClient` (in_memory) | ✅ |

**Вывод:** все 6 AC выполнены и покрыты тестами. Принцип session-binding соблюдён: callback берёт `supabase_user_id` из записи сессии ([`handlers.py:290`](../../src/core/api/handlers.py)), не из браузерной сессии (callback — публичный, без `get_current_user`).

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| F1 | MEDIUM | Doc-stale | backlog-story помечена `⚪ Todo` / эпик `EPIC-IDS-EID`; реально 🟢 Done под `EPIC-IDS-09`. Секция «Точки в коде» утверждает «Заглушки: /auth/eid/start (171-181)» — теперь ложно (реализовано) | [`STORY-IDS-EID-01...md:5-6,24`](../tasks/backlog-stories/STORY-IDS-EID-01-eid-verification-flow.md) |
| F2 | LOW | Security-observation | `verified_person_hash` считается с **пустым HMAC-ключом**, если `DOGESTONIA_EID_SECRET` не задан: `key=deps.config.eid_secret or ""` — в `demo` секрет может отсутствовать → хэш без pepper. В `pilot` секрет обязателен ([`schema.py`](../../src/core/config/schema.py) pilot_required), так что enforced только там | [`handlers.py:283-286`](../../src/core/api/handlers.py) |
| F3 | LOW | Robustness | `return_context`/`requested_action` не валидируются против enum перед персистом. На `in_memory` — сохраняются как есть; на `supabase` БД-CHECK ([миграция сессий](../../supabase/migrations/20260525000002_create_eid_verification_sessions.sql)) отклонит чужое значение → необработанная ошибка PostgREST. Вне AC (scope = «прокинуть флаг»), но потенциальный 500 на supabase | [`handlers.py:152-157`](../../src/core/api/handlers.py) |

> F2/F3 — наблюдения по устойчивости, **не нарушают AC** (AC не требуют непустого secret или enum-валидации). F1 — единственный материальный (документный).

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **211 passed** (было 206 → +5 eID-тестов), **ожидаемо** |
| `/auth/eid/start` 501→200 | поведенческая смена, согласована со story — не регресс |
| `/auth/mock/callback` 501→200/400/409 | реализация callback — не регресс |
| `/auth/eideasy/callback`, `/auth/authentigate/callback` | по-прежнему 501 (`handle_public_stub`) — **ожидаемо**, scope EID-02 |
| Интеграционный контракт `get_by_id` | присутствует в обеих реализациях — без разрыва |
| return_url-валидация (CLEANUP-02) | переиспользована в `handle_auth_eid_start` ([`handlers.py:123-132`](../../src/core/api/handlers.py)) — согласованно |

Регрессий не выявлено.

---

## 5. Итог

- **STORY-IDS-EID-01 — 🟢 исполнена полно и корректно:** старт + mock-callback + orchestration (session lifecycle, conflict 409, audit без PII) реализованы и покрыты 5 e2e-тестами; AC 6/6; `get_by_id` есть и в Supabase-реализации (без интеграционного разрыва); session-binding соблюдён.
- **Материальный finding один — F1 (doc-stale backlog-story).** F2/F3 — LOW-наблюдения по устойчивости вне AC.
- Это первая **функциональная** story после cleanup-волны; eID-флоу теперь рабочий на mock, реальные провайдеры — EID-02.

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; статусы тасков сверены по коду.
- [x] Интеграционный контракт (`get_by_id` cross-impl) проверен отдельно — разрыва нет.
- [x] AC сверены по коду **и** тестам (не только по существованию функций).
- [x] Регрессий нет; 206→211 объяснён.
- [x] F2/F3 явно отделены от AC (наблюдения, не gap-нарушения).
