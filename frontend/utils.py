import os
import re
from datetime import date
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz  # To perform similarity matching on job titles
import base64

# Function for similarity matching (Fuzzy matching for job titles)
def filter_similar_jobs(available_jobs, job_title_input):
    # Filter jobs based on fuzzy matching of job titles
    def get_similarity_score(job_title):
        return fuzz.ratio(job_title.lower(), job_title_input.lower())
    
    available_jobs['similarity_score'] = available_jobs['job_title'].apply(get_similarity_score)
    filtered_jobs = available_jobs[available_jobs['similarity_score'] > 50]  # Only show jobs with similarity score > 50
    return filtered_jobs.sort_values(by='similarity_score', ascending=False)  # Sort by similarity score

# Function to validate email
def is_valid_email(email: str) -> bool:
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email) is not None

# Function to encode file content to Base64
def encode_file_to_base64(file_content: str) -> str:
    return base64.b64encode(file_content).decode("utf-8")
