"""
TOOL 3: Auto Grader Tool
Lab 2 Concept: Tool-Using Agent — grading logic wrapped as a callable tool.
Lab 11 Concept: Agentic SDLC Factory — transforms student answers into
verified, structured grade output.
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def auto_grade(course_id: str, student_answers: dict) -> dict:
    """
    Automatically grade a student's MCQ answers against the answer key.

    Args:
        course_id:       Course code (e.g., 'CS301')
        student_answers: Dict mapping question_id to chosen option letter
                         e.g., {"Q1": "B", "Q2": "C", "Q3": "A", ...}

    Returns:
        dict with score, percentage, grade, per-question breakdown, and
        a feedback summary.
    """
    qb_path = os.path.join(DATA_DIR, "question_bank.json")
    with open(qb_path) as f:
        question_bank = json.load(f)

    if course_id not in question_bank:
        return {"success": False, "error": f"Course '{course_id}' not found.", "score": 0}

    course_data  = question_bank[course_id]
    questions    = {q["id"]: q for q in course_data["questions"]}
    total_marks  = course_data["total_marks"]

    scored       = 0
    breakdown    = []

    for q_id, q in questions.items():
        student_ans = student_answers.get(q_id, "").upper().strip()
        correct     = q["answer"]
        is_correct  = student_ans == correct
        marks_earned = q["marks"] if is_correct else 0
        scored += marks_earned

        breakdown.append({
            "question_id": q_id,
            "question": q["question"],
            "student_answer": student_ans if student_ans else "Not attempted",
            "correct_answer": correct,
            "is_correct": is_correct,
            "marks_earned": marks_earned,
            "max_marks": q["marks"],
        })

    percentage = (scored / total_marks) * 100

    # Grade logic (university-style: S, A, B, C, D, F)
    if percentage >= 90:
        grade, remarks = "S",  "Outstanding 🏆"
    elif percentage >= 80:
        grade, remarks = "A",  "Excellent 🌟"
    elif percentage >= 70:
        grade, remarks = "B",  "Very Good ✅"
    elif percentage >= 60:
        grade, remarks = "C",  "Good 👍"
    elif percentage >= 50:
        grade, remarks = "D",  "Average 📘"
    elif percentage >= 40:
        grade, remarks = "E",  "Pass ✔️"
    else:
        grade, remarks = "F",  "Fail ❌ — Revaluation recommended"

    return {
        "success": True,
        "course_id": course_id,
        "course_name": course_data["course_name"],
        "score": scored,
        "total_marks": total_marks,
        "percentage": round(percentage, 2),
        "grade": grade,
        "remarks": remarks,
        "breakdown": breakdown,
        "unattempted": [q for q in questions if q not in student_answers],
    }
