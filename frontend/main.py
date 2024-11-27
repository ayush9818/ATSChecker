import warnings
import requests
import os
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from handlers.api_handler import APIHandler
from utils import filter_similar_jobs, is_valid_email, encode_file_to_base64
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

# Function to display the header with the "Home" button
def show_header():
    col1, col2 = st.columns([10, 2])
    with col2:
        if st.button("Home", key="nav_home"):
            st.session_state.current_page = "Home"

# Function to display the main page
def show_main_page():
    st.title("ATS Resume Checker")
    st.info("ATS Resume Checker is an AI-powered Job Portal designed to streamline the recruitment process for both recruiters and candidates.")
    st.image("images/app_frontend.jpg", caption="ATS Analysis")

    # Add a blank line before the buttons
    st.write("")

    col1, col2 = st.columns([4, 1])
    with col1:
        if st.button("Applicants"):
            st.session_state.current_page = "Applicants"
            st.rerun()  # Ensure the page re-runs to update display
    with col2:
        if st.button("Recruiters"):
            st.session_state.current_page = "Recruiters"
            st.rerun()  # Ensure the page re-runs to update display

def check_user_job_application(api_handler, user_id, job_id):
    """Check if the user has already applied for the job."""
    try:
        return api_handler.get("jobs/applications/", {"user_id": user_id, "job_id": job_id})
    except Exception as e:
        return None

