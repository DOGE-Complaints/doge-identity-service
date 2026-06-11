# Жёсткий аудит исполнения STORY-IDS-PV-05 (Flow API: request/confirm + rate-limit + аудит)

> **Дата:** 2026-06-11
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-PV-05-verification-flow-api`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md) vs фактический код. Исполнена под **EPIC-IDS-10-phone-verification** (alias `EPIC-IDS-PHONE`), pkg-000026, 6 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): Текущая волна pkg-000026, STORY-IDS-PV-05 🟢 (стр.11,43,518-523).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Роуты | `POST /auth/phone/request`, `POST /auth/phone/confirm` (оба `Depends(get_current_user)`) ([asgi_app.py:285-315](../../src/core/api/asgi_app.py)) |
| Оркестраторы | `handle_phone_request` ([handlers.py:425-503](../../src/core/api/handlers.py)), `handle_phone_confirm` ([handlers.py:506-...](../../src/core/api/handlers.py)) |
| Rate-limit | cooldown по `phone_resend_cooldown_s` от `active.created_at` → `RATE_LIMITED` ([handlers.py:449-466](../../src/core/api/handlers.py)) |
| Prefix-gate | `resolve_dial_prefix` → `COUNTRY_NOT_ALLOWED` ([e164.py:33-43](../../src/core/phone/e164.py)) |
| Аудит без PII | `PhoneAuditEvent` (нет сырого номера/кода) ([models.py:91-99](../../src/core/domain/models.py)); `PhoneAuditLogRepository` + in-memory ([contracts.py:93-103](../../src/core/domain/contracts.py), [repositories.py:355-368](../../src/core/infrastructure/repositories.py)) |
| DI | `phone_audit_log_repository`/`sms_sender_registry`/`phone_verification_session_store` через фабрику ([service_factory.py:36,71](../../src/core/infrastructure/service_factory.py), [dependencies.py:32,111](../../src/core/api/dependencies.py), [providers.py:103-119](../../src/core/infrastructure/providers.py)) |
| SMS-текст в ядре | `build_verification_sms_text(code)` ([sms_text.py:4](../../src/core/phone/sms_text.py)) |
| Тесты | [test_phone_verification_flow.py](../../tests/test_phone_verification_flow.py) — 10 |
| **Offline-сюита** | **299 passed, 9 skipped** ✅ (было 289 → +10) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-10, pkg-000026) | Факт | Статус |
|--------------------------------|------|--------|
| t01 phone audit event + repository | `PhoneAuditEvent` (без PII) + `PhoneAuditLogRepository` Protocol + `InMemoryPhoneAuditLogRepository` ([models.py:91-99](../../src/core/domain/models.py), [contracts.py:93-103](../../src/core/domain/contracts.py), [repositories.py:355-368](../../src/core/infrastructure/repositories.py)) | 🟢 |
| t02 phone services DI wiring | реестр/стор/аудит проброшены в `ApiDependencies` через `ServiceFactory`/`providers` ([service_factory.py:36,71](../../src/core/infrastructure/service_factory.py), [dependencies.py:57,111](../../src/core/api/dependencies.py)) | 🟢 |
| t03 handle phone request orchestrator | normalize→prefix-gate→cooldown(`RATE_LIMITED`)→OTP+сессия→`registry.get_active().send`→`{sent,expires_at}`; ошибки→`SmsErrorCode`; аудит ([handlers.py:425-503](../../src/core/api/handlers.py)) | 🟢 |
| t04 handle phone confirm orchestrator | `get_latest_for_confirm`→ phone_hash-сверка→`verify_phone_code`→`attach_phone_verification`(409 при дубле)→аудит ([handlers.py:506-...](../../src/core/api/handlers.py)) | 🟢 |
| t05 asgi routes + offline flow tests | 2 POST-роута (Bearer) + 10 тестов флоу на `TestClient`/Mock | 🟢 |
| t06 story acceptance verification | AC 5/5 (см. §2); pipeline-story `Status: 🟢 Done` (стр.7), индекс t06 🟢 ([bullrun-launch-index.md:523](../tasks/bullrun-launch-index.md)) | 🟢 |
| **STORY-IDS-PV-05** | flow API request/confirm | **🟢 Done** |

Индекс держит эпик корректно: `EPIC-IDS-10 … 🟡 In Progress — PV-01..PV-05 🟢` ([bullrun-launch-index.md:87](../tasks/bullrun-launch-index.md)).

---

## 2. Сверка Acceptance Criteria story (по коду + тестам)

| AC | Факт (код + тест) | Вердикт |
|----|-------------------|---------|
| `POST /auth/phone/request` (валидный JWT, разрешённый префикс) → сессия `started`, SMS через активный провайдер, `expires_at` | [handlers.py:468-503](../../src/core/api/handlers.py); тест `test_phone_request_creates_session_sends_sms_and_returns_expires_at` | ✅ |
| Неразрешённый префикс → `COUNTRY_NOT_ALLOWED`; повтор раньше cooldown → `RATE_LIMITED` (старый код инвалидирован при новом) | prefix-gate + cooldown ([handlers.py:447,449-466](../../src/core/api/handlers.py)); инвалидация — `create_phone_verification_session` → `mark_failed("superseded")` (PV-03); тесты `..._country_not_allowed`, `..._rate_limited_before_cooldown`, `..._after_cooldown_invalidates_previous_code` | ✅ |
| `confirm` верный код → `phone_verified=true`; неверный/просрочка/лимит → `SmsErrorCode`; дубль → 409 | [handlers.py:528-590](../../src/core/api/handlers.py); тесты `..._full_flow_sets_phone_verified`, `..._wrong_code_returns_code_mismatch`, `..._expired_code`, `..._too_many_attempts`, `..._duplicate_number_returns_409` | ✅ |
| Все события в аудите без PII (нет сырого номера/кода) | `PhoneAuditEvent` без полей номера/кода ([models.py:91-99](../../src/core/domain/models.py)); `_log_phone_audit` передаёт только user_id/event_type/provider/success/reason/request_id ([handlers.py:104-...](../../src/core/api/handlers.py)); тест `test_phone_audit_events_contain_no_pii` | ✅ |
| Полный флоу проходит на `MockSmsSender` офлайн | флоу-тесты на `SMS_PROVIDER=mock`; **299 passed** | ✅ |

**Вывод:** все 5 AC выполнены и покрыты тестами (10 dedicated). Session-binding по `supabase_user_id` из JWT, redirect отсутствует (двухшаговый JSON-флоу), как и задумано (отличие от eID).

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F1** | MEDIUM | Doc-stale | Backlog-story `Status: ⚪ Todo` (стр.6) + AC `[ ]` (стр.32-36) — реально 🟢 Done под pkg-000026. Та же рассинхронизация в [`EPIC-IDS-PHONE.md`](../tasks/backlog-stories/phone-verification/EPIC-IDS-PHONE.md) (строка PV-05 = ⚪ Todo). **Как закрыть:** Status ⚪→🟢, AC `[ ]`→`[x]`, строка таблицы EPIC.md PV-05 → 🟢. Рекуррентный паттерн (PV-01..04). | [`STORY-IDS-PV-05...md:6,32-36`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md) |
| **F2** | LOW | Doc-stale | Индекс декларирует «298 pytest offline» ([bullrun-launch-index.md:11](../tasks/bullrun-launch-index.md)), фактически **299 passed** (off-by-one, как PV-01..04/EID-08). **Как закрыть:** синхронизировать число. | [`bullrun-launch-index.md:11`](../tasks/bullrun-launch-index.md) |

Иных материальных findings нет. Наблюдения (severity none, по scope, **не gap**):
- **Новый стор-метод `get_latest_for_confirm`** ([contracts.py:80](../../src/core/domain/contracts.py), [repositories.py:307](../../src/core/infrastructure/repositories.py)) — сверх перечня PV-03. Нужен, чтобы confirm видел и **`failed`**-сессию (после исчерпания попыток) и отдавал `TOO_MANY_ATTEMPTS` ([handlers.py:536-540](../../src/core/api/handlers.py)), тогда как `get_active_by_user` фильтрует только `started`. Корректное расширение под AC3.
- **PV-05 рефакторнул PV-02-утилиту:** `assert_allowed_dial_prefix` теперь тонкая обёртка над новым `resolve_dial_prefix` (longest-match, возвращает префикс для хранения в сессии) ([e164.py:33-46](../../src/core/phone/e164.py)). Старая функция/её тесты сохранены — не orphan, не противоречие; прогрессивное уточнение.
- **Доп. защита в confirm:** сверка `session.phone_hash == hash_secret(e164)` ([handlers.py:543-548](../../src/core/api/handlers.py)) — confirm требует тот же номер, что в request (anti-mixup). Сверх явных AC, усиление.
- **`resolve_dial_prefix` с пустым allowlist** возвращает `e164[:4]`-фолбэк ([e164.py:35](../../src/core/phone/e164.py)); из конфига недостижимо (`_dial_prefixes` гарантирует ≥1 префикс, PV-02). Безвредно.
- **Telnyx/webhook вне scope:** флоу работает на `MockSmsSender`; реальный sender → [PV-06](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md), приём статусов → [PV-07](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md). Не gaps PV-05.

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **299 passed, 9 skipped** (было 289 → +10 flow-тестов), **ожидаемо** |
| `ApiDependencies` | +3 phone-поля (реестр/стор/аудит), опциональные (`| None`) — eID/OAuth-зависимости не сломаны |
| `asgi_app` | +2 роута; eID-callback/`/me`/auth-роуты не тронуты |
| `handlers.py` | новые `handle_phone_*`/`_log_phone_audit`/`_phone_error_response` — аддитивны; eID-хендлеры без изменений |
| `e164.py` | `assert_allowed_dial_prefix` делегирует в `resolve_dial_prefix` — поведение для PV-02-тестов идентично (зелёные) |
| Сеть в offline | нет (`MockSmsSender`, без сетевых клиентов) |
| PV-01..04 / eID / OAuth | не затронуты — сюита зелёная |

Регрессий не выявлено.

---

## 5. Итог

- **STORY-IDS-PV-05 — 🟢 исполнена полно:** двухшаговый JSON-флоу `request`/`confirm` (Bearer JWT, session-binding по `supabase_user_id`), prefix-gate→`COUNTRY_NOT_ALLOWED`, cooldown→`RATE_LIMITED` с инвалидацией прежнего кода, OTP-сессия (PV-03) + `attach_phone_verification` дедуп→409 (PV-04), активный провайдер (PV-01/02) на `MockSmsSender`, отдельный `PhoneAuditEvent` без PII. AC 5/5, 10 тестов. Связал всю phone-цепочку PV-01..04 в HTTP-флоу.
- **Findings:** **F1 (MEDIUM, doc-stale)** — backlog-story + EPIC.md ⚪→🟢 (рекуррентно); **F2 (LOW)** — индекс 298 vs факт 299.
- Наблюдения (`get_latest_for_confirm`; рефактор `assert_allowed_dial_prefix`→`resolve_dial_prefix`; phone_hash-сверка в confirm; Telnyx→PV-06/07) — по scope, не gaps.

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; 6 тасков + story сверены по коду (pipeline-story 🟢, индекс t01–t06 🟢).
- [x] AC 5/5 сверены по коду **и** тестам; обе ветки флоу (request: ok/prefix/rate-limit; confirm: ok/mismatch/expiry/limit/409) покрыты.
- [x] PII-проверка: `PhoneAuditEvent` без полей номера/кода + тест `..._contain_no_pii`; SMS-текст строит ядро.
- [x] Change propagation: phone-сервисы проведены models→contracts→repositories→providers→service_factory→dependencies→asgi_app; рефактор e164 не сломал PV-02-тесты.
- [x] Регрессий нет; 289→299 (+10) объяснён; границы scope (Telnyx→PV-06/07) прослежены.
