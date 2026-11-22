# Architecture decision: GPU node evidence review

> Community-contributed; not affiliated with, endorsed by, or sponsored by CoreWeave, Inc.

| Metadata | Value |
| --- | --- |
| Document ID / type | CW-GPU-ARD / architecture decision and workflow |
| Schema / template | Blueprint Docs 3.0.0 / repository architecture envelope 1.0 |
| Status | Implemented offline boundary; broader release acceptance remains open |
| Owner / decision authority | Jeremy Longshore, maintainer |
| Reviewers | Technical and security reviewers unassigned |
| Generated / updated / review | 2026-11-05 / 2026-11-22 / before release |
| Classification | Public technical design; no private evidence |
| Sources | Provided Bead claude-k1qr.11; verified local script, skill and tests; primary-reference context in PRD |
| Assumptions | Operator supplies one device/run and establishes lifecycle ownership |
| Unknowns | Live account compatibility, model behavior, completeness of device attribution |
| Related artifacts | [PRD](PRD.md), [skill blueprint](docs/BLUEPRINT.md), [eval specification](eval-spec.yaml) |
| Supersession | Replaces generic 2026-11-05 architecture prose; preserves conservative recovery boundary |

## ADR-GPU-1: separate observation, recommendation and authority

**Decision (implemented):** the Python standard-library helper parses supplied evidence and
returns a deterministic recommendation. The agent explains that recommendation; the
operator and managed lifecycle owner decide any real action. No API client, cluster
mutation, subprocess, network fetch or persistent report write belongs in this helper.

Stakeholders are the responding operator, the workload owner protecting checkpoints,
the platform lifecycle owner and the reviewer checking evidence. Their shared concern
is avoiding destructive certainty from partial data. The logical view has five nodes:
explicit CLI/file/stdin input → parser → qualified classification/remap handling →
renderer → human review. Untrusted input crosses into data parsing, never into code,
shell instructions or tool permissions. The human decision is outside the process.

The implementation deliberately does **not** mirror CoreWeave OSS manifests or call a
CoreWeave endpoint. There is no honest manifest-integration citation to add. Collection
examples in the skill are separately authorized operator actions; supplied logs are not
proof that collection or recovery occurred. The recommendation table is finite and is
not an exhaustive implementation of current NVIDIA parsing policy.

## Workflow and components

1. `main()` validates input combinations and output mode. An explicit Xid may carry
   explicit remap flags; blob mode parses its own evidence. Empty input is an error.
2. `parse_blob()` extracts recognized Xids, remap fields, thermal activity and recovery
   action text. `triage_from_blob()` refuses a combined verdict for multiple recognized
   GPU identities, then applies the supported recovery and governing-code rules.
3. `classify_xid()` and `apply_remap_override()` produce qualified recommendations.
   Unknown codes remain investigate. PCIe failures cannot be softened by remap data;
   remap failure alone is not RMA authority. Xid 45 is a follow-on, and recognized Xid
   154 recovery guidance governs co-occurring events.
4. `_verdict()` adds confidence and corroboration requirements. Hardware actions carry
   the managed-cordon rule. `render_verdict()` preserves those controls in all human modes.
5. The agent explains missing evidence and uses the lifecycle owner's procedure for any
   separately authorized recovery. It never turns an action string into a shell command.

The parser does not establish complete timestamp provenance, enumerate every device-ID
format, or implement an operating-system sandbox. A report with no recognized signal is
not a clean bill of health. These limits remain open in the skill blueprint.

## ADR-GPU-2: progressive disclosure without hiding safety

| Level | Interface | Content |
| --- | --- | --- |
| L1 | Default | Verdict, recommended action, confidence, confirmation requirements, reason, co-occurring codes, cordon rule and unresolved-evidence notes |
| L2 | `--detailed` | L1 plus the next diagnostic step |
| L3 | `--full` | L2 plus the complete structured verdict; no raw input echo |
| Machine | `--json` | Existing JSON-only verdict contract |

