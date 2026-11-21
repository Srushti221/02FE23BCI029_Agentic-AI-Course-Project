"""
Lab 2: Tool-Using Agent
Simple student version: Agent orchestrates 3 separate tools (Calculator, File Reader, Mock API).
Subjects: Machine Learning (ML303) & CNS (CNS302)
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Tool 1: Math Calculator Tool
def calculator_tool(scores):
    return {
        "average": round(sum(scores) / len(scores), 1),
        "highest": max(scores),
        "passed": sum(1 for s in scores if s >= 40)
    }

# Tool 2: File Reader Tool
def file_reader_tool(course_id):
    path = os.path.join(DATA_DIR, "question_bank.json")
    with open(path, "r") as f:
        data = json.load(f)
    return data.get(course_id, {})

# Tool 3: Mock API Tool
def mock_api_tool(student_id):
    api_db = {
        "STU001": {"name": "Rahul Sharma", "cgpa": 8.7, "enrolled": ["AGI301", "CNS302", "ML303"]}
    }
    return api_db.get(student_id, {"error": "Not found"})

if __name__ == "__main__":
    print("=" * 55)
    print("Lab 2: Tool-Using Agent")
    print("=" * 55)

    # 1. Use Tool 2 (File Reader)
    print("\n[Tool 1: File Reader] Fetching exam questions for Machine Learning (ML303)...")
    paper = file_reader_tool("ML303")
    print(f" -> Subject: {paper['course_name']} | Total Questions: {len(paper['questions'])} | Max Marks: {paper['total_marks']}")

    # 2. Use Tool 1 (Calculator)
    print("\n[Tool 2: Calculator] Computing batch statistics for ML303...")
    scores = [85, 92, 78, 64, 45, 95]
    stats = calculator_tool(scores)
    print(f" -> Class Average: {stats['average']} | Highest Score: {stats['highest']} | Passed: {stats['passed']}/{len(scores)}")

    # 3. Use Tool 3 (Mock API)
    print("\n[Tool 3: Mock API] Querying student record for STU001...")
    student = mock_api_tool("STU001")
    print(f" -> Name: {student['name']} | CGPA: {student['cgpa']} | Courses: {', '.join(student['enrolled'])}")

    print("\n" + "=" * 55)
    print("Agent successfully executed all 3 tools!")
    print("=" * 55)
