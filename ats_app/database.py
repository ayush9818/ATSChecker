"""
Author: Ayush Agarwal
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Users(Base):
    __tablename__ = 'Users'

    UserID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    Email = Column(String(255), nullable=False, unique=True)
    ContactNumber = Column(String(15), nullable=True)

    # Relationships
    jobs = relationship("Jobs", secondary="UserJobs", back_populates="users")
    resumes = relationship("UserResumes", back_populates="user")


class Jobs(Base):
    __tablename__ = 'Jobs'

    JobID = Column(Integer, primary_key=True, autoincrement=True)
    JobDescription = Column(Text, nullable=False)

    # Relationships
    users = relationship("Users", secondary="UserJobs", back_populates="jobs")


class UserJobs(Base):
    __tablename__ = 'UserJobs'

    UserJobID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('Users.UserID', ondelete="CASCADE"), nullable=False)
    JobID = Column(Integer, ForeignKey('Jobs.JobID', ondelete="CASCADE"), nullable=False)


class UserResumes(Base):
    __tablename__ = 'UserResumes'

    ResumeID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('Users.UserID', ondelete="CASCADE"), nullable=False)
    ResumePath = Column(String(512), nullable=False)
    YearsOfExperience = Column(Integer, nullable=True)
    College = Column(String(255), nullable=True)
    Skills = Column(Text, nullable=True)
    Misc = Column(Text, nullable=True)

    # Relationships
    user = relationship("Users", back_populates="resumes")


def create_sqlite_db(database_name="job_portal.db"):
    engine = create_engine(f"sqlite:///{database_name}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session

def get_db():
    pass 