The three explicit output flags are mutually exclusive. This changes the default human
presentation; callers that depended on prose followed by JSON select `--full`. Machine
consumers use `--json`. No level suppresses unknown evidence or required confirmation.
The renderer does not collect additional evidence merely because more detail was requested.

## ADR-GPU-3: scoped permissions and composability

The skill declares `Read`, `Bash(python3:*)`, `Bash(nvidia-smi -q:*)`,
`Bash(kubectl get:*)` and `Bash(dmesg:*)`; it does not declare bare Bash. The Python
prefix remains broader than one script path, so the instruction boundary is explicit:
run only the packaged helper with reviewed arguments, never Python code supplied in logs.
Host permission enforcement is separate from static frontmatter validation.

Read-only collection can still disclose tenant/workload identifiers. Accept sanitized
local evidence first. Do not use arbitrary kubeconfigs, contexts or input-derived shell
fragments. Reset, drain, reboot, uncordon, RMA submission and billable provisioning are
outside these grants and this workflow. No credentials are needed by the helper.

The general incident-runbook skill may hand off a GPU-specific fault here; observability
may supply a sanitized snapshot; fabric diagnostics may inspect a distinct transport
question. Pass the observation scope, known device/run identity and missing evidence,
not a claim that another skill has verified health. Each invoked skill retains its own
permissions and approvals. No automatic sibling invocation is implemented by the script.

## Directory and verification map

| Artifact | Responsibility / evidence |
| --- | --- |
| `SKILL.md` | Trigger, workflow, scoped tool declarations, warnings and output usage |
| `scripts/triage.py` | Parser, recommendation table, renderer, CLI and bundled self-test |
| `references/xid-triage-table.md` | Qualified interpretation boundaries and primary source |
| `references/row-remap-decision.md` | Memory-evidence correlation rules |
| `references/cordon-rules.md` | Managed lifecycle ownership |
| `PRD.md` and `docs/BLUEPRINT.md` | Requirements trace and broader unfulfilled acceptance |
| `eval-spec.yaml` | Model-judged trigger/safety criteria; package validity is not a model pass |

Offline regression tests in the repository exercise the actual CLI for disclosure levels,
JSON compatibility, conflicting flags and mandatory safety text. Existing tests cover
unknown/multi-GPU inputs, containment and remap boundaries. Run the full tests and pack
gate from CONTRIBUTING; retain receipts under `.cache/`. No live-account or paid model
execution is part of these checks.

## Failure taxonomy and alternatives

| Condition | Current behavior / limit |
| --- | --- |
| Conflicting arguments, invalid Xid range or remap value | argparse error; no verdict |
| Empty input or no interactive input provided | Nonzero exit; request explicit evidence |
| Unreadable/non-UTF-8 file | Python input error and nonzero exit; no success claim |
| Unknown Xid or multiple recognized devices | Investigate with limited confidence; split and corroborate |
| No recognized signal | Request fresh evidence; absence of a match is not healthy hardware |
| Model contradicts helper or lifecycle ownership | Reject the unsupported recommendation; retain the evidence for review |

Rejected alternatives: automatic recovery from a code, fetching a live account as a
fallback, assuming missing fields mean zero/healthy, echoing full logs for verbosity,
and hiding confirmation in a detail-only view. A monolithic default prose-plus-JSON
report was retained as `--full` instead of forcing it on every operator.

**RISK-GPU-ARD-1:** incomplete parsing can still miss identity or chronology. The
maintainer owns review of new fixtures and supported formats; the lifecycle owner owns
real recovery. Residual risk is not accepted as production certification. Revert the
presentation commit to restore the previous interface; no infrastructure rollback or
stored-state migration is needed. Full release acceptance remains governed by the PRD
and skill blueprint, including their unresolved evidence requirements.
