# Bullrun launch index — doge-identity-service

**Зона:** `doge-identity-service/docs/tasks/`  
**Pipeline (SSOT):** [`ids-epic-execution-pipeline.md`](./ids-epic-execution-pipeline.md)  
**Builder Queue (Zeya888):** [`docs/methodology/Zeya888-builder-queue/core/workflow.md`](../../../docs/methodology/Zeya888-builder-queue/core/workflow.md) §Epic-first

**Коды статусов:** ⚪ Todo · 🟡 In Progress · 🔵 Implemented (Waiting Acceptance) · 🟢 Done

## Актуальная точка

- **Текущая волна:** EPIC-IDS-13 — **P6 Done** ONB-01 audit override (`run_mode=epic_ids_13_onb_01_audit_2026_07_24`, F2 🟢 t05, docs-only, 2026-07-24)
- **Предыдущая волна:** EPIC-IDS-13 — **P5 scaffold** ONB-01 audit (`run_mode=epic_ids_13_onb_01_audit_2026_07_24`, F2 ⚪ t05, docs-only, 2026-07-24)
- **Предыдущая волна:** EPIC-IDS-13 — **P3 Done** ONB-01 (`STORY-IDS-ONB-01-email-in-me-and-supabase-confirm`, pkg-000045, 4/4 tasks, 406 pytest offline, 2026-07-24)
- **Предыдущая волна:** EPIC-IDS-13 — **P1 materialize** ONB-01 (`STORY-IDS-ONB-01-email-in-me-and-supabase-confirm`, `input_mode=backlog_story`, pkg-000045, 4 tasks, 2026-07-24)
- **Предыдущая волна:** EPIC-IDS-07 — **P6 Done** AUTHCORE-02 audit override (`run_mode=epic_ids_07_authcore_02_audit_2026_07_24`, G3 🟢 t05, docs-only, 2026-07-24)
- **Предыдущая волна:** EPIC-IDS-07 — **P5 scaffold** AUTHCORE-02 audit (`run_mode=epic_ids_07_authcore_02_audit_2026_07_24`, G3 ⚪ t05, 2026-07-24)
- **Предыдущая волна:** EPIC-IDS-07 — **P3 Done** AUTHCORE-02 (`STORY-IDS-AUTHCORE-02-me-account-fields`, pkg-000044, 4/4 tasks, 405 pytest offline, 2026-07-24)
- **Audit (post-P3):** ONB-01 — [`identity-onb-01-code-audit-2026-07-24.md`](../analysis/identity-onb-01-code-audit-2026-07-24.md); 🟢 Done подтверждён кодом. **Override (закрыт):** `run_mode=epic_ids_13_onb_01_audit_2026_07_24` — F2 🟢 t05 (docs-only). **F1 🟢 closed** (spa cabinet-доки синхронизированы 2026-07-24: `email`+`email_verified` ✅ live). **F3** ignored. **CAB-02 identity = 3/3**.
- **Audit (post-P3):** AUTHCORE-02 — [`identity-authcore-02-code-audit-2026-07-24.md`](../analysis/identity-authcore-02-code-audit-2026-07-24.md); G3 🟢 closed (override t05); **G2 🟢 closed** (spa-контракт синхронизирован 2026-07-24); **G1 🟢 closed** (ONB-01 P3 Done); G4 ignored
- **Предыдущая волна:** EPIC-IDS-07 — **P1 materialize** AUTHCORE-02 (`STORY-IDS-AUTHCORE-02-me-account-fields`, `input_mode=backlog_story`, pkg-000044, 4 tasks, 2026-07-24)
- **Предыдущая волна:** EPIC-IDS-12 — **P6 Done** SEC-04 audit override (`run_mode=epic_ids_12_sec_04_audit_2026_07_09`, F1–F2 🟢 t06–t07, 405 pytest offline, 2026-07-09)
- **Re-audit (post-override):** SEC-04 — [`epic-ids-12-sec-04-reaudit-2026-07-09.md`](../analysis/epic-ids-12-sec-04-reaudit-2026-07-09.md); F1–F2/F4 🟢 closed; F3 🟢 waived (operator manual rotation; spa [`rotation-decision-sec01.md`](../../../spa-app/docs/tasks/epics/EPIC-SPA-05-security-hardening/stories/STORY-SPA-SEC-01-remove-service-role-from-frontend/task-spa-sec-01-t05-rotation-decision-sec04-sync/rotation-decision-sec01.md))
- **Audit (post-P3):** SEC-04 — [`epic-ids-12-sec-04-audit-2026-07-09.md`](../analysis/epic-ids-12-sec-04-audit-2026-07-09.md)
- **Предыдущая волна:** EPIC-IDS-12 — **P5 scaffold** SEC-04 audit (`run_mode=epic_ids_12_sec_04_audit_2026_07_09`, F1–F2 ⚪ t06–t07, 2026-07-09)
- **Предыдущая волна:** EPIC-IDS-12 — **P3 Done** SEC-04 (`STORY-IDS-SEC-04-service-role-isolation`, pkg-000043, 5/5 tasks, 402 pytest offline, 2026-07-09)
- **Next recommended (HK 2026-07-24):** CLEANUP-04; then DOC-ONB-02…04 / epic gates EPIC-IDS-07/08/12
- **Предыдущая волна:** EPIC-IDS-12 — **P1 materialize** SEC-04 (`STORY-IDS-SEC-04-service-role-isolation`, pkg-000043, 5 tasks, input_mode `backlog_story`, 2026-07-09)
- **Предыдущая волна:** EPIC-IDS-12 — **P6 Done** SEC-06 audit override (`run_mode=epic_ids_12_sec_06_audit_2026_07_04`, F1–F2 🟢, 398 pytest offline, 2026-07-04)
- **Предыдущая волна:** EPIC-IDS-12 — **P5 scaffold** SEC-06 audit (`run_mode=epic_ids_12_sec_06_audit_2026_07_04`, F1–F2 ⚪, 2 tasks, 2026-07-04)
- **Предыдущая волна:** EPIC-IDS-12 — **P3 Done** SEC-06 (`STORY-IDS-SEC-06-supabase-jwks-es256-hardening`, pkg-000042, 8/8 tasks, 398 pytest offline, 2026-07-04) · audit: [`epic-ids-12-sec-06-audit-2026-07-04.md`](../analysis/epic-ids-12-sec-06-audit-2026-07-04.md)
- **Предыдущая волна:** EPIC-IDS-10 — **P6 Done** PV-10 audit override (`run_mode=epic_ids_10_pv_10_audit_2026_06_28`, F1 🟢, docs-only grep gate, 2026-06-28)
- **Предыдущая волна:** EPIC-IDS-10 — **P5 scaffold** PV-10 audit (`run_mode=epic_ids_10_pv_10_audit_2026_06_28`, 1 task F1 ⚪, 2026-06-28)
- **Предыдущая волна:** EPIC-IDS-10 — **P3 Done** PV-10 (`STORY-IDS-PV-10-file-sms-sink-dev`, pkg-000041, 394 pytest offline, 2026-06-28)
- **Предыдущая волна:** EPIC-IDS-10 — **P1 materialize** PV-10 (`STORY-IDS-PV-10-file-sms-sink-dev`, pkg-000041, 7 tasks, input_mode `backlog_story`, 2026-06-28)
- **Audit (post-P3):** SEC-06 — [`epic-ids-12-sec-06-audit-2026-07-04.md`](../analysis/epic-ids-12-sec-06-audit-2026-07-04.md); **override (закрыт):** `run_mode=epic_ids_12_sec_06_audit_2026_07_04` — F1–F2 🟢 (398 pytest offline, 2026-07-04)
- **Audit (post-P3):** PV-10 — [`epic-ids-10-pv-10-file-sms-sink-audit-2026-06-28.md`](../analysis/epic-ids-10-pv-10-file-sms-sink-audit-2026-06-28.md); **override (закрыт):** `run_mode=epic_ids_10_pv_10_audit_2026_06_28` — F1 🟢 (docs-only grep gate, 2026-06-28)
- **Предыдущая волна:** EPIC-IDS-13 — **P3 Done** ONB-01 (`DOC-IDS-ONB-01-lazy-phone-gate-contract`, pkg-000040, docs-only grep gate, 2026-06-26)
- **Предыдущая волна:** EPIC-IDS-13 — **P1 materialize** ONB-01 (`DOC-IDS-ONB-01-lazy-phone-gate-contract`, pkg-000040, 5 tasks, input_mode `backlog_story`, 2026-06-26)
- **Предыдущая волна:** EPIC-IDS-10 — **P3 Done** PV-09 (`STORY-IDS-PV-09-durable-phone-persistence`, pkg-000039, 386 pytest offline, 2026-06-26)
- **Предыдущая волна:** EPIC-IDS-10 — **P1 materialize** PV-09 (`STORY-IDS-PV-09-durable-phone-persistence`, pkg-000039, 7 tasks, input_mode `backlog_story`, 2026-06-26)
- **Предыдущая волна:** EPIC-IDS-12 — **P3 Done** SEC-03 (`STORY-IDS-SEC-03-jwt-validation-hardening`, pkg-000038, 379 pytest offline, 2026-06-26)
- **Предыдущая волна:** EPIC-IDS-12 — **P1 materialize** SEC-03 (`STORY-IDS-SEC-03-jwt-validation-hardening`, pkg-000038, 6 tasks, input_mode `backlog_story`, 2026-06-26)
- **Предыдущая волна:** EPIC-IDS-12 — **P3 Done** SEC-01b (`STORY-IDS-SEC-01b-phone-request-http-rate-limit`, pkg-000036, 371 pytest offline, 2026-06-26)
- **Предыдущая волна:** EPIC-IDS-12 — **P6 Done** SEC-01 audit override (`run_mode=epic_ids_12_sec_01_audit_2026_06_26`, F1–F2 🟢, 370 pytest offline, 2026-06-26)
- **Предыдущая волна:** EPIC-IDS-12 — **P5 scaffold** SEC-01 audit gaps (`run_mode=epic_ids_12_sec_01_audit_2026_06_26`, F1–F2 ⚪, 2 tasks, 2026-06-26)
- **Предыдущая волна:** EPIC-IDS-12 — **P3 Done** SEC-01 (`STORY-IDS-SEC-01-rate-limiting`, pkg-000035, 369 pytest offline, 2026-06-26)
- **Audit (post-P3):** SEC-01 — [`epic-ids-12-sec-01-audit-2026-06-26.md`](../analysis/epic-ids-12-sec-01-audit-2026-06-26.md); **override (закрыт):** `run_mode=epic_ids_12_sec_01_audit_2026_06_26` — F1–F2 🟢 (370 pytest offline, 2026-06-26)
- **Предыдущая волна:** EPIC-IDS-12 — **P1 materialize** SEC-01 (`STORY-IDS-SEC-01-rate-limiting`, pkg-000035, 7 tasks, input_mode `backlog_story`, 2026-06-26)
- **Предыдущая волна:** EPIC-IDS-11 — **P3 Done** OAUTH-04 (`STORY-IDS-OAUTH-04-verify-gate-and-verification-required`, pkg-000034, 366 pytest offline, 2026-06-24)
- **Предыдущая волна:** EPIC-IDS-11 — **P1 materialize** OAUTH-04 (`STORY-IDS-OAUTH-04-verify-gate-and-verification-required`, pkg-000034, 7 tasks, input_mode `backlog_story`, 2026-06-24)
- **Предыдущая волна:** EPIC-IDS-11 — **P6 Done** OAUTH-02 audit override (`run_mode=epic_ids_11_oauth_02_audit_2026_06_24`, F2–F4 🟢, 351 pytest offline, 2026-06-02)
- **Предыдущая волна:** EPIC-IDS-11 — **P5 scaffold** OAUTH-02 audit gaps (`run_mode=epic_ids_11_oauth_02_audit_2026_06_24`, 3 tasks F2–F4 ⚪, 2026-06-24)
- **Предыдущая волна:** EPIC-IDS-11 — **P3 Done** OAUTH-02 (`STORY-IDS-OAUTH-02-introspection-and-service-token`, pkg-000030, 350 pytest offline, 2026-06-24)
- **Предыдущая волна:** EPIC-IDS-11 — **P1 materialize** OAUTH-02 (`STORY-IDS-OAUTH-02-introspection-and-service-token`, pkg-000030, 6 tasks, input_mode `backlog_story`, 2026-06-24)
- **Предыдущая волна:** EPIC-IDS-11 — **P6 Done** OAUTH-01 audit override (`run_mode=epic_ids_11_oauth_01_audit_2026_06_24`, F1–F3 🟢, docs-only, 2026-06-02)
- **Предыдущая волна:** EPIC-IDS-11 — **P5 scaffold** OAUTH-01 audit gaps (`run_mode=epic_ids_11_oauth_01_audit_2026_06_24`, 3 tasks, 2026-06-24)
- **Audit (post-P3):** OAUTH-02 — [`epic-ids-11-oauth-02-audit-2026-06-24.md`](../analysis/epic-ids-11-oauth-02-audit-2026-06-24.md); **override (закрыт):** `run_mode=epic_ids_11_oauth_02_audit_2026_06_24` — F2–F4 🟢 (351 pytest offline, 2026-06-02)
- **Audit (post-P3):** OAUTH-01 — [`epic-ids-11-oauth-01-audit-2026-06-24.md`](../analysis/epic-ids-11-oauth-01-audit-2026-06-24.md); **override (закрыт):** `run_mode=epic_ids_11_oauth_01_audit_2026_06_24` — F1–F3 🟢 (docs-only)
- **Предыдущая волна:** EPIC-IDS-11 OAuth Server — **P3 Done** pkg-000029 (STORY-IDS-OAUTH-01 🟢, 341 pytest offline, 2026-06-24)
- **Предыдущая волна:** EPIC-IDS-11 OAuth Server — **P1 materialize** OAUTH-01 (`STORY-IDS-OAUTH-01-oauth-server-endpoints`, pkg-000029, 7 tasks, input_mode `backlog_story`, 2026-06-24)
- **Предыдущая волна:** EPIC-IDS-10 Phone Verification — **P3 Done** pkg-000028 (STORY-IDS-PV-07 🟢, 329 pytest offline, 2026-06-02)
- **Предыдущая волна:** EPIC-IDS-10 Phone Verification — **P1 materialize** PV-07 (`STORY-IDS-PV-07-telnyx-delivery-webhook`, pkg-000028, 6 tasks, input_mode `backlog_story`, 2026-06-11)
- **Предыдущая волна:** EPIC-IDS-10 Phone Verification — **P6 Done** PV-06 audit override (`run_mode=epic_ids_10_pv_06_audit_2026_06_11`, F1–F3 🟢, 314 pytest offline, 2026-06-02)
- **Предыдущая волна:** EPIC-IDS-10 Phone Verification — **P5 scaffold** PV-06 audit gaps (`run_mode=epic_ids_10_pv_06_audit_2026_06_11`, 2026-06-11)
- **Предыдущая волна:** EPIC-IDS-10 Phone Verification — **P3 Done** pkg-000027 (STORY-IDS-PV-06 🟢, 314 pytest offline, 2026-06-11)
- **Audit (post-P3):** PV-06 — [`epic-ids-10-pv-06-audit-2026-06-11.md`](../analysis/epic-ids-10-pv-06-audit-2026-06-11.md); **override (закрыт):** `run_mode=epic_ids_10_pv_06_audit_2026_06_11` — F1–F3 🟢 (314 pytest offline)
- **Предыдущая волна:** EPIC-IDS-10 Phone Verification — **P1 Done** pkg-000027 materialized (STORY-IDS-PV-06, 6 tasks, 2026-06-11)
- **Предыдущая волна:** EPIC-IDS-10 Phone Verification — **P3 Done** pkg-000026 (STORY-IDS-PV-05 🟢, 298 pytest offline, 2026-06-11)
- **Предыдущая волна:** EPIC-IDS-10 Phone Verification — **P1 Done** pkg-000026 materialized (STORY-IDS-PV-05, 6 tasks, 2026-06-11)
- **Предыдущая волна:** EPIC-IDS-10 Phone Verification — **P3 Done** pkg-000025 (STORY-IDS-PV-04 🟢, 288 pytest offline, 2026-06-11)
- **Предыдущая волна:** EPIC-IDS-10 Phone Verification — **P1 Done** pkg-000025 materialized (STORY-IDS-PV-04, 6 tasks, 2026-06-11)
- **Предыдущая волна:** EPIC-IDS-10 Phone Verification — **P3 Done** pkg-000024 (STORY-IDS-PV-03 🟢, 281 pytest offline, 2026-06-11)
- **Предыдущая волна:** EPIC-IDS-10 Phone Verification — **P1 Done** pkg-000024 materialized (STORY-IDS-PV-03, 6 tasks, 2026-06-11)
- **Предыдущая волна:** EPIC-IDS-10 Phone Verification — **P3 Done** pkg-000023 (STORY-IDS-PV-02 🟢, 268 pytest offline, 2026-06-11)
- **Предыдущая волна:** EPIC-IDS-10 Phone Verification — **P1 Done** pkg-000023 materialized (STORY-IDS-PV-02, 6 tasks, 2026-06-11)
- **Предыдущая волна:** EPIC-IDS-10 Phone Verification — **P3 Done** pkg-000022 (STORY-IDS-PV-01 🟢, 260 pytest offline, 2026-06-11)
- **Предыдущая волна:** EPIC-IDS-10 Phone Verification — **P1 Done** pkg-000022 materialized (STORY-IDS-PV-01, 6 tasks, 2026-06-11)
- **Предыдущая волна:** EPIC-IDS-09 eID Verification — **P3 Done** pkg-000021 (STORY-IDS-EID-08 🟢, 253 pytest offline, 2026-06-11)
- **Предыдущая волна:** EPIC-IDS-09 eID Verification — **P1 Done** pkg-000021 materialized (STORY-IDS-EID-08, 5 tasks, 2026-06-11)
- **Предыдущая волна:** EPIC-IDS-09 eID Verification — **P3 Done** pkg-000020 (STORY-IDS-EID-07 🟢, 244 pytest offline, 2026-06-10)
- **Предыдущая волна:** EPIC-IDS-09 eID Verification — **P1 Done** pkg-000020 materialized (STORY-IDS-EID-07, 6 tasks, 2026-06-10)
- **Предыдущая волна:** EPIC-IDS-09 — **P3 Done** pkg-000019 (STORY-IDS-EID-06 🟢, 232 pytest offline, 2026-06-09)
- **Предыдущая волна:** EPIC-IDS-09 — **P1 Done** pkg-000019 materialized (STORY-IDS-EID-06, 6 tasks, 2026-06-09)
- **Предыдущая волна:** EPIC-IDS-09 — **P3 Done** pkg-000018 (STORY-IDS-EID-05 🟢, 225 pytest offline, 2026-06-09)
- **Предыдущая волна:** EPIC-IDS-09 — **P1 Done** pkg-000018 materialized (STORY-IDS-EID-05, 5 tasks, 2026-06-08)
- **Предыдущая волна:** EPIC-IDS-09 — **P3 Done** pkg-000017 (STORY-IDS-EID-04 🟢, 222 pytest offline, immutable)
- **Предыдущая волна:** EPIC-IDS-09 — **P3 Done** pkg-000016 (STORY-IDS-EID-03 🟢, 218 pytest offline, immutable)
- **Предыдущая волна:** EPIC-IDS-08 Cleanup — **P3 Done** pkg-000014 (CLEANUP-03 🟢, docs-only, immutable)
- **Audit (post-P3):** CLEANUP-03 zero-gap — [`epic-ids-08-cleanup-03-audit-2026-06-06.md`](../analysis/epic-ids-08-cleanup-03-audit-2026-06-06.md); P5 scaffold **activation: none** (material gaps отсутствуют)
- **Audit (post-P3):** EID-01 — [`epic-ids-09-eid-01-audit-2026-06-06.md`](../analysis/epic-ids-09-eid-01-audit-2026-06-06.md); **override (закрыт):** `run_mode=epic_ids_09_eid_01_audit_2026_06_06` — F1 🟢 (F2/F3 deferred)
- **Audit (post-P3):** EID-03 — [`epic-ids-09-eid-03-audit-2026-06-08.md`](../analysis/epic-ids-09-eid-03-audit-2026-06-08.md); P5 scaffold **activation:** `run_mode=epic_ids_09_eid_03_audit_2026_06_08` (1 gap F1)
- **Audit (post-P3):** EID-04 — [`epic-ids-09-eid-04-audit-2026-06-08.md`](../analysis/epic-ids-09-eid-04-audit-2026-06-08.md); **override (закрыт):** `run_mode=epic_ids_09_eid_04_audit_2026_06_08` — F1–F2 🟢 (222 pytest offline)
- **Audit (post-P3):** EID-05 — [`epic-ids-09-eid-05-audit-2026-06-08.md`](../analysis/epic-ids-09-eid-05-audit-2026-06-08.md); **override (закрыт):** `run_mode=epic_ids_09_eid_05_audit_2026_06_08` — F1–F2 🟢 (docs-only)
- **Audit (post-P3):** EID-06 — [`epic-ids-09-eid-06-audit-2026-06-08.md`](../analysis/epic-ids-09-eid-06-audit-2026-06-08.md); **override (закрыт):** `run_mode=epic_ids_09_eid_06_audit_2026_06_08` — F1 🟢 (docs-only)
- **Предыдущая волна:** EPIC-IDS-08 Cleanup — **P3 Done** pkg-000013 (CLEANUP-02 🟢, 206 pytest offline, 2026-06-02); **override (закрыт):** `run_mode=epic_ids_08_cleanup_02_audit_2026_06_05` — F1–F3 🟢
- **Предыдущая волна:** EPIC-IDS-08 Cleanup — **P3 Done** pkg-000011 + **P3 Done** pkg-000012 (CLEANUP-01 + audit F1–F4 🟢, 200 pytest offline, 2026-06-05)
- **Закрыто (runtime):** EPIC-IDS-01 ✅ · EPIC-IDS-02 ✅ · EPIC-IDS-03 ✅ · EPIC-IDS-04 stories ✅ (pkg-000005, **epic gate pending**; override gaps RG-1/RG-2 ⚪)
- **input_mode (active):** `backlog_story` · **active story:** [`STORY-IDS-PV-10-file-sms-sink-dev`](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/STORY-IDS-PV-10-file-sms-sink-dev.md) · **backlog source:** [`STORY-IDS-PV-10-file-sms-sink-dev`](./backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md) · **status:** 🟢 Done (pkg-000041)
- **input_mode (default pkg):** `epic_story` · **override (закрыт):** `run_mode=epic_ids_03_audit_2026_05_28` · **override (partial):** `run_mode=epic_ids_04_audit_2026_05_30` (5/7 gaps closed; RG-1/RG-2 open) · **override (закрыт):** `run_mode=epic_ids_05_reaudit_2026_06_02` — 5/5 gaps 🟢 · **override (закрыт):** `run_mode=epic_ids_06_audit_2026_06_02` — F1–F5 🟢 (196 pytest offline, 2026-06-02) · **override (закрыт):** `run_mode=epic_ids_08_cleanup_02_audit_2026_06_05` — F1–F3 🟢 (206 pytest offline, 2026-06-02)
- **Active package (SSOT):** [`identity-active-package.current.yaml`](./identity-active-package.current.yaml) → [`pkg-000042-20260704-epic-ids-12-sec-06-jwks-es256-hardening.yaml`](./identity-active-packages/pkg-000042-20260704-epic-ids-12-sec-06-jwks-es256-hardening.yaml) (SEC-06, 🟢 Done, immutable after wave)
- **Archival (prev):** [`pkg-000041-20260628-epic-ids-10-pv-10-file-sms-sink-dev.yaml`](./identity-active-packages/pkg-000041-20260628-epic-ids-10-pv-10-file-sms-sink-dev.yaml) (7 tasks PV-10, 🟢 Done, immutable after wave)
- **Archival (prev):** [`pkg-000040-20260626-epic-ids-13-onb-01-lazy-phone-gate-contract.yaml`](./identity-active-packages/pkg-000040-20260626-epic-ids-13-onb-01-lazy-phone-gate-contract.yaml) (5 tasks ONB-01, 🟢 Done, immutable after wave)
- **Archival (prev):** [`pkg-000039-20260626-epic-ids-10-pv-09-durable-phone-persistence.yaml`](./identity-active-packages/pkg-000039-20260626-epic-ids-10-pv-09-durable-phone-persistence.yaml) (7 tasks PV-09, 🟢 Done, immutable after wave)
- **Archival (prev):** [`pkg-000038-20260626-epic-ids-12-sec-03-jwt-validation-hardening.yaml`](./identity-active-packages/pkg-000038-20260626-epic-ids-12-sec-03-jwt-validation-hardening.yaml) (6 tasks SEC-03, 🟢 Done, immutable after wave)
- **Archival (prev):** [`pkg-000037-20260626-epic-ids-12-sec-02-audit-ip-ua-hashing.yaml`](./identity-active-packages/pkg-000037-20260626-epic-ids-12-sec-02-audit-ip-ua-hashing.yaml) (6 tasks SEC-02, 🟢 Done, immutable after wave)
- **Archival (prev):** [`pkg-000036-20260626-epic-ids-12-sec-01b-phone-request-http-rate-limit.yaml`](./identity-active-packages/pkg-000036-20260626-epic-ids-12-sec-01b-phone-request-http-rate-limit.yaml) (6 tasks SEC-01b, 🟢 Done, immutable after wave)
- **Archival (prev):** [`pkg-000035-20260626-epic-ids-12-sec-01-rate-limiting.yaml`](./identity-active-packages/pkg-000035-20260626-epic-ids-12-sec-01-rate-limiting.yaml) (7 tasks SEC-01 + audit t08–t09, 🟢 Done, immutable after wave)
- **Archival (prev):** [`pkg-000034-20260624-epic-ids-11-oauth-04-verify-gate-and-verification-required.yaml`](./identity-active-packages/pkg-000034-20260624-epic-ids-11-oauth-04-verify-gate-and-verification-required.yaml) (7 tasks OAUTH-04, 🟢 Done, immutable after wave)
- **Archival (prev):** [`pkg-000033-20260624-epic-ids-11-oauth-03-persistent-token-store-supabase.yaml`](./identity-active-packages/pkg-000033-20260624-epic-ids-11-oauth-03-persistent-token-store-supabase.yaml) (7 tasks OAUTH-03, 🟢 Done, immutable after wave)
- **Archival (prev):** [`pkg-000030-20260624-epic-ids-11-oauth-02-introspection-and-service-token.yaml`](./identity-active-packages/pkg-000030-20260624-epic-ids-11-oauth-02-introspection-and-service-token.yaml) (6 tasks OAUTH-02, 🟢 Done, immutable after wave close)
- **Archival (prev):** [`pkg-000029-20260624-epic-ids-11-oauth-01-oauth-server-endpoints.yaml`](./identity-active-packages/pkg-000029-20260624-epic-ids-11-oauth-01-oauth-server-endpoints.yaml) (7 tasks OAUTH-01, 🟢 Done, immutable after wave close)
- **Archival (prev):** [`pkg-000028-20260611-epic-ids-10-pv-07-telnyx-delivery-webhook.yaml`](./identity-active-packages/pkg-000028-20260611-epic-ids-10-pv-07-telnyx-delivery-webhook.yaml) (6 tasks PV-07, 🟢 Done, immutable after wave close)
- **Archival (prev):** [`pkg-000027-20260611-epic-ids-10-pv-06-telnyx-sms-sender.yaml`](./identity-active-packages/pkg-000027-20260611-epic-ids-10-pv-06-telnyx-sms-sender.yaml) (6 tasks PV-06, 🟢 Done, immutable after wave close)
- **Archival (prev):** [`pkg-000026-20260611-epic-ids-10-pv-05-verification-flow-api.yaml`](./identity-active-packages/pkg-000026-20260611-epic-ids-10-pv-05-verification-flow-api.yaml) (6 tasks PV-05, 🟢 Done, immutable after wave close)
- **Archival (prev):** [`pkg-000025-20260611-epic-ids-10-pv-04-profile-flag-migration.yaml`](./identity-active-packages/pkg-000025-20260611-epic-ids-10-pv-04-profile-flag-migration.yaml) (6 tasks PV-04, 🟢 Done, immutable after wave close)
- **Archival (prev):** [`pkg-000024-20260611-epic-ids-10-pv-03-otp-engine-session.yaml`](./identity-active-packages/pkg-000024-20260611-epic-ids-10-pv-03-otp-engine-session.yaml) (6 tasks PV-03, 🟢 Done, immutable after wave close)
- **Archival (prev):** [`pkg-000023-20260611-epic-ids-10-pv-02-provider-owned-config.yaml`](./identity-active-packages/pkg-000023-20260611-epic-ids-10-pv-02-provider-owned-config.yaml) (6 tasks PV-02, 🟢 Done, immutable after wave close)
- **Archival (prev):** [`pkg-000022-20260611-epic-ids-10-pv-01-phone-provider-backbone.yaml`](./identity-active-packages/pkg-000022-20260611-epic-ids-10-pv-01-phone-provider-backbone.yaml) (6 tasks PV-01, 🟢 Done, immutable after wave close)
- **Archival (prev):** [`pkg-000021-20260611-epic-ids-09-eid-08-session-secret-box.yaml`](./identity-active-packages/pkg-000021-20260611-epic-ids-09-eid-08-session-secret-box.yaml) (5 tasks EID-08, 🟢 Done, immutable after wave close)
- **Archival (prev):** [`pkg-000020-20260610-epic-ids-09-eid-07-oidc-toolkit.yaml`](./identity-active-packages/pkg-000020-20260610-epic-ids-09-eid-07-oidc-toolkit.yaml) (6 tasks EID-07, 🟢 Done, immutable after wave close)
- **Archival (prev):** [`pkg-000019-20260609-epic-ids-09-eid-06-browser-callback-redirect.yaml`](./identity-active-packages/pkg-000019-20260609-epic-ids-09-eid-06-browser-callback-redirect.yaml) (6 tasks EID-06 + audit t07, 🟢 Done, immutable after wave close)
- **Archival (prev):** [`pkg-000018-20260608-epic-ids-09-eid-05-canonical-provider-contract.yaml`](./identity-active-packages/pkg-000018-20260608-epic-ids-09-eid-05-canonical-provider-contract.yaml) (5 tasks EID-05 + audit t06–t07, 🟢 Done, immutable after wave close)
- **Archival (prev):** [`pkg-000017-20260608-epic-ids-09-eid-04-provider-owned-config.yaml`](./identity-active-packages/pkg-000017-20260608-epic-ids-09-eid-04-provider-owned-config.yaml) (6 tasks EID-04 + audit t07–t08, 🟢 Done, immutable after wave close)
- **Archival (prev):** [`pkg-000016-20260607-epic-ids-09-eid-03-provider-plugin-backbone.yaml`](./identity-active-packages/pkg-000016-20260607-epic-ids-09-eid-03-provider-plugin-backbone.yaml) (6 tasks EID-03, 🟢 Done, immutable after wave close)
- **Archival (prev):** [`pkg-000015-20260606-epic-ids-09-eid-verification-flow.yaml`](./identity-active-packages/pkg-000015-20260606-epic-ids-09-eid-verification-flow.yaml) (6 tasks EID-01 + t07 audit, 🟢 Done, immutable)
- **Archival (prev):** [`pkg-000014-20260605-epic-ids-08-cleanup-03-doc-drift.yaml`](./identity-active-packages/pkg-000014-20260605-epic-ids-08-cleanup-03-doc-drift.yaml) (6 tasks CLEANUP-03, 🟢 Done, immutable after wave close)
- **Archival (prev):** [`pkg-000013-20260602-epic-ids-08-cleanup-02-placeholders-hardening.yaml`](./identity-active-packages/pkg-000013-20260602-epic-ids-08-cleanup-02-placeholders-hardening.yaml) (7 tasks CLEANUP-02, 🟢 Done, immutable after wave close)
- **Archival (prev):** [`pkg-000012-20260605-epic-ids-08-cleanup-01-audit-gaps.yaml`](./identity-active-packages/pkg-000012-20260605-epic-ids-08-cleanup-01-audit-gaps.yaml) (4 audit tasks 🟢 Done, immutable)
- **Archival (prev):** [`pkg-000011-20260605-epic-ids-08-cleanup-remove-stories.yaml`](./identity-active-packages/pkg-000011-20260605-epic-ids-08-cleanup-remove-stories.yaml) (7 tasks CLEANUP-01, 🟢 Done, immutable)
- **Archival (prev):** [`pkg-000010-20260605-epic-ids-07-authcore-01-audit-gaps.yaml`](./identity-active-packages/pkg-000010-20260605-epic-ids-07-authcore-01-audit-gaps.yaml) (6 audit tasks 🟢 Done, immutable)
- **Archival (prev):** [`pkg-000009-20260604-epic-ids-07-auth-core-profile-me.yaml`](./identity-active-packages/pkg-000009-20260604-epic-ids-07-auth-core-profile-me.yaml) (6 tasks AUTHCORE-01, Done, immutable)
- **Archival (prev):** [`pkg-000008-20260602-epic-ids-06-testing-architecture.yaml`](./identity-active-packages/pkg-000008-20260602-epic-ids-06-testing-architecture.yaml) (15 tasks, 5 stories, Done)
- **Archival (prev):** [`pkg-000006-20260530-epic-ids-05-supabase-persistence.yaml`](./identity-active-packages/pkg-000006-20260530-epic-ids-05-supabase-persistence.yaml) (EPIC-IDS-05 Done stories)
- **Archival (prev):** [`pkg-000005-20260529-epic-ids-04-soa-service-factory.yaml`](./identity-active-packages/pkg-000005-20260529-epic-ids-04-soa-service-factory.yaml) (EPIC-IDS-04 Done stories)
- **Archival (prev):** [`pkg-000004-20260529-epic-ids-03-dependency-injection.yaml`](./identity-active-packages/pkg-000004-20260529-epic-ids-03-dependency-injection.yaml) (EPIC-IDS-03 Done)
- **Archival:** [`pkg-000003-20260528-epic-ids-02-fastapi-transport.yaml`](./identity-active-packages/pkg-000003-20260528-epic-ids-02-fastapi-transport.yaml) (EPIC-IDS-02 Done)
- **Указатель:** [`identity-active-package.current.yaml`](./identity-active-package.current.yaml)
- **Verify:** `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify`
- **Decompose marker:** [`pkg-000002-20260528-epic-ids-02-fastapi-transport-pending.yaml`](./identity-active-packages/pkg-000002-20260528-epic-ids-02-fastapi-transport-pending.yaml) (`input_kind=epic_decompose_pending`, archival transition step)
- **Gap wave (override-only):** … · **audit SEC-06 2026-07-04:** **`run_mode=epic_ids_12_sec_06_audit_2026_07_04`** — F1–F2 🟢 · **audit PV-10 2026-06-28:** **`run_mode=epic_ids_10_pv_10_audit_2026_06_28`** — F1 🟢 · **audit SEC-01 2026-06-26:** **`run_mode=epic_ids_12_sec_01_audit_2026_06_26`** — F1–F2 🟢 · **audit OAUTH-02 2026-06-24:** **`run_mode=epic_ids_11_oauth_02_audit_2026_06_24`** — F2–F4 🟢 · **audit OAUTH-01 2026-06-24:** **`run_mode=epic_ids_11_oauth_01_audit_2026_06_24`** — F1–F3 🟢 · **audit PV-06 2026-06-11:** **`run_mode=epic_ids_10_pv_06_audit_2026_06_11`** — F1–F3 🟢. Default YAML SSOT: **`pkg-000042`** ([`identity-active-package.current.yaml`](./identity-active-package.current.yaml)).
- **Builder resolve (обязательно перед batch-run):** [identity-operator-contract.md](../../../docs/methodology/Zeya888-builder-queue/contracts/identity-operator-contract.md) — index + active pkg + `--verify`; эпик без task queue ниже → P1 decompose.

