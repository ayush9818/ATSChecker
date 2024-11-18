"""
Author: Ayush Agarwal
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

from ats_app.models.ai_models import ResumeScore

class StatusEnum(str, Enum):
    SUCCESS = "success"
    ERROR = "error"

class ResumeAnalysisResponse(BaseModel):
    status: StatusEnum = Field(description="Status of the resume analysis request")
    message: str = Field(description="Additional information about the analysis process")
    data: Optional[ResumeScore] = Field(description="Detailed resume analysis results")

class CreateUserRequest(BaseModel):
    name: str
    email: str
    contact_number: Optional[str] = None

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    contact_number: Optional[str] = None

    class Config:
        orm_mode = True

class CreateJobRequest(BaseModel):
    job_description: str
    job_title : str
    employment_type : str 
    company_name : str


class JobResponse(BaseModel):
    job_id: int
    job_description: str
    job_title : str
    employment_type : str 
    company_name : str

    class Config:
        orm_mode = True

class ApplyJobRequest(BaseModel):
    user_id: int
    job_id: int
    resume_id: int

    class Config:
        orm_mode = True

class ApplicationResponse(BaseModel):
    application_id: int
    user_name: str
    user_email: str
    user_contact: Optional[str]
    job_title: str
    company_name: str
    resume_path: str
    skills: Optional[str]
    years_of_experience: Optional[int]

    class Config:
        orm_mode = True

class UploadResumeRequest(BaseModel):
    user_id: int
    resume_body: bytes
    file_name: str

    class Config:
        orm_mode = True

class ResumeResponse(BaseModel):
    resume_id: int
    user_id: int
    resume_path: str
    years_of_experience: Optional[int]
    education: Optional[str]
    skills: Optional[str]
    work_experience: Optional[str]

    class Config:
        orm_mode = True
