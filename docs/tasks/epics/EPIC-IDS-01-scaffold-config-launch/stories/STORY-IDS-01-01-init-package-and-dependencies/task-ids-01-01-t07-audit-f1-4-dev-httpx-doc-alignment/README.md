## Task workspace — `task-ids-01-01-t07-audit-f1-4-dev-httpx-doc-alignment`

- Story: [`../STORY-IDS-01-01-init-package-and-dependencies.md`](../STORY-IDS-01-01-init-package-and-dependencies.md)
- Audit source: [`../../../../audit-report-2026-05-28.md`](../../../../audit-report-2026-05-28.md) (F1-4)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** ready  
**Wave:** `override epic_ids_01_audit_2026_05_28`  
---

## Task: fix — выровнять Story 1 docs с dev-зависимостью `httpx`

### Цель
Добавить `httpx>=0.27.0` в текст Story 1 Outputs (dev-deps), чтобы документация совпадала с `pyproject.toml`.

### Факты из кода
1. Аудит F1-4: `pyproject.toml` содержит `httpx` в `project.optional-dependencies.dev`.
2. Story 1 Output в эпике не перечисляет `httpx` среди dev deps.

### AC/DoD
- [ ] (P0) В Story 1 Output отражён `httpx>=0.27.0` как dev dependency.

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-01-scaffold-config-launch/EPIC-IDS-01-scaffold-config-launch.md`
