## Task workspace — `task-ids-01-01-t08-audit-f1-5-pyright-config-alignment`

- Story: [`../STORY-IDS-01-01-init-package-and-dependencies.md`](../STORY-IDS-01-01-init-package-and-dependencies.md)
- Audit source: [`../../../../audit-report-2026-05-28.md`](../../../../audit-report-2026-05-28.md) (F1-5)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** ready  
**Wave:** `override epic_ids_01_audit_2026_05_28`  
---

## Task: fix — устранить конфликт pyright-конфигураций

### Цель
Согласовать `pyrightconfig.json` и `[tool.pyright]` (`pyproject.toml`) для `extraPaths`.

### Факты из кода
1. Аудит F1-5 фиксирует расхождение: `pyrightconfig.json` (`extraPaths=["src"]`) vs `pyproject.toml` (`["src","tests"]`).
2. Приоритет у `pyrightconfig.json`, из-за чего `tests` исключаются из effective config.

### AC/DoD
- [ ] (P0) Effective pyright config включает `tests` в `extraPaths`.
- [ ] (P0) Выбран один SSOT-подход: либо синхронизация обоих файлов, либо удаление дублирующего конфига.

### Где менять код
- `doge-identity-service/pyrightconfig.json`
- `doge-identity-service/pyproject.toml`
