"""
Author: Ayush Agarwal
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class EducationEntry(BaseModel):
    degree: Optional[str] = Field(default=None, description="Name of the degree obtained, e.g., Bachelor of Science, Master of Engineering.")
    institution: Optional[str] = Field(default=None, description="Name of the institution where the degree was pursued.")

class SkillsEntry(BaseModel):
    technical: List[str] = Field(default_factory=list, description="Technical Skills")
    non_technical: List[str] = Field(default_factory=list, description="Non-Technical or Soft Skills")

class WorkExperienceEntry(BaseModel):
    company: Optional[str] = Field(default=None, description="Name of the company candidate has worked at")
    role: Optional[str] = Field(default=None, description="Job role at the company")
    start_date: Optional[str] = Field(default=None, description="Start date of the Job.")
    end_date: Optional[str] = Field(default=None, description="End date of the Job.")

class ResumeContent(BaseModel):
    name: Optional[str] = Field(default=None, description="Name of the candidate")
    skills: Optional[SkillsEntry] = Field(default_factory=SkillsEntry, description="Technical and Non-Technical Skills of the candidate")
    education: List[EducationEntry] = Field(default_factory=list, description="List of educational qualifications, where each entry contains details about degree, institution, and dates.")
    work_experience: List[WorkExperienceEntry] = Field(default_factory=list, description="List of work experiences, where each experience include company name, role, start date and end date.")
    suggested_resume_category: Optional[str] = Field(default=None, description="Suggested Resume Category (based on the skills and experience)") 
    recommended_job_roles: List[str] = Field(default_factory=list, description="Recommended Job Roles (based on the candidate's skills and experience)")
    years_of_experience: Optional[int] = Field(default=None, description="Years of Experience, calculated from work experience")

class ResumeScore(BaseModel):
    perc_match: int = Field(description="Percentage match between the job description and the resume (0-100)")
    matching_keywords: List[str] = Field(description="List of important keywords or skills found in both the resume and job description")
    missing_keywords: List[str] = Field(description="List of important keywords or skills from the job description missing in the resume")
    improvement_suggestions: List[str] = Field(description="Specific suggestions to improve the resume for better alignment with the job description")
    profile_summary: str = Field(description="Concise profile summary of the candidate based on their entire resume")
    top_strengths: List[str] = Field(description="Top 3 strengths of the candidate relevant to the job description")
    areas_for_improvement: List[str] = Field(description="Top 3 areas for improvement or skills to develop for better job fit")
    ats_compatibility_score: int = Field(description="Score for how well the resume is formatted for ATS systems (0-100)")
    experience_level_match: str = Field(description="Assessment of how well the candidate's experience level matches the job requirements")