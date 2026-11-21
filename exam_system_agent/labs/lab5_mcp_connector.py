"""
Lab 5: MCP-Style Connector
Simple student version: A single connector interface accessing File, SQLite DB, and API.
Subject: Agentic AI (AGI301)
"""

import sys
import os
import json
import sqlite3

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DB_FILE = os.path.join(DATA_DIR, "exam_allocations.db")

class ExamMCPConnector:
    def __init__(self):
        # Create sample SQLite table
        conn = sqlite3.connect(DB_FILE)
        conn.execute("CREATE TABLE IF NOT EXISTS rooms (code TEXT PRIMARY KEY, hall TEXT, invigilator TEXT)")
        conn.execute("INSERT OR REPLACE INTO rooms VALUES ('AGI301', 'Hall-101', 'Dr. Kulkarni')")
        conn.commit()
        conn.close()

    def get_from_database(self, course_id):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT hall, invigilator FROM rooms WHERE code = ?", (course_id,))
        row = cursor.fetchone()
        conn.close()
        return {"hall": row[0], "invigilator": row[1]} if row else {}

    def get_from_file(self, course_id):
        with open(os.path.join(DATA_DIR, "question_bank.json")) as f:
            data = json.load(f)
        return data.get(course_id, {})

    def get_from_api(self, course_id):
        # Simulated Syllabus API endpoint
        return {"units": "LLM Agents, Multi-Agent Swarms, Tool Calling, MCP Protocol"}

if __name__ == "__main__":
    print("=" * 55)
    print("Lab 5: MCP-Style Connector (Unified Gateway)")
    print("Subject: Agentic AI (AGI301)")
    print("=" * 55)

    connector = ExamMCPConnector()

    # Source 1: SQLite DB
    db_res = connector.get_from_database("AGI301")
    print(f"\n[Source 1: SQLite Database via MCP]")
    print(f" -> Allocated Venue: {db_res['hall']} | Invigilator: {db_res['invigilator']}")

    # Source 2: Local File
    file_res = connector.get_from_file("AGI301")
    print(f"\n[Source 2: File System via MCP]")
    print(f" -> Subject: {file_res['course_name']} | Questions in file: {len(file_res['questions'])}")

    # Source 3: Simulated API
    api_res = connector.get_from_api("AGI301")
    print(f"\n[Source 3: Web API via MCP]")
    print(f" -> Syllabus Topics: {api_res['units']}")

    print("\n" + "=" * 55)
    print("Agent accessed 3 sources through ONE unified connector!")
    print("=" * 55)
