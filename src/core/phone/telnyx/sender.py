from __future__ import annotations

import httpx

from core.phone.base import SmsErrorCode, SmsSendResult, SmsSenderError
from core.phone.telnyx.config import TelnyxSettings, is_e164_sender
from core.phone.telnyx.errors import extract_telnyx_error_codes, map_telnyx_error, map_telnyx_timeout

_SUCCESS_STATUSES = frozenset({"queued", "sent"})


class TelnyxSmsSender:
    def __init__(self, *, settings: TelnyxSettings, http_client: httpx.Client) -> None:
        self._settings = settings
        self._http = http_client

    @property
    def provider_name(self) -> str:
        return "telnyx"

    def send(self, *, to_e164: str, text: str) -> SmsSendResult:
        payload: dict[str, str] = {
            "from": self._settings.from_sender,
            "to": to_e164,
            "text": text,
            "type": self._settings.message_type,
        }
        if self._settings.messaging_profile_id:
            payload["messaging_profile_id"] = self._settings.messaging_profile_id
        elif not is_e164_sender(self._settings.from_sender):
            raise SmsSenderError(
                "Telnyx messaging profile is required for alphanumeric sender",
                code=SmsErrorCode.SEND_FAILED,
            )
        if self._settings.encoding:
            payload["encoding"] = self._settings.encoding

        url = f"{self._settings.api_base_url.rstrip('/')}/v2/messages"
        headers = {
            "Authorization": f"Bearer {self._settings.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = self._http.post(url, headers=headers, json=payload)
        except httpx.TimeoutException as exc:
            raise map_telnyx_timeout() from exc

        if response.status_code == 200:
            return self._parse_success_response(response)

        error_codes = extract_telnyx_error_codes(response)
        raise map_telnyx_error(status_code=response.status_code, error_codes=error_codes)

    def _parse_success_response(self, response: httpx.Response) -> SmsSendResult:
        try:
            body = response.json()
        except ValueError as exc:
            raise SmsSenderError(
                "Telnyx returned non-JSON success response",
                code=SmsErrorCode.UNKNOWN,
            ) from exc

        data = body.get("data") or {}
        message_id = data.get("id")
        to_entries = data.get("to") or []
        first_status = to_entries[0].get("status") if to_entries else None

        if message_id and first_status in _SUCCESS_STATUSES:
            return SmsSendResult(provider_message_id=str(message_id), accepted=True)

        raise SmsSenderError(
            "Unexpected Telnyx success response",
            code=SmsErrorCode.UNKNOWN,
        )
