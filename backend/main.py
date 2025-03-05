from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import uvicorn
import os
from typing import List, Optional

# Import routers
from backend.routers import users, resumes, jobs

# Create FastAPI app
app = FastAPI(
    title="Deep Job Apply",
    description="Automated job application system using browser automation and AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Deep Job Apply API"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(resumes.router, prefix="/api/resumes", tags=["resumes"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
