"""
Author: Ayush Agarwal
"""

entity_extraction_prompt = """
You are a resume parsing assistant. 
Given the following resume text, extract all the important details like name, contact information/email,
education, work experience, skills, year of experience, suggested_resume_category and recommendeded_job_roles
If any detail is not found, just skip that and don't provide any reasoning for anything.

The resume text:
{resume}
"""