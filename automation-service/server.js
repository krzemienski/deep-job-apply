const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const winston = require('winston');
const path = require('path');
const fs = require('fs');
const { URL } = require('url');

// Set up logging
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'automation.log' })
  ]
});

// Add stealth plugin to puppeteer
puppeteer.use(StealthPlugin());

// Create Express app
const app = express();
app.use(cors());
app.use(bodyParser.json());

// Helper function to detect job board from URL
function detectJobBoard(url) {
  const hostname = new URL(url).hostname.toLowerCase();

  if (hostname.includes('linkedin')) return 'linkedin';
  if (hostname.includes('indeed')) return 'indeed';
  if (hostname.includes('glassdoor')) return 'glassdoor';
  if (hostname.includes('monster')) return 'monster';
  if (hostname.includes('ziprecruiter')) return 'ziprecruiter';
  if (hostname.includes('amazon.jobs')) return 'amazon';
  if (hostname.includes('careers.google.com')) return 'google';
  if (hostname.includes('metacareers')) return 'meta';
  if (hostname.includes('jobs.apple.com')) return 'apple';
  if (hostname.includes('netflix.wd1')) return 'netflix';
  if (hostname.includes('microsoft')) return 'microsoft';
  if (hostname.includes('nvidia')) return 'nvidia';
  if (hostname.includes('tiktok')) return 'tiktok';
  if (hostname.includes('disneycareers')) return 'disney';
  if (hostname.includes('mux.com')) return 'mux';
  if (hostname.includes('greenhouse.io')) return 'greenhouse';
  if (hostname.includes('wellfound.com')) return 'wellfound';
  if (hostname.includes('builtinnyc')) return 'builtin';
  return 'unknown';
}

// Utility function to wait random time to appear more human-like
async function randomWait(page, min = 1000, max = 3000) {
  const waitTime = Math.floor(Math.random() * (max - min) + min);
  await page.waitForTimeout(waitTime);
}

// Handle job application
async function applyToJob(jobUrl, resumePath, resumeData) {
  const logs = [];
  const logEntry = (message, level = 'info') => {
    const entry = { 
      timestamp: new Date().toISOString(), 
      message, 
      level 
    };
    logs.push(entry);
    logger.log(level, message);
    return entry;
  };

  logEntry(`Starting job application for ${jobUrl}`);
  
  // Check if resumePath exists
  try {
    if (!fs.existsSync(resumePath)) {
      logEntry(`Resume file not found at ${resumePath}`, 'error');
      // Try looking in the uploads directory (common Docker path)
      const altPath = path.join('/app/uploads', path.basename(resumePath));
      logEntry(`Trying alternative path: ${altPath}`);
      
      if (fs.existsSync(altPath)) {
        logEntry(`Found resume at alternative path: ${altPath}`);
        resumePath = altPath;
      } else {
        return { success: false, logs };
      }
    }
  } catch (error) {
    logEntry(`Error checking resume path: ${error.message}`, 'error');
  }
  
  let browser;
  try {
    // Launch browser with appropriate arguments for Docker
    const launchOptions = {
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--disable-gpu',
        '--window-size=1366,768'
      ],
      defaultViewport: { width: 1366, height: 768 }
    };
    
    // Check if running in Docker and use appropriate Chrome path
    if (process.env.PUPPETEER_EXECUTABLE_PATH) {
      logEntry(`Using Chrome at ${process.env.PUPPETEER_EXECUTABLE_PATH}`);
      launchOptions.executablePath = process.env.PUPPETEER_EXECUTABLE_PATH;
    }
    
    logEntry('Launching browser');
    browser = await puppeteer.launch(launchOptions);
    
    const page = await browser.newPage();
    
    // Set user agent to avoid detection
    await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36');
    
    // Enable console logging from the page
    page.on('console', msg => logEntry(`Browser console: ${msg.text()}`, 'debug'));
    
    logEntry(`Navigating to ${jobUrl}`);
    await page.goto(jobUrl, { waitUntil: 'networkidle2', timeout: 60000 });
    
    // Take screenshot for debugging
    const screenshotPath = path.join('/app', 'job-page.png');
    await page.screenshot({ path: screenshotPath });
    logEntry(`Saved screenshot to ${screenshotPath}`);
    
    // Detect which job board we're dealing with
    const jobBoard = detectJobBoard(jobUrl);
    logEntry(`Detected job board: ${jobBoard}`);
    
    // Apply job board specific strategies
    let success = false;
    switch (jobBoard) {
      case 'amazon':
        success = await applyAmazon(page, resumePath, resumeData, logEntry);
        break;
      case 'google':
        success = await applyGoogle(page, resumePath, resumeData, logEntry);
        break;
      case 'meta':
        success = await applyMeta(page, resumePath, resumeData, logEntry);
        break;
      case 'apple':
        success = await applyApple(page, resumePath, resumeData, logEntry);
        break;
      case 'netflix':
        success = await applyNetflix(page, resumePath, resumeData, logEntry);
        break;
      default:
        success = await applyGeneric(page, resumePath, resumeData, logEntry);
    }
    
    if (success) {
      logEntry('Successfully applied to job');
      return { success: true, logs };
    } else {
      logEntry('Failed to complete application process', 'error');
      return { success: false, logs };
    }
    
  } catch (error) {
    logEntry(`Error applying to job: ${error.message}`, 'error');
    return { success: false, logs };
  } finally {
    // Close browser
    if (browser) {
      await browser.close();
    }
  }
}

