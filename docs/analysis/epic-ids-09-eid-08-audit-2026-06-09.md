# Жёсткий аудит исполнения STORY-IDS-EID-08 (SessionSecretBox для PKCE code_verifier)

> **Дата:** 2026-06-09
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-EID-08-session-secret-box`](../tasks/backlog-stories/STORY-IDS-EID-08-session-secret-box.md) vs фактический код. Исполнена под **EPIC-IDS-09-eid-verification** (pkg-000021), 5 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): EPIC-IDS-09, Текущая волна — pkg-000021, STORY-IDS-EID-08 🟢 (стр.11,33).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Модуль | `src/core/security/session_secret.py` (1 файл, 50 строк) |
| Порт + реализация | `SessionSecretBox` (Protocol, `@runtime_checkable`), `FernetSessionSecretBox`, `SessionSecretError`, `build_session_secret_box` ([session_secret.py:15-50](../../src/core/security/session_secret.py)) |
| Крипто-основа | `cryptography.fernet.Fernet`; зависимость `cryptography>=42.0.0` объявлена ([pyproject.toml:17](../../pyproject.toml)), установлена 48.0.0 ✅ |
| Конфиг-ключ | `EID_SESSION_ENC_KEY` читается ([schema.py:123](../../src/core/config/schema.py)); pilot fail-fast ([schema.py:138](../../src/core/config/schema.py)); demo-дефолт ([schema.py:146-147](../../src/core/config/schema.py)) |
| Проводка | `ProviderRuntime.secret_box: SessionSecretBox | None` ([runtime.py:20](../../src/core/providers/runtime.py)); `build_session_secret_box(...)` для всех профилей ([runtime_factory.py:27,33](../../src/core/providers/runtime_factory.py)) |
| Тесты | [test_session_secret_box.py](../../tests/test_session_secret_box.py) — 8; +2 в [test_config_schema.py:130-169](../../tests/test_config_schema.py) |
| **Offline-сюита** | **254 passed, 9 skipped** ✅ (было 244 → +10) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-09, pkg-000021) | Факт | Статус |
|--------------------------------|------|--------|
| t01 session secret box fernet port | `SessionSecretBox` (Protocol) + `FernetSessionSecretBox` (`seal`/`open`, tamper→`SessionSecretError`) + `build_session_secret_box` ([session_secret.py:19-50](../../src/core/security/session_secret.py)) | 🟢 |
| t02 eid session enc key config pilot failfast | `EID_SESSION_ENC_KEY` required в pilot (`ConfigError`), demo-дефолт `_DEMO_EID_SESSION_ENC_KEY` ([schema.py:20,123,138,146-147](../../src/core/config/schema.py)) | 🟢 |
| t03 session secret box provider runtime wire | слот `ProviderRuntime.secret_box`; фабрика строит и кладёт ([runtime.py:20](../../src/core/providers/runtime.py), [runtime_factory.py:27,33](../../src/core/providers/runtime_factory.py)) | 🟢 |
| t04 offline session secret box tests | 8 тестов (round-trip / tamper / key-separation / demo-default / pilot-failfast / pilot-accept / runtime-wire / runtime-key-not-eid-secret) | 🟢 |
| t05 story acceptance verification | AC 5/5 (см. §2); pipeline-story `Status: 🟢 Done` (стр.7), t05 AC `[x]` | 🟢 |
| **STORY-IDS-EID-08** | SessionSecretBox primitive + slot | **🟢 Done** |

Индекс держит эпик корректно: Текущая волна pkg-000021 «STORY-IDS-EID-08 🟢» ([bullrun-launch-index.md:11,33](../tasks/bullrun-launch-index.md)).

---

## 2. Сверка Acceptance Criteria story (по коду + тестам)

| AC | Факт (код + тест) | Вердикт |
|----|-------------------|---------|
| `SessionSecretBox` (порт + Fernet); `seal`/`open` обратимы; round-trip-тест | Protocol + `FernetSessionSecretBox.seal/open` ([session_secret.py:23-45](../../src/core/security/session_secret.py)); тест `test_fernet_session_secret_box_round_trip` (`open(seal(x))==x`, `token!=x`) | ✅ |
| `EID_SESSION_ENC_KEY` обязателен в pilot (`ConfigError`), допустим дефолт в demo | pilot_required tuple ([schema.py:138](../../src/core/config/schema.py)); demo fallback ([schema.py:146-147](../../src/core/config/schema.py)); тесты `test_pilot_missing_eid_session_enc_key_raises_config_error` (match `EID_SESSION_ENC_KEY`), `test_demo_profile_uses_ephemeral_default_when_env_unset` | ✅ |
| `secret_box` доступен провайдерам через `ProviderRuntime` | runtime.py:20 + runtime_factory.py:33; тест `test_build_provider_runtime_wires_secret_box` (`isinstance FernetSessionSecretBox`) | ✅ |
| Ключ шифрования отделён от `eid_secret` (разные назначения) | `eid_secret` → HMAC ([hashing.py](../../src/core/security/hashing.py)); `eid_session_enc_key` → Fernet; отдельные поля конфига ([schema.py:122-123](../../src/core/config/schema.py)); тесты `test_build_session_secret_box_does_not_use_eid_secret`, `test_runtime_secret_box_uses_eid_session_enc_key_not_eid_secret` (токен под одним ключом не открывается другим) | ✅ |
| Offline-набор зелёный | **254 passed, 9 skipped** | ✅ |

**Вывод:** все 5 AC выполнены и покрыты тестами (8 dedicated + 2 в config-schema). F7 Authentigate-аудита (нет helper'а шифрования session-секретов после CLEANUP-02) закрыт provider-agnostic примитивом с **отдельным** ключом.

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F1** | MEDIUM | Doc-stale | Backlog-story помечена `Status: ⚪ Todo` (стр.6), AC-чекбоксы `[ ]` (стр.33-37) — реально 🟢 Done под `EPIC-IDS-09` (pkg-000021). Секция «Точки в коде (текущее состояние)» описывает пред-состояние («helper'а шифрования **нет** (убрали в CLEANUP-02)») — теперь helper есть. **Как закрыть:** Status ⚪→🟢, AC `[ ]`→`[x]`, обновить «Точки в коде» (добавить `session_secret.py`, `EID_SESSION_ENC_KEY`, слот в runtime). Рекуррентный паттерн (как у EID-04/05/06/07). | [`STORY-IDS-EID-08...md:6,25-29,33-37`](../tasks/backlog-stories/STORY-IDS-EID-08-session-secret-box.md) |
| **F2** | LOW | Doc-stale | Индекс декларирует «253 pytest offline» ([bullrun-launch-index.md:11](../tasks/bullrun-launch-index.md)), фактически **254 passed** (off-by-one). **Как закрыть:** синхронизировать число в строке Текущей волны. | [`bullrun-launch-index.md:11`](../tasks/bullrun-launch-index.md) |

Иных материальных findings нет. Наблюдения (severity none, по scope, **не gap**):
- **`_DEMO_EID_SESSION_ENC_KEY` — фиксированная константа** в исходнике ([schema.py:20](../../src/core/config/schema.py)), не эфемерный (per-process) ключ. Имя теста `..._uses_ephemeral_default...` неточно («ephemeral» ≠ хардкод-дефолт). Безопасно: ключ demo-only, в pilot не используется (guard fail-fast), комментарий это фиксирует ([schema.py:19](../../src/core/config/schema.py)). По scope story («demo — дефолтный/эфемерный допустим») — допустимо.
- **`secret_box` строится для всех профилей** (в отличие от `oidc`/`http_client`, которые non-mock-only). Корректно: PKCE-секреты нужны и в mock-флоу; слот `| None` сохранён для типовой гибкости, но фабрика всегда заполняет.
- **Реальное использование** (`start_flow` пишет `code_verifier_encrypted=seal(...)`, callback `open(...)`) — **вне scope EID-08** (отнесено к [EID-02](../tasks/backlog-stories/STORY-IDS-EID-02-real-eid-providers.md)). Поля `code_verifier_encrypted/_hash` в модели существуют ([models.py:49-50]), пишутся пока nullable — это ожидаемо, не gap данной story.

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **254 passed, 9 skipped** (было 244 → +10 EID-08-тестов), **ожидаемо** |
| Новый модуль `session_secret.py` | аддитивный; HMAC `hashing.py` и `eid_secret` не затронуты (ключи разделены) |
| `ProviderRuntime` | добавлен слот `secret_box`; `oidc`/`http_client`/`clock` без изменений |
| `load_config_from_env` | новое поле `eid_session_enc_key`; pilot-валидация расширена (+1 required), demo получает дефолт — существующие config-тесты зелёные (часть 254) |
| Сеть в offline | нет (крипто локальное, без сетевых клиентов) |
| eID-флоу (EID-01/05/06/07) | не затронут — сюита зелёная |

Регрессий не выявлено.

---

## 5. Итог

- **STORY-IDS-EID-08 — 🟢 исполнена полно:** provider-agnostic `SessionSecretBox` (Protocol + `FernetSessionSecretBox`, обратимые `seal`/`open`, tamper→`SessionSecretError`), отдельный ключ `EID_SESSION_ENC_KEY` (fail-fast в pilot, demo-дефолт), доступен через `ProviderRuntime.secret_box`, ключ отделён от HMAC `eid_secret`. AC 5/5, 8 dedicated-тестов. F7 Authentigate-аудита закрыт.
- **Findings:** **F1 (MEDIUM, doc-stale backlog-story)** — рекуррентный (Status ⚪→🟢 + «точки в коде»); **F2 (LOW)** — индекс 253 vs факт 254 offline.
- Наблюдения (demo-key хардкод, secret_box для всех профилей, использование в EID-02) — по scope, не gaps.

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; статусы 5 тасков и story сверены по коду (pipeline-story 🟢, t05 AC `[x]`).
- [x] AC 5/5 сверены по коду **и** тестам; разделение ключей подтверждено тестом cross-key (`wrong.open(token)` → `SessionSecretError`).
- [x] Регрессий нет; 244→254 (+10) объяснён; offline без сети.
- [x] Наблюдения (demo-key константа; secret_box для всех профилей; usage в EID-02) отделены от material findings (по scope).
- [x] F2 (off-by-one в индексе) пойман сверкой задекларированного числа с фактическим прогоном.
