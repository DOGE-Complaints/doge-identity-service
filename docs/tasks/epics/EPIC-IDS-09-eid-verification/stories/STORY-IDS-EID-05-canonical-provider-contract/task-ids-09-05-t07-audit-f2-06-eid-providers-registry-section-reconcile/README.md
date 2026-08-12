## Task workspace — `task-ids-09-05-t07-audit-f2-06-eid-providers-registry-section-reconcile`

- Story: [`../STORY-IDS-EID-05-canonical-provider-contract.md`](../STORY-IDS-EID-05-canonical-provider-contract.md)
- Audit source: [`../../../../../../analysis/epic-ids-09-eid-05-audit-2026-06-08.md`](../../../../../../analysis/epic-ids-09-eid-05-audit-2026-06-08.md) (F2)

---
**Приоритет:** P1  
**Сложность:** M  
**Статус:** done  
**Wave:** `override epic_ids_09_eid_05_audit_2026_06_08`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-09-eid-05-audit-2026-06-08.md`](../../../../../../analysis/epic-ids-09-eid-05-audit-2026-06-08.md) §F2  
---

## Task: fix — reconcile 06-eid-providers registry section with EID-03/04 facts (F2)

### Цель
Устранить внутреннее противоречие в [`06-eid-providers.md`](../../../../../../../docs/runtime-docs/06-eid-providers.md): верх документа (F12 + `EidErrorCode`) актуален после EID-05, секция реестра/провайдеров — pre-EID-03/04 (KeyError, «только mock», hardcode `providers.py`).

### Почему это важно
Runtime-doc — парадигма-якорь story EID-05; противоречивые секции реестра вводят операторов в ошибку при intake EID-02/EID-06 и маскируют уже реализованную plugin-платформу.

### Факты из кода
1. Stale registry narrative: [`06-eid-providers.md:41`](../../../../../../../docs/runtime-docs/06-eid-providers.md) — «зарегистрирован **только `mock`**».
2. Stale KeyError trap: [`06-eid-providers.md:51`](../../../../../../../docs/runtime-docs/06-eid-providers.md) — «`get_active()` упадёт с `KeyError`».
3. Stale provider table: [`06-eid-providers.md:48-49`](../../../../../../../docs/runtime-docs/06-eid-providers.md) — «authentigate — конфиг есть, кода нет».
4. Stale add-provider step: [`06-eid-providers.md:62`](../../../../../../../docs/runtime-docs/06-eid-providers.md) — «словарь жёстко содержит только mock» в `providers.py`.
5. Descriptor catalog: [`registry_builder.py:10-14`](../../../../../../../src/core/providers/registry_builder.py) — `MOCK_EID_DESCRIPTOR`, `EIDEASY_EID_DESCRIPTOR`, `AUTHENTIGATE_EID_DESCRIPTOR`.
6. Lazy registry: [`registry_builder.py:27-40`](../../../../../../../src/core/providers/registry_builder.py) — `build_registry(runtime)`.
7. Wiring: [`providers.py:96`](../../../../../../../src/core/infrastructure/providers.py) — `registry = build_registry(provider_runtime)`.
8. Guard (not KeyError): [`registry.py:16-21`](../../../../../../../src/core/providers/registry.py) — `ProviderNotRegisteredError`.
9. EID-05 sections already correct: [`06-eid-providers.md:19-37`](../../../../../../../docs/runtime-docs/06-eid-providers.md) — каноническая идентичность + `EidErrorCode`.

### Gap / Проблема
Doc-drift / internal contradiction в runtime-doc; накопленный debt EID-03/04, всплывший при правке 06 в EID-05 (audit F2 MEDIUM).

### AC/DoD
- [x] (P0) §«Реестр и выбор активного» описывает `build_registry`, дескрипторы, `ProviderNotRegisteredError` (не KeyError / не «только mock»).
- [x] (P0) Таблица провайдеров отражает факт: mock ✅; eideasy/authentigate — descriptor + `config_spec` (runtime build deferred до EID-02), не «кода нет».
- [x] (P0) Убрать/заменить «⚠️ Ловушка (gap EID-1)… KeyError» на guard + `ConfigError` narrative.
- [x] (P0) «Как добавить провайдера» шаг 2 — descriptor + `ALL_EID_PROVIDER_DESCRIPTORS` / `build_registry`, не hardcode dict в `providers.py`.
- [x] (P1) Секции F12 + `EidErrorCode` (EID-05) **не** регрессировать.
- [x] (P1) Story AC #3 doc traceability (06 как контракт-якорь).

### Где менять код
- `doge-identity-service/docs/runtime-docs/06-eid-providers.md` (§39-64, 59-64)

### Out of scope
- Backlog sync (t06).
- Код, pytest.
- Секция «Текущее состояние целиком» про 01-api stubs (отдельный drift, не в audit F2).
- Реализация EID-02 runtime providers.

### Проверка
```bash
grep -n "KeyError\|только \`mock\`\|providers.py.*только mock\|gap EID-1" \
  doge-identity-service/docs/runtime-docs/06-eid-providers.md
grep -n "build_registry\|ProviderNotRegisteredError\|ALL_EID_PROVIDER_DESCRIPTORS" \
  doge-identity-service/docs/runtime-docs/06-eid-providers.md
```
