import warnings
import requests
import os
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from handlers.api_handler import APIHandler
from handlers.s3_handler import S3Handler
from utils import filter_similar_jobs
import pandas as pd

# Suppress warnings
warnings.filterwarnings("ignore")

# Load environment variables from .env file
load_dotenv()

# Function to inject CSS into the app
def inject_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Inject custom CSS styles
# inject_css("style.css")

# Streamlit app title
st.title("ATS Analysis for Job Applicants")

st.image("images/app_frontend.jpg", caption="ATS Analysis")

if __name__ == "__main__":
    # Retrieve base API URLs from environment variables
    BASE_GET_API = os.getenv("BASE_GET_API")
    BASE_POST_API = os.getenv("BASE_POST_API")

    # Initialize API handler in session state if not already present
    if "api_handler" not in st.session_state:
        st.session_state["api_get_handler"] = APIHandler(base_url=BASE_GET_API)
        st.session_state["api_post_handler"] = APIHandler(base_url=BASE_POST_API)

    # Initialize session state for recently uploaded resumes if not already present
    if "recent_resumes" not in st.session_state:
        st.session_state["recent_resumes"] = None

    # Function to fetch available job listings (models)
    # def fetch_jobs():
    #     all_jobs = st.session_state["api_get_handler"].get("/jobs/", [])
    #     st.session_state["all_jobs"] = all_jobs
    #     st.session_state["last_fetch_time"] = datetime.now()
    #     st.rerun()  # Rerun the app to refresh the display
    def fetch_jobs():
        return [
    {
        "job_title": "AI/ML Engineer",
        "job_description": (
            "About the Job:\n"
            "OpenAI is at the forefront of artificial intelligence research and deployment. We are seeking an AI/ML Engineer passionate about developing and implementing cutting-edge machine learning models to solve real-world problems.\n\n"
            "Responsibilities:\n"
            "- Design, develop, and deploy machine learning models and algorithms.\n"
            "- Collaborate with cross-functional teams to integrate AI solutions into products.\n"
            "- Stay updated with the latest research and advancements in AI/ML.\n"
            "- Optimize models for performance and scalability.\n\n"
            "Qualifications:\n"
            "- Bachelor's or Master's degree in Computer Science, Engineering, or a related field.\n"
            "- 3+ years of experience in machine learning and AI development.\n"
            "- Proficiency in Python and frameworks such as TensorFlow or PyTorch.\n"
            "- Strong problem-solving skills and ability to work in a team environment.\n\n"
            "Benefits:\n"
            "- Competitive salary and equity options.\n"
            "- Comprehensive health, dental, and vision insurance.\n"
            "- Flexible working hours and remote work options.\n"
            "- Opportunities for continuous learning and professional development."
        ),
        "company_name": "OpenAI", 
        "employment_type" : "Full Time"
    },
    {
        "job_title": "Data Scientist",
        "job_description": (
            "About the Job:\n"
            "Google is looking for a Data Scientist to join our analytics team. The ideal candidate will have a strong background in data analysis and a passion for deriving insights from large datasets to drive business decisions.\n\n"
            "Responsibilities:\n"
            "- Analyze complex datasets to identify trends and patterns.\n"
            "- Develop predictive models to support business objectives.\n"
            "- Collaborate with product and engineering teams to implement data-driven solutions.\n"
            "- Communicate findings to stakeholders through reports and presentations.\n\n"
            "Qualifications:\n"
            "- Master's degree in Statistics, Mathematics, Computer Science, or a related field.\n"
            "- 2+ years of experience in data analysis or a related role.\n"
            "- Proficiency in SQL, R, and Python.\n"
            "- Strong analytical skills and attention to detail.\n\n"
            "Benefits:\n"
            "- Competitive salary and performance bonuses.\n"
            "- Health and wellness programs.\n"
            "- Access to Google's extensive resources and tools.\n"
            "- Opportunities for career growth and advancement."
        ),
        "company_name": "Google",
        "employment_type" : "Internship"
    },
    {
        "job_title": "Software Engineer",
        "job_description": (
            "About the Job:\n"
            "Microsoft is seeking a Software Engineer to join our development team. The successful candidate will work on building and maintaining software applications that meet the needs of our users.\n\n"
            "Responsibilities:\n"
            "- Write clean, maintainable, and efficient code.\n"
            "- Participate in code reviews and contribute to team knowledge sharing.\n"
            "- Collaborate with designers and product managers to define software requirements.\n"
            "- Troubleshoot and debug applications to ensure optimal performance.\n\n"
            "Qualifications:\n"
            "- Bachelor's degree in Computer Science or a related field.\n"
            "- 3+ years of experience in software development.\n"
            "- Proficiency in C#, .NET, and Azure services.\n"
            "- Strong understanding of software development principles and methodologies.\n\n"
            "Benefits:\n"
            "- Competitive salary and stock options.\n"
            "- Comprehensive health benefits.\n"
            "- Flexible work schedules and telecommuting options.\n"
            "- Access to Microsoft's learning and development resources."
        ),
        "company_name": "Microsoft",
        "employment_type" : "Full Time"
    },
    {
        "job_title": "Product Manager",
        "job_description": (
            "About the Job:\n"
            "Amazon is looking for a Product Manager to lead the development of new products and features. The ideal candidate will have a strong understanding of market trends and customer needs.\n\n"
            "Responsibilities:\n"
            "- Define product vision and strategy.\n"
            "- Gather and prioritize product and customer requirements.\n"
            "- Work closely with engineering, marketing, and sales teams to deliver products.\n"
            "- Analyze market trends and competitors to inform product decisions.\n\n"
            "Qualifications:\n"
            "- Bachelor's degree in Business, Marketing, or a related field.\n"
            "- 4+ years of experience in product management.\n"
            "- Strong analytical and problem-solving skills.\n"
            "- Excellent communication and leadership abilities.\n\n"
            "Benefits:\n"
            "- Competitive salary and comprehensive benefits package.\n"
            "- Employee discount on Amazon products.\n"
            "- Opportunities for career advancement.\n"
            "- Dynamic and inclusive work environment."
        ),
        "company_name": "Amazon",
        "employment_type" : "Full Time"
    }
]

    # Step 1: Collect user information
    st.info("Enter Your Information (Step 1)")

    # Display note for existing users and One-click Apply
    st.markdown("""
    **Note:** *We will update your information if you are an existing user. Use One-click Apply to select from your last 3 uploaded resumes.*
    """)

    # User input fields
    name = st.text_input("Your Name (*)")
    email = st.text_input("Your Email (*)")
    contact = st.text_input("Your Contact (*)")

    # Submit button for user information
    if st.button("Submit"):
        if name and email and contact:
            # Prepare data to send in POST request
            login_data = {
                "name": name,
                "email": email,  # User's email
                "contact": contact,  # User's contact number
            }
            # Endpoint to send user information for processing
            login_endpoint = "/login/"
            try:
                response = st.session_state["api_post_handler"].post(login_endpoint, login_data)
                st.success("Your information has been submitted.")
            except requests.exceptions.HTTPError as err:
                st.error(f"An error occurred: {err}")
        else:
            st.error("Please fill in all required fields.")

    # Step 2: Upload resume for new or existing users
    st.info("Are you a new user or want to update your resume? (Step 2)")

    # Resume upload section
    uploaded_resume = st.file_uploader("Upload Your Resume", type=["pdf"])

    if uploaded_resume:
        st.write("File uploaded successfully.")

        # Submit button to handle resume upload to S3
        if st.button("Submit Resume"):
            if uploaded_resume:
                # Use the S3Handler class to upload the file directly to S3
                s3_path = f"resumes/{uploaded_resume.name}"  # S3 directory and filename
                s3_client = S3Handler()  # Assuming this is your S3 handler class

                try:
                    # Upload the file directly to S3 (using the file's buffer)
                    s3_client.upload_fileobj(uploaded_resume, s3_path)

                    # If needed, you can store additional metadata or log actions here

                    st.success("Your resume has been uploaded successfully to S3.")
                except Exception as e:
                    st.error(f"An error occurred while uploading your resume to S3: {e}")
            else:
                st.error("Please upload a valid resume.")
        
    # Step 3: Find Available Jobs
    st.info("Find Available Jobs (Step 3)")

    # Input fields for job search
    job_title_input = st.text_input("Enter Job Title (e.g., Software Engineer, Data Scientist):")
    # Dropdown for employment type
    employment_type = st.selectbox(
        "Search by Employment Type:", 
        options=["Full Time", "Internship", "Part-time"],
        index=0  # Default to "Full Time"
    )

    # Fetch jobs when the Submit button is pressed
    if st.button("Search Jobs"):
        available_jobs = fetch_jobs()

        if available_jobs:
            available_jobs_df = pd.DataFrame(available_jobs)
            
            # Filter jobs based on employment type
            filtered_available_jobs = available_jobs_df[available_jobs_df['employment_type'] == employment_type]
            
            # Perform similarity search on job titles
            similar_jobs = filter_similar_jobs(filtered_available_jobs, job_title_input)

            if not similar_jobs.empty:
                for idx, job in similar_jobs.iterrows():
                    company_name = job.get("company_name")
                    job_title = job.get("job_title")
                    employment_type = job.get("employment_type")
                    job_description = job.get("job_description")

                    # Display the job details
                    st.write(f"**Company Name:** {company_name}")
                    st.write(f"**Employment Type:** {employment_type}")
                    st.write(f"**Job Title:** {job_title}")
                    st.write(f"**Job Description:** {job_description}")
                    
                    # Add Apply and ATS Analysis buttons for each job with unique keys using the index
                    col1, col2 = st.columns([1, 1])  # Create two columns for buttons
                    with col1:
                        if st.button(f"Apply for {job_title}", key=f"apply_{idx}"):  # Unique key using index
                            st.write(f"You've clicked Apply for Job {idx}.")
                            # Add your application logic here
                    with col2:
                        if st.button(f"ATS Analysis for {job_title}", key=f"ats_{idx}"):  # Unique key using index
                            st.write(f"You've clicked ATS Analysis for Job {idx}.")
            else:
                st.write("No similar jobs found based on your search criteria.")
        else:
            st.write("No jobs found.")

        