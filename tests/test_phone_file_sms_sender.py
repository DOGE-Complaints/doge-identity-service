"""EPIC-IDS-10 STORY-IDS-PV-10 — File SMS sink dev provider (offline)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, get_api_dependencies
from core.config import ConfigError, load_config_from_env
from core.phone.file.file_sender import FileSmsSender, sanitize_phone_log_basename
from core.phone.registry_builder import build_sms_registry, registered_sms_provider_names
from core.phone.runtime_factory import build_sms_provider_runtime
from tests.test_phone_verification_flow import (
    _DEMO_USER_ID,
    _EE_PHONE,
    _demo_bearer_token,
    _extract_code,
    _request_phone,
)

_OTHER_PHONE = "+37256666666"


def _minimal_env(**overrides: str) -> dict[str, str]:
    base = {
        "APP_PROFILE": "demo",
        "API_BASE_URL": "http://localhost:8100",
        "DB_BACKEND": "in_memory",
        "EID_PROVIDER": "mock",
        "SMS_PROVIDER": "file",
    }
    base.update(overrides)
    return base


def _pilot_env(**overrides: str) -> dict[str, str]:
    base = {
        "APP_PROFILE": "pilot",
        "API_BASE_URL": "https://identity.dogestonia.ee",
        "DB_BACKEND": "supabase",
        "EID_PROVIDER": "mock",
        "SMS_PROVIDER": "mock",
        "SUPABASE_URL": "https://example.supabase.co",
        "SUPABASE_SERVICE_ROLE": "sr",
        "DATABASE_URL": "postgresql://postgres:pass@example:5432/postgres",
        "DOGESTONIA_EID_SECRET": "eid-secret",
        "EID_SESSION_ENC_KEY": "2zy6gKOpxhkaNwtmufGZqYb0T88uh-tkKHC5ygQOnIM=",
        "OAUTH_ACCESS_TOKEN_SECRET": "oauth",
        "GPT_OAUTH_CLIENT_SECRET": "gpt-secret",
        "SERVICE_API_TOKEN": "service-api-token",
    }
    base.update(overrides)
    return base


@pytest.fixture
def file_outbox(tmp_path: Path) -> Path:
    outbox = tmp_path / "sms-outbox"
    outbox.mkdir()
    return outbox


def test_registered_sms_provider_names_includes_file() -> None:
    assert "file" in registered_sms_provider_names()


def test_sanitize_phone_log_basename_strips_unsafe_chars() -> None:
    assert sanitize_phone_log_basename("+37255555555") == "+37255555555"
    assert sanitize_phone_log_basename("../+37255555555") == "+37255555555"
    assert "/" not in sanitize_phone_log_basename("+372/5555")


def test_file_sender_appends_two_lines_same_number(file_outbox: Path) -> None:
    sender = FileSmsSender(outbox_dir=file_outbox)
    sender.send(to_e164=_EE_PHONE, text="first code 111111")
    sender.send(to_e164=_EE_PHONE, text="second code 222222")

    log_path = file_outbox / "+37255555555.log"
    assert log_path.exists()
    lines = log_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert "first code 111111" in lines[0]
    assert "second code 222222" in lines[1]
    assert lines[0].split("\t", 1)[0].endswith("Z")
    assert lines[1].split("\t", 1)[0].endswith("Z")
    first_ts = lines[0].split("\t", 1)[0]
    second_ts = lines[1].split("\t", 1)[0]
    assert first_ts <= second_ts


def test_file_sender_uses_different_files_for_different_numbers(file_outbox: Path) -> None:
    sender = FileSmsSender(outbox_dir=file_outbox)
    sender.send(to_e164=_EE_PHONE, text="code-a")
    sender.send(to_e164=_OTHER_PHONE, text="code-b")

    assert (file_outbox / "+37255555555.log").read_text(encoding="utf-8").strip().endswith("code-a")
    assert (file_outbox / "+37256666666.log").read_text(encoding="utf-8").strip().endswith("code-b")


def test_pilot_profile_rejects_file_sms_provider() -> None:
    with pytest.raises(ConfigError, match="SMS_PROVIDER=file is forbidden"):
        load_config_from_env(_pilot_env(SMS_PROVIDER="file"))


def test_file_sms_provider_loads_in_demo_profile(file_outbox: Path) -> None:
    cfg = load_config_from_env(
        _minimal_env(FILE_SMS_OUTBOX_DIR=str(file_outbox)),
    )
    assert cfg.sms_provider == "file"


def test_build_sms_provider_runtime_file_skips_http_client(file_outbox: Path) -> None:
    config = load_config_from_env(
        _minimal_env(FILE_SMS_OUTBOX_DIR=str(file_outbox)),
    )
    runtime = build_sms_provider_runtime(
        config=config,
        env=_minimal_env(FILE_SMS_OUTBOX_DIR=str(file_outbox)),
    )
    assert runtime.http_client is None
    registry = build_sms_registry(runtime)
    sender = registry.get_active(config)
    assert isinstance(sender, FileSmsSender)


@pytest.fixture
def file_sms_client(
    monkeypatch: pytest.MonkeyPatch,
    test_client: TestClient,
    file_outbox: Path,
) -> TestClient:
    _clear_api_dependencies_cache()
    monkeypatch.setenv("SMS_PROVIDER", "file")
    monkeypatch.setenv("FILE_SMS_OUTBOX_DIR", str(file_outbox))
    monkeypatch.setenv("PHONE_ALLOWED_DIAL_PREFIXES", "+372")
    monkeypatch.setenv("PHONE_RESEND_COOLDOWN_S", "60")
    yield test_client
    _clear_api_dependencies_cache()


def test_phone_request_with_file_provider_writes_outbox_log(
    file_sms_client: TestClient,
    file_outbox: Path,
) -> None:
    token = _demo_bearer_token()
    response = _request_phone(file_sms_client, token=token, phone=_EE_PHONE)
    assert response.status_code == 200

    log_path = file_outbox / "+37255555555.log"
    assert log_path.exists()
    line = log_path.read_text(encoding="utf-8").strip()
    assert "\t" in line
    text = line.split("\t", 1)[1]
    code = _extract_code(text)
    assert len(code) == 6

    deps = get_api_dependencies()
    assert deps.sms_sender_registry is not None
    sender = deps.sms_sender_registry.get_active(deps.config)
    assert isinstance(sender, FileSmsSender)
    assert sender.provider_name == "file"

    session = deps.phone_verification_session_store.get_active_by_user(
        _DEMO_USER_ID,
        now=datetime.now(timezone.utc),
    )
    assert session is not None
    assert session.provider_message_id is not None
    assert session.provider_message_id.startswith("file-")
