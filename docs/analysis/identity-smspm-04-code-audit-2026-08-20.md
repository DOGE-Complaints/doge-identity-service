# Аудит по коду: STORY-IDS-SMSPM-04 (delivery report / webhook) — 2026-08-20

> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — verified-state, только проверяемые claims с путями; регрессии; gaps с severity + как закрыть. Findings-only.
> **Объект:** pipeline [`STORY-IDS-SMSPM-04-delivery-report-webhook`](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-04-delivery-report-webhook/STORY-IDS-SMSPM-04-delivery-report-webhook.md) · backlog [`STORY-IDS-SMSPM-04-delivery-report-webhook`](../tasks/backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md) (`input_mode=backlog_story`, pkg-000049).
> **Fence (не invent AC):** GET webhook + secret path (**не** Ed25519); confirm/OTP ungated (D-04-5); forward-only ingest; optional `report` на send; audit без plaintext phone.
> **Bullrun:** статусы task/story — touchpoints **в этом файле**. `bullrun-launch-index.md` VAL не правил. P5 не стартовать.

---

## Вердикт

**STORY-IDS-SMSPM-04 = 🟢 Done — подтверждено фактическим кодом.** `GET /webhooks/smspm/delivery/{shared_secret}` → `compare_digest` (не Ed25519); 200 plain `OK` / 401 mismatch; parse `id`/`status` без записи `toNumber`; `apply_delivery_update` forward-only по `provider_message_id`; confirm не смотрит `delivery_status`; `SMSPM_REPORT_URL` set → send JSON `report`; audit event без plaintext phone/OTP. Offline **443 passed, 13 deselected**; smspm-slice **37 passed, 1 deselected**.

**vs story AC: 0 OPEN / 6.** Material gaps: **нет** (0×Critical, 0×HIGH, 0×MEDIUM). Product Story Done **да** и gap-list пуст — оба явно.

Независимо перепрогнано (2026-08-20): совпадает с [run-summary](../tasks/run-reports/identity-build-windows/run-summary-20260820-1106-epic-ids-14-smspm-04-pkg-000049.md).

---

## Bullrun status touchpoints (без правок индекса)

| Якорь | Строки | Заявлено | Факт-код/docs | Вердикт |
|-------|--------|----------|---------------|---------|
| §Актуальная точка | [bullrun:11-13](../tasks/bullrun-launch-index.md) | SMSPM-04 🟢 pkg-000049; P3 6/6; 443 pytest | route+handler+ingest+`report`+tests; 443/13 | ✅ |
| input_mode / active story | [bullrun:123](../tasks/bullrun-launch-index.md) | `backlog_story` · SMSPM-04 🟢 pkg-000049 | pipeline/backlog Meta 🟢; AC `[x]` 6/6 | ✅ |
| Active pkg | [bullrun:125](../tasks/bullrun-launch-index.md) | pkg-000049 🟢 6 paths | [`pkg-000049:11-17`](../tasks/identity-active-packages/pkg-000049-20260820-epic-ids-14-smspm-04-delivery-report-webhook.yaml); 6× README Status `done`; t06 PASS | ✅ |
| Epic registry EPIC-IDS-14 | [bullrun:191](../tasks/bullrun-launch-index.md) | 🟡 — SMSPM-01/02/04 🟢; SMSPM-03 ⚪ | SMSPM-03 t04 BLOCKED (другая story) | ✅ эпик не Done |
| Task queue t01–t06 | [bullrun:842-847](../tasks/bullrun-launch-index.md) | все 🟢 pkg-000049 | gates PASS ниже | ✅ |
| Stories EPIC-IDS-14 SMSPM-04 | [bullrun:919](../tasks/bullrun-launch-index.md) | 🟢 Done (pkg-000049) | Meta 🟢; [INDEX:10](../tasks/backlog-stories/smspm/INDEX.md) 🟢; dashboard 40/42 | ✅ нет drift ⚪ |

**Актуализация в отчёте:** t01–t06 и product story = 🟢 по коду. Строки индекса **факт-верны**. HK «do not start P4» в [bullrun:12](../tasks/bullrun-launch-index.md) — snapshot после P3; этот VAL-отчёт P4 по fence, индекс не менялся.

