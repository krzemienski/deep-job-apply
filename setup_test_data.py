#!/usr/bin/env python3
"""
Setup test data for the Deep Job Apply application.
This script:
1. Copies the résumé file to the uploads directory
2. Parses job URLs from the markdown file
3. Creates a JSON file with the job URLs for testing
"""

import os
import json
import re
import shutil
from pathlib import Path

# Create uploads directory if it doesn't exist
os.makedirs('uploads', exist_ok=True)

# Copy résumé file to uploads directory
resume_path = 'docs/Nick_Krzemienski_072024_cv.pdf'
if os.path.exists(resume_path):
    shutil.copy(resume_path, 'uploads/')
    print(f"✅ Copied résumé file to uploads directory: {resume_path}")
else:
    print(f"❌ Résumé file not found: {resume_path}")

# Parse job URLs from markdown file
jobs_path = 'docs/jobs.md'
job_urls = []

if os.path.exists(jobs_path):
    with open(jobs_path, 'r') as f:
        content = f.read()

    # Extract URLs using regex
    # Look for markdown links in the format [text](url)
    url_pattern = r'\[Link\]\((https?://[^\s\)]+)\)'
    matches = re.findall(url_pattern, content)

    # Extract job titles and companies
    lines = content.split('\n')
    jobs = []

    for line in lines:
        if '|' in line and '[Link]' in line:
            parts = line.split('|')
            if len(parts) >= 4:  # Should have job title, company, and URL columns
                job_title = parts[1].strip()
                company = parts[2].strip()
                url_match = re.search(url_pattern, parts[3])
                if url_match:
                    url = url_match.group(1)
                    jobs.append({
                        "title": job_title,
                        "company": company,
                        "url": url
                    })

    # Save job URLs to JSON file
    if jobs:
        with open('test_jobs.json', 'w') as f:
            json.dump(jobs, f, indent=2)
        print(f"✅ Parsed {len(jobs)} job URLs from {jobs_path} and saved to test_jobs.json")
    else:
        print(f"❌ No job URLs found in {jobs_path}")
else:
    print(f"❌ Jobs markdown file not found: {jobs_path}")

# Create a simple HTML file to display the test data
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deep Job Apply - Test Data</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2 {
            color: #2563eb;
        }
        .job-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .job-card {
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 16px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .job-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .company {
            color: #6b7280;
            font-size: 0.9rem;
        }
        .title {
            font-weight: 600;
            margin: 8px 0;
        }
        .apply-btn {
            display: inline-block;
            background-color: #2563eb;
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
            text-decoration: none;
            font-weight: 500;
            margin-top: 12px;
        }
        .apply-btn:hover {
            background-color: #1d4ed8;
        }
        .resume-section {
            margin-top: 40px;
            padding: 20px;
            background-color: #f9fafb;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <h1>Deep Job Apply - Test Data</h1>

    <div class="resume-section">
        <h2>Test Résumé</h2>
        <p>The following résumé file has been copied to the uploads directory:</p>
        <p><strong>File:</strong> Nick_Krzemienski_072024_cv.pdf</p>
        <p>This file will be used for testing the application's résumé parsing and job application functionality.</p>
    </div>

    <h2>Test Job URLs</h2>
    <p>The following job URLs have been parsed from the jobs.md file and can be used for testing:</p>

    <div class="job-list" id="jobList">
        <!-- Job cards will be inserted here by JavaScript -->
    </div>

    <script>
        // Fetch and display job data
        fetch('test_jobs.json')
            .then(response => response.json())
            .then(jobs => {
                const jobList = document.getElementById('jobList');

                jobs.forEach(job => {
                    const jobCard = document.createElement('div');
                    jobCard.className = 'job-card';

                    jobCard.innerHTML = `
                        <div class="company">${job.company}</div>
                        <div class="title">${job.title}</div>
                        <a href="${job.url}" target="_blank" class="apply-btn">View Job</a>
                    `;

                    jobList.appendChild(jobCard);
                });
            })
            .catch(error => {
                console.error('Error loading job data:', error);
                document.getElementById('jobList').innerHTML = '<p>Error loading job data. Please run setup_test_data.py first.</p>';
            });
    </script>
</body>
</html>
"""

with open('test_data.html', 'w') as f:
    f.write(html_content)
print("✅ Created test_data.html to display test data")

print("\nSetup complete! You can now:")
print("1. Run the application using 'docker-compose up' or './dev.sh'")
print("2. Open test_data.html in your browser to view the test data")
print("3. Use the test data to test the application's functionality")
