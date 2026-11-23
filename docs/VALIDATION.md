# Validation record

Prepared 2026-11-22; publication and HAOS acceptance updated 2026-11-23.
The maintainer reports successful HAOS functional playback testing. Catalog submission
and admission remain on hold.

## Source and runtime

| Input | Revision |
| --- | --- |
| Original working checkout | `165eb3a03d764aaa9a87f3883b660b2a38da4202` |
| Official community-provider template | `a0f66150438d843f013924c9d6f1738b56ecfbdd` |
| Official catalog checker | `78c6043f5cab20acc58b4ce6773f8d86f9315f24` |
| Official HAOS add-on | `91b6950e8e57dc0be559e1cc9cd9c81f2390cd97` |
| Pinned MA test runtime from template | `126c6d646ec14ee680e7051258e82dab0a09bac2` |
| Local Python | 3.14.7, existing interpreter via `.venv/bin/python` |
| Linux CI Python | 3.14.4 |
| First successful GitHub CI source | `3ba7838da4cf8ff0cf66d0b36e838303d5255535` |
| Standalone provider content SHA256 | `5a376d72b1616fb7cee3ee22ef84c8e58e6983a287d120facee2d414bc8c12da` |

The working checkout was clean before inspection and remains unchanged. Its current
implementation already had HTTP/HTTPS stream validation, catalog search, artist releases,
favorites and playlist sync; it was not the earlier manually configured show-ID starter.
The extraction retained its setup keys, option key, provider domain and composite IDs.
No live database was opened or modified. Development settings were read only to verify
the configured account. No global Python installation or PATH change was made.

## Completed checks

| Check | Result and scope |
| --- | --- |
| Original provider baseline | 132 tests passed in the original checkout |
| Standalone test suite | 149 passed, including migrated regressions, official template file checks and real-MA setup tests |
| Real MA boot/discovery | Community-tier discovery from this repository, secure setup form and persisted encrypted synthetic password |
| Real MA account failure | Mocked rejected credentials return a retryable form without creating a provider |
| Real MA provider reload | Unload/reload authenticates again and resolves composite `1747:29990` without transient lookup state |
| Lint/format/types/spelling | All pre-commit hooks passed: Ruff check, Ruff format, mypy and codespell |
| Official local catalog checker | `registry.check.check_folder` passed with current reserved domains, manifest/content/icon checks, dependency activation and isolated MA import |
| Provider dependencies | Empty manifest requirements; no extra provider wheels needed |
| Live account authentication | Passed using the configured development account; credentials never printed |
| Live subscription entitlement | Passed |
| Live show/track metadata | Show 1747 contains track 29990 (Axilla) |
| Live token refresh | Passed after forcing only the in-memory token/entitlement deadlines to expire |
| GitHub Linux tests | 149 passed on Python 3.14.4 |
| GitHub Linux lint/types/spelling | Passed |
| Official nightly container check | Passed: `livephish: passed` |
| HAOS login, browse and playback | Passed — maintainer report on 2026-11-23 |
| HAOS backward seeking | Passed — maintainer report |
| HAOS natural transition and manual next | Passed — maintainer report |
| HAOS app restart recovery | Passed — maintainer stopped/started DEV SERVER, then browsed and played successfully |
| HAOS lossless signal path | Screenshot: FLAC 44.1 kHz / 16-bit stereo input, FLAC 48 kHz / 16-bit stereo output on Amzn Echo Show 5 White |

