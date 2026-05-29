from __future__ import annotations

import logging

import pytest

from core.logging_setup import configure_logging, log_runtime_exception


def test_configure_logging_sets_debug_level() -> None:
    configure_logging("DEBUG")
    assert logging.getLogger().level == logging.DEBUG


def test_configure_logging_json_format_does_not_raise() -> None:
    configure_logging("INFO", log_format="json")


def test_log_runtime_exception_emits_without_error(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.ERROR, logger="core.runtime"):
        log_runtime_exception(
            ValueError("test"),
            trace_id="abc",
            path="/me",
        )
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.name == "core.runtime"
    assert record.levelno == logging.ERROR
    assert "/me" in record.getMessage()
    assert "abc" in record.getMessage()
    assert "ValueError('test')" in record.getMessage()
