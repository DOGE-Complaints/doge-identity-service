from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING
from urllib.parse import urlencode

from core.domain.models import AuthorizationRequest
from core.oauth.errors import OAuthClientError, OAuthError, OAuthGrantError, oauth_error_body
from core.oauth.request_context import (
    action_requires_phone_verification,
    normalize_requested_action,
    normalize_return_context,
)
from core.oauth.scope import parse_scope_param, validate_requested_scopes
from core.oauth.spa_login import build_spa_oauth_login_url
from core.oauth.verification_required import build_verification_required_response

if TYPE_CHECKING:
    from core.api.dependencies import ApiDependencies
    from core.api.security import UserClaims


def _now() -> datetime:
    return datetime.now(timezone.utc)


def handle_oauth_authorize(
    deps: ApiDependencies,
    *,
    query: dict[str, str],
) -> tuple[str | None, dict | None, int]:
    client_store = deps.oauth_client_store
    auth_request_store = deps.oauth_authorization_request_store
    if client_store is None or auth_request_store is None:
        body = oauth_error_body("invalid_request", "OAuth server is not configured.")
        return None, body, 503

    response_type = query.get("response_type", "").strip()
    client_id = query.get("client_id", "").strip()
    redirect_uri = query.get("redirect_uri", "").strip()
    state = query.get("state", "").strip()
    scope_raw = query.get("scope")
    code_challenge = query.get("code_challenge") or None
    code_challenge_method = query.get("code_challenge_method") or None
    requested_action_raw = query.get("requested_action")
    return_context_raw = query.get("return_context")

    if not client_id:
        return None, oauth_error_body("invalid_request", "client_id is required."), 400
    if not redirect_uri:
        return None, oauth_error_body("invalid_request", "redirect_uri is required."), 400
    if not state:
        return None, oauth_error_body("invalid_request", "state is required."), 400
    if response_type != "code":
        return None, oauth_error_body("unsupported_response_type", "Only code is supported."), 400

    try:
        requested_action = normalize_requested_action(requested_action_raw)
    except ValueError:
        return None, oauth_error_body("invalid_request", "requested_action is not allowed."), 400
    return_context = normalize_return_context(return_context_raw)

    client = client_store.get_client(client_id)
    if client is None:
        return None, oauth_error_body("invalid_client", "Unknown OAuth client."), 400
    if redirect_uri != client.redirect_uri:
        return None, oauth_error_body("invalid_redirect_uri", "redirect_uri mismatch."), 400

    try:
        scopes = validate_requested_scopes(
            parse_scope_param(scope_raw),
            allowed_scopes=client.scopes,
        )
    except ValueError:
        return None, oauth_error_body("invalid_scope", "Requested scope is not allowed."), 400

    if code_challenge is not None and code_challenge_method not in (None, "", "S256"):
        return None, oauth_error_body("invalid_request", "Only S256 PKCE is supported."), 400

    now = _now()
    oauth_request_id = secrets.token_urlsafe(24)
    ttl_s = deps.config.oauth_authorization_code_ttl_s
    request = AuthorizationRequest(
        oauth_request_id=oauth_request_id,
        client_id=client_id,
        redirect_uri=redirect_uri,
        scopes=scopes,
        state=state,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method if code_challenge else None,
        created_at=now,
        expires_at=now + timedelta(seconds=ttl_s),
        requested_action=requested_action,
        return_context=return_context,
    )
    auth_request_store.save(request)
    redirect_url = build_spa_oauth_login_url(deps.config, oauth_request_id=oauth_request_id)
    return redirect_url, None, 302


def handle_oauth_authorize_complete(
    deps: ApiDependencies,
    *,
    current_user: UserClaims,
    oauth_request_id: str,
) -> tuple[str | None, dict | None, int]:
    token_service = deps.oauth_token_service
    auth_request_store = deps.oauth_authorization_request_store
    profile_repository = deps.profile_repository
    if token_service is None or auth_request_store is None:
        body = oauth_error_body("invalid_request", "OAuth server is not configured.")
        return None, body, 503

    request_id = oauth_request_id.strip()
    if not request_id:
        return None, oauth_error_body("invalid_request", "oauth_request_id is required."), 400

    now = _now()
    auth_request = auth_request_store.get(request_id)
    if auth_request is None:
        return None, oauth_error_body("invalid_grant", "Authorization request expired or unknown."), 400
    if now >= auth_request.expires_at:
        return None, oauth_error_body("invalid_grant", "Authorization request expired or unknown."), 400

    if action_requires_phone_verification(auth_request.requested_action):
        phone_verified = False
        if profile_repository is not None:
            profile = profile_repository.get_by_supabase_user_id(current_user.supabase_user_id)
            if profile is not None:
                phone_verified = profile.phone_verified
        if not phone_verified:
            body, status = build_verification_required_response(
                deps.config,
                return_context=auth_request.return_context,
            )
            return None, body, status

    auth_request = auth_request_store.consume(request_id, now=now)
    if auth_request is None:
        return None, oauth_error_body("invalid_grant", "Authorization request expired or unknown."), 400

    code = token_service.issue_authorization_code(
        supabase_user_id=current_user.supabase_user_id,
        client_id=auth_request.client_id,
        scopes=auth_request.scopes,
        redirect_uri=auth_request.redirect_uri,
        code_challenge=auth_request.code_challenge,
        code_challenge_method=auth_request.code_challenge_method,
    )
    query = urlencode({"code": code, "state": auth_request.state})
    redirect_url = f"{auth_request.redirect_uri}?{query}"
    return redirect_url, None, 302


def handle_oauth_token(
    deps: ApiDependencies,
    *,
    form: dict[str, str],
) -> tuple[dict | None, int]:
    token_service = deps.oauth_token_service
    if token_service is None:
        return oauth_error_body("invalid_request", "OAuth server is not configured."), 503

    grant_type = form.get("grant_type", "").strip()
    if grant_type != "authorization_code":
        return oauth_error_body("unsupported_grant_type", "Only authorization_code is supported."), 400

    code = form.get("code", "").strip()
    client_id = form.get("client_id", "").strip()
    client_secret = form.get("client_secret", "").strip()
    redirect_uri = form.get("redirect_uri", "").strip()
    code_verifier = form.get("code_verifier") or None

    if not code or not client_id or not client_secret or not redirect_uri:
        return oauth_error_body("invalid_request", "Missing required token parameters."), 400

    try:
        access_token = token_service.issue_access_token(
            code=code,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            code_verifier=code_verifier,
        )
    except OAuthClientError as exc:
        return oauth_error_body(exc.error, exc.error_description), exc.status_code
    except OAuthGrantError as exc:
        return oauth_error_body(exc.error, exc.error_description), exc.status_code
    except OAuthError as exc:
        return oauth_error_body(exc.error, exc.error_description), exc.status_code

    claims = token_service.validate_access_token(access_token)
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": deps.config.oauth_access_token_ttl_s,
        "scope": " ".join(claims.scopes),
    }, 200
