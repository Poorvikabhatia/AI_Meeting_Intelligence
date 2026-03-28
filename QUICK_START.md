# 🚀 Quick Start Guide

Get the AI Meeting Intelligence System running in 5 minutes!

## Step 1: Get Your Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Create a new API key
4. Copy it

## Step 2: Configure Environment

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_api_key_here
```

## Step 3: Install Dependencies

```bash
cd d:\python\AI_Meeting_Intelligence
pip install -r requirements.txt
```

## Step 4: Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🎯 Try It Out

### Option A: Load Demo Data
1. Click **"📚 Load Demo Data"** on the Home page
2. Click **"🚀 Generate Tasks"**
3. Watch the AI extract tasks from the demo transcript

### Option B: Use Your Own Transcript
1. Paste your meeting transcript
2. Click **"🚀 Generate Tasks"**
3. Tasks will be extracted and displayed

---

## 📊 Explore the Features

### Dashboard
- View real-time metrics
- See task distribution charts
- Check for escalation alerts

### Task Manager
- Filter tasks by owner or status
- Toggle task completion status
- Delete tasks if needed

### Audit Logs
- View all system activities
- See when tasks were created/updated
- Export logs as JSON or CSV

---

## ❓ Common Issues

### "GROQ_API_KEY not found"
→ Make sure `.env` file has your API key

### "No module named 'groq'"
→ Run `pip install -r requirements.txt` again

### "Port 8501 already in use"
→ Run `streamlit run app.py --server.port 8502`

---

## 💡 Pro Tips

1. **Demo Data**: Use the demo button first to understand the system
2. **Batch Processing**: Process multiple transcripts to build up tasks
3. **Task Filtering**: Use filters to focus on specific owners or statuses
4. **Audit Trail**: Always export logs for compliance and tracking
5. **Error Handling**: The system gracefully falls back to mock data if API fails

---

## 📈 Next Steps

- Customize the task extraction prompts
- Add more demo data
- Integrate with your calendar system
- Set up email notifications
- Connect to a database for persistent storage

---

**Happy task managing! 🎉**
