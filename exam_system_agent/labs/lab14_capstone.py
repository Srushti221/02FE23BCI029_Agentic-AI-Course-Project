"""
Lab 14: Capstone Project Studio
Simple student version: End-to-end Online Exam System with 7 AI Agents & 4 Expected Outputs.
Subject: Agentic AI (AGI301)
Grading Structure:
- Internal Marks (CIE) : 50 Marks
- External Exam (SEE)  : 50 Marks (Section A: 25 + Section B: 25)
- Total Marks          : 100 Marks
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.eligibility_tool import check_eligibility
from tools.question_fetcher_tool import fetch_exam_questions
from tools.grader_tool import auto_grade
from tools.dashboard_report_tool import generate_dashboard_view
from agents.proctoring_agent import ProctoringIntegrityAgent
from agents.subjective_grading_agent import SubjectiveGradingAssistAgent
from agents.grievance_revaluation_agent import GrievanceRevaluationAgent

def run_capstone():
    print("=" * 60)
    print("Lab 14: Online Course Examination System Agent (Capstone)")
    print("Subject: Agentic AI (AGI301)")
    print("=" * 60)

    # -------------------------------------------------------------
    # AGENT 1: Registration & Eligibility Agent -> OUTPUT 1
    # -------------------------------------------------------------
    print("\n[Agent 1: Registration & Eligibility]")
    students = ["STU001", "STU002", "STU003"]
    registration_list = []
    for sid in students:
        res = check_eligibility(sid, "AGI301")
        registration_list.append(res)
    
    print("\n>>> OUTPUT 1: REGISTRATION LIST")
    for s in registration_list:
        status_text = "APPROVED" if s["eligible"] else "REJECTED (Low attendance/internals)"
        print(f" - {s['student_name']:<15} ({s['student_id']}) : {status_text} | Internal: {s.get('internal_marks', 0)}/50")

    # -------------------------------------------------------------
    # AGENT 2: Exam Delivery Agent
    # -------------------------------------------------------------
    print("\n[Agent 2: Exam Delivery]")
    paper = fetch_exam_questions("AGI301")
    print(f" -> Delivered External Exam: {paper['course_name']} (Section A: 25M + Section B: 25M = 50 Marks)")

    # -------------------------------------------------------------
    # AGENT 3: Proctoring & Integrity Agent -> OUTPUT 2
    # -------------------------------------------------------------
    print("\n[Agent 3: Proctoring & Integrity]")
    proctor = ProctoringIntegrityAgent()
    rep1 = proctor.monitor_session("STU001", "AGI301", [])
    rep3 = proctor.monitor_session("STU003", "AGI301", [{"type": "tab_switch", "duration_sec": 3}])
    
    print("\n>>> OUTPUT 2: INTEGRITY REPORT")
    print(f" - Rahul Sharma (STU001) : Status = {rep1['status']} (Clean session)")
    print(f" - Arjun Nair   (STU003) : Status = {rep3['status']} (1 Tab-switch detected)")

    # -------------------------------------------------------------
    # AGENT 4 & 5: Auto-Grading & Subjective Assist Agents -> OUTPUT 3
    # -------------------------------------------------------------
    print("\n[Agent 4: Auto-Grading & Agent 5: Subjective Grading Assist]")
    # Candidate Rahul Sharma (STU001)
    mcq_res = auto_grade("AGI301", {"Q1": "B", "Q2": "C", "Q3": "B", "Q4": "B", "Q5": "B"})
    sec_a_marks = int((mcq_res["score"] / mcq_res["total_marks"]) * 25) # 25 marks
    
    subj_agent = SubjectiveGradingAssistAgent()
    short_q = "What are the main components of an AI Agent?"
    short_ans = "An agent has a planner, memory to store data, and tools to perform actions."
    short_res = subj_agent.evaluate_short_answer("AGI301", short_q, short_ans) # 25 marks
    sec_b_marks = short_res["marks_awarded"]

    external_total = sec_a_marks + sec_b_marks # 50 marks
    internal_marks = 46                         # 50 marks
    final_total = internal_marks + external_total # 100 marks

    print("\n>>> OUTPUT 3: DRAFT GRADES (Rahul Sharma)")
    print(f" - Internal Marks (CIE) : {internal_marks}/50")
    print(f" - External Exam (SEE)  : {external_total}/50 (Section A: {sec_a_marks}/25, Section B: {sec_b_marks}/25)")
    print(f" - Grand Draft Total    : {final_total}/100")

    # -------------------------------------------------------------
    # AGENT 6: Result Publishing Agent -> OUTPUT 4
    # -------------------------------------------------------------
    print("\n[Agent 6: Result Publishing]")
    dashboard = generate_dashboard_view("Rahul Sharma", "STU001", "Agentic AI (AGI301)", 
                                        internal_marks, external_total, rep1["status"])
    print("\n>>> OUTPUT 4: PUBLISHED RESULTS (Faculty Signed)")
    print(dashboard["card_text"])

    # -------------------------------------------------------------
    # AGENT 7: Grievance & Revaluation Agent
    # -------------------------------------------------------------
    print("\n[Agent 7: Grievance & Revaluation]")
    grievance_agent = GrievanceRevaluationAgent()
    claim = grievance_agent.file_grievance("STU003", "AGI301", "SecB", "Request re-total of Section B answer", current_marks=78)
    print(f" - Grievance ID   : {claim['grievance_id']}")
    print(f" - Student Claim  : {claim['claim']}")
    print(f" - Decision       : {claim['decision']} ({claim['rationale']})")
    print(f" - Updated Score  : {claim['original_marks']}/100 -> {claim['revised_marks']}/100")

    print("\n" + "=" * 60)
    print("All 7 Agents Executed Successfully!")
    print("=" * 60)

if __name__ == "__main__":
    run_capstone()
