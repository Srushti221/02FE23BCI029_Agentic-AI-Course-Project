"""
TOOL 5: Dashboard Report Tool
Formats final result card showing:
- Internal Marks (out of 50)
- External Exam Marks (out of 50)
- Total Marks (out of 100) & Grade (S, A, B, C, D, E, F)
"""

def generate_dashboard_view(student_name: str, student_id: str, course_name: str, 
                            internal_marks: int, external_marks: int, integrity_status: str) -> dict:
    total_marks = internal_marks + external_marks  # out of 100
    percentage = total_marks

    # University Grade Scale (out of 100)
    if total_marks >= 90:
        grade = "S (Outstanding 🏆)"
    elif total_marks >= 80:
        grade = "A (Excellent 🌟)"
    elif total_marks >= 70:
        grade = "B (Very Good ✅)"
    elif total_marks >= 60:
        grade = "C (Good 👍)"
    elif total_marks >= 50:
        grade = "D (Average 📘)"
    elif total_marks >= 40:
        grade = "E (Pass ✔️)"
    else:
        grade = "F (Fail ❌)"

    is_certified = integrity_status != "MALPRACTICE_FLAGGED" and total_marks >= 40

    card = (
        f"=====================================================\n"
        f"  KLE TECH OFFICIAL SEMESTER GRADE CARD\n"
        f"=====================================================\n"
        f"  Student Name   : {student_name} ({student_id})\n"
        f"  Course Name    : {course_name}\n"
        f"  Internal (CIE) : {internal_marks}/50\n"
        f"  External (SEE) : {external_marks}/50\n"
        f"  Total Score    : {total_marks}/100 -> Grade: {grade}\n"
        f"  Integrity Check: {integrity_status}\n"
        f"  Final Decision : {'PASSED & CERTIFIED' if is_certified else 'WITHHELD / ON HOLD'}\n"
        f"====================================================="
    )

    return {
        "student_id": student_id,
        "internal_marks": internal_marks,
        "external_marks": external_marks,
        "total_marks": total_marks,
        "grade": grade,
        "is_certified": is_certified,
        "card_text": card
    }
