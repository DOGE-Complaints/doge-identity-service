# STORY-IDS-DOC-DRAFT-05 — Browser-submit security canon sync (identity docs)

## Meta
- **Key:** `STORY-IDS-DOC-DRAFT-05-browser-submit-security-canon-sync`
- **Пакет:** [`story-draft-handoff/`](./INDEX.md) (cross-repo; gateway handoff)
- **Status:** 🟢 Done — docs-sync выполнен, verified по коду/докам 2026-07-04 (см. «Статус исполнения» ниже). ⚠️ Выполнено **вне pipeline** — нет pkg-записи в [`bullrun-launch-index`](../../bullrun-launch-index.md).
- **Тип:** docs (runtime-docs identity only)
- **Основание:** D-DRAFT-5 ([gateway interview](../../../../../doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/interview-story-draft-handoff-2026-07-03.md)); [GW-DRAFT-03](../../../../../doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon.md) (gateway-side supersede + этот файл-указатель)
- **Зависит от:** gateway GW-DRAFT-01/02 Done (browser-submit as-built в gateway)
- **Решения (интервью 2026-07-04):** [`identity-mvp-hardening-interview`](../../../analysis/identity-mvp-hardening-interview-2026-07-04.md) — **D-6:** GPT↔identity OAuth (`/oauth/authorize|token|introspect`) **остаётся каноном**; стори лишь фиксирует, что подача истории — браузером, не трогая статус OAuth в коде. ⚠️ Наблюдение (вне scope): у `/oauth/introspect` после удаления gateway-клиента может не остаться потребителя — отдельный вопрос позже.

## Статус исполнения (verified 2026-07-04)
Обе цели **приведены к browser-submit** и это подтверждается кодом/доками:
- [`04-security.md`](../../../runtime-docs/04-security.md): §A = «browser-submit + OAuth» ([:9,11](../../../runtime-docs/04-security.md)), browser-submit sequence ([:33-73](../../../runtime-docs/04-security.md)), **Superseded GW-DRAFT-03** ([:92-94](../../../runtime-docs/04-security.md)); OAuth/introspection сохранены (D-6, [:108](../../../runtime-docs/04-security.md)).
- [`09-gateway-expectations.md`](../../../runtime-docs/09-gateway-expectations.md): §«Подача истории (browser-submit handoff)» ([:15-29](../../../runtime-docs/09-gateway-expectations.md)), auth-model таблица совпадает с реальными роутами gateway (`POST /story-drafts`, `GET /{id}`, `POST /{id}/submit`); OAuth сохранён (D-6).
- Не-superseded «GPT сам шлёт» = 0 (только в Superseded-блоках); cross-links на gateway as-built присутствуют и резолвятся.

## Зачем (исходная постановка)
Gateway развернул модель «браузер сабмитит» (story-draft handoff). Identity runtime-docs описывали **GPT-direct submit** как каноничный user path. Нужно было привести identity SSOT к browser-submit **в этом репозитории** — gateway сам чужой канон не правит (D-DRAFT-5). ✅ Выполнено.

## Scope (in)
- Обновить [`04-security.md`](../../../runtime-docs/04-security.md) **§A** sequence + шаги: GPT стешит → браузер сабмитит; убрать/пометить superseded «GPT сам шлёт историю в gateway»
- Обновить [`09-gateway-expectations.md`](../../../runtime-docs/09-gateway-expectations.md) блок «Подача истории из GPT» (L13–18 area): browser-submit + `/story-drafts*` на gateway
- Сохранить валидные части: introspection/OAuth для GPT Actions, `/me`, `phone_verified`, `verification_required` канон
- Ссылка на gateway as-built: [`API_REFERENCE`](../../../../../doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md) §6.8, [`story-draft-handoff`](../../../../../doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/INDEX.md)

## Out of scope
- Правки gateway `src/` или gateway backlog (GW-DRAFT-04 code removal)
- SPA/GPT client implementation

## Инвентарь доков (что синхронизируем)
| Док | Что сейчас | Действие |
|-----|-----------|----------|
| [`04-security.md`](../../../runtime-docs/04-security.md) §A | sequence «GPT сам шлёт историю в gateway» | ⚠️ **REWRITE** → browser-submit; старое пометить superseded |
| [`09-gateway-expectations.md`](../../../runtime-docs/09-gateway-expectations.md) блок «Подача истории из GPT» | GPT-direct submit | ⚠️ **REWRITE** → `/story-drafts*` browser-submit |
| OAuth/introspection/`/me`/`phone_verified`/`verification_required` канон | описан | ✅ **KEEP** (D-6 — OAuth остаётся) |

## Change-propagation (все затронутые)
- [`04-security.md`](../../../runtime-docs/04-security.md), [`09-gateway-expectations.md`](../../../runtime-docs/09-gateway-expectations.md); указатель в gateway [`security-env-api-access.md`](../../../../../doge-complaints-gateway/docs/runtime-docs/security-env-api-access.md) §4.2 (кросс-ссылка, gateway-сторона — не правим).
- Если есть doc-тест на содержимое runtime-docs — синхронизировать. **НЕ трогать** gateway `src/`/backlog (D-DRAFT-5) и OAuth-статус в коде (D-6).

## Подзадачи
- **T01 — Инвентарь.** Найти точные места в [`04-security.md`](../../../runtime-docs/04-security.md) §A и [`09-gateway-expectations.md`](../../../runtime-docs/09-gateway-expectations.md), где утверждается GPT-direct submit; сверить с gateway as-built ([`API_REFERENCE`](../../../../../doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md) §6.8, [`story-draft-handoff`](../../../../../doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/INDEX.md)).
- **T02 — 04-security §A.** Переписать sequence на browser-submit: GPT стешит (`POST /story-drafts`, service-auth) → браузер сабмитит (`POST /story-drafts/{id}/submit`, Supabase Bearer) → gateway форвардит identity `/me` → гейт `phone_verified`. Старое «GPT сам шлёт» — пометить superseded, не удаляя контекст.
- **T03 — 09-gateway-expectations.** Блок подачи истории → browser-submit + `/story-drafts*`; **сохранить** OAuth/introspection/`/me` как валидные (D-6).
- **T04 — Cross-links.** Добавить ссылки на gateway as-built; убедиться, что identity-канон не противоречит gateway.
- **T05 — Gate.** `grep` «GPT сам создаёт историю» без superseded-контекста = 0; OAuth-канон сохранён (D-6); ссылки резолвятся; doc-тест (если есть) зелёный.

## Acceptance Criteria
- [x] `04-security.md` §A отражает browser-submit как актуальный user story path (verified [:9,33-73](../../../runtime-docs/04-security.md))
- [x] `09-gateway-expectations.md` не утверждает «GPT сам создаёт историю» без superseded-контекста (verified [:29](../../../runtime-docs/09-gateway-expectations.md))
- [x] Cross-links на gateway story-draft-handoff docs присутствуют (API_REFERENCE §6.8, security-env-api-access §4)

## Швы
[`04-security.md`](../../../runtime-docs/04-security.md), [`09-gateway-expectations.md`](../../../runtime-docs/09-gateway-expectations.md); gateway pointer в [`security-env-api-access.md`](../../../../../doge-complaints-gateway/docs/runtime-docs/security-env-api-access.md) §4.2.
