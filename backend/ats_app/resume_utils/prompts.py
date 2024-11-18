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

resume_match_prompt = """
Act as an advanced Applicant Tracking System (ATS) with extensive expertise in the tech industry, specifically in software engineering, data science, data analysis, and big data engineering. Your task is to meticulously evaluate the provided resume against the given job description.

Consider the following:
1. The job market is highly competitive, so provide detailed, actionable feedback to improve the resume.
2. Analyze the resume for both hard skills (technical abilities) and soft skills (interpersonal qualities).
3. Consider the candidate's experience level and how it aligns with the job requirements.
4. Evaluate the resume's formatting and structure for ATS compatibility.
5. Assess the clarity and impact of the candidate's achievements and responsibilities.

Please provide the following:
1. An accurate percentage match between the resume and the job description.
2. A comprehensive list of matching keywords and skills found in both the resume and job description
3. A comprehensive list of missing keywords and skills from the job description.
4. Suggestions for improving the resume to better match the job description.
5. A brief profile summary of the candidate based on their resume.
6. Top 3 strengths of the candidate relevant to the job description.
7. Top 3 areas for improvement or skills to develop.

Resume: {text}
Job Description: {jd}
"""