// Generic application strategy for unknown job sites
async function applyGeneric(page, resumePath, resumeData, logEntry) {
  try {
    logEntry('Using generic application strategy');
    
    // Look for apply button
    const applyButtonSelectors = [
      "button:has-text('Apply')",
      "a:has-text('Apply')",
      "button:has-text('Apply Now')",
      "a:has-text('Apply Now')",
      "button:has-text('Easy Apply')",
      "button:has-text('Quick Apply')",
      "[aria-label*='apply' i]",
      "[data-automation*='apply' i]"
    ];
    
    logEntry('Looking for apply button');
    let applyButton = null;
    for (const selector of applyButtonSelectors) {
      try {
        applyButton = await page.$(selector);
        if (applyButton) {
          logEntry(`Found apply button with selector: ${selector}`);
          break;
        }
      } catch (e) {
        // Continue to next selector
      }
    }
    
    if (!applyButton) {
      logEntry('Could not find apply button', 'warning');
      // Try to take a screenshot for debugging
      await page.screenshot({ path: '/app/no-apply-button.png' });
      return false;
    }
    
    // Click the apply button
    await applyButton.click();
    logEntry('Clicked apply button');
    
    // Wait for form to load
    await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 30000 }).catch(() => {
      logEntry('No navigation occurred after clicking apply', 'warning');
    });
    
    await randomWait(page);
    
    // Take screenshot after clicking apply
    await page.screenshot({ path: '/app/after-apply-click.png' });
    
    // Try to upload resume
    logEntry('Attempting to upload resume');
    const fileInputSelectors = [
      "input[type='file']",
      "input[accept='.pdf']",
      "input[accept='application/pdf']",
      "input[name*='resume' i]",
      "input[name*='cv' i]"
    ];
    
    let resumeUploaded = false;
    for (const selector of fileInputSelectors) {
      try {
        const fileInput = await page.$(selector);
        if (fileInput) {
          await fileInput.uploadFile(resumePath);
          logEntry(`Uploaded resume using selector: ${selector}`);
          resumeUploaded = true;
          break;
        }
      } catch (e) {
        logEntry(`Error uploading with selector ${selector}: ${e.message}`, 'debug');
      }
    }
    
    if (!resumeUploaded) {
      logEntry('Could not upload resume, attempting to proceed anyway', 'warning');
    }
    
    // Fill form fields
    logEntry('Filling out application form');
    const formFields = {
      "input[name*='name' i], input[placeholder*='name' i]": resumeData.name,
      "input[name*='email' i], input[placeholder*='email' i]": resumeData.contact_info?.email,
      "input[name*='phone' i], input[placeholder*='phone' i]": resumeData.contact_info?.phone || '',
      "textarea[name*='summary' i], textarea[placeholder*='summary' i], textarea[name*='about' i]": resumeData.summary
    };
    
    for (const [selector, value] of Object.entries(formFields)) {
      if (value) {
        try {
          const field = await page.$(selector);
          if (field) {
            await field.click();
            await field.type(value, { delay: 30 }); // Add delay to typing to appear more human-like
            logEntry(`Filled field ${selector}`);
          }
        } catch (e) {
          logEntry(`Error filling field ${selector}: ${e.message}`, 'warning');
        }
      }
    }
    
    // Submit the application
    logEntry('Attempting to submit application');
    const submitButtonSelectors = [
      "button[type='submit']",
      "button:has-text('Submit')",
      "button:has-text('Apply')",
      "input[type='submit']",
      "button.submit",
      "button.apply"
    ];
    
    let submitted = false;
    for (const selector of submitButtonSelectors) {
      try {
        const submitButton = await page.$(selector);
        if (submitButton) {
          await submitButton.click();
          logEntry(`Clicked submit button with selector: ${selector}`);
          
          // Wait for submission to complete
          await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 30000 }).catch(() => {
            logEntry('No navigation occurred after submission', 'warning');
          });
          
          logEntry('Application submitted successfully');
          submitted = true;
          break;
        }
      } catch (e) {
        logEntry(`Error with submit button ${selector}: ${e.message}`, 'debug');
      }
    }
    
    if (!submitted) {
      logEntry('Could not find submit button', 'warning');
      return false;
    }
    
    // Take screenshot for confirmation
    await page.screenshot({ path: '/app/application-submitted.png' });
    return true;
    
  } catch (error) {
    logEntry(`Error in generic application process: ${error.message}`, 'error');
    return false;
  }
}

