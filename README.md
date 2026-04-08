# AI Job Application Tracker

I found the process of tracking sent applications, updating statuses, and managing follow-ups was error-prone and tedious to maintain. This is an AI-driven workflow that eliminates that friction.

## How It Works

**Job Intake**
A web-based tool built with Flask where you input a job posting. OpenAI's GPT-4o mini parses the raw text into structured data — company, role, location, salary, and key requirements — and automatically logs it into a Google Sheet.

**Email Monitoring**
Incoming emails are processed on an hourly basis using Google Cloud Scheduler and Cloud Functions. GPT-4o mini classifies each email into categories such as rejections, interview requests, or assessments. Based on that classification, the system updates the application status in the sheet and, when relevant, creates a Google Calendar event for interviews.

What originally took minutes per application with constant manual follow-ups now takes seconds with significantly less cognitive overhead.

## Tech Stack

- **Backend:** Python, Flask
- **AI:** OpenAI GPT-4o mini
- **Google APIs:** Sheets, Gmail, Calendar
- **Infrastructure:** Google Cloud Scheduler, Cloud Functions

## Setup

You'll need your own API keys — this tool does not include any credentials.

- **OpenAI API key** — [platform.openai.com](https://platform.openai.com)
- **Google OAuth credentials** — enable the Gmail, Sheets, and Calendar APIs in [Google Cloud Console](https://console.cloud.google.com) and download a `credentials.json` for a Desktop app

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add a `.env` file with your `OPENAI_API_KEY`
4. Place your `credentials.json` in the project root
5. Run: `python app.py`
6. Open `http://127.0.0.1:5000` — on first run, a browser window will prompt you to authorize Google access

## Sheet Color Legend

Row colors update automatically as application statuses change.

| Color | Status |
|-------|--------|
| 🔵 Light blue | Applied |
| 🟢 Light green | Interview Scheduled |
| 🟡 Light yellow | Online Assessment |
| 🔴 Light pink | Rejected |
| 💚 Mint green | Offer |
