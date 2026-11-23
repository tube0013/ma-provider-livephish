# Source provenance review

Reviewed 2026-11-23 for the initial public release of `tube0013/ma-provider-livephish`.

## Result

The earlier open item was whether the LivePhish API research reference introduced
unlicensed source into this provider. Review of the original Git history, the Python
implementation, the reference Go source and the files being published found protocol
compatibility material, rather than copied downloader implementation text or assets.
The source audit is complete; no unlicensed downloader source was identified for removal.
The repository retains Apache-2.0 for its Python provider and template-derived material,
with the research reference credited separately in NOTICE.

The reference's lack of a license is not treated as permission to redistribute its code.
It is not a dependency, vendored component, executable, or source archive of this project.
This is a source-comparison finding, not a claim that the reference project itself is
Apache-licensed or that the service endorses this integration.

## Source inventory

| Material | Evidence and treatment |
| --- | --- |
| LivePhish Python provider, setup, English strings, icons and unit tests | Introduced in the maintainer's local MA checkout by `tube0013` in `1c3da78bb35d2f9adebbc3347c23c2523feec7fd`; follow-up fixes in `5c331a6a193c715880f9d9fbb6c83add14cebffa` and `165eb3a03d764aaa9a87f3883b660b2a38da4202`. Extracted from that working checkout, not generated from the Go project during packaging. |
| MA provider integration patterns | The built-in Nugs provider informed the integration. Music Assistant server is Apache-2.0; its attribution and license are retained. |
| Repository layout, file tests, CI and development container | Adapted from official community-provider-template commit `a0f66150438d843f013924c9d6f1738b56ecfbdd`, Apache-2.0. The root LICENSE is byte-identical to the template's license. |
| Standalone fixes, server-loading/transport tests and documentation | Added in this repository during preparation and review. Distributed under its Apache-2.0 license. |
| Dependencies | Resolved in `uv.lock`, not vendored source. The installed provider's manifest has no extra package requirements. |
| Test records | Small synthetic API-shaped records and public show/track identifiers; no captured account responses, artwork files or music. |

Original checkout commit IDs identify the local development history, not additional
repositories that must be installed or published. Only this standalone repository is
being published.

## API research reference

Reference: [jlamons/LivePhish-Downloader](https://github.com/jlamons/LivePhish-Downloader),
a fork of [Sorrow446/LivePhish-Downloader](https://github.com/Sorrow446/LivePhish-Downloader).
Inspected source revision: `1009d19c8e9c2404807e59430c2fdd7a1e8ce394`.
No license file exists at that revision; GitHub's license metadata for both repositories
was null when checked on 2026-11-23.

Comparison focused on the API-facing portions of `main.go` and `structs.go` against
`livephish/client.py`, provider parsing and setup. Shared material consists of service
field/method names, OAuth parameters, public app client/signing constants, quality
platform numbers, response keys and the signing procedure needed for interoperability.
The shared Python/Go string literals were reviewed: 37 in the client, 17 in provider
parsing and the setup step name `user`. These are protocol or ordinary vocabulary,
not copied error messages, documentation, comments or downloader features.

The implementation is materially different:

- The Python client uses modern subscription and stash APIs, rotating refresh tokens,
  explicit entitlement validation, asynchronous locks, bounded expiring caches, paced
  requests and shared rate-limit cooldowns. The Go reference uses legacy secure API
  user/subscription calls and a synchronous downloader workflow.
- The Python web-stream signature uses the observed millisecond timestamp format and
  web playback parameters. The Go reference uses its older seconds-based signature and
  Android request shape. The common signing prefix and payload field names describe
  service interoperability, not a copied implementation.
- Go downloader file naming, CLI/config parsing, progress reporting, Go response
  structs, media-file writes and download loops are absent. No Go source, Go module
  files, downloader binaries, reference config, screenshot, archive or README prose
  is tracked in this repository or its publication history.

Copyright protection of program expression is distinct from functional algorithms
and system design; see the [U.S. Copyright Office's Circular 61](https://www.copyright.gov/circs/circ61.pdf).
That distinction supports documenting protocol research separately from source reuse.
For unlicensed source itself, [GitHub's licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)
explains why public visibility alone does not grant an open-source license.

## Publication checks

The published Git history is limited to the standalone provider repository. Neither the
original MA development data nor the downloaded research checkout is included. Account
credentials, encryption keys, cookies, bearer/refresh tokens and signed playback URLs
are excluded. API client/signing constants embedded in the provider are service protocol
constants, not credentials copied from the maintainer's account.

No upstream author's permission or new license was obtained or claimed, and no message
was sent to either reference project. New third-party source must receive its own
provenance/license review before inclusion.
