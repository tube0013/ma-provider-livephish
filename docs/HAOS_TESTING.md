# HAOS test procedure

## Verified HAOS test environment (2026-11-23)

Read-only Supervisor inventory after the maintainer's playback tests:

| App | Installed version | State |
| --- | --- | --- |
| Music Assistant NIGHTLY | 2.11.0.dev2026112303 | Stopped |
| Music Assistant | 2.10.13 | Stopped |
| Music Assistant DEV SERVER | 2.11.0.dev2026112303 | Started |

The maintainer installed and operated DEV SERVER, entered credentials securely, and
performed the acceptance tests below. The assistant only read the app inventory and
recorded the report; it did not change HAOS configuration or playback. App version is
Supervisor-reported; an independent in-app server build string was not captured.

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

On 2026-11-23 the maintainer reported successful testing of the published standalone
provider in HAOS DEV SERVER. These are maintainer-observed functional results, distinct
from the automated tests. The maintainer also confirmed that these behaviors had worked
in the original local provider implementation before standalone packaging.

The screenshot supplied with the test report identifies the playback example as **Strange Design**, Trey
Anastasio, **11/21/26 Divided Sky Benefit with Billy Strings, Worcester, MA**,
provider track `2834:41607`. It shows the selected player **Amzn Echo Show 5 White**,
FLAC input at **44.1 kHz / 16-bit / stereo**, and FLAC output at
**48 kHz / 16-bit / stereo**. The selected protocol and exact quality-option settings
were not separately recorded. The screenshot is not copied into this repository.

| Case | Observed action | Result and evidence |
| --- | --- | --- |
| Login and browsing | Add provider, sign in, browse catalog, select a show and track | Passed — maintainer report |
| Playback | Start selected tracks | Passed — all attempted streams worked per maintainer; screenshot confirms the example above |
| Backward seek | Seek backward in the playing track | Passed — maintainer reported no issues |
| Natural transition | Let playback advance from one track to the next | Passed — maintainer report |
| Manual next | Manually advance to the next track | Passed — maintainer report |
| App restart recovery | Stop DEV SERVER, start it fresh, browse and play again | Passed — maintainer report |
| Lossless playback | Play the screenshot example on the Echo Show | Passed — FLAC input/output confirmed by MA's signal-path display |

Forward seeking, manual previous, every individual AAC/FLAC/ALAC option, natural token
expiry, concurrent-queue enforcement and network-outage recovery were not individually
identified in this report. The existing automated tests cover refresh/rejection,
entitlement/quality selection, URL handling and throttling; a prior real-account probe
also verified forced in-memory token expiry and refresh. These distinctions do not
invalidate the successful functional playback acceptance above.

For future regression runs, record the exact provider ref, in-app MA version, player
protocol, selected quality option and elapsed session duration. Do not record service URLs.

Do not provoke real 429s or change subscription/region to test denials. Mocked tests cover
those failure paths. Account-wide limits across other LivePhish apps still require the
user to stop those clients; the provider cannot police external sessions.

Natural token expiry on HAOS is distinct from the successful forced in-memory refresh
probe documented in VALIDATION.md. Playback, backward seeking, transitions and app restart
recovery now have maintainer-observed HAOS evidence.

## Return to production

Stop DEV SERVER first, then restart the MA app that was running before the test
(current inventory: NIGHTLY). Verify its original library, settings and player playback.
Leave stable 2.10.13 stopped unless the user explicitly chooses otherwise. DEV SERVER's
private test data can remain for future tests; never point production at it.

Sources: [DEV SERVER README](https://github.com/music-assistant/home-assistant-addon/blob/main/music_assistant_dev/README.md)
and [app options](https://github.com/music-assistant/home-assistant-addon/blob/main/music_assistant_dev/config.yaml),
inspected at commit `91b6950e8e57dc0be559e1cc9cd9c81f2390cd97`.
