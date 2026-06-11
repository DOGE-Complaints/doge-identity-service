# Жёсткий аудит исполнения STORY-IDS-PV-03 (OTP-движок + сессия верификации)

> **Дата:** 2026-06-11
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-PV-03-otp-engine-session`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md) vs фактический код. Исполнена под **EPIC-IDS-10-phone-verification** (alias `EPIC-IDS-PHONE`), pkg-000024, 6 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): Текущая волна pkg-000024, STORY-IDS-PV-03 🟢 (стр.11,39,500-505).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Модель сессии | `PhoneVerificationSession` (12 полей: id/user/phone_hash/dial_prefix/code_hash/status/attempts/created_at/expires_at/provider/provider_message_id) ([models.py:63-75](../../src/core/domain/models.py)) |
| Модель результата | `PhoneVerificationResult(provider, dial_prefix, subject_hash, verified_at)` ([models.py:78-82](../../src/core/domain/models.py)) |
| Контракт стора | `PhoneVerificationSessionStore` (`create`/`get_by_id`/`get_active_by_user`/`replace`/`mark_consumed`/`mark_failed`/`expire_pending`) ([contracts.py](../../src/core/domain/contracts.py)) |
| In-memory стор | `InMemoryPhoneVerificationSessionStore` ([repositories.py:195-247](../../src/core/infrastructure/repositories.py)) |
| OTP-движок | `create_phone_verification_session`, `verify_phone_code` ([otp_engine.py](../../src/core/phone/otp_engine.py)) |
| Криптослучайность | `secrets.choice` ([otp_engine.py:23-24](../../src/core/phone/otp_engine.py)); сверка — `hmac.compare_digest` ([otp_engine.py:27-29](../../src/core/phone/otp_engine.py)) |
| Тесты | [test_phone_otp_engine.py](../../tests/test_phone_otp_engine.py) — 7; [test_phone_verification_session_store.py](../../tests/test_phone_verification_session_store.py) — 5 |
| **Offline-сюита** | **281 passed, 9 skipped** ✅ (было 269 → +12) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-10, pkg-000024) | Факт | Статус |
|--------------------------------|------|--------|
| t01 phone verification session + result models | `PhoneVerificationSession` + `PhoneVerificationResult` (frozen dataclasses) ([models.py:63-82](../../src/core/domain/models.py)) | 🟢 |
| t02 phone verification session store in-memory | контракт `PhoneVerificationSessionStore` + `InMemoryPhoneVerificationSessionStore` (`get_active_by_user` = latest started, не просроченный) ([contracts.py](../../src/core/domain/contracts.py), [repositories.py:195-247](../../src/core/infrastructure/repositories.py)); тесты store (5) | 🟢 |
| t03 otp generate + session create + invalidate | `create_phone_verification_session`: `secrets`-код длины `phone_code_length`, `code_hash=hash_secret(code,key)`, `expires_at=now+ttl`; инвалидация прежнего активного через `mark_failed("superseded")` ([otp_engine.py:32-64](../../src/core/phone/otp_engine.py)) | 🟢 |
| t04 otp verify + attempts + expiry + result | `verify_phone_code`: expiry→`CODE_EXPIRED`, match→`mark_consumed`+`PhoneVerificationResult`, mismatch→`attempts++`+`CODE_MISMATCH`, ≥лимит→`status=failed`+`TOO_MANY_ATTEMPTS` ([otp_engine.py:67-132](../../src/core/phone/otp_engine.py)) | 🟢 |
| t05 offline phone otp + session tests | 7 engine + 5 store = 12 тестов | 🟢 |
| t06 story acceptance verification | AC 6/6 (см. §2); pipeline-story `Status: 🟢 Done` (стр.7), индекс t06 🟢 ([bullrun-launch-index.md:505](../tasks/bullrun-launch-index.md)) | 🟢 |
| **STORY-IDS-PV-03** | OTP-движок + сессия | **🟢 Done** |

Индекс держит эпик корректно: `EPIC-IDS-10 … 🟡 In Progress — PV-01 🟢; PV-02 🟢; PV-03 🟢` ([bullrun-launch-index.md:81](../tasks/bullrun-launch-index.md)).

---

## 2. Сверка Acceptance Criteria story (по коду + тестам)

| AC | Факт (код + тест) | Вердикт |
|----|-------------------|---------|
| `PhoneVerificationSession` + store (in-memory + supabase-совместимый интерфейс) с `attempts` | модель ([models.py:63-75](../../src/core/domain/models.py)); Protocol-контракт + in-memory ([contracts.py](../../src/core/domain/contracts.py), [repositories.py:195](../../src/core/infrastructure/repositories.py)); тесты `test_create_and_get_by_id`, `test_replace_updates_attempts` | ✅ |
| OTP криптослучайно, хранится только хэш; код не логируется | `secrets.choice` ([otp_engine.py:24](../../src/core/phone/otp_engine.py)); хранится `code_hash` (не plaintext); тесты `test_create_returns_plaintext_code_and_stores_hash_only` (`code_hash != code`), `test_plaintext_code_not_logged` (`code not in caplog.text`) | ✅ |
| Сверка: верный→ok; неверный→`CODE_MISMATCH`+`attempts++`; ≥лимит→`TOO_MANY_ATTEMPTS`; просрочка→`CODE_EXPIRED` | [otp_engine.py:86-132](../../src/core/phone/otp_engine.py); тесты `test_verify_success...`, `test_verify_mismatch_increments_attempts`, `test_verify_too_many_attempts`, `test_verify_expired_code` (коды сверены `is SmsErrorCode.*`) | ✅ |
| Повторный `request` инвалидирует прежний код пользователя | `get_active_by_user`→`mark_failed("superseded")` ([otp_engine.py:45-47](../../src/core/phone/otp_engine.py)); тест `test_repeat_create_invalidates_previous_session` (первый → `status=failed`, verify первым кодом → `SmsSenderError`) | ✅ |
| `subject_hash = hash_secret(e164)` без провайдер-префикса | [otp_engine.py:96](../../src/core/phone/otp_engine.py); тест `test_verify_success_returns_subject_hash_without_provider_prefix` (`subject_hash == hash_secret(e164, key)`, `":" not in subject_hash`) | ✅ |
| Offline-тесты: успех/несовпадение/просрочка/лимит/повтор-инвалидация | 12 тестов, **281 passed** | ✅ |

**Вывод:** все 6 AC выполнены и покрыты тестами (12). Ядро берёт на себя то, что у eID делал внешний провайдер (генерация/сверка/срок/попытки) — provider-agnostic, без `SessionSecretBox` (по scope не нужен, код одноразовый и хэшируется).

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F1** | MEDIUM | Doc-stale | Backlog-story `Status: ⚪ Todo` (стр.6) + AC `[ ]` (стр.33-38) — реально 🟢 Done под pkg-000024. Та же рассинхронизация в [`EPIC-IDS-PHONE.md`](../tasks/backlog-stories/phone-verification/EPIC-IDS-PHONE.md) (строка PV-03 = ⚪ Todo). **Как закрыть:** Status ⚪→🟢, AC `[ ]`→`[x]`, строка таблицы EPIC.md PV-03 → 🟢. Рекуррентный паттерн (PV-01/PV-02). | [`STORY-IDS-PV-03...md:6,33-38`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md) |
| **F2** | LOW | Doc-stale | Индекс декларирует «280 pytest offline» ([bullrun-launch-index.md:11](../tasks/bullrun-launch-index.md)), фактически **281 passed** (off-by-one, как PV-01/PV-02/EID-08). **Как закрыть:** синхронизировать число. | [`bullrun-launch-index.md:11`](../tasks/bullrun-launch-index.md) |
| **F3** | LOW | Consistency | Терминальный статус при просрочке **на верификации** ≠ при sweep'е. `verify_phone_code` на истёкшем коде зовёт `mark_failed(session_id, "expired")` → `status="failed"` ([otp_engine.py:87](../../src/core/phone/otp_engine.py), [repositories.py:231-236](../../src/core/infrastructure/repositories.py)), тогда как `expire_pending` ставит `status="expired"` ([repositories.py:245](../../src/core/infrastructure/repositories.py)). Один и тот же домен-факт «код истёк» даёт два разных статуса. Оба терминальные/не-`started`, AC об ошибке `CODE_EXPIRED` соблюдён — функционально не gap, но семантика статуса расходится. **Как закрыть:** на expiry-пути в verify использовать `expired`-переход (а не `mark_failed`), либо задокументировать, что `failed` поглощает `expired` на verify-пути. | [`otp_engine.py:86-88`](../../src/core/phone/otp_engine.py) |

Иных материальных findings нет. Наблюдения (severity none, по scope, **не gap**):
- **`mark_failed` игнорирует `reason`** (`del reason`, [repositories.py:232](../../src/core/infrastructure/repositories.py)) — «superseded»/«expired» не персистятся. Story не требует хранить причину; для in-memory приемлемо.
- **`phone_hash` == `subject_hash`** (оба `hash_secret(e164, key)` с одним ключом, [otp_engine.py:53,96](../../src/core/phone/otp_engine.py)) — значения совпадают; избыточно по именам, но безвредно (разные семантические роли: хранение vs результат).
- **HMAC-ключ — `config.eid_secret`** ([otp_engine.py:19-20](../../src/core/phone/otp_engine.py)). Story говорила «переиспользуем `hashing.py`»; pepper берётся из eID-секрета (единый HMAC-pepper, не Fernet). По scope — допустимо; отдельного phone-ключа story не требовала.
- **Контракт стора добавил `replace`** сверх перечня в scope story (create/get_by_id/get_active_by_user/mark_consumed/mark_failed/expire_pending) — нужен для инкремента `attempts` на frozen-модели; разумное расширение, покрыт тестом `test_replace_updates_attempts`.
- **Движок ещё не подключён к HTTP-флоу** (request/confirm) — **вне scope PV-03** (оркестрация → [PV-05](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md)); запись флага профиля/дедуп → [PV-04](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md). Supabase-реализация стора пока только in-memory (контракт supabase-совместим, конкретная репа — позже).

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **281 passed, 9 skipped** (было 269 → +12 OTP/store тестов), **ожидаемо** |
| Новые модели/контракт/стор | аддитивные; `VerificationSession`/`VerificationSessionStore` (eID) не затронуты — отдельные классы рядом |
| `otp_engine.py` | новый модуль; импортирует `hashing.py`/`config`/`models`/`contracts` read-only |
| `secrets`/`hmac.compare_digest` | constant-time сверка; код не пишется в лог (тест `caplog`) |
| Сеть в offline | нет |
| eID/OAuth/phone-config (PV-01/02) | не затронуты — сюита зелёная |

Регрессий не выявлено.

---

## 5. Итог

- **STORY-IDS-PV-03 — 🟢 исполнена полно:** `PhoneVerificationSession`/`PhoneVerificationResult` + Protocol-стор (+in-memory), OTP-движок (`secrets`-генерация, `hash_secret`-хранение, TTL, `hmac.compare_digest`-сверка, `attempts`-лимит→`TOO_MANY_ATTEMPTS`, expiry→`CODE_EXPIRED`, mismatch→`CODE_MISMATCH`), инвалидация прежней сессии, `subject_hash` без провайдер-префикса. AC 6/6, 12 тестов.
- **Findings:** **F1 (MEDIUM, doc-stale)** — backlog-story + EPIC.md ⚪→🟢 (рекуррентно); **F2 (LOW)** — индекс 280 vs факт 281; **F3 (LOW, consistency)** — expiry-на-verify даёт `failed`, sweep — `expired` (расхождение терминального статуса).
- Наблюдения (`reason` не персистится; `phone_hash`==`subject_hash`; ключ=`eid_secret`; `replace` сверх scope; флоу→PV-05/04) — по scope, не gaps.

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; 6 тасков + story сверены по коду (pipeline-story 🟢, индекс t01–t06 🟢).
- [x] AC 6/6 сверены по коду **и** тестам; 4 ветки verify (ok/mismatch/limit/expiry) + invalidate + no-log проверены.
- [x] Регрессий нет; 269→281 (+12) объяснён; eID-сессия (VerificationSession) не затронута.
- [x] Границы scope прослежены: HTTP-флоу→PV-05, флаг/дедуп→PV-04, supabase-стор позже (не gaps PV-03).
- [x] F3 (расхождение `failed`/`expired`) пойман сверкой verify-пути с `expire_pending`; классифицирован LOW (оба терминальные, AC по коду ошибки соблюдён).
