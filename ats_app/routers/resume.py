
"""
Author: Ayush Agarwal
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
import os
import uuid
from pathlib import Path
import base64
import boto3
import json


from ats_app.database import models
from ats_app.database.models import get_db
from ats_app.models import response_schema as schemas
from ats_app.crud import fetch_resume_path, fetch_job_description
from ats_app.resume_utils.resume_matcher import create_ats_chain, perform_ats_analysis
from ats_app.resume_utils.entity_extractor import create_entity_extractor_chain, extract_entities

router = APIRouter(tags=["resume"])

ATS_CHAIN = create_ats_chain()
ENTITY_CHAIN = create_entity_extractor_chain()

TEMP_DIR = Path().cwd() / 'data'
TEMP_DIR.mkdir(exist_ok=True, parents=True)

BUCKET_NAME=os.environ['BUCKET_NAME']
BUCKET_DIR=os.environ['BUCKET_DIR']

def download_from_s3(s3_path):
    return None

def upload_to_s3(local_file_path, s3_file_path):
    s3 = boto3.client("s3")
    try:
        s3.upload_file(local_file_path, BUCKET_NAME, s3_file_path)
        return f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_file_path}"
    except Exception as e:
        raise e


@router.post("/analyze", response_model=schemas.ResumeAnalysisResponse)
def analyze_resume(resume_id: str, job_id: str):
    resume_path = fetch_resume_path(resume_id)
    if not resume_path:
        raise HTTPException(status_code=404, detail="Resume not found")

    job_description = fetch_job_description(job_id)
    if not job_description:
        raise HTTPException(
            status_code=404, detail="Job description not found")

    try:
        resume_path = download_from_s3(resume_path)
        analysis_result = perform_ats_analysis(
            ATS_CHAIN, resume_path, job_description)

        return schemas.ResumeAnalysisResponse(
            status=schemas.StatusEnum.SUCCESS,
            message="Resume analysis completed successfully",
            data=analysis_result
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred during resume analysis")


@router.post("/upload")
def upload_resume(
    request: schemas.UploadResumeRequest, db: Session = Depends(get_db)
):
    file_name = request.file_name
    print(f"File Name : {file_name}")
    if not file_name.endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400, detail="Unsupported file type. Only PDF and DOCX are allowed.")

    file_extension = os.path.splitext(file_name)[1]
    unique_file_name = f"{os.path.splitext(file_name)[0]}--{uuid.uuid4()}{file_extension}"

    local_file_path = TEMP_DIR / unique_file_name

    resume_binary = base64.b64decode(request.resume_body)
    with open(local_file_path, "wb") as f:
        f.write(resume_binary)

    print(f"Resume saved locally at {str(local_file_path)}")

    s3_file_path = os.path.join(BUCKET_DIR, unique_file_name)
    try:
        s3_url = upload_to_s3(local_file_path, s3_file_path)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to upload to S3.")

    print(f"{unique_file_name} uploaded to s3 successfully.")
    
    print("Extracting Entities")
    extracted_entities = extract_entities(llm_chain=ENTITY_CHAIN, 
                                        file_path=str(local_file_path))

    skills = []
    for skill in extracted_entities.skills.technical:
        skills.append(skill)
    for skill in extracted_entities.skills.non_technical:
        skills.append(skill)
    skills = ",".join(skills)

    extracted_data = {
        "years_of_experience": extracted_entities.years_of_experience,
        "education": json.dumps([ed.model_dump() for ed in extracted_entities.education]),
        "skills": skills,
        "work_experience": json.dumps([we.model_dump() for we in extracted_entities.work_experience])
    }   

    print("Adding Resume to database.")
    new_resume = models.UserResumes(
        user_id=request.user_id,
        resume_path=s3_url,
        years_of_experience=extracted_data["years_of_experience"],
        education=extracted_data["education"],
        skills=extracted_data["skills"],
        work_experience=extracted_data["work_experience"]
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    os.remove(local_file_path)

    return {
        "message": "Resume uploaded successfully.",
        "resume_id": new_resume.resume_id,
        "s3_url": s3_url
    }


@router.get("/", response_model=list[schemas.ResumeResponse])
def fetch_resume(
    user_id: int = Query(None, description="Filter by user ID (optional)"),
    resume_id: int = Query(None, description="Filter by resume ID (optional)"),
    db: Session = Depends(get_db),
):
    query = db.query(models.UserResumes)

    if user_id:
        query = query.filter(models.UserResumes.user_id == user_id)
    if resume_id:
        query = query.filter(models.UserResumes.resume_id == resume_id)

    results = query.all()

    if not results:
        raise HTTPException(status_code=404, detail="No resumes found for the given criteria.")

    return results