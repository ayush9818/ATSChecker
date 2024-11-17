"""
Author: Ayush Agarwal
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ats_app.database import Users, get_db
from ats_app.models.response_schema import CreateUserRequest


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=dict)
def create_user(request: CreateUserRequest, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(Users).filter(Users.Email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists.")

    # Create and add the user
    new_user = Users(Name=request.name, Email=request.email, ContactNumber=request.contact_number)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.UserID}
