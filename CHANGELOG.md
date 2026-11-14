# Changelog

Notable changes to the standalone repository are recorded here. Package versions
and plugin display versions are separate; this log does not declare an npm release.

## Unreleased

### Added

- Contributor, support, security and agent guidance; ownership and issue/PR templates.
- Shared development dependency pins and automated dependency-update configuration.

### Changed

- CI action pins and time limits, documented local setup, and working-tree secret scanning.
- Ignore rules for local credentials, Terraform state and private evidence.
- Public homepage now points to the canonical repository README instead of a missing marketplace page.

## Standalone extraction — 2026-11-13

- Extracted from the Tons of Skills marketplace with source history preserved.
- Added standalone pinned tooling and offline CI for 26 skills, three reviewer
  agents and 11 eval packages.
- Retained the preceding NCCL transport and ellipsis-redacted Xid parsing fixes.
- Preserved package version 1.0.7 and plugin display version 1.15.0.

Earlier changes remain in [Git history](https://github.com/jeremylongshore/unofficial-coreweave-operator-pack/commits/main/).
