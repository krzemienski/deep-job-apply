from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
import os
import uuid
from typing import List, Optional
import shutil
from datetime import datetime

from backend.models import Resume, ResumeData, ResumeResponse, ResumeUpload, User
from backend.routers.users import get_current_active_user

# Create router
router = APIRouter()

# Mock database (replace with actual database in production)
fake_resumes_db = {}

# Directory for storing resume files
UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Helper functions
def parse_resume_pdf(file_path: str) -> ResumeData:
    """
    Parse a resume PDF file and extract structured data.
    This is a placeholder implementation. In a real application,
    you would use libraries like PyPDF2, pdfminer.six, or similar.
    """
    # For demonstration purposes, we'll use the sample resume data from the prompt
    return ResumeData(
        name="Nick Krzemienski",
        title="Engineering Lead, Video Innovations @ fuboTV",
        summary="Over 12 years of experience in software engineering management and technical leadership.",
        core_experience=[
            "Engineering Lead, Video Innovations, fuboTV Inc.",
            "Engineering Lead, VOD Encoding & Operations, fuboTV Inc.",
            "Engineering Manager, AppleTV & Roku, fuboTV Inc.",
            "Software Engineer, iOS, fuboTV Inc.",
            "Principal Developer & Founder, KODA LABS INC.",
            "Squad Leader, United States Marine Corps Reserve",
            "Founder & Managing Director for various projects",
            "Mobile Developer, SHODOGG",
            "Ops Intern, Argus Information and Advisory Services",
        ],
        education=["Bachelor of Computer Science, Iona College"],
        portfolio={
            "website": "awesome.video",
            "github": "github.com/krzemienski",
            "twitter": "twitter.com/nkrzemienski",
        },
        contact_info={
            "email": "krzemienski@gmail.com",
        },
        skills=[
            "Software Engineering Management",
            "Technical Leadership",
            "Mobile Development",
            "Web Development",
            "OTT Video",
            "Swift",
            "FFmpeg",
            "ISO Standards",
            "Encoding Workflows",
            "AWS",
            "Docker",
            "Kubernetes",
        ],
    )


# Endpoints
@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...), current_user: User = Depends(get_current_active_user)
):
    """
    Upload a resume file (PDF) and parse it to extract structured data.
    """
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported",
        )

    # Generate a unique filename
    file_id = str(uuid.uuid4())
    filename = f"{file_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse the resume
    try:
        parsed_data = parse_resume_pdf(file_path)
    except Exception as e:
        os.remove(file_path)  # Clean up on error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error parsing resume: {str(e)}",
        )

    # Create resume record
    resume = Resume(
        user_id=current_user.id,
        filename=file.filename,
        file_path=file_path,
        parsed_data=parsed_data,
    )

    # Store in database
    fake_resumes_db[resume.id] = resume.dict()

    # Return response
    return ResumeResponse(
        id=resume.id,
        filename=resume.filename,
        parsed_data=resume.parsed_data,
        created_at=resume.created_at,
    )


@router.get("/", response_model=List[ResumeResponse])
async def list_resumes(current_user: User = Depends(get_current_active_user)):
    """
    List all resumes for the current user.
    """
    user_resumes = [
        ResumeResponse(
            id=resume_id,
            filename=resume_data["filename"],
            parsed_data=resume_data.get("parsed_data"),
            created_at=resume_data["created_at"],
        )
        for resume_id, resume_data in fake_resumes_db.items()
        if resume_data["user_id"] == current_user.id
    ]
    return user_resumes


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: str, current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific resume by ID.
    """
    if resume_id not in fake_resumes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found"
        )

    resume_data = fake_resumes_db[resume_id]

    # Check if the resume belongs to the current user
    if resume_data["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resume",
        )

    return ResumeResponse(
        id=resume_id,
        filename=resume_data["filename"],
        parsed_data=resume_data.get("parsed_data"),
        created_at=resume_data["created_at"],
    )


@router.get("/{resume_id}/download")
async def download_resume(
    resume_id: str, current_user: User = Depends(get_current_active_user)
):
    """
    Download the original resume file.
    """
    if resume_id not in fake_resumes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found"
        )

    resume_data = fake_resumes_db[resume_id]

    # Check if the resume belongs to the current user
    if resume_data["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resume",
        )

    file_path = resume_data["file_path"]
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resume file not found"
        )

    return FileResponse(
        file_path, filename=resume_data["filename"], media_type="application/pdf"
    )


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: str, current_user: User = Depends(get_current_active_user)
):
    """
    Delete a resume.
    """
    if resume_id not in fake_resumes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found"
        )

    resume_data = fake_resumes_db[resume_id]

    # Check if the resume belongs to the current user
    if resume_data["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this resume",
        )

    # Delete the file
    file_path = resume_data["file_path"]
    if os.path.exists(file_path):
        os.remove(file_path)

    # Remove from database
    del fake_resumes_db[resume_id]

    return None
