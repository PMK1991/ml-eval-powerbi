"""Medium MCP Server - Read and publish articles on Medium."""

import sys
import os

# Ensure the parent directory is on the path so the package can be imported
# when run directly via `python medium_mcp_server/server.py`
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP
from medium_mcp_server.medium_client import (
    get_user_profile,
    list_publications,
    create_post,
    fetch_user_feed,
    fetch_tag_feed,
    fetch_publication_feed,
)

mcp = FastMCP("medium-server")


# --- Write tools (require MEDIUM_TOKEN) ---


@mcp.tool()
async def get_my_profile() -> dict:
    """Get the authenticated Medium user's profile information.

    Returns the user's id, username, display name, profile URL, and avatar URL.
    Requires the MEDIUM_TOKEN environment variable to be set.
    """
    return await get_user_profile()


@mcp.tool()
async def list_my_publications() -> list[dict]:
    """List all publications the authenticated Medium user is a member of.

    Returns a list of publications with their id, name, description, and URL.
    Use publication IDs with publish_post to publish to a specific publication.
    """
    profile = await get_user_profile()
    user_id = profile["id"]
    return await list_publications(user_id)


@mcp.tool()
async def publish_post(
    title: str,
    content: str,
    content_format: str = "markdown",
    publish_status: str = "draft",
    tags: list[str] | None = None,
    canonical_url: str | None = None,
    publication_id: str | None = None,
) -> dict:
    """Publish a post to Medium, either to your profile or to a publication.

    Args:
        title: The title of the post.
        content: The body of the post in HTML or Markdown format.
        content_format: Either 'markdown' or 'html'. Defaults to 'markdown'.
        publish_status: Either 'draft' or 'public'. Defaults to 'draft' for safety.
        tags: Up to 3 tags for the post.
        canonical_url: The original URL if this was published elsewhere first.
        publication_id: If provided, publishes to this publication instead of your profile.
            Use list_my_publications to find publication IDs.

    Returns:
        The created post data including its URL and ID.
    """
    if tags and len(tags) > 3:
        return {"error": "Medium allows a maximum of 3 tags per post."}
    if content_format not in ("markdown", "html"):
        return {"error": "content_format must be 'markdown' or 'html'."}
    if publish_status not in ("draft", "public"):
        return {"error": "publish_status must be 'draft' or 'public'."}

    profile = await get_user_profile()
    user_id = profile["id"]

    return await create_post(
        user_id=user_id,
        title=title,
        content=content,
        content_format=content_format,
        publish_status=publish_status,
        tags=tags or [],
        canonical_url=canonical_url,
        publication_id=publication_id,
    )


# --- Read tools (no auth needed, via RSS) ---


@mcp.tool()
async def read_user_posts(username: str) -> list[dict]:
    """Read the most recent posts from a Medium user via their RSS feed.

    Args:
        username: The Medium username (without the @ symbol).

    Returns:
        Up to 10 recent posts with title, link, published date, author, summary, and tags.
    """
    return await fetch_user_feed(username)


@mcp.tool()
async def read_tag_posts(tag: str) -> list[dict]:
    """Read recent Medium posts for a specific tag/topic via RSS.

    Args:
        tag: The tag name (e.g., 'machine-learning', 'python', 'data-science').
            Use hyphens for multi-word tags.

    Returns:
        Up to 10 recent posts with title, link, published date, author, summary, and tags.
    """
    return await fetch_tag_feed(tag)


@mcp.tool()
async def read_publication_posts(publication_slug: str) -> list[dict]:
    """Read recent posts from a Medium publication via RSS.

    Args:
        publication_slug: The publication's URL slug (e.g., 'towards-data-science',
            'better-programming'). This is the part after medium.com/ in the publication URL.

    Returns:
        Up to 10 recent posts with title, link, published date, author, summary, and tags.
    """
    return await fetch_publication_feed(publication_slug)


if __name__ == "__main__":
    mcp.run()
