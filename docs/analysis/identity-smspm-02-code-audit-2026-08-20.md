# Аудит по коду: STORY-IDS-SMSPM-02 (SMSPM SMS sender) — 2026-08-20

> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — verified-state, только проверяемые claims с путями; регрессии; gaps с severity + как закрыть. Findings-only.
> **Объект:** pipeline [`STORY-IDS-SMSPM-02-sms-sender`](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-02-sms-sender/STORY-IDS-SMSPM-02-sms-sender.md) · backlog [`STORY-IDS-SMSPM-02-sms-sender`](../tasks/backlog-stories/smspm/STORY-IDS-SMSPM-02-sms-sender.md) (`input_mode=backlog_story`, pkg-000047).
> **Scope (fence, не invent AC):** HTTP send **в DoD**; live T05 = skip-without-creds (SPIKE вне очереди); runbook = SMSPM-03; webhook/`report` = SMSPM-04; OTP engine / Verify API вне scope.
> **Bullrun:** статусы task/story — touchpoints **в этом файле**. `bullrun-launch-index.md` VAL не правил.

---

## Вердикт

**STORY-IDS-SMSPM-02 = 🟢 Done — подтверждено фактическим кодом.** HTTP POST (hash/token в JSON, `toNumber` без `+`, без Bearer, без `report`) реализован; descriptor `build` → `SmspmSmsSender` + обязательный `httpx.Client`; ошибки D-02-2; `/auth/phone/request` → `get_active().send` → id в сессии; клиенту `sent`/`expires_at` без OTP. Offline **428 passed, 13 deselected**; smspm-slice **22 passed, 1 deselected**; live marker **1 skipped** без `SMSPM_*`.

**vs story AC: 0 OPEN** (5/5 AC). Найдено **2 gap'а** (0×HIGH, 0×MEDIUM, 2×LOW) — индекс-дрейф и неподключённый optional `smsId` (D-02-6 recommend). Ни один не ломает AC.

Независимо перепрогнано (2026-08-20): совпадает с [run-summary](../tasks/run-reports/identity-build-windows/run-summary-20260820-1027-epic-ids-14-smspm-02-pkg-000047.md).

---

## Bullrun status touchpoints (без правок индекса)

| Якорь | Строки | Заявлено | Факт-код | Вердикт |
|-------|--------|----------|----------|---------|
| §Актуальная точка | [bullrun:11-13](../tasks/bullrun-launch-index.md) | SMSPM-02 🟢 pkg-000047; P3 6/6; 428 pytest | `sender.py` + `errors.py` + descriptor wire; 428 offline | ✅ |
| input_mode / active story | [bullrun:107](../tasks/bullrun-launch-index.md) | `backlog_story` · SMSPM-02 🟢 | pipeline/backlog Meta 🟢 | ✅ |
| Active pkg | [bullrun:109](../tasks/bullrun-launch-index.md) | pkg-000047 🟢 6 paths | 6 task README Status done + t06 PASS | ✅ |
| Epic registry EPIC-IDS-14 | [bullrun:173](../tasks/bullrun-launch-index.md) | 🟡 — SMSPM-01/02 🟢; SMSPM-03…04 backlog | runbook/webhook не в `smspm/` | ✅ эпик не Done |
| Task queue t01–t06 | [bullrun:812-817](../tasks/bullrun-launch-index.md) | все 🟢 pkg-000047 | см. пер-таск | ✅ |
| **Stories EPIC-IDS-14 SMSPM-02** | [bullrun:887](../tasks/bullrun-launch-index.md) | **⚪ Todo** (pkg-000047) | story Meta 🟢; backlog INDEX 🟢; tasks 🟢 | ❌ **drift → F1** |

**Актуализация в отчёте:** t01–t06 и product story = 🟢 по коду. Строка Stories [887] **не** факт-верна (осталась ⚪). Эпик 🟡 корректен (SMSPM-03…04).

---

## Пер-таск верификация (по коду)

