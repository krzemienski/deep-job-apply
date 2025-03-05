#!/bin/bash

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo "tmux is not installed. Please install it to run this script."
    echo "On macOS: brew install tmux"
    echo "On Ubuntu/Debian: sudo apt-get install tmux"
    exit 1
fi

# Kill any existing tmux session with the same name
tmux kill-session -t deep-job-apply 2>/dev/null

# Create a new tmux session
tmux new-session -d -s deep-job-apply

# Split the window horizontally
tmux split-window -h -t deep-job-apply

# Run backend in the left pane
tmux send-keys -t deep-job-apply:0.0 "cd backend && echo 'Starting backend server...' && python -m venv venv 2>/dev/null || true && source venv/bin/activate && pip install -r requirements.txt && uvicorn main:app --reload" C-m

# Run frontend in the right pane
tmux send-keys -t deep-job-apply:0.1 "cd frontend && echo 'Starting frontend server...' && npm install && npm run dev" C-m

# Attach to the tmux session
tmux attach-session -t deep-job-apply

echo "Development servers started!"
echo "Backend running at: http://localhost:8000"
echo "Frontend running at: http://localhost:3000"
