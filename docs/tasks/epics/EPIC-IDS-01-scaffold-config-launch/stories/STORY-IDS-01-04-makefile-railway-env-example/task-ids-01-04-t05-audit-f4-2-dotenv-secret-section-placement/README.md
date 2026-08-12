## Task workspace — `task-ids-01-04-t05-audit-f4-2-dotenv-secret-section-placement`

- Story: [`../STORY-IDS-01-04-makefile-railway-env-example.md`](../STORY-IDS-01-04-makefile-railway-env-example.md)
- Audit source: [`../../../../audit-report-2026-05-28.md`](../../../../audit-report-2026-05-28.md) (F4-2)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** ready  
**Wave:** `override epic_ids_01_audit_2026_05_28`  
---

## Task: fix — перенести `DOGESTONIA_EID_SECRET` в секцию Identity Secrets

### Цель
Согласовать структуру `.env.example`: переменная `DOGESTONIA_EID_SECRET` должна находиться рядом с комментариями генерации секрета в секции Identity Secrets.

### Факты из кода
1. Аудит F4-2: `DOGESTONIA_EID_SECRET` сейчас в секции Identity Provider.
2. Комментарии генерации HMAC-секрета находятся в секции Identity Secrets.

### AC/DoD
- [ ] (P0) `DOGESTONIA_EID_SECRET` перемещён в секцию Identity Secrets.
- [ ] (P1) Секция Identity Provider содержит только provider-selection поля.

### Где менять код
- `doge-identity-service/.env.example`
