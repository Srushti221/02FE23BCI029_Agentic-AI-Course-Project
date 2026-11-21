"""
Online Course Examination System Agent — Main Orchestrator
===========================================================
Lab 7  — Agentic Node Graph: This file wires all agents into a directed pipeline.
Lab 14 — Capstone Project Studio: Full team-owned agentic system running end-to-end.

Pipeline:
  Student Data → [Agent 1: Registration & Eligibility]
              → [Agent 2: Exam Delivery]
              → [Agent 3: Auto-Grading]
              → [Agent 4: Result Publishing]

Expected Outputs (per spec):
  ✅ Registration list    — from Agent 1
  ✅ Integrity report     — from Agent 4 (proctoring summary)
  ✅ Draft grades         — from Agent 3
  ✅ Published results    — from Agent 4
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from agents.registration_agent     import RegistrationEligibilityAgent
from agents.exam_delivery_agent    import ExamDeliveryAgent
from agents.grading_agent          import AutoGradingAgent
from agents.result_publishing_agent import ResultPublishingAgent


# ==========================================================================
# Helper: pretty section header
# ==========================================================================
def header(title: str, lab: str = ""):
    tag = f"  [{lab}]" if lab else ""
    print(f"\n{'='*62}")
    print(f"  {title}{tag}")
    print(f"{'='*62}")


# ==========================================================================
# STEP 0: Wire the multi-agent pipeline (Lab 7 — Agentic Node Graph)
# ==========================================================================
def build_pipeline():
    reg_agent      = RegistrationEligibilityAgent()
    delivery_agent = ExamDeliveryAgent(registration_agent=reg_agent)
    grading_agent  = AutoGradingAgent()
    publish_agent  = ResultPublishingAgent(grading_agent=grading_agent)
    return reg_agent, delivery_agent, grading_agent, publish_agent


# ==========================================================================
# Demo run (non-interactive — simulated answers for showcase)
# ==========================================================================
def run_demo():

    header("ONLINE COURSE EXAMINATION SYSTEM AGENT", "Lab 14 — Capstone")
    print("  KLE Tech | Project #7 | Python Multi-Agent Pipeline")

    reg_agent, delivery_agent, grading_agent, publish_agent = build_pipeline()

    course_id = "CS301"   # Data Structures exam

    # ----------------------------------------------------------------
    # PHASE 1: Registration & Eligibility Check (Agent 1)
    # Lab 1 concept: Agent decides, doesn't just chat
    # ----------------------------------------------------------------
    header("PHASE 1 — Registration & Eligibility", "Lab 1 + Lab 2")

    student_course_pairs = [
        ("STU001", course_id),  # Should PASS
        ("STU002", course_id),  # Low attendance — FAIL
        ("STU003", course_id),  # Should PASS
        ("STU004", course_id),  # Fees not paid + low attendance — FAIL
    ]

    reg_agent.bulk_process(student_course_pairs)

    print(f"\n  📋 Registration List Summary:")
    for entry in reg_agent.get_registration_list():
        icon = "✅" if entry["eligible"] else "❌"
        print(f"    {icon}  {entry['student_id']} — {entry['student_name']:20s} | {entry['status_summary']}")

    # ----------------------------------------------------------------
    # PHASE 2: Exam Delivery (Agent 2) — simulated answers
    # Lab 2: Tool-Using Agent calling question_fetcher_tool
    # ----------------------------------------------------------------
    header("PHASE 2 — Exam Delivery (Simulated)", "Lab 2 + Lab 5")

    # Simulated answers for eligible students
    # (In real use, delivery_agent.deliver_exam(..., interactive=True))
    student_submissions = [
        {
            "student_id": "STU001",
            "course_id":  course_id,
            "answers": {"Q1": "B", "Q2": "C", "Q3": "C", "Q4": "B", "Q5": "C"},  # 5/5 correct
        },
        {
            "student_id": "STU003",
            "course_id":  course_id,
            "answers": {"Q1": "B", "Q2": "A", "Q3": "C", "Q4": "B", "Q5": "A"},  # 3/5 correct
        },
    ]

    # Show questions fetched by Agent 2
    print(f"\n  [Exam Delivery Agent] Fetching questions for {course_id}...")
    result = delivery_agent.deliver_exam("STU001", course_id, interactive=False)
    print(f"  Questions fetched successfully: {result['success']}")
    print(f"  (In real mode, students answer interactively via terminal)")

    # ----------------------------------------------------------------
    # PHASE 3: Auto-Grading (Agent 3)
    # Lab 2: Tool-Using Agent calling grader_tool
    # ----------------------------------------------------------------
    header("PHASE 3 — Auto-Grading", "Lab 2 + Lab 8")

    for submission in student_submissions:
        grading_agent.grade(
            submission["student_id"],
            submission["course_id"],
            submission["answers"]
        )

    # ----------------------------------------------------------------
    # PHASE 4: Result Publishing (Agent 4)
    # Lab 12: Safety & Governance — faculty sign-off gate
    # ----------------------------------------------------------------
    header("PHASE 4 — Result Publishing", "Lab 7 + Lab 12")

    # Simulated proctoring integrity flags
    integrity_flags = {
        "STU001": "Clear",
        "STU003": "Tab-switch detected (1 event)",
    }

    report = publish_agent.publish_results(
        course_id       = course_id,
        faculty_approval= True,          # Change to False to see HOLD behaviour
        integrity_flags = integrity_flags,
    )

    # ----------------------------------------------------------------
    # PHASE 5: Integrity Report (from Result Publishing Agent)
    # ----------------------------------------------------------------
    header("PHASE 5 — Integrity Report", "Lab 12")
    ir = report.get("integrity_report", {})
    print(f"  Total flagged : {ir.get('total_flagged', 0)}")
    print(f"  Clear students: {ir.get('clear_students', 0)}")
    print(f"  Recommendation: {ir.get('recommendation', '')}")
    if ir.get("flagged_cases"):
        print("  Flagged cases:")
        for sid, reason in ir["flagged_cases"].items():
            print(f"    • {sid}: {reason}")

    # ----------------------------------------------------------------
    # Summary
    # ----------------------------------------------------------------
    header("PIPELINE COMPLETE — Summary")
    approved = reg_agent.get_approved_students()
    print(f"  Eligible students   : {len(approved)}/{len(student_course_pairs)}")
    print(f"  Exams delivered     : {len(student_submissions)}")
    print(f"  Draft grades created: {len(student_submissions)}")
    print(f"  Results published   : {report.get('total_students', 0)}")
    print(f"  Integrity flags     : {ir.get('total_flagged', 0)} case(s)")
    print(f"\n  ✅ All 4 agents ran successfully across the pipeline!\n")


# ==========================================================================
# Entry point
# ==========================================================================
if __name__ == "__main__":
    run_demo()
