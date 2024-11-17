"""
Author: Ayush Agarwal
"""
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

from ats_app.resume_utils.entity_extractor import (
    create_entity_extractor_chain, 
    extract_entities, 
)
from ats_app.resume_utils.resume_matcher import (
    create_ats_chain, 
    perform_ats_analysis
)
from ats_app.models.response_schema import ResumeAnalysisResponse, StatusEnum
from ats_app.crud import (
    fetch_job_description_from_db, 
    fetch_resume_from_db
)

app = FastAPI()

ENTITY_CHAIN = create_entity_extractor_chain()
ATS_CHAIN = create_ats_chain()


@app.post("/analyze_resume", response_model=ResumeAnalysisResponse)
async def analyze_resume(resume_id: str, job_id: str):

    # TODO : Implement the fetch_resume from db function
    resume_path = await fetch_resume_from_db(resume_id)
    if not resume_path:
        raise HTTPException(status_code=404, detail="Resume not found")

   # TODO : Implement the fetch job description from db function
    job_description = await fetch_job_description_from_db(job_id)
    if not job_description:
        raise HTTPException(status_code=404, detail="Job description not found")

    try:
        analysis_result = await perform_ats_analysis(resume_path, job_description)

        return ResumeAnalysisResponse(
            status=StatusEnum.SUCCESS,
            message="Resume analysis completed successfully",
            data=analysis_result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during resume analysis")


if __name__ == "__main__":
    entity_chain = create_entity_extractor_chain()
    resume_path = "/nfs/home/scg1143/ATSChecker/sample_data/resume.pdf"
    entities = extract_entities(entity_chain, file_path=resume_path)
    import pdb;pdb.set_trace();
