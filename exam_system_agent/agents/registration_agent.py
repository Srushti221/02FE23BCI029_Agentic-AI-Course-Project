"""
AGENT 1: Registration & Eligibility Agent
=========================================
Lab 1  — Agent vs Chatbot: This agent DECIDES (approve/reject) rather than
          just responding. It acts on rules, not conversation alone.
Lab 2  — Tool-Using Agent: Uses the check_eligibility TOOL.
Lab 4  — Memory & Retrieval: Maintains a session-level eligibility registry
          (in-memory) so downstream agents can query it without re-checking.

Role:
  Verifies every student's eligibility before the exam.
  Produces a "Registration List" — the first Expected Output from the spec.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tools.eligibility_tool import check_eligibility


class RegistrationEligibilityAgent:
    """
    Checks whether each student meets the eligibility criteria for a given
    course exam. Maintains an in-memory registry of approved students.
    """

    def __init__(self):
        self.name = "Registration & Eligibility Agent"
        # Lab 4 — Memory: session-level registry acts as stored reference
        self._registry: dict[str, dict] = {}  # key: f"{student_id}::{course_id}"

    # ------------------------------------------------------------------
    # Core agent action
    # ------------------------------------------------------------------
    def process(self, student_id: str, course_id: str) -> dict:
        """
        Invoke the eligibility tool and store result in memory.
        Returns the eligibility result dict.
        """
        print(f"\n[{self.name}] Checking eligibility for {student_id} in {course_id}...")

        # ← TOOL CALL (Lab 2 concept)
        result = check_eligibility(student_id, course_id)

        # ← MEMORY WRITE (Lab 4 concept)
        key = f"{student_id}::{course_id}"
        self._registry[key] = result

        # Agent decision logic (Lab 1 — Agent behaviour)
        if result["eligible"]:
            print(f"   ✅ {result['student_name']} is ELIGIBLE for {result['course_name']}")
        else:
            print(f"   ❌ {result['student_name']} is NOT ELIGIBLE:")
            for r in result["reasons"]:
                print(f"      • {r}")

        return result

    def bulk_process(self, student_course_pairs: list[tuple]) -> list[dict]:
        """Process multiple students at once and return a registration list."""
        registration_list = []
        for student_id, course_id in student_course_pairs:
            result = self.process(student_id, course_id)
            registration_list.append(result)
        return registration_list

    # ------------------------------------------------------------------
    # Memory query (Lab 4 — Retrieval)
    # ------------------------------------------------------------------
    def is_registered(self, student_id: str, course_id: str) -> bool:
        """Allow downstream agents to check eligibility without re-running."""
        key = f"{student_id}::{course_id}"
        entry = self._registry.get(key)
        return entry["eligible"] if entry else False

    def get_registration_list(self) -> list[dict]:
        """Return all processed eligibility records (the Registration List output)."""
        return list(self._registry.values())

    def get_approved_students(self) -> list[dict]:
        """Return only the approved students."""
        return [v for v in self._registry.values() if v["eligible"]]
