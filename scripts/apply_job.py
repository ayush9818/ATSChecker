import requests

def apply_for_job(api_url, user_id, job_id, resume_id):

    url = f"{api_url}/apply"

    payload = {
        "user_id": user_id,
        "job_id": job_id,
        "resume_id": resume_id
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            print("Application submitted successfully.")
            print("Response:", response.json())
        elif response.status_code == 400:
            print("Failed to apply:", response.json().get("detail"))
        else:
            print(f"Unexpected error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


api_url = "http://127.0.0.1:8000/jobs/"
user_id = 1
job_id = 1
resume_id = 1

apply_for_job(api_url, user_id, job_id, resume_id)
