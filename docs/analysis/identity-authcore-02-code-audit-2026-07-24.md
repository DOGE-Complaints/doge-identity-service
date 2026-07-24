# Аудит по коду: STORY-IDS-AUTHCORE-02 (`/me` account fields) — 2026-07-24

> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — verified-state, только проверяемые claims с путями; регрессии; gaps с severity + как закрыть. Findings-only (реализацию не предлагаю).
> **Объект:** [`STORY-IDS-AUTHCORE-02-me-account-fields`](../tasks/backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md) (pkg-000044).
> **Синхронизирован отчёт:** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) — статусы task/story подтверждены аудитом (drift не найден); findings ниже вынесены в gap-queue индекса.
> **Решения-основа:** [`identity-cabinet-me-fields-interview-2026-07-13`](identity-cabinet-me-fields-interview-2026-07-13.md) (D-CAB-1/2/3).

---

## Вердикт

**STORY-IDS-AUTHCORE-02 = 🟢 Done — подтверждено фактическим кодом.** Все 4 таска реализованы; scope-контракт (`created_at` + `account_status`, без `email`) исполнен точно по решениям D-CAB-1/2; регрессий нет; offline-сюита независимо перепрогнана зелёной (**405 passed, 12 deselected** — совпадает с [run-summary](../tasks/run-reports/identity-build-windows/run-summary-20260724-1223-epic-ids-07-authcore-02-pkg-000044.md)). Индекс `bullrun-launch-index.md` отражает статусы корректно — правок статусов не требуется.

Найдено **4 gap'а** (0×HIGH, 1×MEDIUM, 3×LOW) — все про **координацию/полноту umbrella-контракта CAB-02 и fidelity доков**, ни один не является дефектом реализации AUTHCORE-02.

---

## Пер-таск верификация (по коду)

| Task | Требование стори | Факт в коде | Вердикт |
|------|------------------|-------------|---------|
| **t01** me_response | базовый dict: `account_status="active"` + `created_at=None`; в `if profile is not None:` → `created_at=_format_datetime(profile.created_at)` | [`me_response.py:33-34`](../../src/core/api/me_response.py) (base) + [`:48`](../../src/core/api/me_response.py) (profile-блок); `email`/`email_verified` НЕ добавлены (правильно — ONB-01) | ✅ Done |
| **t02** api-docs | `openapi.yaml MeData`: `created_at [string,null]` date-time + `account_status` enum + «MVP: active»; `API_REFERENCE.md §6` — те же | [`openapi.yaml:84-91`](../runtime-docs/api-reference/openapi.yaml) (`created_at` nullable+desc, `account_status` enum `[active,pending,suspended,archived]` + desc «MVP: always emits `active`»); [`API_REFERENCE.md:82-83,93-94`](../runtime-docs/api-reference/API_REFERENCE.md) | ✅ Done |
| **t03** tests | с профилем → ISO `created_at`; без профиля → `null`; `account_status=="active"` в обоих | [`test_me_profile.py:83-84,86`](../../tests/test_me_profile.py) (профиль) + [`:149-150`](../../tests/test_me_profile.py) (no-profile, + проверка `repo.get_by...(...) is None`) | ✅ Done |
| **t04** (pipeline) story acceptance verification | верификация приёмки | run-summary t04 🟢; ⚠️ это **не** исходный T04 стори (см. G4) | ✅ Done (иной scope) |

**Guard-проверки (независимо перепрогнаны):**
- `grep account_status supabase/bootstrap/` → **пусто** — миграции/колонки нет (D-CAB-1 соблюдён). ✅
- `.venv/bin/python -m pytest -m "not live_integration"` → **405 passed, 12 deselected** (2026-07-24). ✅
- `pytest tests/test_me_profile.py` → **5 passed**. ✅

**AC стори:** все 5 пунктов `[x]` ([story:56-60](../tasks/backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md)) — каждый подтверждён кодом выше. Status 🟢 Done в обеих копиях (backlog + epic-materialized) и в [INDEX auth-core](../tasks/backlog-stories/auth-core/INDEX.md) (2/2, 100%).

