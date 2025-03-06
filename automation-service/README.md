# Deep Job Apply - Puppeteer Automation Service

This service handles browser automation for the Deep Job Apply application using Puppeteer. It provides a REST API that the Python backend can call to automate job applications.

## Features

- Uses Puppeteer with stealth plugins to avoid bot detection
- Handles various job board formats (Amazon, Google, Meta, etc.)
- Provides detailed logs of the application process
- Includes automatic fallback strategies for unknown job boards

## Setup

### Prerequisites

- Node.js 16+ and npm

### Installation

1. Navigate to the automation-service directory:
```
cd /path/to/deep-job-apply/automation-service
```

2. Install dependencies:
```
npm install
```

## Running the Service

Start the service:
```
npm start
```

For development with auto-restart:
```
npm run dev
```

The service will run on port 3001 by default (can be changed with the PORT environment variable).

## API Endpoints

### Apply to a Job

**POST /api/apply**

Request body:
```json
{
  "jobUrl": "https://example.com/job/1234",
  "resumePath": "/path/to/resume.pdf",
  "resumeData": {
    "name": "John Doe",
    "title": "Software Engineer",
    "summary": "Experienced software engineer...",
    "contact_info": {
      "email": "john@example.com",
      "phone": "123-456-7890"
    },
    "experience": ["Position 1", "Position 2"],
    "education": "Bachelor of Computer Science"
  }
}
```

Response:
```json
{
  "success": true,
  "logs": [
    {
      "timestamp": "2023-08-10T12:34:56.789Z",
      "message": "Starting job application",
      "level": "info"
    },
    ...
  ]
}
```

### Health Check

**GET /api/health**

Response:
```json
{
  "status": "healthy"
}
```

## Job Board Support

The service automatically detects job boards and applies appropriate strategies for:

- LinkedIn
- Indeed
- Glassdoor
- Monster
- ZipRecruiter
- Amazon
- Google
- Meta/Facebook
- Apple
- Netflix
- Microsoft
- Nvidia
- TikTok
- Disney
- General job boards (using a generic approach)

## Screenshots

The service generates screenshots during the application process for debugging purposes:
- `application-submitted.png`: Shows the page after submission
- `no-apply-button.png`: Created when apply button cannot be found

## Troubleshooting

- If the browser fails to launch, make sure all dependencies are installed: `sudo apt-get install gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget`

- Enable debug logs by setting the environment variable: `DEBUG=puppeteer:*`
