# EPIC-IDS-CLEANUP — Чистка scope, заготовок и документации

> **ID:** `EPIC-IDS-CLEANUP` (pipeline `EPIC-IDS-08`) · **Статус:** 🟡 In Progress (CLEANUP-01/02/03 🟢 Done — pkg-000011…013; **остаётся:** CLEANUP-04 ⚪ Todo) · **Тип:** Tech-debt / Hygiene
> **Синхронизировано с** [`bullrun-launch-index`](../../bullrun-launch-index.md) 2026-06-26.

## Назначение
Привести identity к согласованной парадигме (решения 2026-06-04): убрать всё, что относится к историям (домен gateway), закрыть «заготовки без поведения» и устранить рассинхрон документации с кодом. Это не новая функциональность, а наведение порядка — чтобы функциональные эпики (AUTH-CORE / EID / OAUTH) строились на чистой базе.

## Почему отдельный эпик
Задачи-чистки не ложатся в инфраструктурные эпики 01–06 (они Done) и не относятся к функциональным AUTH-CORE/EID/OAUTH. Объединять их по смыслу логично в одном hygiene-эпике.

## Stories
| Story | Тема | Статус |
|-------|------|--------|
| [STORY-IDS-CLEANUP-01](STORY-IDS-CLEANUP-01-remove-stories-from-identity.md) | Вынос историй из identity + починка `/ready` (вкл. HIGH-gap SB-1) | 🟢 Done |
| [STORY-IDS-CLEANUP-02](STORY-IDS-CLEANUP-02-placeholders-hardening.md) | Чистка заготовок и хардненинг | 🟢 Done |
| [STORY-IDS-CLEANUP-03](STORY-IDS-CLEANUP-03-doc-drift.md) | Устранение рассинхрона документации | 🟢 Done |
| [STORY-IDS-CLEANUP-04](STORY-IDS-CLEANUP-04-spec-reconciliation.md) | spec reconciliation: gateway-copies + eID drift + crypto naming | ⚪ Todo |

## Связь
Источник задач — [identity-todo-backlog-2026-06-04](../../../analysis/identity-todo-backlog-2026-06-04.md), [gap-analysis-full-2026-06-04](../../../analysis/gap-analysis-full-2026-06-04.md).
