"""
TOOL 2: Question Fetcher Tool
Lab 2 Concept: Tool-Using Agent — agents call this tool to fetch exam questions
from the question bank (simulates an Exam Delivery Platform).
Lab 5 Concept: MCP-Style Connector — acts like a data-source connector.
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def fetch_exam_questions(course_id: str) -> dict:
    """
    Fetch exam questions for a given course from the question bank.

    Args:
        course_id: Course code (e.g., 'CS301')

    Returns:
        dict with course metadata and list of questions (options shuffled is
        handled by Exam Delivery Agent at presentation time).
    """
    qb_path = os.path.join(DATA_DIR, "question_bank.json")
    with open(qb_path) as f:
        question_bank = json.load(f)

    if course_id not in question_bank:
        return {
            "success": False,
            "error": f"No question bank found for course '{course_id}'.",
            "questions": []
        }

    course_data = question_bank[course_id]
    return {
        "success": True,
        "course_id": course_id,
        "course_name": course_data["course_name"],
        "total_questions": len(course_data["questions"]),
        "total_marks": course_data["total_marks"],
        "duration_minutes": course_data["duration_minutes"],
        "questions": course_data["questions"],
    }
