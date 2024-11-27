import requests
import json


class APIHandler:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, api_url, params):
        url = self.base_url + api_url
        print(f"API URL : {url}")
        
        response = requests.get(url, params=params)

        response.raise_for_status()  # Raise an exception for any HTTP error status codes
        
        data = response.json()
        if isinstance(data, dict) and "data" in data:
            # If response contains a "data" key, return the nested data
            return data["data"]
        elif isinstance(data, list):
            # If response is already a list, return it directly
            return data
        else:
            # Handle unexpected response format
            print("Unexpected response format:", data)
            return []
    

    def post(self, api_url, data):
        url = self.base_url + api_url
        # Convert the dictionary to JSON format
        json_data = json.dumps(data)
        # Set the appropriate headers for your request
        headers = {"Content-Type": "application/json"}
        # Make a POST request to the API endpoint
      
        response = requests.post(url, data=json_data, headers=headers)
        return response