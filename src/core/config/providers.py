from __future__ import annotations

from os import environ
from typing import Mapping

from core.config.env_file import merge_dotenv_from_cwd
from core.config.schema import AppConfig, load_config_from_env


def resolve_config_env(env: Mapping[str, str] | None = None) -> dict[str, str]:
    if env is None:
        priority = dict(environ)
        source = dict(priority)
        merge_dotenv_from_cwd(source, priority=priority)
        return source
    return dict(env)


def provide_app_config(env: Mapping[str, str] | None = None) -> AppConfig:
    source = resolve_config_env(env)
    source.setdefault("APP_PROFILE", "demo")
    source.setdefault("API_BASE_URL", "http://localhost:8100")
    source.setdefault("REQUEST_TIMEOUT_S", "15")
    source.setdefault("OIDC_REQUEST_TIMEOUT_S", "10")
    source.setdefault("DB_BACKEND", "in_memory")
    source.setdefault("EID_PROVIDER", "mock")
    source.setdefault("SMS_PROVIDER", "mock")
    source.setdefault("PHONE_ALLOWED_DIAL_PREFIXES", "+372")
    source.setdefault("PHONE_CODE_LENGTH", "6")
    source.setdefault("PHONE_CODE_TTL_S", "300")
    source.setdefault("PHONE_MAX_ATTEMPTS", "5")
    source.setdefault("PHONE_RESEND_COOLDOWN_S", "60")
    source.setdefault("PHONE_ONE_ACCOUNT_PER_NUMBER", "true")
    return load_config_from_env(source)
