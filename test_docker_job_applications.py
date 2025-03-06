import requests
import json
import time
import sys
import argparse
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='Test job applications using Docker containers')
    parser.add_argument('--host', default='localhost', help='Backend host (default: localhost)')
    parser.add_argument('--test-jobs', default='test_jobs.json', help='Path to test jobs JSON file')
    parser.add_argument('--limit', type=int, default=2, help='Maximum number of jobs to test')
    parser.add_argument('--wait-time', type=int, default=30, help='Time to wait for job processing in seconds')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output with logs')
    return parser.parse_args()

def get_auth_token(base_url):
    """Get authentication token by logging in"""
    login_data = {
        "username": "test@example.com",
        "password": "password123"
    }
    response = requests.post(f"{base_url}/api/users/token", json=login_data)
    if response.status_code == 200:
        return response.json().get("access_token")
    print(f"Failed to authenticate: {response.status_code} - {response.text}")
    return None

def get_or_create_resume(base_url, headers):
    """Get existing resume or create a new one if none exists"""
    # First check if we have resumes
    response = requests.get(f"{base_url}/api/resumes/", headers=headers)
    if response.status_code == 200:
        resumes = response.json()
        if resumes:
            print(f"Found existing resume with ID: {resumes[0]['id']}")
            return resumes[0]["id"]
    
    # If no resume exists, create one
    print("No resume found, creating a test resume...")
    
    # Prepare test resume metadata
    resume_data = {
        "name": "Nick Krzemienski Resume",
        "description": "Engineering Lead with video experience"
    }
    
    # Create the resume metadata first
    response = requests.post(f"{base_url}/api/resumes/", headers=headers, json=resume_data)
    if response.status_code != 201:
        print(f"Failed to create resume metadata: {response.status_code} - {response.text}")
        return None
    
    resume_id = response.json()["id"]
    print(f"Created resume metadata with ID: {resume_id}")
    
    # Sample PDF path (in Docker context, this would be a shared volume path)
    sample_pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_resume.pdf")
    
    # Check if sample PDF exists, if not create a simple one
    if not os.path.exists(sample_pdf_path):
        try:
            from reportlab.pdfgen import canvas
            c = canvas.Canvas(sample_pdf_path)
            c.drawString(100, 750, "Nick Krzemienski")
            c.drawString(100, 730, "Engineering Lead, Video Innovations @ fuboTV")
            c.drawString(100, 710, "Email: krzemienski@gmail.com")
            c.drawString(100, 690, "Website: awesome.video")
            c.drawString(100, 670, "Over 12 years of experience in software engineering management")
            c.save()
            print(f"Created sample resume PDF at {sample_pdf_path}")
        except Exception as e:
            print(f"Could not create sample PDF: {str(e)}")
            return resume_id  # Return ID even without PDF for testing
    
    # Upload the resume file if it exists
    if os.path.exists(sample_pdf_path):
        with open(sample_pdf_path, 'rb') as f:
            file_dict = {'file': (os.path.basename(sample_pdf_path), f, 'application/pdf')}
            # Remove Content-Type header for multipart file upload
            upload_headers = headers.copy()
            if 'Content-Type' in upload_headers:
                del upload_headers['Content-Type']
            
            response = requests.post(
                f"{base_url}/api/resumes/{resume_id}/upload",
                headers=upload_headers,
                files=file_dict
            )
            if response.status_code == 200:
                print(f"Successfully uploaded resume file for ID: {resume_id}")
            else:
                print(f"Failed to upload resume file: {response.status_code} - {response.text}")
    
    return resume_id

def apply_for_job(base_url, headers, job_url, resume_id):
    """Apply for a job with the given URL and resume ID"""
    data = {
        "resume_id": resume_id,
        "job_url": job_url
    }
    response = requests.post(f"{base_url}/api/jobs/", headers=headers, json=data)
    if response.status_code in (200, 201):
        return response.json()
    print(f"Failed to create job application: {response.status_code} - {response.text}")
    return None

def check_job_status(base_url, headers, application_id, verbose=False):
    """Check job application status"""
    response = requests.get(f"{base_url}/api/jobs/{application_id}", headers=headers)
    if response.status_code == 200:
        result = response.json()
        if verbose and "logs" in result:
            print("\nApplication Logs:")
            for log in result["logs"]:
                print(f"{log.get('timestamp', '')} [{log.get('level', 'info')}] {log.get('message', '')}")
        return result
    print(f"Failed to retrieve job status: {response.status_code} - {response.text}")
    return None

def load_test_jobs(file_path):
    """Load test jobs from JSON file"""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading test jobs: {str(e)}")
        return []

def main():
    args = parse_arguments()
    
    # Configure API settings
    base_url = f"http://{args.host}:8001"
    print(f"Testing job applications with backend at {base_url}")
    
    # Get authentication token
    token = get_auth_token(base_url)
    if not token:
        print("Authentication failed. Please check your credentials.")
        sys.exit(1)
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Get or create resume
    resume_id = get_or_create_resume(base_url, headers)
    if not resume_id:
        print("Failed to get or create a resume. Exiting.")
        sys.exit(1)
    
    print(f"Using resume with ID: {resume_id}")
    
    # Load test jobs
    test_jobs = load_test_jobs(args.test_jobs)
    if not test_jobs:
        print("No test jobs found. Please check your test_jobs.json file.")
        sys.exit(1)
    
    print(f"Loaded {len(test_jobs)} test jobs")
    
    # Select a diverse set of job boards for testing
    companies = ['Amazon', 'Google', 'Meta', 'Apple', 'Netflix']
    test_selection = []
    
    for company in companies:
        company_jobs = [job for job in test_jobs if job['company'] == company]
        if company_jobs:
            test_selection.append(company_jobs[0])
    
    # Limit the number of jobs to test
    test_selection = test_selection[:args.limit]
    print(f"Selected {len(test_selection)} jobs for testing")
    
    # Apply for jobs
    job_applications = []
    for i, job in enumerate(test_selection):
        print(f"\nApplying for job {i+1}/{len(test_selection)}: {job['title']} at {job['company']}")
        
        # Apply for the job
        application = apply_for_job(base_url, headers, job['url'], resume_id)
        if application:
            print(f"Job application created. ID: {application['id']}")
            job_applications.append({
                'id': application['id'],
                'title': job['title'],
                'company': job['company'],
                'url': job['url']
            })
        else:
            print(f"Failed to create job application for {job['title']}")
        
        # Wait a bit to avoid overwhelming the server
        time.sleep(2)
    
    # Check status of applications after a delay
    if job_applications:
        print(f"\nWaiting {args.wait_time} seconds for job applications to process...")
        time.sleep(args.wait_time)
        
        print("\nJob Application Status:")
        successful = 0
        failed = 0
        
        for app in job_applications:
            status = check_job_status(base_url, headers, app['id'], args.verbose)
            if status:
                result = f"ID: {app['id']} - Status: {status['status']} - Title: {app['title']} - Company: {app['company']}"
                print(result)
                
                if status['status'] == 'succeeded':
                    successful += 1
                elif status['status'] == 'failed':
                    failed += 1
            else:
                print(f"ID: {app['id']} - Failed to retrieve status")
        
        print(f"\nSummary: {successful} succeeded, {failed} failed, {len(job_applications) - successful - failed} processing")
    else:
        print("No job applications were created.")

if __name__ == "__main__":
    main()
