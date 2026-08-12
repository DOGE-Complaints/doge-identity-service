## Task workspace — `task-ids-01-02-t07-audit-f2-4-eideasy-methods-default-order-alignment`

- Story: [`../STORY-IDS-01-02-appconfig.md`](../STORY-IDS-01-02-appconfig.md)
- Audit source: [`../../../../audit-report-2026-05-28.md`](../../../../audit-report-2026-05-28.md) (F2-4)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** ready  
**Wave:** `override epic_ids_01_audit_2026_05_28`  
---

## Task: fix — унифицировать порядок `EIDEASY_ALLOWED_METHODS`

### Цель
Привести default-порядок `EIDEASY_ALLOWED_METHODS` к одному виду в `schema.py` и `.env.example`.

### Факты из кода
1. Аудит F2-4 фиксирует расхождение порядка между кодом и env-шаблоном.
2. Story 2/4 артефакты должны быть консистентны для операторского DX.

### AC/DoD
- [ ] (P0) Порядок `EIDEASY_ALLOWED_METHODS` одинаков в `schema.py` и `.env.example`.
- [ ] (P1) Story docs обновлены при необходимости (если фикс меняет текст артефактов).

### Где менять код
- `doge-identity-service/src/core/config/schema.py`
- `doge-identity-service/.env.example`
