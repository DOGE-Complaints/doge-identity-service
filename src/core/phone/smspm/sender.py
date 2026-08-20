from __future__ import annotations

import httpx

from core.phone.base import SmsErrorCode, SmsSendResult, SmsSenderError
from core.phone.smspm.config import SmspmSettings
from core.phone.smspm.errors import extract_smspm_error_text, map_smspm_error, map_smspm_timeout


class SmspmSmsSender:
    def __init__(self, *, settings: SmspmSettings, http_client: httpx.Client) -> None:
        self._settings = settings
        self._http = http_client

    @property
    def provider_name(self) -> str:
        return "smspm"

    def send(self, *, to_e164: str, text: str, sms_id: str | None = None) -> SmsSendResult:
        payload: dict[str, str] = {
            "hash": self._settings.hash,
            "token": self._settings.token,
            "toNumber": to_e164.lstrip("+"),
            "fromNumber": self._settings.from_sender,
            "text": text,
        }
        if sms_id:
            payload["smsId"] = sms_id
        if self._settings.report_url:
            payload["report"] = self._settings.report_url

        url = self._settings.api_base_url.rstrip("/")
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = self._http.post(url, headers=headers, json=payload)
        except httpx.TimeoutException as exc:
            raise map_smspm_timeout() from exc

        if response.status_code == 200:
            return self._parse_success_response(response)

        error_text = extract_smspm_error_text(response)
        raise map_smspm_error(status_code=response.status_code, error_text=error_text)

    def _parse_success_response(self, response: httpx.Response) -> SmsSendResult:
        try:
            body = response.json()
        except ValueError as exc:
            raise SmsSenderError(
                "SMSPM returned non-JSON success response",
                code=SmsErrorCode.UNKNOWN,
            ) from exc

        messages = body.get("messages") if isinstance(body, dict) else None
        first = messages[0] if isinstance(messages, list) and messages else None
        message_id = first.get("id") if isinstance(first, dict) else None
        if message_id:
            return SmsSendResult(provider_message_id=str(message_id), accepted=True)

        raise SmsSenderError(
            "Unexpected SMSPM success response",
            code=SmsErrorCode.UNKNOWN,
        )