# Function for Applicants page
def show_applicants_page():    
    st.title("Applicants Page")
    # Add content for applicants here
    st.info("Welcome, Applicants! Here you can analyze ATS data for your job applications.")
    st.image("images/app_frontend.jpg", caption="ATS Analysis")

    # Initialize session states
    if "search_results" not in st.session_state:
        st.session_state.search_results = None
    if "applied_jobs" not in st.session_state:
        st.session_state.applied_jobs = set()
    if "job_title_input" not in st.session_state:
        st.session_state.job_title_input = ""
    if "selected_employment_type" not in st.session_state:
        st.session_state.selected_employment_type = "Full Time"

    # Step 1: Collect user information
    st.info("Enter Your Information (Step 1)")

    # Display note for existing users and One-click Apply
    st.markdown("""
    **Note:** *We will update your information if you are an existing user. Use One-click Apply to select from your most recently uploaded resumes.*
    """)

    # User input fields
    name = st.text_input("Your Name (*)")
    email = st.text_input("Your Email (*)")
    contact = st.text_input("Your Contact (*)")

    # Submit button for user information
    if st.button("Submit"):
        if name and email and contact:
            if not is_valid_email(email):
                st.error("Invalid email address. Please provide a valid email.")
            else:
                try:
                    # Attempt to register a new user
                    user_data = {"name": name, "email": email, "contact": contact}
                    response = st.session_state["api_handler"].post("users/", user_data)

                    if response.status_code == 200:
                        st.success(f"Hello, {name}! Your information has been submitted.")
                    else:
                        print(f"Unexpected error occurred: {response.status_code} - {response.text}")
                        if response.status_code == 400:
                            try:
                                print("Email already exists. Retrieving your information...")
                                # Retrieve existing user data
                                user_response = st.session_state["api_handler"].get("users/", {"email": email})
                                user_data = user_response[0]
                                user_name = user_data.get("name", "User")  # Default to "User" if name is missing
                                st.success(f"Welcome back, {user_name}!")
                                st.session_state["user_id"] = user_data.get("user_id")
                            except requests.exceptions.HTTPError as nested_err:
                                st.error(f"Error while retrieving user information: {nested_err}")
                        else:
                            st.error(f"An error occurred during registration: {response.status_code}")  # Fix: use `response.status_code`
                except requests.exceptions.RequestException as err:
                    st.error(f"An error occurred during registration: {err}")

        else:
            st.error("Please fill in all required fields.")

    # Step 2: Upload resume for new or existing users
    st.info("Are you a new user or want to update your resume? (Step 2)")

    # Resume upload section
    uploaded_resume = st.file_uploader("Upload Your Resume", type=["pdf"])

    if uploaded_resume:
        st.write("File uploaded successfully.")

        # Submit button to handle resume upload to API
        if st.button("Submit Resume"):
            try:
                # Use the uploaded file directly
                file_name = uploaded_resume.name 

                # Read the file content as binary
                file_content = uploaded_resume.read()

                # Encode the file content to Base64
                base64_resume = encode_file_to_base64(file_content)

                # Prepare the payload
                payload = {
                    "user_id": st.session_state.get("user_id"),
                    "resume_body": base64_resume,
                    "file_name": file_name
                }

                # Send the request to the API
                response = st.session_state["api_handler"].post("resume/upload/", payload)

                # Handle the response
                if response.status_code == 200:
                    st.success("Your resume has been uploaded successfully.")
                else:
                    st.error(f"Failed to upload resume. Error code: {response.status_code}")
                    st.write(f"Error details: {response.text}")

            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

    # Step 3: Find Available Jobs
    st.info("Find Available Jobs (Step 3)")
    
    fetch_last_resume_id()
    
    if not st.session_state.get("user_id"):
        st.warning("Please log in before reviewing all the available jobs in your search.")
    elif not st.session_state.get("resume_id"):
        st.warning("Please upload your resume before reviewing all the available jobs in your search.")
    else:
        # Create a form for job search to handle first-click submission
        with st.form(key='job_search_form'):
            job_title_input = st.text_input(
                "Enter Job Title (e.g., Software Engineer, Data Scientist):",
                value=st.session_state.job_title_input
            )
            employment_type = st.selectbox(
                "Search by Employment Type:", 
                options=["Full Time", "Internship", "Part Time"],
                index=["Full Time", "Internship", "Part Time"].index(st.session_state.selected_employment_type)
            )
            search_submitted = st.form_submit_button("Search Jobs")

            if search_submitted:
                st.session_state.job_title_input = job_title_input
                st.session_state.selected_employment_type = employment_type
                fetch_jobs()
                
                # Process search results
                available_jobs = st.session_state.get("all_jobs", [])
                if available_jobs:
                    available_jobs_df = pd.DataFrame(available_jobs)
                    filtered_available_jobs = available_jobs_df[available_jobs_df['employment_type'] == employment_type]
                    similar_jobs = filter_similar_jobs(filtered_available_jobs, job_title_input)
                    st.session_state.search_results = similar_jobs.to_dict('records')
                else:
                    st.session_state.search_results = []

        # Display search results
        if st.session_state.search_results:
            for job in st.session_state.search_results:
                with st.container():
                    job_id = job.get("job_id")
                    company_name = job.get("company_name")
                    job_title = job.get("job_title")
                    employment_type = job.get("employment_type")
                    job_description = job.get("job_description")
                    user_id = st.session_state.get("user_id")
                    resume_id = st.session_state.get("resume_id")

                    st.markdown("---")
                    st.write(f"**Company Name:** {company_name}")
                    st.write(f"**Employment Type:** {employment_type}")
                    st.write(f"**Job Title:** {job_title}")
                    st.write(f"**Job Description:** {job_description}")

                    # Check application status
                    application_status = check_user_job_application(
                        st.session_state["api_handler"], 
                        user_id, 
                        job_id
                    )

                    if st.button("ATS Analysis", key=f"ats_{job_id}"):
                        st.info("Performing ATS analysis for this role...")
                        
                        try:
                            # Fetch analysis response from API
                            response = st.session_state["api_handler"].get(
                                "resume/analyze/", 
                                {"resume_id": resume_id, "job_id": job_id}
                            )
                            
                            if response:
                                # Display ATS compatibility score
                                st.header("ATS Analysis Results")
                                st.metric("ATS Compatibility Score", f"{response['ats_compatibility_score']}%")
                                
                                # Display profile summary
                                st.subheader("Profile Summary")
                                st.markdown(response['profile_summary'])
                                
                                # Display strengths
                                st.subheader("Top Strengths")
                                for strength in response['top_strengths']:
                                    st.success(f"✅ {strength}")
                                
                                # Display areas for improvement
                                st.subheader("Areas for Improvement")
                                for improvement in response['areas_for_improvement']:
                                    st.warning(f"⚠️ {improvement}")
                                
                                # Display keyword matching
                                st.subheader("Keyword Analysis")
                                st.write("**Matching Keywords:**")
                                st.write(", ".join(response['matching_keywords']))
                                
                                st.write("**Missing Keywords:**")
                                st.write(", ".join(response['missing_keywords']))
                                
                                # Display improvement suggestions
                                st.subheader("Improvement Suggestions")
                                for suggestion in response['improvement_suggestions']:
                                    st.info(f"💡 {suggestion}")
                                
                                # Display experience level match
                                st.subheader("Experience Level Match")
                                st.markdown(response['experience_level_match'])
                            else:
                                st.warning("No analysis data returned. Please try again later.")

                        except Exception as e:
                            st.error("Failed to fetch ATS analysis. Please try again.")
                            print("Error during ATS analysis:", e)
                   
                    # Check if already applied
                    if application_status or job_id in st.session_state.applied_jobs:
                        st.success("✓ You have already applied for this role.")
                    else:
                        if st.button(f"Apply", key=f"apply_{job_id}"):
                            try:
                                apply_data = {
                                    "user_id": user_id,
                                    "job_id": job_id,
                                    "resume_id": resume_id,
                                }
                                response = st.session_state["api_handler"].post("jobs/apply/", apply_data)

                                if response.status_code == 200:
                                    # Add to applied jobs set
                                    st.session_state.applied_jobs.add(job_id)
                                    st.success("You have successfully applied for this job!")
                                else:
                                    st.error("Failed to apply for the job. Please try again later.")
                                    
                            except Exception as e:
                                st.error(f"An error occurred while applying for the job: {e}")
                                         
        elif st.session_state.search_results == []:
            st.write("No similar jobs found based on your search criteria.")

