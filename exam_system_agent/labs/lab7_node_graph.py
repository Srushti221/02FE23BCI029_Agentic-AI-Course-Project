"""
Lab 7: Agentic Node Graph
Simple student version: A step-by-step pipeline connecting 4 functions.
Step 1: Check Eligibility -> Step 2: Fetch Exam -> Step 3: Grade Answers -> Step 4: Show Result Card
Subjects: Machine Learning (ML303)
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.eligibility_tool import check_eligibility
from tools.question_fetcher_tool import fetch_exam_questions
from tools.grader_tool import auto_grade

# Node 1: Eligibility Check (Attendance + Minimum Internal Marks)
def node1_check_eligibility(student_id, course_id):
    print(f"\n[Node 1: Eligibility Check]")
    result = check_eligibility(student_id, course_id)
    if not result["eligible"]:
        print(f"Failed: {student_id} is not eligible for {course_id}")
        return False, result
    print(f"Passed: {result['student_name']} is eligible (Internals: {result['internal_marks']}/50)")
    return True, result

# Node 2: Fetch External Exam Paper
def node2_fetch_exam(course_id):
    print(f"\n[Node 2: Exam Delivery]")
    paper = fetch_exam_questions(course_id)
    print(f"Fetched External Exam paper: {paper['course_name']} (Max: 50 Marks)")
    return paper

# Node 3: Grade External Exam (Scaled to 50 Marks)
def node3_grade_exam(course_id, answers):
    print(f"\n[Node 3: Auto-Grading]")
    grade_data = auto_grade(course_id, answers)
    # Scale objective evaluation to 50 marks
    scaled_external = int((grade_data["score"] / grade_data["total_marks"]) * 50)
    print(f"External Exam Scored: {scaled_external}/50")
    return scaled_external

# Node 4: Publish Combined Result
def node4_publish_result(student_name, course_name, internal_marks, external_marks):
    total = internal_marks + external_marks
    grade = "S" if total >= 90 else ("A" if total >= 80 else ("B" if total >= 70 else "C"))
    print(f"\n[Node 4: Result Publication]")
    print("-" * 50)
    print(f"Student Name   : {student_name}")
    print(f"Course         : {course_name}")
    print(f"Internal (CIE) : {internal_marks}/50")
    print(f"External (SEE) : {external_marks}/50")
    print(f"Grand Total    : {total}/100 -> Grade: {grade}")
    print("-" * 50)

def run_pipeline(student_id, course_id, student_answers):
    # Step 1
    eligible, info = node1_check_eligibility(student_id, course_id)
    if not eligible:
        print("Pipeline stopped early.")
        return

    # Step 2
    paper = node2_fetch_exam(course_id)

    # Step 3
    external_score = node3_grade_exam(course_id, student_answers)

    # Step 4
    node4_publish_result(info["student_name"], paper["course_name"], info["internal_marks"], external_score)

if __name__ == "__main__":
    print("=" * 60)
    print("Lab 7: Agentic Node Graph (Internal + External Assessment)")
    print("=" * 60)

    answers = {"Q1": "B", "Q2": "B", "Q3": "A", "Q4": "C", "Q5": "B"} # 60%
    run_pipeline("STU001", "ML303", answers)
