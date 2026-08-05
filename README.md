================================================================================
                ELECTROGASTROGRAPHY (EGG) AI CLINICAL ANALYSIS SYSTEM
================================================================================

This is a web application built with Flask that helps healthcare professionals
analyze Electrogastrography (EGG) signals. It allows users to upload EGG data,
view patient information, visualize signals, and receive AI-generated diagnostic
results with explainable predictions.

--------------------------------------------------------------------------------
1. FEATURES
--------------------------------------------------------------------------------

• Patient Information
  - Store patient ID, hospital number, name, age, gender, weight, height,
    and medication status.

• EGG Data Upload
  - Upload EGG signal files in CSV or Excel (.xlsx) format.

• Signal Analysis
  - Automatically extracts important EGG features such as:
      - Bradygastria Power
      - Normogastria Power
      - Tachygastria Power
      - Dominant Frequency (CPM)

• AI Prediction
  - Predicts the patient's risk level:
      - Healthy
      - Early Risk
      - Moderate Risk
      - High Risk
  - Displays prediction confidence and clinical recommendations.

• Signal Visualization
  - Displays the uploaded EGG waveform using Chart.js.

• Explainable AI
  - Shows SHAP explanations to help clinicians understand why the AI made
    a particular prediction.

--------------------------------------------------------------------------------
2. PROJECT STRUCTURE
--------------------------------------------------------------------------------

egg-ai-analysis/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python packages
├── Procfile                # Render deployment file
├── runtime.txt             # Python version
├── uploads/                # Uploaded datasets
│
├── static/
│   ├── css/
│   └── js/
│
└── templates/
    ├── base.html
    ├── upload.html
    └── explainability.html

--------------------------------------------------------------------------------
3. RUNNING THE PROJECT
--------------------------------------------------------------------------------

Step 1: Clone the repository

git clone https://github.com/your-username/egg-ai-analysis.git

cd egg-ai-analysis

Step 2: Create a virtual environment

Linux/macOS

python3 -m venv venv
source venv/bin/activate

Windows

python -m venv venv
venv\Scripts\activate

Step 3: Install dependencies

pip install -r requirements.txt

Step 4: Create the database

python -c "from app import db, app; app.app_context(); db.create_all()"

Step 5: Run the application

python app.py

Open your browser and visit:

http://127.0.0.1:5000

--------------------------------------------------------------------------------
4. REQUIRED PYTHON PACKAGES
--------------------------------------------------------------------------------

Your requirements.txt should include:

Flask
Flask-SQLAlchemy
Flask-Login
pandas
numpy
scikit-learn
shap
openpyxl
gunicorn
psycopg2-binary

--------------------------------------------------------------------------------
5. DEPLOYING TO RENDER
--------------------------------------------------------------------------------

1. Push your project to GitHub.

2. Create a PostgreSQL database on Render.

3. Create a new Python Web Service.

4. Set the following commands:

Build Command

pip install -r requirements.txt

Start Command

gunicorn app:app

5. Add the following environment variables:

FLASK_ENV=production

SECRET_KEY=your_secret_key

DATABASE_URL=your_render_database_url

PYTHON_VERSION=3.10.12

6. Create the database tables

python -c "from app import db, app; app.app_context(); db.create_all()"

--------------------------------------------------------------------------------
6. DATA FORMAT
--------------------------------------------------------------------------------

The uploaded CSV or Excel file should contain one column of EGG signal values.

Example:

Amplitude_mV

0.045

0.048

0.052

0.041

...

--------------------------------------------------------------------------------
7. TECHNOLOGIES USED
--------------------------------------------------------------------------------

• Python
• Flask
• SQLite / PostgreSQL
• Pandas
• NumPy
• Scikit-learn
• SHAP
• Chart.js
• Bootstrap 5

--------------------------------------------------------------------------------
8. LICENSE
--------------------------------------------------------------------------------

This project is released under the MIT License.

================================================================================
