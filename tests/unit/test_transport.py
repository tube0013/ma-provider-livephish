"""Exercise request pacing, revoked tokens and safe errors without a service connection."""

from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest

from livephish.client import LivePhishClient, LivePhishError


@pytest.mark.parametrize(
    ("retry_after", "delay"),
    [
        ("7200", 7200),
        ("Sun, 22 Nov 2026 21:00:00 GMT", 3600),
        ("invalid", 60),
        ("0", 30),
    ],
)
async def test_retry_after_blocks_all_requests(retry_after: str, delay: int) -> None:
    """Honor both Retry-After forms before the next request, including another API host."""
    response = MagicMock(status=429, headers={"Retry-After": retry_after})
    session = MagicMock()
    session.request.return_value.__aenter__ = AsyncMock(return_value=response)
    client = LivePhishClient(session, "", "")
    with (
        patch("livephish.client.time.monotonic", return_value=100),
        patch("livephish.client.time.time", return_value=1795377600),
        patch("livephish.client.asyncio.sleep", new_callable=AsyncMock) as sleep,
    ):
        with pytest.raises(LivePhishError, match="rate limited"):
            await client._request("GET", "https://streamapi.livephish.com/api.aspx", "catalog")
        response.status = 200
        response.json = AsyncMock(return_value={})
        await client._request("GET", "https://stash.livephish.com/api/v1/stash", "user")
        assert sleep.await_args_list[1].args == (delay,)


async def test_unauthorized_invalidates_cached_authentication() -> None:
    """A revoked access token forces authentication on the next protected operation."""
    response = MagicMock(status=401)
    session = MagicMock()
    session.request.return_value.__aenter__ = AsyncMock(return_value=response)
    client = LivePhishClient(session, "", "")
    client._expires = client._token_expires = float("inf")
    with pytest.raises(LivePhishError, match="HTTP 401"):
        await client._request("GET", "https://stash.livephish.com/api/v1/stash", "user")
    assert client._expires == client._token_expires == 0
    assert session.request.call_args.kwargs["allow_redirects"] is False


async def test_transport_error_redacts_sensitive_url() -> None:
    """Network errors cannot publish the request URL or credentials."""
    session = MagicMock()
    session.request.side_effect = aiohttp.ClientConnectionError(
        "https://example.test/?token=secret"
    )
    client = LivePhishClient(session, "private-user", "private-password")
    with pytest.raises(LivePhishError, match="connection or JSON response failure") as error:
        await client._request("GET", "https://streamapi.livephish.com/api.aspx", "stream")
    assert "secret" not in str(error.value)
    assert "private" not in str(error.value)
