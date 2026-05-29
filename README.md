# Phishing Simulator

A full-stack phishing simulation and security awareness training tool built as a Final Year Project. Uses AI-generated phishing templates for red-team training exercises.

## Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** Jinja2 Templates, Tailwind CSS (CDN)
- **Database:** SQLite via SQLAlchemy
- **AI Integration:** Groq API (llama-3.3-70b) for realistic phishing email generation
- **Environment:** Python 3.14+

## Features

- **Target Management** – Add and manage phishing simulation targets
- **AI Template Generation** – Generate realistic phishing email templates from any theme using Groq AI
- **Campaign Launch** – Pair targets with templates and launch campaigns
- **Tracking & Analytics** – Track clicks, IPs, user agents for each campaign
- **Educational Feedback** – Redirects to a page highlighting red flags in the phishing email

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your GROQ_API_KEY to .env

# Run the app
python main.py
```

Visit `http://localhost:8000` in your browser.

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key for Groq AI |
| `DATABASE_URL` | Database connection URL (default: sqlite:///./phishing_sim.db) |

## Project Structure

```
├── main.py                 # FastAPI app & routing
├── database.py             # SQLAlchemy models
├── ai_utils.py             # Groq AI integration
├── templates/              # Jinja2 HTML templates
│   ├── layout.html
│   ├── dashboard.html
│   ├── targets.html
│   ├── templates.html
│   ├── campaigns.html
│   └── success.html
├── static/                 # Static assets
├── requirements.txt
└── .env                    # (ignored)
```
