# Admissible Claim Register v1

Repo: `admissibility-interrogation-surface`  
Version: v0.1  
Date: 2026-05-07  
Authority: AlvianTech / Ricky Jones

---

## Admitted claims

1. On the demonstrated path, a structured five-question interrogation chain determines admissibility before a DecisionRecord may be formed.
2. FIRST_FAIL evaluation halts the chain at the earliest UNSATISFIED question.
3. No further questions are evaluated after a halt.
4. A pre-decision denial receipt is emitted on halt.
5. The receipt records which question failed, in what order, and confirms no DecisionRecord was created.
6. The receipt is integrity-bound by a SHA256 hash.
7. The verifier (`replay_verifier.py`) can confirm hash integrity and correct halt behaviour from the receipt alone.

---

## Explicitly not claimed

- That this surface replaces the commit gate (`commit-gate-core`). It is upstream of it.
- That a PASS result guarantees the resulting DecisionRecord will pass the commit gate.
- Path-universal coverage across all execution paths.
- Production readiness, certification, or standardisation.
- Equivalence to or derivation from any third-party governance system.

---

## Scope boundary

This repo is path-local. It demonstrates the interrogation mechanism on the paths implemented in `interrogate.py`. It does not assert that all paths in a real system route through this surface.
