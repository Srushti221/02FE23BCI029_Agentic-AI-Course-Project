# Run the dashboard (VS Code)
1. File > Open Folder > select `exam_system_agent`
2. Terminal > New Terminal, then:
   python -m venv venv
   venv\Scripts\activate        (Windows)   |   source venv/bin/activate   (Mac/Linux)
   pip install -r requirements.txt
   python app.py
3. Open http://127.0.0.1:5000

Or press F5 (Run Exam Dashboard) after installing flask.
