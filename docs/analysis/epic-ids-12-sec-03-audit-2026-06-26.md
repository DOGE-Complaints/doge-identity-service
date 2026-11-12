# Жёсткий аудит исполнения STORY-IDS-SEC-03 (JWT validation hardening — `aud` + key-import)

> **Дата:** 2026-06-26
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity. Не предлагаю реализацию — только findings.
> **Предмет:** [`STORY-IDS-SEC-03-jwt-validation-hardening`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md) vs фактический код. Исполнена под **EPIC-IDS-12** (pkg-000038), 6 tasks.
> **Контекст:** гэп **G-5** из [full-audit §3](./identity-backend-full-audit-2026-06-24.md) (`aud` не валидировался; форма импорта ключа raw vs b64url не сверена).
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): pkg-000038, SEC-03 🟢 (стр.11,70,126,686-691).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| `aud` в registry | `aud={"essential": True, "value": "authenticated"}` ([supabase_validator.py:22](../../src/core/auth/supabase_validator.py)) — **валидируется** |
| iss/sub/exp/role сохранены | iss/sub/exp essential ([:19-21](../../src/core/auth/supabase_validator.py)); явная проверка `role != authenticated` ([:35-36](../../src/core/auth/supabase_validator.py)); `sub` непустой ([:38-40](../../src/core/auth/supabase_validator.py)) |
| Форма импорта ключа | `OctKey.import_key(jwt_secret)` (raw) ([:17](../../src/core/auth/supabase_validator.py)) — подтверждена каноном (тест ниже) |
| alg-pinning | `algorithms=["HS256"]` ([:27](../../src/core/auth/supabase_validator.py)); тест `test_alg_none_attack_rejected` |
| Тесты | [test_supabase_jwt_validator.py](../../tests/test_supabase_jwt_validator.py) — 9 (incl. `wrong_aud`, `missing_aud`, `raw_octkey_import_is_canonical`) |
| Спека 09 | G-5 «закрыт SEC-03» ([09:6,43,48](../requirements/09-supabase-jwt-validation.md)); residual-note «aud не валидируется» **удалён** |
| Decision-doc | [`epic-ids-12-sec-03-jwt-aud-decision-2026-06-26.md`](./epic-ids-12-sec-03-jwt-aud-decision-2026-06-26.md) — существует (live-sanity raw-ключа) |
| **Offline-сюита** | **379 passed, 12 deselected** ✅ (совпадает с индексом; +1 deselected = live key-import sanity) |

---

## 1. Актуализация тасков и story (по коду)

| Таск (EPIC-IDS-12, pkg-000038) | Факт | Статус |
|--------------------------------|------|--------|
| t01 live supabase jwt aud decision record | decision-doc + spec 09 нота | 🟢 |
| t02 confirm octkey import form live token | live_integration sanity (deselected offline) + offline канон-тест | 🟢 |
| t03 aud claim registry or spec waiver | `aud` в `JWTClaimsRegistry` ([:22](../../src/core/auth/supabase_validator.py)) | 🟢 |
| t04 offline jwt aud key regression tests | `wrong_aud`/`missing_aud`/`raw_octkey_canonical` | 🟢 |
| t05 spec 09 g5 gap closure docs | spec 09 синхронизирован, note снят | 🟢 |
| t06 story acceptance verification | AC 5/5 (см. §2) | 🟢 |
| **STORY-IDS-SEC-03** | JWT hardening (`aud` + key-import) | **🟢 Done** |

**Индекс корректен:** `EPIC-IDS-12 … SEC-01 🟢; SEC-01b 🟢; SEC-02 🟢; SEC-03 🟢` ([bullrun-launch-index.md:126](../tasks/bullrun-launch-index.md)); pkg-000038 Done, 379 offline (стр.11). **EPIC-IDS-SEC.md:26** — SEC-03 🟢 Done (в синхроне, без дрейфа).

> **G-5 закрыт.** Это последний реальный code-гэп из full-audit §3, относящийся к security-hardening. Эпик **EPIC-IDS-12 (SEC-01/01b/02/03)** по коду завершён.

---

## 2. Сверка Acceptance Criteria (по коду + тестам + докам)

