"""
AGENT 2: Exam Delivery Agent
=============================
Lab 2  — Tool-Using Agent: Uses the question_fetcher TOOL to pull questions
          from the question bank.
Lab 5  — MCP-Style Connector: Acts like a lightweight data-source connector
          between the question bank (data source) and the student interface.
Lab 7  — Agentic Node Graph: This agent is a node in the multi-agent pipeline;
          it only delivers exams to students already approved by Agent 1.

Role:
  Fetches exam questions, presents them to the student, and collects answers.
  Coordinates with RegistrationEligibilityAgent before serving any exam.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tools.question_fetcher_tool import fetch_exam_questions


class ExamDeliveryAgent:
    """
    Responsible for fetching and presenting exam questions to eligible students,
    and collecting their responses.
    """

    def __init__(self, registration_agent=None):
        self.name = "Exam Delivery Agent"
        # Lab 7 — Agent dependency: holds reference to upstream agent
        self.registration_agent = registration_agent

    # ------------------------------------------------------------------
    # Core agent action
    # ------------------------------------------------------------------
    def deliver_exam(self, student_id: str, course_id: str,
                     interactive: bool = True) -> dict:
        """
        Check eligibility via upstream agent, fetch questions, and collect
        answers either interactively (CLI) or return questions for auto-answer.

        Args:
            student_id:   Student taking the exam
            course_id:    Course for which exam is being delivered
            interactive:  If True, prompts the user; if False, returns questions

        Returns:
            dict with student_id, course_id, answers, and exam metadata
        """
        print(f"\n[{self.name}] Starting exam delivery for {student_id} — {course_id}")

        # ← ELIGIBILITY GATE (Agent-to-Agent coordination, Lab 7)
        if self.registration_agent:
            if not self.registration_agent.is_registered(student_id, course_id):
                print(f"   🚫 Access denied: {student_id} is not eligible for {course_id}.")
                return {
                    "success": False,
                    "student_id": student_id,
                    "course_id": course_id,
                    "error": "Student not eligible or not registered.",
                    "answers": {}
                }

        # ← TOOL CALL: Fetch questions (Lab 2)
        exam_data = fetch_exam_questions(course_id)

        if not exam_data["success"]:
            print(f"   ⚠️  Could not fetch questions: {exam_data['error']}")
            return {"success": False, "error": exam_data["error"], "answers": {}}

        print(f"\n   📋 Exam: {exam_data['course_name']}")
        print(f"   📝 Questions: {exam_data['total_questions']}  |  "
              f"⏱  Duration: {exam_data['duration_minutes']} mins  |  "
              f"🏆 Total Marks: {exam_data['total_marks']}\n")

        answers = {}
        questions = exam_data["questions"]

        if interactive:
            answers = self._collect_answers_interactive(questions)
        else:
            # Non-interactive: just display questions and return blank answers
            self._display_questions(questions)
            print("   [Non-interactive mode: answers will be supplied externally]")

        return {
            "success": True,
            "student_id": student_id,
            "course_id": course_id,
            "course_name": exam_data["course_name"],
            "total_marks": exam_data["total_marks"],
            "answers": answers,
            "questions_seen": len(questions),
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _display_questions(self, questions: list):
        for i, q in enumerate(questions, 1):
            print(f"   Q{i}. {q['question']}  [{q['marks']} marks]")
            for opt in q["options"]:
                print(f"       {opt}")

    def _collect_answers_interactive(self, questions: list) -> dict:
        answers = {}
        for i, q in enumerate(questions, 1):
            print(f"   Q{i}. {q['question']}  [{q['marks']} marks]")
            for opt in q["options"]:
                print(f"       {opt}")
            while True:
                choice = input("   Your answer (A/B/C/D): ").strip().upper()
                if choice in ["A", "B", "C", "D"]:
                    answers[q["id"]] = choice
                    break
                print("   ⚠️  Please enter A, B, C, or D.")
            print()
        return answers
