from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from os import environ
from typing import Mapping


class ConfigError(ValueError):
    """Raised when environment configuration is invalid."""


class DeploymentProfile(str, Enum):
    DEMO = "demo"
    PILOT = "pilot"


@dataclass(frozen=True)
class AppConfig:
    profile: DeploymentProfile
    port: int
    api_base_url: str
    log_level: str
    log_format: str
    request_timeout_s: int
    oidc_request_timeout_s: int
    supabase_url: str
    supabase_service_role: str
    supabase_jwt_secret: str
    database_url: str
    authentigate_issuer: str
    authentigate_client_id: str
    authentigate_client_secret: str
    authentigate_redirect_uri: str
    authentigate_scopes: str
    eid_secret: str
    node_id: str
    oauth_access_token_secret: str
    oauth_access_token_ttl_s: int
    oauth_authorization_code_ttl_s: int
    gpt_oauth_client_id: str
    gpt_oauth_client_secret: str
    gpt_oauth_redirect_uri: str
    eid_provider: str
    eideasy_env: str
    eideasy_base_url: str
    eideasy_client_id: str
    eideasy_client_secret: str
    eideasy_redirect_uri: str
    eideasy_allowed_methods: str
    eideasy_default_country: str
    eideasy_allowed_countries: str
    db_backend: str
    db_enabled: bool
    cors_allowed_origins: str
    allowed_return_urls: str


def _value(source: Mapping[str, str], key: str, default: str = "") -> str:
    return str(source.get(key, default)).strip()


def _required(source: Mapping[str, str], key: str) -> str:
    value = _value(source, key)
    if not value:
        raise ConfigError(f"Required env var {key!r} is missing or empty")
    return value


def _int(source: Mapping[str, str], key: str, default: str) -> int:
    raw = _value(source, key, default)
    try:
        return int(raw)
    except ValueError as exc:
        raise ConfigError(f"{key} must be integer, got {raw!r}") from exc


def _profile(source: Mapping[str, str]) -> DeploymentProfile:
    raw = _value(source, "APP_PROFILE", "demo").lower()
    if raw == DeploymentProfile.DEMO.value:
        return DeploymentProfile.DEMO
    if raw == DeploymentProfile.PILOT.value:
        return DeploymentProfile.PILOT
    raise ConfigError(f"APP_PROFILE must be 'demo' or 'pilot', got {raw!r}")


