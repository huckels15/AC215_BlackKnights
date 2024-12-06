#!/bin/bash

# Start the backend and frontend services concurrently
concurrently \
    "cd /app/backend && nodemon server.js" \
    "cd /app/frontend && serve -s build -l 3000"
