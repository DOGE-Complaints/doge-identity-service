# Жёсткий аудит исполнения STORY-IDS-SEC-02 (хэшированные IP/UA в аудит-событиях)

> **Дата:** 2026-06-26
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity. Не предлагаю реализацию — только findings.
> **Предмет:** [`STORY-IDS-SEC-02-audit-ip-ua-hashing`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md) vs фактический код. Исполнена под **EPIC-IDS-12** (pkg-000037), 6 tasks.
> **Контекст:** гэп **G-2b** из [full-audit §3](./identity-backend-full-audit-2026-06-24.md) (IP/UA не хешировались; eID-аудит хардкодил `ip_hash=None`).
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): pkg-000037, SEC-02 🟢 (стр.11,70,125,679-684).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Контекст-хелперы | [`request_context.py`](../../src/core/api/request_context.py) — `client_ip(request, trusted_proxy_count)`, `user_agent(request)` |
| Хэш-обёртка | [`audit_context.py:19-22`](../../src/core/security/audit_context.py) `hash_audit_value` → `hash_secret`; None/empty → None |
| Сборка хэшей из запроса | `audit_hashes_from_request` ([audit_context.py:25-37](../../src/core/security/audit_context.py)) → `AuditHashes(ip_hash, user_agent_hash)` |
| Ключ + proxy | `_audit_hashes_from_request` ([asgi_app.py:63-69](../../src/core/api/asgi_app.py)) — `hashing_key=config.eid_secret`, `trusted_proxy_count=config.rate_limit_trusted_proxy_count` |
| Wiring (оба режима) | `audit=_audit_hashes_from_request(request)` на роутах eid/start, callback, phone/request, phone/confirm ([asgi_app.py:324,353,371,389](../../src/core/api/asgi_app.py)) |
| Модели | `EIDAuditEvent.ip_hash/user_agent_hash` ([models.py:101-102](../../src/core/domain/models.py)); `PhoneAuditEvent.ip_hash/user_agent_hash` ([models.py:116-117](../../src/core/domain/models.py)) |
| Персистентность eID | `ip_hash/user_agent_hash` в строке ([db_supabase.py:202-203,218-219](../../src/core/infrastructure/db_supabase.py)); колонки в [миграции `…3:15-16`](../../supabase/migrations/20260525000003_create_eid_audit_events.sql) + bootstrap | 
| Тесты | [test_audit_ip_ua_hashing.py](../../tests/test_audit_ip_ua_hashing.py) — 4 |
| **Offline-сюита** | **375 passed, 11 deselected** ✅ (совпадает с индексом) |

---

## 1. Актуализация тасков и story (по коду)

| Таск (EPIC-IDS-12, pkg-000037) | Факт | Статус |
|--------------------------------|------|--------|
| t01 phone audit event ip/ua model fields | `PhoneAuditEvent.ip_hash/user_agent_hash` ([models.py:116-117](../../src/core/domain/models.py)) | 🟢 |
| t02 audit ip/ua hmac hashing helper | `hash_audit_value`/`audit_hashes_from_request` ([audit_context.py](../../src/core/security/audit_context.py)) | 🟢 |
| t03 eid audit request-context wiring | eid/start+callback передают `audit=` ([asgi_app.py:324,353](../../src/core/api/asgi_app.py)) | 🟢 |
| t04 phone audit request-context wiring | phone/request+confirm передают `audit=` ([asgi_app.py:371,389](../../src/core/api/asgi_app.py)) | 🟢 |
| t05 offline audit ip/ua hash no-pii tests | 4 теста (HMAC, oба режима, no-raw) | 🟢 |
| t06 story acceptance verification | AC 5/5 (см. §2) | 🟢 |
| **STORY-IDS-SEC-02** | хэш IP/UA в аудите (eID + phone) | **🟢 Done** |

**Индекс корректен:** `EPIC-IDS-12 … SEC-01 🟢; SEC-01b 🟢; SEC-02 🟢; SEC-03 ⚪` ([bullrun-launch-index.md:125](../tasks/bullrun-launch-index.md)); pkg-000037 Done, 375 offline (стр.11).

> **G-2b закрыт.** Остаток G-2 — **G-2a (durable phone-аудит)** — вне SEC-02; принадлежит [PV-09](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md) (документированный split, [EPIC-IDS-SEC.md:29](../tasks/backlog-stories/security-hardening/EPIC-IDS-SEC.md)).

---

## 2. Сверка Acceptance Criteria (по коду + тестам)

