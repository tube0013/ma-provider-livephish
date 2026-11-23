# Release and catalog submission

Nothing in this document authorizes a remote write. Repository publication, a release
and a catalog submission each require the maintainer's explicit request.

## Gates before publication and release

- Owner and repository confirmed on 2026-11-23: `tube0013/ma-provider-livephish`.
  Publication and a normal `v0.1.0` release were explicitly authorized in the session.
  Catalog submission remains unauthorized.
- Source provenance review completed: see PROVENANCE.md and NOTICE. The reference
  project's Go source is not included or treated as Apache-licensed.
- Run `.venv/bin/python -m pytest` and
  `.venv/bin/python -m pre_commit run --all-files` with the committed lockfile.
- Publish the reviewed source and run CI, including `catalog`, in the official
  nightly Linux server image. Do not treat the passing local macOS check as Linux
  CI evidence.
- Complete and record the HAOS acceptance table before submission. An import check
  cannot establish playback, seeking or transitions.
- Keep domain `livephish`, setup keys `username`/`password`, the `quality` option and
  composite `show:track` IDs. No stored-data rename or migration is introduced here.
- Update CHANGELOG.md and VALIDATION.md with the actual tested commit and results.

## First normal release

After tests pass and the maintainer explicitly requests the release, publish version
`v0.1.0` from the reviewed commit. It must be a **published normal GitHub release**, not
a draft or prerelease, even though the provider's manifest stage is alpha. No tag
prefix is needed for this single-provider repository. Ensure `pyproject.toml`, changelog
and release tag agree, and record the commit SHA in the HAOS test record.

Suggested release title: **LivePhish 0.1.0**

Suggested release body (update compatibility evidence before publishing):

> First standalone LivePhish music provider for Music Assistant. Browse and search
> Phish and side projects, import saved albums and playlists, and play entitled AAC,
> FLAC or ALAC through MA. An active LivePhish streaming subscription is required.
>
> Preserves composite track IDs and service-signed HTTP/HTTPS audio URLs inside the
> server, applies one concurrent MA stream, and honors rate-limit cooldowns. No
> downloading, exporting or playlist editing is provided.
>
> Compatibility and HAOS playback results: link the completed validation record for
> this release. Stable MA 2.10 support is not claimed. This is an unofficial integration.
>
> Setup and support: repository README and issue tracker.

## Submission form values

Only after a public repository, normal release, passing CI and HAOS tests exist, and
the maintainer explicitly requests submission, open the catalog's
[Submit a provider form](https://github.com/music-assistant/community-catalog/issues/new?template=submit-provider.yml).
The submitter must own the repository or be a code owner in its released manifest.

| Field | Proposed value |
| --- | --- |
| Repository | `tube0013/ma-provider-livephish` |
| Folder | `livephish` |
| Tag prefix | Leave empty |
| Moving from the server | Leave unchecked: this is a local experimental provider, not an upstream built-in |
| Repository/code owner confirmation | Maintainer confirms |
| Catalog rules confirmation | Maintainer reads and confirms |

Do not submit a generic issue or create the catalog's registry files yourself. The
submission workflow checks the latest release and a registry maintainer decides admission.
Later normal releases are discovered automatically. The catalog currently tests nightly,
beta and stable 2.11; compatibility is determined per channel, not assumed from the
provider's local tests.

Sources: [official template](https://github.com/music-assistant/community-provider-template),
[catalog admission](https://github.com/music-assistant/community-catalog#admission),
[exact requirements](https://github.com/music-assistant/community-catalog/blob/main/MAINTAINING.md#what-a-provider-needs),
and [submission form schema](https://github.com/music-assistant/community-catalog/blob/main/.github/ISSUE_TEMPLATE/submit-provider.yml).
