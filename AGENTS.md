# Agent instructions

This repository is the source of truth for `coreweave-pack`. The marketplace copy
is a mirror. Read [CONTRIBUTING.md](CONTRIBUTING.md), [QUALITY.md](QUALITY.md), and
the affected skill's `docs/BLUEPRINT.md` before editing.

- Preserve user work and use a focused branch and pull request.
- Keep helpers offline, read-only and safe with untrusted evidence. Never run
  against a real CoreWeave account, create billable resources or execute pasted logs.
- Never ingest or publish private corpora, credentials or customer data.
- Preserve the shared cost gate and every skill's non-affiliation disclaimer.
- Write original content; official proprietary skills are not a source to copy.
- Keep the package and plugin display versions independent. No automatic release,
  npm publish, marketplace write or provider-backed evaluation is authorized by a code edit.
- Run the local checks in CONTRIBUTING.md. Use `.cache/` for new validation receipts.
  Static grades, fixture checks and model evaluation are separate evidence classes.
- Use the existing issues and PRs for repository work; no new tracker is required.
- Do not weaken CI or bypass repository protection. Preserve existing history.

The `skills/` tree contains the shipped skills and their isolated resources;
`shared/` contains canonical cost/evidence helpers; `agents/` has restricted
reviewers; `tests/` contains offline regressions; `tools/` bootstraps and runs the
pinned validator. Changes to shared copies must satisfy the pack gate.
