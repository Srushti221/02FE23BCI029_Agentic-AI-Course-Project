"""
Lab 6: OpenCLA / OpenClaw Runtime Environment
Simple student version: A basic runner that executes tools and logs what happened.
Subjects: Agentic AI, ML, CNS, DBMS
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.eligibility_tool import check_eligibility
from tools.grader_tool import auto_grade

# Simple runtime that stores tools and logs calls
class SimpleRuntime:
    def __init__(self):
        self.tools = {}
        self.logs = []

    def add_tool(self, name, func):
        self.tools[name] = func
        print(f"[Runtime] Tool added: {name}")

    def run_tool(self, name, **kwargs):
        print(f"[Runtime] Running {name}...")
        result = self.tools[name](**kwargs)
        
        # Log this event
        time_str = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"{time_str} - Executed {name}")
        return result

    def show_logs(self):
        print("\n--- Audit Log ---")
        for entry in self.logs:
            print(entry)

if __name__ == "__main__":
    print("=" * 50)
    print("Lab 6: OpenCLA Runtime")
    print("=" * 50)

    app = SimpleRuntime()

    # 1. Register tools
    app.add_tool("check_eligibility", check_eligibility)
    app.add_tool("auto_grade", auto_grade)

    # 2. Check student eligibility
    print("\nStep 1: Check eligibility")
    el_result = app.run_tool("check_eligibility", student_id="STU001", course_id="AGI301")
    student_name = el_result["student_name"]
    print(f"Student: {student_name}")
    print(f"Status: {el_result['status_summary']}")

    # 3. Grade an exam with realistic student marks
    print(f"\nStep 2: Auto grade Agentic AI exam for {student_name}")
    student_answers = {"Q1": "B", "Q2": "C", "Q3": "B", "Q4": "A", "Q5": "C"}  # 3 right, 2 wrong
    gr_result = app.run_tool("auto_grade", course_id="AGI301", student_answers=student_answers)
    print(f"Student: {student_name}")
    print(f"Result: {gr_result['score']}/{gr_result['total_marks']} Marks (Grade: {gr_result['grade']})")

    # 4. Show audit logs
    app.show_logs()
