#!/usr/bin/env bash
# Fetch the pinned grading toolchain into .cache/ (gitignored).
#   - Tons of Skills marketplace schema validator at a pinned commit (the grading authority)
#   - its kernel schemas (@intentsolutions/core) and the j-rig CLI, exact versions
#   - gitleaks, checksum-verified
# Bump MARKETPLACE_SHA and VALIDATOR_SHA256 together, deliberately.
set -euo pipefail
cd "$(dirname "$0")/.."

MARKETPLACE_SHA=eb855e5fe218ea1e320f993f10061db37009a7b3
VALIDATOR_SHA256=716e732fed464f2920379588f592d55cbeea2db525d9e3014a74b8b62aa6b197
JRIG_CLI=0.3.0
KERNEL=0.10.0

mkdir -p .cache/marketplace/scripts .cache/bin
url="https://raw.githubusercontent.com/jeremylongshore/tons-of-skills-marketplace/${MARKETPLACE_SHA}/scripts/validate-skills-schema.py"
curl --fail --location --silent --show-error --retry 2 "$url" -o .cache/marketplace/scripts/validate-skills-schema.py
echo "${VALIDATOR_SHA256}  .cache/marketplace/scripts/validate-skills-schema.py" | sha256sum --check --status \
  || { echo "schema validator checksum mismatch" >&2; exit 1; }

# The validator reads kernel schemas from node_modules beside it. --ignore-scripts:
# j-rig check needs no native SQLite build.
[[ -f .cache/marketplace/package.json ]] || echo '{"private": true}' > .cache/marketplace/package.json
npm install --prefix .cache/marketplace --no-save --no-audit --no-fund --ignore-scripts --silent \
  "@intentsolutions/jrig-cli@${JRIG_CLI}" "@intentsolutions/core@${KERNEL}"

[[ -x .cache/bin/gitleaks ]] || bash tools/install-gitleaks.sh .cache/bin
echo "toolchain ready in .cache/"
