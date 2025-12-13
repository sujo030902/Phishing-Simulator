# Phishing Simulator Deployment Guide

This guide will walk you through deploying your **Backend to Render** and your **Frontend to Vercel**.

## Phase 1: Deploy Backend (Render)

1.  **Sign Up/Login**: Go to [render.com](https://render.com) and log in with your GitHub account.
2.  **Create New Service**:
    *   Click the **New +** button.
    *   Select **Web Service**.
3.  **Connect Repository**:
    *   Find `Phishing-Simulator` in the list and click **Connect**.
4.  **Configure Settings**:
    *   **Name**: `phishing-simulator-backend` (or similar).
    *   **Region**: Choose the one closest to you (e.g., `Singapore`, `Frankfurt`, `Ohio`).
    *   **Branch**: `main`.
    *   **Root Directory**: `backend` (This is important! Type `backend`).
    *   **Runtime**: `Python 3`.
    *   **Build Command**: `pip install -r requirements.txt`.
    *   **Start Command**: `gunicorn "app:create_app()"`.
    *   **Instance Type**: `Free`.
5.  **Environment Variables**:
    *   Scroll down to "Environment Variables" and click **Add Environment Variable**.
    *   Add the following:
        *   `GROQ_API_KEY`: `your_actual_groq_api_key`
        *   `SECRET_KEY`: `generate_a_random_secure_string`
        *   `PYTHON_VERSION`: `3.10.0` (Recommended)
6.  **Deploy**:
    *   Click **Create Web Service**.
    *   Wait for the deployment to finish. You should see "Your service is live".
    *   **Copy your Backend URL**: It will look like `https://phishing-simulator-backend.onrender.com`.

### ⚠️ Important Note on Database
On the **Free Tier**, Render's disk is ephemeral. This means **if the server restarts (which happens on free tier), your SQLite database will be wiped**.
*   **For persistent data**: You should create a **PostgreSQL** database on Render (New + -> PostgreSQL) and add its `Internal Connection URL` as the `DATABASE_URL` environment variable in your Web Service.

## Phase 2: Deploy Frontend (Vercel)

1.  **Sign Up/Login**: Go to [vercel.com](https://vercel.com) and log in with GitHub.
2.  **Add New Project**:
    *   Click **Add New...** -> **Project**.
    *   Import `Phishing-Simulator`.
3.  **Configure Project**:
    *   **Framework Preset**: Vite (should be auto-detected).
    *   **Root Directory**: Answer `Edit` and select `frontend`.
4.  **Environment Variables**:
    *   Expand the "Environment Variables" section.
    *   Key: `VITE_API_URL`
    *   Value: `https://YOUR_BACKEND_URL.onrender.com/api` (Make sure to include `/api` at the end!)
5.  **Deploy**:
    *   Click **Deploy**.
    *   Wait for it to build and complete.

## Phase 3: Connect & Test

1.  Once Vercel is live, open your new App URL.
2.  Try to generate a template or view the dashboard.
3.  If it fails, check the **Inspect Element -> Console** for CORS errors or network failures.
