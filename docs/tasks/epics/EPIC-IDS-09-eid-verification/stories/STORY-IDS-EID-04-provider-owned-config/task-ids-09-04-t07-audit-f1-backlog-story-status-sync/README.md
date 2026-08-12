## Task workspace — `task-ids-09-04-t07-audit-f1-backlog-story-status-sync`

- Story: [`../STORY-IDS-EID-04-provider-owned-config.md`](../STORY-IDS-EID-04-provider-owned-config.md)
- Audit source: [`../../../../../../analysis/epic-ids-09-eid-04-audit-2026-06-08.md`](../../../../../../analysis/epic-ids-09-eid-04-audit-2026-06-08.md) (F1)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_09_eid_04_audit_2026_06_08`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-09-eid-04-audit-2026-06-08.md`](../../../../../../analysis/epic-ids-09-eid-04-audit-2026-06-08.md) §F1  
---

## Task: fix — backlog story status and code refs sync (F1)

### Цель
Привести backlog SSOT [`STORY-IDS-EID-04-provider-owned-config.md`](../../../../../../backlog-stories/STORY-IDS-EID-04-provider-owned-config.md) в соответствие с фактом: story 🟢 Done под **EPIC-IDS-09**, provider-owned config реализован (не eideasy-`if` в schema).

### Почему это важно
Backlog INDEX и операторы читают backlog как SSOT; устаревший `⚪ Todo`, устаревшие «Точки в коде» и AC `[ ]` вводят в заблуждение при следующем intake (EID-05+).

### Факты из кода
1. [`backlog-stories/STORY-IDS-EID-04-provider-owned-config.md:6`](../../../../../../backlog-stories/STORY-IDS-EID-04-provider-owned-config.md) — `Status: ⚪ Todo`.
2. [`backlog-stories/...:27-31`](../../../../../../backlog-stories/STORY-IDS-EID-04-provider-owned-config.md) — «Точки в коде» — устаревший `schema.py:96-112` (eideasy `if` + membership).
3. Pipeline story: [`../STORY-IDS-EID-04-provider-owned-config.md`](../STORY-IDS-EID-04-provider-owned-config.md) — 🟢 Done, AC [x].
4. Delegated validation: [`schema.py:88-93,118`](../../../../../../../src/core/config/schema.py) — `_validate_active_eid_provider_config` → `config_spec.validate`.
5. `ProviderConfigSpec`: [`config_spec.py:16-29`](../../../../../../../src/core/providers/config_spec.py).
6. Authentigate/eideasy config: [`authentigate/config.py`](../../../../../../../src/core/providers/authentigate/config.py), [`eideasy/config.py`](../../../../../../../src/core/providers/eideasy/config.py).

### Gap / Проблема
Doc-stale в backlog; расхождение backlog ↔ pipeline ↔ код (audit F1 MEDIUM).

### AC/DoD
- [x] (P0) Backlog Meta: `Status: 🟢 Done`.
- [x] (P0) Секция «Точки в коде» отражает `ProviderConfigSpec` / делегированную валидацию / `AuthentigateSettings` (не eideasy-`if` в schema).
- [x] (P0) AC checkboxes в backlog [x] — **verbatim** формулировки AC не менять.
- [x] (P1) Ссылка на pipeline story / pkg-000017 как источник исполнения.

### Где менять код
- `doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-EID-04-provider-owned-config.md` only

### Out of scope
- Изменение AC текста story (verbatim).
- Код, pytest, runtime-docs.
- F2 из audit (отдельный task t08).
- Pipeline story «Точки в коде» (audit F1 scope = backlog only).

### Проверка
```bash
grep -n "Status\|eideasy\|ProviderConfigSpec\|_validate_active_eid_provider_config\|AuthentigateSettings" \
  doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-EID-04-provider-owned-config.md
```
