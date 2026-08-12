# SPIKE-IDS-EID-09 — Demo-доступ Authentigate и подтверждение рантайм-деталей

## Meta
- **Key:** `SPIKE-IDS-EID-09-authentigate-demo-access`
- **Epic:** `EPIC-IDS-09` (alias `EPIC-IDS-EID`)
- **Status:** ⚪ Todo · **Тип:** Spike / внешняя зависимость (не код)
- **Источник:** аудит [`authentigate-compatibility-audit-2026-06-07`](../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F14), §4
- **Зависит от:** — (можно вести параллельно; **обязателен до live-теста** [EID-02](STORY-IDS-EID-02-real-eid-providers.md))

## Зачем простыми словами
Часть деталей Authentigate нельзя узнать из кода — только из реального demo-окружения SK. Этот спайк — получить demo-доступ и подтвердить рантайм-детали, на которых нельзя «гадать», прежде чем их хардкодить в адаптере.

## Scope (получить и зафиксировать)
- **Demo-доступ:** запросить через e-Service Portal (Demo Plan, бесплатно), указать test environment details, дождаться подтверждения.
- **Регистрация demo-клиента:** Client ID/Secret, Redirect URI (`https://<public-host>/auth/authentigate/callback`), Allowed IPs, Allowed Countries=EE, Service Name=DOGEstonia.
- **Подтвердить рантайм:**
  - точный JSON-ключ `attributes.*` в `id_token` (в доках возможна опечатка `attribues`);
  - доступность `client_secret_basic` (иначе понадобится `private_key_jwt` + управление ключами);
  - разрешённые для нашего клиента `acr_values` (Authentigate отвергает неразрешённые);
  - формат `scope` (короткие имена vs полные claim-URL).
- **Операционка:** публичный host/туннель для `redirect_uri`; Smart-ID **Qualified (Q)** demo-аккаунты (Basic/NQ не работают).
- **Коммерческое:** Starter-план, setup fee, минимальный срок, требования к юр.лицу.

## Вне scope
- Любой код адаптера — [EID-02](STORY-IDS-EID-02-real-eid-providers.md) и enabling-стори EID-03…08.

## Acceptance Criteria
- [ ] Demo-доступ получен, demo-клиент зарегистрирован, credentials у команды.
- [ ] Подтверждены: ключ `attributes.*`, `client_secret_basic`, разрешённые `acr_values`, формат `scope` — результаты записаны в анализ-зону/обновление гайда.
- [ ] Подтверждены demo Smart-ID Q аккаунты и публичный redirect host.
- [ ] Зафиксированы коммерческие условия (или открытые вопросы к SK).

## Парадигма-якорь
[06-eid-providers](../../../runtime-docs/06-eid-providers.md); гайд [`Authentigate Integration guide.md`](../../../tech-requirements/Authentigate%20Integration%20guide.md) §5, §6, §21.
