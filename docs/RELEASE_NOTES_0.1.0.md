Initial standalone LivePhish community music provider for Music Assistant.

- Browse and search Phish and side projects, concert shows, studio albums and song performances.
- Sync saved albums and playlists; preserve stable `show:track` IDs.
- Play subscription-entitled AAC, FLAC or ALAC through MA with a one-stream limit.
- Preserve signed HTTP/HTTPS audio URLs inside the server and honor API rate-limit cooldowns.

An active LivePhish streaming subscription is required. This is an unofficial integration;
the provider's manifest stage remains alpha.

### Validation

149 local tests pass, including real-MA discovery, secure setup, rejected login and
provider reload recovery. All [Linux CI jobs](https://github.com/tube0013/ma-provider-livephish/actions/runs/45234614930)
passed, including 149 tests, lint/types/spelling and the official nightly catalog
container check. Pre-commit checks pass. Live account login, entitlement,
show 1747 / Axilla metadata and forced in-memory token refresh were verified.
Source provenance and component attribution are documented in
[PROVENANCE.md](https://github.com/tube0013/ma-provider-livephish/blob/v0.1.0/docs/PROVENANCE.md).

Audible HAOS playback, seeking, next-track transitions, full app restart and natural
token expiry remain to be tested. Stable MA 2.10 compatibility is not claimed.
The provider has not been submitted to the community catalog.

### HAOS testing

Use **Music Assistant DEV SERVER**, with its own data, from the official
[HA add-on repository](https://github.com/music-assistant/home-assistant-addon).
A public release does not make this provider available for arbitrary-repository
installation into the normal NIGHTLY app's Marketplace.

The existing HAOS NIGHTLY app was observed running `2.11.0.dev2026112203` on
2026-11-23. Coordinate stopping it before starting DEV SERVER, which shares its ports.
Use these DEV SERVER options:

```yaml
log_level: info
server_repo: ""
frontend_repo: ""
provider_repo: "tube0013/ma-provider-livephish@v0.1.0"
safe_mode: false
```

The empty server/frontend settings use the DEV SERVER image's baked-in nightly;
record its actual version when testing. The public repository is fetched at startup.
The user signs in securely through MA. Stop DEV SERVER before returning to the original
NIGHTLY app.

See the [HAOS acceptance checklist](https://github.com/tube0013/ma-provider-livephish/blob/v0.1.0/docs/HAOS_TESTING.md)
and [validation record](https://github.com/tube0013/ma-provider-livephish/blob/v0.1.0/docs/VALIDATION.md).
