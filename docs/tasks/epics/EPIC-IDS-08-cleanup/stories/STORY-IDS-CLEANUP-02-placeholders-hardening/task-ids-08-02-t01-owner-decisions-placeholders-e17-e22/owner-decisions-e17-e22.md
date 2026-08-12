# Owner decisions — E17–E22 (STORY-IDS-CLEANUP-02)

Decision date: 2026-06-02 · Wave: pkg-000013 · Ref: backlog Scope + gap §10

| ID | Decision | Rationale |
|----|----------|-----------|
| **E17** `ALLOWED_RETURN_URLS` | **довести** | Open-redirect risk (gap P2); req-11 требует allowlist; route `/auth/eid/start` пока stub — validation helper + tests на уровне `core/security/return_url.py`, wiring в eID epic позже. |
| **E18** `StubBearerTokenAuth` | **убрать** | Backlog Scope явно: «удалить неиспользуемый класс»; prod DI → `SupabaseJwtBearerTokenAuth` с 2026-05-29 (EPIC-IDS-04). |
| **E20** `CODE_VERIFIER_ENCRYPTION_KEY` | **убрать** | AES-секрет pilot-required, но encryption в `src/` отсутствует (gap P5); defer cipher до functional Authentigate epic. |
| **E21** idempotency-резолвер | **убрать** | Нет POST consumers в prod routes; helper-only placeholder (gap P6); EPIC-IDS-02 tests покрывали resolver — удалить модуль + tests. |
| **E22** пустые пакеты | **убрать** | `core.audit`, `core.oauth`, `core.profiles` — docstring-only, zero imports; «наполнить» = functional epic (backlog «Вне scope»). |