The initial local catalog check ran on macOS against the template's pinned server.
On 2026-11-23, [GitHub CI run 45234614930](https://github.com/tube0013/ma-provider-livephish/actions/runs/45234614930)
also passed all jobs on Linux: tests, lint/types/spelling and the official reusable
nightly catalog workflow. The latter ran in `ghcr.io/music-assistant/server:nightly`,
image digest `sha256:4589c6a7396a68e878c468898948ec5c439cdf49bb8e091df5a2aea42c6efe90`.
It checks installation/import on Linux amd64 and resolves any extra provider requirements
for arm64; there are no extra provider requirements here. The CI run does not establish
arm64 playback coverage, and the HAOS host architecture was not captured. CI installation/import
success is separate from the maintainer-reported HAOS playback results now
recorded in HAOS_TESTING.md.

Local verification commands:

```sh
.venv/bin/python -m pytest -q
.venv/bin/python -m pre_commit run --all-files
```

For the local catalog check, the standalone `.venv/bin/python` imported the downloaded
catalog's `registry.check.check_folder`, loaded its `reserved_domains.json`, and checked
`livephish/`. The checker returned `passed=True`, with no reason/output/unavailable flag.
It does not authenticate the provider or play audio. The real service probe separately
performed login, entitlement, show metadata and refresh calls only; no audio URL was
requested and no audio was downloaded, written or played.

## Review findings and changes

| Area | Outcome |
| --- | --- |
| Token lifetime | Finite positive TTL required; proportional early-expiry margin; auth lock coalesces concurrent refreshes |
| Refresh failures | Only invalid-grant rejection permits password fallback; transient outages retain the refresh token |
| Revoked access | HTTP 401 invalidates token and entitlement deadlines; next protected action reauthenticates. The failed action surfaces a safe error and may require retry |
| Subscription/quality | Explicit entitlement required; lossless only with reported HighQuality access; no tier or region bypass added |
| Request security | Credentials in HTTPS identity POST; bearer headers on HTTPS account APIs; redirects disabled |
| Safe errors | Stage and HTTP status only; connection/JSON errors hide request URLs and bodies |
| Rate limits | Serialized API calls, at least one second apart; 429 cooldown shared across API hosts. Fixed HTTP-date handling and removed the one-hour cap so long waits are honored |
| Repeated metadata | Bounded in-memory caches, locks on misses, one-hour metadata expiry, one-minute account-response expiry |
| Catalog scope | Saved-library sync does not walk the service catalog. Artist listing remains scoped to one artist. Studio-album browsing now requests only album pages, avoiding concert enumeration |
| Audio URLs | Existing fix retained: accept HTTP/HTTPS with host, reject userinfo/invalid URLs, return the signed string unchanged only to MA's internal stream resolver |
| Stream limit | Existing `max_concurrent_streams = 1`, single provider instance; cannot enforce sessions opened in external apps |
| Setup/data | Existing username/password and quality keys retained; no stored-data migration introduced |
| Packaging | `livephish/`, English manifest/setup strings, provides, real existing codeowner, confirmed documentation/support URLs, Apache-2.0, NOTICE, template CI and lockfile |

The original album-browse and search parsing were split into private helpers to meet
the template's complexity checks. No other feature rewrite was undertaken. The original
checkout has not received these standalone changes.

## Publication and HAOS acceptance status

The public repository and normal `v0.1.0` release were published on 2026-11-23 at
`0aea80f7fe72e452cc623edaf2eebd5000f5a773`. [Final CI run 45235274555](https://github.com/tube0013/ma-provider-livephish/actions/runs/45235274555)
passed all jobs on that exact commit. The published archive was verified against the
provider content hash above. GitHub detects Apache-2.0. Source provenance review is
complete (see PROVENANCE.md and NOTICE). Catalog submission remains on hold.

The maintainer subsequently installed DEV SERVER, added LivePhish, signed in, browsed,
and successfully tested playback, backward seeking, automatic next-track transitions,
manual next and stop/start app recovery. All attempted audio streams worked. The
screenshot confirms lossless FLAC for Strange Design, provider track `2834:41607`,
on Amzn Echo Show 5 White. See HAOS_TESTING.md for the detailed acceptance record.

A read-only Supervisor check on 2026-11-23 found DEV SERVER
`2.11.0.dev2026112303` started, NIGHTLY `2.11.0.dev2026112303` stopped, and stable
`2.10.13` stopped. The app version was read independently; the playback observations
are the maintainer's report, supported by the screenshot's signal-path details.

Natural token expiry over a complete HAOS session was not specifically reported;
the earlier real-account forced refresh and mocked expiry tests remain its current
evidence. Individual quality-option coverage, concurrent-queue enforcement and outage
recovery were not itemized. Stable 2.10 compatibility is unverified and is not claimed.

This documentation update records successful testing. Provider code and the published
v0.1.0 tag and release assets are unchanged; catalog submission remains pending.
