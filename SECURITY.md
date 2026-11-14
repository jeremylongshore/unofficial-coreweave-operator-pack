# Security policy

This community pack is not affiliated with, endorsed by, or sponsored by CoreWeave, Inc.
This policy covers this repository's helpers, skill instructions and packaging.
Provider account incidents should also go through your provider's support process.

## Report privately

Email **jeremy@intentsolutions.io** with subject `CoreWeave community pack security`.
Do not open a public issue with an exploit, credential or customer evidence.
Include the affected commit/version, file, impact and a minimal synthetic
reproduction. Do not send live secrets, kubeconfigs, private logs or model data.

Reports receive best-effort triage. There is no guaranteed response or remediation
SLA. The maintainer and reporter will coordinate disclosure after assessing impact
and a fix; credit is optional and requires the reporter's consent.

## Maintenance scope

Fixes target `main`; older releases have no promised backport window. Use the
current source and check its CI results. No live-account validation, independent
security certification or bug-bounty payment is implied.

Potential issues include command execution from supplied evidence, secret leakage,
path traversal, false health assertions and bypasses of the human cost gate.
Missing or stale evidence must stay unknown or blocked. Review the
[quality limits](QUALITY.md) and [contribution safety rules](CONTRIBUTING.md#safety-and-evidence).
