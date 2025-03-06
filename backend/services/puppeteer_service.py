import aiohttp
import os
import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PuppeteerService:
    """
    Service to communicate with the Puppeteer automation service.
    """
    
    def __init__(self, base_url: str = None):
        """
        Initialize the Puppeteer service.
        
        Args:
            base_url: The base URL of the Puppeteer automation service.
        """
        # Use environment variable if provided, otherwise default to localhost
        self.base_url = base_url or os.environ.get("PUPPETEER_SERVICE_URL", "http://localhost:3001")
        logger.info(f"Initializing PuppeteerService with base_url: {self.base_url}")
        
    async def apply_to_job(
        self, 
        job_url: str, 
        resume_path: str, 
        resume_data: Dict[str, Any]
    ) -> tuple[bool, List[Dict[str, Any]]]:
        """
        Apply to a job using the Puppeteer automation service.
        
        Args:
            job_url: The URL of the job to apply to.
            resume_path: The path to the resume file.
            resume_data: Structured resume data.
            
        Returns:
            Tuple of (success, logs)
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/api/apply"
                payload = {
                    "jobUrl": job_url,
                    "resumePath": resume_path,
                    "resumeData": resume_data
                }
                
                logger.info(f"Sending request to Puppeteer service: {url}")
                logger.info(f"Job URL: {job_url}")
                logger.info(f"Resume path: {resume_path}")
                
                async with session.post(url, json=payload) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Error from Puppeteer service: {error_text}")
                        return False, [{
                            "timestamp": datetime.now().isoformat(),
                            "message": f"Error from automation service: {error_text}",
                            "level": "error"
                        }]
                    
                    result = await response.json()
                    return result["success"], result["logs"]
                    
        except Exception as e:
            logger.error(f"Error communicating with Puppeteer service: {str(e)}")
            return False, [{
                "timestamp": datetime.now().isoformat(),
                "message": f"Error communicating with automation service: {str(e)}",
                "level": "error"
            }]
    
    async def check_health(self) -> bool:
        """
        Check if the Puppeteer service is healthy.
        
        Returns:
            True if the service is healthy, False otherwise.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/health") as response:
                    return response.status == 200
        except Exception:
            return False
