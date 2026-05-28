from pathlib import Path

from core.config.env_file import _parse_dotenv_file, merge_dotenv_from_path
from core.config.providers import provide_app_config


def test_merge_dotenv_preserves_priority(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "# comment",
                "APP_PROFILE=pilot",
                "API_BASE_URL='http://from-env-file'",
                'DB_BACKEND="supabase"',
                "EID_PROVIDER=mock",
            ]
        ),
        encoding="utf-8",
    )

    target = {"API_BASE_URL": "http://from-shell"}
    merge_dotenv_from_path(env_file, target, priority={"API_BASE_URL": "shell"})

    assert target["API_BASE_URL"] == "http://from-shell"
    assert target["APP_PROFILE"] == "pilot"
    assert target["DB_BACKEND"] == "supabase"
    assert target["EID_PROVIDER"] == "mock"


def test_provide_app_config_uses_explicit_mapping_only() -> None:
    cfg = provide_app_config(
        {
            "APP_PROFILE": "demo",
            "API_BASE_URL": "http://localhost:8100",
            "DB_BACKEND": "in_memory",
            "EID_PROVIDER": "mock",
            "REQUEST_TIMEOUT_S": "15",
            "OIDC_REQUEST_TIMEOUT_S": "10",
        }
    )
    assert cfg.api_base_url == "http://localhost:8100"
    assert cfg.db_backend == "in_memory"
    assert cfg.eid_provider == "mock"


def test_parse_dotenv_file_handles_comments_and_quotes(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "# comment",
                "KEY1=val1",
                'KEY2="quoted"',
                "KEY3='single-quoted'",
                "",
            ]
        ),
        encoding="utf-8",
    )
    result = _parse_dotenv_file(env_file)
    assert result == {"KEY1": "val1", "KEY2": "quoted", "KEY3": "single-quoted"}
