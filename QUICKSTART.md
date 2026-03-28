# 🚀 Quick Start Guide - New Features

## Installation

All new files are already in place:

```
agents/
  ├── followup_agent.py       ✅ NEW
  └── deadline_agent.py       ✅ NEW

services/
  └── email_service.py        ✅ NEW

app.py                         ✅ UPDATED
FEATURES_DOCUMENTATION.md      ✅ NEW (this file)
```

## Environment Setup (Optional - Only for Email Feature)

### For Gmail Users:

1. **Generate App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Generate and copy the 16-character password

2. **Set Environment Variables:**

   **Windows (Command Prompt):**
   ```cmd
   set EMAIL_USER=your.email@gmail.com
   set EMAIL_PASS=xxxxxxxxxxxxxxxx
   ```

   **Windows (PowerShell):**
   ```powershell
   $env:EMAIL_USER="your.email@gmail.com"
   $env:EMAIL_PASS="xxxxxxxxxxxxxxxx"
   ```

   **Mac/Linux:**
   ```bash
   export EMAIL_USER="your.email@gmail.com"
   export EMAIL_PASS="xxxxxxxxxxxxxxxx"
   ```

3. **Or Create .env file:**
   ```
   EMAIL_USER=your.email@gmail.com
   EMAIL_PASS=xxxxxxxxxxxxxxxx
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   ```

### For Other Email Providers:

| Provider | SMTP Server | Port |
|----------|-------------|------|
| Gmail | smtp.gmail.com | 587 |
| Outlook | smtp-mail.outlook.com | 587 |
| Yahoo | smtp.mail.yahoo.com | 587 |
| SendGrid | smtp.sendgrid.net | 587 |

## Running the Application

```bash
streamlit run app.py
```

## Using the New Features

### Feature 1: Follow-up Generator
✅ **Works immediately** - No setup required!

**How to use:**
1. Navigate to Dashboard
2. Expand any task's "Follow-up & Email Options"
3. Select from 3 tabs:
   - 📍 Reminder
   - ⚠️ Escalation  
   - 💼 Professional Follow-up
4. Copy text as needed

### Feature 2: Email Sending
⚠️ **Requires setup** - Configure email first

**How to use:**
1. Set EMAIL_USER and EMAIL_PASS environment variables
2. In task expander, scroll to "Email Reminder" section
3. Enter recipient email
4. Select message type
5. Click "Send Email"
6. Check confirmation

### Feature 3: Deadline Intelligence  
✅ **Works immediately** - No setup required!

**How to use:**
1. Look at task cards on Dashboard
2. Each task shows urgency badge:
   - 🔴 Critical (today/ASAP/overdue)
   - 🟡 Urgent (tomorrow/3 days)
   - 🟢 Normal (next week)
   - ⚪ Low Priority (future/none)
3. Urgency updates automatically based on task deadline

## Testing Without Email

To test the system without email credentials:

1. ✅ **Follow-up messages** - Works fine, try generating them
2. ✅ **Deadline badges** - Works fine, see urgency levels
3. ⚠️ **Email button** - Shows warning if credentials not set

You can skip email setup and use the other 2 features immediately!

## Troubleshooting

### Email Not Sending?

**Problem:** "Email credentials not configured"
- **Solution:** Set EMAIL_USER and EMAIL_PASS environment variables

**Problem:** "SMTP Authentication failed"
- **Solution:** 
  - Check correct email/password
  - For Gmail, use app password (not regular password)
  - Disable "Less secure app access" on Gmail
  - Check if 2FA is preventing login

**Problem:** Email sends but doesn't arrive
- **Solution:**
  - Check spam/junk folder
  - Verify recipient email is correct
  - Check email provider's rate limits

### Deadline Badge Not Showing?

**Problem:** Urgency badge missing
- **Solution:** Ensure task has a deadline field

**Problem:** Wrong urgency level
- **Solution:** Check deadline format matches supported patterns:
  - ✅ "Today", "Tomorrow", "Next week", "ASAP"
  - ✅ "12/25/2024", "2024-12-25"
  - ✅ "Within 3 days", "End of month"

### Follow-up Messages Not Generating?

**Problem:** Empty message areas
- **Solution:** 
  - Restart app: `streamlit run app.py`
  - Check Python console for errors
  - Ensure task has title/description

## File Summary

| File | Purpose | Status |
|------|---------|--------|
| `agents/followup_agent.py` | Generate follow-up messages | ✅ Ready |
| `agents/deadline_agent.py` | Analyze deadline urgency | ✅ Ready |
| `services/email_service.py` | Send reminder emails | ✅ Ready (needs credentials) |
| `app.py` | Main Streamlit app | ✅ Updated |

## Next Steps

1. ✅ All features installed
2. ✅ Try follow-ups and deadline features immediately
3. ⏳ (Optional) Configure email when ready
4. 📖 Read FEATURES_DOCUMENTATION.md for details

## Questions?

- Check FEATURES_DOCUMENTATION.md for detailed explanations
- Review app.py code around line 750+ for UI implementation
- Check agents/ and services/ files for backend logic

---

**Ready to go!** 🎉 Start extracting tasks and using the new intelligent workflow features!
