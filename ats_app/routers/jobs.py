
"""
Author: Ayush Agarwal
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from ats_app.database import models 
from ats_app.database.models import get_db
from ats_app.models import response_schema as schemas
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

router = APIRouter(tags=["jobs"])

@router.get("/", response_model=List[schemas.JobResponse])
def fetch_jobs(
    job_id: Optional[int] = Query(None, description="Filter by job ID"),
    job_title: Optional[str] = Query(None, description="Filter by job Title"),
    employment_type: Optional[str] = Query(None, description="Filter by Employment Type"),
    company_name: Optional[str] = Query(None, description="Filter by Company Name"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Jobs)

    if job_id is not None:
        query = query.filter(models.Jobs.job_id == job_id)
    if job_title is not None:
        query = query.filter(models.Jobs.job_title == job_title)
    if employment_type is not None:
        query = query.filter(models.Jobs.employment_type == employment_type)
    if company_name is not None:
        query = query.filter(models.Jobs.company_name == company_name)

    jobs = query.all()
    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found with the provided filters.")

    return jobs


@router.post("/", response_model=schemas.JobResponse)
def create_job(request: schemas.CreateJobRequest, db: Session = Depends(get_db)):
    new_job = models.Jobs(job_description=request.job_description, 
                          job_title=request.job_title,
                          employment_type=request.employment_type, 
                          company_name=request.company_name
                          )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.post("/apply", response_model=dict)
def apply_for_job(request: schemas.ApplyJobRequest, db: Session = Depends(get_db)):
    existing_entry = db.query(models.UserJobs).filter(
        models.UserJobs.user_id == request.user_id,
        models.UserJobs.job_id == request.job_id
    ).first()
    
    if existing_entry:
        raise HTTPException(
            status_code=400, 
            detail="You have already applied for this job."
        )
    
    new_entry = models.UserJobs(
        user_id=request.user_id,
        job_id=request.job_id,
        resume_id=request.resume_id
    )
    db.add(new_entry)
    try:
        db.commit()
        db.refresh(new_entry)
        return {"message": "Application submitted successfully.", "application_id": new_entry.id}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail="An error occurred while processing your application."
        )

@router.get("/applicants/count", response_model=dict)
def get_applicant_count(
        job_id: int = Query(..., description="Job ID to calculate the number of applicants"),
        db: Session = Depends(get_db)
    ):
    count = db.query(func.count(models.UserJobs.id)).filter(models.UserJobs.job_id == job_id).scalar()
    return {"job_id": job_id, "total_applicants": count}

@router.get("/applications", response_model=list[schemas.ApplicationResponse])
def get_user_applications(
    user_id: int = Query(None, description="Filter by user ID"),
    job_id: int = Query(None, description="Filter by job ID"),
    years_of_experience: int = Query(None, description="Minimum years of experience (optional)"),
    skills: list[str] = Query(None, description="Filter by skills (comma-separated, optional)"),
    db: Session = Depends(get_db),
):
    query = db.query(
        models.UserJobs.id.label("application_id"),
        models.Users.name.label("user_name"),
        models.Users.email.label("user_email"),
        models.Users.contact_number.label("user_contact"),
        models.Jobs.job_title.label("job_title"),
        models.Jobs.company_name.label("company_name"),
        models.UserResumes.resume_path.label("resume_path"),
        models.UserResumes.skills.label("skills"),
        models.UserResumes.years_of_experience.label("years_of_experience")
    ).join(models.Users, models.UserJobs.user_id == models.Users.user_id
    ).join(models.Jobs, models.UserJobs.job_id == models.Jobs.job_id
    ).join(models.UserResumes, models.UserJobs.resume_id == models.UserResumes.resume_id)

    if user_id:
        query = query.filter(models.UserJobs.user_id == user_id)
    if job_id:
        query = query.filter(models.UserJobs.job_id == job_id)

    results = query.all()

    filtered_results = []
    for row in results:
        if years_of_experience is not None:
            if row.years_of_experience is None or row.years_of_experience < years_of_experience:
                continue

        if skills:
            resume_skills = {skill.strip().lower() for skill in (row.skills or "").split(",")}
            input_skills = {skill.strip().lower() for skill in skills}
            if not resume_skills.intersection(input_skills):
                continue

        filtered_results.append(row)

    if not filtered_results:
        raise HTTPException(status_code=404, detail="No applications found for the given criteria.")

    return [
        schemas.ApplicationResponse(
            application_id=row.application_id,
            user_name=row.user_name,
            user_email=row.user_email,
            user_contact=row.user_contact,
            job_title=row.job_title,
            company_name=row.company_name,
            resume_path=row.resume_path,
            skills=row.skills,
            years_of_experience=row.years_of_experience,
        )
        for row in filtered_results
    ]
