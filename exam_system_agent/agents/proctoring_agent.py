"""
AGENT 3: Proctoring & Integrity Agent
Role:
  Monitors live telemetry and behavioral signals during online exams.
  Uses the proctoring_signal_tool to compute risk scores.
Produces:
  Integrity Report (One of the 4 Expected Outputs from the slide)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.proctoring_signal_tool import analyze_proctoring_signals

class ProctoringIntegrityAgent:
    def __init__(self):
        self.name = "Proctoring & Integrity Agent"
        self._integrity_records = {}

    def monitor_session(self, student_id: str, course_id: str, telemetry_events: list = None) -> dict:
        # Tool call to proctoring_signal_tool
        signal_audit = analyze_proctoring_signals(telemetry_events)

        record = {
            "student_id": student_id,
            "course_id": course_id,
            "status": signal_audit["status"],
            "risk_score": signal_audit["risk_score"],
            "violations": signal_audit["details"],
            "advisory": signal_audit["advisory"]
        }
        self._integrity_records[f"{student_id}_{course_id}"] = record
        return record

    def get_integrity_report(self, student_id: str, course_id: str) -> dict:
        return self._integrity_records.get(f"{student_id}_{course_id}")
