# HAOS test procedure

## Verified starting point (rechecked 2026-11-23)

Read-only Supervisor inventory:

| App | Installed version | State |
| --- | --- | --- |
| Music Assistant NIGHTLY | 2.11.0.dev2026112203 | Started |
| Music Assistant | 2.10.13 | Stopped |
| Music Assistant DEV SERVER | Not installed | — |

Recheck this inventory immediately before testing. No HAOS apps have been stopped,
installed, reconfigured or started during preparation. The running NIGHTLY app is the
one to return to afterward, unless the user chooses differently.

## Prerequisites

1. Use the confirmed public repository `tube0013/ma-provider-livephish`.
2. Use the `v0.1.0` release tag for a reproducible first test. Development branches,
   including `codex/community-catalog-prep`, can also be loaded directly; a release
   is not required by the DEV SERVER repository route.
3. Agree with the user on a test window and speaker before stopping the running NIGHTLY
   app or changing playback. Stop playback in other LivePhish clients too.
4. In the Home Assistant app store, use the official repository
   `https://github.com/music-assistant/home-assistant-addon` and install
   **Music Assistant DEV SERVER**. This is a separate app with separate private data.
   Do not copy production MA data or use `~/.musicassistant-livephish-dev` as its data.

The normal MA Marketplace is not an arbitrary GitHub repository installer.
The supported direct-repository route is the DEV SERVER app.

## Exact DEV SERVER options

For the initial release:

```yaml
log_level: info
server_repo: ""
frontend_repo: ""
provider_repo: "tube0013/ma-provider-livephish@v0.1.0"
safe_mode: false
```

The empty server/frontend settings use the versions baked into the DEV SERVER image.
Record the actual MA version shown after startup; a later installation may have a newer
base than the inventory above. `provider_repo` accepts a branch, tag, commit, or `@pr-12`.
For reproducible retests, replace the branch suffix with its published commit SHA.

Stop the running MA app during the coordinated window before starting DEV SERVER:
they use the same host ports. Open DEV SERVER, create its separate user and add LivePhish.
The user enters credentials securely in the setup form. Add only the chosen test player;
keep its volume low. A restart fetches updated provider code.

## Playback acceptance record

Run each case on the chosen HAOS player. Record provider commit, MA version, quality,
player model/protocol, time, observed behavior and pass/fail. Do not record service URLs.

| Case | Action | Expected result | Result |
| --- | --- | --- | --- |
| Login | Add LivePhish with an entitled account | Provider loads; catalog and setlist appear | Pending |
| Baseline | Play Axilla, show 1747, track 1747:29990 | Audible playback; elapsed time advances | Pending |
| Seek | Seek forward to 60 seconds, backward to 15 | Audio resumes near requested position | Pending |
| Transition | Queue two consecutive tracks from show 1747, let the first end | Next track starts once, in order | Pending |
| Manual next | Skip forward and back within the queue | Correct performances play; no stale URL failures | Pending |
| Restart | Stop audio, restart DEV SERVER, resolve 1747:29990 again | Fresh login/entitlement and correct metadata/playback | Pending |
| Entitlement refresh | After over 15 minutes, start another track | Recheck succeeds without a login prompt | Pending |
| Token expiry | After the actual token lifetime, start a new track | Refresh/relogin succeeds without leaking tokens | Pending |
| Quality | Test AAC, auto and entitled lossless separately | Only entitled quality plays; codec verified by MA | Pending |
| Concurrent playback | Attempt a second independent MA queue on a second player | MA honors the provider's one-stream limit | Pending |
| Recovery | Stop playback, temporarily disconnect network, then reconnect/retry | Safe error, then recovery without a request storm | Pending |

Do not provoke real 429s or change subscription/region to test denials. Mocked tests cover
those failure paths. Account-wide limits across other LivePhish apps still require the
user to stop those clients; the provider cannot police external sessions.

Natural token expiry on HAOS is distinct from the successful forced in-memory refresh
probe documented in VALIDATION.md. Audible playback, seeking and transitions cannot be
inferred from passing import checks or the `can_seek` flag.

## Return to production

Stop DEV SERVER first, then restart the MA app that was running before the test
(current inventory: NIGHTLY). Verify its original library, settings and player playback.
Leave stable 2.10.13 stopped unless the user explicitly chooses otherwise. DEV SERVER's
private test data can remain for future tests; never point production at it.

Sources: [DEV SERVER README](https://github.com/music-assistant/home-assistant-addon/blob/main/music_assistant_dev/README.md)
and [app options](https://github.com/music-assistant/home-assistant-addon/blob/main/music_assistant_dev/config.yaml),
inspected at commit `91b6950e8e57dc0be559e1cc9cd9c81f2390cd97`.
