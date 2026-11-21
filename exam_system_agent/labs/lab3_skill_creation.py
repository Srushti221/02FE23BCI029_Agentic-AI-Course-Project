"""
Lab 3: Skill Creation
Simple student version: Creating two reusable skills (Profile Skill & Summary Skill).
Subjects: Agentic AI (AGI301)
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Skill 1: Reusable Profile Lookup
class StudentProfileSkill:
    def get_profile(self, student_id):
        with open(os.path.join(DATA_DIR, "students_db.json")) as f:
            db = json.load(f)
        s = db["students"].get(student_id, {})
        return {
            "name": s.get("name"),
            "attendance": f"{s.get('attendance')}%",
            "internal_marks": f"{s.get('internal_marks', 0)}/50",
            "status": "Regular" if s.get("attendance", 0) >= 75 else "Shortage"
        }

# Skill 2: Reusable Marksheet Summary
class ResultSummarySkill:
    def format_summary(self, name, subject, internal, external):
        total = internal + external
        grade = "S" if total >= 90 else ("A" if total >= 80 else "B")
        return (
            f"Student: {name} | Subject: {subject}\n"
            f" -> Internal (CIE): {internal}/50 | External (SEE): {external}/50\n"
            f" -> Grand Total   : {total}/100 -> Grade: {grade}"
        )

if __name__ == "__main__":
    print("=" * 60)
    print("Lab 3: Skill Creation (Internal + External Assessment)")
    print("=" * 60)

    profile_skill = StudentProfileSkill()
    summary_skill = ResultSummarySkill()

    # Using Skill 1
    print("\n[Executing Skill 1: Profile Lookup]")
    p1 = profile_skill.get_profile("STU001")
    print(f" -> Name: {p1['name']} | Attendance: {p1['attendance']} | Internals: {p1['internal_marks']}")

    # Using Skill 2
    print("\n[Executing Skill 2: Result Summary Generator]")
    report = summary_skill.format_summary(p1["name"], "Agentic AI", internal=46, external=50)
    print(report)

    print("\n" + "=" * 60)
    print("Skills successfully created and reused by Agent!")
    print("=" * 60)
