# STORY-IDS-CLEANUP-04 — Глубокая сверка спеков (gateway-копии + eID drift + crypto naming)

## Meta
- **Key:** `STORY-IDS-CLEANUP-04-spec-reconciliation`
- **Epic:** `EPIC-IDS-CLEANUP` (см. [EPIC-IDS-CLEANUP.md](EPIC-IDS-CLEANUP.md))
- **Status:** ⚪ Todo
- **Тип:** Doc task (только документация; критерий — Definition of Done, а не code-AC)
- **Источник:** [`identity-backend-full-audit-2026-06-24`](../../../analysis/identity-backend-full-audit-2026-06-24.md) — HD-1, §4 (📝 doc-stale), G-4
- **Зависит от:** — (можно в любой момент; логически после CLEANUP-03)

## Зачем простыми словами
Аудит 2026-06-24 закрыл бо́льшую часть рассинхрона документации точечными правками (10/13/08/09 + новый 19-phone и т.п.). Но три блока спеков нельзя было поправить «в строчку» — они требуют либо переписывания против реального кода, либо отдельного решения (ADR). На время аудита их пометили **баннерами сверху** (reference-only / eID-deferred), но **тела документов остались старыми**. Эта story доводит сверку до конца: каждый из трёх блоков либо переписывается под факт, либо формально депрекейтится/фиксируется решением.

Это **чисто документная** задача: код — истина, его не трогаем (см. решения Q1–Q4 аудита, §0).

## Scope

### 1. Gateway-копии: переписать ИЛИ депрекейтнуть (HD-1)
[`requirements/06-technical-scaffold.md`](../../../requirements/06-technical-scaffold.md), [`requirements/07-env-configuration-spec.md`](../../../requirements/07-env-configuration-spec.md) и **ВСЕ** [`tech-requirements/impl-epic-01`](../../../tech-requirements/impl-epic-01-scaffold-config-launch.md)…[`impl-epic-06`](../../../tech-requirements/impl-epic-06-testing-architecture.md) скопированы из `doge-complaints-gateway` — описывают истории/кластеризацию (`/intake/stories`, `stories`/`doge_issues`-таблицы, `ServiceTokenAuth`, `CLUSTER_*`), а **не** identity. Сейчас несут только баннер «reference-only».
- **DoD:** по каждому файлу принять и **единообразно** исполнить одно из двух:
  - **(a) переписать** против реального кода identity ([`src/`](../../../../src/) — роуты `/me`/`/auth/*`/`/oauth/*`, `BearerTokenAuth`/Supabase-JWT, `ProfileRepository`/`VerificationSessionStore`, 3 identity-таблицы); **или**
  - **(b) формально депрекейтнуть/удалить** с явным указателем на настоящий SSOT: [`src/`](../../../../src/) + [`runtime-docs/`](../../../runtime-docs/) + [`requirements/19-phone-verification-flow.md`](../../../requirements/19-phone-verification-flow.md).
- Решение фиксируется в шапке story-результата или ADR; запрещён смешанный исход (часть переписана, часть с висящим reference-only баннером без указателя).

### 2. eID-спеки: сверить тело с descriptor-рефактором и реальными redirect-маркерами
[`requirements/11-eid-verification-flow.md`](../../../requirements/11-eid-verification-flow.md), [`12-authentigate-oidc-client.md`](../../../requirements/12-authentigate-oidc-client.md), [`17-eid-provider-abstraction.md`](../../../requirements/17-eid-provider-abstraction.md), [`18-eideasy-provider.md`](../../../requirements/18-eideasy-provider.md) несут баннер «eID DEFERRED», но **тела отстали** от descriptor/registry-рефактора и используют устаревшие redirect-маркеры (`?context=` / `?error=`).
- Реальный код: маркеры `?eid_status=verified` и `?eid_status=error&eid_error=<code>` ([`eid_callback.py:52-60`](../../../../src/core/api/eid_callback.py)); провайдеры — descriptor-паттерн ([`src/core/providers/`](../../../../src/core/providers/)).
- **DoD:** тела 11/12/17/18 приведены к descriptor-паттерну и фактическим redirect-маркерам; статус **eID-deferred** при этом сохранён ясным (баннер + текст не создают впечатления «подключено»).

### 3. Crypto-naming: подтвердить ADR-ом и применить (G-4)
Спеки 07/11/12/16 требуют env `CODE_VERIFIER_ENCRYPTION_KEY` и `aes_gcm_encrypt`; реальный код — env `EID_SESSION_ENC_KEY` ([`schema.py:156`](../../../../src/core/config/schema.py)) и Fernet (`FernetSessionSecretBox`, [`session_secret.py:28-45`](../../../../src/core/security/session_secret.py)).
- **DoD:** через ADR зафиксировать, принят ли переименование (`EID_SESSION_ENC_KEY`) + Fernet (вместо AES-GCM) как решение:
  - **если да** — обновить спеки [`07`](../../../requirements/07-env-configuration-spec.md), [`11`](../../../requirements/11-eid-verification-flow.md), [`12`](../../../requirements/12-authentigate-oidc-client.md), [`16`](../../../requirements/16-security-privacy-observability.md) на реальные имена/алгоритм;
  - **если нет** — зафиксировать гэп (он активируется только при подключении живого eID — отложено, поэтому сейчас это doc-решение, а не code-fix).

## Вне scope
- **Изменения кода** — это документная задача (код = истина по Q1–Q4 аудита).
- **Точечные правки, уже выполненные аудитом** — `requirements/10`, `13`, `08`, `09`, новый `19-phone-verification-flow.md`, баннеры и пр. (см. §7 аудита). **Не переделывать.**
- Code-гэпы G-1/G-2/G-3/G-5 — у них свои треки (только отчёт, Q2).

## Definition of Done (проверяемые doc-state чеки)
- [ ] **Gateway-копии:** в `requirements/06`, `07` и каждом `impl-epic-01..06` исполнен единый исход — либо тело переписано под identity-код (нет упоминаний `stories`/`doge_issues`/`cluster_*`/`doge-complaints-gateway`), либо файл депрекейтнут с явным указателем на SSOT (`src/` + `runtime-docs/` + `19-phone-verification-flow.md`). Висящих reference-only баннеров без разрешения нет.
- [ ] **eID-спеки:** в `requirements/11`, `12`, `17`, `18` отсутствуют маркеры `?context=` / `?error=`; присутствуют `?eid_status=verified` / `?eid_status=error&eid_error=`; тела ссылаются на descriptor-паттерн (`src/core/providers/`); статус eID-deferred остаётся явным.
- [ ] **Crypto-naming:** заведён ADR с решением по `EID_SESSION_ENC_KEY` + Fernet vs AES-GCM. При «принято» — спеки 07/11/12/16 не содержат `CODE_VERIFIER_ENCRYPTION_KEY`/`aes_gcm_encrypt`, а содержат реальные имена/алгоритм. При «не принято» — гэп зафиксирован со ссылкой на трек активации (при подключении живого eID).
- [ ] Нет новых противоречий между затронутыми спеками и [`runtime-docs/`](../../../runtime-docs/) / [`src/`](../../../../src/).

## Парадигма-якорь
[`identity-backend-full-audit-2026-06-24`](../../../analysis/identity-backend-full-audit-2026-06-24.md) (HD-1, §4, G-4), [`src/`](../../../../src/), [`runtime-docs/`](../../../runtime-docs/).
