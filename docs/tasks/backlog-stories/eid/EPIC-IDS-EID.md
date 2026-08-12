# EPIC-IDS-EID — eID-верификация и платформа провайдеров

> **ID:** `EPIC-IDS-EID` (alias `EPIC-IDS-09`) · **Статус:** 🟢 Платформа EID-01/03…08 Done; 🟦 подключение боевого eID — **POST-MVP** (заменено верификацией телефона) · **Тип:** Функциональный
> **Не декомпозирован** в pipeline — набор backlog-стори.
>
> 🟦 **Подключение боевого eID (Authentigate) — POST-MVP:** ждёт **донейшнов на оплату подписки SK** (это платные подписка/транзакции). До тех пор задачу «реальный уникальный человек» решает верификация телефона. Connection-стори вынесены в [`eid-deferred/`](../eid-deferred/README.md). Платформа провайдеров (EID-01, 03…08) — 🟢 Done, переиспользуется как образец для phone-verification.

## Назначение
eID-верификация (подтверждение «за аккаунтом реальный уникальный человек») и **подключаемая платформа провайдеров**. Выбор MVP-провайдера — **Authentigate** (OIDC-gateway SK ID Solutions; eID Easy отложен как дорогой). Группа enabling-стори EID-03…08 расширяет архитектуру так, чтобы провайдеров можно было добавлять как plugin'ы под разные стандарты (OAuth2/OIDC/…); EID-02 — capstone, собирающий Authentigate поверх этой платформы.

## Почему отдельная группа enabling-стори
Аудит [`authentigate-compatibility-audit-2026-06-07`](../../../analysis/authentigate-compatibility-audit-2026-06-07.md) показал: гайд совместим на уровне adapter, но рабочему боевому провайдеру мешают разрывы уровня платформы (реестр/конфиг/контракт/redirect/OIDC/крипто). Их решаем **доработкой абстракций, не костылями** (см. §6 аудита), иначе каждый новый провайдер будет плодить `if`-ы в ядре.

## Stories

### Платформа провайдеров (enabling) — 🟢 готова
| Story | Тема | Гэпы аудита | Статус |
|-------|------|-------------|--------|
| [STORY-IDS-EID-01](STORY-IDS-EID-01-eid-verification-flow.md) | eID-флоу (start/callback/orchestration) на mock | — | 🟢 Done |
| [STORY-IDS-EID-03](STORY-IDS-EID-03-provider-plugin-backbone.md) | Plugin-платформа: дескрипторы, DI-контекст, реестр-guard | F5, F9, F13-guard | 🟢 Done |
| [STORY-IDS-EID-04](STORY-IDS-EID-04-provider-owned-config.md) | Provider-owned configuration | F3, F4, F10 | 🟢 Done |
| [STORY-IDS-EID-05](STORY-IDS-EID-05-canonical-provider-contract.md) | Канон контракта: ошибки + идентичность субъекта | F2, F12 | 🟢 Done |
| [STORY-IDS-EID-06](STORY-IDS-EID-06-browser-callback-redirect.md) | Браузерный callback: redirect + динамический роут | F1 🔴, F6, F11 | 🟢 Done |
| [STORY-IDS-EID-07](STORY-IDS-EID-07-oidc-toolkit.md) | Provider-agnostic OIDC-тулкит (discovery/JWKS/id_token) | F8 | 🟢 Done |
| [STORY-IDS-EID-08](STORY-IDS-EID-08-session-secret-box.md) | SessionSecretBox для PKCE code_verifier | F7 | 🟢 Done |

### Подключение Authentigate (декомпозиция EID-02) — 🟦 POST-MVP, ждёт донейшнов на оплату SK (см. [eid-deferred/](../eid-deferred/README.md))
| Story | Тема | Контрактный шов | Статус |
|-------|------|-----------------|--------|
| [SPIKE-IDS-EID-09](../eid-deferred/SPIKE-IDS-EID-09-authentigate-demo-access.md) | Demo-доступ + подтверждение рантайма (внешнее) | F14 | ⚪ Todo |
| [STORY-IDS-EID-10](../eid-deferred/STORY-IDS-EID-10-provider-settings-wiring.md) | Provider settings wiring (типизированные настройки в `ProviderRuntime`) | шов платформы | ⚪ Todo |
| [STORY-IDS-EID-11](../eid-deferred/STORY-IDS-EID-11-authentigate-oidc-client.md) | Authentigate OIDC client: discovery + token exchange | vendor transport | ⚪ Todo |
| [STORY-IDS-EID-12](../eid-deferred/STORY-IDS-EID-12-authentigate-start-flow.md) | `start_flow`: PKCE + authorize-URL + session persistence | request-half | ⚪ Todo |
| [STORY-IDS-EID-13](../eid-deferred/STORY-IDS-EID-13-authentigate-callback-mapping.md) | `handle_callback`: token + id_token + claims mapping | response-half | ⚪ Todo |
| [STORY-IDS-EID-14](../eid-deferred/STORY-IDS-EID-14-authentigate-registration-tests-docs.md) | Go-live: регистрация + сквозные тесты + доки | assembly | ⚪ Todo |
| [STORY-IDS-EID-02](../eid-deferred/STORY-IDS-EID-02-real-eid-providers.md) | **Umbrella:** декомпозирована в EID-10…14 | EID-1, EID-2 | 🔵 Декомпозирована |

## Порядок реализации

**Платформа (сделано):** EID-03 (фундамент) → параллельно EID-04 / EID-05 / EID-07 / EID-08 → EID-06 (опирается на коды из EID-05).

**Authentigate (текущее):** EID-10 (закрыть шов настроек) → EID-11 (OIDC client) → параллельно EID-12 (start_flow) и EID-13 (callback) → EID-14 (регистрация+тесты+доки). **SPIKE-09** — параллельно с самого начала (long-lead запрос доступа у SK), гейтит только live-тест EID-14.

```
[платформа: EID-03 → {04,05,07,08} → 06]  🟢
                     │
EID-10 (settings) ── EID-11 (client) ──┬─ EID-12 (start_flow) ─┐
                                       └─ EID-13 (callback) ────┼─ EID-14 (go-live)
SPIKE-09 (demo, параллельно) ───────────────────────────────────┘ (gate live-test)
```

## Связь
Аудит совместимости [`authentigate-compatibility-audit-2026-06-07`](../../../analysis/authentigate-compatibility-audit-2026-06-07.md) (§6 — архитектурные решения), контекст потребностей [`eid-provider-integration-needs-2026-06-07`](../../../analysis/eid-provider-integration-needs-2026-06-07.md), гайд [`Authentigate Integration guide.md`](../../../tech-requirements/Authentigate%20Integration%20guide.md), парадигма [06-eid-providers](../../../runtime-docs/06-eid-providers.md).
