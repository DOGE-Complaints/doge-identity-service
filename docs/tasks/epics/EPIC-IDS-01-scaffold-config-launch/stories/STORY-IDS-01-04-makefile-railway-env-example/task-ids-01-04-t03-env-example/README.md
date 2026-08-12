## Task workspace — `task-ids-01-04-t03-env-example`

- Story: [`../STORY-IDS-01-04-makefile-railway-env-example.md`](../STORY-IDS-01-04-makefile-railway-env-example.md)
- Decision Ref: [`../../../../../../requirements/07-env-configuration-spec.md`](../../../../../../requirements/07-env-configuration-spec.md) §«example.env» + req-17/18; оператор: файл **`.env.example`**

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000001`  
---

## Task: implement — .env.example template

### Цель
Корневой `.env.example`: deployment, supabase, authentigate, identity secrets, oauth, CORS, `EID_PROVIDER=mock`, `OIDC_REQUEST_TIMEOUT_S`, `EIDEASY_*` placeholders (req-18).

### Факты из кода
1. [`requirements/07-env-configuration-spec.md`](../../../../../../requirements/07-env-configuration-spec.md) L72–138 — содержимое шаблона (имя файла в spec: `example.env`; **эпик/оператор: `.env.example`**).
2. Эпик §Story 4: расширение vs req-06 base set (`SUPABASE_JWT_SECRET`, `EID_PROVIDER`).
3. [`requirements/17-eid-provider-abstraction.md`](../../../../../../requirements/17-eid-provider-abstraction.md) — `EID_PROVIDER`, `NODE_ID`.
4. [`requirements/18-eideasy-provider.md`](../../../../../../requirements/18-eideasy-provider.md) — `EIDEASY_*` block.

### Gap / Проблема
Новый разработчик не знает полный env surface identity-сервиса.

### AC/DoD
- [x] (P0) `doge-identity-service/.env.example` существует; не содержит реальных секретов.
- [x] (P0) Секции: Deployment, Supabase, Authentigate, Identity secrets, OAuth, CORS, EID provider (`EID_PROVIDER=mock` default).
- [x] (P0) `DOGESTONIA_EID_SECRET` documented (не `EID_HASH_SECRET`).
- [x] (P1) Комментарии генерации секретов из req-07 §«Генерация секретов».

### Где менять код
- `doge-identity-service/.env.example`

### Out of scope
- Коммит реального `.env`
- `COMPLAINTS_GATEWAY_URL` (эпик §9 open)

### Команды проверки
```bash
cd doge-identity-service && test -f .env.example && grep -E '^(APP_PROFILE|DOGESTONIA_EID_SECRET|EID_PROVIDER|OIDC_REQUEST_TIMEOUT_S)=' .env.example
```
