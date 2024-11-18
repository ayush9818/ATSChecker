"""
Author: Ayush Agarwal
"""
import os
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint, JSON
from sqlalchemy.orm import relationship, sessionmaker, declarative_base


DATABASE_URI = os.environ['DATABASE_URI']

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Users(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    contact_number = Column(String(15), nullable=True)

    # Relationships
    jobs = relationship("Jobs", secondary="UserJobs", back_populates="users")
    resumes = relationship("UserResumes", back_populates="user")


class Jobs(Base):
    __tablename__ = 'Jobs'

    job_id = Column(Integer, primary_key=True, autoincrement=True)
    job_title = Column(Text, nullable=False)
    job_description = Column(Text, nullable=False)
    employment_type = Column(Text, nullable=False)
    company_name = Column(Text, nullable=False)

    # Relationships
    users = relationship("Users", secondary="UserJobs", back_populates="jobs")


class UserJobs(Base):
    __tablename__ = 'UserJobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id', ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey('Jobs.job_id', ondelete="CASCADE"), nullable=False)
    resume_id = Column(Integer, ForeignKey('UserResumes.resume_id', ondelete="CASCADE"), nullable=False)

    # To enforce user apply to one job once
    __table_args__ = (
        UniqueConstraint('user_id', 'job_id', name='unique_user_job'),
    )


class UserResumes(Base):
    __tablename__ = 'UserResumes'

    resume_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id', ondelete="CASCADE"), nullable=False)
    resume_path = Column(String(512), nullable=False)
    years_of_experience = Column(Integer, nullable=True)
    education = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)
    work_experience = Column(Text, nullable=True)

    # Relationships
    user = relationship("Users", back_populates="resumes")


def init_database():
    Base.metadata.create_all(engine)
    print("Database Schema Initialised")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    init_database()