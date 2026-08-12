# Acceptance verification — task-ids-09-04-t07-audit-f1-backlog-story-status-sync

- **Wave:** `override epic_ids_09_eid_04_audit_2026_06_08`
- **Audit:** F1 ([`epic-ids-09-eid-04-audit-2026-06-08.md`](../../../../../../analysis/epic-ids-09-eid-04-audit-2026-06-08.md))

## Evidence

```bash
grep -n "Status\|ProviderConfigSpec\|_validate_active_eid_provider_config\|AuthentigateSettings\|pkg-000017" \
  doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-EID-04-provider-owned-config.md
```

- Meta: `Status: 🟢 Done`, `Epic: EPIC-IDS-09`
- «Точки в коде»: `ProviderConfigSpec`, делегированная валидация, `AuthentigateSettings` (не eideasy-`if` в schema)
- AC checkboxes [x] — verbatim формулировки сохранены
- Ссылка на pipeline story + pkg-000017 в Meta «Исполнение»

## AC/DoD

| Criterion | Result |
|-----------|--------|
| Backlog Meta Status 🟢 Done | PASS |
| «Точки в коде» — реализованные модули | PASS |
| AC [x] verbatim | PASS |
| Pipeline story / pkg-000017 link | PASS |
