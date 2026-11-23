"""Load and configure the community provider in a real, isolated MA server."""

import importlib
from unittest.mock import AsyncMock, patch

from music_assistant_models.enums import ConfigEntryType, FlowStepType, MediaType, ProviderTier

from music_assistant.mass import MusicAssistant
from music_assistant.models.music_provider import MusicProvider
from tests import DOMAIN


async def test_provider_loads(mass: MusicAssistant) -> None:
    """Discover the repository with the same community tier used by installed releases."""
    manifest = mass.get_provider_manifest(DOMAIN)
    assert manifest.tier == ProviderTier.COMMUNITY
    assert manifest.has_setup_flow


async def test_setup_and_restart_safe_track(mass: MusicAssistant) -> None:
    """Complete secure setup and resolve a composite ID using synthetic service responses."""
    module = importlib.import_module("music_assistant.providers.livephish.client")
    album = {
        "containerID": 1747,
        "artistID": 1,
        "artistName": "Phish",
        "containerInfo": "Moon Palace Resort",
        "performanceDate": "02/26/2022",
        "tracks": [{"trackID": 29990, "songTitle": "Axilla", "trackNum": 1}],
    }
    with (
        patch.object(module.LivePhishClient, "authenticate", AsyncMock()) as authenticate,
        patch.object(module.LivePhishClient, "album", AsyncMock(return_value=album)),
        patch.object(module.LivePhishClient, "favorite_albums", AsyncMock(return_value=[])),
        patch.object(module.LivePhishClient, "playlists", AsyncMock(return_value=[])),
    ):
        step = await mass.config.setup_provider(DOMAIN)
        assert step.type == FlowStepType.FORM
        assert {entry.key for entry in step.entries} == {"username", "password"}
        assert next(entry for entry in step.entries if entry.key == "password").type == (
            ConfigEntryType.SECURE_STRING
        )
        finish = await mass.config.submit_setup_flow(
            step.flow_id, {"username": "synthetic-user", "password": "synthetic-password"}
        )
        assert finish.type == FlowStepType.FINISH
        assert finish.result is not None
        provider = mass.get_provider(finish.result["instance_id"])
        assert isinstance(provider, MusicProvider)
        authenticate.assert_awaited()
        assert provider.max_concurrent_streams == 1
        track = await provider.get_track("1747:29990")
        assert track.name == "Axilla"
        assert track.media_type == MediaType.TRACK
        assert track.item_id == "1747:29990"
        assert "synthetic-password" not in str(mass.config.get("providers"))
        instance_id = provider.instance_id
        await mass.unload_provider(instance_id)
        await mass.load_provider(instance_id)
        reloaded = mass.get_provider(instance_id)
        assert isinstance(reloaded, MusicProvider)
        assert reloaded is not provider
        assert (await reloaded.get_track("1747:29990")).name == "Axilla"
        assert authenticate.await_count == 2


async def test_failed_login_returns_retryable_form(mass: MusicAssistant) -> None:
    """A rejected account returns a safe setup error and creates no provider instance."""
    module = importlib.import_module("music_assistant.providers.livephish.client")
    with patch.object(
        module.LivePhishClient,
        "authenticate",
        AsyncMock(side_effect=module.LivePhishAuthError("login: credentials expired or rejected")),
    ):
        step = await mass.config.setup_provider(DOMAIN)
        failed = await mass.config.submit_setup_flow(
            step.flow_id, {"username": "synthetic-user", "password": "synthetic-password"}
        )
        assert failed.type == FlowStepType.FORM
        assert failed.errors
        assert "synthetic-password" not in str(failed.errors)
        assert not any(provider.domain == DOMAIN for provider in mass.providers)
        await mass.config.abort_setup_flow(step.flow_id)