// Amazon specific job application strategy
async function applyAmazon(page, resumePath, resumeData, logEntry) {
  try {
    logEntry('Using Amazon-specific application strategy');
    
    // Check for sign-in or apply button
    const signInButton = await page.$('a:has-text("Sign in")');
    if (signInButton) {
      logEntry('Amazon requires sign-in before applying', 'warning');
      return false;
    }
    
    // Look for apply button
    const applyButton = await page.$('a.apply-button, a:has-text("Apply Now")');
    if (!applyButton) {
      logEntry('Could not find Amazon apply button', 'warning');
      return false;
    }
    
    await applyButton.click();
    logEntry('Clicked apply button');
    
    // Wait for form to load
    await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 30000 }).catch(() => {
      logEntry('No navigation occurred after clicking apply', 'warning');
    });
    
    // Follow the same logic as generic handler after this point
    return await applyGeneric(page, resumePath, resumeData, logEntry);
    
  } catch (error) {
    logEntry(`Error in Amazon application process: ${error.message}`, 'error');
    return false;
  }
}

// Google specific job application strategy
async function applyGoogle(page, resumePath, resumeData, logEntry) {
  try {
    logEntry('Using Google-specific application strategy');
    
    // Click apply button (Google careers usually has a clearly labeled apply button)
    const applyButton = await page.$('a:has-text("Apply"), button:has-text("Apply")');
    if (applyButton) {
      await applyButton.click();
      logEntry('Clicked apply button');
      
      // Google usually redirects to a new application page or system
      await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 30000 }).catch(() => {
        logEntry('No navigation occurred after clicking apply', 'warning');
      });
      
      // Follow generic strategy for the application form
      return await applyGeneric(page, resumePath, resumeData, logEntry);
    } else {
      logEntry('Could not find Google apply button', 'warning');
      return false;
    }
    
  } catch (error) {
    logEntry(`Error in Google application process: ${error.message}`, 'error');
    return false;
  }
}

// Meta specific job application strategy
async function applyMeta(page, resumePath, resumeData, logEntry) {
  // Similar implementation as other job board specific strategies
  logEntry('Using Meta-specific application strategy');
  return await applyGeneric(page, resumePath, resumeData, logEntry);
}

// Apple specific job application strategy 
async function applyApple(page, resumePath, resumeData, logEntry) {
  logEntry('Using Apple-specific application strategy');
  return await applyGeneric(page, resumePath, resumeData, logEntry);
}

// Netflix specific job application strategy
async function applyNetflix(page, resumePath, resumeData, logEntry) {
  logEntry('Using Netflix-specific application strategy');
  return await applyGeneric(page, resumePath, resumeData, logEntry);
}

// Define API endpoints
app.post('/api/apply', async (req, res) => {
  const { jobUrl, resumePath, resumeData } = req.body;
  
  if (!jobUrl || !resumePath || !resumeData) {
    return res.status(400).json({ error: 'Missing required parameters', logs: [] });
  }
  
  logger.info(`Received application request for job: ${jobUrl}`);
  logger.info(`Resume path: ${resumePath}`);
  
  try {
    const result = await applyToJob(jobUrl, resumePath, resumeData);
    res.json(result);
  } catch (error) {
    logger.error(`Error in /api/apply endpoint: ${error.message}`);
    res.status(500).json({ error: error.message, logs: [] });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// Start the server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  logger.info(`Automation service running on port ${PORT}`);
  console.log(`Automation service running on port ${PORT}`);
});

module.exports = { applyToJob };