## Epic registry (EPIC-IDS-*)

> Файл эпика без task queue в этом индексе = **не декомпозирован** → `@.cursor/commands/bullrun-epic-decompose.md`, не P3 Execute.

| Epic | Epic file | pkg / queue | Decompose |
|------|-----------|-------------|-----------|
| EPIC-IDS-01 | [EPIC-IDS-01-scaffold-config-launch.md](./epics/EPIC-IDS-01-scaffold-config-launch/EPIC-IDS-01-scaffold-config-launch.md) | pkg-000001 · [task queue](#task-queue-epic-ids-01) | 🟢 Done |
| EPIC-IDS-02 | [EPIC-IDS-02-fastapi-transport.md](./epics/EPIC-IDS-02-fastapi-transport/EPIC-IDS-02-fastapi-transport.md) | pkg-000003 · [task queue](#task-queue-epic-ids-02) | 🟢 Done |
| EPIC-IDS-03 | [EPIC-IDS-03-dependency-injection.md](./epics/EPIC-IDS-03-dependency-injection/EPIC-IDS-03-dependency-injection.md) | pkg-000004 · [task queue](#task-queue-epic-ids-03) | 🟢 Done |
| EPIC-IDS-04 | [EPIC-IDS-04-soa-service-factory.md](./epics/EPIC-IDS-04-soa-service-factory/EPIC-IDS-04-soa-service-factory.md) | pkg-000005 · [task queue](#task-queue-epic-ids-04) | 🟢 Done (override RG-1/RG-2 ⚪) |
| EPIC-IDS-05 | [EPIC-IDS-05-supabase-persistence.md](./epics/EPIC-IDS-05-supabase-persistence/EPIC-IDS-05-supabase-persistence.md) | pkg-000006 · [task queue](#task-queue-epic-ids-05) | 🟢 Done (re-audit 2026-06-02: 5/5 gaps closed) |
| EPIC-IDS-06 | [EPIC-IDS-06-testing-architecture.md](./epics/EPIC-IDS-06-testing-architecture/EPIC-IDS-06-testing-architecture.md) | pkg-000008 · [task queue](#task-queue-epic-ids-06) | 🟢 Done — 5/5 stories (audit 2026-06-02: 1 MEDIUM + 5 LOW, [report](../analysis/epic-ids-06-audit-2026-06-02.md)) |
| EPIC-IDS-07 | [EPIC-IDS-07-auth-core.md](./epics/EPIC-IDS-07-auth-core/EPIC-IDS-07-auth-core.md) | pkg-000009 + pkg-000010 + **pkg-000044** · [task queue](#task-queue-epic-ids-07) | 🟡 In Progress — AUTHCORE-01+02 🟢; epic gate pending |
| EPIC-IDS-08 | [EPIC-IDS-08-cleanup.md](./epics/EPIC-IDS-08-cleanup/EPIC-IDS-08-cleanup.md) | pkg-000011 + pkg-000012 + pkg-000013 + pkg-000014 · [task queue](#task-queue-epic-ids-08) | 🟡 In Progress — CLEANUP-01/02/03 🟢; epic gate pending |
| EPIC-IDS-09 | [EPIC-IDS-09-eid-verification.md](./epics/EPIC-IDS-09-eid-verification/EPIC-IDS-09-eid-verification.md) | pkg-000021 · [task queue](#task-queue-epic-ids-09) | 🟡 In Progress — EID-01 🟢; EID-03 🟢; EID-04 🟢; EID-05 🟢; EID-06 🟢; EID-07 🟢; EID-08 🟢 |
| EPIC-IDS-10 | [EPIC-IDS-10-phone-verification.md](./epics/EPIC-IDS-10-phone-verification/EPIC-IDS-10-phone-verification.md) | pkg-000041 · [task queue](#task-queue-epic-ids-10) | 🟡 In Progress — PV-01 🟢; PV-02 🟢; PV-03 🟢; PV-04 🟢; PV-05 🟢; PV-06 🟢; PV-07 🟢; PV-09 🟢; PV-10 🟢 |
| EPIC-IDS-11 | [EPIC-IDS-11-oauth-server.md](./epics/EPIC-IDS-11-oauth-server/EPIC-IDS-11-oauth-server.md) | pkg-000034 · [task queue](#task-queue-epic-ids-11) | 🟡 In Progress — OAUTH-01 🟢; OAUTH-02 🟢; OAUTH-03 🟢; OAUTH-04 🟢 |
| EPIC-IDS-12 | [EPIC-IDS-12-security-hardening.md](./epics/EPIC-IDS-12-security-hardening/EPIC-IDS-12-security-hardening.md) | pkg-000043 · [task queue](#task-queue-epic-ids-12) | 🟡 In Progress — SEC-01 🟢; SEC-01b 🟢; SEC-02 🟢; SEC-03 🟢; SEC-04 🟢; SEC-06 🟢 |
| EPIC-IDS-13 | [EPIC-IDS-13-onboarding.md](./epics/EPIC-IDS-13-onboarding/EPIC-IDS-13-onboarding.md) | pkg-000040 + **pkg-000045** · [task queue](#task-queue-epic-ids-13) | 🟡 In Progress — DOC-ONB-01 🟢; ONB-01 🟢 (pkg-000045) |

**Рекомендуемый next (default):** CLEANUP-04; epic gates EPIC-IDS-07/08/12; DOC-ONB-02…04 (spa/product). (ONB-01 🟢 pkg-000045 + F2 override 🟢 + F1 spa 🟢; AUTHCORE-02 🟢 pkg-000044; SEC-04 🟢.)

## Gap queue (override-only, audit EPIC-IDS-01 2026-05-28)

| Finding | Story | Gap task README | Status |
|------|-------|-------------|--------|
| F1-1 | STORY-IDS-01-01 | [t04 security init](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-01-init-package-and-dependencies/task-ids-01-01-t04-audit-f1-1-security-init/README.md) | 🟢 Done |
| F1-2 | STORY-IDS-01-01 | [t05 story1 AC wording](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-01-init-package-and-dependencies/task-ids-01-01-t05-audit-f1-2-story1-ac-collect-wording/README.md) | 🟢 Done |
| F1-3 | STORY-IDS-01-01 | [t06 hashing doc alignment](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-01-init-package-and-dependencies/task-ids-01-01-t06-audit-f1-3-hashing-placeholder-doc-alignment/README.md) | 🟢 Done |
| F1-4 | STORY-IDS-01-01 | [t07 dev deps doc alignment](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-01-init-package-and-dependencies/task-ids-01-01-t07-audit-f1-4-dev-httpx-doc-alignment/README.md) | 🟢 Done |
| F1-5 | STORY-IDS-01-01 | [t08 pyright alignment](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-01-init-package-and-dependencies/task-ids-01-01-t08-audit-f1-5-pyright-config-alignment/README.md) | 🟢 Done |
| F2-1 | STORY-IDS-01-02 | [t04 pilot API_BASE_URL fail-fast](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-02-appconfig/task-ids-01-02-t04-audit-f2-1-pilot-api-base-url-fail-fast/README.md) | 🟢 Done |
| F2-2 | STORY-IDS-01-02 | [t05 db_enabled tests](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-02-appconfig/task-ids-01-02-t05-audit-f2-2-db-enabled-test-coverage/README.md) | 🟢 Done |
| F2-3 | STORY-IDS-01-02 | [t06 pilot oauth secret test](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-02-appconfig/task-ids-01-02-t06-audit-f2-3-pilot-oauth-secret-isolated-test/README.md) | 🟢 Done |
| F2-4 | STORY-IDS-01-02 | [t07 eideasy methods order](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-02-appconfig/task-ids-01-02-t07-audit-f2-4-eideasy-methods-default-order-alignment/README.md) | 🟢 Done |
| F3-1 | STORY-IDS-01-03 | [t04 parse_dotenv_file test](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-03-custom-dotenv-parser/task-ids-01-03-t04-audit-f3-1-parse-dotenv-file-test/README.md) | 🟢 Done |
| F4-1 | STORY-IDS-01-04 | [t04 test-live flags cleanup](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-04-makefile-railway-env-example/task-ids-01-04-t04-audit-f4-1-test-live-flags-cleanup/README.md) | 🟢 Done |
| F4-2 | STORY-IDS-01-04 | [t05 dotenv secret section](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-04-makefile-railway-env-example/task-ids-01-04-t05-audit-f4-2-dotenv-secret-section-placement/README.md) | 🟢 Done |

## Gap queue (override-only, audit EPIC-IDS-02 2026-05-28)

| Finding | Story | Gap task README | Status |
|---------|-------|-----------------|--------|
| A-1 | STORY-IDS-02-04 | [t04 cors headers test](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-04-fastapi-app-lifespan-cors-middleware/task-ids-02-04-t04-audit-a1-cors-response-headers-test/README.md) | 🟢 Done |
| A-2 | STORY-IDS-02-05 | [t04 ready supabase 503 test](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-05-routes-contract-health-ready-identity-stubs/task-ids-02-05-t04-audit-a2-ready-supabase-503-test/README.md) | 🟢 Done |

## Gap queue (override-only, audit EPIC-IDS-03 2026-05-28)

> Отчёт: [`docs/analysis/epic-ids-03-audit-2026-05-28.md`](../analysis/epic-ids-03-audit-2026-05-28.md)

| Finding | Story | Gap task README | Status |
|---------|-------|-----------------|--------|
| DI-1 | STORY-IDS-03-02 | [t04 lifespan logging assertion](./epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-02-build-api-dependencies-singleton-lifespan/task-ids-03-02-t04-audit-di-1-lifespan-logging-assertion/README.md) | 🟢 Done |
| DI-2 | STORY-IDS-03-02 | [t05 create_app dual-config note](./epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-02-build-api-dependencies-singleton-lifespan/task-ids-03-02-t05-audit-di-2-create-app-dual-config-note/README.md) | 🟢 Done |
| DI-3 | STORY-IDS-03-03 | [t03 unreachable block lint](./epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-03-epic-ids-04-extension-hook-contract/task-ids-03-03-t03-audit-di-3-unreachable-block-lint/README.md) | 🟢 Done |
| DI-4 | STORY-IDS-03-03 | [t04 optional fields test cleanup](./epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-03-epic-ids-04-extension-hook-contract/task-ids-03-03-t04-audit-di-4-optional-fields-test-cleanup/README.md) | 🟢 Done |

## Gap queue (override-only, audit EPIC-IDS-04 2026-05-30)

> Отчёт: [`epic-ids-04-audit-2026-05-30.md`](./epics/EPIC-IDS-04-soa-service-factory/epic-ids-04-audit-2026-05-30.md)

| Finding | Story | Gap task README | Status |
|---------|-------|-----------------|--------|
| RG-1 | STORY-IDS-04-06 | [t04 epic hook test cleanup](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-06-provide-factory-di-integration/task-ids-04-06-t04-audit-rg-1-epic-hook-test-cleanup/README.md) | ⚪ Todo |
| RG-2 | STORY-IDS-04-06 | [t05 zero arg assertion](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-06-provide-factory-di-integration/task-ids-04-06-t05-audit-rg-2-zero-arg-assertion/README.md) | ⚪ Todo |
| S5-1 | STORY-IDS-04-05 | [t04 bearer protocol ssot](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-05-supabase-jwt-bearer-auth/task-ids-04-05-t04-audit-s5-1-bearer-protocol-ssot/README.md) | 🟢 Done |
| S2-1 | STORY-IDS-04-02 | [t04 client secret doc](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-02-inmemory-repositories/task-ids-04-02-t04-audit-s2-1-client-secret-doc/README.md) | 🟢 Done |
| S1-2 | STORY-IDS-04-01 | [t04 mutable collection fields](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-01-domain-protocols-contracts/task-ids-04-01-t04-audit-s1-2-mutable-collection-fields/README.md) | 🟢 Done |
| S5-2 | STORY-IDS-04-05 | [t05 redundant iss check](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-05-supabase-jwt-bearer-auth/task-ids-04-05-t05-audit-s5-2-redundant-iss-check/README.md) | 🟢 Done |
| S6-1 | STORY-IDS-04-05 | [t06 me integration test hardening](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-05-supabase-jwt-bearer-auth/task-ids-04-05-t06-audit-s6-1-me-integration-test-hardening/README.md) | 🟢 Done |

## Gap queue (override-only, audit EPIC-IDS-05 2026-05-31)

> Отчёт: [`audit-report-2026-05-31.md`](./epics/EPIC-IDS-05-supabase-persistence/audit-report-2026-05-31.md)  
> **activation:** `run_mode=epic_ids_05_audit_2026_05_31` · [`ID_builder.plan.md`](../../../.cursor/plans/ID_builder.plan.md)

| Gap ID | Story | Task README | Status | Wave |
|--------|-------|-------------|--------|------|
| RG-1 | — | — (superseded: STORY-IDS-05-06 t02) | superseded (Story 06) | — |
| S2-1 | STORY-IDS-05-02 | [t04 oauth store env doc](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-02-supabase-repositories-identity-set/task-ids-05-02-t04-audit-s2-1-oauth-store-env-doc/README.md) | ⚪ Todo | override epic_ids_05_audit_2026_05_31 |
| S3-2 | STORY-IDS-05-03 | [t05 health db request timeout](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-03-five-level-healthcheck/task-ids-05-03-t05-audit-s3-2-health-db-request-timeout/README.md) | ⚪ Todo | override epic_ids_05_audit_2026_05_31 |
| S3-1 | STORY-IDS-05-03 | [t04 dual health db comment](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-03-five-level-healthcheck/task-ids-05-03-t04-audit-s3-1-dual-health-db-comment/README.md) | ⚪ Todo | override epic_ids_05_audit_2026_05_31 |
| S2-2 | STORY-IDS-05-02 | [t05 mark consumed started guard](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-02-supabase-repositories-identity-set/task-ids-05-02-t05-audit-s2-2-mark-consumed-started-guard/README.md) | ⚪ Todo | override epic_ids_05_audit_2026_05_31 |
| S1-1 | STORY-IDS-05-01 | [t03 empty service role key test](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-01-supabase-database-http-client/task-ids-05-01-t03-audit-s1-1-empty-service-role-key-test/README.md) | ⚪ Todo | override epic_ids_05_audit_2026_05_31 |

## Gap queue (override-only, re-audit EPIC-IDS-05 2026-06-02)

> Отчёт: [`re-audit-report-2026-06-02.md`](./epics/EPIC-IDS-05-supabase-persistence/re-audit-report-2026-06-02.md)  
> **activation:** `run_mode=epic_ids_05_reaudit_2026_06_02` · [`ID_builder.plan.md`](../../../.cursor/plans/ID_builder.plan.md) · **pkg (archival):** [`pkg-000007-20260602-epic-ids-05-reaudit-gaps.yaml`](./identity-active-packages/pkg-000007-20260602-epic-ids-05-reaudit-gaps.yaml)

| Gap ID | Story | Task README | Status | Wave |
|--------|-------|-------------|--------|------|
| RG-1 | — | — (superseded: STORY-IDS-05-06 t02) | superseded (Story 06) | — |
| S2-1 | STORY-IDS-05-02 | [t04 oauth store env doc](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-02-supabase-repositories-identity-set/task-ids-05-02-t04-audit-s2-1-oauth-store-env-doc/README.md) | 🟢 Done | override epic_ids_05_reaudit_2026_06_02 |
| S3-1 | STORY-IDS-05-03 | [t04 dual health db comment](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-03-five-level-healthcheck/task-ids-05-03-t04-audit-s3-1-dual-health-db-comment/README.md) | 🟢 Done | override epic_ids_05_reaudit_2026_06_02 |
| S1-1 | STORY-IDS-05-01 | [t03 empty service role key test](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-01-supabase-database-http-client/task-ids-05-01-t03-audit-s1-1-empty-service-role-key-test/README.md) | 🟢 Done | override epic_ids_05_reaudit_2026_06_02 |
| S2-2 | STORY-IDS-05-02 | [t05 mark consumed started guard](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-02-supabase-repositories-identity-set/task-ids-05-02-t05-audit-s2-2-mark-consumed-started-guard/README.md) | 🟢 Done | override epic_ids_05_reaudit_2026_06_02 |
| S3-2 | STORY-IDS-05-03 | [t05 health db request timeout](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-03-five-level-healthcheck/task-ids-05-03-t05-audit-s3-2-health-db-request-timeout/README.md) | 🟢 Done | override epic_ids_05_reaudit_2026_06_02 |

## Gap queue (override-only, audit EPIC-IDS-06 2026-06-02)

> Отчёт: [`epic-ids-06-audit-2026-06-02.md`](../analysis/epic-ids-06-audit-2026-06-02.md)
> **activation:** `run_mode=epic_ids_06_audit_2026_06_02` · [`ID_builder.plan.md`](../../../.cursor/plans/ID_builder.plan.md) · **pkg (default, unchanged):** [`pkg-000008-20260602-epic-ids-06-testing-architecture.yaml`](./identity-active-packages/pkg-000008-20260602-epic-ids-06-testing-architecture.yaml)
> **Контекст:** 5/5 stories 🟢 Done (193 pytest offline). Findings — кросс-срезовые (изоляция / doc↔code / структура), не «задача не сделана». Блокирующих нет.

| Gap ID | Severity | Суть | Файл:строка | Task README | Status |
|--------|----------|------|-------------|-------------|--------|
| F1 | MEDIUM | import-time `provide_app_config()` не изолирован autouse-фикстурой; epic §8 verify cmd#3 крэшит сбор | `asgi_app.py:346-347` | [t03 audit f1 asgi import time](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-01-conftest-autouse-fixtures/task-ids-06-01-t03-audit-f1-asgi-import-time-config-isolation/README.md) | 🟢 Done |
| F2 | LOW | AC S5 заявляет исключение smoke через `testpaths`; реально `collect_ignore` | `conftest.py:9` | [t03 audit f2 smoke ac doc](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-05-live-server-smoke/task-ids-06-05-t03-audit-f2-smoke-exclusion-ac-doc-align/README.md) | 🟢 Done |
| F3 | LOW | `tests/integration/__init__.py` + `tests/smoke/__init__.py` из §5 отсутствуют | epic §5 | [t04 audit f3 init files](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-03-live-supabase-integration/task-ids-06-03-t04-audit-f3-tests-package-init-files/README.md) | 🟢 Done |
| F4 | LOW | маркер `smoke` объявлен дважды (pyproject + smoke/conftest) | `pyproject.toml:38` | [t04 audit f4 smoke marker](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-05-live-server-smoke/task-ids-06-05-t04-audit-f4-smoke-marker-ssot/README.md) | 🟢 Done |
| F5 | LOW | `asyncio_mode=auto` + `pytest-asyncio` + паттерн ASGITransport не используются (0 async-тестов) | `pyproject.toml:30,35` | [t06 audit f5 asyncio config](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-02-http-bootstrap-di-smoke-tests/task-ids-06-02-t06-audit-f5-pytest-asyncio-config-align/README.md) | 🟢 Done |
| F6 | LOW | битая ссылка на файл эпика в индексе | `bullrun-launch-index.md:36` | — (index-only, done) | 🟢 Done |

## Gap queue (override-only, audit EPIC-IDS-07 AUTHCORE-01 2026-06-05)

> Отчёт: [`epic-ids-07-authcore-01-audit-2026-06-05.md`](../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md)
> **activation:** `pkg-000010` (active via [`identity-active-package.current.yaml`](./identity-active-package.current.yaml))
> **run_mode:** `epic_ids_07_authcore_01_audit_2026_06_05`
> **Контекст:** STORY-IDS-AUTHCORE-01 🟢 Done; post-audit F1–F6 закрыты P3 2026-06-05 (200 pytest offline).

| Gap ID | Severity | Суть | Файл:строка | Task README | Status |
|--------|----------|------|-------------|-------------|--------|
| F1 | MEDIUM | offline 1 failed: тест не ловит `ConfigError` при cwd `.env` merge | `test_asgi_import_config_isolation.py:28-41` | [t07 audit f1 dotenv cwd test isolation](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t07-audit-f1-dotenv-cwd-test-isolation/README.md) | 🟢 Done |
| F2 | MEDIUM | backlog-story `⚪ Todo`, stub 501, alias эпика | `backlog-stories/...:5-6,24` | [t08 audit f2 backlog story sync](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t08-audit-f2-backlog-story-status-sync/README.md) | 🟢 Done |
| F3 | LOW | `handle_me_stub` осиротел | `handlers.py:41-52` | [t09 audit f3 remove handle me stub](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t09-audit-f3-remove-handle-me-stub/README.md) | 🟢 Done |
| F4 | LOW | «базовые права» — только `role`, doc не зафиксирован | `me_response.py:17-34` | [t10 audit f4 basic rights doc align](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t10-audit-f4-basic-rights-doc-align/README.md) | 🟢 Done |
| F5 | MEDIUM | индекс «199 passed» / epic doc stub 501 | `bullrun-launch-index.md:11` | [t11 audit f5 bullrun index sync](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t11-audit-f5-bullrun-index-factual-sync/README.md) | 🟢 Done |
| F6 | MEDIUM | нет `.gitignore`; `.env` с service_role untracked | корень сервиса | [t12 audit f6 gitignore env](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t12-audit-f6-gitignore-env/README.md) | 🟢 Done |

## Gap queue (override-only, audit EPIC-IDS-07 AUTHCORE-02 2026-07-24)

> Отчёт: [`identity-authcore-02-code-audit-2026-07-24.md`](../analysis/identity-authcore-02-code-audit-2026-07-24.md)
> **activation:** `run_mode=epic_ids_07_authcore_02_audit_2026_07_24` (P6 Done 2026-07-24T14:05:39Z; default pkg-000044 unchanged)
> **Контекст:** STORY-IDS-AUTHCORE-02 🟢 Done — подтверждено кодом (4/4 tasks, 405 pytest offline, миграции нет). Регрессий нет; статусы индекса факт-верны. Override scope = **G3** (docs-only t05) — 🟢 closed. **G2 🟢 closed** отдельно 2026-07-24 (SPA cabinet-контракт синхронизирован под поставку `created_at`+`account_status`). **G1 🟢 closed** (ONB-01 pkg-000045); **G4** ignored.

| Gap ID | Severity | Суть | Файл:строка | Task README / disposition | Status |
|--------|----------|------|-------------|---------------------------|--------|
| G3 | LOW | `created_at`-семантика (=первая верификация, не регистрация) не вынесена в consumer-facing api-reference | `openapi.yaml:87`, `API_REFERENCE.md:83` | [t05 audit g3 created_at semantics docs](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-02-me-account-fields/task-ids-07-02-t05-audit-g3-created-at-semantics-docs/README.md) | 🟢 Done |
| G1 | MEDIUM | Umbrella CAB-02 закрыт 2/3: `email` в `/me` отсутствует | `me_response.py` (нет `email`) | out of override → [ONB-01](./backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md) | 🟢 Done (ONB-01 pkg-000045) |
| G2 | LOW | Cross-repo drift: SPA §0/§4 placeholder | `spa-app/.../STORY-SPA-CAB-api-requirements.md:7,31,40-41,100`; `STORY-SPA-CAB-02:21` | spa-doc синхронизирован 2026-07-24: `created_at`+`account_status` ✅ live, `email`→ONB-01 | 🟢 Done (spa) |
| G4 | LOW | Traceability: backlog T04 ≠ pipeline t04 | backlog story vs bullrun | ignored (working-doc filter P5) | — ignored |

## Gap queue (override-only, audit EPIC-IDS-13 ONB-01 2026-07-24)

> Отчёт: [`identity-onb-01-code-audit-2026-07-24.md`](../analysis/identity-onb-01-code-audit-2026-07-24.md)
> **activation:** `run_mode=epic_ids_13_onb_01_audit_2026_07_24` (P6 Done 2026-07-24T20:44:05Z; default pkg-000045 unchanged)
> **Контекст:** STORY-IDS-ONB-01 🟢 Done — подтверждено кодом (4/4 pkg tasks, 406 pytest offline, миграций нет). Override scope = **F2** (docs-only t05) — 🟢 closed. **F1 🟢 closed** (spa-doc 2026-07-24); **F3** ignored (working-doc). CAB-02 identity = 3/3.

| Gap ID | Severity | Суть | Файл:строка | Task README / disposition | Status |
|--------|----------|------|-------------|---------------------------|--------|
| F2 | LOW | `email_verified` семантика неполна для OAuth/`email=null` потребителя | `me_response.py:22`, `security.py:64`; api-reference | [t05 audit f2 email_verified oauth semantics docs](./epics/EPIC-IDS-13-onboarding/stories/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm/task-ids-13-02-t05-audit-f2-email-verified-oauth-semantics-docs/README.md) | 🟢 Done |
| F1 | LOW | Обратный SPA drift: `email` live, cabinet-доки всё ещё «ждёт ONB-01» | `spa-app/.../STORY-SPA-CAB-api-requirements.md`; `STORY-SPA-CAB-02` | spa-doc синхронизирован 2026-07-24: `email`+`email_verified` ✅ live (ONB-01 pkg-000045) | 🟢 Done (spa) |
| F3 | LOW | Traceability: backlog T01–T03 ≠ pipeline t04 | backlog story vs bullrun | ignored (working-doc filter P5) | — ignored |

## Gap queue (override-only, audit EPIC-IDS-08 CLEANUP-01 2026-06-05)

> Отчёт: [`epic-ids-08-cleanup-01-audit-2026-06-05.md`](../analysis/epic-ids-08-cleanup-01-audit-2026-06-05.md)
> **activation:** [`pkg-000012`](./identity-active-packages/pkg-000012-20260605-epic-ids-08-cleanup-01-audit-gaps.yaml) (active via [`identity-active-package.current.yaml`](./identity-active-package.current.yaml))
> **Контекст:** STORY-IDS-CLEANUP-01 🟢 Done; post-audit F1–F4 🟢 Done P3 2026-06-05 (200 pytest offline).

| Gap ID | Severity | Суть | Файл:строка | Task README | Status |
|--------|----------|------|-------------|-------------|--------|
| F1 | MEDIUM | runbook §3 предписывает story_drafts migration vs DEPRECATED/bootstrap | `runbook/supabase-project-setup.md:62` vs `migrations/...:1-2` | [t08 audit f1 runbook align](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity/task-ids-08-01-t08-audit-f1-runbook-story-drafts-migration-align/README.md) | 🟢 Done |
| F2 | MEDIUM | story_drafts в migration/runbook тестах (AC3 residual) | `test_supabase_runbook_docs.py:17`; `test_supabase_migrations_sql.py:45,87` | [t09 audit f2 migration tests](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity/task-ids-08-01-t09-audit-f2-story-migration-tests-residual/README.md) | 🟢 Done |
| F3 | LOW | пустой каталог `src/core/stories/` после t04 | `src/core/stories/` | [t10 audit f3 empty stories dir](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity/task-ids-08-01-t10-audit-f3-remove-empty-stories-directory/README.md) | 🟢 Done |
| F4 | LOW | backlog-story `⚪ Todo`, устаревшие code refs | `backlog-stories/STORY-IDS-CLEANUP-01...md:6,24-27` | [t11 audit f4 backlog sync](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity/task-ids-08-01-t11-audit-f4-backlog-story-status-sync/README.md) | 🟢 Done |

## Gap queue (override-only, audit EPIC-IDS-08 CLEANUP-02 2026-06-05)

> Отчёт: [`epic-ids-08-cleanup-02-audit-2026-06-05.md`](../analysis/epic-ids-08-cleanup-02-audit-2026-06-05.md)
> **activation:** `run_mode=epic_ids_08_cleanup_02_audit_2026_06_05`
> **Контекст:** STORY-IDS-CLEANUP-02 🟢 Done; pkg-000013 default unchanged ([`identity-active-package.current.yaml`](./identity-active-package.current.yaml)).

| Gap ID | Severity | Суть | Файл:строка | Task README | Status |
|--------|----------|------|-------------|-------------|--------|
| F1 | MEDIUM | `validate_return_url` 0 callers — open-redirect не enforced | [`return_url.py:26`](../../src/core/security/return_url.py); [`handlers.py:65`](../../src/core/api/handlers.py) | [t08 audit f1 return url enforcement](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/task-ids-08-02-t08-audit-f1-return-url-validator-enforcement/README.md) | 🟢 Done |
| F2 | LOW | пустые dirs `core.audit/oauth/profiles` + 03-soa «удалены» неточно | `src/core/{audit,oauth,profiles}/`; [`03-soa-roles.md:64`](../../docs/runtime-docs/03-soa-roles.md) | [t09 audit f2 empty layer dirs doc](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/task-ids-08-02-t09-audit-f2-empty-layer-directories-doc-align/README.md) | 🟢 Done |
| F3 | LOW | `01-api.md` ссылка на удалённый `idempotency.py` | [`01-api.md:50`](../../docs/runtime-docs/01-api.md) | [t10 audit f3 idempotency doc drift](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/task-ids-08-02-t10-audit-f3-idempotency-runtime-doc-drift/README.md) | 🟢 Done |

## Gap queue (override-only, audit EPIC-IDS-08 CLEANUP-03 2026-06-06)

> Отчёт: [`epic-ids-08-cleanup-03-audit-2026-06-06.md`](../analysis/epic-ids-08-cleanup-03-audit-2026-06-06.md)
> **activation:** none
> **Контекст:** STORY-IDS-CLEANUP-03 🟢 Done; pkg-000014 default unchanged ([`identity-active-package.current.yaml`](./identity-active-package.current.yaml)).

| Gap ID | Severity | Суть | Файл:строка | Task README | Status |
|--------|----------|------|-------------|-------------|--------|
| — | — | material gaps отсутствуют | audit §4, §6 | — | n/a |
| O1 | none | backlog Meta без alias «→ EPIC-IDS-08» | [`STORY-IDS-CLEANUP-03-doc-drift.md:5`](./backlog-stories/cleanup/STORY-IDS-CLEANUP-03-doc-drift.md) | — | deferred (no task) |
| O2 | none | дата волны `2026-06-02` vs имя pkg `20260605` | [`bullrun-launch-index.md:11`](./bullrun-launch-index.md) | — | deferred (no task) |

## Gap queue (override-only, audit EPIC-IDS-09 EID-01 2026-06-06)

> Отчёт: [`epic-ids-09-eid-01-audit-2026-06-06.md`](../analysis/epic-ids-09-eid-01-audit-2026-06-06.md)
> **activation:** `run_mode=epic_ids_09_eid_01_audit_2026_06_06`
> **Контекст:** STORY-IDS-EID-01 🟢 Done; pkg-000015 default unchanged ([`identity-active-package.current.yaml`](./identity-active-package.current.yaml)).

| Gap ID | Severity | Суть | Файл:строка | Task README | Status |
|--------|----------|------|-------------|-------------|--------|
| F1 | MEDIUM | backlog doc-stale: Status Todo, stub refs, AC [ ] | [`STORY-IDS-EID-01-eid-verification-flow.md:5-6,24-34`](./backlog-stories/eid/STORY-IDS-EID-01-eid-verification-flow.md) | [t07 audit f1 backlog story status sync](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-01-eid-verification-flow/task-ids-09-01-t07-audit-f1-backlog-story-status-sync/README.md) | 🟢 Done |
| F2 | LOW | пустой `eid_secret` → hash без pepper в demo | [`handlers.py:283-286`](../../src/core/api/handlers.py) | — | deferred (no task) |
| F3 | LOW | нет enum-валидации `return_context`/`requested_action` → потенц. 500 на Supabase CHECK | [`handlers.py:152-157`](../../src/core/api/handlers.py) | — | deferred (no task) |

## Gap queue (override-only, audit EPIC-IDS-09 EID-03 2026-06-08)

> Отчёт: [`epic-ids-09-eid-03-audit-2026-06-08.md`](../analysis/epic-ids-09-eid-03-audit-2026-06-08.md)
> **activation:** `run_mode=epic_ids_09_eid_03_audit_2026_06_08`
> **Контекст:** STORY-IDS-EID-03 🟢 Done; pkg-000016 default unchanged ([`identity-active-package.current.yaml`](./identity-active-package.current.yaml)).

| Gap ID | Severity | Суть | Файл:строка | Task README | Status |
|--------|----------|------|-------------|-------------|--------|
| F1 | MEDIUM | backlog doc-stale: Status Todo, hardcode/KeyError refs, AC [ ] | [`STORY-IDS-EID-03-provider-plugin-backbone.md:6,26-37`](./backlog-stories/eid/STORY-IDS-EID-03-provider-plugin-backbone.md) | [t07 audit f1 backlog story status sync](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-03-provider-plugin-backbone/task-ids-09-03-t07-audit-f1-backlog-story-status-sync/README.md) | ⚪ Todo |
| F2 | LOW | `build_registry` молча пропускает active без descriptor; fail-fast только на `get_active` | [`registry_builder.py:22-26`](../../src/core/providers/registry_builder.py) | — | deferred (no task) |

## Gap queue (override-only, audit EPIC-IDS-09 EID-04 2026-06-08)

> Отчёт: [`epic-ids-09-eid-04-audit-2026-06-08.md`](../analysis/epic-ids-09-eid-04-audit-2026-06-08.md)
> **activation:** `run_mode=epic_ids_09_eid_04_audit_2026_06_08`
> **Контекст:** STORY-IDS-EID-04 🟢 Done; pkg-000017 default unchanged ([`identity-active-package.current.yaml`](./identity-active-package.current.yaml)).

| Gap ID | Severity | Суть | Файл:строка | Task README | Status |
|--------|----------|------|-------------|-------------|--------|
| F1 | MEDIUM | backlog doc-stale: Status Todo, устаревшие «Точки в коде», AC [ ] | [`STORY-IDS-EID-04-provider-owned-config.md:6,27-31`](./backlog-stories/eid/STORY-IDS-EID-04-provider-owned-config.md) | [t07 audit f1 backlog story status sync](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-04-provider-owned-config/task-ids-09-04-t07-audit-f1-backlog-story-status-sync/README.md) | 🟢 Done |
| F2 | MEDIUM | membership literal дублирует каталог дескрипторов (AC3 partial) | [`schema.py:106-107`](../../src/core/config/schema.py) | [t08 audit f2 eid provider membership from descriptors](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-04-provider-owned-config/task-ids-09-04-t08-audit-f2-eid-provider-membership-from-descriptors/README.md) | 🟢 Done |

## Gap queue (override-only, audit EPIC-IDS-09 EID-05 2026-06-08)

> Отчёт: [`epic-ids-09-eid-05-audit-2026-06-08.md`](../analysis/epic-ids-09-eid-05-audit-2026-06-08.md)
> **activation:** `run_mode=epic_ids_09_eid_05_audit_2026_06_08`
> **Контекст:** STORY-IDS-EID-05 🟢 Done; pkg-000018 default unchanged ([`identity-active-package.current.yaml`](./identity-active-package.current.yaml)).

| Gap ID | Severity | Суть | Файл:строка | Task README | Status |
|--------|----------|------|-------------|-------------|--------|
| F1 | MEDIUM | backlog doc-stale: Status Todo, устаревшие «Точки в коде», AC [ ] | [`STORY-IDS-EID-05-canonical-provider-contract.md:6,23-34`](./backlog-stories/eid/STORY-IDS-EID-05-canonical-provider-contract.md) | [t06 audit f1 backlog story status sync](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-05-canonical-provider-contract/task-ids-09-05-t06-audit-f1-backlog-story-status-sync/README.md) | 🟢 Done |
| F2 | MEDIUM | 06-eid-providers registry section stale (KeyError / only mock vs EID-03/04) | [`06-eid-providers.md:39-64`](../../runtime-docs/06-eid-providers.md) | [t07 audit f2 06 eid providers registry section reconcile](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-05-canonical-provider-contract/task-ids-09-05-t07-audit-f2-06-eid-providers-registry-section-reconcile/README.md) | 🟢 Done |

## Gap queue (override-only, audit EPIC-IDS-09 EID-06 2026-06-08)

> Отчёт: [`epic-ids-09-eid-06-audit-2026-06-08.md`](../analysis/epic-ids-09-eid-06-audit-2026-06-08.md)
> **activation:** `run_mode=epic_ids_09_eid_06_audit_2026_06_08`
> **Контекст:** STORY-IDS-EID-06 🟢 Done; pkg-000019 default unchanged ([`identity-active-package.current.yaml`](./identity-active-package.current.yaml)).

| Gap ID | Severity | Суть | Файл:строка | Task README | Status |
|--------|----------|------|-------------|-------------|--------|
| F1 | MEDIUM | backlog doc-stale: Status Todo, устаревшие «Точки в коде», AC [ ] | [`STORY-IDS-EID-06-browser-callback-redirect.md:6,25-37`](./backlog-stories/eid/STORY-IDS-EID-06-browser-callback-redirect.md) | [t07 audit f1 backlog story status sync](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-06-browser-callback-redirect/task-ids-09-06-t07-audit-f1-backlog-story-status-sync/README.md) | 🟢 Done |

## Gap queue (override-only, audit EPIC-IDS-10 PV-06 2026-06-11)

> Отчёт: [`epic-ids-10-pv-06-audit-2026-06-11.md`](../analysis/epic-ids-10-pv-06-audit-2026-06-11.md)
> **activation:** `run_mode=epic_ids_10_pv_06_audit_2026_06_11`
> **Контекст:** STORY-IDS-PV-06 🟢 Done; pkg-000027 default unchanged ([`identity-active-package.current.yaml`](./identity-active-package.current.yaml)).

| Gap ID | Severity | Суть | Файл:строка | Task README | Status |
|--------|----------|------|-------------|-------------|--------|
| F3 | MEDIUM | Telnyx settings из `os.environ` vs merged env для `AppConfig` (`.env`-only creds → ConfigError) | [`runtime_factory.py:24`](../../src/core/phone/runtime_factory.py); [`providers.py:11-15`](../../src/core/config/providers.py) | [t07 audit f3 sms runtime merged env source](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-06-telnyx-sms-sender/task-ids-10-06-t07-audit-f3-sms-runtime-merged-env-source/README.md) | 🟢 Done |
| F1 | MEDIUM | backlog doc-stale: Status Todo, AC [ ]; EPIC-IDS-PHONE PV-06 ⚪ | [`STORY-IDS-PV-06-telnyx-sms-sender.md:6,32-36`](./backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md); [`EPIC-IDS-PHONE.md:27`](./backlog-stories/phone-verification/EPIC-IDS-PHONE.md) | [t08 audit f1 backlog epic alias doc sync](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-06-telnyx-sms-sender/task-ids-10-06-t08-audit-f1-backlog-epic-alias-doc-sync/README.md) | 🟢 Done |
| F2 | LOW | индекс «314 pytest offline» — verified factual 314 (`pytest -m "not live_integration"`, audit 315 miscount) | [`bullrun-launch-index.md:12`](./bullrun-launch-index.md) | [t09 audit f2 bullrun pytest count sync](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-06-telnyx-sms-sender/task-ids-10-06-t09-audit-f2-bullrun-pytest-count-sync/README.md) | 🟢 Done |

## Gap queue (override-only, audit EPIC-IDS-10 PV-10 2026-06-28)

> Отчёт: [`epic-ids-10-pv-10-file-sms-sink-audit-2026-06-28.md`](../analysis/epic-ids-10-pv-10-file-sms-sink-audit-2026-06-28.md)
> **activation:** `run_mode=epic_ids_10_pv_10_audit_2026_06_28`
> **Контекст:** STORY-IDS-PV-10 🟢 Done; pkg-000041 default unchanged ([`identity-active-package.current.yaml`](./identity-active-package.current.yaml)).

| Gap ID | Severity | Суть | Файл:строка | Task README | Status |
|--------|----------|------|-------------|-------------|--------|
| F1 | LOW | pipeline «Целевое поведение» ms vs code seconds | [`STORY-IDS-PV-10-file-sms-sink-dev.md:27-28`](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/STORY-IDS-PV-10-file-sms-sink-dev.md) | [t08 audit f1 pipeline story timestamp example sync](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/task-ids-10-10-t08-audit-f1-pipeline-story-timestamp-example-sync/README.md) | 🟢 Done |
| F2 | LOW | EPIC-IDS-PHONE header PV-10 | [`EPIC-IDS-PHONE.md:3`](./backlog-stories/phone-verification/EPIC-IDS-PHONE.md) | — | closed inline (P4 audit) |
| INFO-1..3 | INFO | не дефекты / out of scope | audit §2 | — | excluded |

## Gap queue (override-only, audit EPIC-IDS-11 OAUTH-01 2026-06-24)

> Отчёт: [`epic-ids-11-oauth-01-audit-2026-06-24.md`](../analysis/epic-ids-11-oauth-01-audit-2026-06-24.md)
> **activation:** `run_mode=epic_ids_11_oauth_01_audit_2026_06_24`
> **Контекст:** STORY-IDS-OAUTH-01 🟢 Done; pkg-000029 default unchanged.

| Gap ID | Severity | Суть | Файл:строка | Task README | Status |
|--------|----------|------|-------------|-------------|--------|
| F1 | MEDIUM | backlog doc-stale: Status Todo, AC [ ], устаревшие «Точки в коде» | [`STORY-IDS-OAUTH-01...md:6,26-40`](./backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) | [t08 audit f1 backlog story doc sync](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-01-oauth-server-endpoints/task-ids-11-01-t08-audit-f1-backlog-story-doc-sync/README.md) | 🟢 Done |
| F2 | MEDIUM | EPIC-IDS-OAUTH backlog: OAUTH-01 ⚪, «501» в назначении/статусе | [`EPIC-IDS-OAUTH.md:8,17,22`](./backlog-stories/oauth/EPIC-IDS-OAUTH.md) | [t09 audit f2 epic oauth backlog index sync](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-01-oauth-server-endpoints/task-ids-11-01-t09-audit-f2-epic-oauth-backlog-index-sync/README.md) | 🟢 Done |
| F3 | MEDIUM | runtime-docs + OAUTH-02/03/04: «OAuth 501» после OAUTH-01 build | [`04-security.md:68+`](./runtime-docs/04-security.md); [`09-gateway-expectations.md:33`](./runtime-docs/09-gateway-expectations.md) | [t10 audit f3 runtime docs oauth 501 drift sync](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-01-oauth-server-endpoints/task-ids-11-01-t10-audit-f3-runtime-docs-oauth-501-drift-sync/README.md) | 🟢 Done |

## Gap queue (override-only, audit EPIC-IDS-11 OAUTH-02 2026-06-24)

> Отчёт: [`epic-ids-11-oauth-02-audit-2026-06-24.md`](../analysis/epic-ids-11-oauth-02-audit-2026-06-24.md)
> **activation:** `run_mode=epic_ids_11_oauth_02_audit_2026_06_24`
> **Контекст:** STORY-IDS-OAUTH-02 🟢 Done; pkg-000030 default unchanged. F1 excluded (backlog already 🟢 on disk).

| Gap ID | Severity | Суть | Файл:строка | Task README | Status |
|--------|----------|------|-------------|-------------|--------|
| F2 | MEDIUM | EPIC-IDS-OAUTH backlog: OAUTH-02 ⚪, «introspection не построены» | [`EPIC-IDS-OAUTH.md:8,18,22,28-29`](./backlog-stories/oauth/EPIC-IDS-OAUTH.md) | [t07 audit f2 epic oauth backlog index sync](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-02-introspection-and-service-token/task-ids-11-02-t07-audit-f2-epic-oauth-backlog-index-sync/README.md) | 🟢 Done |
| F3 | MEDIUM | runtime-docs: «introspect отсутствует» / «нет SERVICE_API_TOKEN» после OAUTH-02 | [`04-security.md:68,92-95`](./runtime-docs/04-security.md); [`09-gateway-expectations.md:32,34,47`](./runtime-docs/09-gateway-expectations.md) | [t08 audit f3 runtime docs introspection drift sync](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-02-introspection-and-service-token/task-ids-11-02-t08-audit-f3-runtime-docs-introspection-drift-sync/README.md) | 🟢 Done |
| F4 | MEDIUM | `SERVICE_API_TOKEN` не в pilot fail-fast → introspect открыт в pilot | [`schema.py:174-184`](../../src/core/config/schema.py); [`security.py:108-110`](../../src/core/api/security.py) | [t09 audit f4 pilot service api token fail fast](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-02-introspection-and-service-token/task-ids-11-02-t09-audit-f4-pilot-service-api-token-fail-fast/README.md) | 🟢 Done |

## Gap queue (override-only, audit EPIC-IDS-12 SEC-01 2026-06-26)

> Отчёт: [`epic-ids-12-sec-01-audit-2026-06-26.md`](../analysis/epic-ids-12-sec-01-audit-2026-06-26.md)
> **activation:** `run_mode=epic_ids_12_sec_01_audit_2026_06_26`
> **Контекст:** STORY-IDS-SEC-01 pipeline 🟢 Done; pkg-000035 default unchanged.

| Finding | Story | Gap task README | Status | Wave |
|---------|-------|-----------------|--------|------|
| F1 | STORY-IDS-SEC-01 | [t08 audit f1 backlog sec-01 story sync](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01-rate-limiting/task-ids-12-01-t08-audit-f1-backlog-sec-01-story-sync/README.md) | 🟢 Done | override epic_ids_12_sec_01_audit_2026_06_26 |
| F2 | STORY-IDS-SEC-01 | [t09 audit f2 callback ip xff trusted proxy](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01-rate-limiting/task-ids-12-01-t09-audit-f2-callback-ip-xff-trusted-proxy/README.md) | 🟢 Done | override epic_ids_12_sec_01_audit_2026_06_26 |

## Gap queue (override-only, audit EPIC-IDS-12 SEC-06 2026-07-04)

> Отчёт: [`epic-ids-12-sec-06-audit-2026-07-04.md`](../analysis/epic-ids-12-sec-06-audit-2026-07-04.md)
> **activation:** `run_mode=epic_ids_12_sec_06_audit_2026_07_04`
> **Контекст:** STORY-IDS-SEC-06 pipeline 🟢 Done; pkg-000042 default unchanged.

| Finding | Story | Gap task README | Status | Wave |
|---------|-------|-----------------|--------|------|
| F1 | STORY-IDS-SEC-06 | [t09 audit f1 jwks httpx client lifespan close](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t09-audit-f1-jwks-httpx-client-lifespan-close/README.md) | 🟢 Done | override epic_ids_12_sec_06_audit_2026_07_04 |
| F2 | STORY-IDS-SEC-06 | [t10 audit f2 live integration jwks only cleanup](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t10-audit-f2-live-integration-jwks-only-cleanup/README.md) | 🟢 Done | override epic_ids_12_sec_06_audit_2026_07_04 |

## Gap queue (override-only, audit EPIC-IDS-12 SEC-04 2026-07-09)

> Отчёт: [`epic-ids-12-sec-04-audit-2026-07-09.md`](../analysis/epic-ids-12-sec-04-audit-2026-07-09.md)
> **activation:** `run_mode=epic_ids_12_sec_04_audit_2026_07_09`
> **Контекст:** STORY-IDS-SEC-04 pipeline 🟢 Done (волна); pkg-000043 default unchanged.

| Finding | Story | Gap task README | Status | Wave |
|---------|-------|-----------------|--------|------|
| F1 | STORY-IDS-SEC-04 | [t06 audit f1 platform wording separation sync](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/task-ids-12-05-t06-audit-f1-platform-wording-separation-sync/README.md) | 🟢 Done | override epic_ids_12_sec_04_audit_2026_07_09 |
| F2 | STORY-IDS-SEC-04 | [t07 audit f2 no expose guard depth](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/task-ids-12-05-t07-audit-f2-no-expose-guard-depth/README.md) | 🟢 Done | override epic_ids_12_sec_04_audit_2026_07_09 |

## Task queue (override EPIC-IDS-06 audit 2026-06-02)

| Gap | Story | Task README | Status | Wave |
|-----|-------|-------------|--------|------|
| F1 | STORY-IDS-06-01 | [t03 audit f1 asgi import time config isolation](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-01-conftest-autouse-fixtures/task-ids-06-01-t03-audit-f1-asgi-import-time-config-isolation/README.md) | 🟢 Done | override epic_ids_06_audit_2026_06_02 |
| F2 | STORY-IDS-06-05 | [t03 audit f2 smoke exclusion ac doc align](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-05-live-server-smoke/task-ids-06-05-t03-audit-f2-smoke-exclusion-ac-doc-align/README.md) | 🟢 Done | override epic_ids_06_audit_2026_06_02 |
| F3 | STORY-IDS-06-03 | [t04 audit f3 tests package init files](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-03-live-supabase-integration/task-ids-06-03-t04-audit-f3-tests-package-init-files/README.md) | 🟢 Done | override epic_ids_06_audit_2026_06_02 |
| F4 | STORY-IDS-06-05 | [t04 audit f4 smoke marker ssot](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-05-live-server-smoke/task-ids-06-05-t04-audit-f4-smoke-marker-ssot/README.md) | 🟢 Done | override epic_ids_06_audit_2026_06_02 |
| F5 | STORY-IDS-06-02 | [t06 audit f5 pytest asyncio config align](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-02-http-bootstrap-di-smoke-tests/task-ids-06-02-t06-audit-f5-pytest-asyncio-config-align/README.md) | 🟢 Done | override epic_ids_06_audit_2026_06_02 |

## Task queue (override EPIC-IDS-08 CLEANUP-02 audit 2026-06-05)

| Gap | Story | Task README | Status | Wave |
|-----|-------|-------------|--------|------|
| F1 | STORY-IDS-CLEANUP-02 | [t08 audit f1 return url enforcement](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/task-ids-08-02-t08-audit-f1-return-url-validator-enforcement/README.md) | 🟢 Done | override epic_ids_08_cleanup_02_audit_2026_06_05 |
| F2 | STORY-IDS-CLEANUP-02 | [t09 audit f2 empty layer dirs doc](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/task-ids-08-02-t09-audit-f2-empty-layer-directories-doc-align/README.md) | 🟢 Done | override epic_ids_08_cleanup_02_audit_2026_06_05 |
| F3 | STORY-IDS-CLEANUP-02 | [t10 audit f3 idempotency doc drift](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/task-ids-08-02-t10-audit-f3-idempotency-runtime-doc-drift/README.md) | 🟢 Done | override epic_ids_08_cleanup_02_audit_2026_06_05 |

## Task queue (EPIC-IDS-01)

| Epic | Story | Task README | Status | Input package |
|------|-------|-------------|--------|---------------|
| EPIC-IDS-01 | STORY-IDS-01-01 | [t01 package skeleton](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-01-init-package-and-dependencies/task-ids-01-01-t01-package-directory-skeleton/README.md) | 🟢 Done | pkg-000001 |
| EPIC-IDS-01 | STORY-IDS-01-01 | [t02 pyproject](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-01-init-package-and-dependencies/task-ids-01-01-t02-pyproject-and-pyright/README.md) | 🟢 Done | pkg-000001 |
| EPIC-IDS-01 | STORY-IDS-01-01 | [t03 editable install](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-01-init-package-and-dependencies/task-ids-01-01-t03-editable-install-verify/README.md) | 🟢 Done | pkg-000001 |
| EPIC-IDS-01 | STORY-IDS-01-02 | [t01 config schema](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-02-appconfig/task-ids-01-02-t01-config-schema/README.md) | 🟢 Done | pkg-000001 |
| EPIC-IDS-01 | STORY-IDS-01-02 | [t02 config exports](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-02-appconfig/task-ids-01-02-t02-config-package-exports/README.md) | 🟢 Done | pkg-000001 |
| EPIC-IDS-01 | STORY-IDS-01-02 | [t03 config tests](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-02-appconfig/task-ids-01-02-t03-config-schema-tests/README.md) | 🟢 Done | pkg-000001 |
| EPIC-IDS-01 | STORY-IDS-01-03 | [t01 env file](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-03-custom-dotenv-parser/task-ids-01-03-t01-env-file-merge/README.md) | 🟢 Done | pkg-000001 |
| EPIC-IDS-01 | STORY-IDS-01-03 | [t02 provide_app_config](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-03-custom-dotenv-parser/task-ids-01-03-t02-provide-app-config/README.md) | 🟢 Done | pkg-000001 |
| EPIC-IDS-01 | STORY-IDS-01-03 | [t03 dotenv tests](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-03-custom-dotenv-parser/task-ids-01-03-t03-dotenv-parser-tests/README.md) | 🟢 Done | pkg-000001 |
| EPIC-IDS-01 | STORY-IDS-01-04 | [t01 Makefile](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-04-makefile-railway-env-example/task-ids-01-04-t01-makefile-targets/README.md) | 🟢 Done | pkg-000001 |
| EPIC-IDS-01 | STORY-IDS-01-04 | [t02 railpack](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-04-makefile-railway-env-example/task-ids-01-04-t02-railpack-json/README.md) | 🟢 Done | pkg-000001 |
| EPIC-IDS-01 | STORY-IDS-01-04 | [t03 .env.example](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-04-makefile-railway-env-example/task-ids-01-04-t03-env-example/README.md) | 🟢 Done | pkg-000001 |

## Task queue (EPIC-IDS-02)

| Epic | Story | Task README | Status | Input package |
|------|-------|-------------|--------|---------------|
| EPIC-IDS-02 | STORY-IDS-02-01 | [t01 envelope core](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-01-response-envelope-error-trace-id/task-ids-02-01-t01-envelope-core/README.md) | 🟢 Done | pkg-000003 |
| EPIC-IDS-02 | STORY-IDS-02-01 | [t02 idempotency key](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-01-response-envelope-error-trace-id/task-ids-02-01-t02-idempotency-key-resolver/README.md) | 🟢 Done | pkg-000003 |
| EPIC-IDS-02 | STORY-IDS-02-01 | [t03 envelope tests](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-01-response-envelope-error-trace-id/task-ids-02-01-t03-envelope-acceptance-tests/README.md) | 🟢 Done | pkg-000003 |
| EPIC-IDS-02 | STORY-IDS-02-02 | [t01 logging setup](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-02-logging-setup/task-ids-02-02-t01-configure-logging-runtime/README.md) | 🟢 Done | pkg-000003 |
| EPIC-IDS-02 | STORY-IDS-02-02 | [t02 logging verification](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-02-logging-setup/task-ids-02-02-t02-logging-verification/README.md) | 🟢 Done | pkg-000003 |
| EPIC-IDS-02 | STORY-IDS-02-03 | [t01 unauthorized protocol](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-03-auth-security-primitives-bearer-stub/task-ids-02-03-t01-unauthorized-error-and-protocol/README.md) | 🟢 Done | pkg-000003 |
| EPIC-IDS-02 | STORY-IDS-02-03 | [t02 stub bearer dependency](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-03-auth-security-primitives-bearer-stub/task-ids-02-03-t02-stub-bearer-auth-and-current-user/README.md) | 🟢 Done | pkg-000003 |
| EPIC-IDS-02 | STORY-IDS-02-03 | [t03 auth primitives verification](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-03-auth-security-primitives-bearer-stub/task-ids-02-03-t03-auth-primitives-verification/README.md) | 🟢 Done | pkg-000003 |
| EPIC-IDS-02 | STORY-IDS-02-04 | [t01 app and lifespan](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-04-fastapi-app-lifespan-cors-middleware/task-ids-02-04-t01-create-app-and-lifespan/README.md) | 🟢 Done | pkg-000003 |
| EPIC-IDS-02 | STORY-IDS-02-04 | [t02 middleware handlers](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-04-fastapi-app-lifespan-cors-middleware/task-ids-02-04-t02-runtime-middleware-and-exception-handlers/README.md) | 🟢 Done | pkg-000003 |
| EPIC-IDS-02 | STORY-IDS-02-04 | [t03 dependencies cache](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-04-fastapi-app-lifespan-cors-middleware/task-ids-02-04-t03-api-dependencies-cache-hooks/README.md) | 🟢 Done | pkg-000003 |
| EPIC-IDS-02 | STORY-IDS-02-05 | [t01 health readiness handlers](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-05-routes-contract-health-ready-identity-stubs/task-ids-02-05-t01-health-and-readiness-handlers/README.md) | 🟢 Done | pkg-000003 |
| EPIC-IDS-02 | STORY-IDS-02-05 | [t02 route contract stubs](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-05-routes-contract-health-ready-identity-stubs/task-ids-02-05-t02-identity-route-contract-stubs/README.md) | 🟢 Done | pkg-000003 |
| EPIC-IDS-02 | STORY-IDS-02-05 | [t03 options preflight](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-05-routes-contract-health-ready-identity-stubs/task-ids-02-05-t03-options-preflight-contract/README.md) | 🟢 Done | pkg-000003 |

## Task queue (EPIC-IDS-03)

| Epic | Story | Task README | Status | Input package |
|------|-------|-------------|--------|---------------|
| EPIC-IDS-03 | STORY-IDS-03-01 | [t01 dataclass handler alias](./epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-01-api-dependencies-dataclass-handler-alias/task-ids-03-01-t01-api-dependencies-dataclass-handler-alias/README.md) | 🟢 Done | pkg-000004 |
| EPIC-IDS-03 | STORY-IDS-03-01 | [t02 dataclass verification](./epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-01-api-dependencies-dataclass-handler-alias/task-ids-03-01-t02-api-dependencies-dataclass-verification/README.md) | 🟢 Done | pkg-000004 |
| EPIC-IDS-03 | STORY-IDS-03-02 | [t01 build factory](./epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-02-build-api-dependencies-singleton-lifespan/task-ids-03-02-t01-build-api-dependencies-factory/README.md) | 🟢 Done | pkg-000004 |
| EPIC-IDS-03 | STORY-IDS-03-02 | [t02 asgi singleton lifespan](./epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-02-build-api-dependencies-singleton-lifespan/task-ids-03-02-t02-asgi-singleton-lifespan-integration/README.md) | 🟢 Done | pkg-000004 |
| EPIC-IDS-03 | STORY-IDS-03-02 | [t03 singleton verification](./epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-02-build-api-dependencies-singleton-lifespan/task-ids-03-02-t03-singleton-behavior-verification/README.md) | 🟢 Done | pkg-000004 |
| EPIC-IDS-03 | STORY-IDS-03-03 | [t01 todo epic hooks](./epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-03-epic-ids-04-extension-hook-contract/task-ids-03-03-t01-todo-epic-hooks-in-build-factory/README.md) | 🟢 Done | pkg-000004 |
| EPIC-IDS-03 | STORY-IDS-03-03 | [t02 field list alignment](./epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-03-epic-ids-04-extension-hook-contract/task-ids-03-03-t02-contract-field-list-alignment/README.md) | 🟢 Done | pkg-000004 |

## Task queue (EPIC-IDS-04)

| Epic | Story | Task README | Status | Input package |
|------|-------|-------------|--------|---------------|
| EPIC-IDS-04 | STORY-IDS-04-01 | [t01 domain contracts protocols](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-01-domain-protocols-contracts/task-ids-04-01-t01-domain-contracts-protocols/README.md) | 🟢 Done | pkg-000005 |
| EPIC-IDS-04 | STORY-IDS-04-01 | [t02 domain models dataclasses](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-01-domain-protocols-contracts/task-ids-04-01-t02-domain-models-dataclasses/README.md) | 🟢 Done | pkg-000005 |
| EPIC-IDS-04 | STORY-IDS-04-01 | [t03 story1 acceptance verification](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-01-domain-protocols-contracts/task-ids-04-01-t03-story1-acceptance-verification/README.md) | 🟢 Done | pkg-000005 |
| EPIC-IDS-04 | STORY-IDS-04-02 | [t01 hash secret contract verify](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-02-inmemory-repositories/task-ids-04-02-t01-hash-secret-contract-verify/README.md) | 🟢 Done | pkg-000005 |
| EPIC-IDS-04 | STORY-IDS-04-02 | [t02 inmemory repositories](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-02-inmemory-repositories/task-ids-04-02-t02-inmemory-repositories/README.md) | 🟢 Done | pkg-000005 |
| EPIC-IDS-04 | STORY-IDS-04-02 | [t03 story2 acceptance verification](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-02-inmemory-repositories/task-ids-04-02-t03-story2-acceptance-verification/README.md) | 🟢 Done | pkg-000005 |
| EPIC-IDS-04 | STORY-IDS-04-03 | [t01 service factory protocol and default](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-03-service-factory-default/task-ids-04-03-t01-service-factory-protocol-and-default/README.md) | 🟢 Done | pkg-000005 |
| EPIC-IDS-04 | STORY-IDS-04-03 | [t02 story3 acceptance verification](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-03-service-factory-default/task-ids-04-03-t02-story3-acceptance-verification/README.md) | 🟢 Done | pkg-000005 |
| EPIC-IDS-04 | STORY-IDS-04-04 | [t01 eid provider port base](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-04-eid-provider-registry-mock/task-ids-04-04-t01-eid-provider-port-base/README.md) | 🟢 Done | pkg-000005 |
| EPIC-IDS-04 | STORY-IDS-04-04 | [t02 eid registry and mock provider](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-04-eid-provider-registry-mock/task-ids-04-04-t02-eid-registry-and-mock-provider/README.md) | 🟢 Done | pkg-000005 |
| EPIC-IDS-04 | STORY-IDS-04-04 | [t03 story4 acceptance verification](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-04-eid-provider-registry-mock/task-ids-04-04-t03-story4-acceptance-verification/README.md) | 🟢 Done | pkg-000005 |
| EPIC-IDS-04 | STORY-IDS-04-05 | [t01 supabase jwt validator impl](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-05-supabase-jwt-bearer-auth/task-ids-04-05-t01-supabase-jwt-validator-impl/README.md) | 🟢 Done | pkg-000005 |
| EPIC-IDS-04 | STORY-IDS-04-05 | [t02 supabase jwt bearer token auth](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-05-supabase-jwt-bearer-auth/task-ids-04-05-t02-supabase-jwt-bearer-token-auth/README.md) | 🟢 Done | pkg-000005 |
| EPIC-IDS-04 | STORY-IDS-04-05 | [t03 story5 acceptance verification](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-05-supabase-jwt-bearer-auth/task-ids-04-05-t03-story5-acceptance-verification/README.md) | 🟢 Done | pkg-000005 |
| EPIC-IDS-04 | STORY-IDS-04-06 | [t01 provide service factory](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-06-provide-factory-di-integration/task-ids-04-06-t01-provide-service-factory/README.md) | 🟢 Done | pkg-000005 |
| EPIC-IDS-04 | STORY-IDS-04-06 | [t02 build api dependencies integration](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-06-provide-factory-di-integration/task-ids-04-06-t02-build-api-dependencies-integration/README.md) | 🟢 Done | pkg-000005 |
| EPIC-IDS-04 | STORY-IDS-04-06 | [t03 story6 epic integration verification](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-06-provide-factory-di-integration/task-ids-04-06-t03-story6-epic-integration-verification/README.md) | 🟢 Done | pkg-000005 |

## Task queue (EPIC-IDS-05)

| Epic | Story | Task README | Status | Input package |
|------|-------|-------------|--------|---------------|
| EPIC-IDS-05 | STORY-IDS-05-01 | [t01 supabase database http client](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-01-supabase-database-http-client/task-ids-05-01-t01-supabase-database-http-client/README.md) | 🟢 Done | pkg-000006 |
| EPIC-IDS-05 | STORY-IDS-05-01 | [t02 story1 acceptance verification](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-01-supabase-database-http-client/task-ids-05-01-t02-story1-acceptance-verification/README.md) | 🟢 Done | pkg-000006 |
| EPIC-IDS-05 | STORY-IDS-05-02 | [t01 profile and verification session repos](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-02-supabase-repositories-identity-set/task-ids-05-02-t01-profile-and-verification-session-repos/README.md) | 🟢 Done | pkg-000006 |
| EPIC-IDS-05 | STORY-IDS-05-02 | [t02 audit oauth story health repos](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-02-supabase-repositories-identity-set/task-ids-05-02-t02-audit-oauth-story-health-repos/README.md) | 🟢 Done | pkg-000006 |
| EPIC-IDS-05 | STORY-IDS-05-02 | [t03 story2 acceptance verification](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-02-supabase-repositories-identity-set/task-ids-05-02-t03-story2-acceptance-verification/README.md) | 🟢 Done | pkg-000006 |
| EPIC-IDS-05 | STORY-IDS-05-03 | [t01 supabase database healthcheck methods](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-03-five-level-healthcheck/task-ids-05-03-t01-supabase-database-healthcheck-methods/README.md) | 🟢 Done | pkg-000006 |
| EPIC-IDS-05 | STORY-IDS-05-03 | [t02 build api dependencies db checks](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-03-five-level-healthcheck/task-ids-05-03-t02-build-api-dependencies-db-checks/README.md) | 🟢 Done | pkg-000006 |
| EPIC-IDS-05 | STORY-IDS-05-03 | [t03 story3 acceptance verification](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-03-five-level-healthcheck/task-ids-05-03-t03-story3-acceptance-verification/README.md) | 🟢 Done | pkg-000006 |
| EPIC-IDS-05 | STORY-IDS-05-04 | [t01 req08 core migrations](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-04-sql-schema-migrations/task-ids-05-04-t01-req08-core-migrations/README.md) | 🟢 Done | pkg-000006 |
| EPIC-IDS-05 | STORY-IDS-05-04 | [t02 req17 req15 migrations](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-04-sql-schema-migrations/task-ids-05-04-t02-req17-req15-migrations/README.md) | 🟢 Done | pkg-000006 |
| EPIC-IDS-05 | STORY-IDS-05-04 | [t03 story4 acceptance verification](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-04-sql-schema-migrations/task-ids-05-04-t03-story4-acceptance-verification/README.md) | 🟢 Done | pkg-000006 |
| EPIC-IDS-05 | STORY-IDS-05-05 | [t01 supabase setup runbook](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-05-supabase-project-setup-live-credentials/task-ids-05-05-t01-supabase-setup-runbook/README.md) | 🟢 Done | pkg-000006 |
| EPIC-IDS-05 | STORY-IDS-05-05 | [t02 ci test secrets layout](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-05-supabase-project-setup-live-credentials/task-ids-05-05-t02-ci-test-secrets-layout/README.md) | 🟢 Done | pkg-000006 |
| EPIC-IDS-05 | STORY-IDS-05-05 | [t03 story5 acceptance verification](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-05-supabase-project-setup-live-credentials/task-ids-05-05-t03-story5-acceptance-verification/README.md) | 🟢 Done | pkg-000006 |
| EPIC-IDS-05 | STORY-IDS-05-06 | [t01 provide service factory supabase branch](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-06-backend-switch-provide-service-factory/task-ids-05-06-t01-provide-service-factory-supabase-branch/README.md) | 🟢 Done | pkg-000006 |
| EPIC-IDS-05 | STORY-IDS-05-06 | [t02 supabase fallback test migration](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-06-backend-switch-provide-service-factory/task-ids-05-06-t02-supabase-fallback-test-migration/README.md) | 🟢 Done | pkg-000006 |
| EPIC-IDS-05 | STORY-IDS-05-06 | [t03 story6 acceptance verification](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-06-backend-switch-provide-service-factory/task-ids-05-06-t03-story6-acceptance-verification/README.md) | 🟢 Done | pkg-000006 |

## Task queue (EPIC-IDS-06)

| Epic | Story | Task README | Status | Input package |
|------|-------|-------------|--------|---------------|
| EPIC-IDS-06 | STORY-IDS-06-01 | [t01 conftest autouse fixtures](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-01-conftest-autouse-fixtures/task-ids-06-01-t01-conftest-autouse-fixtures/README.md) | 🟢 Done | pkg-000008 |
| EPIC-IDS-06 | STORY-IDS-06-01 | [t02 story1 acceptance verification](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-01-conftest-autouse-fixtures/task-ids-06-01-t02-story1-acceptance-verification/README.md) | 🟢 Done | pkg-000008 |
| EPIC-IDS-06 | STORY-IDS-06-02 | [t01 bootstrap smoke tests](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-02-http-bootstrap-di-smoke-tests/task-ids-06-02-t01-bootstrap-smoke-tests/README.md) | 🟢 Done | pkg-000008 |
| EPIC-IDS-06 | STORY-IDS-06-02 | [t02 http transport smoke tests](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-02-http-bootstrap-di-smoke-tests/task-ids-06-02-t02-http-transport-smoke-tests/README.md) | 🟢 Done | pkg-000008 |
| EPIC-IDS-06 | STORY-IDS-06-02 | [t03 di singleton and service factory tests](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-02-http-bootstrap-di-smoke-tests/task-ids-06-02-t03-di-singleton-and-service-factory-tests/README.md) | 🟢 Done | pkg-000008 |
| EPIC-IDS-06 | STORY-IDS-06-02 | [t04 eid registry and jwt validator tests](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-02-http-bootstrap-di-smoke-tests/task-ids-06-02-t04-eid-registry-and-jwt-validator-tests/README.md) | 🟢 Done | pkg-000008 |
| EPIC-IDS-06 | STORY-IDS-06-02 | [t05 story2 acceptance verification](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-02-http-bootstrap-di-smoke-tests/task-ids-06-02-t05-story2-acceptance-verification/README.md) | 🟢 Done | pkg-000008 |
| EPIC-IDS-06 | STORY-IDS-06-03 | [t01 supabase connectivity health tests](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-03-live-supabase-integration/task-ids-06-03-t01-supabase-connectivity-health-tests/README.md) | 🟢 Done | pkg-000008 |
| EPIC-IDS-06 | STORY-IDS-06-03 | [t02 supabase identity roundtrip tests](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-03-live-supabase-integration/task-ids-06-03-t02-supabase-identity-roundtrip-tests/README.md) | 🟢 Done | pkg-000008 |
| EPIC-IDS-06 | STORY-IDS-06-03 | [t03 story3 acceptance verification](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-03-live-supabase-integration/task-ids-06-03-t03-story3-acceptance-verification/README.md) | 🟢 Done | pkg-000008 |
| EPIC-IDS-06 | STORY-IDS-06-04 | [t01 test offline workflow](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-04-ci-workflows-offline-live/task-ids-06-04-t01-test-offline-workflow/README.md) | 🟢 Done | pkg-000008 |
| EPIC-IDS-06 | STORY-IDS-06-04 | [t02 integration live workflow and secrets doc](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-04-ci-workflows-offline-live/task-ids-06-04-t02-integration-live-workflow-and-secrets-doc/README.md) | 🟢 Done | pkg-000008 |
| EPIC-IDS-06 | STORY-IDS-06-04 | [t03 story4 acceptance verification](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-04-ci-workflows-offline-live/task-ids-06-04-t03-story4-acceptance-verification/README.md) | 🟢 Done | pkg-000008 |
| EPIC-IDS-06 | STORY-IDS-06-05 | [t01 smoke conftest and local server tests](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-05-live-server-smoke/task-ids-06-05-t01-smoke-conftest-and-local-server-tests/README.md) | 🟢 Done | pkg-000008 |
| EPIC-IDS-06 | STORY-IDS-06-05 | [t02 story5 acceptance verification](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-05-live-server-smoke/task-ids-06-05-t02-story5-acceptance-verification/README.md) | 🟢 Done | pkg-000008 |

## Task queue (EPIC-IDS-07)

| Epic | Story | Task README | Status | Input package |
|------|-------|-------------|--------|---------------|
| EPIC-IDS-07 | STORY-IDS-AUTHCORE-01 | [t01 missing profile behavior decision](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t01-missing-profile-behavior-decision/README.md) | 🟢 Done | pkg-000009 |
| EPIC-IDS-07 | STORY-IDS-AUTHCORE-01 | [t02 handle me handler](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t02-handle-me-handler/README.md) | 🟢 Done | pkg-000009 |
| EPIC-IDS-07 | STORY-IDS-AUTHCORE-01 | [t03 me response payload](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t03-me-response-payload/README.md) | 🟢 Done | pkg-000009 |
| EPIC-IDS-07 | STORY-IDS-AUTHCORE-01 | [t04 asgi route wire handle me](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t04-asgi-route-wire-handle-me/README.md) | 🟢 Done | pkg-000009 |
| EPIC-IDS-07 | STORY-IDS-AUTHCORE-01 | [t05 me offline tests](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t05-me-offline-tests/README.md) | 🟢 Done | pkg-000009 |
| EPIC-IDS-07 | STORY-IDS-AUTHCORE-01 | [t06 story acceptance verification](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t06-story-acceptance-verification/README.md) | 🟢 Done | pkg-000009 |
| EPIC-IDS-07 | STORY-IDS-AUTHCORE-01 | [t07 audit f1 dotenv cwd test isolation](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t07-audit-f1-dotenv-cwd-test-isolation/README.md) | 🟢 Done | pkg-000010 |
| EPIC-IDS-07 | STORY-IDS-AUTHCORE-01 | [t08 audit f2 backlog story status sync](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t08-audit-f2-backlog-story-status-sync/README.md) | 🟢 Done | pkg-000010 |
| EPIC-IDS-07 | STORY-IDS-AUTHCORE-01 | [t09 audit f3 remove handle me stub](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t09-audit-f3-remove-handle-me-stub/README.md) | 🟢 Done | pkg-000010 |
| EPIC-IDS-07 | STORY-IDS-AUTHCORE-01 | [t10 audit f4 basic rights doc align](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t10-audit-f4-basic-rights-doc-align/README.md) | 🟢 Done | pkg-000010 |
| EPIC-IDS-07 | STORY-IDS-AUTHCORE-01 | [t11 audit f5 bullrun index factual sync](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t11-audit-f5-bullrun-index-factual-sync/README.md) | 🟢 Done | pkg-000010 |
| EPIC-IDS-07 | STORY-IDS-AUTHCORE-01 | [t12 audit f6 gitignore env](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/task-ids-07-01-t12-audit-f6-gitignore-env/README.md) | 🟢 Done | pkg-000010 |
| EPIC-IDS-07 | STORY-IDS-AUTHCORE-02 | [t01 me response created_at account_status](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-02-me-account-fields/task-ids-07-02-t01-me-response-created-at-account-status/README.md) | 🟢 Done | pkg-000044 |
| EPIC-IDS-07 | STORY-IDS-AUTHCORE-02 | [t02 me api docs created_at account_status](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-02-me-account-fields/task-ids-07-02-t02-me-api-docs-created-at-account-status/README.md) | 🟢 Done | pkg-000044 |
| EPIC-IDS-07 | STORY-IDS-AUTHCORE-02 | [t03 me profile offline tests account fields](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-02-me-account-fields/task-ids-07-02-t03-me-profile-offline-tests-account-fields/README.md) | 🟢 Done | pkg-000044 |
| EPIC-IDS-07 | STORY-IDS-AUTHCORE-02 | [t04 story acceptance verification](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-02-me-account-fields/task-ids-07-02-t04-story-acceptance-verification/README.md) | 🟢 Done | pkg-000044 |
| EPIC-IDS-07 | STORY-IDS-AUTHCORE-02 | [t05 audit g3 created_at semantics docs](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-02-me-account-fields/task-ids-07-02-t05-audit-g3-created-at-semantics-docs/README.md) | 🟢 Done | override epic_ids_07_authcore_02_audit_2026_07_24 |

## Task queue (EPIC-IDS-09)

| Epic | Story | Task README | Status | Input package |
|------|-------|-------------|--------|---------------|
| EPIC-IDS-09 | STORY-IDS-EID-01 | [t01 handle auth eid start orchestration](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-01-eid-verification-flow/task-ids-09-01-t01-handle-auth-eid-start-orchestration/README.md) | 🟢 Done | pkg-000015 |
| EPIC-IDS-09 | STORY-IDS-EID-01 | [t02 asgi eid start wire body](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-01-eid-verification-flow/task-ids-09-01-t02-asgi-eid-start-wire-body/README.md) | 🟢 Done | pkg-000015 |
| EPIC-IDS-09 | STORY-IDS-EID-01 | [t03 mock callback orchestration](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-01-eid-verification-flow/task-ids-09-01-t03-mock-callback-orchestration/README.md) | 🟢 Done | pkg-000015 |
| EPIC-IDS-09 | STORY-IDS-EID-01 | [t04 session lifecycle audit events](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-01-eid-verification-flow/task-ids-09-01-t04-session-lifecycle-audit-events/README.md) | 🟢 Done | pkg-000015 |
| EPIC-IDS-09 | STORY-IDS-EID-01 | [t05 mock eid flow offline tests](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-01-eid-verification-flow/task-ids-09-01-t05-mock-eid-flow-offline-tests/README.md) | 🟢 Done | pkg-000015 |
| EPIC-IDS-09 | STORY-IDS-EID-01 | [t06 story acceptance verification](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-01-eid-verification-flow/task-ids-09-01-t06-story-acceptance-verification/README.md) | 🟢 Done | pkg-000015 |
| EPIC-IDS-09 | STORY-IDS-EID-01 | [t07 audit f1 backlog story status sync](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-01-eid-verification-flow/task-ids-09-01-t07-audit-f1-backlog-story-status-sync/README.md) | 🟢 Done | override epic_ids_09_eid_01_audit_2026_06_06 |
| EPIC-IDS-09 | STORY-IDS-EID-03 | [t01 descriptor runtime types](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-03-provider-plugin-backbone/task-ids-09-03-t01-descriptor-runtime-types/README.md) | 🟢 Done | pkg-000016 |
| EPIC-IDS-09 | STORY-IDS-EID-03 | [t02 provider runtime factory](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-03-provider-plugin-backbone/task-ids-09-03-t02-provider-runtime-factory/README.md) | 🟢 Done | pkg-000016 |
| EPIC-IDS-09 | STORY-IDS-EID-03 | [t03 lazy registry mock descriptor](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-03-provider-plugin-backbone/task-ids-09-03-t03-lazy-registry-mock-descriptor/README.md) | 🟢 Done | pkg-000016 |
| EPIC-IDS-09 | STORY-IDS-EID-03 | [t04 registry guard config error](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-03-provider-plugin-backbone/task-ids-09-03-t04-registry-guard-config-error/README.md) | 🟢 Done | pkg-000016 |
| EPIC-IDS-09 | STORY-IDS-EID-03 | [t05 offline registry guard tests](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-03-provider-plugin-backbone/task-ids-09-03-t05-offline-registry-guard-tests/README.md) | 🟢 Done | pkg-000016 |
| EPIC-IDS-09 | STORY-IDS-EID-03 | [t06 story acceptance verification](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-03-provider-plugin-backbone/task-ids-09-03-t06-story-acceptance-verification/README.md) | 🟢 Done | pkg-000016 |
| EPIC-IDS-09 | STORY-IDS-EID-03 | [t07 audit f1 backlog story status sync](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-03-provider-plugin-backbone/task-ids-09-03-t07-audit-f1-backlog-story-status-sync/README.md) | ⚪ Todo | override epic_ids_09_eid_03_audit_2026_06_08 |
| EPIC-IDS-09 | STORY-IDS-EID-04 | [t01 provider config spec types](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-04-provider-owned-config/task-ids-09-04-t01-provider-config-spec-types/README.md) | 🟢 Done | pkg-000017 |
| EPIC-IDS-09 | STORY-IDS-EID-04 | [t02 authentigate settings config spec](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-04-provider-owned-config/task-ids-09-04-t02-authentigate-settings-config-spec/README.md) | 🟢 Done | pkg-000017 |
| EPIC-IDS-09 | STORY-IDS-EID-04 | [t03 delegated validation schema cleanup](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-04-provider-owned-config/task-ids-09-04-t03-delegated-validation-schema-cleanup/README.md) | 🟢 Done | pkg-000017 |
| EPIC-IDS-09 | STORY-IDS-EID-04 | [t04 env example authentigate vars](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-04-provider-owned-config/task-ids-09-04-t04-env-example-authentigate-vars/README.md) | 🟢 Done | pkg-000017 |
| EPIC-IDS-09 | STORY-IDS-EID-04 | [t05 offline provider config tests](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-04-provider-owned-config/task-ids-09-04-t05-offline-provider-config-tests/README.md) | 🟢 Done | pkg-000017 |
| EPIC-IDS-09 | STORY-IDS-EID-04 | [t06 story acceptance verification](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-04-provider-owned-config/task-ids-09-04-t06-story-acceptance-verification/README.md) | 🟢 Done | pkg-000017 |
| EPIC-IDS-09 | STORY-IDS-EID-04 | [t07 audit f1 backlog story status sync](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-04-provider-owned-config/task-ids-09-04-t07-audit-f1-backlog-story-status-sync/README.md) | 🟢 Done | override epic_ids_09_eid_04_audit_2026_06_08 |
| EPIC-IDS-09 | STORY-IDS-EID-04 | [t08 audit f2 eid provider membership from descriptors](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-04-provider-owned-config/task-ids-09-04-t08-audit-f2-eid-provider-membership-from-descriptors/README.md) | 🟢 Done | override epic_ids_09_eid_04_audit_2026_06_08 |
| EPIC-IDS-09 | STORY-IDS-EID-05 | [t01 eid error code enum](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-05-canonical-provider-contract/task-ids-09-05-t01-eid-error-code-enum/README.md) | 🟢 Done | pkg-000018 |
| EPIC-IDS-09 | STORY-IDS-EID-05 | [t02 orchestrator provider error handling](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-05-canonical-provider-contract/task-ids-09-05-t02-orchestrator-provider-error-handling/README.md) | 🟢 Done | pkg-000018 |
| EPIC-IDS-09 | STORY-IDS-EID-05 | [t03 canonical subject hash contract](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-05-canonical-provider-contract/task-ids-09-05-t03-canonical-subject-hash-contract/README.md) | 🟢 Done | pkg-000018 |
| EPIC-IDS-09 | STORY-IDS-EID-05 | [t04 offline contract tests](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-05-canonical-provider-contract/task-ids-09-05-t04-offline-contract-tests/README.md) | 🟢 Done | pkg-000018 |
| EPIC-IDS-09 | STORY-IDS-EID-05 | [t05 story acceptance verification](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-05-canonical-provider-contract/task-ids-09-05-t05-story-acceptance-verification/README.md) | 🟢 Done | pkg-000018 |
| EPIC-IDS-09 | STORY-IDS-EID-05 | [t06 audit f1 backlog story status sync](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-05-canonical-provider-contract/task-ids-09-05-t06-audit-f1-backlog-story-status-sync/README.md) | 🟢 Done | override epic_ids_09_eid_05_audit_2026_06_08 |
| EPIC-IDS-09 | STORY-IDS-EID-05 | [t07 audit f2 06 eid providers registry section reconcile](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-05-canonical-provider-contract/task-ids-09-05-t07-audit-f2-06-eid-providers-registry-section-reconcile/README.md) | 🟢 Done | override epic_ids_09_eid_05_audit_2026_06_08 |
| EPIC-IDS-09 | STORY-IDS-EID-06 | [t01 eid callback outcome dataclass](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-06-browser-callback-redirect/task-ids-09-06-t01-eid-callback-outcome-dataclass/README.md) | 🟢 Done | pkg-000019 |
| EPIC-IDS-09 | STORY-IDS-EID-06 | [t02 dynamic callback route registry guard](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-06-browser-callback-redirect/task-ids-09-06-t02-dynamic-callback-route-registry-guard/README.md) | 🟢 Done | pkg-000019 |
| EPIC-IDS-09 | STORY-IDS-EID-06 | [t03 callback redirect render accept negotiate](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-06-browser-callback-redirect/task-ids-09-06-t03-callback-redirect-render-accept-negotiate/README.md) | 🟢 Done | pkg-000019 |
| EPIC-IDS-09 | STORY-IDS-EID-06 | [t04 offline redirect and json regression tests](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-06-browser-callback-redirect/task-ids-09-06-t04-offline-redirect-and-json-regression-tests/README.md) | 🟢 Done | pkg-000019 |
| EPIC-IDS-09 | STORY-IDS-EID-06 | [t05 spa first runtime docs](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-06-browser-callback-redirect/task-ids-09-06-t05-spa-first-runtime-docs/README.md) | 🟢 Done | pkg-000019 |
| EPIC-IDS-09 | STORY-IDS-EID-06 | [t06 story acceptance verification](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-06-browser-callback-redirect/task-ids-09-06-t06-story-acceptance-verification/README.md) | 🟢 Done | pkg-000019 |
| EPIC-IDS-09 | STORY-IDS-EID-06 | [t07 audit f1 backlog story status sync](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-06-browser-callback-redirect/task-ids-09-06-t07-audit-f1-backlog-story-status-sync/README.md) | 🟢 Done | override epic_ids_09_eid_06_audit_2026_06_08 |
| EPIC-IDS-09 | STORY-IDS-EID-07 | [t01 oidc discovery client](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-07-oidc-toolkit/task-ids-09-07-t01-oidc-discovery-client/README.md) | 🟢 Done | pkg-000020 |
| EPIC-IDS-09 | STORY-IDS-EID-07 | [t02 jwks cache refresh on unknown kid](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-07-oidc-toolkit/task-ids-09-07-t02-jwks-cache-refresh-on-unknown-kid/README.md) | 🟢 Done | pkg-000020 |
| EPIC-IDS-09 | STORY-IDS-EID-07 | [t03 id token validator rs256 claims](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-07-oidc-toolkit/task-ids-09-07-t03-id-token-validator-rs256-claims/README.md) | 🟢 Done | pkg-000020 |
| EPIC-IDS-09 | STORY-IDS-EID-07 | [t04 oidc toolkit provider runtime wire](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-07-oidc-toolkit/task-ids-09-07-t04-oidc-toolkit-provider-runtime-wire/README.md) | 🟢 Done | pkg-000020 |
| EPIC-IDS-09 | STORY-IDS-EID-07 | [t05 offline oidc toolkit mocked http tests](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-07-oidc-toolkit/task-ids-09-07-t05-offline-oidc-toolkit-mocked-http-tests/README.md) | 🟢 Done | pkg-000020 |
| EPIC-IDS-09 | STORY-IDS-EID-07 | [t06 story acceptance verification](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-07-oidc-toolkit/task-ids-09-07-t06-story-acceptance-verification/README.md) | 🟢 Done | pkg-000020 |
| EPIC-IDS-09 | STORY-IDS-EID-08 | [t01 session secret box fernet port](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-08-session-secret-box/task-ids-09-08-t01-session-secret-box-fernet-port/README.md) | 🟢 Done | pkg-000021 |
| EPIC-IDS-09 | STORY-IDS-EID-08 | [t02 eid session enc key config pilot failfast](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-08-session-secret-box/task-ids-09-08-t02-eid-session-enc-key-config-pilot-failfast/README.md) | 🟢 Done | pkg-000021 |
| EPIC-IDS-09 | STORY-IDS-EID-08 | [t03 session secret box provider runtime wire](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-08-session-secret-box/task-ids-09-08-t03-session-secret-box-provider-runtime-wire/README.md) | 🟢 Done | pkg-000021 |
| EPIC-IDS-09 | STORY-IDS-EID-08 | [t04 offline session secret box tests](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-08-session-secret-box/task-ids-09-08-t04-offline-session-secret-box-tests/README.md) | 🟢 Done | pkg-000021 |
| EPIC-IDS-09 | STORY-IDS-EID-08 | [t05 story acceptance verification](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-08-session-secret-box/task-ids-09-08-t05-story-acceptance-verification/README.md) | 🟢 Done | pkg-000021 |

## Task queue (EPIC-IDS-10)

| Epic | Story | Task README | Status | Input package |
|------|-------|-------------|--------|---------------|
| EPIC-IDS-10 | STORY-IDS-PV-01 | [t01 sms sender port dto error codes](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-01-phone-provider-backbone/task-ids-10-01-t01-sms-sender-port-dto-error-codes/README.md) | 🟢 Done | pkg-000022 |
| EPIC-IDS-10 | STORY-IDS-PV-01 | [t02 sms descriptor provider runtime](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-01-phone-provider-backbone/task-ids-10-01-t02-sms-descriptor-provider-runtime/README.md) | 🟢 Done | pkg-000022 |
| EPIC-IDS-10 | STORY-IDS-PV-01 | [t03 sms registry builder guard](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-01-phone-provider-backbone/task-ids-10-01-t03-sms-registry-builder-guard/README.md) | 🟢 Done | pkg-000022 |
| EPIC-IDS-10 | STORY-IDS-PV-01 | [t04 mock sms sender descriptor](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-01-phone-provider-backbone/task-ids-10-01-t04-mock-sms-sender-descriptor/README.md) | 🟢 Done | pkg-000022 |
| EPIC-IDS-10 | STORY-IDS-PV-01 | [t05 offline sms registry tests](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-01-phone-provider-backbone/task-ids-10-01-t05-offline-sms-registry-tests/README.md) | 🟢 Done | pkg-000022 |
| EPIC-IDS-10 | STORY-IDS-PV-01 | [t06 story acceptance verification](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-01-phone-provider-backbone/task-ids-10-01-t06-story-acceptance-verification/README.md) | 🟢 Done | pkg-000022 |
| EPIC-IDS-10 | STORY-IDS-PV-02 | [t01 sms provider config spec](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-02-provider-owned-config/task-ids-10-02-t01-sms-provider-config-spec/README.md) | 🟢 Done | pkg-000023 |
| EPIC-IDS-10 | STORY-IDS-PV-02 | [t02 appconfig phone fields sms provider validation](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-02-provider-owned-config/task-ids-10-02-t02-appconfig-phone-fields-sms-provider-validation/README.md) | 🟢 Done | pkg-000023 |
| EPIC-IDS-10 | STORY-IDS-PV-02 | [t03 e164 normalize prefix allowlist](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-02-provider-owned-config/task-ids-10-02-t03-e164-normalize-prefix-allowlist/README.md) | 🟢 Done | pkg-000023 |
| EPIC-IDS-10 | STORY-IDS-PV-02 | [t04 env example phone block](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-02-provider-owned-config/task-ids-10-02-t04-env-example-phone-block/README.md) | 🟢 Done | pkg-000023 |
| EPIC-IDS-10 | STORY-IDS-PV-02 | [t05 offline phone config e164 tests](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-02-provider-owned-config/task-ids-10-02-t05-offline-phone-config-e164-tests/README.md) | 🟢 Done | pkg-000023 |
| EPIC-IDS-10 | STORY-IDS-PV-02 | [t06 story acceptance verification](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-02-provider-owned-config/task-ids-10-02-t06-story-acceptance-verification/README.md) | 🟢 Done | pkg-000023 |
| EPIC-IDS-10 | STORY-IDS-PV-03 | [t01 phone verification session result models](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-03-otp-engine-session/task-ids-10-03-t01-phone-verification-session-result-models/README.md) | 🟢 Done | pkg-000024 |
| EPIC-IDS-10 | STORY-IDS-PV-03 | [t02 phone verification session store inmemory](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-03-otp-engine-session/task-ids-10-03-t02-phone-verification-session-store-inmemory/README.md) | 🟢 Done | pkg-000024 |
| EPIC-IDS-10 | STORY-IDS-PV-03 | [t03 otp generate session create invalidate](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-03-otp-engine-session/task-ids-10-03-t03-otp-generate-session-create-invalidate/README.md) | 🟢 Done | pkg-000024 |
| EPIC-IDS-10 | STORY-IDS-PV-03 | [t04 otp verify attempts expiry result](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-03-otp-engine-session/task-ids-10-03-t04-otp-verify-attempts-expiry-result/README.md) | 🟢 Done | pkg-000024 |
| EPIC-IDS-10 | STORY-IDS-PV-03 | [t05 offline phone otp session tests](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-03-otp-engine-session/task-ids-10-03-t05-offline-phone-otp-session-tests/README.md) | 🟢 Done | pkg-000024 |
| EPIC-IDS-10 | STORY-IDS-PV-03 | [t06 story acceptance verification](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-03-otp-engine-session/task-ids-10-03-t06-story-acceptance-verification/README.md) | 🟢 Done | pkg-000024 |
| EPIC-IDS-10 | STORY-IDS-PV-04 | [t01 profiles phone migration sql](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-04-profile-flag-migration/task-ids-10-04-t01-profiles-phone-migration-sql/README.md) | 🟢 Done | pkg-000025 |
| EPIC-IDS-10 | STORY-IDS-PV-04 | [t02 profile record phone fields contract](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-04-profile-flag-migration/task-ids-10-04-t02-profile-record-phone-fields-contract/README.md) | 🟢 Done | pkg-000025 |
| EPIC-IDS-10 | STORY-IDS-PV-04 | [t03 inmemory attach phone dedup](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-04-profile-flag-migration/task-ids-10-04-t03-inmemory-attach-phone-dedup/README.md) | 🟢 Done | pkg-000025 |
| EPIC-IDS-10 | STORY-IDS-PV-04 | [t04 supabase profile phone mapping attach](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-04-profile-flag-migration/task-ids-10-04-t04-supabase-profile-phone-mapping-attach/README.md) | 🟢 Done | pkg-000025 |
| EPIC-IDS-10 | STORY-IDS-PV-04 | [t05 me response phone fields tests](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-04-profile-flag-migration/task-ids-10-04-t05-me-response-phone-fields-tests/README.md) | 🟢 Done | pkg-000025 |
| EPIC-IDS-10 | STORY-IDS-PV-04 | [t06 story acceptance verification](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-04-profile-flag-migration/task-ids-10-04-t06-story-acceptance-verification/README.md) | 🟢 Done | pkg-000025 |
| EPIC-IDS-10 | STORY-IDS-PV-05 | [t01 phone audit event repository](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-05-verification-flow-api/task-ids-10-05-t01-phone-audit-event-repository/README.md) | 🟢 Done | pkg-000026 |
| EPIC-IDS-10 | STORY-IDS-PV-05 | [t02 phone services di wiring](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-05-verification-flow-api/task-ids-10-05-t02-phone-services-di-wiring/README.md) | 🟢 Done | pkg-000026 |
| EPIC-IDS-10 | STORY-IDS-PV-05 | [t03 handle phone request orchestrator](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-05-verification-flow-api/task-ids-10-05-t03-handle-phone-request-orchestrator/README.md) | 🟢 Done | pkg-000026 |
| EPIC-IDS-10 | STORY-IDS-PV-05 | [t04 handle phone confirm orchestrator](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-05-verification-flow-api/task-ids-10-05-t04-handle-phone-confirm-orchestrator/README.md) | 🟢 Done | pkg-000026 |
| EPIC-IDS-10 | STORY-IDS-PV-05 | [t05 asgi routes offline flow tests](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-05-verification-flow-api/task-ids-10-05-t05-asgi-routes-offline-flow-tests/README.md) | 🟢 Done | pkg-000026 |
| EPIC-IDS-10 | STORY-IDS-PV-05 | [t06 story acceptance verification](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-05-verification-flow-api/task-ids-10-05-t06-story-acceptance-verification/README.md) | 🟢 Done | pkg-000026 |
| EPIC-IDS-10 | STORY-IDS-PV-06 | [t01 telnyx settings config spec](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-06-telnyx-sms-sender/task-ids-10-06-t01-telnyx-settings-config-spec/README.md) | 🟢 Done | pkg-000027 |
| EPIC-IDS-10 | STORY-IDS-PV-06 | [t02 telnyx sms sender http send](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-06-telnyx-sms-sender/task-ids-10-06-t02-telnyx-sms-sender-http-send/README.md) | 🟢 Done | pkg-000027 |
| EPIC-IDS-10 | STORY-IDS-PV-06 | [t03 telnyx error code mapping](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-06-telnyx-sms-sender/task-ids-10-06-t03-telnyx-error-code-mapping/README.md) | 🟢 Done | pkg-000027 |
| EPIC-IDS-10 | STORY-IDS-PV-06 | [t04 telnyx descriptor registry runtime](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-06-telnyx-sms-sender/task-ids-10-06-t04-telnyx-descriptor-registry-runtime/README.md) | 🟢 Done | pkg-000027 |
| EPIC-IDS-10 | STORY-IDS-PV-06 | [t05 offline telnyx sender tests](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-06-telnyx-sms-sender/task-ids-10-06-t05-offline-telnyx-sender-tests/README.md) | 🟢 Done | pkg-000027 |
| EPIC-IDS-10 | STORY-IDS-PV-06 | [t06 story acceptance verification](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-06-telnyx-sms-sender/task-ids-10-06-t06-story-acceptance-verification/README.md) | 🟢 Done | pkg-000027 |
| EPIC-IDS-10 | STORY-IDS-PV-06 | [t07 audit f3 sms runtime merged env source](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-06-telnyx-sms-sender/task-ids-10-06-t07-audit-f3-sms-runtime-merged-env-source/README.md) | 🟢 Done | override epic_ids_10_pv_06_audit_2026_06_11 |
| EPIC-IDS-10 | STORY-IDS-PV-06 | [t08 audit f1 backlog epic alias doc sync](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-06-telnyx-sms-sender/task-ids-10-06-t08-audit-f1-backlog-epic-alias-doc-sync/README.md) | 🟢 Done | override epic_ids_10_pv_06_audit_2026_06_11 |
| EPIC-IDS-10 | STORY-IDS-PV-06 | [t09 audit f2 bullrun pytest count sync](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-06-telnyx-sms-sender/task-ids-10-06-t09-audit-f2-bullrun-pytest-count-sync/README.md) | 🟢 Done | override epic_ids_10_pv_06_audit_2026_06_11 |
| EPIC-IDS-10 | STORY-IDS-PV-07 | [t01 session delivery fields and message id persist](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-07-telnyx-delivery-webhook/task-ids-10-07-t01-session-delivery-fields-and-message-id-persist/README.md) | 🟢 Done | pkg-000028 |
| EPIC-IDS-10 | STORY-IDS-PV-07 | [t02 telnyx webhook signature verifier](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-07-telnyx-delivery-webhook/task-ids-10-07-t02-telnyx-webhook-signature-verifier/README.md) | 🟢 Done | pkg-000028 |
| EPIC-IDS-10 | STORY-IDS-PV-07 | [t03 delivery status ingest idempotency](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-07-telnyx-delivery-webhook/task-ids-10-07-t03-delivery-status-ingest-idempotency/README.md) | 🟢 Done | pkg-000028 |
| EPIC-IDS-10 | STORY-IDS-PV-07 | [t04 webhook handler route and audit](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-07-telnyx-delivery-webhook/task-ids-10-07-t04-webhook-handler-route-and-audit/README.md) | 🟢 Done | pkg-000028 |
| EPIC-IDS-10 | STORY-IDS-PV-07 | [t05 offline telnyx webhook tests](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-07-telnyx-delivery-webhook/task-ids-10-07-t05-offline-telnyx-webhook-tests/README.md) | 🟢 Done | pkg-000028 |
| EPIC-IDS-10 | STORY-IDS-PV-07 | [t06 story acceptance verification](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-07-telnyx-delivery-webhook/task-ids-10-07-t06-story-acceptance-verification/README.md) | 🟢 Done | pkg-000028 |
| EPIC-IDS-10 | STORY-IDS-PV-09 | [t01 phone persistence migration sql](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-09-durable-phone-persistence/task-ids-10-09-t01-phone-persistence-migration-sql/README.md) | 🟢 Done | pkg-000039 |
| EPIC-IDS-10 | STORY-IDS-PV-09 | [t02 supabase phone verification session store](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-09-durable-phone-persistence/task-ids-10-09-t02-supabase-phone-verification-session-store/README.md) | 🟢 Done | pkg-000039 |
| EPIC-IDS-10 | STORY-IDS-PV-09 | [t03 supabase phone audit log repository](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-09-durable-phone-persistence/task-ids-10-09-t03-supabase-phone-audit-log-repository/README.md) | 🟢 Done | pkg-000039 |
| EPIC-IDS-10 | STORY-IDS-PV-09 | [t04 di phone store backend selection](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-09-durable-phone-persistence/task-ids-10-09-t04-di-phone-store-backend-selection/README.md) | 🟢 Done | pkg-000039 |
| EPIC-IDS-10 | STORY-IDS-PV-09 | [t05 bootstrap full init parity](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-09-durable-phone-persistence/task-ids-10-09-t05-bootstrap-full-init-parity/README.md) | 🟢 Done | pkg-000039 |
| EPIC-IDS-10 | STORY-IDS-PV-09 | [t06 offline phone durability regression tests](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-09-durable-phone-persistence/task-ids-10-09-t06-offline-phone-durability-regression-tests/README.md) | 🟢 Done | pkg-000039 |
| EPIC-IDS-10 | STORY-IDS-PV-09 | [t07 story acceptance verification](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-09-durable-phone-persistence/task-ids-10-09-t07-story-acceptance-verification/README.md) | 🟢 Done | pkg-000039 |
| EPIC-IDS-10 | STORY-IDS-PV-10 | [t01 file sms sender core](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/task-ids-10-10-t01-file-sms-sender-core/README.md) | 🟢 Done | pkg-000041 |
| EPIC-IDS-10 | STORY-IDS-PV-10 | [t02 file sms config spec](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/task-ids-10-10-t02-file-sms-config-spec/README.md) | 🟢 Done | pkg-000041 |
| EPIC-IDS-10 | STORY-IDS-PV-10 | [t03 file descriptor registry runtime](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/task-ids-10-10-t03-file-descriptor-registry-runtime/README.md) | 🟢 Done | pkg-000041 |
| EPIC-IDS-10 | STORY-IDS-PV-10 | [t04 pilot file provider fail fast](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/task-ids-10-10-t04-pilot-file-provider-fail-fast/README.md) | 🟢 Done | pkg-000041 |
| EPIC-IDS-10 | STORY-IDS-PV-10 | [t05 dev hygiene gitignore env example](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/task-ids-10-10-t05-dev-hygiene-gitignore-env-example/README.md) | 🟢 Done | pkg-000041 |
| EPIC-IDS-10 | STORY-IDS-PV-10 | [t06 offline file sms tests](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/task-ids-10-10-t06-offline-file-sms-tests/README.md) | 🟢 Done | pkg-000041 |
| EPIC-IDS-10 | STORY-IDS-PV-10 | [t07 story acceptance verification](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/task-ids-10-10-t07-story-acceptance-verification/README.md) | 🟢 Done | pkg-000041 |
| EPIC-IDS-10 | STORY-IDS-PV-10 | [t08 audit f1 pipeline story timestamp example sync](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/task-ids-10-10-t08-audit-f1-pipeline-story-timestamp-example-sync/README.md) | 🟢 Done | override epic_ids_10_pv_10_audit_2026_06_28 |

## Task queue (EPIC-IDS-11)

| Epic | Story | Task | Status | pkg |
|------|-------|------|--------|-----|
| EPIC-IDS-11 | STORY-IDS-OAUTH-01 | [t01 authorization request store and contracts](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-01-oauth-server-endpoints/task-ids-11-01-t01-authorization-request-store-and-contracts/README.md) | 🟢 Done | pkg-000029 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-01 | [t02 rfc6749 errors scope validation client secret](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-01-oauth-server-endpoints/task-ids-11-01-t02-rfc6749-errors-scope-validation-client-secret/README.md) | 🟢 Done | pkg-000029 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-01 | [t03 oauth authorize handler and route](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-01-oauth-server-endpoints/task-ids-11-01-t03-oauth-authorize-handler-and-route/README.md) | 🟢 Done | pkg-000029 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-01 | [t04 oauth complete token handlers and routes](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-01-oauth-server-endpoints/task-ids-11-01-t04-oauth-complete-token-handlers-and-routes/README.md) | 🟢 Done | pkg-000029 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-01 | [t05 oauth access token bearer dependency](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-01-oauth-server-endpoints/task-ids-11-01-t05-oauth-access-token-bearer-dependency/README.md) | 🟢 Done | pkg-000029 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-01 | [t06 offline oauth server tests](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-01-oauth-server-endpoints/task-ids-11-01-t06-offline-oauth-server-tests/README.md) | 🟢 Done | pkg-000029 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-01 | [t07 story acceptance verification](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-01-oauth-server-endpoints/task-ids-11-01-t07-story-acceptance-verification/README.md) | 🟢 Done | pkg-000029 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-02 | [t01 service api token config](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-02-introspection-and-service-token/task-ids-11-02-t01-service-api-token-config/README.md) | 🟢 Done | pkg-000030 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-02 | [t02 service token auth dependency](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-02-introspection-and-service-token/task-ids-11-02-t02-service-token-auth-dependency/README.md) | 🟢 Done | pkg-000030 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-02 | [t03 oauth introspection handler](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-02-introspection-and-service-token/task-ids-11-02-t03-oauth-introspection-handler/README.md) | 🟢 Done | pkg-000030 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-02 | [t04 oauth introspect route](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-02-introspection-and-service-token/task-ids-11-02-t04-oauth-introspect-route/README.md) | 🟢 Done | pkg-000030 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-02 | [t05 offline introspection tests](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-02-introspection-and-service-token/task-ids-11-02-t05-offline-introspection-tests/README.md) | 🟢 Done | pkg-000030 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-02 | [t06 story acceptance verification](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-02-introspection-and-service-token/task-ids-11-02-t06-story-acceptance-verification/README.md) | 🟢 Done | pkg-000030 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-02 | [t07 audit f2 epic oauth backlog index sync](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-02-introspection-and-service-token/task-ids-11-02-t07-audit-f2-epic-oauth-backlog-index-sync/README.md) | 🟢 Done | override epic_ids_11_oauth_02_audit_2026_06_24 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-02 | [t08 audit f3 runtime docs introspection drift sync](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-02-introspection-and-service-token/task-ids-11-02-t08-audit-f3-runtime-docs-introspection-drift-sync/README.md) | 🟢 Done | override epic_ids_11_oauth_02_audit_2026_06_24 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-02 | [t09 audit f4 pilot service api token fail fast](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-02-introspection-and-service-token/task-ids-11-02-t09-audit-f4-pilot-service-api-token-fail-fast/README.md) | 🟢 Done | override epic_ids_11_oauth_02_audit_2026_06_24 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-03 | [t01 oauth supabase migration sql](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-03-persistent-token-store-supabase/task-ids-11-03-t01-oauth-supabase-migration-sql/README.md) | 🟢 Done | pkg-000033 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-03 | [t02 supabase authorization request store](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-03-persistent-token-store-supabase/task-ids-11-03-t02-supabase-authorization-request-store/README.md) | 🟢 Done | pkg-000033 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-03 | [t03 supabase oauth token service](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-03-persistent-token-store-supabase/task-ids-11-03-t03-supabase-oauth-token-service/README.md) | 🟢 Done | pkg-000033 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-03 | [t04 di oauth store backend selection](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-03-persistent-token-store-supabase/task-ids-11-03-t04-di-oauth-store-backend-selection/README.md) | 🟢 Done | pkg-000033 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-03 | [t05 offline supabase oauth store tests](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-03-persistent-token-store-supabase/task-ids-11-03-t05-offline-supabase-oauth-store-tests/README.md) | 🟢 Done | pkg-000033 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-03 | [t06 durability and stateless jwt tests](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-03-persistent-token-store-supabase/task-ids-11-03-t06-durability-and-stateless-jwt-tests/README.md) | 🟢 Done | pkg-000033 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-03 | [t07 story acceptance verification](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-03-persistent-token-store-supabase/task-ids-11-03-t07-story-acceptance-verification/README.md) | 🟢 Done | pkg-000033 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-04 | [t01 oauth request context schema](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-04-verify-gate-and-verification-required/task-ids-11-04-t01-oauth-request-context-schema/README.md) | 🟢 Done | pkg-000034 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-04 | [t02 oauth authorize relay handlers](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-04-verify-gate-and-verification-required/task-ids-11-04-t02-oauth-authorize-relay-handlers/README.md) | 🟢 Done | pkg-000034 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-04 | [t03 oauth verify gate phone branch](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-04-verify-gate-and-verification-required/task-ids-11-04-t03-oauth-verify-gate-phone-branch/README.md) | 🟢 Done | pkg-000034 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-04 | [t04 verification required contract](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-04-verify-gate-and-verification-required/task-ids-11-04-t04-verification-required-contract/README.md) | 🟢 Done | pkg-000034 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-04 | [t05 verify need vs sms error http mapping](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-04-verify-gate-and-verification-required/task-ids-11-04-t05-verify-need-vs-sms-error-http-mapping/README.md) | 🟢 Done | pkg-000034 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-04 | [t06 offline oauth verify gate tests](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-04-verify-gate-and-verification-required/task-ids-11-04-t06-offline-oauth-verify-gate-tests/README.md) | 🟢 Done | pkg-000034 |
| EPIC-IDS-11 | STORY-IDS-OAUTH-04 | [t07 story acceptance verification](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-04-verify-gate-and-verification-required/task-ids-11-04-t07-story-acceptance-verification/README.md) | 🟢 Done | pkg-000034 |

## Task queue (EPIC-IDS-13)

| Epic | Story | Task | Status | pkg |
|------|-------|------|--------|-----|
| EPIC-IDS-13 | DOC-IDS-ONB-01 | [t01 lazy gate doc gap audit](./epics/EPIC-IDS-13-onboarding/stories/DOC-IDS-ONB-01-lazy-phone-gate-contract/task-ids-13-01-t01-lazy-gate-doc-gap-audit/README.md) | 🟢 Done | pkg-000040 |
| EPIC-IDS-13 | DOC-IDS-ONB-01 | [t02 gateway lazy phone gate section](./epics/EPIC-IDS-13-onboarding/stories/DOC-IDS-ONB-01-lazy-phone-gate-contract/task-ids-13-01-t02-gateway-lazy-phone-gate-section/README.md) | 🟢 Done | pkg-000040 |
| EPIC-IDS-13 | DOC-IDS-ONB-01 | [t03 ui lazy verify screen expectation](./epics/EPIC-IDS-13-onboarding/stories/DOC-IDS-ONB-01-lazy-phone-gate-contract/task-ids-13-01-t03-ui-lazy-verify-screen-expectation/README.md) | 🟢 Done | pkg-000040 |
| EPIC-IDS-13 | DOC-IDS-ONB-01 | [t04 pv05 runbook crosslinks sequence](./epics/EPIC-IDS-13-onboarding/stories/DOC-IDS-ONB-01-lazy-phone-gate-contract/task-ids-13-01-t04-pv05-runbook-crosslinks-sequence/README.md) | 🟢 Done | pkg-000040 |
| EPIC-IDS-13 | DOC-IDS-ONB-01 | [t05 story acceptance verification](./epics/EPIC-IDS-13-onboarding/stories/DOC-IDS-ONB-01-lazy-phone-gate-contract/task-ids-13-01-t05-story-acceptance-verification/README.md) | 🟢 Done | pkg-000040 |
| EPIC-IDS-13 | STORY-IDS-ONB-01 | [t01 me response email and email_verified](./epics/EPIC-IDS-13-onboarding/stories/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm/task-ids-13-02-t01-me-response-email-and-email-verified/README.md) | 🟢 Done | pkg-000045 |
| EPIC-IDS-13 | STORY-IDS-ONB-01 | [t02 confirm email runbook and me api docs](./epics/EPIC-IDS-13-onboarding/stories/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm/task-ids-13-02-t02-confirm-email-runbook-and-me-api-docs/README.md) | 🟢 Done | pkg-000045 |
| EPIC-IDS-13 | STORY-IDS-ONB-01 | [t03 me profile offline tests email fields](./epics/EPIC-IDS-13-onboarding/stories/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm/task-ids-13-02-t03-me-profile-offline-tests-email-fields/README.md) | 🟢 Done | pkg-000045 |
| EPIC-IDS-13 | STORY-IDS-ONB-01 | [t04 story acceptance verification](./epics/EPIC-IDS-13-onboarding/stories/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm/task-ids-13-02-t04-story-acceptance-verification/README.md) | 🟢 Done | pkg-000045 |
| EPIC-IDS-13 | STORY-IDS-ONB-01 | [t05 audit f2 email_verified oauth semantics docs](./epics/EPIC-IDS-13-onboarding/stories/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm/task-ids-13-02-t05-audit-f2-email-verified-oauth-semantics-docs/README.md) | 🟢 Done | override epic_ids_13_onb_01_audit_2026_07_24 |

## Task queue (EPIC-IDS-12)

| Epic | Story | Task | Status | pkg |
|------|-------|------|--------|-----|
| EPIC-IDS-12 | STORY-IDS-SEC-01 | [t01 rate limit config schema](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01-rate-limiting/task-ids-12-01-t01-rate-limit-config-schema/README.md) | 🟢 Done | pkg-000035 |
| EPIC-IDS-12 | STORY-IDS-SEC-01 | [t02 in-memory rate limiter store](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01-rate-limiting/task-ids-12-01-t02-in-memory-rate-limiter-store/README.md) | 🟢 Done | pkg-000035 |
| EPIC-IDS-12 | STORY-IDS-SEC-01 | [t03 rate limit dependency 429 envelope](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01-rate-limiting/task-ids-12-01-t03-rate-limit-dependency-429-envelope/README.md) | 🟢 Done | pkg-000035 |
| EPIC-IDS-12 | STORY-IDS-SEC-01 | [t04 sensitive routes wiring](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01-rate-limiting/task-ids-12-01-t04-sensitive-routes-wiring/README.md) | 🟢 Done | pkg-000035 |
| EPIC-IDS-12 | STORY-IDS-SEC-01 | [t05 otp cooldown coexistence policy](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01-rate-limiting/task-ids-12-01-t05-otp-cooldown-coexistence-policy/README.md) | 🟢 Done | pkg-000035 |
| EPIC-IDS-12 | STORY-IDS-SEC-01 | [t06 offline rate limit tests](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01-rate-limiting/task-ids-12-01-t06-offline-rate-limit-tests/README.md) | 🟢 Done | pkg-000035 |
| EPIC-IDS-12 | STORY-IDS-SEC-01 | [t07 story acceptance verification](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01-rate-limiting/task-ids-12-01-t07-story-acceptance-verification/README.md) | 🟢 Done | pkg-000035 |
| EPIC-IDS-12 | STORY-IDS-SEC-01 | [t08 audit f1 backlog sec-01 story sync](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01-rate-limiting/task-ids-12-01-t08-audit-f1-backlog-sec-01-story-sync/README.md) | 🟢 Done | override epic_ids_12_sec_01_audit_2026_06_26 |
| EPIC-IDS-12 | STORY-IDS-SEC-01 | [t09 audit f2 callback ip xff trusted proxy](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01-rate-limiting/task-ids-12-01-t09-audit-f2-callback-ip-xff-trusted-proxy/README.md) | 🟢 Done | override epic_ids_12_sec_01_audit_2026_06_26 |
| EPIC-IDS-12 | STORY-IDS-SEC-01b | [t01 phone request rate limit config schema](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01b-phone-request-http-rate-limit/task-ids-12-02-t01-phone-request-rate-limit-config-schema/README.md) | 🟢 Done | pkg-000036 |
| EPIC-IDS-12 | STORY-IDS-SEC-01b | [t02 phone request rate limit dependency](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01b-phone-request-http-rate-limit/task-ids-12-02-t02-phone-request-rate-limit-dependency/README.md) | 🟢 Done | pkg-000036 |
| EPIC-IDS-12 | STORY-IDS-SEC-01b | [t03 phone request route wiring](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01b-phone-request-http-rate-limit/task-ids-12-02-t03-phone-request-route-wiring/README.md) | 🟢 Done | pkg-000036 |
| EPIC-IDS-12 | STORY-IDS-SEC-01b | [t04 cooldown http window coexistence policy](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01b-phone-request-http-rate-limit/task-ids-12-02-t04-cooldown-http-window-coexistence-policy/README.md) | 🟢 Done | pkg-000036 |
| EPIC-IDS-12 | STORY-IDS-SEC-01b | [t05 offline phone request rate limit tests](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01b-phone-request-http-rate-limit/task-ids-12-02-t05-offline-phone-request-rate-limit-tests/README.md) | 🟢 Done | pkg-000036 |
| EPIC-IDS-12 | STORY-IDS-SEC-01b | [t06 story acceptance verification](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01b-phone-request-http-rate-limit/task-ids-12-02-t06-story-acceptance-verification/README.md) | 🟢 Done | pkg-000036 |
| EPIC-IDS-12 | STORY-IDS-SEC-02 | [t01 phone audit event ip ua model fields](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-02-audit-ip-ua-hashing/task-ids-12-03-t01-phone-audit-event-ip-ua-model-fields/README.md) | 🟢 Done | pkg-000037 |
| EPIC-IDS-12 | STORY-IDS-SEC-02 | [t02 audit ip ua hmac hashing helper](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-02-audit-ip-ua-hashing/task-ids-12-03-t02-audit-ip-ua-hmac-hashing-helper/README.md) | 🟢 Done | pkg-000037 |
| EPIC-IDS-12 | STORY-IDS-SEC-02 | [t03 eid audit request context wiring](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-02-audit-ip-ua-hashing/task-ids-12-03-t03-eid-audit-request-context-wiring/README.md) | 🟢 Done | pkg-000037 |
| EPIC-IDS-12 | STORY-IDS-SEC-02 | [t04 phone audit request context wiring](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-02-audit-ip-ua-hashing/task-ids-12-03-t04-phone-audit-request-context-wiring/README.md) | 🟢 Done | pkg-000037 |
| EPIC-IDS-12 | STORY-IDS-SEC-02 | [t05 offline audit ip ua hash no pii tests](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-02-audit-ip-ua-hashing/task-ids-12-03-t05-offline-audit-ip-ua-hash-no-pii-tests/README.md) | 🟢 Done | pkg-000037 |
| EPIC-IDS-12 | STORY-IDS-SEC-02 | [t06 story acceptance verification](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-02-audit-ip-ua-hashing/task-ids-12-03-t06-story-acceptance-verification/README.md) | 🟢 Done | pkg-000037 |
| EPIC-IDS-12 | STORY-IDS-SEC-03 | [t01 live supabase jwt aud decision record](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-03-jwt-validation-hardening/task-ids-12-04-t01-live-supabase-jwt-aud-decision-record/README.md) | 🟢 Done | pkg-000038 |
| EPIC-IDS-12 | STORY-IDS-SEC-03 | [t02 confirm octkey import form live token](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-03-jwt-validation-hardening/task-ids-12-04-t02-confirm-octkey-import-form-live-token/README.md) | 🟢 Done | pkg-000038 |
| EPIC-IDS-12 | STORY-IDS-SEC-03 | [t03 aud claim registry or spec waiver](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-03-jwt-validation-hardening/task-ids-12-04-t03-aud-claim-registry-or-spec-waiver/README.md) | 🟢 Done | pkg-000038 |
| EPIC-IDS-12 | STORY-IDS-SEC-03 | [t04 offline jwt aud key regression tests](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-03-jwt-validation-hardening/task-ids-12-04-t04-offline-jwt-aud-key-regression-tests/README.md) | 🟢 Done | pkg-000038 |
| EPIC-IDS-12 | STORY-IDS-SEC-03 | [t05 spec 09 g5 gap closure docs](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-03-jwt-validation-hardening/task-ids-12-04-t05-spec-09-g5-gap-closure-docs/README.md) | 🟢 Done | pkg-000038 |
| EPIC-IDS-12 | STORY-IDS-SEC-03 | [t06 story acceptance verification](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-03-jwt-validation-hardening/task-ids-12-04-t06-story-acceptance-verification/README.md) | 🟢 Done | pkg-000038 |
| EPIC-IDS-12 | STORY-IDS-SEC-04 | [t01 service role boundary docs sync](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/task-ids-12-05-t01-service-role-boundary-docs-sync/README.md) | 🟢 Done | pkg-000043 · audit F1 closed t06 |
| EPIC-IDS-12 | STORY-IDS-SEC-04 | [t02 no expose service role guard tests](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/task-ids-12-05-t02-no-expose-service-role-guard-tests/README.md) | 🟢 Done | pkg-000043 · audit F2 closed t07 |
| EPIC-IDS-12 | STORY-IDS-SEC-04 | [t03 service role rotation runbook](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/task-ids-12-05-t03-service-role-rotation-runbook/README.md) | 🟢 Done | pkg-000043 |
| EPIC-IDS-12 | STORY-IDS-SEC-04 | [t04 spa sec 01 coordination checklist](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/task-ids-12-05-t04-spa-sec-01-coordination-checklist/README.md) | 🟢 Done | pkg-000043 · F3 waived operator manual |
| EPIC-IDS-12 | STORY-IDS-SEC-04 | [t05 story acceptance verification](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/task-ids-12-05-t05-story-acceptance-verification/README.md) | 🟢 Done | pkg-000043 · audit 2026-07-09 |
| EPIC-IDS-12 | STORY-IDS-SEC-04 | [t06 audit f1 platform wording separation sync](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/task-ids-12-05-t06-audit-f1-platform-wording-separation-sync/README.md) | 🟢 Done | override epic_ids_12_sec_04_audit_2026_07_09 |
| EPIC-IDS-12 | STORY-IDS-SEC-04 | [t07 audit f2 no expose guard depth](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/task-ids-12-05-t07-audit-f2-no-expose-guard-depth/README.md) | 🟢 Done | override epic_ids_12_sec_04_audit_2026_07_09 |
| EPIC-IDS-12 | STORY-IDS-SEC-06 | [t01 change propagation audit](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t01-change-propagation-audit/README.md) | 🟢 Done | pkg-000042 |
| EPIC-IDS-12 | STORY-IDS-SEC-06 | [t02 jwks only validator](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t02-jwks-only-validator/README.md) | 🟢 Done | pkg-000042 |
| EPIC-IDS-12 | STORY-IDS-SEC-06 | [t03 jwks cache di wiring](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t03-jwks-cache-di-wiring/README.md) | 🟢 Done | pkg-000042 |
| EPIC-IDS-12 | STORY-IDS-SEC-06 | [t04 remove supabase jwt secret](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t04-remove-supabase-jwt-secret/README.md) | 🟢 Done | pkg-000042 |
| EPIC-IDS-12 | STORY-IDS-SEC-06 | [t05 es256 mock jwks test harness](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t05-es256-mock-jwks-test-harness/README.md) | 🟢 Done | pkg-000042 |
| EPIC-IDS-12 | STORY-IDS-SEC-06 | [t06 offline jwks validator tests](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t06-offline-jwks-validator-tests/README.md) | 🟢 Done | pkg-000042 |
| EPIC-IDS-12 | STORY-IDS-SEC-06 | [t07 jwks only docs sync](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t07-jwks-only-docs-sync/README.md) | 🟢 Done | pkg-000042 |
| EPIC-IDS-12 | STORY-IDS-SEC-06 | [t08 story acceptance verification](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t08-story-acceptance-verification/README.md) | 🟢 Done | pkg-000042 |
| EPIC-IDS-12 | STORY-IDS-SEC-06 | [t09 audit f1 jwks httpx client lifespan close](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t09-audit-f1-jwks-httpx-client-lifespan-close/README.md) | 🟢 Done | override epic_ids_12_sec_06_audit_2026_07_04 |
| EPIC-IDS-12 | STORY-IDS-SEC-06 | [t10 audit f2 live integration jwks only cleanup](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t10-audit-f2-live-integration-jwks-only-cleanup/README.md) | 🟢 Done | override epic_ids_12_sec_06_audit_2026_07_04 |

## Stories (EPIC-IDS-07)

| Story key | Anchor | Status |
|-----------|--------|--------|
| STORY-IDS-AUTHCORE-01-profile-and-me | [story](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/STORY-IDS-AUTHCORE-01-profile-and-me.md) | 🟢 Done |
| STORY-IDS-AUTHCORE-02-me-account-fields | [story](./epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-02-me-account-fields/STORY-IDS-AUTHCORE-02-me-account-fields.md) | 🟢 Done (pkg-000044) |

## Stories (EPIC-IDS-13)

| Story key | Anchor | Status |
|-----------|--------|--------|
| DOC-IDS-ONB-01-lazy-phone-gate-contract | [story](./epics/EPIC-IDS-13-onboarding/stories/DOC-IDS-ONB-01-lazy-phone-gate-contract/DOC-IDS-ONB-01-lazy-phone-gate-contract.md) | 🟢 Done |
| STORY-IDS-ONB-01-email-in-me-and-supabase-confirm | [story](./epics/EPIC-IDS-13-onboarding/stories/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md) | 🟢 Done (pkg-000045) |

## Stories (EPIC-IDS-12)

| Story key | Anchor | Status |
|-----------|--------|--------|
| STORY-IDS-SEC-01-rate-limiting | [story](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01-rate-limiting/STORY-IDS-SEC-01-rate-limiting.md) | 🟢 Done |
| STORY-IDS-SEC-01b-phone-request-http-rate-limit | [story](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01b-phone-request-http-rate-limit/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md) | 🟢 Done |
| STORY-IDS-SEC-02-audit-ip-ua-hashing | [story](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-02-audit-ip-ua-hashing/STORY-IDS-SEC-02-audit-ip-ua-hashing.md) | 🟢 Done |
| STORY-IDS-SEC-03-jwt-validation-hardening | [story](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-03-jwt-validation-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md) | 🟢 Done |
| STORY-IDS-SEC-04-service-role-isolation | [story](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/STORY-IDS-SEC-04-service-role-isolation.md) | 🟢 Done (pkg-000043 + audit override; rotation operator manual) |
| STORY-IDS-SEC-06-supabase-jwks-es256-hardening | [story](./epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md) | 🟢 Done |

## Stories (EPIC-IDS-11)

| Story key | Anchor | Status |
|-----------|--------|--------|
| STORY-IDS-OAUTH-01-oauth-server-endpoints | [story](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-01-oauth-server-endpoints/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) | 🟢 Done |
| STORY-IDS-OAUTH-02-introspection-and-service-token | [story](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-02-introspection-and-service-token/STORY-IDS-OAUTH-02-introspection-and-service-token.md) | 🟢 Done |
| STORY-IDS-OAUTH-03-persistent-token-store-supabase | [story](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-03-persistent-token-store-supabase/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) | 🟢 Done |
| STORY-IDS-OAUTH-04-verify-gate-and-verification-required | [story](./epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-04-verify-gate-and-verification-required/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md) | 🟢 Done |

## Stories (EPIC-IDS-10)

| Story key | Anchor | Status |
|-----------|--------|--------|
| STORY-IDS-PV-01-phone-provider-backbone | [story](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-01-phone-provider-backbone/STORY-IDS-PV-01-phone-provider-backbone.md) | 🟢 Done |
| STORY-IDS-PV-02-provider-owned-config | [story](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-02-provider-owned-config/STORY-IDS-PV-02-provider-owned-config.md) | 🟢 Done |
| STORY-IDS-PV-03-otp-engine-session | [story](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-03-otp-engine-session/STORY-IDS-PV-03-otp-engine-session.md) | 🟢 Done |
| STORY-IDS-PV-04-profile-flag-migration | [story](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-04-profile-flag-migration/STORY-IDS-PV-04-profile-flag-migration.md) | 🟢 Done |
| STORY-IDS-PV-05-verification-flow-api | [story](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-05-verification-flow-api/STORY-IDS-PV-05-verification-flow-api.md) | 🟢 Done |
| STORY-IDS-PV-06-telnyx-sms-sender | [story](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-06-telnyx-sms-sender/STORY-IDS-PV-06-telnyx-sms-sender.md) | 🟢 Done |
| STORY-IDS-PV-07-telnyx-delivery-webhook | [story](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-07-telnyx-delivery-webhook/STORY-IDS-PV-07-telnyx-delivery-webhook.md) | 🟢 Done |
| STORY-IDS-PV-09-durable-phone-persistence | [story](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-09-durable-phone-persistence/STORY-IDS-PV-09-durable-phone-persistence.md) | 🟢 Done |
| STORY-IDS-PV-10-file-sms-sink-dev | [story](./epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/STORY-IDS-PV-10-file-sms-sink-dev.md) | 🟢 Done |

## Stories (EPIC-IDS-09)

| Story key | Anchor | Status |
|-----------|--------|--------|
| STORY-IDS-EID-01-eid-verification-flow | [story](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-01-eid-verification-flow/STORY-IDS-EID-01-eid-verification-flow.md) | 🟢 Done |
| STORY-IDS-EID-03-provider-plugin-backbone | [story](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md) | 🟢 Done |
| STORY-IDS-EID-04-provider-owned-config | [story](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-04-provider-owned-config/STORY-IDS-EID-04-provider-owned-config.md) | 🟢 Done |
| STORY-IDS-EID-05-canonical-provider-contract | [story](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-05-canonical-provider-contract/STORY-IDS-EID-05-canonical-provider-contract.md) | 🟢 Done |
| STORY-IDS-EID-06-browser-callback-redirect | [story](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-06-browser-callback-redirect/STORY-IDS-EID-06-browser-callback-redirect.md) | 🟢 Done |
| STORY-IDS-EID-07-oidc-toolkit | [story](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-07-oidc-toolkit/STORY-IDS-EID-07-oidc-toolkit.md) | 🟢 Done |
| STORY-IDS-EID-08-session-secret-box | [story](./epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-08-session-secret-box/STORY-IDS-EID-08-session-secret-box.md) | 🟢 Done |

## Task queue (EPIC-IDS-08)

| Epic | Story | Task README | Status | Input package |
|------|-------|-------------|--------|---------------|
| EPIC-IDS-08 | STORY-IDS-CLEANUP-01 | [t01 remove story drafts required tables](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity/task-ids-08-01-t01-remove-story-drafts-required-tables/README.md) | 🟢 Done | pkg-000011 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-01 | [t02 remove story http routes](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity/task-ids-08-01-t02-remove-story-http-routes/README.md) | 🟢 Done | pkg-000011 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-01 | [t03 remove storydraft domain and repos](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity/task-ids-08-01-t03-remove-storydraft-domain-and-repos/README.md) | 🟢 Done | pkg-000011 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-01 | [t04 remove core stories package](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity/task-ids-08-01-t04-remove-core-stories-package/README.md) | 🟢 Done | pkg-000011 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-01 | [t05 migration fate and req15 deprecated](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity/task-ids-08-01-t05-migration-fate-and-req15-deprecated/README.md) | 🟢 Done | pkg-000011 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-01 | [t06 story related tests cleanup](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity/task-ids-08-01-t06-story-related-tests-cleanup/README.md) | 🟢 Done | pkg-000011 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-01 | [t07 story acceptance verification](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity/task-ids-08-01-t07-story-acceptance-verification/README.md) | 🟢 Done | pkg-000011 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-01 | [t08 audit f1 runbook story drafts align](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity/task-ids-08-01-t08-audit-f1-runbook-story-drafts-migration-align/README.md) | 🟢 Done | pkg-000012 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-01 | [t09 audit f2 story migration tests residual](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity/task-ids-08-01-t09-audit-f2-story-migration-tests-residual/README.md) | 🟢 Done | pkg-000012 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-01 | [t10 audit f3 remove empty stories directory](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity/task-ids-08-01-t10-audit-f3-remove-empty-stories-directory/README.md) | 🟢 Done | pkg-000012 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-01 | [t11 audit f4 backlog story status sync](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity/task-ids-08-01-t11-audit-f4-backlog-story-status-sync/README.md) | 🟢 Done | pkg-000012 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-02 | [t01 owner decisions placeholders e17 e22](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/README.md) | 🟢 Done | pkg-000013 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-02 | [t02 allowed return urls e17](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/task-ids-08-02-t02-allowed-return-urls-e17/README.md) | 🟢 Done | pkg-000013 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-02 | [t03 remove stub bearer token auth e18](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/task-ids-08-02-t03-remove-stub-bearer-token-auth-e18/README.md) | 🟢 Done | pkg-000013 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-02 | [t04 code verifier encryption key e20](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/task-ids-08-02-t04-code-verifier-encryption-key-e20/README.md) | 🟢 Done | pkg-000013 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-02 | [t05 idempotency resolver e21](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/task-ids-08-02-t05-idempotency-resolver-e21/README.md) | 🟢 Done | pkg-000013 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-02 | [t06 empty layer packages e22](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/task-ids-08-02-t06-empty-layer-packages-e22/README.md) | 🟢 Done | pkg-000013 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-02 | [t07 story acceptance verification](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/task-ids-08-02-t07-story-acceptance-verification/README.md) | 🟢 Done | pkg-000013 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-02 | [t08 audit f1 return url enforcement](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/task-ids-08-02-t08-audit-f1-return-url-validator-enforcement/README.md) | 🟢 Done | override epic_ids_08_cleanup_02_audit_2026_06_05 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-02 | [t09 audit f2 empty layer dirs doc](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/task-ids-08-02-t09-audit-f2-empty-layer-directories-doc-align/README.md) | 🟢 Done | override epic_ids_08_cleanup_02_audit_2026_06_05 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-02 | [t10 audit f3 idempotency doc drift](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/task-ids-08-02-t10-audit-f3-idempotency-runtime-doc-drift/README.md) | 🟢 Done | override epic_ids_08_cleanup_02_audit_2026_06_05 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-03 | [t01 req08 req02 migration count doc3](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-03-doc-drift/task-ids-08-03-t01-req08-req02-migration-count-doc3/README.md) | 🟢 Done | pkg-000014 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-03 | [t02 env example authentigate redirect cfg3](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-03-doc-drift/task-ids-08-03-t02-env-example-authentigate-redirect-cfg3/README.md) | 🟢 Done | pkg-000014 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-03 | [t03 req15 deprecated verify doc1](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-03-doc-drift/task-ids-08-03-t03-req15-deprecated-verify-doc1/README.md) | 🟢 Done | pkg-000014 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-03 | [t04 req02 req03 gateway direction sync](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-03-doc-drift/task-ids-08-03-t04-req02-req03-gateway-direction-sync/README.md) | 🟢 Done | pkg-000014 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-03 | [t05 requirements runtime docs crosscheck ac4](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-03-doc-drift/task-ids-08-03-t05-requirements-runtime-docs-crosscheck-ac4/README.md) | 🟢 Done | pkg-000014 |
| EPIC-IDS-08 | STORY-IDS-CLEANUP-03 | [t06 story acceptance verification](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-03-doc-drift/task-ids-08-03-t06-story-acceptance-verification/README.md) | 🟢 Done | pkg-000014 |

## Stories (EPIC-IDS-08)

| Story key | Anchor | Status |
|-----------|--------|--------|
| STORY-IDS-CLEANUP-01-remove-stories-from-identity | [story](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md) | 🟢 Done |
| STORY-IDS-CLEANUP-02-placeholders-hardening | [story](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-02-placeholders-hardening/STORY-IDS-CLEANUP-02-placeholders-hardening.md) | 🟢 Done |
| STORY-IDS-CLEANUP-03-doc-drift | [story](./epics/EPIC-IDS-08-cleanup/stories/STORY-IDS-CLEANUP-03-doc-drift/STORY-IDS-CLEANUP-03-doc-drift.md) | 🟢 Done |

## Stories (EPIC-IDS-01)

| Story key | Anchor | Status |
|-----------|--------|--------|
| STORY-IDS-01-01-init-package-and-dependencies | [story](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-01-init-package-and-dependencies/STORY-IDS-01-01-init-package-and-dependencies.md) | 🟢 Done |
| STORY-IDS-01-02-appconfig | [story](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-02-appconfig/STORY-IDS-01-02-appconfig.md) | 🟢 Done |
| STORY-IDS-01-03-custom-dotenv-parser | [story](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-03-custom-dotenv-parser/STORY-IDS-01-03-custom-dotenv-parser.md) | 🟢 Done |
| STORY-IDS-01-04-makefile-railway-env-example | [story](./epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-04-makefile-railway-env-example/STORY-IDS-01-04-makefile-railway-env-example.md) | 🟢 Done |

## Stories (EPIC-IDS-02)

| Story key | Anchor | Status |
|-----------|--------|--------|
| STORY-IDS-02-01-response-envelope-error-trace-id | [story](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-01-response-envelope-error-trace-id/STORY-IDS-02-01-response-envelope-error-trace-id.md) | 🟢 Done |
| STORY-IDS-02-02-logging-setup | [story](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-02-logging-setup/STORY-IDS-02-02-logging-setup.md) | 🟢 Done |
| STORY-IDS-02-03-auth-security-primitives-bearer-stub | [story](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-03-auth-security-primitives-bearer-stub/STORY-IDS-02-03-auth-security-primitives-bearer-stub.md) | 🟢 Done |
| STORY-IDS-02-04-fastapi-app-lifespan-cors-middleware | [story](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-04-fastapi-app-lifespan-cors-middleware/STORY-IDS-02-04-fastapi-app-lifespan-cors-middleware.md) | 🟢 Done |
| STORY-IDS-02-05-routes-contract-health-ready-identity-stubs | [story](./epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-05-routes-contract-health-ready-identity-stubs/STORY-IDS-02-05-routes-contract-health-ready-identity-stubs.md) | 🟢 Done |

## Stories (EPIC-IDS-03)

| Story key | Anchor | Status |
|-----------|--------|--------|
| STORY-IDS-03-01-api-dependencies-dataclass-handler-alias | [story](./epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-01-api-dependencies-dataclass-handler-alias/STORY-IDS-03-01-api-dependencies-dataclass-handler-alias.md) | 🟢 Done |
| STORY-IDS-03-02-build-api-dependencies-singleton-lifespan | [story](./epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-02-build-api-dependencies-singleton-lifespan/STORY-IDS-03-02-build-api-dependencies-singleton-lifespan.md) | 🟢 Done |
| STORY-IDS-03-03-epic-ids-04-extension-hook-contract | [story](./epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-03-epic-ids-04-extension-hook-contract/STORY-IDS-03-03-epic-ids-04-extension-hook-contract.md) | 🟢 Done |

## Stories (EPIC-IDS-04)

| Story key | Anchor | Status |
|-----------|--------|--------|
| STORY-IDS-04-01-domain-protocols-contracts | [story](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-01-domain-protocols-contracts/STORY-IDS-04-01-domain-protocols-contracts.md) | 🟢 Done |
| STORY-IDS-04-02-inmemory-repositories | [story](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-02-inmemory-repositories/STORY-IDS-04-02-inmemory-repositories.md) | 🟢 Done |
| STORY-IDS-04-03-service-factory-default | [story](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-03-service-factory-default/STORY-IDS-04-03-service-factory-default.md) | 🟢 Done |
| STORY-IDS-04-04-eid-provider-registry-mock | [story](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-04-eid-provider-registry-mock/STORY-IDS-04-04-eid-provider-registry-mock.md) | 🟢 Done |
| STORY-IDS-04-05-supabase-jwt-bearer-auth | [story](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-05-supabase-jwt-bearer-auth/STORY-IDS-04-05-supabase-jwt-bearer-auth.md) | 🟢 Done |
| STORY-IDS-04-06-provide-factory-di-integration | [story](./epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-06-provide-factory-di-integration/STORY-IDS-04-06-provide-factory-di-integration.md) | 🟢 Done |

## Stories (EPIC-IDS-05)

| Story key | Anchor | Status |
|-----------|--------|--------|
| STORY-IDS-05-01-supabase-database-http-client | [story](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-01-supabase-database-http-client/STORY-IDS-05-01-supabase-database-http-client.md) | 🟢 Done |
| STORY-IDS-05-02-supabase-repositories-identity-set | [story](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-02-supabase-repositories-identity-set/STORY-IDS-05-02-supabase-repositories-identity-set.md) | 🟢 Done |
| STORY-IDS-05-03-five-level-healthcheck | [story](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-03-five-level-healthcheck/STORY-IDS-05-03-five-level-healthcheck.md) | 🟢 Done |
| STORY-IDS-05-04-sql-schema-migrations | [story](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-04-sql-schema-migrations/STORY-IDS-05-04-sql-schema-migrations.md) | 🟢 Done |
| STORY-IDS-05-05-supabase-project-setup-live-credentials | [story](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-05-supabase-project-setup-live-credentials/STORY-IDS-05-05-supabase-project-setup-live-credentials.md) | 🟢 Done |
| STORY-IDS-05-06-backend-switch-provide-service-factory | [story](./epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-06-backend-switch-provide-service-factory/STORY-IDS-05-06-backend-switch-provide-service-factory.md) | 🟢 Done |

## Stories (EPIC-IDS-06)

| Story key | Anchor | Status |
|-----------|--------|--------|
| STORY-IDS-06-01-conftest-autouse-fixtures | [story](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-01-conftest-autouse-fixtures/STORY-IDS-06-01-conftest-autouse-fixtures.md) | 🟢 Done |
| STORY-IDS-06-02-http-bootstrap-di-smoke-tests | [story](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-02-http-bootstrap-di-smoke-tests/STORY-IDS-06-02-http-bootstrap-di-smoke-tests.md) | 🟢 Done |
| STORY-IDS-06-03-live-supabase-integration | [story](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-03-live-supabase-integration/STORY-IDS-06-03-live-supabase-integration.md) | 🟢 Done |
| STORY-IDS-06-04-ci-workflows-offline-live | [story](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-04-ci-workflows-offline-live/STORY-IDS-06-04-ci-workflows-offline-live.md) | 🟢 Done |
| STORY-IDS-06-05-live-server-smoke | [story](./epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-05-live-server-smoke/STORY-IDS-06-05-live-server-smoke.md) | 🟢 Done |

## Run Reports Registry

| Window | Report | Notes |
|--------|--------|-------|
| flat 1–3 | [`identity-cursor-build-window--flat-1-3.md`](./run-reports/identity-build-windows/identity-cursor-build-window--flat-1-3.md) | STORY-IDS-02-01 t01–t03 — 🟢 Done 2026-05-29 |
| flat 4–5 | [`identity-cursor-build-window--flat-4-5.md`](./run-reports/identity-build-windows/identity-cursor-build-window--flat-4-5.md) | STORY-IDS-02-02 t01–t02 — 🟢 Done 2026-05-29 |
| flat 6–8 | [`identity-cursor-build-window--flat-6-8.md`](./run-reports/identity-build-windows/identity-cursor-build-window--flat-6-8.md) | STORY-IDS-02-03 t01–t03 — 🟢 Done 2026-05-29 |
| flat 1–14 | [`identity-cursor-build-window--flat-1-14.md`](./run-reports/identity-build-windows/identity-cursor-build-window--flat-1-14.md) | EPIC-IDS-02 full pkg-000003 P3 — 🟢 Done 2026-05-29 |
| full | [`run-summary-20260529-epic-ids-02-p3-full-pkg-000003.md`](./run-reports/run-summary-20260529-epic-ids-02-p3-full-pkg-000003.md) | Epic gate + 40 pytest |
| override | [`run-summary-20260529-epic-ids-02-audit-gaps-override.md`](./run-reports/run-summary-20260529-epic-ids-02-audit-gaps-override.md) | A-1/A-2 gaps — 🟢 Done, 43 pytest |
| story01 | [`run-summary-20260529-epic-ids-03-story01-pkg-000004.md`](./run-reports/run-summary-20260529-epic-ids-03-story01-pkg-000004.md) | STORY-IDS-03-01 t01–t02 — 🟢 Done, 48 pytest |
| story02 | [`run-summary-20260529-epic-ids-03-story02-pkg-000004.md`](./run-reports/run-summary-20260529-epic-ids-03-story02-pkg-000004.md) | STORY-IDS-03-02 t01–t03 — 🟢 Done, 54 pytest |
| story03 | [`run-summary-20260529-epic-ids-03-story03-epic-gate-pkg-000004.md`](./run-reports/run-summary-20260529-epic-ids-03-story03-epic-gate-pkg-000004.md) | STORY-IDS-03-03 + epic gate — 🟢 Done, 56 pytest |
| full pkg-000004 | [`run-summary-20260529-epic-ids-03-p3-full-pkg-000004.md`](./run-reports/run-summary-20260529-epic-ids-03-p3-full-pkg-000004.md) | EPIC-IDS-03 complete |
| story01 pkg-000005 | [`run-summary-20260530-epic-ids-04-story01-pkg-000005.md`](./run-reports/run-summary-20260530-epic-ids-04-story01-pkg-000005.md) | STORY-IDS-04-01 t01–t03 — 🟢 Done, 61 pytest |
| story02 pkg-000005 | [`run-summary-20260530-epic-ids-04-story02-pkg-000005.md`](./run-reports/run-summary-20260530-epic-ids-04-story02-pkg-000005.md) | STORY-IDS-04-02 t01–t03 — 🟢 Done, 76 pytest |
| story03 pkg-000005 | [`run-summary-20260530-epic-ids-04-story03-pkg-000005.md`](./run-reports/run-summary-20260530-epic-ids-04-story03-pkg-000005.md) | STORY-IDS-04-03 t01–t02 — 🟢 Done, 81 pytest |
| story04 pkg-000005 | [`run-summary-20260530-epic-ids-04-story04-pkg-000005.md`](./run-reports/run-summary-20260530-epic-ids-04-story04-pkg-000005.md) | STORY-IDS-04-04 t01–t03 — 🟢 Done, 87 pytest |
| story05 pkg-000005 | [`run-summary-20260530-epic-ids-04-story05-pkg-000005.md`](./run-reports/run-summary-20260530-epic-ids-04-story05-pkg-000005.md) | STORY-IDS-04-05 t01–t03 — 🟢 Done, 95 pytest |
| story06 pkg-000005 | [`run-summary-20260530-epic-ids-04-story06-pkg-000005.md`](./run-reports/run-summary-20260530-epic-ids-04-story06-pkg-000005.md) | STORY-IDS-04-06 t01–t03 — 🟢 Done, 102 pytest · **pkg-000005 stories complete** |
| audit gaps override | [`run-summary-20260530-epic-ids-04-audit-gaps-override.md`](./run-reports/run-summary-20260530-epic-ids-04-audit-gaps-override.md) | `run_mode=epic_ids_04_audit_2026_05_30` — S5-1/S2-1/S1-2/S5-2/S6-1 🟢 · RG-1/RG-2 ⚪ |
| story01 pkg-000006 | [`run-summary-20260531-epic-ids-05-story01-pkg-000006.md`](./run-reports/run-summary-20260531-epic-ids-05-story01-pkg-000006.md) | STORY-IDS-05-01 t01–t02 — 🟢 Done, 109 pytest |
| story02 pkg-000006 | [`run-summary-20260531-epic-ids-05-story02-pkg-000006.md`](./run-reports/run-summary-20260531-epic-ids-05-story02-pkg-000006.md) | STORY-IDS-05-02 t01–t03 — 🟢 Done, 116 pytest |
| story03 pkg-000006 | [`run-summary-20260531-epic-ids-05-story03-pkg-000006.md`](./run-reports/run-summary-20260531-epic-ids-05-story03-pkg-000006.md) | STORY-IDS-05-03 t01–t03 — 🟢 Done, 125 pytest |
| story04 pkg-000006 | [`run-summary-20260531-epic-ids-05-story04-pkg-000006.md`](./run-reports/run-summary-20260531-epic-ids-05-story04-pkg-000006.md) | STORY-IDS-05-04 t01–t03 — 🟢 Done, 134 pytest |
| story05 pkg-000006 | [`run-summary-20260531-epic-ids-05-story05-pkg-000006.md`](./run-reports/run-summary-20260531-epic-ids-05-story05-pkg-000006.md) | STORY-IDS-05-05 t01–t03 — 🟢 Done, 150 pytest |
| story06 pkg-000006 | [`run-summary-20260531-epic-ids-05-story06-pkg-000006.md`](./run-reports/run-summary-20260531-epic-ids-05-story06-pkg-000006.md) | STORY-IDS-05-06 t01–t03 — 🟢 Done, 154 pytest · **pkg-000006 complete** |
| STORY-IDS-05-01 | [`identity-cursor-build-window--STORY-IDS-05-01-supabase-database-http-client.md`](./run-reports/identity-build-windows/identity-cursor-build-window--STORY-IDS-05-01-supabase-database-http-client.md) | t01–t02 — 🟢 Done 2026-05-31 |
| STORY-IDS-05-02 | [`identity-cursor-build-window--STORY-IDS-05-02-supabase-repositories-identity-set.md`](./run-reports/identity-build-windows/identity-cursor-build-window--STORY-IDS-05-02-supabase-repositories-identity-set.md) | t01–t03 — 🟢 Done 2026-05-31 |
| STORY-IDS-05-03 | [`identity-cursor-build-window--STORY-IDS-05-03-five-level-healthcheck.md`](./run-reports/identity-build-windows/identity-cursor-build-window--STORY-IDS-05-03-five-level-healthcheck.md) | t01–t03 — 🟢 Done 2026-05-31 |
| STORY-IDS-05-04 | [`identity-cursor-build-window--STORY-IDS-05-04-sql-schema-migrations.md`](./run-reports/identity-build-windows/identity-cursor-build-window--STORY-IDS-05-04-sql-schema-migrations.md) | t01–t03 — 🟢 Done 2026-05-31 |
| STORY-IDS-05-05 | [`identity-cursor-build-window--STORY-IDS-05-05-supabase-project-setup-live-credentials.md`](./run-reports/identity-build-windows/identity-cursor-build-window--STORY-IDS-05-05-supabase-project-setup-live-credentials.md) | t01–t03 — 🟢 Done 2026-05-31 |
| STORY-IDS-05-06 | [`identity-cursor-build-window--STORY-IDS-05-06-backend-switch-provide-service-factory.md`](./run-reports/identity-build-windows/identity-cursor-build-window--STORY-IDS-05-06-backend-switch-provide-service-factory.md) | t01–t03 — 🟢 Done 2026-05-31 |
| re-audit gaps override | [`run-summary-20260602-epic-ids-05-reaudit-gaps-override.md`](./run-reports/run-summary-20260602-epic-ids-05-reaudit-gaps-override.md) | `run_mode=epic_ids_05_reaudit_2026_06_02` — 5/5 gaps 🟢, 156 pytest |
