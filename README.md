EGG-AI-Predict
# Flask ML Web Application

A full-stack web application built with Flask, integrated with Machine Learning & Deep Learning models (TensorFlow, Scikit-Learn), and deployed on Render.

## 📌 Project Overview

This project provides a web-based interface for interactive data visualization, user authentication, and real-time machine learning predictions. It connects a Flask backend with database management (Flask-SQLAlchemy) and interactive frontend data reporting (Plotly).

### Key Features
- Authentication System: Secure user login and registration powered by Flask-Login.
- Database Integration: Managed data models with Flask-SQLAlchemy and ORM mappings.
- Interactive Data Visualization: Data analytics dashboards rendered with Plotly.
- ML/DL Inference: Machine learning model integration using TensorFlow, scikit-learn, pandas, and numpy.
- Production Deployment: Production-ready deployment setup using Gunicorn on Render.

---

## 🛠️ Tech Stack & Dependencies

- Backend Framework: Python 3.11, Flask, Werkzeug
- Database & Auth: Flask-SQLAlchemy, Flask-Login, SQLAlchemy
- Data Processing & ML: TensorFlow, Scikit-Learn, Pandas, NumPy, SciPy
- Data Visualization: Plotly
- Production Server: Gunicorn
- Deployment Platform: Render

---

## 🚀 What We Accomplished (Engineering & Deployment)

1. Resolved Python & Dependency Conflicts:
   - Fixed build failures caused by incompatible version locks (tensorflow, sqlalchemy) across Python minor versions.
   - Standardized the environment on Python 3.11.9.
2. Clean Dependency Management:
   - Replaced rigid pip freeze dependency locks with a clean, flexible Requirement.txt configuration to ensure seamless cross-platform builds.
3. Render Deployment Pipeline Setup:
   - Configured the PYTHON_VERSION environment variable on Render to enforce Python 3.11 compatibility.
   - Configured Gunicorn as the WSGI server (gunicorn app:app) for handling web concurrency.

---

## 📁 Project Structure

├── app.py              # Main Flask application & route declarations
├── models.py           # Database models & ORM configuration
├── Requirement.txt     # Clean dependency list for Render builds
├── static/             # CSS, JavaScript, and static assets
├── templates/          # HTML templates (Jinja2)
└── README.md           # Project documentation

---

## 💻 Local Development Setup

### 1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

### 2. Set Up a Virtual Environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

### 3. Install Dependencies
pip install -r Requirement.txt

### 4. Run the Application
python app.py

Open your browser and navigate to http://127.0.0.1:5000.

---

## ☁️ Deployment on Render

1. Connect your GitHub repository to Render.
2. Create a new Web Service.
3. Set the build parameters:
   - Environment: Python 3
   - Build Command: pip install -r Requirement.txt
   - Start Command: gunicorn app:app
4. Add Environment Variable:
   - Key: PYTHON_VERSION
   - Value: 3.11.9
5. Click Deploy.
