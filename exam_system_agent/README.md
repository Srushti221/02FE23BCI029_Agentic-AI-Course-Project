# Online Course Examination System Agent
# Project #7 — KLE Tech Lab Curriculum

A complete multi-agent Python system for managing online exams
from student registration to result publication.

## Run the full demo
```
python main.py
```

## Run individual lab files
```
python labs/lab1_agent_vs_chatbot.py
python labs/lab2_tool_using_agent.py
python labs/lab4_memory_retrieval.py
python labs/lab7_node_graph.py
```

## Project structure
```
exam_system_agent/
├── main.py                        # Full pipeline orchestrator (Lab 14)
├── agents/
│   ├── registration_agent.py      # Agent 1 — Eligibility Check (Lab 1, 2, 4)
│   ├── exam_delivery_agent.py     # Agent 2 — Exam Delivery    (Lab 2, 5, 7)
│   ├── grading_agent.py           # Agent 3 — Auto-Grading     (Lab 2, 8, 11)
│   └── result_publishing_agent.py # Agent 4 — Result Publish   (Lab 7, 12)
├── tools/
│   ├── eligibility_tool.py        # Tool 1 — Eligibility rules engine
│   ├── question_fetcher_tool.py   # Tool 2 — Question bank connector
│   └── grader_tool.py             # Tool 3 — MCQ auto-grader
├── data/
│   ├── students_db.json           # Student records
│   └── question_bank.json         # MCQ question bank
└── labs/
    ├── lab1_agent_vs_chatbot.py
    ├── lab2_tool_using_agent.py
    ├── lab4_memory_retrieval.py
    └── lab7_node_graph.py
```
