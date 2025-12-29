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
-   **Framework**: HTTP Server (for local dev) / Vercel Serverless Functions (for deployment)
-   **Database**: In-memory store (for demo/local use)
-   **AI Integration**: Google Gemini API (for template generation)

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

1.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    ```
2.  Activate the virtual environment:
    -   Windows: `venv\Scripts\activate`
    -   Mac/Linux: `source venv/bin/activate`
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Set up environment variables:
    -   Create a `.env` file in the root directory.
    -   Add your Gemini API key:
      ```
      GEMINI_API_KEY=your_gemini_api_key_here
      ```
    -   Get your API key from: https://makersuite.google.com/app/apikey
5.  Start the development server:
    ```bash
    python dev_server.py
    ```
    The backend will run on `http://localhost:3000`

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

1.  Start the backend server (in the root directory):
    ```bash
    python dev_server.py
    ```

2.  Start the frontend (in a new terminal, navigate to frontend directory):
    ```bash
    cd frontend
    npm run dev
    ```

3.  Open your browser and navigate to the frontend URL (usually `http://localhost:5173`).

4.  Use the **Dashboard** to view active campaigns.

5.  Go to **Templates** to generate AI-powered email templates (requires GEMINI_API_KEY).

6.  Go to **Targets** to add employees/targets for simulations.

7.  Launch a new simulation via the **Campaign Manager**.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
