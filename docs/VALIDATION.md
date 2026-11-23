# Validation record

Prepared 2026-11-22; publication review updated 2026-11-23. Catalog admission and
HAOS functional playback testing are pending.

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

The initial local catalog check ran on macOS against the template's pinned server.
On 2026-11-23, [GitHub CI run 45234614930](https://github.com/tube0013/ma-provider-livephish/actions/runs/45234614930)
also passed all jobs on Linux: tests, lint/types/spelling and the official reusable
nightly catalog workflow. The latter ran in `ghcr.io/music-assistant/server:nightly`,
image digest `sha256:4589c6a7396a68e878c468898948ec5c439cdf49bb8e091df5a2aea42c6efe90`.
It checks installation/import on Linux amd64 and resolves any extra provider requirements
for arm64; there are no extra provider requirements here. An arm64 runtime/playback test
has not been performed. CI installation/import success does not establish audible HAOS
playback or the installed HAOS nightly's exact runtime behavior.

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

## Publication status and remaining HAOS work

GitHub owner/repository `tube0013/ma-provider-livephish` was confirmed and published
publicly on 2026-11-23. GitHub detects Apache-2.0. Source provenance review is complete
(see PROVENANCE.md and NOTICE). A normal `v0.1.0` testing release was explicitly
requested; catalog submission remains on hold.

- Coordinate the HAOS test window and speaker. NIGHTLY `2.11.0.dev2026112203` is running;
  stable `2.10.13` is installed but stopped. DEV SERVER is not installed.
- Complete audible playback, seeking, natural next-track transitions, full HAOS restart,
  natural token expiry, quality and concurrent-stream acceptance in HAOS_TESTING.md.

Passing a forced refresh probe is not evidence of a complete natural-expiry playback
session. Passing a provider reload test is not evidence of HAOS restart recovery.
Stable 2.10 compatibility is unverified and is not claimed.
