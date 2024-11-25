# Frontend Setup Guide for ATSChecker



**1. Clone the Repository**

```bash
git clone https://github.com/ayush9818/ATSChecker.git
cd ATSChecker/frontend
```

**2. Build the Docker Image**
```bash
docker build -f Dockerfile -t ats_app_frontend .
```

**3. Configure Environment Variables**

- Copy the environment variable template:
    ```bash
    cp env_template .env
    ```
- Open the `.env` file and configure the following variables:
   - **BASE_API**: Specify the base URL of the backend API that the application will interact with.

**4. Run the Docker Container**

Run the backend service in a containerized environment:
```bash
docker run -it --env-file $(pwd)/.env -v $(pwd)/db:/home/data -p 8000:8000 ats_app_frontend
```