# eID-подключение — POST-MVP (deferred, ждёт донейшнов)

> **Статус:** 🟦 **POST-MVP** — ждёт **донейшнов на оплату подписки SK**. **Не брать в работу**, пока не появится финансирование/решение вернуть eID. (заведено 2026-06-10)

## Почему post-MVP
Подключение боевого eID-провайдера (**Authentigate**, SK ID Solutions) — это **платные подписка/транзакции SK**. Включаем это, **когда появятся донейшны на оплату подписки** (post-MVP). До тех пор задачу «убедиться, что за аккаунтом реальный человек» решает более дешёвая **верификация телефона** (см. отдельный функционал phone-verification) — отсюда и отдельная папка, чтобы не мешать активному бэклогу, но и не потерять проделанную проработку.

## Что здесь лежит (декомпозиция EID-02)
| Story | Тема |
|-------|------|
| [STORY-IDS-EID-02](STORY-IDS-EID-02-real-eid-providers.md) | Umbrella: Authentigate provider (декомпозирована в EID-10…14) |
| [SPIKE-IDS-EID-09](SPIKE-IDS-EID-09-authentigate-demo-access.md) | Demo-доступ Authentigate + подтверждение рантайма (внешнее) |
| [STORY-IDS-EID-10](STORY-IDS-EID-10-provider-settings-wiring.md) | Provider settings wiring |
| [STORY-IDS-EID-11](STORY-IDS-EID-11-authentigate-oidc-client.md) | Authentigate OIDC client (discovery + token exchange) |
| [STORY-IDS-EID-12](STORY-IDS-EID-12-authentigate-start-flow.md) | `start_flow`: PKCE + authorize-URL + session persistence |
| [STORY-IDS-EID-13](STORY-IDS-EID-13-authentigate-callback-mapping.md) | `handle_callback`: token + id_token + claims mapping |
| [STORY-IDS-EID-14](STORY-IDS-EID-14-authentigate-registration-tests-docs.md) | Go-live: регистрация + сквозные тесты + доки |

## Что НЕ отложено (осталось в активном бэклоге)
**Платформа провайдеров EID-01, EID-03…08** (`../STORY-IDS-EID-0X-*.md`) — уже **сделана (🟢 Done)**, код в репозитории. Это провайдер-агностичный каркас (дескрипторы, реестр, конфиг-спеки, OIDC-тулкит, SessionSecretBox, redirect-оркестрация). Он остаётся как фундамент: phone-verification строится **по тем же архитектурным паттернам** (а не на этих eID-классах напрямую — phone это отдельный функционал). Когда eID вернём — здешние стори собираются поверх готовой платформы.

## Связанные документы
- Аудит совместимости: [`authentigate-compatibility-audit-2026-06-07`](../../../analysis/authentigate-compatibility-audit-2026-06-07.md)
- Контекст потребностей кода: [`eid-provider-integration-needs-2026-06-07`](../../../analysis/eid-provider-integration-needs-2026-06-07.md)
- Эпик-индекс: [`EPIC-IDS-EID.md`](../eid/EPIC-IDS-EID.md)
- Мануал песочницы (на будущее): [`authentigate-sandbox-setup-howto`](../../../tech-requirements/authentigate-sandbox-setup-howto.md)
