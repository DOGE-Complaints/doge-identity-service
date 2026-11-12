# 01. Миссия сервиса

> **Статус:** НЕ реализовано. Requirements document.
> **Сервис:** `doge-identity-service`
> **Источник:** `docs/Identify/identity-backend.md`, kick-off интервью CTO-CPO 2026-05-25

---

## Product intent

`doge-identity-service` — слой доверия и авторизации DOGEstonia.

Сервис отвечает на один вопрос: **"Можно ли этому пользователю совершить это действие?"**

Он не хранит stories, не кластеризует контент, не управляет публичными данными. Его единственная роль — знать, кто перед ним, верифицирован ли этот человек как уникальный гражданин, и выдать токен доступа другим сервисам.

---

## Целевой результат

- Пользователь входит в DOGEstonia через email/password или magic link (Supabase Auth).
- Однократно подтверждает личность через эстонский eID (Authentigate).
- После верификации — может подавать stories, голосовать и совершать любые civic-действия.
- Custom GPT (ChatGPT) получает доступ к DOGEstonia API через стандартный OAuth 2.0 Authorization Code Flow.
- Другие сервисы (doge-complaints-gateway) валидируют Bearer-токен от identity-service и принимают решения об авторизации.

---

## Value proposition

- **Для граждан:** один вход, одна верификация — дальше всё работает. Никаких повторных верификаций при каждой подаче.
- **Для платформы:** защита от ботов, дублей и Sybil-атак на уровне инфраструктуры, не бизнес-логики.
- **Для Custom GPT:** стандартный OAuth 2.0 без экспозиции eID-системы наружу.
- **Для будущего Web3-слоя:** data model уже содержит wallet-поля; eID — временный anti-Sybil механизм до перехода к wallet signatures.

---

## CTO framing

- Сервис — отдельный репозиторий и отдельный деплой. Не добавляется в `doge-complaints-gateway`.
- Stack: Python 3.11+, FastAPI, Supabase (Auth + Postgres), Authentigate (SaaS OIDC).
- Authentigate — внешний SaaS, никогда не экспонируется в GPT или на frontend напрямую.
- Supabase OAuth 2.1 Server — не используется. identity-service реализует OAuth server самостоятельно.
- eID verification = временный trust bootstrap layer. Долгосрочно — wallet signatures.

---

## KPI верхнего уровня

- Доля верифицированных story submissions (должна быть 100% при включённом gate).
- Уровень false-reject при eID конфликтах (должен быть 0% для case A и B; case C — корректный отказ).
- Время eID flow end-to-end (< 30 секунд при штатной работе Authentigate).
- Отсутствие утечки PII в logs, audit events, API responses.

---

## ADR-кандидаты

- ADR-IDS-001: doge-identity-service как отдельный сервис.
- ADR-IDS-002: OAuth 2.0 Authorization Code Flow для Custom GPT.
- ADR-IDS-003: One-time eID verification (не per-action).
- ADR-IDS-004: Mock OIDC сервер для dev до получения Authentigate credentials.
