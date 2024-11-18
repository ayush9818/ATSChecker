# ATSChecker

## Project Setup Guide

Follow the steps below to set up and run the **ATSChecker** project:

### 1. Clone the Repository
```bash
git clone https://github.com/ayush9818/ATSChecker.git
cd ATSChecker
```

### 2. Set Up a Virtual Environment
1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```
2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configure Environment Variables
1. Copy the environment variable template:
   ```bash
   cp env_template .env
   ```
2. Open the `.env` file and configure the following variables:
   - **GEMINI_API_KEY**: Obtain a Gemini API key from the [Gemini API Documentation](https://ai.google.dev/gemini-api/docs/api-key) and add it here.
   - **DATABASE_URI**: Specify the database URI. For example:
     - For a remote PostgreSQL database: `postgresql://<user>:<password>@<host>:<port>/<database>`
     - For local testing, use SQLite: `sqlite:///job_portal.db`

### 4. Launch the API Server
Set up the `PYTHONPATH` and run the API server:
```bash
export PYTHONPATH=$(pwd):$PYTHONPATH
python3 ats_app/app.py
```

### 5. Create Dummy Data (Optional)
To populate the database with sample data, run the following scripts:
```bash
python scripts/create_users.py
python scripts/create_jobs.py
```
