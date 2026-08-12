## Task workspace — `task-ids-09-03-t07-audit-f1-backlog-story-status-sync`

- Story: [`../STORY-IDS-EID-03-provider-plugin-backbone.md`](../STORY-IDS-EID-03-provider-plugin-backbone.md)
- Audit source: [`../../../../../../analysis/epic-ids-09-eid-03-audit-2026-06-08.md`](../../../../../../analysis/epic-ids-09-eid-03-audit-2026-06-08.md) (F1)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** todo  
**Wave:** `override epic_ids_09_eid_03_audit_2026_06_08`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-09-eid-03-audit-2026-06-08.md`](../../../../../../analysis/epic-ids-09-eid-03-audit-2026-06-08.md) §F1  
---

## Task: fix — backlog story status and code refs sync (F1)

### Цель
Привести backlog SSOT [`STORY-IDS-EID-03-provider-plugin-backbone.md`](../../../../../../backlog-stories/STORY-IDS-EID-03-provider-plugin-backbone.md) в соответствие с фактом: story 🟢 Done под **EPIC-IDS-09**, plugin-платформа реализована (не hardcode mock / KeyError).

### Почему это важно
Backlog INDEX и операторы читают backlog как SSOT; устаревший `⚪ Todo`, «жёстко вшит mock» и «KeyError» вводят в заблуждение при следующем intake (EID-04+).

### Факты из кода
1. [`backlog-stories/STORY-IDS-EID-03-provider-plugin-backbone.md:6`](../../../../../../backlog-stories/STORY-IDS-EID-03-provider-plugin-backbone.md) — `Status: ⚪ Todo`.
2. [`backlog-stories/...:26-27`](../../../../../../backlog-stories/STORY-IDS-EID-03-provider-plugin-backbone.md) — «Точки в коде» — hardcode `providers.py:92`, `KeyError` в `registry.py:11-14`.
3. Pipeline story: [`../STORY-IDS-EID-03-provider-plugin-backbone.md`](../STORY-IDS-EID-03-provider-plugin-backbone.md) — 🟢 Done, AC [x].
4. Runtime wiring: [`providers.py:92-96`](../../../../../../../src/core/infrastructure/providers.py) — `build_provider_runtime` → `build_registry`.
5. Guard: [`registry.py:16-23`](../../../../../../../src/core/providers/registry.py) — `ProviderNotRegisteredError(ConfigError)`.
6. Plugin modules: [`descriptor.py`](../../../../../../../src/core/providers/descriptor.py), [`registry_builder.py`](../../../../../../../src/core/providers/registry_builder.py), [`mock/descriptor.py`](../../../../../../../src/core/providers/mock/descriptor.py).

### Gap / Проблема
Doc-stale в backlog; расхождение backlog ↔ pipeline ↔ код (audit F1 MEDIUM).

### AC/DoD
- [ ] (P0) Backlog Meta: `Status: 🟢 Done`.
- [ ] (P0) Секция «Точки в коде» отражает `EIDProviderDescriptor` / `ProviderRuntime` / `build_registry` / `ProviderNotRegisteredError` (не hardcode/KeyError).
- [ ] (P0) AC checkboxes в backlog [x] — **verbatim** формулировки AC не менять.
- [ ] (P1) Ссылка на pipeline story / pkg-000016 как источник исполнения.

### Где менять код
- `doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-EID-03-provider-plugin-backbone.md` only

### Out of scope
- Изменение AC текста story (verbatim).
- Код, pytest, runtime-docs.
- F2 из audit (deferred observation).
- Pipeline story «Точки в коде» (audit F1 scope = backlog only).

### Проверка
```bash
grep -n "Status\|KeyError\|providers.py:92\|ProviderNotRegisteredError\|build_registry\|EIDProviderDescriptor" \
  doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-EID-03-provider-plugin-backbone.md
```