| AC | Факт | Вердикт |
|----|------|---------|
| Request-контекст (IP/UA) доходит до аудита для **обоих** режимов (не `None`) | `_audit_hashes_from_request` на 4 роутах ([asgi_app.py:324,353,371,389](../../src/core/api/asgi_app.py)); handler пишет `audit.ip_hash/user_agent_hash` ([handlers.py:136-137,169-170](../../src/core/api/handlers.py)) | ✅ |
| IP/UA только как хэш (`hash_secret`); сырое отсутствует — тестом | `hash_audit_value`→`hash_secret` ([audit_context.py:19-22](../../src/core/security/audit_context.py)); тесты `..._records_hashed_ip_ua_not_raw` (eid+phone) | ✅ |
| `PhoneAuditEvent` получает `ip_hash`/`user_agent_hash` | [models.py:116-117](../../src/core/domain/models.py) | ✅ |
| Инвариант «нет PII в аудите» | тесты `test_eid_start_audit_records_hashed_ip_ua_not_raw`, `test_phone_request_audit_records_hashed_ip_ua_not_raw` | ✅ |
| Алгоритм хэша зафиксирован; спека 16 обновлена при расхождении | HMAC-SHA256 (тест `test_hash_audit_value_uses_hmac_sha256`); [spec 16:148-160](../requirements/16-security-privacy-observability.md) переписан на `HMAC-SHA256 via hash_secret + DOGESTONIA_EID_SECRET` | ✅ |

**Вывод:** все 5 AC выполнены кодом+тестами+доками. IP берётся trusted-proxy-aware (тот же `client_ip`-механизм, что SEC-01 F2), ключ — единый `eid_secret`. Переиспользует `hash_secret` без дублирования крипто.

---

## 3. Findings (severity + как закрыть; без реализации)

Код SEC-02 — без материальных дефектов. Findings — **doc-staleness** (рекуррентный: код 🟢, чекбоксы/состав отстают).

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F1** | MEDIUM | Doc-stale (внутр. противоречие) | Story `Status: 🟢 Done` (стр.6), но **все 5 AC = `[ ]`** (стр.32-36) — при выполненных. **Как закрыть:** проставить AC `[x]`. | [`STORY-IDS-SEC-02...md:32-36`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md) |
| **F2** | MEDIUM | Doc-stale (пакет-индекс) | [`EPIC-IDS-SEC.md:25`](../tasks/backlog-stories/security-hardening/EPIC-IDS-SEC.md) состав SEC-02 = **⚪ Todo** — по факту 🟢 (pkg-000037); bullrun-эпик-строка уже 🟢. **Как закрыть:** SEC-02 → 🟢 Done. | [`EPIC-IDS-SEC.md:25`](../tasks/backlog-stories/security-hardening/EPIC-IDS-SEC.md) |

Наблюдения (severity none/LOW, по scope, **не gaps SEC-02**):
- **O1:** phone-аудит с хэшами пишется только in-memory ([`InMemoryPhoneAuditLogRepository` repositories.py:362](../../src/core/infrastructure/repositories.py)); durable Supabase phone-audit — **PV-09** (G-2a), не SEC-02. eID-аудит уже durable (Supabase, колонки `ip_hash/user_agent_hash` есть).
- **O2:** ключ хэша = `eid_secret` (единый HMAC-секрет для person/phone/IP/UA) — корректно для аудита (некорректируемые, но коррелируемые хэши); согласовано со spec 16.
- **O3:** `client_ip` для аудита наследует trusted-proxy-логику (default `RATE_LIMIT_TRUSTED_PROXY_COUNT=0` → XFF не доверяется) — консистентно с SEC-01.

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **375 passed, 11 deselected** (было 371 → **+4**: audit-hash тесты) |
| Новые модули `request_context.py`, `audit_context.py` | аддитивны |
| Аудит-функции (`handlers.py`) | сигнатура `audit=` уже была (дефолт None) → теперь передаётся реальный контекст; обратная совместимость сохранена |
| eID-аудит (Supabase) | колонки `ip_hash/user_agent_hash` уже существовали (миграция `…3`) — заполняются, не ломая схему |
| OAuth/rate-limit/phone-флоу | не затронуты |

Регрессий не выявлено.

---

## 5. Итог

- **SEC-02 — 🟢 исполнена полно:** IP/UA доходят до аудита для **обоих** режимов (eID + phone), хэшируются HMAC-SHA256 (`hash_secret`, ключ `eid_secret`), сырое не хранится; `PhoneAuditEvent` получил поля; spec 16 синхронизирован. AC 5/5, 4 теста. Таски t01–t06 🟢; индекс корректен.
- **G-2b закрыт.** G-2a (durable phone-аудит) — отдельно в PV-09 (документированный split).
- **Findings — только doc-staleness:** **F1** (story AC `[ ]` при 🟢), **F2** (EPIC-IDS-SEC состав SEC-02 ⚪). Наблюдения O1–O3 — вне AC.
- **Регрессий нет** (375 passed).

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; 6 тасков + story + 5 AC сверены по коду, тестам и докам.
- [x] Data-flow проверен сквозь оба режима (eid/start+callback, phone/request+confirm) до записи `ip_hash/user_agent_hash`.
- [x] AC5 (алгоритм) проверен: HMAC-SHA256 в коде/тесте **и** spec 16 переписан под факт.
- [x] G-2b/G-2a разведены: SEC-02 = хэширование (закрыто), PV-09 = durability (отдельно).
- [x] Регрессий нет; 371→375 (+4) объяснён; индекс 375 = факт.