| AC | Факт | Вердикт |
|----|------|---------|
| Принято/задокументировано решение по `aud` (валидировать ИЛИ note в 09) | **валидируется**; spec [09:43,48](../requirements/09-supabase-jwt-validation.md) + [decision-doc](./epic-ids-12-sec-03-jwt-aud-decision-2026-06-26.md) | ✅ |
| Если валидировать — тест: `aud≠authenticated` отклонён, `aud=authenticated` проходит | `test_wrong_aud_raises` ([:105](../../tests/test_supabase_jwt_validator.py)), `test_missing_aud_raises` ([:111](../../tests/test_supabase_jwt_validator.py)), happy `test_valid_token_returns_user_claims` | ✅ |
| Форма импорта ключа подтверждена против реального токена; код+спека одна форма | raw `OctKey.import_key` ([:17](../../src/core/auth/supabase_validator.py)); offline-канон `test_raw_octkey_import_is_canonical_for_supabase_hs256` ([:122](../../tests/test_supabase_jwt_validator.py)) + live sanity; spec [09:92](../requirements/09-supabase-jwt-validation.md) raw | ✅ |
| G-5 разрыв код↔спека устранён (нет открытых «честных note») | grep по 09: residual «не валидируется/намеренно не» = **0** | ✅ |
| Регрессий нет: iss/sub/exp/role сохранены | registry + role/sub-проверки; тесты `iss_mismatch`, `expired`, `wrong_signature`, `alg_none_attack` зелёные | ✅ |

**Вывод:** все 5 AC выполнены кодом+тестами+доками. Покрытие валидатора — 9 тестов, включая защиту от `alg=none` и канон-сверку формы ключа (raw vs b64url-обёртка).

---

## 3. Findings (severity + как закрыть; без реализации)

Код SEC-03 — без материальных дефектов. Единственный finding — **doc-staleness** (рекуррентный паттерн чекбоксов).

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F1** | MEDIUM | Doc-stale (внутр. противоречие) | Story `Status: 🟢 Done` (стр.6), но **все 5 AC = `[ ]`** (стр.29-33) — при выполненных. **Как закрыть:** проставить AC `[x]`. | [`STORY-IDS-SEC-03...md:29-33`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md) |

> **Без F2:** в отличие от SEC-01b/SEC-02, пакет-индекс [`EPIC-IDS-SEC.md:26`](../tasks/backlog-stories/security-hardening/EPIC-IDS-SEC.md) держит SEC-03 = **🟢 Done** (синхронно) — дрейфа состава нет.

Наблюдения (severity none, **не gaps**):
- **O1:** `aud` зафиксирован как `value="authenticated"` (одно значение). Supabase для anon-токенов использует `aud="authenticated"` после логина — соответствует целевой модели (anon-доступ в identity не нужен). Если в будущем понадобится несколько audience — расширяемо, но сейчас корректно.
- **O2:** raw-импорт ключа подтверждён каноном offline **и** live-sanity (decision-doc) — форма зафиксирована однозначно, «честная note» о неопределённости снята.

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **379 passed, 12 deselected** (было 375 → **+4** offline JWT-теста; deselected 11→12: +1 live key-import sanity) |
| Изменение валидатора | +`aud` в registry + `sub`-непустой — аддитивно; iss/exp/role-путь сохранён |
| Прочие auth-потребители (`/me`, OAuth bearer, eID/phone) | принимают те же Supabase-JWT — сюита зелёная |

Регрессий не выявлено (ужесточение `aud` совместимо: реальные Supabase-токены после логина несут `aud=authenticated`).

---

## 5. Итог

- **SEC-03 — 🟢 исполнена полно:** `aud=authenticated` валидируется через `JWTClaimsRegistry`; форма импорта ключа подтверждена raw (offline-канон + live-sanity); spec 09 синхронизирован, G-5 note снят; iss/sub/exp/role сохранены; защита от `alg=none`. AC 5/5, 9 тестов. Таски t01–t06 🟢; индексы (bullrun + EPIC-IDS-SEC) корректны.
- **G-5 закрыт** → EPIC-IDS-12 (SEC-01/01b/02/03) по коду завершён. Остаток full-audit §3: G-2a/G-3 (PV-09), G-4 (CLEANUP-04) — вне SEC.
- **Findings:** только **F1** (story AC `[ ]` при Status 🟢). F2 (состав-дрейф) **не возник** — EPIC-IDS-SEC SEC-03 уже 🟢.
- **Регрессий нет** (379 passed).

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; 6 тасков + story + 5 AC сверены по коду, тестам и докам.
- [x] AC4 (нет открытых note) проверен grep'ом по спеке 09 — residual = 0.
- [x] Форма ключа: offline-канон-тест (raw vs b64url) **и** live-sanity decision-doc — оба подтверждают raw.
- [x] Регрессий нет; 375→379 (+4 offline / +1 live deselected) объяснён; индекс 379 = факт.
- [x] G-5-завершённость и закрытие эпика SEC зафиксированы; единственный finding (F1) отделён от кода (дефектов нет).
