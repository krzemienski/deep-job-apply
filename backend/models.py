from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
import uuid


# Enums
class ApplicationStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


# Database Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    hashed_password: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ResumeData(BaseModel):
    name: str
    title: str
    summary: str
    core_experience: List[str]
    education: List[str]
    portfolio: Dict[str, str]
    contact_info: Dict[str, str]
    skills: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None


class Resume(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    filename: str
    file_path: str
    parsed_data: Optional[ResumeData] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class JobApplication(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    resume_id: str
    job_url: HttpUrl
    status: ApplicationStatus = ApplicationStatus.PENDING
    logs: List[Dict[str, Any]] = []
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


# API Request/Response Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class ResumeUpload(BaseModel):
    filename: str


class ResumeResponse(BaseModel):
    id: str
    filename: str
    parsed_data: Optional[ResumeData] = None
    created_at: datetime


class JobApplicationCreate(BaseModel):
    resume_id: str
    job_url: HttpUrl


class JobApplicationResponse(BaseModel):
    id: str
    job_url: HttpUrl
    status: ApplicationStatus
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None


class JobApplicationLog(BaseModel):
    application_id: str
    logs: List[Dict[str, Any]]
