## Task workspace — `task-ids-07-01-t12-audit-f6-gitignore-env`

- Story: [`../STORY-IDS-AUTHCORE-01-profile-and-me.md`](../STORY-IDS-AUTHCORE-01-profile-and-me.md)
- Audit source: [`../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md) (F6)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000010`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md) §F6  
---

## Task: implement — `.gitignore` for service root (F6)

### Цель
Добавить `doge-identity-service/.gitignore`, исключающий `.env` и типичные локальные секреты/артефакты, чтобы случайный `git add` не закоммитил `SUPABASE_SERVICE_ROLE` из cwd `.env`.

### Почему это важно
Audit: `git check-ignore .env` → не игнорируется; в `.env` рабочий service_role (untracked). Severity MEDIUM — латентная утечка секрета + усиливает F1 (dev `.env` в cwd).

### Факты из кода
1. Корень сервиса: **нет** `.gitignore` (audit §F6).
2. Cwd `.env` с `SUPABASE_SERVICE_ROLE` — подмешивается в [`providers.py:14`](../../../../../../../src/core/config/providers.py).
3. [`epic-ids-07-authcore-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md) §F6 — рекомендация hygiene.

### Gap / Проблема
Отсутствие git-игнора для `.env` при локальной разработке с реальными creds.

### AC/DoD
- [x] (P0) Файл `doge-identity-service/.gitignore` существует.
- [x] (P0) `.env` и `.env.*` (кроме `.env.example` если есть) в ignore.
- [x] (P0) `git check-ignore -v doge-identity-service/.env` возвращает match (при наличии файла).
- [x] (P1) Минимальный набор: `.venv/`, `__pycache__/`, `.pytest_cache/` — по конвенции Python-проекта (не раздувать).
- [x] (P1) **Не** коммитить содержимое реального `.env`.

### Где менять код
- `doge-identity-service/.gitignore` (new)

### Out of scope
- Удаление существующего `.env` с диска оператора.
- Rotation скомпрометированных ключей.
- Изменение `merge_dotenv_from_cwd` (t07).

### Проверка
```bash
test -f doge-identity-service/.gitignore
git check-ignore -v doge-identity-service/.env || echo "no .env on disk — ok if missing"
```
