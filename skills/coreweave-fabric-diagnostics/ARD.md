# Architecture decision: NCCL transport evidence review

> Community-contributed; not affiliated with, endorsed by, or sponsored by CoreWeave, Inc.

| Metadata | Value |
| --- | --- |
| Document ID / type | CW-FABRIC-ARD / architecture decision and workflow |
| Schema / template | Blueprint Docs 3.0.0 / repository architecture envelope 1.0 |
| Status | Implemented offline boundary; broader release acceptance remains open |
| Owner / decision authority | Jeremy Longshore, maintainer |
| Reviewers | Technical and security reviewers unassigned |
| Generated / updated / review | 2026-11-05 / 2026-11-22 / before release |
| Classification | Public; sanitized or synthetic diagnostics only |
| Sources | Provided Bead claude-k1qr.15; verified script/tests; retained research context below |
| Assumptions | Supplied evidence belongs to an operator-identified run and communicating containers |
| Unknowns | Live topology, effective admission, model behavior and measured performance baseline |
| Related artifacts | [PRD](PRD.md), [skill blueprint](docs/BLUEPRINT.md), [eval specification](eval-spec.yaml) |
| Supersession | Replaces generic 2026-11-05 prose, including the inapplicable cost-renderer assertion |

## ADR-FABRIC-1: observations stay separate from fabric health

**Decision (implemented):** parse local NCCL, resource and port evidence into separate
observations. Transport selection, GPU-direct evidence, resource configuration and
bandwidth are different facts. A single positive signal cannot certify the path.
The helper never queries Kubernetes, installs drivers, runs benchmarks or changes a Pod.

The workload operator needs an explanation of a slow run; the platform owner controls
network/node changes; the reviewer needs reproducible evidence without tenant secrets.
The logical view is explicit file/stdin → independent detectors → qualified result →
renderer → operator review. The trust boundary separates untrusted pasted data from
instructions and execution. PyYAML safe loading is used for resource blocks; it does
not turn arbitrary YAML into a trusted Kubernetes object or an admitted Pod.

## Components and workflow

1. `main()` validates input and mutually exclusive output flags. File reads are local;
   empty input is rejected. `scripts/requirements.txt` pins the PyYAML dependency.
2. `detect_transport()` distinguishes positive IB/Socket selections, GDR markers and
   failed attempts. WARN/ERROR lines do not become positive transport observations.
   Bootstrap sockets and empty IB device lists do not prove a data path.
3. `detect_single_node()` evaluates supported topology/local-channel markers. This is
   a bounded heuristic, not timestamp/rank provenance or a complete topology parser.
4. `resource_findings()` parses each recognized resource block independently. Limits
   may supply omitted requests; explicit requests must match. It never joins one
   container's request with another container's limit or validates an entire manifest.
5. `detect_ibstat()` reports recognized logical/physical port observations;
   `detect_busbw()` extracts a supported average-bandwidth line. No universal threshold,
   causal slowdown or dollar saving is derived.
6. `diagnose()` retains independent fields and proposes corroboration. `render()`
   presents the observations without executing its diagnostic checklist. The operator
   identifies the actual run, image, devices and lifecycle owner before any next action.

`rdma_engaged` is a compatibility field about transport applicability, not a health
certificate. `gpu_direct_rdma_confirmed` requires its own positive evidence. Mixed
transport lines require rank/run separation; absent evidence remains unknown. Full
identity, chronology and malformed-input coverage remain broader blueprint requirements.

## ADR-FABRIC-2: progressive disclosure

| Level | Interface | Included content |
| --- | --- | --- |
| L1 | Default | Verdict, transport, separate GDR observation, all resource gaps, port findings, observed bandwidth qualification and safety boundary |
| L2 | `--detailed` | L1 plus the complete proposed diagnostic checklist |
| L3 | `--full` | L2 plus the complete structured verdict; not the raw input |
| Machine | `--json` | Existing JSON-only result contract |

Output flags are mutually exclusive. The previous human checklist view is available
through `--detailed`; JSON consumers keep `--json`. Detail levels never suppress
contradictory evidence or authorize cluster changes, and do not fetch additional data.
Default reports always retain the warning against host-driver changes, resets and
managed health-cordon overrides. Bandwidth remains unverified against a baseline.

