import requests
from faker import Faker

fake = Faker()

API_URL = "http://0.0.0.0:8000/users/"

def create_random_user():
    user_data = {
        "name": fake.name(),
        "email": fake.email(),
        "contact_number": fake.phone_number()
    }
    return user_data

def create_users(num_users=10):
    for i in range(num_users):
        user_data = create_random_user()
        response = requests.post(API_URL, json=user_data)
        if response.status_code == 200 or response.status_code == 201:
            print(f"User {i+1} created successfully: {response.json()}")
        else:
            print(f"Failed to create User {i+1}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    num_users = 10 
    create_users(num_users)
