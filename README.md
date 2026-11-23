# LivePhish for Music Assistant

An unofficial community music provider for [Music Assistant](https://music-assistant.io).
Browse Phish and side projects, search shows and individual performances, sync saved
releases and playlists, and play audio through Music Assistant to your own speakers.
An active LivePhish streaming subscription is required. LivePhish, Nugs and Phish do
not sponsor or endorse this provider.

This provider is **not yet admitted to the community catalog**. The initial `v0.1.0`
release is intended for testing with the nightly-based HAOS DEV SERVER. See
[releases](https://github.com/tube0013/ma-provider-livephish/releases) and the
[validation record](docs/VALIDATION.md) for the current evidence and limitations.

## Features and account access

- Browse artists, concert years, recent shows and studio albums.
- Search artists, releases and individual song performances.
- Read saved albums and playlists into the MA library; playlist order and duplicates
  are preserved. Editing the LivePhish library from MA is not implemented.
- Resolve tracks from stable `show:track` IDs, including `1747:29990` (Axilla,
  02/26/22 Moon Palace Resort).
- Select automatic, AAC, FLAC or ALAC quality. Automatic selects FLAC only when the
  service reports HighQuality entitlement; otherwise it selects AAC. Explicit
  lossless selection fails when that entitlement is absent.
- Allow one concurrent stream. Stop playback in other LivePhish clients before testing.

Catalog browsing does not import the whole catalog into your library. Library sync
reads your saved releases and playlists. Artist album listing fetches only that artist's
releases, with cached, paced pagination. Catalog and album metadata expire after an hour;
account library responses expire after a minute. Caches are bounded and stay in memory.

## Installation and login

Once this provider has a published release and has been admitted, enable the community
catalog in Music Assistant's Marketplace and install LivePhish there. Until then, use
the [HAOS DEV SERVER testing procedure](docs/HAOS_TESTING.md). A normal NIGHTLY app
cannot install an arbitrary provider repository through Marketplace; publishing a
release does not change that.

Add LivePhish under Settings → Music sources. Enter your LivePhish email and password
in MA's setup form. MA stores setup secrets encrypted in its own configuration. Access
and refresh tokens stay in memory, and entitlement is rechecked at most every 15 minutes
or before token expiry. A rejected refresh token allows one password login attempt;
network failures do not trigger repeated password logins. Reconfigure the provider if
your credentials change.

Login and API requests use HTTPS and do not follow redirects. LivePhish may return an
HTTP audio URL: valid HTTP and HTTPS URLs are preserved exactly, including signatures,
and are used only inside the server. This provider never downloads or archives audio.

## Compatibility and development

Development targets Python 3.14 and the exact server revision in `pyproject.toml`, inherited
from the official template. HAOS inventory on 2026-11-22 showed NIGHTLY
`2.11.0.dev2026112203` running and stable `2.10.13` stopped. Stable 2.10 compatibility is
not claimed. Current catalog channels start at stable 2.11. See
[validation evidence and remaining work](docs/VALIDATION.md).

Use an existing Python 3.14 interpreter. Do not install global Python or change PATH:

```sh
# Substitute the absolute path of your existing virtual-environment Python.
/absolute/path/to/existing/.venv/bin/python -m uv sync \
  --python /absolute/path/to/existing/.venv/bin/python --no-python-downloads --locked
.venv/bin/python -m pytest
.venv/bin/python -m pre_commit run --all-files
scripts/run.sh
```

The runner uses this repository's `.venv/bin/python` and stores its separate data in
`.data/`. It must not point at production or the original experimental data directory.
The optional VS Code development container supplies the server's Linux base and ffmpeg;
local playback needs a compatible ffmpeg installation. Tests boot a real MA server on
loopback with temporary data, mocked discovery and synthetic account responses; no real
credentials or audio are needed.

The manifest has no additional dependencies. The server supplies aiohttp and MA models.
CI runs lint, type, spelling and provider tests plus the official reusable nightly
catalog checks. Those catalog checks verify installation and import, not audible playback.

## Support and release

Report reproducible problems in the [provider issue tracker](https://github.com/tube0013/ma-provider-livephish/issues)
and include MA version, provider release, player type and
steps to reproduce. Remove credentials, cookies, tokens, account identifiers and signed
stream URLs from any logs before sharing them. Start with info logging.

[Release and submission procedure](docs/RELEASING.md) covers the first release
and the official submission form. Follow the
[community catalog rules](https://github.com/music-assistant/.github/blob/main/COMMUNITY_CATALOG_RULES.md)
and Music Assistant's
[usage policy](https://github.com/music-assistant/.github/blob/main/USAGE_POLICY.md).

## License and acknowledgements

Apache-2.0; see [LICENSE](LICENSE) and [NOTICE](NOTICE). The standalone layout and checks
come from the official community-provider template. The MA Nugs provider and the
LivePhish protocol research reference are recorded in NOTICE and the completed
[source provenance review](docs/PROVENANCE.md). No downloader is included.
