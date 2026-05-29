# PhishSim: Phishing Simulator & Security Training Tool

This is a full-stack Phishing Simulator developed as a Final Year Project. It uses FastAPI for the backend, SQLAlchemy with SQLite for data persistence, and the Google Gemini AI API for generating realistic phishing templates.

## 🏗️ Architecture & Tech Stack
- **Backend:** FastAPI (Python 3.14+)
- **Frontend:** Jinja2 Templates, Tailwind CSS (CDN), FontAwesome
- **Database:** SQLite (`phishing_sim.db`)
- **AI Integration:** `google-genai` (Gemini 2.0 Flash) with a robust error-handling fallback.
- **Environment:** Python Virtual Environment in `./venv`.

## 📂 Key Files
- `main.py`: Core application logic, routing, and tracking endpoints.
- `database.py`: SQLAlchemy models (Target, Template, Campaign, Click).
- `ai_utils.py`: Gemini AI client and HTML template generation logic.
- `templates/`: HTML views for Dashboard, Targets, Campaigns, and Feedback.
- `.env`: (Ignored) Stores `GEMINI_API_KEY` and `DATABASE_URL`.

## 🛠️ Workflows
1. **Target Management:** Add recipient emails via the Targets tab.
2. **AI Template Generation:** Enter a theme (e.g., "PayPal Alert") in the Templates tab to generate a styled HTML email using AI.
3. **Campaign Launch:** Pair a Target with a Template.
4. **Simulation/Inbox View:** Use the "View Inbox" feature in the Campaigns tab to preview the email and click the simulated link.
5. **Educational Feedback:** Clicking a tracking link redirects the user to `success.html`, which provides an interactive analysis of the phishing attempt.

## 🛡️ Mandates & Security
- **API Key Protection:** NEVER commit the `.env` file. It contains the Gemini API key.
- **Tracking:** The `/track/{campaign_id}` route logs basic click metadata (IP, User-Agent) before redirecting to the educational page.

## 🚀 Roadmap / Pending Tasks
- [ ] Implement actual SMTP email sending (currently simulated via "View Inbox").
- [ ] Add CSV export for campaign results on the Dashboard.
- [ ] Implement User Authentication (Admin Login) for the simulator dashboard.
- [ ] Add more granular "Red Flag" highlights on the feedback page based on template type.

## 📝 Resuming Work
When starting a new session, run:
`cd /home/saket/Documents/Final_Year_project && ./venv/bin/python main.py`
