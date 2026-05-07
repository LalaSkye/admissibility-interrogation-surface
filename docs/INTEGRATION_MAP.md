# Integration Map

This repo sits at the **pre-decision layer** of the AlvianTech execution-boundary stack.

```
┌─────────────────────────────────────────────────┐
│   admissibility-interrogation-surface           │  ← this repo
│   Five questions. FIRST_FAIL. Pre-decision      │
│   denial receipt if any question UNSATISFIED.   │
└────────────────────┬────────────────────────────┘
                     │ PASS → DecisionRecord may be formed
                     ▼
┌─────────────────────────────────────────────────┐
│   commit-gate-core                              │
│   Validates DecisionRecord at commit boundary.  │
│   github.com/LalaSkye/commit-gate-core          │
└────────────────────┬────────────────────────────┘
                     │ HOLD → refusal emitted
                     ▼
┌─────────────────────────────────────────────────┐
│   refusal-receipt-chain                         │
│   Receipt chain after boundary refusal.         │
│   github.com/LalaSkye/refusal-receipt-chain     │
└─────────────────────────────────────────────────┘
```

## What each layer proves

| Layer | Repo | Claim |
|---|---|---|
| Pre-decision | admissibility-interrogation-surface | No DecisionRecord forms if any admissibility question is UNSATISFIED |
| Commit gate | commit-gate-core | No state mutation without a valid DecisionRecord |
| Refusal receipt | refusal-receipt-chain | Refusal events are receipt-bound and replayable |

## What the stack does not prove

- Path-universal coverage (all three are path-local).
- That the layers are deployed in sequence in any production system.
