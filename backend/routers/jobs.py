from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import asyncio

from backend.models import (
    JobApplication,
    JobApplicationCreate,
    JobApplicationResponse,
    JobApplicationLog,
    ApplicationStatus,
    User,
    Resume,
)
from backend.routers.users import get_current_active_user

# Create router
router = APIRouter()

# Mock database (replace with actual database in production)
fake_jobs_db = {}
fake_resumes_db = {}  # This would be imported from the resumes module in a real app


# Helper functions
async def process_job_application(application_id: str):
    """
    Process a job application in the background.
    This function would use browser automation to apply for the job.
    """
    # Get the application from the database
    application = fake_jobs_db.get(application_id)
    if not application:
        return

    # Update status to processing
    application["status"] = ApplicationStatus.PROCESSING
    application["updated_at"] = datetime.now()

    # Add a log entry
    application["logs"].append(
        {
            "timestamp": datetime.now().isoformat(),
            "message": "Starting job application process",
            "level": "info",
        }
    )

    try:
        # In a real implementation, this would use Playwright/Selenium/Puppeteer
        # to automate the job application process
        await asyncio.sleep(5)  # Simulate processing time

        # Simulate success (in a real app, this would depend on the automation result)
        application["status"] = ApplicationStatus.SUCCEEDED
        application["logs"].append(
            {
                "timestamp": datetime.now().isoformat(),
                "message": "Successfully applied to job",
                "level": "info",
            }
        )
    except Exception as e:
        # Handle errors
        application["status"] = ApplicationStatus.FAILED
        application["error_message"] = str(e)
        application["logs"].append(
            {
                "timestamp": datetime.now().isoformat(),
                "message": f"Error applying to job: {str(e)}",
                "level": "error",
            }
        )

    # Update completion time
    application["completed_at"] = datetime.now()
    application["updated_at"] = datetime.now()


# Endpoints
@router.post("/", response_model=JobApplicationResponse)
async def create_job_application(
    job_create: JobApplicationCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new job application task.
    """
    # Check if the resume exists and belongs to the user
    if job_create.resume_id not in fake_resumes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found"
        )

    resume_data = fake_resumes_db[job_create.resume_id]
    if resume_data["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to use this resume",
        )

    # Create job application
    job_application = JobApplication(
        user_id=current_user.id,
        resume_id=job_create.resume_id,
        job_url=job_create.job_url,
    )

    # Store in database
    fake_jobs_db[job_application.id] = job_application.dict()

    # Start background task to process the application
    background_tasks.add_task(process_job_application, job_application.id)

    # Return response
    return JobApplicationResponse(
        id=job_application.id,
        job_url=job_application.job_url,
        status=job_application.status,
        created_at=job_application.created_at,
        completed_at=job_application.completed_at,
    )


@router.get("/", response_model=List[JobApplicationResponse])
async def list_job_applications(
    status: Optional[ApplicationStatus] = None,
    current_user: User = Depends(get_current_active_user),
):
    """
    List all job applications for the current user.
    Optionally filter by status.
    """
    user_applications = [
        JobApplicationResponse(
            id=app_id,
            job_url=app_data["job_url"],
            status=app_data["status"],
            error_message=app_data.get("error_message"),
            created_at=app_data["created_at"],
            completed_at=app_data.get("completed_at"),
        )
        for app_id, app_data in fake_jobs_db.items()
        if app_data["user_id"] == current_user.id
        and (status is None or app_data["status"] == status)
    ]
    return user_applications


@router.get("/{application_id}", response_model=JobApplicationResponse)
async def get_job_application(
    application_id: str, current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific job application by ID.
    """
    if application_id not in fake_jobs_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job application not found"
        )

    app_data = fake_jobs_db[application_id]

    # Check if the application belongs to the current user
    if app_data["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this job application",
        )

    return JobApplicationResponse(
        id=application_id,
        job_url=app_data["job_url"],
        status=app_data["status"],
        error_message=app_data.get("error_message"),
        created_at=app_data["created_at"],
        completed_at=app_data.get("completed_at"),
    )


@router.get("/{application_id}/logs", response_model=JobApplicationLog)
async def get_job_application_logs(
    application_id: str, current_user: User = Depends(get_current_active_user)
):
    """
    Get logs for a specific job application.
    """
    if application_id not in fake_jobs_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job application not found"
        )

    app_data = fake_jobs_db[application_id]

    # Check if the application belongs to the current user
    if app_data["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this job application",
        )

    return JobApplicationLog(
        application_id=application_id,
        logs=app_data.get("logs", []),
    )


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_application(
    application_id: str, current_user: User = Depends(get_current_active_user)
):
    """
    Delete a job application.
    """
    if application_id not in fake_jobs_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job application not found"
        )

    app_data = fake_jobs_db[application_id]

    # Check if the application belongs to the current user
    if app_data["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this job application",
        )

    # Remove from database
    del fake_jobs_db[application_id]

    return None


@router.post("/{application_id}/retry", response_model=JobApplicationResponse)
async def retry_job_application(
    application_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retry a failed job application.
    """
    if application_id not in fake_jobs_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job application not found"
        )

    app_data = fake_jobs_db[application_id]

    # Check if the application belongs to the current user
    if app_data["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to retry this job application",
        )

    # Check if the application is in a failed state
    if app_data["status"] != ApplicationStatus.FAILED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only failed applications can be retried",
        )

    # Reset application status
    app_data["status"] = ApplicationStatus.PENDING
    app_data["error_message"] = None
    app_data["updated_at"] = datetime.now()
    app_data["completed_at"] = None

    # Add a log entry
    app_data["logs"].append(
        {
            "timestamp": datetime.now().isoformat(),
            "message": "Retrying job application",
            "level": "info",
        }
    )

    # Start background task to process the application
    background_tasks.add_task(process_job_application, application_id)

    return JobApplicationResponse(
        id=application_id,
        job_url=app_data["job_url"],
        status=app_data["status"],
        error_message=app_data.get("error_message"),
        created_at=app_data["created_at"],
        completed_at=app_data.get("completed_at"),
    )
