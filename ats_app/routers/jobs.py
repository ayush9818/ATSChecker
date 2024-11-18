
"""
Author: Ayush Agarwal
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from ats_app.database import models 
from ats_app.database.models import get_db
from ats_app.models import response_schema as schemas

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