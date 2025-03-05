import asyncio
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from backend.models import JobApplication, Resume, ApplicationStatus
from backend.automation.browser import apply_to_job_url


class JobApplicationService:
    """
    Service for processing job applications using browser automation.
    """

    def __init__(self, jobs_db: Dict[str, Dict], resumes_db: Dict[str, Dict]):
        self.jobs_db = jobs_db
        self.resumes_db = resumes_db

    async def process_application(self, application_id: str) -> bool:
        """
        Process a job application using browser automation.
        Returns True if the application was successful, False otherwise.
        """
        # Get the application from the database
        application = self.jobs_db.get(application_id)
        if not application:
            return False

        # Update status to processing
        application["status"] = ApplicationStatus.PROCESSING
        application["updated_at"] = datetime.now()
        application["logs"] = application.get("logs", [])

        # Add a log entry
        application["logs"].append(
            {
                "timestamp": datetime.now().isoformat(),
                "message": "Starting job application process",
                "level": "info",
            }
        )

        try:
            # Get the resume
            resume_id = application["resume_id"]
            resume_data = self.resumes_db.get(resume_id)
            if not resume_data:
                raise ValueError(f"Resume with ID {resume_id} not found")

            # Get the resume file path
            resume_path = resume_data["file_path"]
            if not os.path.exists(resume_path):
                raise ValueError(f"Resume file not found at {resume_path}")

            # Get the job URL
            job_url = application["job_url"]

            # Apply to the job
            success, logs = await apply_to_job_url(
                job_url, resume_path, resume_data["parsed_data"]
            )

            # Add browser automation logs to application logs
            for log in logs:
                application["logs"].append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "message": log["message"],
                        "level": log["level"],
                    }
                )

            # Update application status based on result
            if success:
                application["status"] = ApplicationStatus.SUCCEEDED
                application["logs"].append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "message": "Successfully applied to job",
                        "level": "info",
                    }
                )
            else:
                application["status"] = ApplicationStatus.FAILED
                application["error_message"] = "Failed to apply to job"
                application["logs"].append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "message": "Failed to apply to job",
                        "level": "error",
                    }
                )

            return success

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
            return False

        finally:
            # Update completion time
            application["completed_at"] = datetime.now()
            application["updated_at"] = datetime.now()


# Singleton instance
job_application_service = None


def get_job_application_service(jobs_db, resumes_db) -> JobApplicationService:
    """
    Get or create the JobApplicationService singleton instance.
    """
    global job_application_service
    if job_application_service is None:
        job_application_service = JobApplicationService(jobs_db, resumes_db)
    return job_application_service
