from playwright.async_api import async_playwright, Page
import asyncio
import logging
from typing import List, Dict, Any, Optional, Callable
import re
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JobApplier:
    """
    Class for automating job applications using Playwright.
    """

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.logs = []

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def start(self):
        """Start the browser."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

        # Set up event listeners
        self.page.on("console", lambda msg: self._log(f"Console: {msg.text}", "debug"))
        self.page.on("pageerror", lambda err: self._log(f"Page error: {err}", "error"))

    async def close(self):
        """Close the browser."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    def _log(self, message: str, level: str = "info"):
        """Add a log entry."""
        if level == "error":
            logger.error(message)
        elif level == "warning":
            logger.warning(message)
        elif level == "debug":
            logger.debug(message)
        else:
            logger.info(message)

        self.logs.append(
            {
                "timestamp": asyncio.get_event_loop().time(),
                "message": message,
                "level": level,
            }
        )

    async def navigate(self, url: str, wait_until: str = "networkidle"):
        """Navigate to a URL."""
        self._log(f"Navigating to {url}")
        await self.page.goto(url, wait_until=wait_until)
        self._log(f"Loaded page: {self.page.url}")

    async def find_apply_button(self) -> Optional[str]:
        """
        Find the 'Apply' button on the page.
        Returns the selector if found, None otherwise.
        """
        self._log("Looking for apply button")

        # Common selectors for apply buttons
        apply_button_selectors = [
            "button:has-text('Apply')",
            "a:has-text('Apply')",
            "button:has-text('Apply Now')",
            "a:has-text('Apply Now')",
            "button:has-text('Easy Apply')",
            "button:has-text('Quick Apply')",
            "[aria-label*='apply' i]",
            "[data-automation*='apply' i]",
        ]

        for selector in apply_button_selectors:
            try:
                button = await self.page.wait_for_selector(selector, timeout=1000)
                if button:
                    self._log(f"Found apply button with selector: {selector}")
                    return selector
            except Exception:
                continue

        self._log("Could not find apply button", "warning")
        return None

    async def fill_form(self, resume_data):
        """
        Fill out the job application form using resume data.
        This is a simplified implementation that would need to be expanded
        for real-world use.
        """
        self._log("Filling out application form")

        # Common form field selectors and their corresponding resume data
        form_fields = {
            "input[name*='name' i], input[placeholder*='name' i]": resume_data.name,
            "input[name*='email' i], input[placeholder*='email' i]": resume_data.contact_info.get(
                "email"
            ),
            "input[name*='phone' i], input[placeholder*='phone' i]": resume_data.contact_info.get(
                "phone", ""
            ),
            "textarea[name*='summary' i], textarea[placeholder*='summary' i], textarea[name*='about' i]": resume_data.summary,
        }

        for selector, value in form_fields.items():
            if value:
                try:
                    field = await self.page.wait_for_selector(selector, timeout=1000)
                    if field:
                        await field.fill(value)
                        self._log(f"Filled field {selector} with value")
                except Exception as e:
                    self._log(f"Error filling field {selector}: {str(e)}", "warning")

        self._log("Form filling completed")

    async def upload_resume(self, resume_path: str):
        """
        Upload a resume file.
        """
        self._log(f"Attempting to upload resume from {resume_path}")

        # Common file input selectors
        file_input_selectors = [
            "input[type='file']",
            "input[accept='.pdf']",
            "input[accept='application/pdf']",
            "input[name*='resume' i]",
            "input[name*='cv' i]",
        ]

        for selector in file_input_selectors:
            try:
                file_input = await self.page.wait_for_selector(selector, timeout=1000)
                if file_input:
                    await file_input.set_input_files(resume_path)
                    self._log(f"Uploaded resume using selector: {selector}")
                    return True
            except Exception as e:
                self._log(f"Error with file input {selector}: {str(e)}", "debug")

        self._log("Could not find file input for resume upload", "warning")
        return False

    async def submit_application(self):
        """
        Submit the job application.
        """
        self._log("Attempting to submit application")

        # Common submit button selectors
        submit_button_selectors = [
            "button[type='submit']",
            "button:has-text('Submit')",
            "button:has-text('Apply')",
            "input[type='submit']",
            "button.submit",
            "button.apply",
        ]

        for selector in submit_button_selectors:
            try:
                button = await self.page.wait_for_selector(selector, timeout=1000)
                if button:
                    await button.click()
                    self._log(f"Clicked submit button with selector: {selector}")

                    # Wait for submission to complete
                    await self.page.wait_for_load_state("networkidle")
                    self._log("Application submitted successfully")
                    return True
            except Exception as e:
                self._log(f"Error with submit button {selector}: {str(e)}", "debug")

        self._log("Could not find submit button", "warning")
        return False

    async def detect_job_board(self, url: str) -> str:
        """
        Detect which job board the URL belongs to.
        Returns the name of the job board.
        """
        domain = urlparse(url).netloc.lower()

        if "linkedin.com" in domain:
            return "linkedin"
        elif "indeed.com" in domain:
            return "indeed"
        elif "glassdoor.com" in domain:
            return "glassdoor"
        elif "monster.com" in domain:
            return "monster"
        elif "ziprecruiter.com" in domain:
            return "ziprecruiter"
        else:
            return "unknown"

    async def apply_to_job(self, job_url: str, resume_path: str, resume_data):
        """
        Apply to a job using the provided resume.
        """
        try:
            # Start the browser if not already started
            if not self.browser:
                await self.start()

            # Navigate to the job posting
            await self.navigate(job_url)

            # Detect job board
            job_board = await self.detect_job_board(job_url)
            self._log(f"Detected job board: {job_board}")

            # Find and click the apply button
            apply_button = await self.find_apply_button()
            if apply_button:
                await self.page.click(apply_button)
                self._log("Clicked apply button")

                # Wait for the application form to load
                await self.page.wait_for_load_state("networkidle")

                # Upload resume
                resume_uploaded = await self.upload_resume(resume_path)

                # Fill out the form
                await self.fill_form(resume_data)

                # Submit the application
                submitted = await self.submit_application()

                if submitted:
                    self._log("Job application completed successfully")
                    return True, self.logs
                else:
                    self._log("Failed to submit application", "error")
                    return False, self.logs
            else:
                self._log("Could not find apply button", "error")
                return False, self.logs

        except Exception as e:
            self._log(f"Error applying to job: {str(e)}", "error")
            return False, self.logs
        finally:
            # Close the browser
            await self.close()


# Example usage
async def apply_to_job_url(job_url: str, resume_path: str, resume_data):
    """
    Apply to a job at the given URL using the provided resume.
    """
    async with JobApplier(headless=False) as applier:
        success, logs = await applier.apply_to_job(job_url, resume_path, resume_data)
        return success, logs
