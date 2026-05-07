"""Admissibility interrogation chain.

Runs five structured questions before a DecisionRecord may be formed.
First UNSATISFIED answer halts the chain (FIRST_FAIL evaluation).
Emits a pre-decision receipt regardless of outcome.
"""

import argparse
import hashlib
import json
import os
import uuid
from datetime import datetime, timezone

QUESTIONS = [
    "authority_present",
    "scope_bounded",
    "evidence_admissible",
    "state_lineage_intact",
    "outcome_lawful_at_commit",
]

# Scenarios: each entry is a dict mapping question key → bool (True = SATISFIED)
SCENARIOS = {
    "all_pass": {
        "authority_present": True,
        "scope_bounded": True,
        "evidence_admissible": True,
        "state_lineage_intact": True,
        "outcome_lawful_at_commit": True,
    },
    "fail_scope": {
        "authority_present": True,
        "scope_bounded": False,  # ← fails here
        "evidence_admissible": True,
        "state_lineage_intact": True,
        "outcome_lawful_at_commit": True,
    },
    "fail_authority": {
        "authority_present": False,  # ← fails here
        "scope_bounded": True,
        "evidence_admissible": True,
        "state_lineage_intact": True,
        "outcome_lawful_at_commit": True,
    },
    "fail_evidence": {
        "authority_present": True,
        "scope_bounded": True,
        "evidence_admissible": False,  # ← fails here
        "state_lineage_intact": True,
        "outcome_lawful_at_commit": True,
    },
    "fail_lineage": {
        "authority_present": True,
        "scope_bounded": True,
        "evidence_admissible": True,
        "state_lineage_intact": False,  # ← fails here
        "outcome_lawful_at_commit": True,
    },
    "fail_lawful": {
        "authority_present": True,
        "scope_bounded": True,
        "evidence_admissible": True,
        "state_lineage_intact": True,
        "outcome_lawful_at_commit": False,  # ← fails here
    },
}


def run_interrogation(scenario_name: str) -> dict:
    scenario = SCENARIOS[scenario_name]
    run_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()
    evaluations = []
    halt_at = None
    decision_record_permitted = False

    for i, question in enumerate(QUESTIONS, start=1):
        answer = scenario[question]
        status = "SATISFIED" if answer else "UNSATISFIED"
        evaluations.append({"question_number": i, "question": question, "status": status})
        print(f"[Q{i}] {question:<30} → {status}")

        if not answer:
            halt_at = i
            print(f"HALT: chain stopped at question {i}. No further evaluation.")
            break
    else:
        decision_record_permitted = True

    result = "PASS" if decision_record_permitted else "PRE_DECISION_DENIAL"
    print(f"\nRESULT: {result}")
    if decision_record_permitted:
        print("DecisionRecord formation is permitted on this path.")
    else:
        print("No DecisionRecord created. No commit surface exists.")

    receipt = {
        "schema": "pre-decision-denial-receipt-v1",
        "run_id": run_id,
        "scenario": scenario_name,
        "timestamp": timestamp,
        "result": result,
        "decision_record_created": False,
        "halt_at_question": halt_at,
        "evaluations": evaluations,
    }

    receipt_str = json.dumps(receipt, sort_keys=True)
    receipt["sha256"] = hashlib.sha256(receipt_str.encode()).hexdigest()

    os.makedirs("receipts", exist_ok=True)
    receipt_path = f"receipts/{scenario_name}_{run_id[:8]}.json"
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2)

    print(f"Receipt: {receipt_path}")
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run admissibility interrogation chain.")
    parser.add_argument(
        "--scenario",
        choices=list(SCENARIOS.keys()),
        default="all_pass",
        help="Scenario to run (default: all_pass)",
    )
    args = parser.parse_args()
    run_interrogation(args.scenario)
