# Process Audit — EPIC-IDS-05 re-audit scaffold (2026-06-02)

## Контекст запроса

Оператор сообщил, что внешний аудит посчитал работу слабой, и запросил:

1. подтвердить/опровергнуть это с доказательствами;
2. если это косяк исполнителя — провести жёсткий аудит процесса;
3. оформить выводы в analysis-зоне.

Метод проверки: `analysis.mdc` (только проверяемые факты из файлов, без предположений).

---

## Источники фактов

- Re-audit результата по коду:  
  `doge-identity-service/docs/tasks/epics/EPIC-IDS-05-supabase-persistence/re-audit-report-2026-06-02.md`
- Индекс очередей/статусов:  
  `doge-identity-service/docs/tasks/bullrun-launch-index.md`
- План билдер-процесса identity (safe-override):  
  `.cursor/plans/ID_builder.plan.md`
- Обновлённые task README (пример):  
  `doge-identity-service/docs/tasks/epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-02-supabase-repositories-identity-set/task-ids-05-02-t04-audit-s2-1-oauth-store-env-doc/README.md`
- Активный pkg указатель:  
  `doge-identity-service/docs/tasks/identity-active-package.current.yaml`

---

## Фактическое состояние (что правда)

### 1) P5 был выполнен как scaffold, а не как закрытие runtime-gap

Это **факт**, а не баг сам по себе:

- Re-audit явно показывает 5 открытых runtime gap и 1 закрытый (`RG-1`):  
  `re-audit-report-2026-06-02.md` (таблица: `S2-1`, `S3-1`, `S1-1`, `S2-2`, `S3-2` = `ОТКРЫТ`).
- В `bullrun-launch-index.md` эти 5 gap стоят как `⚪ Todo` в re-audit wave (`run_mode=epic_ids_05_reaudit_2026_06_02`), что консистентно с P5 scaffold-only.

Вывод: внешняя оценка «слабая работа» частично может быть из неверного ожидания (ждали runtime fix, а выполнен только scaffold).

### 2) Документационный scaffold действительно сделан

Пример task README содержит секции `task-standard`:

- `Цель`, `Факты из кода`, `Gap`, `AC/DoD`, `Где менять`, `План выполнения`, `Проверка`  
  (`.../task-ids-05-02-t04-audit-s2-1-oauth-store-env-doc/README.md`).

---

## Подтверждённый косяк процесса (мой)

### Косяк: в `ID_builder.plan.md` потеряны ранее существовавшие override-режимы

Проверка по файлу:

- В `ID_builder.plan.md` сейчас есть `run_mode=epic_ids_05_reaudit_2026_06_02` и правило для `epic_ids_01_audit_2026_05_28`.
- Поиск по файлу не находит старые режимы:
  - `run_mode=epic_ids_02_audit_2026_05_28`
  - `run_mode=epic_ids_03_audit_2026_05_28`
  - `run_mode=epic_ids_04_audit_2026_05_30`
  - `run_mode=epic_ids_05_audit_2026_05_31`

При этом `bullrun-launch-index.md` продолжает ссылаться на эти волны как активные/частично закрытые (например, EPIC-IDS-04 partial и EPIC-IDS-05 audit wave).

Это создаёт рассинхрон SSOT:

- index говорит, что эти override-волны существуют;
- `ID_builder.plan.md` больше не содержит соответствующих подразделов.

По `analysis.mdc` это `architectural drift` и `single source of truth` violation.

---

## Root Cause Analysis

1. Выполнялись последовательные правки в одном и том же блоке safe-override внутри `ID_builder.plan.md`.
2. Не была сделана обязательная post-change сверка на сохранение всех существующих `run_mode` разделов.
3. Из-за этого произошло непреднамеренное «сужение» плана до части override-режимов.

Ключевая процессная ошибка: отсутствие change-propagation/consistency-check после правок критичного SSOT-файла.

---

## Влияние

### Что не сломано

- Runtime-код `src/` не менялся.
- Активный pkg указатель корректен:  
  `identity-active-package.current.yaml` → `pkg-000006`.
- Re-audit gap status в index соответствует реальному коду.

### Что сломано

- `ID_builder.plan.md` стал неполным относительно index по override-режимам IDS-02/03/04/05(audit).
- Это может приводить к неправильному поведению в сессиях, где оператор укажет один из пропавших `run_mode`.

---

## Вердикт по запросу

1. Утверждение внешнего аудита о «слабой работе» **частично подтверждается**:
   - если ожидалось runtime-исправление — это не было целью P5;
   - но есть реальный процессный косяк: повреждение полноты `ID_builder.plan.md`.
2. Косяк исполнителя **есть**, он подтверждён файловыми доказательствами.

---

## Корректирующие действия (обязательные)

1. Восстановить в `ID_builder.plan.md` все ранее поддерживаемые override-подразделы, на которые ссылается index:
   - `epic_ids_02_audit_2026_05_28`
   - `epic_ids_03_audit_2026_05_28`
   - `epic_ids_04_audit_2026_05_30`
   - `epic_ids_05_audit_2026_05_31`
   - сохранить `epic_ids_05_reaudit_2026_06_02`.
2. Синхронизировать «Жёсткое правило исполнения override» с полным списком.
3. Запустить consistency-check:
   - каждый `run_mode`, упомянутый в `bullrun-launch-index.md`, должен иметь одноимённый safe-override подраздел в `ID_builder.plan.md` (или явную пометку, что режим удалён).
4. Добавить в процесс мини-gate после правок `ID_builder.plan.md`: проверка наличия всех legacy `run_mode` перед завершением.

---

## Короткий итог

- P5 scaffold по EPIC-IDS-05 сделан.
- Внешний упрёк по «слабой работе» обоснован в части процессной дисциплины: подтверждён косяк с неполной сохранностью `ID_builder.plan.md`.
- Требуется отдельный corrective pass для восстановления полной override-матрицы.
