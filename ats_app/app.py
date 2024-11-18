"""
Author: Ayush Agarwal
"""
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

load_dotenv()

from ats_app.routers import users, jobs, resume 
from ats_app.database.models import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

# ENTITY_CHAIN = create_entity_extractor_chain()
# ATS_CHAIN = create_ats_chain()
@app.get("/")
def root():
    return {"message": "Welcome to the Job Portal API"}

app.include_router(users.router, prefix="/users")
app.include_router(jobs.router, prefix="/jobs")
app.include_router(resume.router, prefix="/resume")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
