# 21. Verification boolean, node-selected integration, audit log

Parent: docs/requirements backlog/REQ7-DOGEstonia-Threads-Entity-Social-Governance.md §0, §5.4, T-REQ7-05, D4, D28, D31, AC-REQ7-04  
Parent-id: doge-threads-entity-social-governance  
Siblings: doge-complaints-gateway/docs/requirements/52-issue-thread-context-and-node-verification.md (contract: pack names validation type and integration name; this service runs them and does not own the pack; no API parameters in that pack lock); doge-threads/docs/requirements/01-entity-thread-core.md (contract: callers receive the user’s **verified boolean** only); spa-app/docs/requirements/17-issue-thread-feed-ux-and-reactions.md (contract: TBD-question — spa starts the flow; this service performs it)  
Status: Draft — awaiting PA.2 (shell scope 2026-09-21; Part A locks applied — expose verified boolean this wave)  
Related algorithms parent: docs/requirements backlog/REQ8-DOGEstonia-Threads-Metrics-Voice-Governance.md (voice profile aggregate later — not this child’s AC)  
Architecture: [docs/architecture/TECH-ARCH-threads-verification-boolean.md](../architecture/TECH-ARCH-threads-verification-boolean.md)  
Interview: [docs/analysis/zeya888.req-target-tech-arch-interview-21-verification-boolean-and-audit-2026-09-21.md](../analysis/zeya888.req-target-tech-arch-interview-21-verification-boolean-and-audit-2026-09-21.md)  

Дата: 2026-09-21  
Проект: doge-identity-service  
Фокус: shell — исполнить верификацию ноды; **this wave** отдать потребителям method-opaque **verified boolean** + лог. Legacy `phone_verified` may coexist. Метрики/алгоритмы не здесь (REQ8). Prefer extending existing consumer surface; **do not invent a new path**

---

## 1) Goal

Identity не решает, телефон это или eID. Нода задаёт тип валидации и название интеграции в своём pack (gateway sibling). Параметры API в этот lock не входят. Этот сервис проводит ту интеграцию, пишет лог попытки и **в этой волне** отдаёт другим сервисам method-opaque **verified boolean** пользователя. Этот булеан не раскрывает, как верификация получена. Сегодняшний `phone_verified` — legacy parallel, **не** достаточный единственный consumer contract после этой REQ.

## 2) Scope / Out of scope

### In scope

- Execute the integration the node configured (`phone` or `eID`, named integration). The node pays that provider (parent §5.4). API parameters are not part of this pack lock.
- Persist success as the user’s **verified boolean**. Consumers read that name. They do not receive provider payloads or a method-named flag as the sole contract.
- **This wave:** expose that verified boolean on the consumer surface used by gateway / threads / spa (prefer extend existing `GET /me` response — **no new path invented**). Exact JSON field string for the boolean remains Open (product name locked: verified boolean).
- Legacy `phone_verified` may remain in the same response during transition; it must not be the only flag consumers check after this REQ (parent D4).
- Audit log of the attempt: who, which provider, success or failure. Phone and eID logs already exist (see verified state). This REQ requires that a node-selected integration still produces such a log. The log may name the provider; the verified boolean must not.
- Uus Veerenni target: pack validation type = phone. The consumer-facing flag is still named verified boolean.
- Callers (gateway submit, threads write, spa before write) use the verified boolean only.

### Out of scope

- Defining the pack block (gateway 52).
- Thread rules, voice weight, reactions.
- Landing configuration.
- Inventing a **new** HTTP path (extending existing `/me` is allowed).
- Appointing moderators.
- Voice profile aggregate / sanction ladder — **REQ8**.

## 3) Verified current state

| Fact | Path |
|------|------|
| `GET /me` includes `phone_verified` | `src/core/api/me_response.py:31` default false; `:46` from profile |
| `account_status` is always `"active"` in that builder | `src/core/api/me_response.py:36`; lines 38–51 do not overwrite it from the profile |
| Phone attempt audit | `src/core/api/handlers.py:114-142` `_log_phone_audit` (`provider`, `success`, `failure_reason`) |
| eID attempt audit | `src/core/api/handlers.py:145-176` `_log_eid_audit` (early return if repo missing at 160; event written after) |
| Gateway ignores pack and requires phone | `doge-complaints-gateway/src/core/identity/verification_gate.py:19-25` |
| Phone flow is the active gate in the identity requirements index | `docs/requirements/README-index.md` row 19: “Реализовано (активный гейт верификации)”; eID rows 11–13, 17–18 are not marked as the active gate |

Unknown: a config intake on this service that already accepts “node pack says use this validation type and this integration name”. Not seen in `me_response.py`. No field named verified boolean in the files cited above.

## 4) Target behavior

1. A node whose pack says phone uses the phone integration and sets the user’s verified boolean only after success. Uus Veerenni is this case. The flag does not say “phone”.
2. A node whose pack says eID uses an eID integration named in that pack. Failure does not set the boolean. Callers still see the same verified boolean, not a second method bit.
3. Every attempt is logged with the provider name. Existing phone and eID audit functions are the precedent, not a new event schema.
4. threads and gateway do not receive provider secrets, raw phone numbers, or the method in the check result. Gateway already keeps story authors as opaque ids (primer privacy invariant; parent D19).
5. `account_status: "active"` is not the verified boolean. Sanctions that suspend an account are a different ladder — **REQ8** §5.4 (sanction ladder) — and are not implemented by this boolean.
6. After this wave, consumers must be able to read a method-opaque verified boolean. `phone_verified` alone is insufficient as the sole contract (legacy may coexist).

## 5) Acceptance criteria

1. AC-ID-THR-01: Draft does not mandate a **new** HTTP path. Prefer extending the existing consumer surface (`GET /me`). Exact JSON field string for the verified boolean is Open; product name is locked.
2. AC-ID-THR-02: This service executes verification; the gateway pack sibling defines validation type and integration name, not API parameters (parent §5.4, D4).
3. AC-ID-THR-03: **This wave** the consumer contract **includes** the verified boolean plus an audit log. The boolean does not disclose method. Provider payloads are not part of the check result. Legacy `phone_verified` may coexist but is not sufficient alone (parent D4, AC-REQ7-04).
4. AC-ID-THR-04: Uus Veerenni example is phone. The requirement still allows another node to select `eID` without rewriting threads.
5. AC-ID-THR-05: Existing phone and eID audit functions are cited as the logging precedent (`handlers.py:114-176`).

## 6) Open questions

- How the pack’s validation type and integration name reach this service (sibling gateway 52). No route in parent. API parameters are not part of the lock.
- Exact JSON field name for the verified boolean on the wire (product name locked).
- Whether eID runtime is available for a node that selects it. Index row 19 says phone is the active gate; eID rows are not marked implemented as the active gate.

## 7) Dependencies

- Parent §5.4, T-REQ7-05, D4, D28, AC-REQ7-04.
- gateway 52 owns the pack policy.
- threads 01 and spa 17 only consume the verified boolean.
- **REQ8** [`docs/requirements backlog/REQ8-DOGEstonia-Threads-Metrics-Voice-Governance.md`](../../../docs/requirements%20backlog/REQ8-DOGEstonia-Threads-Metrics-Voice-Governance.md) may later replace raw-signal voice source with an identity profile aggregate (seam); sanction ladder lives there (§5.4) — not required for this shell child.
