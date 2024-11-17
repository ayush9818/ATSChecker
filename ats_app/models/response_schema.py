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
    pass