---

## Пер-таск верификация (по коду)

| Task | Требование стори | Факт | Вердикт |
|------|------------------|------|---------|
| **t01** Route + handler | `GET /webhooks/smspm/delivery/{shared_secret}`; 401 mismatch; body `OK`; не Ed25519 | [`asgi_app.py:411-423`](../../src/core/api/asgi_app.py) без `Depends(get_current_user)`; [`handlers.py:759-837`](../../src/core/api/handlers.py) `secrets.compare_digest`; missing secret → 503 `CONFIG_ERROR`; success `return None, 200` → plain `OK`; **нет** `verify_telnyx_webhook_signature` в этом handler | 🟢 Done |
| **t02** Parse + ingest | query `id`/`status`; omit `toNumber`; map D-04-2; forward-only D-04-3 | [`delivery_ingest.py:28-46`](../../src/core/phone/smspm/delivery_ingest.py): `id`/`status` only; `_STATUS_MAP` queued/submitted→sent/sent/delivered/failed → `CANONICAL_DELIVERY_STATUSES`; [`apply_delivery_update`](../../src/core/phone/telnyx/delivery_ingest.py) (`:71-100`) rank + FINAL noop | 🟢 Done |
| **t03** Sender `report` | `SMSPM_REPORT_URL` set → POST `report`; unset → как SMSPM-02 | [`sender.py:29-30`](../../src/core/phone/smspm/sender.py); [`config.py:12,38`](../../src/core/phone/smspm/config.py) optional, **not** in `SMSPM_REQUIRED_ENV`; tests include/absent `report` | 🟢 Done |
| **t04** Offline tests | happy-path; 401; replay; confirm unchanged | [`test_smspm_delivery_webhook.py`](../../tests/test_smspm_delivery_webhook.py) + [`test_smspm_delivery_ingest.py`](../../tests/test_smspm_delivery_ingest.py); slice **37 passed, 1 deselected**; full **443/13** | 🟢 Done |
| **t05** Env docs | `SMSPM_WEBHOOK_SHARED_SECRET` + `SMSPM_REPORT_URL` в `.env.example` / runbook pointer | [`.env.example:85-86`](../../.env.example); runbook row [`:25`](../runbook/phone-sms-verification.md) + env names [`:63-64`](../runbook/phone-sms-verification.md) + pointer [`:147`](../runbook/phone-sms-verification.md); Telnyx POST row [`:24`](../runbook/phone-sms-verification.md) и §6 B [`:121-145`](../runbook/phone-sms-verification.md) на месте | 🟢 Done |
| **t06** Story gate | все parent AC | [t06 acceptance](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-04-delivery-report-webhook/task-ids-14-04-t06-story-acceptance-verification/acceptance-verification-task-ids-14-04-t06-story-acceptance-verification.md) PASS `2026-08-20T11:06:55Z` | 🟢 Done |

Story T01–T07 схлопнуты в pkg в 6 task folders (T02–T04 → t02; T06→t04; T07→t05) — совпадает с nested tasks pipeline [`:85-91`](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-04-delivery-report-webhook/STORY-IDS-SMSPM-04-delivery-report-webhook.md).

---

## Сверка Acceptance Criteria (verbatim backlog = pipeline)

Источник: backlog [`:70-75`](../tasks/backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md) = pipeline [`:73-78`](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-04-delivery-report-webhook/STORY-IDS-SMSPM-04-delivery-report-webhook.md).

