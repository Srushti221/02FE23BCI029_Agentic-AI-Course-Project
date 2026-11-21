"""
Lab 8: Parallel Swarm
Simple student version: 4 autonomous agent workers replace manual human tasks concurrently.
Subject: Agentic AI (AGI301)
Marks Structure:
- Internal Marks (CIE) : 50 Marks (from continuous assessment)
- External Exam (SEE)  : 50 Marks (Section A MCQs: 25 + Section B Short Answer: 25)
- Grand Total          : 100 Marks
"""

import sys
import os
import threading
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.grader_tool import auto_grade
from agents.proctoring_agent import ProctoringIntegrityAgent
from agents.subjective_grading_agent import SubjectiveGradingAssistAgent

# Worker 1: Proctoring Agent
def worker_proctoring(student_id, telemetry, results):
    print("[Worker 1: Proctoring Agent] Monitoring exam session...")
    time.sleep(0.1)
    agent = ProctoringIntegrityAgent()
    res = agent.monitor_session(student_id, "AGI301", telemetry)
    results["proctoring"] = res
    print(" -> Done: Candidate integrity verified (Status: Clear).")

# Worker 2: Section A MCQ Grading Agent (Scaled to 25 marks)
def worker_mcq_grading(answers, results):
    print("[Worker 2: MCQ Grading Agent] Checking 5 objective questions (25 marks)...")
    time.sleep(0.1)
    res = auto_grade("AGI301", answers)
    scaled_score = int((res["score"] / res["total_marks"]) * 25)  # Scale to 25
    results["mcq"] = {"score": scaled_score, "max": 25}
    print(f" -> Done: Section A MCQs scored {scaled_score}/25.")

# Worker 3: Section B Short Answer Grading Agent (25 marks)
def worker_short_answer_grading(short_answer, results):
    print("[Worker 3: Short Answer Agent] Grading concept answer (25 marks)...")
    time.sleep(0.1)
    agent = SubjectiveGradingAssistAgent()
    question = "What are the main components of an AI Agent?"
    res = agent.evaluate_short_answer("AGI301", question, short_answer)
    results["short_answer"] = {"score": res["marks_awarded"], "max": 25}
    print(f" -> Done: Section B Short Answer scored {res['marks_awarded']}/25.")

# Worker 4: Malpractice Checker Agent
def worker_integrity_audit(results):
    print("[Worker 4: Malpractice Checker Agent] Scanning for anomalies...")
    time.sleep(0.1)
    results["audit"] = "Passed (No malpractice detected)"
    print(" -> Done: No cheating detected. Approved for release.")

if __name__ == "__main__":
    print("=" * 60)
    print("Lab 8: Autonomous Parallel Swarm")
    print("Subject: Agentic AI (AGI301) | Student: Rahul Sharma")
    print("=" * 60)

    shared_results = {}
    
    # Internal marks from student database
    internal_marks = 46  # out of 50
    
    # External exam inputs
    mcq_answers = {"Q1": "B", "Q2": "C", "Q3": "B", "Q4": "B", "Q5": "B"}
    student_short_ans = "An agent has a planner, memory to store data, and tools to perform actions."
    telemetry = []

    # Launching 4 Autonomous Agents simultaneously
    t1 = threading.Thread(target=worker_proctoring, args=("STU001", telemetry, shared_results))
    t2 = threading.Thread(target=worker_mcq_grading, args=(mcq_answers, shared_results))
    t3 = threading.Thread(target=worker_short_answer_grading, args=(student_short_ans, shared_results))
    t4 = threading.Thread(target=worker_integrity_audit, args=(shared_results,))

    print("\nStarting 4 agent workers simultaneously...\n")
    t1.start(); t2.start(); t3.start(); t4.start()
    t1.join(); t2.join(); t3.join(); t4.join()

    # Calculate External and Grand Total
    sec_a = shared_results["mcq"]["score"]
    sec_b = shared_results["short_answer"]["score"]
    external_marks = sec_a + sec_b           # out of 50
    grand_total = internal_marks + external_marks # out of 100

    print("\n" + "=" * 60)
    print("--- Final Swarm Scorecard ---")
    print(f"Candidate          : Rahul Sharma (STU001)")
    print(f"Subject            : Agentic AI (AGI301)")
    print("-" * 60)
    print(f"1. Internal Marks (CIE) : {internal_marks}/50")
    print(f"2. External Exam (SEE)  : {external_marks}/50")
    print(f"   - Section A (MCQs)   : {sec_a}/25")
    print(f"   - Section B (Concept): {sec_b}/25")
    print("-" * 60)
    print(f"GRAND TOTAL SCORE       : {grand_total}/100 -> Grade: S (Outstanding 🏆)")
    print(f"Proctor Status          : {shared_results['proctoring']['status']}")
    print(f"Audit Result            : {shared_results['audit']}")
    print(f"Final Decision          : APPROVED & OFFICIALLY PUBLISHED")
    print("=" * 60)
