#!/bin/bash
# Start backend in background
cd /home/runner/workspace/backend
python run.py &
BACKEND_PID=$!

# Start frontend
cd /home/runner/workspace/frontend
npm run dev

# Cleanup on exit
trap "kill $BACKEND_PID" EXIT
