import requests

API_URL = "http://127.0.0.1:8000/jobs/"


jobs = [
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

# Function to create jobs in the database
def create_jobs(jobs):
    for idx, job in enumerate(jobs, start=1):
        response = requests.post(API_URL, json=job)
        if response.status_code == 200 or response.status_code == 201:
            print(f"Job {idx} created successfully: {response.json()}")
        else:
            print(f"Failed to create Job {idx}: {response.status_code} - {response.text}")

# Main function
if __name__ == "__main__":
    create_jobs(jobs)
