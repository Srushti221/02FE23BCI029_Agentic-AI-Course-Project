"""
Lab 1: Autonomous Agent Workflow (Clarify -> Plan -> Act -> Revise)
Subject: Agentic AI (AGI301)
Student: Rahul Sharma (STU001) & Ananya Sharma (STU002)
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.eligibility_tool import check_eligibility

class ExamEligibilityAgent:
    def check_student(self, student_id, course_id):
        print(f"\n--- Checking Exam Request: {student_id} for {course_id} ---")
        
        # Step 1: Clarify
        print(f"[1. Clarify] Verifying candidate: {student_id} for External Exam ({course_id})")
        
        # Step 2: Plan
        print(f"[2. Plan] Querying attendance and Internal Marks (CIE) via check_eligibility tool...")
        res = check_eligibility(student_id, course_id)
        
        # Step 3: Act
        if res["eligible"]:
            print(f"[3. Act] Hall Ticket APPROVED for {res['student_name']}.")
            print(f" -> Attendance: {res['attendance']}% | Internal Marks: {res['internal_marks']}/50")
            print(f" -> Venue: Hall 101 | External Exam: Tomorrow 10:00 AM (Max: 50 Marks)")
            print(f"[4. Revise] No changes needed. Ready for external exam.")
        else:
            reasons = ", ".join(res["reasons"])
            print(f"[3. Act] Hall Ticket REJECTED for {res['student_name']}.")
            print(f" -> Reasons: {reasons}")
            # Step 4: Revise
            print(f"[4. Revise] Corrective Action: Attend makeup classes and submit improvement internals.")

if __name__ == "__main__":
    print("=" * 60)
    print("Lab 1: Autonomous Agent Workflow (Agentic AI)")
    print("=" * 60)

    agent = ExamEligibilityAgent()
    agent.check_student("STU001", "AGI301")  # Rahul Sharma (Eligible)
    agent.check_student("STU002", "AGI301")  # Ananya Sharma (Ineligible)
    print("=" * 60)
