## Task workspace — `task-ids-08-02-t06-empty-layer-packages-e22`

- Story: [`../STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../STORY-IDS-CLEANUP-02-placeholders-hardening.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-02-placeholders-hardening.md) Scope E22; [`../task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/owner-decisions-e17-e22.md`](../task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/owner-decisions-e17-e22.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000013`  
**Skill declared:** python-pro  
---

## Task: refactor — empty layer packages (E22)

### Цель
Выполнить owner decision по E22 для пакетов `core.audit`, `core.oauth`, `core.profiles`: наполнить по мере эпиков (placeholder) или убрать.

### Почему это важно
Docstring-only packages вводят в заблуждение о наличии слоя ([`03-soa-roles`](../../../../../../../runtime-docs/03-soa-roles.md):64). Story AC #1; «Вне scope» запрещает функциональное наполнение — только remove или explicit keep.

### Факты из кода
1. [`src/core/audit/__init__.py`](../../../../../../../src/core/audit/__init__.py) — `"""Audit layer package."""`
2. [`src/core/oauth/__init__.py`](../../../../../../../src/core/oauth/__init__.py) — `"""OAuth layer package."""`
3. [`src/core/profiles/__init__.py`](../../../../../../../src/core/profiles/__init__.py) — `"""Profiles layer package."""`
4. Import sites `core.audit|core.oauth|core.profiles` в `src/` — отсутствуют (grep 2026-06-02).

### Gap / Проблема
Три пустых пакета-заготовки без поведения.

### AC/DoD
- [ ] (P0) Story AC #1: решение E22 из t01 выполнено для всех трёх пакетов.
- [ ] (P0) Если «убрать»: Story AC #3 — каталоги удалены; `rg "core\.audit|core\.oauth|core\.profiles"` в `src/` = 0.
- [ ] (P0) Если «оставить placeholder»: явная запись в owner-decisions; без добавления функционального кода (backlog «Вне scope»).
- [ ] (P1) Offline pytest green.

### Где менять код
- [`src/core/audit/`](../../../../../../../src/core/audit/) — remove или keep
- [`src/core/oauth/`](../../../../../../../src/core/oauth/) — remove или keep
- [`src/core/profiles/`](../../../../../../../src/core/profiles/) — remove или keep
- [`docs/runtime-docs/03-soa-roles.md`](../../../../../../../docs/runtime-docs/03-soa-roles.md) — только если t01 = убрать (минимальная правка mention)

### Out of scope
- Функциональные реализации audit/oauth/profiles — backlog «Вне scope»
- CLEANUP-03 full runtime-docs sync

### Проверка
```bash
cd doge-identity-service
rg "core\.audit|core\.oauth|core\.profiles" src/
test ! -d src/core/audit/__init__.py 2>/dev/null || test -f src/core/audit/__init__.py
.venv/bin/python -m pytest -m "not live_integration" -q
```
