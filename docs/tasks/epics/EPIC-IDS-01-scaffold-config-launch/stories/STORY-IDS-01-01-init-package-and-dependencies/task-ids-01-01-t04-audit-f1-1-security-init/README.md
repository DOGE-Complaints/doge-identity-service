## Task workspace — `task-ids-01-01-t04-audit-f1-1-security-init`

- Story: [`../STORY-IDS-01-01-init-package-and-dependencies.md`](../STORY-IDS-01-01-init-package-and-dependencies.md)
- Audit source: [`../../../../audit-report-2026-05-28.md`](../../../../audit-report-2026-05-28.md) (F1-1)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** ready  
**Wave:** `override epic_ids_01_audit_2026_05_28`  
---

## Task: fix — добавить `src/core/security/__init__.py`

### Цель
Закрыть gap F1-1: выровнять пакетную структуру `core.security` с остальными подпакетами и убрать риск нестабильного импорта.

### Факты из кода
1. [`audit-report-2026-05-28.md`](../../../../audit-report-2026-05-28.md) фиксирует отсутствие `src/core/security/__init__.py` (F1-1).
2. Story 1 требует единообразный скелет `src/core/*` (см. [`EPIC-IDS-01-scaffold-config-launch.md`](../../../../EPIC-IDS-01-scaffold-config-launch.md)).

### Gap / Проблема
`core.security` без `__init__.py` нарушает консистентность package scaffold.

### AC/DoD
- [ ] (P0) Создан `src/core/security/__init__.py`.
- [ ] (P0) Импорт `from core.security.hashing import hash_secret` завершается без ошибок.

### Где менять код
- `doge-identity-service/src/core/security/__init__.py`

### Команды проверки
```bash
cd doge-identity-service && . .venv/bin/activate
python3.11 -c "from core.security.hashing import hash_secret; print(hash_secret('x', key='k'))"
```
