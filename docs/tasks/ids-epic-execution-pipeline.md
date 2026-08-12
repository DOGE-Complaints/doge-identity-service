# Identity — Epic-first execution pipeline

> **Профиль Builder Queue:** `identity`  
> **Операторский маршрут:** [`docs/methodology/Zeya888-builder-queue/core/workflow.md`](../../../docs/methodology/Zeya888-builder-queue/core/workflow.md) §«Маршрут Epic-first»

## SSOT

| Слой | Источник |
|------|----------|
| Эпик (scope, Stories, AC) | `docs/tasks/epics/EPIC-IDS-*.md` |
| Requirements (детали) | `docs/requirements/` — только то, на что эпик ссылается |
| Очередь исполнения | immutable `identity-active-packages/pkg-*.yaml` |
| Статусы волн | `docs/tasks/bullrun-launch-index.md` (после P1; **после каждого task** — sync в той же итерации) |
| Backlog package rows | `docs/tasks/backlog-stories/*/INDEX.md` |
| Backlog snapshot | `docs/tasks/identity-backlog-dashboard.md` (derived) |
| Операторский контракт | [`docs/methodology/Zeya888-builder-queue/contracts/identity-operator-contract.md`](../../../docs/methodology/Zeya888-builder-queue/contracts/identity-operator-contract.md) |

## После закрытия story (sync checklist)

1. `bullrun-launch-index.md` §«Актуальная точка» + §«Epic registry».
2. Package `docs/tasks/backlog-stories/<pkg>/INDEX.md` (Status + Progress).
3. Root `docs/tasks/backlog-stories/INDEX.md` (open stories / package table).
4. `docs/tasks/identity-backlog-dashboard.md` — пересчёт (см. [backlog-dashboard-maintenance.md](../../../docs/methodology/Zeya888-builder-queue/workflow/backlog-dashboard-maintenance.md)).

## Перед batch-run (обязательно)

1. `bullrun-launch-index.md` §«Актуальная точка» + §«Epic registry».
2. `identity-active-package.current.yaml` → active pkg.
3. `builder_resolve_queue.py --project identity --verify` — FAIL = стоп.
4. Эпик-файл без task queue в индексе → **не декомпозирован** → P1 + `bullrun-epic-decompose`, не Execute.
5. Оператор указал `input_mode: epic_story | requirement` (или `run_mode=…` для audit override).

## Gate: Story parent AC

После **последнего** task README в story — проверить Acceptance Criteria соответствующей Story в файле эпика (`### Story N`).

## Gate: Epic AC

После всех stories эпика — §2 Epic Goal и §8 Верификация эпика в `$epicFile`.

## Build window

Генерация из корня workspace:

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --list
```

См. workflow §P2 (epic): `--story-key` или `--window-flat-start` / `--window-flat-end`.
