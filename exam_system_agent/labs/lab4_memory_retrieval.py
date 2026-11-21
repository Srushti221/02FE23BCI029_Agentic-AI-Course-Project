"""
Lab 4: Memory & Retrieval
Simple student version: Demonstrating Session Memory (RAM Cache) vs Stored Reference (Disk).
Subject: Agentic AI (AGI301)
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.eligibility_tool import check_eligibility

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
GRADE_STORE = os.path.join(DATA_DIR, "grade_history.json")

class MemoryAgent:
    def __init__(self):
        self.session_cache = {}  # In-memory RAM Cache

    def get_eligibility(self, student_id, course_id):
        key = f"{student_id}_{course_id}"
        # 1. Check Session Cache (Fast Retrieval)
        if key in self.session_cache:
            print(f"[Memory Cache Hit] Retrieved {student_id} from Session RAM.")
            return self.session_cache[key]

        # 2. Cache Miss: Execute Tool and Store
        print(f"[Memory Cache Miss] Calling check_eligibility tool for {student_id}...")
        result = check_eligibility(student_id, course_id)
        self.session_cache[key] = result
        return result

    def save_to_disk(self, student_id, course_id, grade):
        # Stored Reference (Persistent Disk Memory)
        print(f"\n[Persistent Memory] Saving grade for {student_id} to disk...")
        data = {}
        if os.path.exists(GRADE_STORE):
            with open(GRADE_STORE, "r") as f:
                data = json.load(f)
        data[f"{student_id}_{course_id}"] = {"grade": grade, "subject": "Agentic AI"}
        with open(GRADE_STORE, "w") as f:
            json.dump(data, f, indent=2)
        print(f" -> Saved to {os.path.basename(GRADE_STORE)} permanently.")

if __name__ == "__main__":
    print("=" * 55)
    print("Lab 4: Memory & Retrieval (Session Cache vs Disk)")
    print("=" * 55)

    agent = MemoryAgent()

    # Call 1: Tool execution
    res1 = agent.get_eligibility("STU001", "AGI301")
    print(f" -> Status: {res1['student_name']} is {res1['status_summary']}\n")

    # Call 2: Retrieved from memory cache
    res2 = agent.get_eligibility("STU001", "AGI301")
    print(f" -> Status: {res2['student_name']} is {res2['status_summary']}")

    # Save to persistent storage
    agent.save_to_disk("STU001", "AGI301", "Grade: S")
    print("=" * 55)
