# Admissibility Interrogation Surface

New to this work? Start here:
[https://github.com/LalaSkye/start-here](https://github.com/LalaSkye/start-here)

**Pre-decision interrogation surface for execution-boundary governance.**

Most boundary proofs show the gate.

This repo shows what runs *before* the gate — the structured interrogation that determines whether a `DecisionRecord` may be formed at all.

> **No question left UNSATISFIED → a DecisionRecord *may* be formed.**  
> **First UNSATISFIED → chain halts. No DecisionRecord is created. No commit surface exists.**

The proof is the pre-decision denial receipt.

Claim discipline for this repo is controlled in [`docs/governance/ADMISSIBLE_CLAIM_REGISTER_v1.md`](docs/governance/ADMISSIBLE_CLAIM_REGISTER_v1.md).

Run the verifier locally: `python replay_verifier.py`

---

## 1. Definition

Admissibility interrogation is the structured pre-decision check that runs before an action is allowed to enter the DecisionRecord formation stage.

Each question in the interrogation chain must return `SATISFIED`.

If any question returns `UNSATISFIED`, the chain halts at that point using FIRST_FAIL evaluation. No further questions are evaluated. No DecisionRecord is created.

This is earlier than the commit gate. The commit gate checks a DecisionRecord. This surface determines whether a DecisionRecord can exist.

---

## 2. The interrogation questions

This repo implements five interrogation questions scoped to the path-local AlvianTech execution-boundary model:

| # | Question | Fail condition |
|---|---|---|
| 1 | Is authority present and valid? | No authority, expired authority, or unrecognised authority token |
| 2 | Is scope defined and bounded? | Scope absent, unbounded, or wider than the requesting agent's mandate |
| 3 | Is evidence admissible? | No evidence record, tampered record, or evidence referencing a different action |
| 4 | Is state lineage intact? | State relied upon is unverifiable, stale, or derived from a non-admissible prior |
| 5 | Is the proposed outcome lawful at commit? | Outcome would violate a preserved invariant on the current path |

First `UNSATISFIED` halts. The receipt records which question failed and why.

---

## Try it in 30 seconds

```bash
git clone https://github.com/LalaSkye/admissibility-interrogation-surface.git
cd admissibility-interrogation-surface
python interrogate.py
```

Expected output (all satisfied):

```text
[Q1] authority_present       → SATISFIED
[Q2] scope_bounded           → SATISFIED
[Q3] evidence_admissible     → SATISFIED
[Q4] state_lineage_intact    → SATISFIED
[Q5] outcome_lawful_at_commit → SATISFIED
RESULT: PASS — DecisionRecord formation is permitted
Receipt: receipts/sample_pass.json
```

Expected output (failure at Q2):

```bash
python interrogate.py --scenario fail_scope
```

```text
[Q1] authority_present → SATISFIED
[Q2] scope_bounded     → UNSATISFIED — scope absent
HALT: chain stopped at question 2. No further evaluation.
RESULT: PRE_DECISION_DENIAL
Receipt: receipts/sample_deny.json
```

If evaluation continues past an `UNSATISFIED` answer, the interrogation surface is broken.

---

## What this repo proves

- A structured interrogation chain can determine admissibility before a DecisionRecord is formed.
- FIRST_FAIL evaluation stops the chain at the earliest failure point.
- A pre-decision denial receipt is emitted when the chain halts.
- No DecisionRecord is created on halt — there is no commit surface to reach.

---

## What this repo does not prove

- That a DecisionRecord, once formed, is valid at the commit gate — see [`commit-gate-core`](https://github.com/LalaSkye/commit-gate-core).
- That the full refusal receipt chain is intact — see [`refusal-receipt-chain`](https://github.com/LalaSkye/refusal-receipt-chain).
- Path-universal coverage across all reachable execution paths.
- Production readiness, certification, or standardisation.

---

## Boundary

This repo proves one narrow claim:

> On the demonstrated path, a structured pre-decision interrogation halts before a DecisionRecord is formed when any admissibility question is UNSATISFIED.

Small surface. Clear failure mode. Receipts over reassurance.

---

## Relation to other repos

```
admissibility-interrogation-surface   ← this repo (pre-decision layer)
        ↓
  commit-gate-core                    (decision record validation at commit)
        ↓
  refusal-receipt-chain               (receipt chain after refusal)
```

---

## Status

`v0.1` — five questions, FIRST_FAIL evaluation, pre-decision denial receipt.

Small surface. Clear failure mode. Receipts over reassurance.

---

## License

MIT. Use it. Break it. Tell me how.
