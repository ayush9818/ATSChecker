# Backend Setup Guide for ATSChecker



**1. Clone the Repository**

```bash
git clone https://github.com/ayush9818/ATSChecker.git
cd ATSChecker/backend
```

**2. Build the Docker Image**
```bash
docker build -f Dockerfile -t ats_app_backend .
```

**3. Configure Environment Variables**

- Copy the environment variable template:
    ```bash
    cp env_template .env
    ```
- Open the `.env` file and configure the following variables:
   - **GEMINI_API_KEY**: Obtain a Gemini API key from the [Gemini API Documentation](https://ai.google.dev/gemini-api/docs/api-key) and add it here.
   - **DATABASE_URI**: Use SQLite for local testing:
     ```plaintext
     sqlite:////home/data/job_portal.db
     ```
   - **BUCKET_NAME**: Specify the S3 bucket name where resumes and other files will be stored.
   - **BUCKET_DIR**: Specify the directory path within the S3 bucket for uploading files.

**4. Run the Docker Container**

Run the backend service in a containerized environment:
```bash
docker run -it --env-file $(pwd)/.env -v $(pwd)/db:/home/data -p 8000:8000 ats_app_backend
```

**5. Push docker image to ECR**

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 911167903346.dkr.ecr.us-east-1.amazonaws.com

docker tag ats_app_backend:latest 911167903346.dkr.ecr.us-east-1.amazonaws.com/ats-app-backend:latest

docker push 911167903346.dkr.ecr.us-east-1.amazonaws.com/ats-app-backend:latest
```



**6. Create Dummy Data (Optional)**

To populate the database with sample data, run the following scripts:
```bash
cd ATSChecker/
python scripts/create_users.py
python scripts/create_jobs.py
python scripts/upload_resume.py
```

