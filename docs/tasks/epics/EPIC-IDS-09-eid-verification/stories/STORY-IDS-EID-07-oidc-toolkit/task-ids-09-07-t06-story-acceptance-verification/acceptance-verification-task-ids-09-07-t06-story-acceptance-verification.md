# Acceptance verification — task-ids-09-07-t06-story-acceptance-verification

- **Gate:** PASS (2026-06-10)
- **Wave:** pkg-000020
- **Story:** STORY-IDS-EID-07-oidc-toolkit

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| Модуль `core/security/oidc/` содержит `OidcDiscoveryClient`, `JwksCache`, `IdTokenValidator`, не зависящие от конкретного провайдера | PASS | t01–t03 — `discovery.py`, `jwks_cache.py`, `id_token.py`, `__init__.py` |
| Discovery и JWKS кэшируются; неизвестный `kid` инициирует обновление JWKS | PASS | t01/t02 — cache; t05 — `test_discovery_client_caches_*`, `test_jwks_cache_resolves_unknown_kid_*`, `test_id_token_validator_refreshes_jwks_on_unknown_kid` |
| `IdTokenValidator` проверяет подпись RS256 + `iss/aud/exp/iat/nonce`; невалидный токен → `IDENTITY_VALIDATION_FAILED` | PASS | t03 — `IdTokenValidator`; t05 — parametrize validation failures, `OidcIdTokenValidationError.code` |
| Тулкит доступен провайдерам через `ProviderRuntime` | PASS | t04 — `OidcToolkit`, `runtime_factory.py`; t05 — `test_build_provider_runtime_wires_oidc_*` |
| Тесты с замоканными discovery/JWKS/подписью; offline-набор зелёный | PASS | t05 — `tests/test_oidc_toolkit.py`; 244 pytest offline |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
# 244 passed
```