| Task | Требование стори | Факт | Вердикт |
|------|------------------|------|---------|
| **t01** `SmspmSmsSender.send` | POST JSON hash/token/`toNumber` strip `+`/`fromNumber`/`text`/optional `smsId`; parse `messages[0].id` | [`sender.py:19-45,47-65`](../../src/core/phone/smspm/sender.py); URL = `api_base_url` без path ([SA §4.2](../tasks/backlog-stories/smspm/solution-architecture-smspm-sms-provider.md)); нет `Authorization`/`report` | ✅ Done |
| **t02** `errors.py` | D-02-2 + timeout → `PROVIDER_UNAVAILABLE` | [`errors.py:25-54`](../../src/core/phone/smspm/errors.py): 5xx→UNAVAILABLE; 401→SEND_FAILED; `"invalid phone"` в тексте→INVALID_PHONE; прочий 4xx→SEND_FAILED; else UNKNOWN; timeout отдельным mapper | ✅ Done |
| **t03** Wire | descriptor `build` + httpx | [`descriptor.py:10-23`](../../src/core/phone/smspm/descriptor.py) `SmspmSmsSender` + require `http_client`; stub отсутствует (`rg SmspmSmsStub` в `src/` = 0) | ✅ Done |
| **t04** Offline tests | success; 401; invalid phone; 5xx; missing id; no secrets/OTP/MSISDN in logs | [`tests/test_smspm_sms_sender.py`](../../tests/test_smspm_sms_sender.py) + timeout/other 4xx/`smsId`/`report` absent | ✅ Done |
| **t05** Live skip-without-creds | marker + skip без creds (SPIKE вне очереди) | [`test_smspm_live_send_skips_without_credentials`](../../tests/test_smspm_sms_sender.py) `@pytest.mark.live_integration`; skip без HASH/TOKEN/FROM; live-run: **1 skipped** | ✅ Done (паттерн как Telnyx) |
| **t06** story gate | 5 parent AC | [t06 acceptance](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-02-sms-sender/task-ids-14-02-t06-story-acceptance-verification/acceptance-verification-task-ids-14-02-t06-story-acceptance-verification.md) PASS `2026-08-20T10:27:17Z` | ✅ Done |

---

## Сверка Acceptance Criteria (verbatim backlog = pipeline)

Источник: backlog [`:66-71`](../tasks/backlog-stories/smspm/STORY-IDS-SMSPM-02-sms-sender.md) = pipeline [`:69-74`](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-02-sms-sender/STORY-IDS-SMSPM-02-sms-sender.md).

| AC | Факт | Вердикт |
|----|------|---------|
| При `SMS_PROVIDER=smspm` и валидных creds `POST /auth/phone/request` доставляет SMS через SMSPM; ответ клиенту без кода | Route [`asgi_app.py:359-375`](../../src/core/api/asgi_app.py) → [`handlers.py:494-504`](../../src/core/api/handlers.py) `registry.get_active` → `sender.send`; active smspm = `SmspmSmsSender` ([`descriptor.py:17`](../../src/core/phone/smspm/descriptor.py), тест `test_build_sms_registry_active_smspm`); payload [`handlers.py:530-534`](../../src/core/api/handlers.py) только `sent`/`expires_at` | ✅ |
| При успехе (D-02-1) provider message id сохраняется в phone-сессии | Parse `messages[0].id` → `SmsSendResult` ([`sender.py:56-60`](../../src/core/phone/smspm/sender.py)); [`handlers.py:505-507`](../../src/core/api/handlers.py) `dataclasses.replace` + `session_store.replace` | ✅ |
| Ошибки по D-02-2; секреты/OTP/full MSISDN не в логах (D-02-7) | mapper [`errors.py:25-49`](../../src/core/phone/smspm/errors.py) логирует `code`/`http_status`/`reason` label, не body; тест `test_smspm_send_does_not_log_secrets_otp_or_msisdn` | ✅ |
| Offline T04 зелёные; live T05 skip без creds | 22 passed / 1 deselected (smspm files); live 1 skipped; full 428/13 | ✅ |
| `mock\|file\|telnyx` без регрессий; MVP без `report` (D-02-5) | 428 offline; payload `"report" not in body` (success + smsId tests); `report` нет в `src/core/phone/smspm/` | ✅ |

