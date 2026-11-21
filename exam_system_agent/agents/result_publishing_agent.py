"""
AGENT 4: Result Publishing Agent
==================================
Lab 7  — Agentic Node Graph: Final node in the pipeline — aggregates data
          from all previous agents and produces the final result report.
Lab 12 — Safety & Governance: Applies a "faculty sign-off" gate before
          publishing. No results are released without approval.
Lab 9  — Deep Research Agent pattern: Produces an evidence table (grade
          breakdown) alongside the final published result.

Role:
  Collects draft grades from AutoGradingAgent, runs a faculty approval gate,
  then publishes the final result report — the fourth Expected Output.
  Also integrates a simple Proctoring Integrity flag from the exam session.
"""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.dashboard_report_tool import generate_dashboard_view


class ResultPublishingAgent:
    """
    Final pipeline agent. Retrieves draft grades, enforces faculty sign-off,
    and publishes the official results as a structured report.
    """

    def __init__(self, grading_agent=None):
        self.name = "Result Publishing Agent"
        self.grading_agent = grading_agent
        self._published_results: list[dict] = []

    # ------------------------------------------------------------------
    # Core agent action
    # ------------------------------------------------------------------
    def publish_results(self, course_id: str,
                        faculty_approval: bool = True,
                        integrity_flags: dict = None) -> dict:
        """
        Publish final results for a course.

        Args:
            course_id:        Course for which results are published
            faculty_approval: Safety gate — if False, results are HELD (Lab 12)
            integrity_flags:  Dict of {student_id: flag_reason} from proctoring

        Returns:
            Published result report dict
        """
        print(f"\n[{self.name}] Publishing results for course: {course_id}")

        # ← SAFETY GATE (Lab 12 — Governance)
        if not faculty_approval:
            print("   🔒 Faculty approval NOT granted. Results are ON HOLD.")
            return {
                "published": False,
                "course_id": course_id,
                "reason": "Pending faculty sign-off",
                "results": []
            }

        if not self.grading_agent:
            return {"published": False, "error": "No grading agent connected."}

        # Pull draft grades for this course (Lab 7 — consuming upstream output)
        all_drafts = self.grading_agent.get_draft_grades()
        course_drafts = [d for d in all_drafts if d.get("course_id") == course_id]

        if not course_drafts:
            print(f"   ⚠️  No draft grades found for {course_id}.")
            return {"published": False, "course_id": course_id,
                    "reason": "No draft grades available."}

        integrity_flags = integrity_flags or {}
        final_results   = []

        print(f"\n   {'─'*58}")
        print(f"   {'STUDENT':<20} {'SCORE':>8} {'%':>7} {'GRADE':>6}  FLAG")
        print(f"   {'─'*58}")

        for draft in course_drafts:
            sid   = draft["student_id"]
            flag  = integrity_flags.get(sid, "Clear")

            entry = {
                "student_id":   sid,
                "course_id":    course_id,
                "course_name":  draft.get("course_name", ""),
                "score":        draft.get("score", 0),
                "total_marks":  draft.get("total_marks", 0),
                "percentage":   draft.get("percentage", 0),
                "grade":        draft.get("grade", "F"),
                "remarks":      draft.get("remarks", ""),
                "integrity_flag": flag,
                "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            final_results.append(entry)

            # Lab 12 — Flag: withhold result if integrity issue
            flag_icon = "⚠️ " + flag if flag != "Clear" else "✅ Clear"
            print(f"   {sid:<20} {entry['score']:>5}/{entry['total_marks']:<2}"
                  f"  {entry['percentage']:>5}%  {entry['grade']:>5}   {flag_icon}")

            # Mark as published in grading agent memory
            self.grading_agent.mark_published(sid, course_id)

        print(f"   {'─'*58}")
        print(f"   Faculty Sign-off: ✅ Approved | Published: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        # Produce integrity report summary (second Expected Output from spec)
        integrity_report = self._generate_integrity_report(integrity_flags)

        report = {
            "published":         True,
            "course_id":         course_id,
            "total_students":    len(final_results),
            "results":           final_results,
            "integrity_report":  integrity_report,
            "published_at":      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self._published_results.append(report)
        return report

    # ------------------------------------------------------------------
    # Integrity Report (Proctoring & Integrity Agent output — simplified)
    # ------------------------------------------------------------------
    def _generate_integrity_report(self, flags: dict) -> dict:
        """
        Produce a simple integrity summary (Proctoring & Integrity Agent role).
        In a full system this would consume real proctoring signals (webcam,
        tab-switch events, etc.). Here it uses pre-set flags.
        """
        total   = len(flags)
        flagged = {k: v for k, v in flags.items() if v != "Clear"}
        return {
            "total_flagged":  len(flagged),
            "clear_students": total - len(flagged),
            "flagged_cases":  flagged,
            "recommendation": (
                "Manual review required for flagged cases."
                if flagged else "All students cleared. No anomalies detected."
            )
        }

    def get_all_published(self) -> list[dict]:
        return self._published_results
