# BULLRUN-PHASE-LOG

- **Wave:** pkg-000010
- **Process:** P3 Execute gap F4
- **Date:** 2026-06-05

| Phase | Status | Evidence |
|-------|--------|----------|
| Docs | Done | `01-api.md` — базовые права = JWT `role`, без RBAC |

**Контракт:** на этапе AUTHCORE-01 поле `role` в `data` покрывает scope «базовые права»; permission-матрица — вне scope.

```bash
grep -n "role\|права" doge-identity-service/docs/runtime-docs/01-api.md
```
