# STORY-IDS-SEC-02 — Хэшированные IP/UA в аудит-событиях (eID + phone)

## Meta
- **Key:** `STORY-IDS-SEC-02-audit-ip-ua-hashing`
- **Parent Epic:** [`../../EPIC-IDS-12-security-hardening.md`](../../EPIC-IDS-12-security-hardening.md)
- **Epic alias (код/backlog):** `EPIC-IDS-SEC` · [`EPIC-IDS-SEC`](../../../../backlog-stories/security-hardening/EPIC-IDS-SEC.md)
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md`](../../../../backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md)
- **Decision Ref:** [`../../../../backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md`](../../../../backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md); [`identity-backend-full-audit-2026-06-24.md`](../../../../../analysis/identity-backend-full-audit-2026-06-24.md) §3 G-2b
- **Источник:** [`identity-backend-full-audit-2026-06-24.md`](../../../../../analysis/identity-backend-full-audit-2026-06-24.md) — гэп **G-2** (часть G-2b: IP/UA-хэш; HIGH, кросс-режимный eID+phone)
- **Зависит от:** [STORY-IDS-SEC-01](../STORY-IDS-SEC-01-rate-limiting/STORY-IDS-SEC-01-rate-limiting.md) 🟢 (как источник доступа к request-контексту IP/UA в сквозном слое). Пересекается с durable phone-аудитом **PV-09** ([`EPIC-IDS-PHONE`](../../../../backlog-stories/phone-verification/EPIC-IDS-PHONE.md)).

## Зачем простыми словами
Когда что-то идёт не так (подбор кодов, абьюз eID), важно понять «с какого устройства/адреса» это шло — но **без хранения сырых персональных данных**. Спека требует, чтобы в аудит-событиях лежали **хэши** IP и User-Agent (не сам IP, не сам UA). Сейчас этого нет: eID-аудит жёстко пишет `None`, а у phone-события вообще нет полей под IP/UA. Цель стори — на уровне **требований** зафиксировать: request-контекст (IP/UA) должен доходить до аудит-слоя и сохраняться в хэшированном виде, для **обоих** режимов (eID и телефон), переиспользуя существующий механизм хэширования.

## Scope (только требования)
- **Проброс request-контекста:** реальные IP и User-Agent запроса должны доходить до функций логирования аудита (для eID и для phone). Сейчас они туда не передаются вовсе.
- **Хэширование перед хранением:** IP и UA сохраняются **только как HMAC-хэш**, никогда в сыром виде. Переиспользовать существующий хелпер [`hash_secret(plaintext, key=…)`](../../../../../../src/core/security/hashing.py) (HMAC-SHA256), а не вводить новый примитив. (Спека 16 в примере показывает `sha256` без ключа — требование: согласовать на HMAC-с-ключом, как уже принято в сервисе для phone-хэшей; зафиксировать выбор и обновить спеку при расхождении.)
- **Модель данных аудита:** требование — аудит-события (eID и phone) должны нести поля `ip_hash` / `user_agent_hash`. Для eID поля уже есть в модели, но всегда `None`; для phone полей **нет вовсе** — их нужно добавить (требование к модели/хранилищу, конкретная миграция — реализация / пересекается с PV-09).
- **Оба режима обязательны:** eID-аудит и phone-аудит покрываются одинаково (кросс-режимность — суть G-2b).
- **Без PII:** сохраняем только хэши; сырой IP/UA и сырой телефон/код в аудит не попадают (сохранить существующий инвариант).

## Вне scope
- **Durable-хранилище phone-аудита** (таблица `phone_audit_events`, переключение с in-memory на Supabase) — это durable-часть G-2, отдельная стори **PV-09** в [`EPIC-IDS-PHONE`](../../../../backlog-stories/phone-verification/EPIC-IDS-PHONE.md). Здесь — только проброс+хэширование IP/UA; модель-поля согласуются с PV-09, чтобы не разойтись.
- Конкретная SQL-миграция, формат колонок, выбор солта/ключа хэша — реализация.
- Хранение «сырых» IP/UA для форензики — намеренно нет (PII-минимизация).

## Точки в коде (текущее состояние)
- **eID-аудит хардкодит отсутствие IP/UA:** [`handlers.py:162-163`](../../../../../../src/core/api/handlers.py) — в `EIDAuditEvent` передаётся `ip_hash=None, user_agent_hash=None` (поля модели есть, но всегда пустые); сам `_log_eid_audit` ([handlers.py:150-166](../../../../../../src/core/api/handlers.py)) не принимает request-контекста.
- **phone-аудит-событие не имеет полей под IP/UA:** [`models.py:92-101`](../../../../../../src/core/domain/models.py) — `PhoneAuditEvent` содержит `id/supabase_user_id/event_type/provider/success/failure_reason/request_id/created_at` и **никаких** `ip_hash`/`user_agent_hash`.
- **Механизм хэширования существует и готов к переиспользованию:** [`hashing.py:9-11`](../../../../../../src/core/security/hashing.py) — `hash_secret(plaintext, *, key)` = HMAC-SHA256 hex.
- **Спека требует хэшированные IP/UA:** [`16:144-159`](../../../../../requirements/16-security-privacy-observability.md) (сигнатура с `ip_address`/`user_agent`, «Hashes IP and User-Agent before storage») и acceptance [`16:229`](../../../../../requirements/16-security-privacy-observability.md).

## Acceptance Criteria
- [x] Request-контекст (IP, User-Agent) доходит до аудит-функций для **обоих** режимов — eID и phone (а не передаётся `None`, как сейчас в [`handlers.py:162-163`](../../../../../../src/core/api/handlers.py)).
- [x] IP и UA сохраняются исключительно как хэш (через [`hash_secret`](../../../../../../src/core/security/hashing.py)); сырой IP/UA в хранилище аудита отсутствует — проверяемо тестом.
- [x] `PhoneAuditEvent` ([`models.py:92`](../../../../../../src/core/domain/models.py)) получает поля `ip_hash`/`user_agent_hash`, согласованные с eID-аудитом и со стори PV-09.
- [x] Инвариант «нет PII в аудите» сохранён: ни сырого IP/UA, ни сырого телефона/кода — тест подтверждает.
- [x] Выбор алгоритма хэша (HMAC-с-ключом vs sha256 из примера спеки 16) зафиксирован; при расхождении со спекой 16 — спека обновлена под фактический выбор.

## Парадигма-якорь
[`16-security-privacy-observability.md`](../../../../../requirements/16-security-privacy-observability.md) (hashed IP/UA в аудите, PII-минимизация), [`runtime-docs/04-security.md`](../../../../../runtime-docs/04-security.md) (аудит без PII).
