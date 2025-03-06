#!/bin/bash
# Setup script for Deep Job Apply automation service

echo "Setting up Deep Job Apply Puppeteer automation service..."

# Navigate to the automation service directory
cd "$(dirname "$0")/automation-service"

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Start the service in the background
echo "Starting the automation service..."
npm start &

# Wait for service to start
echo "Waiting for service to start..."
sleep 5

# Check if service is running
echo "Checking if service is running..."
if curl -s http://localhost:3001/api/health | grep -q "healthy"; then
    echo "Automation service is running successfully!"
else
    echo "Error: Automation service failed to start."
    echo "Please check logs for more information."
    exit 1
fi

echo "Setup complete! The automation service is now ready to use."
echo "The service is running on http://localhost:3001"
echo ""
echo "To stop the service, run: pkill -f 'node.*server.js'"
