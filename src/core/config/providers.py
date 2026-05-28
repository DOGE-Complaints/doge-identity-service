from __future__ import annotations

from os import environ
from typing import Mapping

from core.config.env_file import merge_dotenv_from_cwd
from core.config.schema import AppConfig, load_config_from_env


def provide_app_config(env: Mapping[str, str] | None = None) -> AppConfig:
    if env is None:
        priority = dict(environ)
        source = dict(priority)
        merge_dotenv_from_cwd(source, priority=priority)
    else:
        source = dict(env)
    source.setdefault("APP_PROFILE", "demo")
    source.setdefault("API_BASE_URL", "http://localhost:8100")
    source.setdefault("REQUEST_TIMEOUT_S", "15")
    source.setdefault("OIDC_REQUEST_TIMEOUT_S", "10")
    source.setdefault("DB_BACKEND", "in_memory")
    source.setdefault("EID_PROVIDER", "mock")
    return load_config_from_env(source)
