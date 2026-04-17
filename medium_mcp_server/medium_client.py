"""Medium API client and RSS feed reader."""

import os
import re
import sys
from html import unescape

import anyio
import feedparser
import httpx

MEDIUM_API_BASE = "https://api.medium.com/v1"
MEDIUM_FEED_BASE = "https://medium.com/feed"


def _get_token() -> str:
    """Read MEDIUM_TOKEN from environment. Raises if not set."""
    token = os.environ.get("MEDIUM_TOKEN", "")
    if not token:
        raise ValueError(
            "MEDIUM_TOKEN environment variable is not set. "
            "Generate one at https://medium.com/me/settings/security"
        )
    return token


def _log(message: str) -> None:
    """Log to stderr to avoid corrupting stdio MCP transport."""
    print(message, file=sys.stderr)


async def _api_request(
    method: str, path: str, json_body: dict | None = None
) -> dict:
    """Make an authenticated request to the Medium API."""
    token = _get_token()
    url = f"{MEDIUM_API_BASE}{path}"
    _log(f"Medium API: {method} {path}")
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.request(
            method,
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json=json_body,
        )
        if response.status_code == 401:
            raise ValueError(
                "Medium API: Invalid or expired token. "
                "Check your MEDIUM_TOKEN at https://medium.com/me/settings/security"
            )
        if response.status_code == 403:
            raise PermissionError(
                "Medium API: Forbidden. Check your permissions (403)."
            )
        response.raise_for_status()
        result = response.json()
        return result.get("data", result)


def _clean_html(html_text: str) -> str:
    """Strip HTML tags and decode entities."""
    text = re.sub(r"<[^>]+>", "", html_text)
    return unescape(text).strip()


def _parse_feed_entry(entry) -> dict:
    """Normalize an RSS feed entry into a clean dict."""
    tags = [t.get("term", "") for t in getattr(entry, "tags", [])]
    summary_raw = getattr(entry, "summary", "") or ""
    return {
        "title": getattr(entry, "title", ""),
        "link": getattr(entry, "link", ""),
        "published": getattr(entry, "published", ""),
        "author": getattr(entry, "author", ""),
        "summary": _clean_html(summary_raw)[:500],
        "tags": tags,
    }


async def _fetch_feed(url: str) -> list[dict]:
    """Fetch and parse an RSS feed, returning normalized entries."""
    _log(f"Fetching RSS: {url}")
    feed = await anyio.to_thread.run_sync(lambda: feedparser.parse(url))
    if feed.bozo:
        _log(f"RSS warning: feed at {url} had parsing issues: {feed.bozo_exception}")
    return [_parse_feed_entry(entry) for entry in feed.entries]


# --- Public API functions (write, require token) ---


async def get_user_profile() -> dict:
    """Get the authenticated user's profile."""
    return await _api_request("GET", "/me")


async def list_publications(user_id: str) -> list[dict]:
    """List publications the user is a member of."""
    return await _api_request("GET", f"/users/{user_id}/publications")


async def create_post(
    user_id: str,
    title: str,
    content: str,
    content_format: str,
    publish_status: str,
    tags: list[str],
    canonical_url: str | None,
    publication_id: str | None,
) -> dict:
    """Create a post on Medium."""
    payload = {
        "title": title,
        "contentFormat": content_format,
        "content": content,
        "publishStatus": publish_status,
    }
    if tags:
        payload["tags"] = tags[:3]
    if canonical_url:
        payload["canonicalUrl"] = canonical_url

    if publication_id:
        path = f"/publications/{publication_id}/posts"
    else:
        path = f"/users/{user_id}/posts"

    return await _api_request("POST", path, json_body=payload)


# --- Public RSS functions (read, no token needed) ---


async def fetch_user_feed(username: str) -> list[dict]:
    """Fetch recent posts from a Medium user via RSS."""
    username = username.lstrip("@")
    return await _fetch_feed(f"{MEDIUM_FEED_BASE}/@{username}")


async def fetch_tag_feed(tag: str) -> list[dict]:
    """Fetch recent posts for a tag via RSS."""
    return await _fetch_feed(f"{MEDIUM_FEED_BASE}/tag/{tag}")


async def fetch_publication_feed(publication_slug: str) -> list[dict]:
    """Fetch recent posts from a publication via RSS."""
    return await _fetch_feed(f"{MEDIUM_FEED_BASE}/{publication_slug}")
