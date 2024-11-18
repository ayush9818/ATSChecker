"""
Author: Ayush Agarwal
"""
from sqlalchemy.orm import Session
from ats_app.database import models

def fetch_resume_path(resume_id: int, db: Session) -> str:
    resume = db.query(models.UserResumes).filter(models.UserResumes.resume_id == resume_id).first()
    if not resume:
        return None
    return resume.resume_path

def fetch_job_description(job_id: int, db: Session) -> str:
    job = db.query(models.Jobs).filter(models.Jobs.job_id == job_id).first()

    if not job:
        return None
    return job.job_description