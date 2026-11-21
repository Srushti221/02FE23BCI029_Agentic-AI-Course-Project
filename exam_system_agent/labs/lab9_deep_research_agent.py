"""
Lab 9: Deep Research Agent
Simple student version: Collects and prints course stats from JSON files into an evidence summary.
Subjects: CNS, Agentic AI, ML, DBMS
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def run_research(course_id):
    # 1. Read files
    with open(os.path.join(DATA_DIR, "students_db.json")) as f:
        students_data = json.load(f)
    with open(os.path.join(DATA_DIR, "question_bank.json")) as f:
        question_data = json.load(f)

    course = question_data.get(course_id, {})
    course_name = course.get("course_name", "Unknown")
    questions = course.get("questions", [])

    # 2. Check student counts
    total_enrolled = 0
    eligible_count = 0
    for sid, info in students_data["students"].items():
        if course_id in info["registered_courses"]:
            total_enrolled += 1
            if info["attendance"] >= 75 and info["fees_paid"]:
                eligible_count += 1

    # 3. Print Briefing
    print(f"\n[Research Summary: {course_name}]")
    print(f"Total Enrolled Students : {total_enrolled}")
    print(f"Eligible for Exam       : {eligible_count}")
    print(f"Questions Prepared      : {len(questions)}")

    # 4. Print Evidence Table
    print("\n--- Evidence Table (Question Bank) ---")
    print(f"{'QID':<5} | {'Marks':<6} | Question")
    print("-" * 55)
    for q in questions:
        print(f"{q['id']:<5} | {q['marks']:<6} | {q['question']}")

if __name__ == "__main__":
    print("=" * 55)
    print("Lab 9: Deep Research Agent (CNS & Agentic AI)")
    print("=" * 55)

    # Run for Computer Networks & Security
    run_research("CNS302")
