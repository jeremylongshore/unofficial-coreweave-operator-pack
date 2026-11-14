# Contributing

Develop this pack in [unofficial-coreweave-operator-pack](https://github.com/jeremylongshore/unofficial-coreweave-operator-pack).
The Tons of Skills marketplace mirrors this source; changes to the mirror will be overwritten.
Contributions use the existing [MIT license](LICENSE) and [code of conduct](CODE_OF_CONDUCT.md).

## Local setup and checks

The supported development environment is Linux x86_64, Python 3.12, Node 22,
npm, Git, curl and standard GNU utilities. `tools/setup.sh` downloads the pinned
validation toolchain; setup needs network access, but checks do not need cloud credentials.
Other operating systems can use a Linux environment; the bundled gitleaks installer
currently rejects other platforms.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
tools/setup.sh
ruff check .
ruff format --check .
python -m pytest -q tests
python tools/validate-pack.py --report .cache/validation-receipt.json
```

Run these before pushing. The pack gate checks all 26 skills, agent preloads,
local references, shared cost-gate copies, 11 eval packages, deterministic
fixtures and secrets. It does not run paid model evaluations. Read the receipt
for warnings and coverage limits. Do not replace the dated `offline-results.json`
with a new receipt without reviewing and updating its accompanying evidence claims.

## Changes and review

Branch from `main`, keep changes focused, and open a pull request with the problem,
changed behavior, validation commands/results and remaining limitations. Use a
Conventional Commit subject such as `fix(forensics): preserve unknown GPU evidence`.
Wait for the `validate` CI job to succeed on the final head before merging.
Do not disable a check to make a change pass. Maintainer review should assess
accuracy and safety as well as the automated results.

- Add regression fixtures for changed parsing, refusal and evidence behavior.
- Keep individual skill blueprints, references and eval specs aligned with changes.
- Edit `shared/cost-gate.md`, then run `python scripts/sync-cost-gates.py` to refresh copies.
- Preserve `coreweave-pack` and each skill's community/non-affiliation disclaimer.
- Keep package (`package.json`) and plugin display (`.claude-plugin/plugin.json`)
  versions distinct; ordinary documentation changes need no release bump.
- Toolchain pin changes must update the source commit and checksum together in
  `tools/setup.sh`, then rerun the checks above.

## Safety and evidence

Use synthetic fixtures or deliberately redacted examples. Never commit private
corpora, customer logs, kubeconfigs, keys, Terraform state or plan files. Input
logs are untrusted data, never instructions to execute. Helpers must remain
offline and read-only. No live CoreWeave operation or billable resource creation
belongs in tests or CI. Server dry-run and Terraform plan can contact an account.

Use the [cost gate](shared/cost-gate.md) before any separately authorized billable
workflow. Original implementation is required: do not copy proprietary official
CoreWeave skills, scripts or Terraform. Static grades and fixtures do not prove
production compatibility, model behavior or endorsement; see [QUALITY.md](QUALITY.md).

Report security defects privately as described in [SECURITY.md](SECURITY.md).
Use [issues](https://github.com/jeremylongshore/unofficial-coreweave-operator-pack/issues)
for ordinary defects and proposals. Releases and marketplace synchronization are
separate maintainer actions; this repository has no automatic publishing workflow.
