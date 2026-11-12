# Отчёт об исправлении findings STORY-IDS-PV-03 (F1/F2/F3)

> **Дата:** 2026-06-11
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — изменения с `file:line`, до/после, регрессии, критерии успеха.
> **Источник findings:** [`epic-ids-10-pv-03-audit-2026-06-11.md`](./epic-ids-10-pv-03-audit-2026-06-11.md) §3.
> **Итог:** все 3 findings закрыты; offline **281 passed, 9 skipped** (без регрессий).

## Сводка

| ID | Severity | Тип | Статус | Суть фикса |
|----|----------|-----|--------|-----------|
| F1 | MEDIUM | Doc-stale | 🟢 Закрыт | Status/AC backlog-story + строка EPIC.md → 🟢 Done |
| F2 | LOW | Doc-stale | 🟢 Закрыт | Индекс «280 offline» → «281» (факт) |
| F3 | LOW | Consistency | 🟢 Закрыт | Expiry-на-verify теперь ставит `expired`, не `failed` (код + тест) |

---

## F3 — расхождение терминального статуса (код)

**Проблема:** `verify_phone_code` на истёкшем коде звал `store.mark_failed(session_id, "expired")` → `status="failed"`, тогда как фоновый `expire_pending` ставит `status="expired"`. Один домен-факт «код истёк» давал два разных статуса.

**Решение:** введён отдельный переход `mark_expired` (зеркало `mark_consumed`), expiry-путь verify переключён на него.

### Изменения (3 файла кода + 1 тест)

**1. Контракт** — [`contracts.py:72`](../../src/core/domain/contracts.py): в Protocol `PhoneVerificationSessionStore` добавлен метод.
```python
def mark_failed(self, session_id: str, reason: str) -> None: ...

def mark_expired(self, session_id: str) -> None: ...   # ← добавлено

def expire_pending(self, now: datetime) -> int: ...
```

**2. In-memory стор** — [`repositories.py:238-242`](../../src/core/infrastructure/repositories.py): реализация (зеркало `mark_consumed`, идемпотентна по отсутствию сессии).
```python
def mark_expired(self, session_id: str) -> None:
    session = self._by_id.get(session_id)
    if session is None:
        return
    self._by_id[session_id] = dataclasses.replace(session, status="expired")
```

**3. OTP-движок** — [`otp_engine.py:87`](../../src/core/phone/otp_engine.py): expiry-путь verify.
```python
# До:
if session.expires_at < current:
    store.mark_failed(session_id, "expired")     # → status="failed"
    raise SmsSenderError(..., code=SmsErrorCode.CODE_EXPIRED)
# После:
if session.expires_at < current:
    store.mark_expired(session_id)               # → status="expired"
    raise SmsSenderError(..., code=SmsErrorCode.CODE_EXPIRED)
```

**4. Тест** — [`test_phone_otp_engine.py` `test_verify_expired_code`](../../tests/test_phone_otp_engine.py): усилен ассертом статуса (код ошибки уже проверялся).
```python
assert exc_info.value.code is SmsErrorCode.CODE_EXPIRED
assert store.get_by_id(session.id) is not None
assert store.get_by_id(session.id).status == "expired"   # ← добавлено
```

### Согласованность изменений (analysis.mdc — change propagation)
- **Все реализации `PhoneVerificationSessionStore` покрыты:** единственная конкретная реализация — `InMemoryPhoneVerificationSessionStore` ([repositories.py:195](../../src/core/infrastructure/repositories.py)). **Supabase-стора для phone ещё нет** — класс `db_supabase.py:462-524` это `SupabaseVerificationSessionStore` (**eID**, отдельная таблица `eid_verification_sessions`), он реализует `VerificationSessionStore`, а не phone-контракт. Когда появится Supabase phone-стор (после PV-03), он унаследует `mark_expired` из Protocol — фикс будущему не противоречит.
- **`@runtime_checkable` Protocol** не сломан: in-memory реализует полный набор методов (проверено зелёной сюитой + grep'ом проводки).
- Семантика `expired` уже существовала в кодовой базе (`expire_pending` + модель `status` enum `started|consumed|failed|expired`) — фикс приводит verify-путь к тому же словарю, без нового состояния.

---

## F1 — рассинхронизация статусов (doc-stale)

Backlog-story и таблица эпика отражали `⚪ Todo`, хотя стори 🟢 Done (pkg-000024).

| Файл | До | После |
|------|----|----|
| [`STORY-IDS-PV-03...md:6`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md) | `Status: ⚪ Todo` | `Status: 🟢 Done` |
| там же, Acceptance Criteria (6 пунктов) | `- [ ]` | `- [x]` |
| [`EPIC-IDS-PHONE.md`](../tasks/backlog-stories/phone-verification/EPIC-IDS-PHONE.md) строка PV-03 | `… | ядро | ⚪ Todo |` | `… | ядро | 🟢 Done |` |

Pipeline-story ([epics/…/STORY-IDS-PV-03…md:7](../tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-03-otp-engine-session/STORY-IDS-PV-03-otp-engine-session.md)) и task-queue в индексе (t01–t06 🟢) уже были корректны — не трогались.

---

## F2 — счётчик тестов в индексе (doc-stale)

| Файл | До | После |
|------|----|----|
| [`bullrun-launch-index.md:11`](../tasks/bullrun-launch-index.md) | `281`(*) расчётно; в файле было `280 pytest offline` | `281 pytest offline` |

Число выставлено по фактическому прогону **после** фикса F3 (усиление существующего теста не добавило тест-функцию, поэтому счёт остался 281, а не вырос до 282).

---

## Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита до фикса | 281 passed, 9 skipped |
| Offline-сюита после фикса | **281 passed, 9 skipped** ✅ |
| Новый метод `mark_expired` | аддитивный; `mark_failed`/`mark_consumed`/`expire_pending` не изменены |
| Поведение verify | код ошибки `CODE_EXPIRED` неизменён; сменился только персистируемый `status` (`failed`→`expired`) на expiry-пути |
| eID-стор (`SupabaseVerificationSessionStore`/`VerificationSessionStore`) | не затронут — phone-контракт отдельный |
| Прочие phone-пути (mismatch/limit/invalidate/success) | без изменений — тесты зелёные |

Регрессий не выявлено.

---

## Quality gate (analysis.mdc)
- [x] Все изменения с `file:line` и примерами до/после.
- [x] Change propagation: единственная phone-реализация обновлена; подтверждено отсутствие Supabase phone-стора (eID-стор не путать).
- [x] Поведенческая граница фикса F3 очерчена: меняется только `status` на expiry-пути, код ошибки `CODE_EXPIRED` сохранён; покрыто ассертом.
- [x] F1/F2 — SSOT приведён к факту (backlog-story + EPIC.md + индекс); pipeline-story/task-queue уже были верны.
- [x] Регрессий нет (281→281); реализация прочих стори не затронута.
