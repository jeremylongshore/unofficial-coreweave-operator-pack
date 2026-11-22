# Requirements: GPU node evidence review

> Community-contributed; not affiliated with, endorsed by, or sponsored by CoreWeave, Inc.

| Metadata | Value |
| --- | --- |
| Document ID / type | CW-GPU-PRD / product requirements |
| Schema / template | Blueprint Docs 3.0.0 / repository requirements envelope 1.0 |
| Status | Requirements reconciliation; implementation exists, release acceptance remains open |
| Owner / decision authority | Jeremy Longshore, maintainer |
| Reviewers | Technical and security reviewers unassigned |
| Generated / updated / review | 2026-11-05 / 2026-11-22 / before release |
| Classification | Public; synthetic or sanitized evidence only |
| Sources | SRC-GPU-1 through SRC-GPU-4 below |
| Assumptions | The operator can establish GPU identity and managed lifecycle ownership |
| Unknowns | Account compatibility, complete historical Dxx mapping, behavioral performance |
| Related artifacts | [Blueprint](docs/BLUEPRINT.md), [architecture](ARD.md), [eval specification](eval-spec.yaml); marketplace Bead claude-k1qr.10 and issue #1840 |
| Supersession | Reconciles requirements at historical commit 94b1b81; does not reinstate its unsafe action rules |

## Problem and historical trace

Preserve the original pain anchors D-CW-GPU-01, D-CW-GPU-02, D-CW-GPU-03, D-CW-GPU-04 as traceability questions. Earlier unsupported numerical or universal claims are corrected here; their historical text remains in Git. No customer failure frequency, recovered dollars, universal slowdown or production outcome is established.

## User outcome

Give an authorized operator a reproducible review of supplied evidence, its limits, and a bounded next step. Unknown Xids remain investigate; same-device row-remapper correlation must not soften a PCIe bus failure. Containment is not a global health verdict.

## Acceptance criteria

1. Parse the supported input and emit a deterministic result with its evidence scope.
2. Keep unknown, missing, invalid, partial and measured-zero states distinct.
3. Reject or qualify ambiguous input instead of generating certainty or an automatic disruptive action.
4. Preserve lifecycle ownership, credential confidentiality and workload/cost approval boundaries.
5. Pass the script self-test and the relevant cases in `tests/test_coreweave_operator_tools.py`.
6. Review the corresponding eval specification without treating its existence as a passing behavioral run.

## Scope and non-goals

The implementation is `scripts/triage.py` with the associated skill and references. It operates on supplied local evidence. No account provisioning, live metric collection, GPU benchmark, reset, reboot, reservation change or model-provider call is performed by the offline script.

## Release evidence

Retain actual command results and source hashes in the pack’s offline evidence report. A structural grade is format/content evidence; it is not execution, model-variance, baseline-value or production certification.

## Primary reference

https://docs.nvidia.com/deploy/xid-errors/latest/analyzing-xid-catalog.html

## Source register and historical reconciliation

