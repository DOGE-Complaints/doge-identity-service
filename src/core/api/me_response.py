from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.api.security import UserClaims
    from core.domain.models import ProfileRecord


def _format_datetime(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


def build_me_data(profile: ProfileRecord | None, current_user: UserClaims) -> dict:
    """Build GET /me `data` payload (envelope applied by handler)."""
    data: dict = {
        "supabase_user_id": current_user.supabase_user_id,
        "eid_verified": False,
        "role": current_user.role,
        "display_name": None,
        "avatar_url": None,
        "eid_provider": None,
        "eid_method": None,
        "eid_country": None,
        "eid_verified_at": None,
    }
    if profile is not None:
        data["eid_verified"] = profile.eid_verified
        data["display_name"] = profile.display_name
        data["avatar_url"] = profile.avatar_url
        data["eid_provider"] = profile.eid_provider
        data["eid_method"] = profile.eid_method
        data["eid_country"] = profile.eid_country
        data["eid_verified_at"] = _format_datetime(profile.eid_verified_at)
    return data
