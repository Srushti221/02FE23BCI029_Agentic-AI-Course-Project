# Online Course Examination System Agent

A simple web dashboard for managing an online course examination process
using multiple AI agents.

## Features

-   **Overview:** View the examination system summary.
-   **Registration & Eligibility:** Check whether students are eligible
    to take a course exam.
-   **Take Exam:** Start an exam for an eligible student and submit
    answers.
-   **Grades & Publishing:** View draft grades and publish results after
    faculty approval and integrity checks.
-   **Short Answers:** Evaluate descriptive answers with the subjective
    grading agent.
-   **Grievance & Revaluation:** Submit a request to review marks for a
    question.
-   **Agent Audit Log:** View actions performed by the agents, such as
    eligibility checks, exam delivery, grading, publishing, and
    grievance decisions.

## Agents Used

1.  **Registration & Eligibility Agent** -- checks student eligibility.
2.  **Exam Delivery Agent** -- fetches and delivers exam questions.
3.  **Auto-Grading Agent** -- evaluates submitted answers and prepares
    grades.
4.  **Proctoring & Integrity Agent** -- checks exam-session integrity.
5.  **Result Publishing Agent** -- publishes results when the required
    approval and integrity conditions are met.
6.  **Subjective Grading Assist Agent** -- evaluates short-answer
    responses.
7.  **Grievance & Revaluation Agent** -- reviews student requests about
    marks.

## Technologies

-   Python
-   Flask
-   HTML, CSS and JavaScript
-   JSON files for sample student, course and question data

## Requirements

-   Python 3.10 or later
-   pip

## How to Run

1.  Open the project folder in VS Code.

2.  Open a terminal in the project folder.

3.  (Optional) Create and activate a virtual environment:

    ``` bash
    python -m venv venv
    ```

    On Windows:

    ``` bash
    venv\Scripts\activate
    ```

    On macOS/Linux:

    ``` bash
    source venv/bin/activate
    ```

4.  Install the required package:

    ``` bash
    pip install -r requirements.txt
    ```

5.  Start the dashboard:

    ``` bash
    python app.py
    ```

6.  Open this address in your browser:

    **http://127.0.0.1:5000**

## Project Files

-   `app.py` -- Flask application that connects the agents to the web
    dashboard.
-   `main.py` -- command-line demo of the multi-agent examination
    pipeline.
-   `requirements.txt` -- Python package requirements.
-   `agents/` -- agent implementation files.
-   `tools/` -- supporting tools, such as the question fetcher.
-   `data/` -- sample student, course and question data.
-   `templates/` -- dashboard HTML template.

## Note

This project uses sample data for demonstration. The audit log and
published-results collection in the Flask application are stored in
memory, so they are reset when the application restarts.
