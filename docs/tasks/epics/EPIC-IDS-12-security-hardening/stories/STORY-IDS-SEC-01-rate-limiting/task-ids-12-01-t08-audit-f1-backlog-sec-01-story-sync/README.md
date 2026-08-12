## Task workspace — `task-ids-12-01-t08-audit-f1-backlog-sec-01-story-sync`

- Story: [`../STORY-IDS-SEC-01-rate-limiting.md`](../STORY-IDS-SEC-01-rate-limiting.md)
- Audit source: [`../../../../../../analysis/epic-ids-12-sec-01-audit-2026-06-26.md`](../../../../../../analysis/epic-ids-12-sec-01-audit-2026-06-26.md) (F1)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_12_sec_01_audit_2026_06_26`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-12-sec-01-audit-2026-06-26.md`](../../../../../../analysis/epic-ids-12-sec-01-audit-2026-06-26.md) §F1  
---

## Task: fix — backlog SEC-01 story sync (F1)

### Цель
Привести backlog [`STORY-IDS-SEC-01-rate-limiting.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md) в соответствие с фактом: SEC-01 🟢 Done (волна pkg-000035, eid/start + callback).

### Почему это важно
Backlog story — persistent SSOT для intake; устаревший `⚪ Todo`, AC `[ ]` и «rate-limiter отсутствует» расходятся с pipeline/epic (уже 🟢) и блокируют корректный контекст для SEC-01b / SEC-02.

### Факты из кода
1. Backlog [`STORY-IDS-SEC-01-rate-limiting.md:6`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md) — `Status: ⚪ Todo`.
2. [`...:29`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md) — «Rate-limiter отсутствует во всём `src/core/`».
3. [`...:34-39`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md) — AC все `[ ]`.
4. Pipeline story 🟢 Done — [`../STORY-IDS-SEC-01-rate-limiting.md`](../STORY-IDS-SEC-01-rate-limiting.md).
5. Runtime: [`rate_limit_config.py`](../../../../../../../src/core/security/rate_limit_config.py), [`rate_limit_dependency.py`](../../../../../../../src/core/api/rate_limit_dependency.py), wiring [`asgi_app.py:304,323`](../../../../../../../src/core/api/asgi_app.py).

### Gap / Проблема
Doc-stale в backlog story после pkg-000035; расхождение только с backlog-файлом (audit F1 MEDIUM).

### AC/DoD
- [ ] (P0) `Status` → 🟢 Done (волна pkg-000035); остаток G-1 → ссылка на [SEC-01b](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md).
- [ ] (P0) AC `[x]` для доставленного: eid/start, callback, 429 envelope, cooldown policy, config+tests.
- [ ] (P0) Scope §`phone/request` — пометка «вынесен в SEC-01b» (не доставлено этой волной).
- [ ] (P0) «Точки в коде» → as-built (`rate_limit*.py`, dependency, wiring); убрать «отсутствует».
- [ ] (P1) Ссылка на split-analysis [`sec-01-g1-rate-limit-split-2026-06-26.md`](../../../../../../analysis/sec-01-g1-rate-limit-split-2026-06-26.md).

### Где менять код
- `doge-identity-service/docs/tasks/backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md`

### Out of scope
- Pipeline story (уже 🟢), runtime code, [`04-security.md`](../../../../../../../runtime-docs/04-security.md) (t09 may touch §8).
- `identity-active-package.current.yaml`, pkg-000035 yaml.
- SEC-01b materialize.

### Проверка
```bash
grep -n "Status\|Todo\|Done\|rate-limiter\|SEC-01b" \
  doge-identity-service/docs/tasks/backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md
```
