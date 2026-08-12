## Task workspace — `task-ids-01-04-t04-audit-f4-1-test-live-flags-cleanup`

- Story: [`../STORY-IDS-01-04-makefile-railway-env-example.md`](../STORY-IDS-01-04-makefile-railway-env-example.md)
- Audit source: [`../../../../audit-report-2026-05-28.md`](../../../../audit-report-2026-05-28.md) (F4-1)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** ready  
**Wave:** `override epic_ids_01_audit_2026_05_28`  
---

## Task: fix — убрать конфликт `-q` и `-v` в `test-live`

### Цель
Сделать `Makefile:test-live` однозначным (оставить `-v` без `-q`), как описано в Story 4.

### Факты из кода
1. Аудит F4-1: `test-live` использует `-q` и `-v` одновременно.
2. Story 4 expectation — `test-live` с verbose режимом.

### AC/DoD
- [ ] (P0) В `Makefile` цель `test-live` больше не содержит конфликтующих флагов.
- [ ] (P1) Story 4 docs/gate при необходимости синхронизированы с новой командой.

### Где менять код
- `doge-identity-service/Makefile`
- `.../STORY-IDS-01-04-makefile-railway-env-example.md`
