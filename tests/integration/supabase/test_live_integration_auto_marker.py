"""Contract test: pytest_collection_modifyitems tags this module as live_integration."""

from __future__ import annotations

import pytest


def test_auto_marker_applied_via_collection_hook(request: pytest.FixtureRequest) -> None:
    """No @pytest.mark.live_integration on this test — only conftest hook."""
    assert request.node.get_closest_marker("live_integration") is not None
