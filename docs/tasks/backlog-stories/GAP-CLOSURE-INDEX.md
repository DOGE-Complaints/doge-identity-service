# GAP-CLOSURE-INDEX — мини-индекс закрытия гэпов backend-аудита

> **Создано:** 2026-06-26 · **Источник:** [`docs/analysis/identity-backend-full-audit-2026-06-24.md`](../../analysis/identity-backend-full-audit-2026-06-24.md) §3 (реальные code-гэпы) + §1/§4 (doc).
> **Назначение:** один лист, чтобы ничего не упустить — все новые стори, заведённые по итогам системного аудита, с привязкой к гэпу, severity и пакету. Все — ⚪ Todo.

## Новые стори по реальным гэпам (§3 аудита)

| Story | Гэп | Severity | Пакет | Суть | Статус |
|-------|-----|----------|-------|------|--------|
| [SEC-01 rate-limiting](security-hardening/STORY-IDS-SEC-01-rate-limiting.md) | G-1 | **HIGH** | 📁 `security-hardening/` | eid/start + callback HTTP 429 (pkg-000035) | 🟢 Done |
| [SEC-01b phone/request HTTP rate-limit](security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md) | G-1 (остаток) | **HIGH** | 📁 `security-hardening/` | `POST /auth/phone/request` per-user 429 (pkg-000036) | 🟢 Done |
| [SEC-02 audit IP/UA hashing](security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md) | G-2b | **HIGH** | 📁 `security-hardening/` | HMAC-хеш IP/UA в eID **и** phone аудит (pkg-000037) | 🟢 Done |
| [SEC-03 JWT validation hardening](security-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md) | G-5 | LOW | 📁 `security-hardening/` | `aud=authenticated` + raw key-import канон (pkg-000038) | 🟢 Done |
| [PV-09 durable phone-persistence](phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md) | G-2a + G-3 + bootstrap | **HIGH**/MED | 📁 `phone-verification/` | Supabase session-стор + audit-репо + `phone_audit_events` + bootstrap parity (pkg-000039) | 🟢 Done |

> **G-1 fully closed:** SEC-01 (eid/start+callback) + SEC-01b (phone/request). **G-2 closed:** G-2a/G-3 → PV-09, G-2b → SEC-02. **G-5 closed:** SEC-03. Все реальные code-гэпы full-audit §3 — 🟢. Остаток — только **G-4** (doc).
> **G-4** (LOW, eID отложен: `CODE_VERIFIER_ENCRYPTION_KEY`/AES-GCM vs `EID_SESSION_ENC_KEY`/Fernet) — не отдельная стори, свёрнут в doc-стори **CLEANUP-04** (решение по неймингу/алгоритму, не код).

## Документация (отдельная стори, по запросу)

| Story | Тип | Пакет | Суть | Статус |
|-------|-----|-------|------|--------|
| [CLEANUP-04 spec-reconciliation](cleanup/STORY-IDS-CLEANUP-04-spec-reconciliation.md) | doc task | 📁 `cleanup/` | переписать/deprecate gateway-копии (req 06/07 + impl-epic-01..06, HD-1); синхронизировать тела eID-спеков 11/12/17/18 (descriptor-рефактор, redirect-маркеры); решить крипто-нейминг G-4 | ⚪ Todo |

## Что уже сделано в самом аудите (НЕ требует стори — для полноты)
- ✅ Спек 10 (`/me`), 13 (verified-hash), 08/09 (статус+миграции), новый 19 (phone-flow), баннеры на gateway-копиях/eID-спеках, runtime-docs 01/08, docs/Identity — актуализированы в ходе аудита (решения Q1/Q3/Q4). Остаток глубокой переработки → CLEANUP-04.

## Структурная уборка корня backlog-stories (2026-06-26)
- 📁 **`cleanup/`** — вынесен из корня (CLEANUP-01/02/03 + новый 04); ~60 inbound-ссылок перепроверены link-check'ом, 0 новых битых.
- 📁 **`auth-core/`** (`AUTHCORE-01` + эпик) и 📁 **`eid/`** (`EID-01/03..08` + эпик) — вынесены из корня (2026-06-26, resolution-aware скрипт: ~30–38 inbound на тему переписаны, pipeline-копии не затронуты, link-check 594=594 → 0 новых битых). Корень backlog-stories теперь содержит только `INDEX.md` + этот мини-индекс.
- **Статусы:** все 8 перенесённых стори — **🟢 Done** (код построен). У `EID-03` и `EID-08` story-файлы держали стейл `⚪ Todo` при `🟢` в эпике — синхронизировано на 🟢 по факту кода (`providers/registry.py`, `security/session_secret.py`).
- Полная карта пакетов — [`INDEX.md`](INDEX.md).

## Статус (синхр. 2026-06-26)
**Все реальные code-гэпы аудита §3 закрыты** 🟢: G-1 (SEC-01/01b), G-2a/G-3 (PV-09), G-2b (SEC-02), G-5 (SEC-03). Остаётся только **doc**: **CLEANUP-04** (⚪, вкл. G-4 крипто-нейминг) — спек-гигиена, не код.

## Что ещё доработать по identity (полная карта — [`INDEX.md`](INDEX.md))
1. **Онбординг** (`identity-onboarding/`): identity-backend остаток — **только `ONB-01`** (email в `/me` + Supabase Confirm). `DOC-ONB-01/05` — ✅ уже покрыты построенным кодом/доками; `DOC-ONB-02/03(landing)/04` — 🔵 frontend/product (spa-app), не identity-backend. Подробности — в [`EPIC-IDS-ONBOARDING`](identity-onboarding/EPIC-IDS-ONBOARDING.md) §«Актуальность».
2. **CLEANUP-04** (doc) — переписать/deprecate gateway-копии спеков + eID-спек drift + G-4.
3. 🟦 **POST-MVP (ждёт донейшнов на оплату SK):** боевой eID — `EID-02/09…14` (`eid-deferred/`).
4. 🔧 **Внешнее/ops:** `SPIKE-PV-08` (Telnyx-аккаунт), `SPIKE-EID-09` (Authentigate demo) — long-lead, гейтят только live-тесты.
