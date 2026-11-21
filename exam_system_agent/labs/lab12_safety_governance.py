"""
Lab 12: Safety & Governance
Simple student version: 4 layers of safety guardrails for high-stakes exam actions.
Layers: Risk Assessment -> Approval Gate -> Evaluation -> Rollback Plan
"""

import sys
import os

class ExamSafetyAgent:
    def assess_risk(self, action):
        # Layer 1: Risk Assessment
        if action == "PUBLISH_RESULTS":
            return "HIGH RISK (Direct impact on student grades)"
        return "LOW RISK"

    def approval_gate(self, faculty_signed):
        # Layer 2: Approval Gate
        print("[Layer 2: Faculty Approval Gate]")
        if faculty_signed:
            print(" -> Approved: Digital faculty sign-off verified.")
            return True
        print(" -> BLOCKED: High-risk action requires faculty approval.")
        return False

    def evaluate_integrity(self, tab_switches):
        # Layer 3: Evaluation
        print("\n[Layer 3: Evaluation]")
        if tab_switches > 2:
            print(f" -> Flagged: Candidate had {tab_switches} tab-switches.")
            return False
        print(" -> Clean: No proctoring violations detected.")
        return True

    def rollback_plan(self):
        # Layer 4: Rollback Plan
        print("\n[Layer 4: Automated Rollback Plan]")
        print(" -> Snapshot restored: Grade publishing rolled back safely.")

if __name__ == "__main__":
    print("=" * 55)
    print("Lab 12: Safety & Governance Guardrails")
    print("=" * 55)

    safety = ExamSafetyAgent()

    # Step 1: Risk Assessment
    risk = safety.assess_risk("PUBLISH_RESULTS")
    print(f"\n[Layer 1: Risk Assessment]\n -> Action: PUBLISH_RESULTS | Level: {risk}")

    # Step 2: Approval Gate
    print("\nAttempt 1: Publishing without faculty sign-off...")
    allowed = safety.approval_gate(faculty_signed=False)

    print("\nAttempt 2: Publishing with faculty sign-off...")
    allowed = safety.approval_gate(faculty_signed=True)

    # Step 3: Evaluation
    safety.evaluate_integrity(tab_switches=0)

    # Step 4: Rollback simulation
    safety.rollback_plan()

    print("\n" + "=" * 55)
    print("Safety guardrails verified for examination operations!")
    print("=" * 55)