---

## Регрессии

**Не найдено.** Существующие поля `/me` (`supabase_user_id/role/display_name/eid_*/phone_*/avatar_url`) не тронуты ([`me_response.py:19-47`](../../src/core/api/me_response.py)); envelope `{data:{…}}` цел ([`test_me_profile.py:157-162`](../../tests/test_me_profile.py)); политика no-auto-provision сохранена (no-profile → 200, `created_at=null`, `account_status="active"`, БД не пишется — [`:132-154`](../../tests/test_me_profile.py)); новых миграций нет.

---

## Gaps (findings)

| ID | Severity | Суть | Файл:строка | Как закрыть |
|----|----------|------|-------------|-------------|
| **G1** | **MEDIUM** | **Umbrella CAB-02 закрыт лишь на 2/3.** Контракт CAB-02 (§0) для identity = `email` + `created_at` + `account_status`. AUTHCORE-02 отдал `created_at`+`account_status`, но **`email` в `/me` отсутствует** ([`me_response.py`](../../src/core/api/me_response.py) — grep `email` пусто) → карточка «Account Summary» не может показать Email. AUTHCORE-02 Done ≠ CAB-02 разблокирован. | `me_response.py` (нет `email`); SPA-потребитель [`STORY-SPA-CAB-02`](../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-02-account-summary-block.md) | Исполнить [`ONB-01`](../tasks/backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md) (`email`+`email_verified`, D-CAB-3) — уже next-recommended в индексе. |
| **G2** | **LOW** | **Cross-repo drift: SPA-контракт устарел.** SPA §0/§4 всё ещё помечает поля как «❌ отсутствуют в контракте / placeholder / нужен identity-extension», хотя identity уже отдаёт `created_at`+`account_status`; и не несёт caveat'ов (`account_status` всегда `active`, `created_at` может быть `null`). Исходный **опциональный** T04 (аннотировать SPA §0) в pkg-000044 не выполнялся. | [`STORY-SPA-CAB-api-requirements.md:17,39-43,100`](../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-api-requirements.md) | Обновить SPA §0/§4: `created_at`+`account_status` — «live (AUTHCORE-02)», пометить `account_status="active"`-константу и `created_at`-nullable placeholder. (spa-сторона, вне identity pkg.) |
| **G3** | **LOW** | **Doc-fidelity: семантика `created_at` не вынесена потребителю.** `created_at` = `profiles.created_at` = «первая верификация», **не** дата регистрации (label «Account Created» неточен для UI). Caveat зафиксирован только в [interview-отчёте D-CAB-2](identity-cabinet-me-fields-interview-2026-07-13.md), но в consumer-facing api-reference описание источник указывает без семантической оговорки. | [`openapi.yaml:87`](../runtime-docs/api-reference/openapi.yaml), [`API_REFERENCE.md:83`](../runtime-docs/api-reference/API_REFERENCE.md) | Добавить в описание `created_at` оговорку «профиль создан при первой верификации, не дата регистрации». |
| **G4** | **LOW** | **Traceability: t04 подменён.** Backlog-стори перечисляет T04 = опциональная SPA §0-пометка ([story:47](../tasks/backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md)), а pipeline исполнил t04 = «story acceptance verification». «4/4 tasks Done» в индексе считает **иной** t04, чем нумерует backlog-стори. Не дефект (T04 был `(опц.)`), но нумерация расходится. | [`bullrun:587`](../tasks/bullrun-launch-index.md) vs [`story:47`](../tasks/backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md) | Синхронизировать текст T04 backlog-стори с фактически исполненным (verification) либо явно пометить SPA §0-пометку как отдельный cross-repo item (= G2). |

---

## Итог для индекса

- Статусы task/story AUTHCORE-02 в `bullrun-launch-index.md` — **факт-верны**, drift не найден; правок статусов нет.
- Findings G1–G4 добавлены в gap-queue индекса (override-only) со ссылкой на этот отчёт.
- **Единственный блокер полноты CAB-02** — G1 (`email`/ONB-01), уже помеченный next-recommended. G2/G3/G4 — LOW, координация доков.
