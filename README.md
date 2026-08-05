================================================================================
          ELECTROGASTROGRAPHY (EGG) AI CLINICAL ANALYSIS SYSTEM
================================================================================

An EHR-integrated web application powered by Flask, Distilled ML Models, and 
Chart.js. The platform enables clinicians to ingest, analyze, and visualize 
continuous Electrogastrography (EGG) time-series datasets, generating diagnostic 
risk assessments and SHAP-based feature interpretability in real time.


--------------------------------------------------------------------------------
1. KEY FEATURES
--------------------------------------------------------------------------------
* Patient EHR Metadata Management: Capture patient vitals, ID, hospital 
  reference numbers, and current medication statuses.
* Continuous EGG Stream Processing: Ingest continuous single-channel EGG 
  microvolt (mV) signals via .csv or .xlsx format.
* Spectral Analysis & Feature Extraction: Automatic calculation of key 
  gastrointestinal spectral metrics:
  - Bradygastria Power (1.0 - 2.5 CPM)
  - Normogastria Power (2.5 - 3.75 CPM)
  - Tachygastria Power (3.75 - 10.0 CPM)
  - Dominant Frequency (CPM)
* Distilled AI Inference: Machine learning classification across risk tiers 
  (Healthy, Early, Moderate, High Risk) with confidence scoring and automated 
  clinical recommendations.
* Interactive Signal Visualization: Real-time client-side rendering of raw 
  time-series microvolt signals using Chart.js.
* SHAP Interpretability Integration: Direct access to feature impact 
  explanations (SHAP) for transparent clinical decision support.


--------------------------------------------------------------------------------
2. SYSTEM ARCHITECTURE
--------------------------------------------------------------------------------
egg-ai-analysis/
├── app.py                     # Main Flask Application (Routes, Models & ML Engine)
├── requirements.txt           # Python Package Dependencies
├── Procfile                   # Gunicorn Entry Point for Render
├── runtime.txt                # Python Engine Version (e.g., python-3.10.12)
├── render.yaml                # Optional Infrastructure-as-Code for Render
├── uploads/                   # Temporary directory for EGG dataset ingestion
├── static/
│   ├── css/                   # Stylesheets & EHR Bootstrap components
│   └── js/                    # Chart.js scripts & UI logic
└── templates/
    ├── base.html              # Core Layout & Shell
    ├── upload.html            # Patient EHR & Interactive Waveform View
    └── explainability.html    # SHAP Diagnostic Interpretability View


--------------------------------------------------------------------------------
3. LOCAL SETUP & DEVELOPMENT
--------------------------------------------------------------------------------

3.1 Prerequisites
Ensure you have Python 3.10+ and Git installed.

3.2 Installation Steps
1. Clone the repository:
   git clone https://github.com/your-username/egg-ai-analysis.git
   cd egg-ai-analysis

2. Create and activate a virtual environment:
   # On macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate

   # On Windows:
   python -m venv venv
   venv\Scripts\activate

3. Install required packages:
   pip install -r requirements.txt

3.3 Key Dependencies
Ensure your requirements.txt contains:
   Flask>=3.0.0
   Flask-SQLAlchemy>=3.1.0
   Flask-Login>=0.6.3
   gunicorn>=21.2.0
   pandas>=2.1.0
   numpy>=1.26.0
   scikit-learn>=1.3.0
   shap>=0.44.0
   openpyxl>=3.1.0
   psycopg2-binary>=2.9.0

3.4 Launch Application Locally
1. Initialize SQLite local database:
   python -c "from app import db, app; app.app_context(); db.create_all()"

2. Launch Flask Development Server:
   python app.py

Access the application in your browser at: http://127.0.0.1:5000/


--------------------------------------------------------------------------------
4. DEPLOYING ON RENDER
--------------------------------------------------------------------------------

Step 1: Prepare Repository Files
Ensure the following files are committed to your GitHub repository:

1. Procfile (no file extension):
   web: gunicorn app:app --workers 2 --threads 4 --timeout 120

2. runtime.txt:
   python-3.10.12

Step 2: Create a PostgreSQL Database on Render
1. Log in to your Render Dashboard (https://dashboard.render.com/).
2. Click New + -> PostgreSQL.
3. Set the Name (e.g., egg-db) and Region.
4. Select the Free tier and click Create Database.
5. Copy the Internal Database URL (or External URL) once created.

Step 3: Deploy the Web Service
1. In the Render Dashboard, click New + -> Web Service.
2. Connect your GitHub repository.
3. Set configuration options:
   - Name: egg-ai-clinical
   - Environment: Python 3
   - Region: Select the same region as your database
   - Branch: main (or master)
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app

Step 4: Configure Environment Variables
Under the Environment tab of your Render Web Service, add the following:

   KEY              VALUE / DESCRIPTION
   -----------------------------------------------------------------------------
   FLASK_ENV        production
   SECRET_KEY       [Generate a random 32-character secret string]
   DATABASE_URL     [Paste your Render PostgreSQL URL; change prefix 
                    postgres:// to postgresql:// if required]
   PYTHON_VERSION   3.10.12

Step 5: Initialize Production Database
To create database tables on Render PostgreSQL:
1. Go to your Web Service in Render.
2. Open the Shell tab on the left sidebar.
3. Run:
   python -c "from app import db, app; app.app_context(); db.create_all()"


--------------------------------------------------------------------------------
5. DATASET INGESTION FORMAT
--------------------------------------------------------------------------------
When uploading EGG recordings (.csv or .xlsx), ensure the file contains a 
continuous time-series vector of voltage readings (mV) in the first column:

Amplitude_mV
0.045
0.048
0.052
0.041
...


--------------------------------------------------------------------------------
6. EXCEPTION SAFEGUARDS & ARCHITECTURE NOTES
--------------------------------------------------------------------------------
* Clean UTF-8 Byte Encoding: All HTML/Jinja template files have been sanitized 
  of invisible non-breaking space bytes (\u00A0) to prevent parser crashes.
* Defensive Jinja Templating: Dynamic lookup attributes 
  (patient.full_name if patient else 'N/A') prevent unhandled 500 runtime 
  UndefinedError exceptions.
* Safe Script Data Injection: Signal vectors use {{ raw_signal | tojson | safe }} 
  to inject valid JavaScript arrays into Chart.js elements without entity 
  encoding issues.


--------------------------------------------------------------------------------
7. LICENSE
--------------------------------------------------------------------------------
This project is licensed under the MIT License.
================================================================================
