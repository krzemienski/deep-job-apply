import requests
import json
import time
import sys

# API configuration
BASE_URL = "http://localhost:8000"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNzQxMjM2OTYxfQ.bKpLpg1qetRBBx-bJG3a-0yOOpDHP5_IE5Do0FhHo9M"
HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Get the resume ID
def get_resume_id():
    response = requests.get(f"{BASE_URL}/api/resumes/", headers=HEADERS)
    if response.status_code == 200:
        resumes = response.json()
        if resumes:
            return resumes[0]["id"]
    return None

# Apply for a job
def apply_for_job(job_url, resume_id):
    data = {
        "resume_id": resume_id,
        "job_url": job_url
    }
    response = requests.post(f"{BASE_URL}/api/jobs/", headers=HEADERS, json=data)
    return response.json() if response.status_code in (200, 201) else None

# Check job application status
def check_job_status(application_id):
    response = requests.get(f"{BASE_URL}/api/jobs/{application_id}", headers=HEADERS)
    return response.json() if response.status_code == 200 else None

# Load test jobs from JSON file
def load_test_jobs(file_path="test_jobs.json"):
    with open(file_path, "r") as f:
        return json.load(f)

# Main function to test job applications
def main():
    # Get resume ID
    resume_id = get_resume_id()
    if not resume_id:
        print("No resume found. Please upload a resume first.")
        sys.exit(1)
    
    print(f"Using resume with ID: {resume_id}")
    
    # Load test jobs
    test_jobs = load_test_jobs()
    print(f"Loaded {len(test_jobs)} test jobs")
    
    # Select jobs from different companies for diverse testing
    test_selection = [
        next(job for job in test_jobs if job['company'] == 'Amazon'),
        next(job for job in test_jobs if job['company'] == 'Google'),
        next(job for job in test_jobs if job['company'] == 'Meta'),
        next(job for job in test_jobs if job['company'] == 'Apple'),
        next(job for job in test_jobs if job['company'] == 'Netflix')
    ]
    
    # Apply for jobs (limit to 5 for testing)
    job_applications = []
    for i, job in enumerate(test_selection):
        print(f"\nApplying for job {i+1}/5: {job['title']} at {job['company']}")
        
        # Apply for the job
        application = apply_for_job(job['url'], resume_id)
        if application:
            print(f"Job application created. ID: {application['id']}")
            job_applications.append(application['id'])
        else:
            print(f"Failed to create job application for {job['title']}")
        
        # Wait a bit to avoid overwhelming the server
        time.sleep(1)
    
    # Check status of applications after a short delay
    if job_applications:
        print("\nWaiting for job applications to process...")
        time.sleep(5)
        
        print("\nJob Application Status:")
        for app_id in job_applications:
            status = check_job_status(app_id)
            if status:
                print(f"ID: {app_id} - Status: {status['status']} - URL: {status['job_url']}")
            else:
                print(f"ID: {app_id} - Failed to retrieve status")
    else:
        print("No job applications were created.")

if __name__ == "__main__":
    main()