**D-02-\* (не отдельный AC):** D-02-3 strip только в sender (`to_e164.lstrip("+")`). D-02-4 JSON hash/token, не Bearer. D-02-5 нет `report`. D-02-6 `smsId` в sender optional — **продуктовый вызов не передаёт** (F2). D-02-7 см. AC #3.

---

## Регрессии

**Не найдено в коде этой волны.**

| Аспект | Факт |
|--------|------|
| OTP engine / Verify API | `otp_engine.py` без SMSPM; ядро по-прежнему генерирует OTP ([`otp_engine.py:49-64`](../../src/core/phone/otp_engine.py)); handler шлёт `build_verification_sms_text(plaintext_code)` | вне scope, не тронут |
| mock/file/telnyx | остаются в `ALL_SMS_PROVIDER_DESCRIPTORS`; сюита 428 | ✅ |
| SMSPM-01 config | `SmspmSettings` / fail-fast без изменений контракта | ✅ |
| Stub SMSPM-01 | `SmspmSmsStub` удалён; registry отдаёт `SmspmSmsSender` ([`test_smspm_config.py:100-108`](../../tests/test_smspm_config.py)) | ожидаемая замена |
| Runbook / webhook | не в этой story (SMSPM-03/04) | ✅ |
| Счётчик сюиты | 417 (SMSPM-01) → **428** (+11 offline sender tests) | ожидаемо |

---

## Gaps (findings)

| ID | Severity | Суть | Файл:строка | Как закрыть |
|----|----------|------|-------------|-------------|
| **F1** | **LOW** | **Index drift: Stories table SMSPM-02 = ⚪ Todo** при Meta/task queue/backlog INDEX/run-summary 🟢. §Актуальная точка уже 🟢. Не дефект send-кода. | [`bullrun-launch-index.md:887`](../tasks/bullrun-launch-index.md) vs [`pipeline Meta:7`](../tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-02-sms-sender/STORY-IDS-SMSPM-02-sms-sender.md); [INDEX:8](../tasks/backlog-stories/smspm/INDEX.md); [bullrun:812-817](../tasks/bullrun-launch-index.md) | В Stories EPIC-IDS-14: ⚪ Todo → 🟢 Done (pkg-000047). Не менять product `src/`. |
| **F2** | **LOW** | **D-02-6 «рекомендуем да»: `smsId` = phone session id не идёт с `/auth/phone/request`.** Sender принимает `sms_id` ([`sender.py:19,27-28`](../../src/core/phone/smspm/sender.py)); unit `test_smspm_send_optional_sms_id`. Протокол [`SmsSenderPort.send`](../../src/core/phone/base.py) = `to_e164, text` без `sms_id`. Handler: [`handlers.py:504`](../../src/core/api/handlers.py) не передаёт `session.id` (сессия уже создана [`otp_engine.py:50-51`](../../src/core/phone/otp_engine.py)). Не AC (optional). | `handlers.py:504`; `base.py:42`; `sender.py:19-28` | Либо прокинуть session id на send (и расширить port, если нужен единый контракт), либо WAIVED reason=optional-recommend. Не блокирует OTP delivery. |

Наблюдения (**не gap**, severity none):

- Live T05 после skip-check не делает POST (как [`test_telnyx_live_send_skips_without_credentials`](../../tests/test_telnyx_sms_sender.py)) — fence: skip-without-creds = AC очереди; live pass после SPIKE = ops/SMSPM-03.
- SA §6 HTTP 429→`RATE_LIMITED` в story **D-02-2 нет**; 429 сейчас падает в 4xx→`SEND_FAILED`. Не invent AC.
- `_phone_error_response` отдаёт `str(exc)` = `"SMSPM request failed"` ([`errors.py:49`](../../src/core/phone/smspm/errors.py)) — без секретов.

---

## Итог для индекса / P5

- Product Story Done (5/5 AC) ≠ пустой gap-list: F1–F2 LOW.
- **vs AC: 0 OPEN.**
- F1 — docs-only bullrun Stories row; F2 — optional `smsId` wiring.
- **P5 не стартовать** из этого отчёта. HTTP send в DoD закрыт кодом. Runbook/webhook = SMSPM-03/04.