| AC | Факт | Вердикт |
|----|------|---------|
| Статусы доставки по provider message id; OTP-confirm без изменения (D-04-5) | Ingest `provider_message_id` → `store.get_by_provider_message_id` ([`delivery_ingest.py:78`](../../src/core/phone/telnyx/delivery_ingest.py)); [`handle_phone_confirm`](../../src/core/api/handlers.py) (`:539-637`) **не** читает `delivery_status`; [`otp_engine.py`](../../src/core/phone/otp_engine.py) без `delivery_status`; `test_confirm_succeeds_when_delivery_status_failed` | ✅ |
| `OK` при валидном secret; 401 mismatch (D-04-1) | 200 `text/plain` `OK` ([`asgi_app.py:421-422`](../../src/core/api/asgi_app.py)); 401 JSON `UNAUTHORIZED` ([`handlers.py:775-790`](../../src/core/api/handlers.py)); `test_valid_secret_*` / `test_bad_secret_returns_401_*` | ✅ |
| Повторные/устаревшие forward-only (D-04-3) | rank + FINAL set ([`telnyx/delivery_ingest.py:86-92`](../../src/core/phone/telnyx/delivery_ingest.py)); replay delivered→submitted остаётся `delivered` (`test_idempotent_replay_does_not_regress_final_status`) | ✅ |
| Аудит без сырого номера/OTP (D-04-6) | `_log_phone_audit` ([`handlers.py:114-141,828-836`](../../src/core/api/handlers.py)): нет phone/`toNumber`/OTP в `PhoneAuditEvent` ([`models.py:93-103`](../../src/core/domain/models.py)); parse не читает `toNumber` ([`delivery_ingest.py:28-46`](../../src/core/phone/smspm/delivery_ingest.py)); `test_delivery_audit_logged_without_pii` | ✅ |
| `SMSPM_REPORT_URL` set → sender `report` (D-04-4) | [`sender.py:29-30`](../../src/core/phone/smspm/sender.py); `test_smspm_send_includes_report_when_url_set`; unset: `"report" not in body` | ✅ |
| Offline T06 зелёные; env T07 | 37/1 slice; 443/13 full; `.env.example:85-86`; runbook names | ✅ |

**D-04-\* (не отдельный AC):** D-04-2 map → canonical (`submitted`→`sent`). D-04-7 optional secret/report — не в `SMSPM_REQUIRED_ENV` ([`test_smspm_config.py:77-78`](../../tests/test_smspm_config.py)). D-G6: GET + path secret, не Ed25519 — ✅.

---

## Регрессии

**Не найдено в коде этой волны.**

| Аспект | Факт |
|--------|------|
| Telnyx POST + Ed25519 | [`asgi_app.py:396-408`](../../src/core/api/asgi_app.py) `POST /webhooks/telnyx/messaging`; [`webhook_signature.py`](../../src/core/phone/telnyx/webhook_signature.py) не вызывается из `handle_smspm_delivery_webhook` | ✅ |
| mock / Telnyx send | сюита 443; SMSPM send без `report` если env пуст | ✅ |
| OTP confirm / `phone_verified` | ungated (D-04-5); вне scope «gate по delivery» | ✅ |
| SMSPM-03 live EE | по-прежнему ⚪ BLOCKED — не эта story | ✅ |
| SMSPM-05 `smsId` | draft; handler `send` без `sms_id` — вне SMSPM-04 | ✅ |
| Счётчик сюиты | 428 (SMSPM-02) → **443** | ожидаемо (+ webhook/ingest/report tests) |

---

## Gaps (findings)

**Нет.** vs AC **0 OPEN**. Actionable gap-list пуст.

Наблюдения (**не gap**, severity none):

- D-04-6 «store message id + status»: `PhoneAuditEvent` не имеет полей message id / delivery_status — то же зеркало, что Telnyx webhook audit (`telnyx_delivery_status_updated`). AC #4 требует omit PII, не новую схему. Не invent AC.
- D-04-1 «или `?key=`»: реализован path-secret, не query `key`. Альтернатива в решении, не AC.
- Invalid query → 400 JSON (`missing message id` / unsupported status), не plain `OK`. D-04-1 задаёт 401/200 OK, не все коды.
- Missing `SMSPM_WEBHOOK_SHARED_SECRET` → 503 (как Telnyx missing public key), не 401.

---

## Итог / P5

- **Story Done: да.** **vs AC: 0 OPEN / 6.**
- **BLOCKED:** нет. **Done:** t01–t06.
- Bullrun 🟢 **совпадает** с диском; drift Stories ⚪ **нет**.
- **P5 не стартовать** из VAL (zero-gap; нет TASKED).
