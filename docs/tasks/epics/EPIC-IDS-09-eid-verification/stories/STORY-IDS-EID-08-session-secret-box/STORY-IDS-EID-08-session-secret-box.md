# STORY-IDS-EID-08 — Защита session-секретов (SessionSecretBox) для PKCE code_verifier

## Meta
- **Key:** `STORY-IDS-EID-08-session-secret-box`
- **Parent Epic:** [`../../../../EPIC-IDS-09-eid-verification.md`](../../../../EPIC-IDS-09-eid-verification.md)
- **Epic alias (код/backlog):** `EPIC-IDS-EID`
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-EID-08-session-secret-box.md`](../../../../backlog-stories/eid/STORY-IDS-EID-08-session-secret-box.md)
- **Decision Ref:** [`../../../../backlog-stories/STORY-IDS-EID-08-session-secret-box.md`](../../../../backlog-stories/eid/STORY-IDS-EID-08-session-secret-box.md); [`authentigate-compatibility-audit-2026-06-07`](../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F7)
- **Источник:** аудит [`authentigate-compatibility-audit-2026-06-07`](../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F7)
- **Зависит от:** [STORY-IDS-EID-03-provider-plugin-backbone](../STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md) (`ProviderRuntime` экспонирует `secret_box`)

## Зачем простыми словами
OIDC с PKCE требует сохранить секрет `code_verifier` на старте флоу и достать его на callback (хранилище сессий не умеет update — всё пишется при создании). В модели сессии есть поле `code_verifier_encrypted`, но **helper'а шифрования нет** (его убрали в CLEANUP-02). Вводим маленький провайдер-агностичный примитив для защиты серверных session-секретов с **отдельным** ключом шифрования (не путать с HMAC `eid_secret`).

## Scope
- **`SessionSecretBox` (порт, новый `core/security/session_secret.py`):** `seal(plaintext) -> str` / `open(token) -> str`. Реализация на Fernet (`cryptography>=42`, уже в зависимостях).
- **Ключ:** новое env `EID_SESSION_ENC_KEY`; fail-fast required в `pilot` (по образцу pilot-валидации [`schema.py:114-127`](../../../../../../src/core/config/schema.py)); в `demo`/in-memory — дефолтный/эфемерный ключ допустим.
- **Использование провайдером:** `start_flow` пишет `code_verifier_encrypted = secret_box.seal(code_verifier)`, `code_verifier_hash = sha256(code_verifier)`; callback — `secret_box.open(...)`. (Само использование — в [EID-02](../../../../backlog-stories/STORY-IDS-EID-02-real-eid-providers.md); здесь — примитив + слот в `ProviderRuntime`.)

## Вне scope
- Логика PKCE/генерация challenge — адаптер Authentigate ([EID-02](../../../../backlog-stories/STORY-IDS-EID-02-real-eid-providers.md)).
- KMS/ротация ключей — за абстракцией порта (можно добавить позже без правки провайдеров).

## Решение владельца (зафиксировать)
PKCE `code_verifier` — одноразовый серверный секрет (TTL≈10 мин, БД-only). **Альтернатива MVP:** хранить открытым в `provider_session_data` и отложить шифрование. **Рекомендация:** ввести `SessionSecretBox` — provider-agnostic примитив (пригодится и для nonce), abstracts крипту для будущей ротации/KMS; **не** переиспользовать `eid_secret` (разделение ключей по назначению).

## Точки в коде (реализовано)
- `SessionSecretBox` + Fernet: [`session_secret.py`](../../../../../../src/core/security/session_secret.py) (`seal`/`open`, `build_session_secret_box`).
- Config: [`schema.py`](../../../../../../src/core/config/schema.py) — `eid_session_enc_key`, `EID_SESSION_ENC_KEY`, pilot fail-fast, demo ephemeral default.
- Runtime wire: [`runtime.py:19-21`](../../../../../../src/core/providers/runtime.py), [`runtime_factory.py:21-31`](../../../../../../src/core/providers/runtime_factory.py).
- Offline tests: [`tests/test_session_secret_box.py`](../../../../../../tests/test_session_secret_box.py) (8 tests).

## Точки в коде (до реализации, archival)
- Поля сессии: `code_verifier_encrypted`/`code_verifier_hash` (nullable) [`models.py:49-50`](../../../../../../src/core/domain/models.py).
- Односторонний HMAC: [`hashing.py:9`](../../../../../../src/core/security/hashing.py).
- Ключ был удалён в CLEANUP-02: [STORY-IDS-CLEANUP-02 E20](../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-02-placeholders-hardening.md).
- Store без update (всё пишется при `create`): [`contracts.py:43-54`](../../../../../../src/core/domain/contracts.py).
- Pilot-валидация конфига (образец fail-fast): [`schema.py:114-127`](../../../../../../src/core/config/schema.py).
- `ProviderRuntime.secret_box` slot exists but always `None`: [`runtime.py:20`](../../../../../../src/core/providers/runtime.py), [`runtime_factory.py:30`](../../../../../../src/core/providers/runtime_factory.py).

## Acceptance Criteria
- [x] Есть `SessionSecretBox` (порт + Fernet-реализация); `seal`/`open` обратимы; round-trip-тест.
- [x] `EID_SESSION_ENC_KEY` обязателен в `pilot` (понятная `ConfigError` при отсутствии), допустим дефолт в `demo`.
- [x] `secret_box` доступен провайдерам через `ProviderRuntime`.
- [x] Ключ шифрования отделён от `eid_secret` (разные назначения).
- [x] Offline-набор зелёный.

## Парадигма-якорь
[04-security](../../../../../runtime-docs/04-security.md) (секреты, ключи), [05-data-model](../../../../../runtime-docs/05-data-model.md) (поля сессии).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-09-08-t01-session-secret-box-fernet-port`](./task-ids-09-08-t01-session-secret-box-fernet-port/README.md) | pkg-000021 |
| 2 | [`task-ids-09-08-t02-eid-session-enc-key-config-pilot-failfast`](./task-ids-09-08-t02-eid-session-enc-key-config-pilot-failfast/README.md) | pkg-000021 |
| 3 | [`task-ids-09-08-t03-session-secret-box-provider-runtime-wire`](./task-ids-09-08-t03-session-secret-box-provider-runtime-wire/README.md) | pkg-000021 |
| 4 | [`task-ids-09-08-t04-offline-session-secret-box-tests`](./task-ids-09-08-t04-offline-session-secret-box-tests/README.md) | pkg-000021 |
| 5 | [`task-ids-09-08-t05-story-acceptance-verification`](./task-ids-09-08-t05-story-acceptance-verification/README.md) | pkg-000021 |
