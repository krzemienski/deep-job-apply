#!/bin/bash

# Create necessary directories
mkdir -p uploads
mkdir -p backend/logs
mkdir -p frontend/public/images

# Make the script executable
chmod +x init.sh

echo "Creating project structure..."

# Check if Python is installed
if command -v python3 &>/dev/null; then
    echo "Python is installed"
else
    echo "Python is not installed. Please install Python 3.11 or higher."
    exit 1
fi

# Check if Node.js is installed
if command -v node &>/dev/null; then
    echo "Node.js is installed"
else
    echo "Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

# Check if Docker is installed
if command -v docker &>/dev/null; then
    echo "Docker is installed"
else
    echo "Docker is not installed. Please install Docker to run the application in containers."
    exit 1
fi

# Check if Docker Compose is installed
if command -v docker-compose &>/dev/null; then
    echo "Docker Compose is installed"
else
    echo "Docker Compose is not installed. Please install Docker Compose to orchestrate the containers."
    exit 1
fi

echo "Project structure created successfully!"
echo ""
echo "To start the application in development mode:"
echo "1. Backend: cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && uvicorn main:app --reload"
echo "2. Frontend: cd frontend && npm install && npm run dev"
echo ""
echo "To start the application using Docker:"
echo "docker-compose up -d"
echo ""
echo "Access the application at:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000"