def show_recruiters_page():
    st.title("Recruiters Page")
    # Add content for recruiters here
    st.info("Welcome, Recruiters! Here you can analyze ATS data for your recruitment process.")
    st.image("images/app_frontend.jpg", caption="ATS Analysis")

    # Section 1: Post a Job
    st.subheader("Post a Job")
    with st.form(key="post_job_form"):
        job_description = st.text_area("Job Description")
        job_title = st.text_input("Job Title")
        # Dropdown for Employment Type
        employment_type = st.selectbox(
            "Employment Type",
            options=["Full Time", "Internship", "Part Time"],
            index=0  # Default option (Full Time)
        )
        company_name = st.text_input("Company Name")
        submit_job = st.form_submit_button("Post Job")

    if submit_job:
        if job_description and job_title and employment_type and company_name:
            post_data = {
                "job_description": job_description,
                "job_title": job_title,
                "employment_type": employment_type,
                "company_name": company_name,
            }
            # Use api_handler.post to send the data
            response = st.session_state["api_handler"].post("jobs/", post_data)
            if response.status_code == 200:
                st.success("Job posted successfully!")
            else:
                st.error(f"Failed to post job. Error: {response.text}")
        else:
            st.warning("Please fill all fields to post a job.")

    # Section 2: Filter Jobs by Company Name and Job Title
    st.subheader("Filter Jobs by Company Name and Job Title")
    company_name_filter = st.text_input("Enter Company Name")
    job_title_filter = st.text_input("Enter Job Title (optional)")
    if st.button("Filter Jobs"):
        if company_name_filter:
            params = {"company_name": company_name_filter}
            if job_title_filter:
                params["job_title"] = job_title_filter

            # Use api_handler.get to filter jobs
            response = st.session_state["api_handler"].get("jobs/", params)
            if response.status_code == 200:
                jobs = response.json()
                if jobs:
                    st.write("Filtered Jobs:")
                    for job in jobs:
                        st.write(job)
                else:
                    st.info("No jobs found for the given criteria.")
            else:
                st.error(f"Failed to fetch jobs. Error: {response.text}")
        else:
            st.warning("Please enter at least the Company Name.")

    # Section 3: Get Applicant Count
    st.subheader("Get Applicant Count for a Job")
    job_id_for_count = st.text_input("Enter Job ID to get applicant count")
    if st.button("Get Applicant Count"):
        if job_id_for_count:
            # Use api_handler.get to fetch the applicant count
            response = st.session_state["api_handler"].get("jobs/applicants/count", {"job_id": job_id_for_count})
            if response.status_code == 200:
                count = response.json().get("total_applicants", 0)
                st.success(f"Number of applicants: {count}")
            else:
                st.error(f"Failed to fetch applicant count. Error: {response.text}")
        else:
            st.warning("Please enter a Job ID.")

    # Section 4: Filter Candidates
    st.subheader("Filter Candidates")
    job_id_filter = st.text_input("Job ID")
    min_experience = st.number_input("Minimum Years of Experience (optional)", min_value=0, step=1, value=0)
    skills_filter = st.text_input("Filter by Skills (comma-separated, optional)")
    if st.button("Filter Candidates"):
        params = {"job_id": job_id_filter}
        if min_experience > 0:
            params["years_of_experience"] = min_experience
        if skills_filter:
            params["skills"] = skills_filter
        # Use api_handler.get to filter candidates
        response = st.session_state["api_handler"].get("jobs/applications", params)
        if response.status_code == 200:
            candidates = response.json()
            if candidates:
                st.write("Filtered Candidates:")
                for candidate in candidates:
                    st.write(candidate)
            else:
                st.info("No candidates found.")
        else:
            st.error(f"Failed to filter candidates. Error: {response.text}")

    # Section 5: Fetch Resumes
    st.subheader("Fetch Resumes")
    user_id_filter = st.text_input("Filter by User ID (optional)")
    resume_id_filter = st.text_input("Filter by Resume ID (optional)")
    top_k_resumes = st.number_input("Find Top K Resumes (sorted by Resume ID, descending)", min_value=1, step=1, value=1)
    if st.button("Fetch Resumes"):
        params = {}
        if user_id_filter:
            params["user_id"] = user_id_filter
        if resume_id_filter:
            params["resume_id"] = resume_id_filter
        params["top_k"] = top_k_resumes
        # Use api_handler.get to fetch resumes
        response = st.session_state["api_handler"].get("resume", params)
        if response.status_code == 200:
            resumes = response.json()
            if resumes:
                st.write("Top Resumes:")
                for resume in resumes:
                    st.write(resume)
            else:
                st.info("No resumes found.")
        else:
            st.error(f"Failed to fetch resumes. Error: {response.text}")

