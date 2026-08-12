## Task workspace — `task-ids-08-02-t09-audit-f2-empty-layer-directories-doc-align`

- Story: [`../STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../STORY-IDS-CLEANUP-02-placeholders-hardening.md)
- Audit source: [`../../../../../../analysis/epic-ids-08-cleanup-02-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-08-cleanup-02-audit-2026-06-05.md) (F2)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_08_cleanup_02_audit_2026_06_05`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-08-cleanup-02-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-08-cleanup-02-audit-2026-06-05.md) §F2 · t06 follow-up  
---

## Task: refactor — empty layer directories + doc align (F2)

### Цель
Устранить residual после t06: пустые каталоги `core.audit`/`core.oauth`/`core.profiles` и неточное утверждение «удалены» в runtime-doc.

### Почему это важно
Промежуточное состояние «ни пакет, ни удалено» + doc drift вводит в заблуждение (аналог F3 CLEANUP-01 для `core.stories/`).

### Факты из кода
1. `src/core/audit/`, `src/core/oauth/`, `src/core/profiles/` — **0 files** (пустые каталоги, verified 2026-06-05; `__init__.py` удалён в P3 t06).
2. Grep `core.audit|core.oauth|core.profiles` в `src/` = 0 import sites.
3. [`03-soa-roles.md:64`](../../../../../../../docs/runtime-docs/03-soa-roles.md) — «placeholder-пакеты … **удалены**» — неточно относительно фактических каталогов.
4. Audit t06: [`epic-ids-08-cleanup-02-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-08-cleanup-02-audit-2026-06-05.md) §1 t06 «🟢 c оговоркой».

### Gap / Проблема
Git не отслеживает пустые каталоги; doc утверждает полное удаление, каталоги остались локально.

### AC/DoD
- [ ] (P0) **Branch A:** удалить `src/core/audit/`, `src/core/oauth/`, `src/core/profiles/` (пустые каталоги); обновить [`03-soa-roles.md:64`](../../../../../../../docs/runtime-docs/03-soa-roles.md) — формулировка согласована с фактом.
- [ ] (P0) **Branch B:** восстановить docstring-only `__init__.py` в трёх каталогах; обновить 03-soa («placeholder, не удалены») — если оператор отклоняет rmdir.
- [ ] (P1) BULLRUN-PHASE-LOG + acceptance-verification в этой папке (P3).

### Где менять код
- [`src/core/audit/`](../../../../../../../src/core/audit/), [`oauth/`](../../../../../../../src/core/oauth/), [`profiles/`](../../../../../../../src/core/profiles/)
- [`docs/runtime-docs/03-soa-roles.md`](../../../../../../../docs/runtime-docs/03-soa-roles.md) — §пустые модули

### Out of scope
- Функциональное наполнение audit/oauth/profiles (backlog «Вне scope»)
- Reopen t06 README status (audit gap only)

### Проверка
```bash
# Branch A:
test ! -d doge-identity-service/src/core/audit
test ! -d doge-identity-service/src/core/oauth
test ! -d doge-identity-service/src/core/profiles
grep -n "audit\|oauth\|profiles" doge-identity-service/docs/runtime-docs/03-soa-roles.md
```
