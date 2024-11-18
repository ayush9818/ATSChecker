import os
import re
from datetime import date
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz  # To perform similarity matching on job titles


# Function for similarity matching (Fuzzy matching for job titles)
def filter_similar_jobs(available_jobs, job_title_input):
    # Filter jobs based on fuzzy matching of job titles
    def get_similarity_score(job_title):
        return fuzz.ratio(job_title.lower(), job_title_input.lower())
    
    available_jobs['similarity_score'] = available_jobs['job_title'].apply(get_similarity_score)
    filtered_jobs = available_jobs[available_jobs['similarity_score'] > 50]  # Only show jobs with similarity score > 50
    return filtered_jobs.sort_values(by='similarity_score', ascending=False)  # Sort by similarity score