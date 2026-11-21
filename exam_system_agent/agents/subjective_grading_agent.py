"""
AGENT 5: Subjective Grading Assist Agent
Evaluates Section B (Short Answer) out of 25 marks.
Combined with Section A MCQs (25 marks), External Exam totals 50 marks.
"""

class SubjectiveGradingAssistAgent:
    def __init__(self):
        self.name = "Subjective Grading Assist Agent"

        self.rubrics = {
            "AGI301": ["planner", "memory", "tools", "action", "mcp"],
            "CNS302": ["encryption", "security", "firewall", "protocol", "keys"],
            "ML303":  ["training", "dataset", "accuracy", "model", "features"],
            "DBMS304":["tables", "primary key", "queries", "acid", "sql"]
        }

    def evaluate_short_answer(self, course_id: str, question: str, student_answer: str) -> dict:
        keywords = self.rubrics.get(course_id, ["concept", "logic"])
        ans = student_answer.lower()
        matched = [k for k in keywords if k in ans]

        # Scoring out of 25 marks
        if len(matched) >= 3:
            marks = 25
            feedback = "Comprehensive answer! All core technical terms present."
        elif len(matched) >= 1:
            marks = 20
            feedback = "Good response. Main points explained clearly."
        else:
            marks = 12
            feedback = "Basic response. Needs more key details."

        return {
            "question": question,
            "student_answer": student_answer,
            "max_marks": 25,
            "marks_awarded": marks,
            "feedback": feedback
        }
