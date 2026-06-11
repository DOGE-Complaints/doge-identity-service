# Жёсткий аудит исполнения STORY-IDS-PV-04 (флаг профиля + миграция + дедуп)

> **Дата:** 2026-06-11
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-PV-04-profile-flag-migration`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md) vs фактический код. Исполнена под **EPIC-IDS-10-phone-verification** (alias `EPIC-IDS-PHONE`), pkg-000025, 6 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): Текущая волна pkg-000025, STORY-IDS-PV-04 🟢 (стр.11,41,509-514).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Миграция | `supabase/migrations/20260611000001_profiles_phone_verification.sql` — 5 колонок + unique-index + CHECK ([migration](../../supabase/migrations/20260611000001_profiles_phone_verification.sql)) |
| `ProfileRecord` phone-поля | `phone_verified`/`verified_phone_hash`/`phone_provider`/`phone_dial_prefix`/`phone_verified_at` ([models.py:34-38](../../src/core/domain/models.py)) |
| Контракт | `ProfileRepository.attach_phone_verification(...)` + `get_by_verified_phone_hash` ([contracts.py:29,44-53](../../src/core/domain/contracts.py)) |
| In-memory репо | `attach_phone_verification` + дедуп через `_by_verified_phone_hash` ([repositories.py:72-76,164-...](../../src/core/infrastructure/repositories.py)) |
| Supabase репо | `attach_phone_verification` (409→`ProfileConflictError`) + `get_by_verified_phone_hash` + row-mapping ([db_supabase.py:385-389,485-565](../../src/core/infrastructure/db_supabase.py)) |
| `/me` | `phone_verified`/`phone_provider`/`phone_dial_prefix`/`phone_verified_at` ([me_response.py:42-45](../../src/core/api/me_response.py)) |
| Тесты | inmemory dedup (3) + supabase (2) + me (1) + migration-sql (1) |
| **Offline-сюита** | **289 passed, 9 skipped** ✅ (было 281 → +8) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-10, pkg-000025) | Факт | Статус |
|--------------------------------|------|--------|
| t01 profiles phone migration sql | ALTER TABLE +5 колонок, `unique_verified_phone_hash` (partial WHERE NOT NULL), `phone_consistency` CHECK ([migration:4-26](../../supabase/migrations/20260611000001_profiles_phone_verification.sql)) | 🟢 |
| t02 profile record phone fields + contract | поля в `ProfileRecord` ([models.py:34-38](../../src/core/domain/models.py)); метод+`get_by_verified_phone_hash` в Protocol ([contracts.py:29,44-53](../../src/core/domain/contracts.py)) | 🟢 |
| t03 inmemory attach phone + dedup | `attach_phone_verification` ставит флаг/хэш/префикс/время; `one_account_per_number` → `ProfileConflictError` при чужом владельце ([repositories.py:164-...](../../src/core/infrastructure/repositories.py)); 3 теста | 🟢 |
| t04 supabase profile phone mapping + attach | row↔record маппинг (`_profile_to_row`/`_profile_from_row`), `attach_phone_verification` с 409→`ProfileConflictError` ([db_supabase.py:101-105,128-132,485-565](../../src/core/infrastructure/db_supabase.py)); 2 теста | 🟢 |
| t05 me response phone fields + tests | `/me` отдаёт 4 phone-поля (без `verified_phone_hash` — PII) ([me_response.py:42-45](../../src/core/api/me_response.py)); тест `test_me_with_phone_verified_profile_returns_phone_fields` | 🟢 |
| t06 story acceptance verification | AC 5/5 (см. §2); pipeline-story `Status: 🟢 Done` (стр.7), индекс t06 🟢 ([bullrun-launch-index.md:514](../tasks/bullrun-launch-index.md)) | 🟢 |
| **STORY-IDS-PV-04** | флаг профиля + миграция + дедуп | **🟢 Done** |

Индекс держит эпик корректно: `EPIC-IDS-10 … 🟡 In Progress — PV-01 🟢; PV-02 🟢; PV-03 🟢; PV-04 🟢` ([bullrun-launch-index.md:84](../tasks/bullrun-launch-index.md)).

---

## 2. Сверка Acceptance Criteria story (по коду + тестам)

| AC | Факт (код + тест) | Вердикт |
|----|-------------------|---------|
| Миграция добавляет phone-колонки + индекс на `verified_phone_hash` | 5 колонок + `CREATE UNIQUE INDEX … unique_verified_phone_hash … WHERE … NOT NULL` ([migration:4-13](../../supabase/migrations/20260611000001_profiles_phone_verification.sql)); тест `test_profiles_phone_verification_columns_and_index` | ✅ |
| `attach_phone_verification` ставит `phone_verified=true` + хэш/префикс/время | in-memory + supabase обе ставят 4 поля ([repositories.py](../../src/core/infrastructure/repositories.py), [db_supabase.py:503-507](../../src/core/infrastructure/db_supabase.py)); тест `test_attach_phone_verification_sets_profile_fields` | ✅ |
| При `PHONE_ONE_ACCOUNT_PER_NUMBER=true` повтор на другом аккаунте → `ProfileConflictError`/409 | `one_account_per_number` гейт ([repositories.py:174-179](../../src/core/infrastructure/repositories.py), [db_supabase.py:495-500](../../src/core/infrastructure/db_supabase.py)); тесты `..._enforces_unique_hash_when_one_account`, `..._allows_duplicate_when_not_one_account`, `..._maps_409_to_profile_conflict_error` | ✅ |
| `/me` отдаёт `phone_verified` и поля | me_response.py:42-45; тест `test_me_with_phone_verified_profile_returns_phone_fields` | ✅ |
| Offline-набор зелёный | **289 passed** | ✅ |

**Вывод:** все 5 AC выполнены и покрыты тестами (7 dedicated). Правило «один номер = один аккаунт» реализовано на двух уровнях (доменный гейт + DB unique-index + 409-маппинг), зеркало eID anti-Sybil.

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F1** | MEDIUM | Doc-stale | Backlog-story `Status: ⚪ Todo` (стр.6) + AC `[ ]` (стр.30-34) — реально 🟢 Done под pkg-000025. Та же рассинхронизация в [`EPIC-IDS-PHONE.md`](../tasks/backlog-stories/phone-verification/EPIC-IDS-PHONE.md) (строка PV-04 = ⚪ Todo). **Как закрыть:** Status ⚪→🟢, AC `[ ]`→`[x]`, строка таблицы EPIC.md PV-04 → 🟢. Рекуррентный паттерн (PV-01/02/03). | [`STORY-IDS-PV-04...md:6,30-34`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md) |
| **F2** | LOW | Doc-stale | Индекс декларирует «288 pytest offline» ([bullrun-launch-index.md:11](../tasks/bullrun-launch-index.md)), фактически **289 passed** (off-by-one, как PV-01/02/03/EID-08). **Как закрыть:** синхронизировать число. | [`bullrun-launch-index.md:11`](../tasks/bullrun-launch-index.md) |

Иных материальных findings нет. Наблюдения (severity none, по scope, **не gap**):
- **Сигнатура `attach_phone_verification` шире scope story:** добавлен kw-параметр `one_account_per_number: bool` ([contracts.py:52](../../src/core/domain/contracts.py)), которого нет в перечне scope (`provider, dial_prefix, verified_phone_hash, verified_at`). Это необходимо для P1-тоггла дедупа (AC3) и проведено консистентно через контракт + обе реализации — корректное расширение, не gap.
- **Бонус-инвариант в миграции:** `phone_consistency` CHECK (`phone_verified=TRUE ⇒ hash & verified_at NOT NULL`, [migration:18-26](../../supabase/migrations/20260611000001_profiles_phone_verification.sql)) — сверх AC (просили колонки+индекс), зеркалит eID-консистентность. Усиление, не gap.
- **`/me` не отдаёт `verified_phone_hash`** (только статус/провайдер/префикс/время) — корректная минимизация PII (хэш — внутренний антидубль-ключ). Supabase row-mapping держит `verified_phone_hash` в `ProfileRecord` для дедупа, но наружу он не уходит.
- **HTTP-409 для phone-флоу ещё не подключён** в роуты: `ProfileConflictError`→409-маппинг в [handlers.py:339](../../src/core/api/handlers.py) живёт в eID-callback; оркестрация вызова `attach_phone_verification` и его HTTP-обёртка — **вне scope PV-04** ([PV-05](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md)). Доменный `ProfileConflictError` поднимается уже сейчас (покрыт тестами), что AC3 и требует.

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **289 passed, 9 skipped** (было 281 → +8 phone-profile тестов), **ожидаемо** |
| `ProfileRecord` | +5 phone-полей (обязательные в dataclass); все конструкторы (in-memory/supabase/me-defaults) заполняют их — существующие profile/me-тесты зелёные |
| `attach_eid_verification`/`get_by_verified_person_hash` | не изменены; phone-дедуп использует отдельный индекс `_by_verified_phone_hash` (in-memory) / отдельную колонку (supabase) |
| Миграция | аддитивная (`ADD COLUMN IF NOT EXISTS`, `DROP CONSTRAINT IF EXISTS` перед `ADD`) — идемпотентна, не ломает существующие профили (default FALSE) |
| `/me` | +4 поля в ответе; eID-поля сохранены |
| eID/phone-OTP (PV-01/02/03) | не затронуты — сюита зелёная |

Регрессий не выявлено.

---

## 5. Итог

- **STORY-IDS-PV-04 — 🟢 исполнена полно:** миграция (5 колонок + partial unique-index + CHECK), phone-поля в `ProfileRecord`, `attach_phone_verification` (in-memory + supabase) с дедупом «один номер = один аккаунт» (`PHONE_ONE_ACCOUNT_PER_NUMBER`→`ProfileConflictError`/409), `/me` отдаёт статус без PII-хэша. AC 5/5, 7 тестов. Зеркало eID anti-Sybil.
- **Findings:** **F1 (MEDIUM, doc-stale)** — backlog-story + EPIC.md ⚪→🟢 (рекуррентно); **F2 (LOW)** — индекс 288 vs факт 289.
- Наблюдения (расширенная сигнатура `attach`; бонус CHECK; PII-минимизация `/me`; HTTP-409 → PV-05) — по scope, не gaps.

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; 6 тасков + story сверены по коду (pipeline-story 🟢, индекс t01–t06 🟢).
- [x] AC 5/5 сверены по коду **и** тестам; дедуп проверен на 3 ветках (enforce / allow-when-off / supabase-409).
- [x] Change propagation: phone-поля проведены через models→contracts→in-memory→supabase→me_response, все конструкторы `ProfileRecord` заполнены.
- [x] Регрессий нет; 281→289 (+8) объяснён; миграция идемпотентна (IF NOT EXISTS / DROP IF EXISTS).
- [x] Границы scope прослежены: HTTP-обёртка/оркестрация attach → PV-05 (не gap PV-04); PII-хэш не утекает в `/me`.
