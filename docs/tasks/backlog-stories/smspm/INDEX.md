# SMSPM — backlog package

> Context: [EPIC-IDS-SMSPM.md](EPIC-IDS-SMSPM.md) · Design: [solution-architecture-smspm-sms-provider.md](solution-architecture-smspm-sms-provider.md)

| Order | Story | Status | Depends |
|-------|-------|--------|---------|
| 1 | [STORY-IDS-SMSPM-01-provider-config-registry](STORY-IDS-SMSPM-01-provider-config-registry.md) ([pipeline](../../epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-01-provider-config-registry/STORY-IDS-SMSPM-01-provider-config-registry.md), pkg-000046) | 🟢 Done | phone backbone Done |
| 2 | [STORY-IDS-SMSPM-02-sms-sender](STORY-IDS-SMSPM-02-sms-sender.md) ([pipeline](../../epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-02-sms-sender/STORY-IDS-SMSPM-02-sms-sender.md), pkg-000047) | 🟢 Done | SMSPM-01; live after SPIKE |
| 3 | [STORY-IDS-SMSPM-03-operator-runbook-smoke](STORY-IDS-SMSPM-03-operator-runbook-smoke.md) ([pipeline](../../epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-03-operator-runbook-smoke/STORY-IDS-SMSPM-03-operator-runbook-smoke.md), pkg-000048) | Todo (t04 BLOCKED) | SMSPM-02 + SPIKE |
| 4 | [STORY-IDS-SMSPM-04-delivery-report-webhook](STORY-IDS-SMSPM-04-delivery-report-webhook.md) ([pipeline](../../epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-04-delivery-report-webhook/STORY-IDS-SMSPM-04-delivery-report-webhook.md), pkg-000049) | 🟢 Done | SMSPM-02 |
| 5 | [STORY-IDS-SMSPM-05-smsid-session-wire](STORY-IDS-SMSPM-05-smsid-session-wire.md) | Todo (draft) | SMSPM-02 🟢; optional PA.3 — **excluded from 2/4** |

**Progress:** 3/4 Done (75%) — SMSPM-05 draft (D-02-6) excluded from package denominator.

### Ops (excluded from progress)

| Story | Status | Notes |
|-------|--------|-------|
| [SPIKE-IDS-SMSPM-01-account-sender-setup](SPIKE-IDS-SMSPM-01-account-sender-setup.md) | Todo | External / SMSPM account |
