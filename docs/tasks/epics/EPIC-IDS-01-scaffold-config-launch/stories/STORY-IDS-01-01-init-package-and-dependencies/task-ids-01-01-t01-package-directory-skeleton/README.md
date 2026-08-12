## Task workspace — `task-ids-01-01-t01-package-directory-skeleton`

- Story: [`../STORY-IDS-01-01-init-package-and-dependencies.md`](../STORY-IDS-01-01-init-package-and-dependencies.md)
- Epic: [`../../../../EPIC-IDS-01-scaffold-config-launch.md`](../../../../EPIC-IDS-01-scaffold-config-launch.md) §Story 1
- Decision Ref: [`../../../../../../requirements/06-technical-scaffold.md`](../../../../../../requirements/06-technical-scaffold.md) §Шаг 1; [`../../../../../../tech-requirements/impl-epic-01-scaffold-config-launch.md`](../../../../../../tech-requirements/impl-epic-01-scaffold-config-launch.md) Task 1.1

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000001`  
---

## Task: implement — package directory skeleton

### Цель
Создать модульное дерево `src/core/*` (пустые `__init__.py`), тестовые и supabase каталоги, placeholder `core/security/hashing.py` — без бизнес-логики.

### Факты из кода
1. [`doge-identity-service/`](../../../../../../../) — каталог `src/` отсутствует (onboarding Phase 0).
2. Эпик §5: [`EPIC-IDS-01-scaffold-config-launch.md`](../../../../EPIC-IDS-01-scaffold-config-launch.md) — перечень `src/core/{api,auth,profiles,oauth,stories,audit,infrastructure,config,security}/`.
3. Gateway reference layout: [`doge-complaints-gateway/src/core/`](../../../../../../../doge-complaints-gateway/src/core/) — паттерн пакетов (не копировать `cluster_*` модули).

### Gap / Проблема
Без скелета директорий последующие задачи не могут добавить `schema.py` / тесты; `import core` падает.

### AC/DoD
- [x] (P0) Директории: `src/core/{api,auth,profiles,oauth,stories,audit,infrastructure,config,security}/` + `tests/`, `tests/integration/supabase/`, `tests/smoke/`, `supabase/migrations/`, `supabase/bootstrap/`.
- [x] (P0) Все перечисленные пакеты содержат пустой `__init__.py`.
- [x] (P0) `src/core/security/hashing.py` — stub с сигнатурой `hash_secret(plaintext: str, *, key: str) -> str`.
- [x] (P1) `tests/__init__.py` присутствует.

### Где менять код
- `doge-identity-service/src/core/**/__init__.py`
- `doge-identity-service/src/core/security/hashing.py`
- `doge-identity-service/tests/**`, `supabase/**`

### Out of scope
- `pyproject.toml` (T02)
- `AppConfig`, FastAPI (STORY-IDS-01-02+)

### Команды проверки
```bash
cd doge-identity-service && find src/core -name '__init__.py' | wc -l
# ожидание: >= 9 пакетов + security module file
```