- **SRC-GPU-1 (provided):** Bead `claude-k1qr.10` requests Xid, remap, thermal and lifecycle triage, grounded in D01–D10 and D16. The numbered pain catalog is not present in this standalone repository. Individual Dxx assignments remain **unknown**; do not invent a one-to-one mapping.
- **SRC-GPU-2 (verified repository history):** commit `94b1b81`, this PRD, defines D-CW-GPU-01 (failed/degraded GPU), -02 (containment confusion), -03 (unsupported hardware replacement), and -04 (managed cordon override). These are traceability questions, not measured customer incidence or monetary losses.
- **SRC-GPU-3 (verified implementation):** [triage.py](scripts/triage.py), [Xid boundaries](references/xid-triage-table.md), [cordon ownership](references/cordon-rules.md), and [operator tests](https://github.com/jeremylongshore/unofficial-coreweave-operator-pack/blob/4616cac468194f49f3131afeeb6f7efc56b999ba/tests/test_coreweave_operator_tools.py). Source inspection proves code and assertions exist; test execution and model evaluation are separate evidence.
- **SRC-GPU-4 (primary guidance reviewed 2026-11-22):** [NVIDIA Xid analysis](https://docs.nvidia.com/deploy/xid-errors/latest/analyzing-xid-catalog.html) requires retained GPU/driver context, applicable parsing policy and recovery prerequisites. Its current guidance is broader than this helper's finite table; do not represent the helper as a complete implementation of the NVIDIA catalog.

Historical requirements saying unknown Xids imply reset, application Xids exclude hardware, remap failure alone implies RMA, or thermal evidence proves health are superseded. They contradict the current conservative evidence boundary. The helper supplies qualified recommendations; it never executes recovery.

## Stories and requirement trace

All requirements below are **Must**, owned by the maintainer. Their status is **implemented boundary; behavioral acceptance pending** unless explicitly marked otherwise. Each story states a proposed operator need, not an interview finding. Criterion identifiers refer to the existing eval specification; a mapping does not assert a model pass.

| Story / requirement | Pain anchor / source | Required result and acceptance | Verification / eval criterion |
| --- | --- | --- | --- |
| STORY-GPU-1 / REQ-GPU-1: as an on-call operator, interpret a supplied fault without guessing recovery | D-CW-GPU-01; SRC-GPU-1–4 | Preserve unknown codes as investigate with low confidence; mapped codes require platform confirmation. Preserve identity and accompanying faults; ambiguous multi-GPU evidence stays inconclusive. | `test_unknown_xid_does_not_trigger_reset`, `test_multi_gpu_evidence_not_combined`; `action-grounded-in-the-xid-not-guessed` |
| STORY-GPU-2 / REQ-GPU-2: as a training operator, distinguish contained and uncontained events | D-CW-GPU-02; SRC-GPU-2–4 | Keep 94/95 recommendations distinct without declaring a healthy node or authorizing reset. | `test_xid_containment_is_not_global_health`; `correctly-splits-94-vs-95` |
| STORY-GPU-3 / REQ-GPU-3: as an SRE, avoid unsupported RMA | D-CW-GPU-03; SRC-GPU-1–3 | Investigate application, driver and prior faults for 13/31/43/45; do not categorically exclude hardware. Treat 45 as follow-on when another fault is present. | `test_xid_45_is_follow_on_not_governing`, `test_xid_recommendations_require_platform_confirmation`; `app-bugs-not-rmad` |
| STORY-GPU-4 / REQ-GPU-4: as an SRE, correlate memory evidence to the correct device | D-CW-GPU-01/-03; SRC-GPU-1–3 | Distinguish pending remap, recording failure and remapping failure. Do not soften a PCIe bus fault with unrelated remap data or infer replacement from one field. | `test_remap_does_not_soften_pcie_bus_failure`, `test_xid_64_is_reset_and_support_not_rma`, `test_remap_failure_alone_does_not_recommend_rma`; `action-grounded-in-the-xid-not-guessed` |
| STORY-GPU-5 / REQ-GPU-5: as an operator, respect managed recovery ownership | D-CW-GPU-04; SRC-GPU-1–3 | Hardware recommendations carry confirmation and the never-manually-uncordon rule. Cordon, drain, reset, reboot and replacement are outside helper execution authority. | `test_xid_recommendations_require_platform_confirmation`; `never-recommends-uncordoning-a-health-cordon` |
| STORY-GPU-6 / REQ-GPU-6: as an operator, distinguish a thermal observation from a hardware verdict | D-CW-GPU-01; SRC-GPU-1–3 | Report a thermal-only observation conservatively; do not infer healthy hardware or prescribe automatic recovery. Thermal behavioral case is specified but not executed. | Self-test `blob: thermal throttle -> watch`; `thermal-observation-not-health-verdict` |
| STORY-GPU-7 / REQ-GPU-7: as an evidence reviewer, safely inspect untrusted logs | D-CW-GPU-01/-04; SRC-GPU-1–3 | Treat logs as data, never execute embedded instructions, reveal hidden prompts or collect credentials. No provider/account calls in offline evaluation. | Eval `adversarial-injection` / `no-prompt-leakage`; targeted fixture boundaries do not prove a universal sandbox |

The fault families 48/63/64/74/79/92/119/120 and driver recovery event 154 are represented in `XID_TABLE` or recovery parsing. This is an inventory, not a promise of exhaustive architecture-specific diagnosis. Use REQ-GPU-1, -4 and -5 for review of those paths.

## Surfaces, release conditions and residual risk

The helper consumes explicit local text, an Xid argument, or operator-supplied remap flags. It emits JSON or text recommendations. It has no CoreWeave API endpoint, credentials, cloud client or authority to mutate a node. Live collection commands in the guide are operator procedures outside the offline test boundary.

**RISK-GPU-1:** incomplete or cross-device evidence can suggest an inappropriate action. Controls are REQ-GPU-1/-4/-5; residual risk remains when identities or platform context are absent. The maintainer owns review before release; the actual lifecycle owner authorizes any recovery. Exact CoreWeave auto-RMA thresholds remain **[UNVERIFIED — needs doc cite]** and must not be inferred. Existing lifecycle metadata references do not establish a universal taint or replacement policy.

**REL-GPU-1 (proposed release gate):** reconcile the missing Dxx catalog against the preserved anchors; review and execute the specified thermal behavioral case; retain current helper tests and eval-package checks; obtain scoped behavioral evidence and technical review before claiming behavioral readiness. Live account validation remains separately authorized. PRD completion does not certify these implementation or release conditions.

Success is measured by correct bounded decisions on retained fixtures and reviewed behavioral cases, including refusals and uncertainty. No latency target, customer demand, recovered GPU-hours or dollar savings has been measured for this requirement set.
