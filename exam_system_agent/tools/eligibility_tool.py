"""
TOOL 1: Eligibility Checker Tool
Rules Engine Tool:
Checks if student is eligible to write the External Exam based on:
1. Attendance >= 75%
2. Assignment completion >= 70%
3. Internal Marks >= 20/50 (40% minimum passing cutoff)
4. Fees Paid
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def check_eligibility(student_id: str, course_id: str) -> dict:
    db_path = os.path.join(DATA_DIR, "students_db.json")
    with open(db_path) as f:
        db = json.load(f)

    students = db["students"]
    courses = db["courses"]

    if student_id not in students:
        return {"eligible": False, "student_name": "Unknown", "reasons": ["Student ID not found."]}

    if course_id not in courses:
        return {"eligible": False, "student_name": "Unknown", "reasons": ["Course code not found."]}

    s = students[student_id]
    reasons = []

    # Rule 1: Attendance
    if s["attendance"] < 75:
        reasons.append(f"Low attendance: {s['attendance']}% (minimum 75% required)")

    # Rule 2: Assignments
    assign_pct = (s["assignments_submitted"] / s["total_assignments"]) * 100
    if assign_pct < 70:
        reasons.append(f"Assignments incomplete: {s['assignments_submitted']}/{s['total_assignments']} ({assign_pct:.0f}%)")

    # Rule 3: Minimum Internal Marks Cutoff (20/50)
    internals = s.get("internal_marks", 0)
    if internals < 20:
        reasons.append(f"Internal marks too low: {internals}/50 (minimum 20/50 required)")

    # Rule 4: Fee payment
    if not s["fees_paid"]:
        reasons.append("College fees pending.")

    # Rule 5: Registered
    if course_id not in s["registered_courses"]:
        reasons.append(f"Not enrolled in {courses.get(course_id)}.")

    eligible = len(reasons) == 0

    return {
        "eligible": eligible,
        "student_id": student_id,
        "student_name": s["name"],
        "course_id": course_id,
        "course_name": courses[course_id],
        "attendance": s["attendance"],
        "internal_marks": internals,
        "reasons": reasons,
        "status_summary": "APPROVED ✅" if eligible else f"REJECTED ❌ ({len(reasons)} issue(s))"
    }
