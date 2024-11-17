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