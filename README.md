# Deep Job Apply

An automated job application system using browser automation and AI to streamline the job application process.

## Overview

Deep Job Apply is a sophisticated automation system designed to streamline the job application process by leveraging browser automation and artificial intelligence. This application enables users to upload their résumé (in PDF format) and supply a list of job URLs. The system then autonomously navigates to each URL, detects relevant application elements (such as "Apply" buttons or form fields), and submits applications based on the résumé details and additional context.

## Features

- **User Authentication**: Secure registration and login system
- **Résumé Upload and Parsing**: Upload PDF résumés and automatically extract information
- **Job URL Management**: Add and manage job application URLs
- **Automated Application Process**: Automatically navigate to job listings and submit applications
- **Real-time Status Tracking**: Monitor application statuses and detailed logs
- **Dashboard**: View all applications and their statuses in one place

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Authentication**: JWT tokens
- **Browser Automation**: Playwright
- **PDF Parsing**: PyPDF2

### Frontend
- **Framework**: Next.js (React)
- **Styling**: Tailwind CSS
- **State Management**: React Hooks

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js (for local development)
- Python 3.11+ (for local development)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/deep-job-apply.git
   cd deep-job-apply
   ```

2. Create a `.env` file in the root directory (or use the provided one):
   ```
   # Backend settings
   SECRET_KEY=supersecretkey
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   BACKEND_CORS_ORIGINS=http://localhost:3000

   # Frontend settings
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. Set up test data (résumé and job URLs):
   ```bash
   # Run the setup script to copy the résumé and parse job URLs
   ./setup_test_data.py

   # This will:
   # - Copy the résumé file (docs/Nick_Krzemienski_072024_cv.pdf) to the uploads directory
   # - Parse job URLs from docs/jobs.md and save them to test_jobs.json
   # - Create a test_data.html file to view the test data
   ```

4. Start the application using Docker Compose:
   ```bash
   docker-compose up -d
   ```

5. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Test Data Viewer: Open test_data.html in your browser

### Local Development

#### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Playwright browsers:
   ```bash
   playwright install chromium
   ```

5. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

#### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

## Project Structure

```
deep-job-apply/
├── backend/                # FastAPI backend
│   ├── automation/         # Browser automation code
│   ├── models/             # Data models
│   ├── routers/            # API routes
│   ├── services/           # Business logic
│   ├── main.py             # Application entry point
│   └── Dockerfile          # Backend Docker configuration
├── frontend/               # Next.js frontend
│   ├── public/             # Static assets
│   ├── src/                # Source code
│   │   ├── app/            # Next.js app directory
│   │   │   ├── dashboard/  # Dashboard pages
│   │   │   ├── login/      # Login page
│   │   │   ├── register/   # Registration page
│   │   │   └── page.tsx    # Landing page
│   │   └── components/     # Reusable components
│   └── Dockerfile          # Frontend Docker configuration
├── uploads/                # Uploaded résumés
├── docker-compose.yml      # Docker Compose configuration
└── .env                    # Environment variables
```

## Usage

1. Register for an account
2. Upload your résumé
3. Add job URLs you want to apply to
4. The system will automatically apply to jobs using your résumé
5. Monitor the status of your applications in the dashboard

## Testing with Sample Data

The project includes sample data for testing purposes:

### Sample Résumé

The sample résumé file is located at `docs/Nick_Krzemienski_072024_cv.pdf`. This file is automatically copied to the `uploads` directory when you run the `setup_test_data.py` script.

### Sample Job URLs

The sample job URLs are parsed from `docs/jobs.md`, which contains a list of job postings from various companies. The script extracts the job titles, companies, and URLs and saves them to `test_jobs.json`.

### Testing Process

1. Run the setup script to prepare the test data:
   ```bash
   ./setup_test_data.py
   ```

2. Start the application:
   ```bash
   docker-compose up -d
   # or
   ./dev.sh
   ```

3. Open the test data viewer in your browser:
   ```bash
   open test_data.html
   ```

4. Register an account on the application (http://localhost:3000/register)

5. Log in to the application (http://localhost:3000/login)

6. Navigate to the dashboard and upload the résumé from the uploads directory

7. Add job URLs from the test data viewer

8. Start the application process and monitor the results

This testing process allows you to verify that the application correctly:
- Parses the résumé
- Navigates to job URLs
- Detects application elements
- Submits applications
- Tracks application status

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)
- [Playwright](https://playwright.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
