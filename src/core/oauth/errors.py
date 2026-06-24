from __future__ import annotations


class OAuthError(Exception):
    def __init__(self, error: str, error_description: str, *, status_code: int = 400) -> None:
        self.error = error
        self.error_description = error_description
        self.status_code = status_code
        super().__init__(error_description)


class OAuthClientError(OAuthError):
    def __init__(self, error: str, error_description: str) -> None:
        super().__init__(error, error_description, status_code=401)


class OAuthGrantError(OAuthError):
    pass


def oauth_error_body(error: str, error_description: str) -> dict[str, str]:
    return {"error": error, "error_description": error_description}
