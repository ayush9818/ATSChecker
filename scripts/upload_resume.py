import base64
import requests

def encode_file_to_base64(file_path: str) -> str:
    """
    Encodes a file to Base64 format.
    :param file_path: Path to the file to be encoded.
    :return: Base64 encoded string of the file.
    """
    with open(file_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode("utf-8")
    return encoded_string

def upload_resume(file_path: str, user_id: int, api_url: str):
    """
    Uploads the Base64 encoded resume to the API.
    :param file_path: Path to the resume file.
    :param user_id: User ID associated with the resume.
    :param api_url: API endpoint to upload the resume.
    """
    # Encode the file to Base64
    file_name = file_path.split("/")[-1]
    base64_resume = encode_file_to_base64(file_path)

    # Prepare the payload
    payload = {
        "user_id": user_id,
        "resume_body": base64_resume,
        "file_name": file_name
    }

    # Send the request
    response = requests.post(api_url, json=payload)

    # Handle the response
    if response.status_code == 200:
        print("Resume uploaded successfully:", response.json())
    else:
        print("Failed to upload resume:", response.status_code, response.text)

# Example usage
file_path = "sample_data/resume.pdf"
user_id = 1
api_url = "http://127.0.0.1:8000/resume/upload"
upload_resume(file_path, user_id, api_url)
