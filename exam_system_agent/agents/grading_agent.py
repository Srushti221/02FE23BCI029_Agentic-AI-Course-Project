"""
AGENT 3: Auto-Grading Agent
============================
Lab 2  — Tool-Using Agent: Calls the auto_grade TOOL.
Lab 8  — Parallel Swarm: In a swarm setup, multiple grading agents could
          grade different courses simultaneously; this single agent models
          one "swarm role".
Lab 11 — Agentic SDLC Factory: Takes raw answers (input), applies grading
          rules (processing), and produces structured grade output (artifact).

Role:
  Receives student answers from ExamDeliveryAgent, calls the grader tool,
  and produces "Draft Grades" — the third Expected Output from the spec.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tools.grader_tool import auto_grade


class AutoGradingAgent:
    """
    Grades student MCQ answers using the auto_grade tool.
    Stores draft grades in memory until the ResultPublishingAgent publishes them.
    """

    def __init__(self):
        self.name = "Auto-Grading Agent"
        # Draft grade store (unpublished) — Lab 4 Memory concept
        self._draft_grades: dict[str, dict] = {}  # key: f"{student_id}::{course_id}"

    # ------------------------------------------------------------------
    # Core agent action
    # ------------------------------------------------------------------
    def grade(self, student_id: str, course_id: str, answers: dict) -> dict:
        """
        Grade a student's answers and store as a draft.

        Args:
            student_id: Student identifier
            course_id:  Course being graded
            answers:    Dict mapping question_id -> chosen option

        Returns:
            Grading result dict (draft grade)
        """
        print(f"\n[{self.name}] Grading {student_id}'s answers for {course_id}...")

        if not answers:
            print("   ⚠️  No answers provided — marking as absent.")
            return {"success": False, "student_id": student_id,
                    "course_id": course_id, "grade": "AB", "score": 0,
                    "remarks": "Absent — No answers submitted"}

        # ← TOOL CALL (Lab 2 concept)
        result = auto_grade(course_id, answers)
        result["student_id"] = student_id
        result["published"]  = False   # Draft — not yet published

        # Store draft (Lab 4 Memory)
        key = f"{student_id}::{course_id}"
        self._draft_grades[key] = result

        # Agent decision: flag poor performers
        if result["success"]:
            pct = result["percentage"]
            print(f"   📊 Score: {result['score']}/{result['total_marks']} "
                  f"({pct}%) — Grade: {result['grade']} — {result['remarks']}")

            if pct < 40:
                print(f"   ⚠️  ALERT: {student_id} scored below passing threshold!")
            if result["unattempted"]:
                print(f"   ℹ️  Unattempted: {result['unattempted']}")

        return result

    def grade_batch(self, submissions: list[dict]) -> list[dict]:
        """
        Grade multiple student submissions.

        Args:
            submissions: List of dicts with keys: student_id, course_id, answers
        """
        return [self.grade(s["student_id"], s["course_id"], s["answers"])
                for s in submissions]

    # ------------------------------------------------------------------
    # Draft grade retrieval
    # ------------------------------------------------------------------
    def get_draft_grades(self) -> list[dict]:
        """Return all draft (unpublished) grades."""
        return [v for v in self._draft_grades.values() if not v.get("published")]

    def get_grade(self, student_id: str, course_id: str) -> dict | None:
        return self._draft_grades.get(f"{student_id}::{course_id}")

    def mark_published(self, student_id: str, course_id: str):
        key = f"{student_id}::{course_id}"
        if key in self._draft_grades:
            self._draft_grades[key]["published"] = True
