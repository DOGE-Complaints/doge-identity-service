# Re-audit закрытия gap-листа SEC-01 (F1 doc-stale, F2 XFF-spoof)

> **Дата:** 2026-06-26
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — закрытие каждого gap проверено по фактическому коду/файлу (`file:line`); регрессии.
> **Источник gap-листа:** [`epic-ids-12-sec-01-audit-2026-06-26.md`](./epic-ids-12-sec-01-audit-2026-06-26.md) §3 (F1 MEDIUM, F2 MEDIUM-security).
> **Итог:** **2/2 закрыты.** Регрессий нет — **370 passed** (+1 spoof-тест).

## Сводка

| ID | Severity | Было | Стало | Вердикт |
|----|----------|------|-------|---------|
| F2 | MEDIUM (security) | callback per-IP доверял спуфабельному `X-Forwarded-For` (первый hop) → обход лимита | trusted-proxy-aware `_client_ip`; default `TRUSTED_PROXY_COUNT=0` → XFF **не доверяется**; spoof-тест | 🟢 **Закрыт** |
| F1 | MEDIUM (doc-stale) | SEC-01 story `⚪ Todo`, AC `[ ]`, «rate-limiter отсутствует», Scope без split-пометки | `🟢 Done`, AC `[x]`, «Точки в коде (as-built)», phone/request → SEC-01b | 🟢 **Закрыт** |

---

## F2 — XFF-spoof обход per-IP лимита → 🟢 ЗАКРЫТ

**Код** ([rate_limit_dependency.py:14-28](../../src/core/api/rate_limit_dependency.py)):
- `_client_ip` теперь читает `config.rate_limit_trusted_proxy_count`:
  - `count == 0` (default) → `X-Forwarded-For` **полностью игнорируется**, ключ = `request.client.host` (строки 26-27). Спуфинг невозможен по умолчанию.
  - `count > 0` → берётся hop по индексу `len(hops) - count - 1` — **правый-недоверенный** IP (тот, что увидел доверенный прокси), а не клиентский первый элемент (строки 18-25).
- **Конфиг:** `rate_limit_trusted_proxy_count` ([schema.py:74,248](../../src/core/config/schema.py)), env `RATE_LIMIT_TRUSTED_PROXY_COUNT` default `0`. ✅
- **Тест:** `test_callback_rate_limit_ignores_spoofed_x_forwarded_for` ([test_rate_limiting.py:77-86](../../tests/test_rate_limiting.py)) — три запроса с разными `X-Forwarded-For` (`1.1.1.1`/`2.2.2.2`/`3.3.3.3`) попадают в **один** ip-bucket (`request.client.host`), и N+1-й лимитируется → ротация XFF **не** обходит окно. ✅
- **Док:** [04-security.md:128](../runtime-docs/04-security.md) — поведение, default и deployment-инструкция («за reverse-proxy выставить число доверенных hop'ов») зафиксированы. ✅

**Вывод:** механизм закрыт правильно — **default-deny** на XFF (count=0), осознанное доверие ровно N hop'ам за прокси, покрыто прямым spoof-тестом и задокументировано.

---

## F1 — backlog-story doc-stale → 🟢 ЗАКРЫТ

[`STORY-IDS-SEC-01-rate-limiting.md`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md):
- **Status:** `⚪ Todo` → **`🟢 Done (волна pkg-000035)`** (стр.6) ✅; добавлена строка «Остаток G-1 → SEC-01b» (стр.7) ✅.
- **Scope:** `POST /auth/phone/request` — «**вынесен в SEC-01b** (не доставлено волной pkg-000035)» (стр.19) ✅; согласование с OTP-cooldown переписано под факт (cooldown=400, 429 не дублирует) (стр.23) ✅.
- **AC:** доставленные `[x]` (стр.41-45) ✅; alt-DEFERRED `[ ]` «не выбрана оператором» (стр.46) — корректно (построено, не deferred).
- **«Точки в коде»:** переписаны на «**as-built, pkg-000035**» — `rate_limit_config.py`/`rate_limit.py`/`rate_limit_dependency.py` (с пометкой `TRUSTED_PROXY_COUNT` — audit F2)/wiring/envelope/cooldown/тесты. Стейл-claim «rate-limiter отсутствует во всём src/core/» **удалён**. ✅

---

## Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **370 passed, 11 deselected** (было 369 → **+1**: `..._ignores_spoofed_x_forwarded_for`) |
| Изменение кода | `_client_ip` (trusted-proxy) + `rate_limit_trusted_proxy_count` config — аддитивно; default 0 не меняет поведение прежних тестов |
| Прежние rate-limit тесты (eid/start, callback, cooldown) | зелёные |

Регрессий нет; прирост +1 объяснён.

---

## Итог
- **F2 (security) — закрыт** правильным механизмом: trusted-proxy-aware IP с default-deny на `X-Forwarded-For` + прямой spoof-тест + doc в 04-security.
- **F1 (doc-stale) — закрыт:** SEC-01 story 🟢 Done, AC `[x]`, «as-built» точки, остаток G-1 явно вынесен в SEC-01b.
- **Регрессий нет** (370 passed, +1 тест).
- Наблюдения O1 (per-process in-memory store) / O3 (cooldown 400) — вне AC, действий не требовали; O1 остаётся pilot-допущением (Redis вне scope).

## Quality gate (analysis.mdc)
- [x] Каждый gap перепроверен по фактическому коду/файлу с `file:line`, не по заявлению.
- [x] F2 подтверждён тремя независимыми точками: код (`_client_ip` + config), тест (spoof), doc (04-security).
- [x] F1 проверен на удаление стейл-claim'а («отсутствует» больше нет) + корректный split (phone/request → SEC-01b).
- [x] Регрессий нет; 369→370 (+1) объяснён.