## ADR-FABRIC-3: integration and permission boundaries

The skill declares Read, Write, Edit, Glob, `Bash(kubectl get:*)` and
`Bash(python3:*)`, not bare Bash. Read/Glob select owner-provided evidence; Write/Edit
are for a reviewed local report or proposed correction, never automatic cluster apply.
The Python prefix is broader than one file, so invoke only the bundled helper with
reviewed arguments. Never run Python or shell text taken from diagnostic input.

A live query requires separately authorized explicit context, namespace and object.
Static tool declarations do not establish runtime permission enforcement; the host may
require approval for an option-prefixed command. Do not expand permissions to avoid
that check. No account credentials are required for local fixture analysis.

This skill does not mirror or execute CoreWeave OSS manifests. The retained research
record `000-docs/003-RL-RSRC-gpu-node-fabric.md` cites
[CoreWeave's NCCL examples at ab7a928](https://github.com/coreweave/nccl-tests/blob/ab7a928135c7aa04f151d993de3d36fffdd3d034/README.md)
as topology/benchmark context, not an imported implementation or an executable recipe.
The [RDMA guidance](https://docs.coreweave.com/products/networking/hpc-interconnect/use-gpudirect-rdma)
is a platform reference for the authorized operator to recheck. Neither link proves
compatibility with the supplied workload. No proprietary official skill is copied.

## Directory and handoff view

| Artifact | Responsibility |
| --- | --- |
| `SKILL.md` | Trigger, workflow, tool declarations and operator limits |
| `scripts/fabric-check.py` | Evidence detectors, result assembly, renderer, CLI and self-test |
| `scripts/requirements.txt` | Pinned parser dependency |
| `references/nccl-debug-reading.md` | Transport/GDR interpretation |
| `references/rdma-engagement-checklist.md` | Resource/device corroboration |
| `references/allreduce-baseline.md` | Equivalent-baseline comparison limits |
| `PRD.md`, `docs/BLUEPRINT.md`, `eval-spec.yaml` | Requirements, open acceptance and model criteria |

The incident-runbook skill can route a transport question here. GPU-node-forensics
handles Xid/device failures; the training workflow handles proposed workload configuration.
Pass sanitized observations with operator-supplied run identity and missing evidence.
No sibling receives inherited mutation authority or an assumed health verdict. The
helper does not invoke sibling skills or agents automatically.

## Failure taxonomy, alternatives and verification

| Condition | Implemented response / limitation |
| --- | --- |
| Invalid flags, empty input, missing interactive input | argparse error; no verdict |
| Unreadable/non-UTF-8 file | Python input error; no successful report |
| Resource block cannot be parsed | Evidence finding; inspect the actual admitted Pod |
| Warning-only or incomplete transport data | Unknown, not positive IB/GDR evidence |
| Mixed transport | Separate ranks/channels/runs before a causal conclusion |
| Down/inactive port | Port observation; not proof of every node fault's root cause |
| Bandwidth without equivalent baseline | Unverified observation; no performance or savings claim |

Rejected alternatives: direct cluster mutation, driver installation, keyword-only
healthy verdicts, combining container resources, fixed slowdown factors and dumping
raw logs for verbosity. The selected structure allows repeatable fixture review while
leaving real workload recovery with its owner.

**RISK-FABRIC-1:** partial or mixed-run evidence can be misattributed. The maintainer
owns new-format and regression review; the workload/platform owner owns real changes.
Residual exposure is not accepted as production certification. Runtime permissions,
model behavior, complete provenance and live NCCL validation remain unproved.

The operator regression suite runs the CLI across output levels, confirms safety and
negative evidence remain visible, rejects conflicting flags and checks JSON compatibility.
Run all tests, diagnostic self-tests and the pack gate from CONTRIBUTING; retain receipts
under `.cache/`. Eval-package checks validate the specification, not model judgments.
Reverting the output-mode commit restores the prior presentation; no persisted data or
infrastructure migration is involved. Broader release acceptance remains in the PRD and
blueprint, not inferred from this architecture document or a passing static grade.
