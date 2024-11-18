"""
Author: Ayush Agarwal
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from ats_app.database import models 
from ats_app.database.models import get_db
from ats_app.models import response_schema as schemas


router = APIRouter(tags=["users"])

@router.get("/", response_model=List[schemas.UserResponse])
def fetch_users(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    name: Optional[str] = Query(None, description="Filter by user name"),
    email: Optional[str] = Query(None, description="Filter by user email"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Users)

    if user_id is not None:
        query = query.filter(models.Users.user_id == user_id)
    if name is not None:
        query = query.filter(models.Users.name == name)
    if email is not None:
        query = query.filter(models.Users.email == email)

    users = query.all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found with the provided filters.")
    return users

@router.post("/", response_model=schemas.UserResponse)
def create_user(request: schemas.CreateUserRequest, db: Session = Depends(get_db)):
    existing_user = db.query(models.Users).filter(models.Users.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists.")

    new_user = models.Users(name=request.name, email=request.email, contact_number=request.contact_number)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print("User Created")
    return new_user

@router.post("/resume/upload")
def upload_resume():
    pass