def load_config_from_env(source: Mapping[str, str] | None = None) -> AppConfig:
    env = source or environ

    # interview 4.5: db_backend must be validated first
    db_backend = _value(env, "DB_BACKEND", "in_memory").lower()
    if db_backend not in {"in_memory", "supabase"}:
        raise ConfigError(f"DB_BACKEND must be in_memory|supabase, got {db_backend!r}")

    profile = _profile(env)
    eid_provider = _value(env, "EID_PROVIDER", "mock").lower()
    if eid_provider not in {"mock", "eideasy", "authentigate"}:
        raise ConfigError(f"EID_PROVIDER must be mock|eideasy|authentigate, got {eid_provider!r}")

    supabase_url = _value(env, "SUPABASE_URL", "")
    supabase_service_role = _value(env, "SUPABASE_SERVICE_ROLE", "")
    supabase_jwt_secret = _value(env, "SUPABASE_JWT_SECRET", "")
    database_url = _value(env, "DATABASE_URL", "")
    eid_secret = str(env.get("DOGESTONIA_EID_SECRET", "")).strip()  # one-liner, no fallback

    if db_backend == "supabase" and (not supabase_url or not supabase_service_role):
        raise ConfigError("DB_BACKEND=supabase requires SUPABASE_URL and SUPABASE_SERVICE_ROLE")

    if eid_provider == "eideasy":
        for key in ("EIDEASY_CLIENT_ID", "EIDEASY_CLIENT_SECRET", "EIDEASY_REDIRECT_URI"):
            if not _value(env, key, ""):
                raise ConfigError(f"{key} is required when EID_PROVIDER=eideasy")

    if profile is DeploymentProfile.PILOT:
        pilot_required = (
            ("API_BASE_URL", _value(env, "API_BASE_URL", "")),
            ("SUPABASE_URL", supabase_url),
            ("SUPABASE_SERVICE_ROLE", supabase_service_role),
            ("SUPABASE_JWT_SECRET", supabase_jwt_secret),
            ("DATABASE_URL", database_url),
            ("DOGESTONIA_EID_SECRET", eid_secret),
            ("OAUTH_ACCESS_TOKEN_SECRET", _value(env, "OAUTH_ACCESS_TOKEN_SECRET", "")),
            ("GPT_OAUTH_CLIENT_SECRET", _value(env, "GPT_OAUTH_CLIENT_SECRET", "")),
        )
        for key, value in pilot_required:
            if not value:
                raise ConfigError(f"{key} is required for APP_PROFILE=pilot")

    return AppConfig(
        profile=profile,
        port=_int(env, "PORT", "8100"),
        api_base_url=_required(env, "API_BASE_URL"),
        log_level=_value(env, "LOG_LEVEL", "INFO").upper(),
        log_format=_value(env, "LOG_FORMAT", "text").lower(),
        request_timeout_s=_int(env, "REQUEST_TIMEOUT_S", "15"),
        oidc_request_timeout_s=_int(env, "OIDC_REQUEST_TIMEOUT_S", "10"),
        supabase_url=supabase_url,
        supabase_service_role=supabase_service_role,
        supabase_jwt_secret=supabase_jwt_secret,
        database_url=database_url,
        authentigate_issuer=_value(env, "AUTHENTIGATE_ISSUER", ""),
        authentigate_client_id=_value(env, "AUTHENTIGATE_CLIENT_ID", ""),
        authentigate_client_secret=_value(env, "AUTHENTIGATE_CLIENT_SECRET", ""),
        authentigate_redirect_uri=_value(env, "AUTHENTIGATE_REDIRECT_URI", ""),
        authentigate_scopes=_value(env, "AUTHENTIGATE_SCOPES", "openid personal_code personal_code_country"),
        eid_secret=eid_secret,
        node_id=_value(env, "NODE_ID", "tallinn"),
        oauth_access_token_secret=_value(env, "OAUTH_ACCESS_TOKEN_SECRET", ""),
        oauth_access_token_ttl_s=_int(env, "OAUTH_ACCESS_TOKEN_TTL_S", "3600"),
        oauth_authorization_code_ttl_s=_int(env, "OAUTH_AUTHORIZATION_CODE_TTL_S", "300"),
        gpt_oauth_client_id=_value(env, "GPT_OAUTH_CLIENT_ID", "openai-custom-gpt"),
        gpt_oauth_client_secret=_value(env, "GPT_OAUTH_CLIENT_SECRET", ""),
        gpt_oauth_redirect_uri=_value(env, "GPT_OAUTH_REDIRECT_URI", ""),
        eid_provider=eid_provider,
        eideasy_env=_value(env, "EIDEASY_ENV", "test"),
        eideasy_base_url=_value(env, "EIDEASY_BASE_URL", "https://test.eideasy.com"),
        eideasy_client_id=_value(env, "EIDEASY_CLIENT_ID", ""),
        eideasy_client_secret=_value(env, "EIDEASY_CLIENT_SECRET", ""),
        eideasy_redirect_uri=_value(env, "EIDEASY_REDIRECT_URI", ""),
        eideasy_allowed_methods=_value(env, "EIDEASY_ALLOWED_METHODS", "smartid,mid-login,ee-id-login"),
        eideasy_default_country=_value(env, "EIDEASY_DEFAULT_COUNTRY", "EE"),
        eideasy_allowed_countries=_value(env, "EIDEASY_ALLOWED_COUNTRIES", "EE"),
        db_backend=db_backend,
        db_enabled=(db_backend == "supabase"),
        cors_allowed_origins=_value(env, "CORS_ALLOWED_ORIGINS", "*"),
        allowed_return_urls=_value(env, "ALLOWED_RETURN_URLS", ""),
    )
