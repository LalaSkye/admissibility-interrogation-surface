"""Replay verifier for pre-decision denial receipts.

Loads a receipt JSON file and verifies:
1. The SHA256 hash matches the receipt content.
2. decision_record_created is False when result is PRE_DECISION_DENIAL.
3. Evaluations stopped at the reported halt question.
4. No evaluation entry exists beyond the halt point.
"""

import argparse
import glob
import hashlib
import json
import sys


def verify_receipt(path: str) -> bool:
    with open(path) as f:
        receipt = json.load(f)

    stored_hash = receipt.pop("sha256", None)
    receipt_str = json.dumps(receipt, sort_keys=True)
    computed_hash = hashlib.sha256(receipt_str.encode()).hexdigest()
    receipt["sha256"] = stored_hash  # restore

    print(f"\nVerifying: {path}")

    # Check 1: hash integrity
    if stored_hash != computed_hash:
        print(f"  [FAIL] Hash mismatch. Stored: {stored_hash} | Computed: {computed_hash}")
        return False
    print("  [PASS] Hash integrity verified.")

    result = receipt.get("result")
    halt_at = receipt.get("halt_at_question")
    evaluations = receipt.get("evaluations", [])
    decision_record_created = receipt.get("decision_record_created")

    # Check 2: no DecisionRecord on denial
    if result == "PRE_DECISION_DENIAL":
        if decision_record_created is not False:
            print("  [FAIL] PRE_DECISION_DENIAL but decision_record_created is not False.")
            return False
        print("  [PASS] No DecisionRecord created on denial.")

    # Check 3: evaluations stopped at halt point
    if halt_at is not None:
        if len(evaluations) != halt_at:
            print(f"  [FAIL] Expected {halt_at} evaluations, found {len(evaluations)}.")
            return False
        print(f"  [PASS] Chain halted at question {halt_at}. No over-evaluation.")

        # Check 4: the halt question is UNSATISFIED
        halt_entry = evaluations[halt_at - 1]
        if halt_entry["status"] != "UNSATISFIED":
            print(f"  [FAIL] Halt question status is {halt_entry['status']}, expected UNSATISFIED.")
            return False
        print(f"  [PASS] Halt question ({halt_entry['question']}) correctly UNSATISFIED.")

    print(f"  VERDICT: receipt is valid.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify pre-decision denial receipts.")
    parser.add_argument(
        "receipts",
        nargs="*",
        help="Receipt JSON files to verify. If omitted, verifies all receipts/ directory.",
    )
    args = parser.parse_args()

    paths = args.receipts or sorted(glob.glob("receipts/*.json"))

    if not paths:
        print("No receipts found to verify.")
        sys.exit(0)

    results = [verify_receipt(p) for p in paths]
    total = len(results)
    passed = sum(results)
    print(f"\n{passed}/{total} receipts verified successfully.")
    sys.exit(0 if passed == total else 1)
