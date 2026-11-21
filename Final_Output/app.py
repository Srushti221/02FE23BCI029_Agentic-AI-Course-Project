"""
Web dashboard for the Online Course Examination System Agent.
Run:  pip install flask  &&  python app.py   ->  http://127.0.0.1:5000
Wraps your existing agents; no agent code is modified.
"""
import os, sys, json
from datetime import datetime
from flask import Flask, jsonify, request, render_template

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from agents.registration_agent import RegistrationEligibilityAgent
from agents.exam_delivery_agent import ExamDeliveryAgent
from agents.grading_agent import AutoGradingAgent
from agents.proctoring_agent import ProctoringIntegrityAgent
from agents.result_publishing_agent import ResultPublishingAgent
from agents.subjective_grading_agent import SubjectiveGradingAssistAgent
from agents.grievance_revaluation_agent import GrievanceRevaluationAgent
from tools.question_fetcher_tool import fetch_exam_questions

app = Flask(__name__)

# ---- wire the pipeline once (same graph as main.py) ----
reg = RegistrationEligibilityAgent()
delivery = ExamDeliveryAgent(registration_agent=reg)
grader = AutoGradingAgent()
proctor = ProctoringIntegrityAgent()
publisher = ResultPublishingAgent(grading_agent=grader)
subjective = SubjectiveGradingAssistAgent()
grievance = GrievanceRevaluationAgent(grading_agent=grader, subjective_agent=subjective)

AUDIT = []          # in-memory audit trail shown in the dashboard
PUBLISHED = {}      # course_id -> latest published report


def log(agent, action, detail):
    AUDIT.append({"time": datetime.now().strftime("%H:%M:%S"),
                  "agent": agent, "action": action, "detail": detail})


def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
        return json.load(f)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/meta")
def meta():
    db = load("students_db.json")
    students = [{"id": k, "name": v["name"], "attendance": v["attendance"],
                 "assignments": f'{v["assignments_submitted"]}/{v["total_assignments"]}',
                 "internal": v["internal_marks"], "fees_paid": v["fees_paid"],
                 "courses": v["registered_courses"]} for k, v in db["students"].items()]
    return jsonify(students=students, courses=db["courses"])


@app.post("/api/register")
def register():
    d = request.json
    res = reg.process(d["student_id"], d["course_id"])
    log(reg.name, f'Eligibility {d["student_id"]}/{d["course_id"]}', res["status_summary"] if "status_summary" in res else "; ".join(res["reasons"]))
    return jsonify(res)


@app.post("/api/register/bulk")
def register_bulk():
    course = request.json["course_id"]
    ids = [s["id"] for s in meta().json["students"]]
    out = [reg.process(sid, course) for sid in ids]
    log(reg.name, f"Bulk eligibility {course}", f'{sum(r["eligible"] for r in out)}/{len(out)} approved')
    return jsonify(out)


@app.get("/api/registrations")
def registrations():
    return jsonify(reg.get_registration_list())


@app.get("/api/exam/<course_id>")
def get_exam(course_id):
    sid = request.args.get("student_id", "")
    if not reg.is_registered(sid, course_id):
        return jsonify(success=False, error="Student is not eligible / not registered. Run the eligibility check first."), 403
    data = fetch_exam_questions(course_id)
    if not data["success"]:
        return jsonify(data), 404
    for q in data["questions"]:          # never send the answer key to the browser
        q.pop("answer", None)
    log(delivery.name, f"Exam delivered {sid}/{course_id}", f'{data["total_questions"]} questions')
    return jsonify(data)


@app.post("/api/submit")
def submit():
    d = request.json
    sid, cid = d["student_id"], d["course_id"]
    if not reg.is_registered(sid, cid):
        return jsonify(success=False, error="Not eligible"), 403
    integ = proctor.monitor_session(sid, cid, d.get("telemetry", []))
    grade = grader.grade(sid, cid, d.get("answers", {}))
    log(proctor.name, f"Session {sid}/{cid}", f'{integ["status"]} (risk {integ["risk_score"]})')
    log(grader.name, f"Graded {sid}/{cid}", f'{grade.get("score")}/{grade.get("total_marks")} -> {grade.get("grade")}')
    return jsonify(grade=grade, integrity=integ)


@app.get("/api/drafts")
def drafts():
    out = []
    for g in grader._draft_grades.values():
        integ = proctor.get_integrity_report(g["student_id"], g["course_id"])
        out.append({**{k: g.get(k) for k in ("student_id", "course_id", "course_name", "score",
                                             "total_marks", "percentage", "grade", "remarks", "published")},
                    "integrity": integ})
    return jsonify(out)


@app.post("/api/publish")
def publish():
    d = request.json
    cid = d["course_id"]
    flags = {}
    for g in grader._draft_grades.values():
        if g["course_id"] == cid:
            r = proctor.get_integrity_report(g["student_id"], cid)
            flags[g["student_id"]] = "Clear" if not r or r["status"] == "CLEAN" else f'{r["status"]}: ' + "; ".join(r["violations"])
    report = publisher.publish_results(cid, faculty_approval=bool(d.get("faculty_approval")), integrity_flags=flags)
    if report.get("published"):
        PUBLISHED[cid] = report
    log(publisher.name, f"Publish {cid}", "PUBLISHED" if report.get("published") else f'HELD - {report.get("reason", report.get("error", ""))}')
    return jsonify(report)


@app.get("/api/published")
def published():
    return jsonify(list(PUBLISHED.values()))


@app.post("/api/grievance")
def file_grievance():
    d = request.json
    res = grievance.file_grievance(d["student_id"], d["course_id"], d.get("question_id", "Q1"),
                                   d["claim"], int(d.get("current_marks", 0)))
    log(grievance.name, res["grievance_id"], f'{res["decision"]} ({res["delta"]:+d} marks)')
    return jsonify(res)


@app.post("/api/subjective")
def subjective_eval():
    d = request.json
    res = subjective.evaluate_short_answer(d["course_id"], d["question"], d["answer"])
    log(subjective.name, f'Short answer {d["course_id"]}', f'{res["marks_awarded"]}/25')
    return jsonify(res)


@app.get("/api/audit")
def audit():
    return jsonify(AUDIT[::-1])


@app.get("/api/stats")
def stats():
    regs = reg.get_registration_list()
    dr = list(grader._draft_grades.values())
    flagged = [r for r in proctor._integrity_records.values() if r["status"] != "CLEAN"]
    return jsonify(checked=len(regs), eligible=sum(r["eligible"] for r in regs),
                   graded=len(dr), avg=round(sum(g.get("percentage", 0) for g in dr) / len(dr), 1) if dr else 0,
                   flagged=len(flagged), published=len(PUBLISHED))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
