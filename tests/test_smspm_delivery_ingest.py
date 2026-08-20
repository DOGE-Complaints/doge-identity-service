"""EPIC-IDS-14 STORY-IDS-SMSPM-04 — SMSPM delivery query parse (offline)."""

from __future__ import annotations

import pytest

from core.phone.smspm.delivery_ingest import parse_smspm_delivery_query


def test_parse_submitted_maps_to_sent() -> None:
    event = parse_smspm_delivery_query({"id": "msg-1", "status": "submitted", "toNumber": "3721"})
    assert event.provider_message_id == "msg-1"
    assert event.delivery_status == "sent"


def test_parse_delivered() -> None:
    event = parse_smspm_delivery_query({"id": "msg-1", "status": "delivered"})
    assert event.delivery_status == "delivered"


def test_parse_failed() -> None:
    event = parse_smspm_delivery_query({"id": "msg-1", "status": "failed"})
    assert event.delivery_status == "failed"


def test_parse_queued() -> None:
    event = parse_smspm_delivery_query({"id": "msg-1", "status": "queued"})
    assert event.delivery_status == "queued"


def test_parse_missing_id_raises() -> None:
    with pytest.raises(ValueError, match="missing message id"):
        parse_smspm_delivery_query({"status": "delivered"})


def test_parse_unsupported_status_raises() -> None:
    with pytest.raises(ValueError, match="unsupported delivery status"):
        parse_smspm_delivery_query({"id": "msg-1", "status": "unknown-status"})
