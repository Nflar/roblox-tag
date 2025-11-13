#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Start FastAPI server on port 8000
uvicorn main:app --host 0.0.0.0 --port 8000
