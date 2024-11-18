-- Create the database
CREATE DATABASE JobPortal;
USE JobPortal;

-- User Table: Stores user details
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    ContactNumber VARCHAR(15) NULL,
);

-- Jobs Table: Stores job details
CREATE TABLE Jobs (
    JobID INT AUTO_INCREMENT PRIMARY KEY,
    JobDescription TEXT NOT NULL,
);

-- UserJobs Table: Junction table for many-to-many relationship between Users and Jobs
CREATE TABLE UserJobs (
    UserJobID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    JobID INT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (JobID) REFERENCES Jobs(JobID) ON DELETE CASCADE
);

-- UserResume Table: Stores user resumes and parsed NER details
CREATE TABLE UserResumes (
    ResumeID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    ResumePath VARCHAR(512) NOT NULL, -- Path to S3 bucket
    YearsOfExperience INT NULL,       -- Parsed NER column: YOE
    College VARCHAR(255) NULL,        -- Parsed NER column: College
    Skills TEXT NULL,                 -- Parsed NER column: Skills
    Misc TEXT NULL,                   -- Parsed NER column: Miscellaneous
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);