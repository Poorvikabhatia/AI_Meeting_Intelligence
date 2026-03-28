# 🧠 AI Meeting Intelligence System

## 📌 Overview
AI Meeting Intelligence System is an AI-powered application that converts unstructured meeting conversations into clear, actionable tasks.

It automatically extracts tasks, identifies owners, assigns priorities, and helps teams track progress — improving productivity and ensuring no task is missed.

---

## 🎯 Problem Statement
In most organizations:
- Meetings generate multiple tasks and decisions
- Tasks are often not properly documented
- Lack of ownership leads to missed deadlines
- No structured system exists for tracking tasks

This results in confusion, inefficiency, and reduced productivity.

---

## 💡 Proposed Solution
This system uses AI to transform meeting conversations into structured workflows by:
- Extracting all actionable tasks
- Identifying task owners
- Detecting deadlines
- Assigning priorities
- Providing a centralized dashboard for tracking

---

## ⚙️ Key Features
- AI-based task extraction from natural language  
- Automatic detection of owner and deadline  
- Task Manager with status tracking  
- Dashboard with real-time insights  
- Audit logs for transparency and traceability  
- Clean, interactive, and user-friendly interface  

---

## 🧠 System Architecture

Meeting Transcript  
        ↓  
AI Model (LLM via Groq)  
        ↓  
Task Extraction Engine  
        ↓  
Task Manager  
        ↓  
Dashboard & Insights  

---

## 🛠 Tech Stack
- Python  
- Streamlit  
- Groq API (LLM)  
- JSON (for data storage)  

---

## 🚀 How to Run Locally

1. Clone the repository
   ```bash
   git clone https://github.com/Poorvikabhatia/AI-Meeting-Intelligence.git  
   ```

2. Navigate to the project folder
   ```bash
   cd AI-Meeting-Intelligence
   ```

3. Create a virtual environment
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment
   ```bash
   venv\Scripts\activate
   ```

5. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

7. Create a .env file and add your API key
   ```bash
   GROQ_API_KEY=your_api_key_here
   ```

9. Run the application
   ```bash
   streamlit run app.py
   ```

10. Open in browser
    ```bash
    http://localhost:8501
    ```   

---

## 📊 Impact
- Saves time spent on manual task tracking  
- Improves team productivity  
- Ensures no task is missed  
- Enhances accountability across teams  

---

## 🔮 Future Scope
- Integration with Slack, Email, and Calendar  
- Real-time speech-to-text meeting processing  
- Automated reminders and notifications  
- Advanced analytics and reporting  

---

## 🎥 Demo
This project demonstrates how AI can convert meeting conversations into structured and trackable workflows.

---

## 📌 Note
This project is developed as part of a hackathon to showcase the potential of AI in automating enterprise workflows.

---
