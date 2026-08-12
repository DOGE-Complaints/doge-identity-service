# Acceptance verification — task-ids-09-04-t04-env-example-authentigate-vars

- **Gate:** PASS (2026-06-08)
- **Wave:** pkg-000017

| Criterion | Result |
|-----------|--------|
| Demo issuer in .env.example | PASS — `AUTHENTIGATE_ISSUER=https://oidc.demo.sk.ee` |
| Full scope URLs | PASS — claim-URL format in `AUTHENTIGATE_SCOPES` |
| ACR/UI_LOCALES/COUNTRY vars | PASS — `.env.example` lines 52-55 |
