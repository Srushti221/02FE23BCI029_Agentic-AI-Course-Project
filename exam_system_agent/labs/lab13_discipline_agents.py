"""
Lab 13: Discipline-Specific Agents (CS & AI Department)
Simple student version: Specialized evaluation worklets for 4 Computer Science domain subjects:
1. Agentic AI (AGI301)
2. Computer Networks & Security (CNS302)
3. Machine Learning (ML303)
4. Database Management Systems (DBMS304)
"""

import sys
import os

# 1. Agentic AI Worklet: Checks agent concepts & autonomy
def worklet_agentic_ai(answer):
    keywords = ["autonomous", "memory", "tool", "mcp", "planner"]
    matched = [k for k in keywords if k in answer.lower()]
    score = 10 if len(matched) >= 2 else 5
    feedback = f"Key terms verified ({', '.join(matched)})." if score == 10 else "Missing core agentic concepts."
    return score, feedback

# 2. Computer Networks & Security (CNS) Worklet: Checks security & protocol terms
def worklet_cns(answer):
    keywords = ["encryption", "security", "firewall", "protocol", "https", "aes"]
    matched = [k for k in keywords if k in answer.lower()]
    score = 10 if len(matched) >= 2 else 5
    feedback = f"Security concepts verified ({', '.join(matched)})." if score == 10 else "Missing network/crypto terms."
    return score, feedback

# 3. Machine Learning (ML) Worklet: Checks model & training logic
def worklet_ml(answer):
    keywords = ["training", "dataset", "overfitting", "model", "features", "loss"]
    matched = [k for k in keywords if k in answer.lower()]
    score = 10 if len(matched) >= 2 else 5
    feedback = f"ML pipeline terms verified ({', '.join(matched)})." if score == 10 else "Missing learning/training terms."
    return score, feedback

# 4. Database Management Systems (DBMS) Worklet: Checks database & transaction rules
def worklet_dbms(answer):
    keywords = ["table", "primary key", "sql", "acid", "normalization", "query"]
    matched = [k for k in keywords if k in answer.lower()]
    score = 10 if len(matched) >= 2 else 5
    feedback = f"Relational terms verified ({', '.join(matched)})." if score == 10 else "Missing database terms."
    return score, feedback

if __name__ == "__main__":
    print("=" * 60)
    print("Lab 13: Domain-Specific Evaluation Worklets (CS & AI)")
    print("=" * 60)

    # 1. Agentic AI
    ans_ai = "An autonomous agent uses tools and persistent memory."
    s_ai, f_ai = worklet_agentic_ai(ans_ai)
    print(f"\n[1. Agentic AI Worklet (AGI301)]")
    print(f" -> Question: What is an AI Agent?")
    print(f" -> Student Answer: '{ans_ai}'")
    print(f" -> Marks: {s_ai}/10 | Feedback: {f_ai}")

    # 2. Computer Networks & Security
    ans_cns = "HTTPS provides secure communication using encryption protocols."
    s_cns, f_cns = worklet_cns(ans_cns)
    print(f"\n[2. CNS Worklet (CNS302)]")
    print(f" -> Question: What is HTTPS?")
    print(f" -> Student Answer: '{ans_cns}'")
    print(f" -> Marks: {s_cns}/10 | Feedback: {f_cns}")

    # 3. Machine Learning
    ans_ml = "Overfitting occurs when the model memorizes the training dataset."
    s_ml, f_ml = worklet_ml(ans_ml)
    print(f"\n[3. Machine Learning Worklet (ML303)]")
    print(f" -> Question: Explain overfitting.")
    print(f" -> Student Answer: '{ans_ml}'")
    print(f" -> Marks: {s_ml}/10 | Feedback: {f_ml}")

    # 4. Database Management Systems
    ans_db = "A primary key uniquely identifies rows in a table."
    s_db, f_db = worklet_dbms(ans_db)
    print(f"\n[4. DBMS Worklet (DBMS304)]")
    print(f" -> Question: What is a primary key?")
    print(f" -> Student Answer: '{ans_db}'")
    print(f" -> Marks: {s_db}/10 | Feedback: {f_db}")

    print("\n" + "=" * 60)
    print("All 4 Computer Science domain worklets evaluated successfully!")
    print("=" * 60)