# Function to fetch all jobs
def fetch_jobs():
    # Fetch all jobs from the API
    all_jobs = st.session_state["api_handler"].get("jobs/", {})
    # Update session state with job data and timestamp
    st.session_state["last_fetch_time"] = datetime.now()
    st.session_state["all_jobs"] = all_jobs

def fetch_last_resume_id():
    """Fetch the latest resume ID for the current user and update session state."""
    try:
        # Fetch the latest resume based on user ID
        response = st.session_state["api_handler"].get(
            "resume/", 
            {"user_id": st.session_state.get("user_id"), "top_k": 1}
        )

        if response:
            latest_resume = response[0]
            st.session_state["resume_id"] = latest_resume.get("resume_id")
        else:
            st.warning("Please update your resume before applying for jobs.")
            st.session_state["resume_id"] = None

    except Exception as e:
        st.error(f"Failed to fetch the latest resume: {e}")
        st.session_state["resume_id"] = None
    
if __name__ == "__main__":
    # Initialize session state for the current page
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"
    
    # Retrieve base API URL from environment variables
    BASE_API = os.getenv("BASE_API")

    # Initialize session state variables if not already present
    if "api_handler" not in st.session_state:
        st.session_state["api_handler"] = APIHandler(base_url=BASE_API)

    if "recent_resumes" not in st.session_state:
        st.session_state["recent_resumes"] = None

    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None

    if "resume_id" not in st.session_state:
        st.session_state["resume_id"] = None

    # Show the header (with "Home" button)
    show_header()

    # Route to the appropriate page
    if st.session_state.current_page == "Home":
        show_main_page()
    elif st.session_state.current_page == "Applicants":
        show_applicants_page()
    elif st.session_state.current_page == "Recruiters":
        show_recruiters_page()
        