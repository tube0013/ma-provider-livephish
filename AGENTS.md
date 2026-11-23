# AGENTS.md

This repository is a community provider for Music Assistant, an async Python server that plays
music from streaming services and libraries on the user's own speakers. Servers install it from the
community catalog; the README links the rules of the catalog and says how to develop, test and
release.

## Never write code that

- gets around an account, a subscription tier, a region or a service's limit of streams, or gets
  around copy protection to give more than the service's own app gives the user's account
  (decoding protected audio with the user's own account to play it is fine);
- downloads, exports or archives music, or writes audio of a service to disk;
- hands a service's own audio address to anything outside the server (a media item, an API result
  or a route);
- calls a service's API without a throttler, asks again for what the cache holds, keeps sending
  while the service asks to wait, or walks its catalogue for one user action;
- sends the user's data anywhere but the service it connects to, loads code from somewhere else
  while it runs, or does something the manifest's description does not mention;
- offers AI assistants tools (`mcp_tools`) whose description or results do more than describe the
  tool and report what it did;
- mainly exists to load other providers, or third-party lists of sources;
- writes into the provider's own folder.

The [community catalog rules](https://github.com/music-assistant/.github/blob/main/COMMUNITY_CATALOG_RULES.md)
have the full text.

## How to work here

- `.venv/bin/python -m pytest`, `.venv/bin/python -m ruff check .`, `.venv/bin/python -m ruff format .`, `.venv/bin/python -m mypy` and
  `.venv/bin/python -m codespell_lib` must pass.
- Never block the event loop; wrap blocking calls in `asyncio.to_thread`.
- Requirements in `manifest.json` are package names with version specifiers only, and come as
  wheels for the Python version and platform of the server: a package that only comes as source
  cannot be installed.
- `provides` in `manifest.json` is for discovery only, such as the filters of the Marketplace;
  what the provider does always comes from its code. A music provider lists the media types it
  offers whatever its config or account (`artist`, `album`, `track`, `playlist`, `radio`,
  `podcast`, `audiobook`, `sound_effect`); a plugin lists its main features (`audio_source`, `ai`,
  `tts`, `scrobble`, `assistant`, `visualizer`, `recommendations`, `fun`).
- Follow the server's code style: Sphinx docstrings with `:param:`, the summary of a multi-line
  docstring on the line after the quotes, comments only where the code is not obvious.
- The server pin is the `music-assistant` line in `pyproject.toml`; change it only when asked.

Use .venv/bin/python explicitly. Never install a global Python or change PATH.
Run .venv/bin/python -m pre_commit run --all-files after code changes.
Do not publish or send GitHub messages without explicit user authorization.
