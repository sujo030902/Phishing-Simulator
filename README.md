# Phishing Simulator

A comprehensive phishing simulation platform designed to help organizations test and improve their security posture. This application allows you to create, manage, and analyze phishing campaigns to educate users about email security risks.

## Features

-   **Dashboard Analytics**: Real-time tracking of campaign statistics (Opened, Clicked, Compromised).
-   **Campaign Management**: Create and schedule phishing simulation campaigns using the `CampaignManager`.
-   **AI-Powered Template Generation**: Generate realistic phishing email templates using AI (via Groq/Gemini) with the `TemplateGenerator`.
-   **Target Management**: Easily add and manage target email lists.
-   **Email Tracking**: Track user interactions with simulated phishing emails.

## Tech Stack

### Backend
-   **Language**: Python
-   **Framework**: Flask (inferred from `app.py`)
-   **Database**: SQLite/SQLAlchemy (inferred from `models.py`)
-   **AI Integration**: Groq API / Google Gemini (for template generation)

### Frontend
-   **Framework**: React (Vite)
-   **Styling**: Tailwind CSS
-   **State Management**: React Hooks

## Setup & Installation

### Prerequisites
-   Node.js (v16+)
-   Python (v3.8+)
-   Git

### Backend Setup

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    ```
3.  Activate the virtual environment:
    -   Windows: `venv\Scripts\activate`
    -   Mac/Linux: `source venv/bin/activate`
4.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5.  Set up environment variables:
    -   Create a `.env` file in the `backend` directory.
    -   Add necessary keys (e.g., `GROQ_API_KEY`, `DATABASE_URL`, `SECRET_KEY`).
6.  Initialize the database:
    ```bash
    python init_db.py
    ```
7.  Start the server:
    ```bash
    python app.py
    ```

### Frontend Setup

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```

## Usage

1.  Open your browser and navigate to the frontend URL (usually `http://localhost:5173`).
2.  Use the **Dashboard** to view active campaigns.
3.  Go to **Templates** to generate or create new email templates.
4.  Launch a new simulation via the **Campaign Manager**.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
